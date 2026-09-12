"""Generador de comandos ESC/POS y transportes hacia la impresora.

Sin dependencias externas salvo Pillow (solo para el logo). Se implementa
únicamente el subconjunto de ESC/POS que entiende cualquier impresora
térmica genérica de 58/80 mm: texto, alineación, negrita, tamaño, tabla de
caracteres, imagen raster (GS v 0), avance, corte y zumbador.

Transportes:
  ImpresoraBluetooth  - RFCOMM (Bluetooth clásico, perfil SPP) con el módulo
                        socket de Python; conecta por trabajo y reintenta.
  ImpresoraArchivo    - escribe los bytes a un archivo o dispositivo
                        (/dev/ruleta-impresora, el nodo usblp de la impresora
                        conectada por cable USB; también un archivo de pruebas).
  ImpresoraVista      - decodifica el flujo y lo muestra como texto en la
                        consola: para ver el boleto sin tener la impresora.
  ImpresoraMemoria    - guarda los trabajos en una lista (pruebas).
"""

from __future__ import annotations

import errno
import logging
import os
import select
import socket
import stat
import time
import unicodedata
from typing import Callable, Iterable

log = logging.getLogger(__name__)

ESC = b"\x1b"
GS = b"\x1d"
FS = b"\x1c"

CMD_INICIALIZAR = ESC + b"@"
CMD_CANCELAR_KANJI = FS + b"."          # las impresoras chinas arrancan en modo GB/Kanji
CMD_ALINEAR = {"izq": ESC + b"a\x00", "centro": ESC + b"a\x01", "der": ESC + b"a\x02"}
CMD_NEGRITA_ON = ESC + b"E\x01"
CMD_NEGRITA_OFF = ESC + b"E\x00"
CMD_FUENTE_A = ESC + b"M\x00"
CMD_FUENTE_B = ESC + b"M\x01"
CMD_ESPACIADO_DEFECTO = ESC + b"2"
CMD_CORTE_COMPLETO = GS + b"V\x00"
CMD_CORTE_PARCIAL = GS + b"V\x01"
CMD_CORTE_AVANCE = GS + b"V\x42\x00"    # GS V 66 0: avanza hasta la cuchilla y corta

ALINEACIONES = ("izq", "centro", "der")
MODOS_CORTE = ("auto", "parcial", "completo", "ninguno")

# Tablas de caracteres (ESC t n) comunes a Epson y a los clones chinos, con el
# códec de Python que las reproduce.
CODECS_TABLA = {0: "cp437", 2: "cp850", 3: "cp860", 16: "cp1252", 17: "cp866", 19: "cp858"}

# Estado en tiempo real: DLE EOT n. La respuesta es 1 byte con bits fijos
# (b0=0, b1=1, b4=1, b7=0) que sirven para validarla.
CMD_ESTADO_IMPRESORA = b"\x10\x04\x01"   # bit 3 = fuera de línea
CMD_ESTADO_PAPEL = b"\x10\x04\x04"       # bits 2-3 = poco papel, bits 5-6 = sin papel
_MASCARA_FIJA_ESTADO = 0x93
_VALOR_FIJO_ESTADO = 0x12
# Bits con significado dentro de esa respuesta. Están aquí una sola vez: los
# usan los dos transportes (Bluetooth y USB) y el diagnóstico.
BITS_SIN_PAPEL = 0x60
BITS_POCO_PAPEL = 0x0C
BIT_FUERA_DE_LINEA = 0x08
_MAX_BYTES_BASURA = 4                    # bytes sueltos que se descartan buscando un estado válido

# Errores de conexión en los que reintentar no sirve de nada.
_ERRNO_SIN_REINTENTO = {errno.EBUSY, errno.EACCES, errno.EPERM}


def soporte_bluetooth() -> bool:
    return hasattr(socket, "AF_BLUETOOTH") and hasattr(socket, "BTPROTO_RFCOMM")


def lineas_antes_corte_por_defecto(modo: str) -> int:
    """'auto' ya avanza hasta la cuchilla; los demás cortan donde está el papel."""
    return 1 if modo == "auto" else 5


class ErrorImpresora(Exception):
    """Error genérico de impresión."""


class ErrorConexion(ErrorImpresora):
    """No se pudo conectar: NO se envió ningún byte (seguro reintentar/revertir)."""


class ErrorEnvio(ErrorImpresora):
    """Falló a mitad del envío: parte del boleto pudo haberse impreso."""

    def __init__(self, mensaje: str, bytes_enviados: int):
        super().__init__(mensaje)
        self.bytes_enviados = bytes_enviados


# --------------------------------------------------------------------------- #
# Estado en tiempo real (DLE EOT), común a todos los transportes
# --------------------------------------------------------------------------- #

def es_estado_valido(byte: int) -> bool:
    """True si el byte cumple los bits fijos de una respuesta DLE EOT."""
    return (byte & _MASCARA_FIJA_ESTADO) == _VALOR_FIJO_ESTADO


def verificar_estado(leer: Callable[[bytes], int | None], quien: str) -> None:
    """Pregunta por el papel y por la línea; aborta si la impresora dice que no puede.

    `leer(comando)` manda un DLE EOT y devuelve el byte de estado, o None si la
    impresora no contesta. La política es la misma por Bluetooth y por USB, y no
    se cambia: si **no contesta** se imprime igual (no responder no es prueba de
    falla) y solo se lanza ErrorConexion —antes de mandar un solo byte del
    boleto— cuando contesta y dice «sin papel» o «fuera de línea». El papel se
    evalúa antes de mandar la segunda pregunta: sin papel ya no hay nada más que
    preguntar.
    """
    papel = leer(CMD_ESTADO_PAPEL)
    if papel is not None:
        if papel & BITS_SIN_PAPEL:
            raise ErrorConexion(f"la impresora {quien} no tiene papel")
        if papel & BITS_POCO_PAPEL:
            log.warning("La impresora %s reporta poco papel: cambia el rollo pronto", quien)
    estado = leer(CMD_ESTADO_IMPRESORA)
    if estado is not None and estado & BIT_FUERA_DE_LINEA:
        raise ErrorConexion(f"la impresora {quien} está fuera de línea (tapa abierta, sin papel o error)")
    if papel is None and estado is None:
        log.debug("La impresora %s no responde al estado en tiempo real; se imprime sin verificar", quien)


def es_dispositivo_caracteres(ruta: str, stat_fn: Callable = os.stat) -> bool:
    """True si la ruta es un dispositivo de caracteres (/dev/ruleta-impresora, /dev/usb/lp0).

    Con un archivo normal (o si la ruta no existe) devuelve False, y entonces
    nadie intenta preguntarle nada: un archivo no contesta.
    """
    try:
        return stat.S_ISCHR(stat_fn(ruta).st_mode)
    except OSError:
        return False


def _hay_algo_que_leer(f, timeout: float) -> bool:
    """Espera hasta `timeout` segundos a que el dispositivo tenga respuesta.

    Sin este límite, una lectura sobre `usblp` puede colgar el servicio para
    siempre, que sería mucho peor que la falla que se intenta detectar.
    """
    try:
        listos, _, _ = select.select([f], [], [], timeout)
    except (OSError, ValueError):   # descriptor cerrado, o un sistema sin select de archivos
        return False
    return bool(listos)


# --------------------------------------------------------------------------- #
# Codificación de texto
# --------------------------------------------------------------------------- #

_REEMPLAZOS = {
    "¿": "?", "¡": "!", "º": "o", "ª": "a", "€": "EUR", "“": '"', "”": '"',
    "‘": "'", "’": "'", "–": "-", "—": "-", "…": "...", "•": "*", " ": " ",
}


def transliterar(texto: str) -> str:
    """Quita acentos y signos que no existen en ASCII (ñ -> n, ¿ -> ?)."""
    salida = []
    for c in texto:
        if c in _REEMPLAZOS:
            salida.append(_REEMPLAZOS[c])
            continue
        descompuesto = unicodedata.normalize("NFKD", c)
        base = "".join(ch for ch in descompuesto if not unicodedata.combining(ch))
        salida.append(base if base.isascii() else "?")
    return "".join(salida)


def codificar(texto: str, codepage: str) -> bytes:
    """Codifica con la tabla de la impresora; lo que no exista se translitera."""
    salida = bytearray()
    for c in texto:
        try:
            salida += c.encode(codepage)
        except UnicodeEncodeError:
            salida += transliterar(c).encode(codepage, errors="replace")
    return bytes(salida)


# --------------------------------------------------------------------------- #
# Constructor de documentos
# --------------------------------------------------------------------------- #

class Documento:
    """Acumula bytes ESC/POS. Cada método devuelve self para encadenar."""

    def __init__(self, codepage: str = "cp858", codepage_n: int = 19,
                 chars_por_linea: int = 48, ancho_puntos: int = 576,
                 juego_internacional: int | None = 0, cancelar_modo_chino: bool = True):
        self.codepage = codepage
        self.codepage_n = codepage_n
        self.chars_por_linea = chars_por_linea
        self.ancho_puntos = ancho_puntos
        self.juego_internacional = juego_internacional
        self.cancelar_modo_chino = cancelar_modo_chino
        self._buf = bytearray()
        self._ancho = 1
        self._alto = 1

    # -- estado -------------------------------------------------------- #

    def bytes(self) -> bytes:
        return bytes(self._buf)

    def crudo(self, datos: bytes) -> "Documento":
        self._buf += datos
        return self

    @property
    def chars_linea_actual(self) -> int:
        """Caracteres que caben en una línea con el tamaño de letra actual."""
        return max(1, self.chars_por_linea // self._ancho)

    # -- comandos -------------------------------------------------------- #

    def inicializar(self) -> "Documento":
        """Prólogo de cada trabajo, en este orden:

        ESC @   reinicia la impresora (y borra basura del enlace recién abierto)
        FS .    cancela el modo de caracteres chinos (si no, los bytes >= 0x80
                se emparejan como ideogramas y los acentos salen en chino)
        ESC R n juego internacional 0 = USA (el defecto de fábrica chino es 15
                y remapea signos ASCII)
        ESC t n tabla de caracteres (ESC @ la había reiniciado)
        """
        self._buf += CMD_INICIALIZAR
        if self.cancelar_modo_chino:
            self._buf += CMD_CANCELAR_KANJI
        if self.juego_internacional is not None:
            self._buf += ESC + b"R" + bytes([self.juego_internacional])
        self._buf += ESC + b"t" + bytes([self.codepage_n])
        self._ancho = self._alto = 1
        return self

    def alinear(self, donde: str) -> "Documento":
        if donde not in CMD_ALINEAR:
            raise ValueError(f"alineación inválida: {donde}")
        self._buf += CMD_ALINEAR[donde]
        return self

    def negrita(self, activa: bool = True) -> "Documento":
        self._buf += CMD_NEGRITA_ON if activa else CMD_NEGRITA_OFF
        return self

    def fuente(self, cual: str = "A") -> "Documento":
        self._buf += CMD_FUENTE_A if cual.upper() == "A" else CMD_FUENTE_B
        return self

    def tamano(self, ancho: int = 1, alto: int | None = None) -> "Documento":
        """GS ! n: multiplicadores de 1 a 8 (nibble alto = ancho, bajo = alto)."""
        if alto is None:
            alto = ancho
        if not (1 <= ancho <= 8 and 1 <= alto <= 8):
            raise ValueError("tamaño fuera de rango (1-8)")
        self._ancho, self._alto = ancho, alto
        self._buf += GS + b"!" + bytes([((ancho - 1) << 4) | (alto - 1)])
        return self

    def texto(self, texto: str) -> "Documento":
        self._buf += codificar(texto, self.codepage)
        return self

    def linea(self, texto: str = "") -> "Documento":
        self._buf += codificar(texto, self.codepage) + b"\n"
        return self

    def lineas(self, textos) -> "Documento":
        for t in textos:
            self.linea(t)
        return self

    def separador(self, caracter: str = "-") -> "Documento":
        return self.linea(caracter * self.chars_linea_actual)

    def alimentar(self, lineas: int = 1) -> "Documento":
        """ESC d n: imprime lo pendiente y avanza n líneas."""
        while lineas > 0:
            paso = min(lineas, 255)
            self._buf += ESC + b"d" + bytes([paso])
            lineas -= paso
        return self

    def cortar(self, modo: str = "auto", lineas_antes: int | None = None) -> "Documento":
        """Avanza el papel y corta.

        auto      GS V 66 0: la impresora avanza hasta su cuchilla y corta (lo
                  más confiable en esta familia; deja una pestaña, es normal).
        parcial   GS V 1 tras avanzar `lineas_antes` líneas.
        completo  GS V 0 tras avanzar (en muchas impresoras chinas es igual al parcial).
        ninguno   solo avanza (impresora sin cortador).
        """
        if modo not in MODOS_CORTE:
            raise ValueError(f"modo de corte inválido: {modo}")
        if lineas_antes is None:
            lineas_antes = lineas_antes_corte_por_defecto(modo)
        if lineas_antes:
            self.alimentar(lineas_antes)
        if modo == "auto":
            self._buf += CMD_CORTE_AVANCE
        elif modo == "parcial":
            self._buf += CMD_CORTE_PARCIAL
        elif modo == "completo":
            self._buf += CMD_CORTE_COMPLETO
        return self

    def beep(self, veces: int = 2, duracion: int = 2) -> "Documento":
        """ESC B n t: n pitidos (1-9) de t unidades (1-9, ~50-100 ms cada una).

        Solo suena si la impresora tiene zumbador y su interruptor DIP lo habilita.
        """
        self._buf += ESC + b"B" + bytes([max(1, min(veces, 9)), max(1, min(duracion, 9))])
        return self

    # -- imagen ---------------------------------------------------------- #

    def imagen(self, img, ancho_max: int | None = None, tramado: bool = False,
               banda: int = 64) -> "Documento":
        """Imprime una imagen PIL con GS v 0, en bandas de `banda` filas.

        Las bandas evitan comandos gigantes que desbordan el búfer de las
        impresoras Bluetooth baratas y salen como basura.
        """
        for comando in raster_gs_v0(img, ancho_max or self.ancho_puntos, tramado, banda):
            self._buf += comando
        return self


def preparar_imagen(img, ancho_max: int, tramado: bool = False):
    """Convierte cualquier imagen PIL a modo '1' con ancho múltiplo de 8.

    Fondo transparente -> blanco. Se reduce si es más ancha que ancho_max
    (nunca se agranda). El relleno a múltiplo de 8 es blanco, para que no
    aparezca una franja negra a la derecha.
    """
    from PIL import Image, ImageOps

    if img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info:
        # Canal alfa o color clave (chunk tRNS en PNG RGB/L/P): Pillow lo
        # respeta al convertir a RGBA; se aplana sobre blanco.
        rgba = img.convert("RGBA")
        fondo = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        img = Image.alpha_composite(fondo, rgba)
    if img.mode == "I" or img.mode.startswith("I;16"):
        # Gris de 16 bits: convert('L') recorta en vez de escalar y saldría en blanco.
        img = img.convert("I").point(lambda v: v / 256).convert("L")
    gris = img.convert("L")

    if gris.width > ancho_max:
        alto = max(1, round(gris.height * ancho_max / gris.width))
        gris = gris.resize((ancho_max, alto), Image.LANCZOS)

    ancho8 = (gris.width + 7) // 8 * 8
    if ancho8 != gris.width:
        gris = ImageOps.pad(gris, (ancho8, gris.height), color=255, centering=(0, 0))

    if tramado:
        return gris.convert("1")  # Floyd-Steinberg
    return gris.point(lambda v: 255 if v >= 128 else 0, mode="1")


def raster_gs_v0(img, ancho_max: int, tramado: bool = False, banda: int = 64):
    """Genera los comandos GS v 0 (uno por banda) para una imagen PIL."""
    bn = preparar_imagen(img, ancho_max, tramado)
    ancho, alto = bn.size
    bytes_por_fila = ancho // 8
    banda = max(1, min(int(banda), 255))
    for y0 in range(0, alto, banda):
        y1 = min(y0 + banda, alto)
        trozo = bn.crop((0, y0, ancho, y1))
        # En modo '1' Pillow empaqueta MSB primero con 1 = blanco; ESC/POS
        # quiere 1 = negro, así que se invierte cada byte.
        datos = bytes(b ^ 0xFF for b in trozo.tobytes())
        filas = y1 - y0
        yield (GS + b"v0\x00"
               + bytes([bytes_por_fila & 0xFF, bytes_por_fila >> 8, filas & 0xFF, filas >> 8])
               + datos)


# --------------------------------------------------------------------------- #
# Transportes
# --------------------------------------------------------------------------- #

class Impresora:
    """Interfaz común: imprimir(bytes) lanza ErrorConexion o ErrorEnvio."""

    nombre = "impresora"

    def imprimir(self, datos: bytes) -> None:
        raise NotImplementedError

    def probar(self) -> None:
        """Verifica que se puede llegar a la impresora; lanza ErrorConexion si no."""

    def cerrar(self) -> None:
        pass


class ImpresoraBluetooth(Impresora):
    nombre = "bluetooth"

    def __init__(self, mac: str, canal: int = 1, reintentos: int = 3,
                 espera_reintento: float = 2.0, timeout: float = 10.0,
                 tamano_bloque: int = 512, pausa_bloque: float = 0.03,
                 pausa_inicial: float = 0.4, pausa_final: float = 1.5,
                 bytes_por_segundo: int = 16000, consultar_estado: bool = True,
                 timeout_estado: float = 1.0,
                 dormir: Callable[[float], None] = time.sleep,
                 fabrica_socket: Callable[[], socket.socket] | None = None):
        self.mac = mac.upper()
        self.canal = canal
        self.reintentos = max(1, reintentos)
        self.espera_reintento = espera_reintento
        self.timeout = timeout
        self.tamano_bloque = tamano_bloque
        self.pausa_bloque = pausa_bloque
        self.pausa_inicial = pausa_inicial        # los módulos BT baratos pierden los primeros bytes
        self.pausa_final = pausa_final
        self.bytes_por_segundo = bytes_por_segundo  # ~16 KB/s drena un enlace SPP típico; 0 = no estimar
        self.consultar_estado = consultar_estado  # DLE EOT antes de imprimir: papel / fuera de línea
        self.timeout_estado = timeout_estado
        self.dormir = dormir
        self._fabrica = fabrica_socket or self._socket_rfcomm

    def _espera_drenado(self, n_bytes: int) -> float:
        """Tiempo a esperar antes de cerrar para que la impresora reciba todo."""
        estimado = n_bytes / self.bytes_por_segundo if self.bytes_por_segundo > 0 else 0.0
        return self.pausa_final + estimado

    @staticmethod
    def _socket_rfcomm() -> socket.socket:
        if not soporte_bluetooth():
            raise ErrorConexion("Este sistema no tiene soporte Bluetooth en el módulo socket (¿no es Linux?)")
        return socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    def _conectar(self, canal: int | None = None) -> socket.socket:
        sock = self._fabrica()
        try:
            # timeout 0 pondría el socket en modo no bloqueante: se trata como "sin límite".
            sock.settimeout(self.timeout if self.timeout and self.timeout > 0 else None)
            sock.connect((self.mac, self.canal if canal is None else canal))
        except Exception:
            self._cerrar(sock)
            raise
        return sock

    def _leer_estado(self, sock, comando: bytes) -> int | None:
        """Envía DLE EOT n y devuelve el byte de estado, o None si no responde."""
        try:
            sock.sendall(comando)
            sock.settimeout(self.timeout_estado)
            for _ in range(_MAX_BYTES_BASURA):   # descarta bytes sueltos que no sean un estado válido
                dato = sock.recv(1)
                if not dato:
                    return None
                if es_estado_valido(dato[0]):
                    return dato[0]
            return None
        except (socket.timeout, TimeoutError):
            return None
        finally:
            try:
                sock.settimeout(self.timeout if self.timeout and self.timeout > 0 else None)
            except OSError:
                pass

    def _verificar_lista(self, sock) -> None:
        """Lanza ErrorConexion si la impresora reporta sin papel o fuera de línea.

        La interpretación de los bits vive en `verificar_estado`, compartida con
        el transporte de archivo/USB: los números están escritos una sola vez.
        """
        verificar_estado(lambda comando: self._leer_estado(sock, comando), self.mac)

    @staticmethod
    def _cerrar(sock) -> None:
        for accion in (lambda: sock.shutdown(socket.SHUT_RDWR), sock.close):
            try:
                accion()
            except (OSError, AttributeError):
                pass

    def probar(self) -> None:
        try:
            sock = self._conectar()
        except OSError as e:
            raise ErrorConexion(_explicar_error_bt(e, self.mac)) from e
        self._cerrar(sock)

    def buscar_canal(self, canales: Iterable[int] = range(1, 31)) -> int | None:
        """Prueba canales RFCOMM hasta que uno acepte la conexión.

        'Connection refused' significa que nadie escucha en ese canal y se sigue
        con el siguiente; cualquier otro error (apagada, sin permiso...) se
        propaga como ErrorConexion porque probar más canales no ayudaría.
        """
        for canal in canales:
            try:
                sock = self._conectar(canal)
            except OSError as e:
                if getattr(e, "errno", None) == errno.ECONNREFUSED:
                    continue
                raise ErrorConexion(_explicar_error_bt(e, self.mac)) from e
            self._cerrar(sock)
            return canal
        return None

    def imprimir(self, datos: bytes) -> None:
        ultimo: Exception | None = None
        for intento in range(1, self.reintentos + 1):
            try:
                sock = self._conectar()
            except OSError as e:
                ultimo = e
                log.warning("Intento %d/%d: no se pudo conectar a %s: %s",
                            intento, self.reintentos, self.mac, _explicar_error_bt(e, self.mac))
                if getattr(e, "errno", None) in _ERRNO_SIN_REINTENTO:
                    break
                if intento < self.reintentos:
                    self.dormir(self.espera_reintento)
                continue

            enviados = 0
            try:
                if self.pausa_inicial:
                    self.dormir(self.pausa_inicial)
                if self.consultar_estado:
                    try:
                        self._verificar_lista(sock)
                    except OSError as e:
                        # El enlace falló durante la consulta: aún no se envió el boleto.
                        ultimo = e
                        log.warning("Intento %d/%d: falló la consulta de estado: %s", intento, self.reintentos, e)
                        if intento < self.reintentos:
                            self.dormir(self.espera_reintento)
                        continue
                for inicio in range(0, len(datos), self.tamano_bloque):
                    bloque = datos[inicio:inicio + self.tamano_bloque]
                    sock.sendall(bloque)
                    enviados += len(bloque)
                    if self.pausa_bloque:
                        self.dormir(self.pausa_bloque)
                espera = self._espera_drenado(len(datos))
                if espera > 0:
                    # RFCOMM puede descartar lo que quede en el búfer al cerrar.
                    self.dormir(espera)
                log.info("Impresos %d bytes en %s (intento %d)", enviados, self.mac, intento)
                return
            except OSError as e:
                if enviados == 0:
                    # Se conectó pero no aceptó ni un byte: tratar como conexión fallida.
                    ultimo = e
                    log.warning("Intento %d/%d: la impresora cerró antes de recibir datos: %s",
                                intento, self.reintentos, e)
                    if intento < self.reintentos:
                        self.dormir(self.espera_reintento)
                    continue
                raise ErrorEnvio(f"Se cortó la conexión tras enviar {enviados} de {len(datos)} bytes: {e}",
                                 enviados) from e
            finally:
                self._cerrar(sock)
        raise ErrorConexion(_explicar_error_bt(ultimo, self.mac) if ultimo else "sin detalle")


_EXPLICACIONES_ERRNO = {
    errno.EHOSTDOWN: "la impresora {mac} está apagada, fuera de alcance o dormida",
    errno.ECONNREFUSED: "la impresora {mac} rechazó la conexión: canal RFCOMM equivocado, ocupada por "
                        "otro dispositivo (¿un celular?) o no está emparejada",
    errno.EBUSY: "ya hay una conexión abierta a {mac} desde esta Raspberry (otro programa o 'rfcomm bind')",
    errno.EACCES: "fallo de autenticación con {mac}: vuelve a emparejar (bluetoothctl remove / pair / trust)",
    errno.EPERM: "sin permiso para usar Bluetooth",
    errno.ETIMEDOUT: "la impresora {mac} no respondió a tiempo",
    errno.ECONNRESET: "la impresora {mac} cerró la conexión",
    errno.EHOSTUNREACH: "no se encontró la impresora {mac}: ¿está emparejada y encendida?",
    errno.ENETDOWN: "el adaptador Bluetooth de la Raspberry está apagado (rfkill unblock bluetooth)",
}


def _explicar_error_bt(e: BaseException | None, mac: str) -> str:
    """Traduce los errores de RFCOMM a algo que el personal entienda."""
    if e is None:
        return "error desconocido"
    texto = str(e)
    num = getattr(e, "errno", None)
    if num in _EXPLICACIONES_ERRNO:
        return _EXPLICACIONES_ERRNO[num].format(mac=mac) + f" ({texto})"
    if isinstance(e, socket.timeout) or "timed out" in texto.lower():
        return f"la impresora {mac} no respondió a tiempo ({texto})"
    if isinstance(e, ErrorImpresora):
        return texto
    return texto or "error desconocido"


class ImpresoraArchivo(Impresora):
    """Escribe el trabajo a un archivo o dispositivo (p. ej. /dev/ruleta-impresora).

    Con `consultar_estado=True` y una ruta que sea un **dispositivo de
    caracteres** (el nodo `usblp` de una impresora USB bidireccional) pregunta
    por el papel antes de mandar el boleto, exactamente igual que el transporte
    Bluetooth. Con un archivo normal (`salida_impresora.bin`, las pruebas) no
    pregunta nada y el comportamiento es el de siempre, `anexar` incluido: un
    archivo no puede contestar.

    Solo un fallo al ABRIR es ErrorConexion (nada se envió). Un fallo a medio
    escribir es ErrorEnvio: el dispositivo pudo imprimir parte del boleto.
    """

    nombre = "archivo"

    def __init__(self, ruta: str, anexar: bool = False, abrir: Callable = open,
                 consultar_estado: bool = False, timeout_estado: float = 1.0,
                 es_dispositivo: Callable[[str], bool] | None = None,
                 esperar_lectura: Callable[..., bool] | None = None):
        self.ruta = ruta
        self.anexar = anexar
        self._abrir = abrir
        self.consultar_estado = consultar_estado   # DLE EOT antes del boleto: papel / fuera de línea
        self.timeout_estado = timeout_estado
        self._es_dispositivo = es_dispositivo or es_dispositivo_caracteres
        self._esperar = esperar_lectura or _hay_algo_que_leer

    def _leer_estado(self, f, comando: bytes) -> int | None:
        """Manda DLE EOT n y devuelve el byte de estado, o None si no contesta."""
        pendiente = memoryview(comando)
        while pendiente:
            n = f.write(pendiente)
            if not n:
                raise OSError(errno.EIO, f"{self.ruta} no aceptó la consulta de estado")
            pendiente = pendiente[n:]
        for _ in range(_MAX_BYTES_BASURA):   # descarta bytes sueltos que no sean un estado válido
            if not self._esperar(f, self.timeout_estado):
                return None
            dato = f.read(1)
            if not dato:
                return None
            if es_estado_valido(dato[0]):
                return dato[0]
        return None

    def consultar_papel(self) -> tuple[int | None, int | None]:
        """Devuelve (byte de papel, byte de estado); None en el que no conteste.

        No interpreta nada ni imprime: es lo que usa el diagnóstico para decir
        si la impresora contesta y qué contesta.
        """
        try:
            f = self._abrir(self.ruta, "r+b", buffering=0)
        except OSError as e:
            raise ErrorConexion(f"no se pudo abrir {self.ruta}: {e}") from e
        try:
            with f:
                return (self._leer_estado(f, CMD_ESTADO_PAPEL),
                        self._leer_estado(f, CMD_ESTADO_IMPRESORA))
        except OSError as e:
            raise ErrorConexion(f"falló la consulta de estado de {self.ruta}: {e}") from e

    def imprimir(self, datos: bytes) -> None:
        preguntar = self.consultar_estado and self._es_dispositivo(self.ruta)
        # "r+b" hace falta para poder LEER la respuesta ("ab" es solo de escritura)
        # y, de paso, no crea el archivo si la ruta no existe. Para todo lo demás
        # se conserva el modo de siempre.
        modo = "r+b" if preguntar else ("ab" if self.anexar else "wb")
        try:
            f = self._abrir(self.ruta, modo, buffering=0)
        except OSError as e:
            raise ErrorConexion(f"no se pudo abrir {self.ruta}: {e}") from e
        enviados = 0
        try:
            with f:
                if preguntar:
                    verificar_estado(lambda comando: self._leer_estado(f, comando), self.ruta)
                vista = memoryview(datos)
                while enviados < len(datos):
                    n = f.write(vista[enviados:])
                    if not n:
                        raise OSError(errno.EIO, "el dispositivo no aceptó más datos")
                    enviados += n
        except OSError as e:
            if enviados == 0:
                raise ErrorConexion(f"{self.ruta} no aceptó ningún byte: {e}") from e
            raise ErrorEnvio(f"fallo tras escribir {enviados} de {len(datos)} bytes en {self.ruta}: {e}",
                             enviados) from e


class ImpresoraMemoria(Impresora):
    """Doble de pruebas. `fallar` permite simular errores."""

    nombre = "memoria"

    def __init__(self):
        self.trabajos: list[bytes] = []
        self.fallar: Exception | None = None

    def imprimir(self, datos: bytes) -> None:
        if self.fallar is not None:
            raise self.fallar
        self.trabajos.append(datos)

    def probar(self) -> None:
        if isinstance(self.fallar, ErrorConexion):
            raise self.fallar


class ImpresoraVista(Impresora):
    """Muestra el boleto como texto en la consola (o en `salida`)."""

    nombre = "vista"

    def __init__(self, codepage: str = "cp850", chars_por_linea: int = 48,
                 salida: Callable[[str], None] = print):
        self.codepage = codepage
        self.chars_por_linea = chars_por_linea
        self.salida = salida
        self.ultimo = ""

    def imprimir(self, datos: bytes) -> None:
        self.ultimo = decodificar_vista(datos, self.codepage, self.chars_por_linea)
        self.salida(self.ultimo)


def decodificar_vista(datos: bytes, codepage: str = "cp850", ancho: int = 48) -> str:
    """Intérprete mínimo de ESC/POS para previsualizar en texto."""
    lineas: list[str] = []
    actual = bytearray()
    texto_linea = ""        # texto ya decodificado de la línea en curso (tras un cambio de tabla)
    codec = codepage
    alineacion = "izq"
    mult = 1
    negrita = False
    i = 0
    n = len(datos)

    def cerrar_linea():
        nonlocal actual, texto_linea
        texto = texto_linea + actual.decode(codec, errors="replace")
        actual = bytearray()
        texto_linea = ""
        ancho_linea = max(1, ancho // mult)
        if alineacion == "centro":
            texto = texto.center(ancho_linea)
        elif alineacion == "der":
            texto = texto.rjust(ancho_linea)
        # Cada carácter ocupa `mult` columnas en el papel: se representa
        # repitiendo cada carácter para que el ancho visual sea fiel.
        if mult > 1:
            texto = "".join(c * mult for c in texto)
        prefijo = ("*" if negrita else " ") + (f"{mult}x" if mult > 1 else "  ") + "|"
        lineas.append(prefijo + texto.rstrip() if texto.strip() else prefijo)

    while i < n:
        b = datos[i]
        if b == 0x0A:
            cerrar_linea()
            i += 1
        elif b == 0x1B and i + 1 < n:  # ESC
            c = datos[i + 1]
            if c == ord("@"):
                if actual or texto_linea:
                    cerrar_linea()
                alineacion, mult, negrita, codec = "izq", 1, False, codepage
                i += 2
            elif c == ord("a"):
                alineacion = ALINEACIONES[min(datos[i + 2], 2)] if i + 2 < n else "izq"
                i += 3
            elif c == ord("E"):
                negrita = bool(datos[i + 2] & 1) if i + 2 < n else False
                i += 3
            elif c == ord("d"):
                if actual:
                    cerrar_linea()
                lineas.extend(["   |"] * (datos[i + 2] if i + 2 < n else 1))
                i += 3
            elif c == ord("t"):
                # Cambio de tabla a media línea: lo ya acumulado se decodifica con la tabla anterior.
                texto_linea += actual.decode(codec, errors="replace")
                actual = bytearray()
                codec = CODECS_TABLA.get(datos[i + 2], codepage) if i + 2 < n else codepage
                i += 3
            elif c in (ord("R"), ord("M"), ord("J"), ord("3")):
                i += 3
            elif c == ord("B"):
                lineas.append("   |[BEEP]")
                i += 4
            elif c == ord("2"):
                i += 2
            else:
                i += 2
        elif b == 0x1C and i + 1 < n:  # FS (modo chino y afines): sin efecto visual
            c = datos[i + 1]
            if c in (ord("."), ord("&")):
                i += 2
            elif c in (ord("-"), ord("W"), ord("!"), ord("C")):
                i += 3
            elif c in (ord("S"), ord("p")):
                i += 4
            else:
                i += 2
        elif b == 0x1D and i + 1 < n:  # GS
            c = datos[i + 1]
            if c == ord("!"):
                if actual:
                    cerrar_linea()
                mult = ((datos[i + 2] >> 4) & 0x07) + 1 if i + 2 < n else 1
                i += 3
            elif c == ord("V"):
                if actual:
                    cerrar_linea()
                m = datos[i + 2] if i + 2 < n else 0
                if m in (65, 66) and i + 3 < n:
                    i += 4
                else:
                    i += 3
                lineas.append("   |" + "=" * ancho + " [CORTE]")
            elif c == ord("v") and i + 7 < n and datos[i + 2] == ord("0"):
                xl, xh, yl, yh = datos[i + 4], datos[i + 5], datos[i + 6], datos[i + 7]
                bpf = xl | (xh << 8)
                filas = yl | (yh << 8)
                if actual:
                    cerrar_linea()
                lineas.append(f"   |[IMAGEN {bpf * 8}x{filas} px]")
                i += 8 + bpf * filas
            else:
                i += 2
        else:
            actual.append(b)
            i += 1
    if actual or texto_linea:
        cerrar_linea()
    return "\n".join(lineas)
