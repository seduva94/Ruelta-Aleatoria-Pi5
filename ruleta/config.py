"""Carga y validación de config.json.

Todas las llaves del archivo están en español porque quien lo edita es el
personal del asadero, no un programador. Cualquier llave omitida toma el
valor por defecto indicado aquí.
"""

from __future__ import annotations

import json
import re
import types
import typing
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

_MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
_HORA_RE = re.compile(r"^([01][0-9]|2[0-3]):[0-5][0-9]$")

FUERA_DE_HORARIO = ("consuelo", "no_jugar")


class ErrorConfig(ValueError):
    """La configuración es inválida; el mensaje dice exactamente qué corregir."""


def minutos_del_dia(hora: str) -> int:
    """Minutos desde la medianoche de una hora "HH:MM" ya validada."""
    h, m = hora.split(":")
    return int(h) * 60 + int(m)


@dataclass(frozen=True)
class Franja:
    """Ventana de horas de un premio, con su propio tope (pieza B, Fase 4d).

    Decisión del usuario del 2026-09-16: la hielera solo de 19:00 a 23:00, y la
    silla y el set BBQ una pieza de 13:00 a 16:00 y otra de 19:00 a 22:00.
    """
    desde_hora: str                   # "HH:MM"
    hasta_hora: str                   # "HH:MM"
    # Piezas que esa franja ABRE ese día. NO es un máximo por franja: el
    # programa cuenta «abiertas hoy menos entregadas hoy», así que lo que una
    # franja abre y nadie gana se arrastra a la siguiente del mismo día (ficha
    # F-269). Lo único que corta el día es el 'tope_diario' del premio.
    tope: int = 1
    # Días operativos en los que esa franja existe (día 2 paso 2, decisión del
    # usuario del 2026-09-22: «horas sueltas y distintas por día»). Lista vacía
    # —o llave ausente— = TODOS los días, que es como se comportaba el programa
    # antes de este paso. Con días puestos, la franja no existe fuera de ellos.
    dias: list[date] = field(default_factory=list)


@dataclass(frozen=True)
class Premio:
    id: str
    nombre: str
    peso: float
    stock: int | None = None          # None = ilimitado
    tope_diario: int | None = None    # None = sin tope por día
    desde: date | None = None         # solo disponible a partir de esta fecha (día operativo)
    hasta: date | None = None         # solo disponible hasta esta fecha inclusive
    detalle: str = ""                 # texto chico debajo del premio en el boleto
    # Lista vacía = sin franjas, disponible a cualquier hora del día (como antes
    # de la Fase 4d). Con franjas, el premio SOLO existe dentro de ellas.
    franjas: list[Franja] = field(default_factory=list)
    # Premio FORZADO (día 2 paso 2, decisión del usuario del 2026-09-22:
    # «después de tal hora, el próximo juego se la saca»). Con `forzado` en true,
    # en cuanto el reloj abre una pieza de este premio la SIGUIENTE jugada se la
    # lleva: sin tómbola y sin esperar la separación mínima entre premios.
    # Mientras esté forzado, su `peso` no decide nada; se conserva porque es lo
    # que vale si alguien vuelve a poner `forzado` en false.
    forzado: bool = False


@dataclass(frozen=True)
class ConfigNegocio:
    nombre: str = "Asadero 33"
    logo: str | None = "logo.png"
    logo_ancho: int = 384             # píxeles; 576 es el ancho máximo de un rollo de 80 mm
    logo_tramado: bool = False        # False = umbral (logos nítidos); True = tramado (fotos)
    titulo_premio: str = "¡GANASTE!"
    pie: list[str] = field(default_factory=lambda: [
        "Presenta este boleto en caja",
        "para reclamar tu premio.",
        "Válido únicamente el día de hoy.",
    ])


@dataclass(frozen=True)
class ConfigImpresora:
    tipo: str = "bluetooth"           # bluetooth | archivo | vista
    mac: str = "00:00:00:00:00:00"
    canal: int = 1
    ruta: str = "salida_impresora.bin"  # solo para tipo=archivo
    ancho_puntos: int = 576
    chars_por_linea: int = 48
    codepage: str = "cp858"           # códec de Python con que se codifica el texto
    codepage_n: int = 19              # valor n de ESC t n que activa esa tabla en la impresora
    juego_internacional: int | None = 0     # ESC R n; 0 = USA evita que se remapeen signos ASCII
    cancelar_modo_chino: bool = True  # FS . tras ESC @; sin esto los acentos salen como ideogramas
    corte: str = "auto"               # auto | parcial | completo | ninguno
    lineas_antes_corte: int | None = None   # None = 1 con 'auto', 5 con los demás
    beep: bool = False
    consultar_estado: bool = True     # pregunta a la impresora si tiene papel antes de cada boleto
    reintentos: int = 3
    espera_reintento_seg: float = 2.0
    timeout_seg: float = 10.0
    tamano_bloque: int = 512          # bytes por envío (si sale basura: 256 y pausa 0.04)
    pausa_bloque_seg: float = 0.03
    pausa_inicial_seg: float = 0.4    # tras conectar, antes del primer byte
    pausa_final_seg: float = 1.5      # deja vaciar el búfer antes de cerrar la conexión
    bytes_por_segundo: int = 16000    # velocidad estimada del enlace para calcular el drenado (0 = no estimar)
    banda_imagen: int = 64            # filas de imagen por comando raster


@dataclass(frozen=True)
class ConfigGPIO:
    boton_jugar: int = 17
    boton_habilitar: int | None = 27
    led: int | None = 22
    modo_habilitar: str = "mantener"  # mantener | siempre
    pull_up: bool = True
    rebote_ms: int = 30
    # Segundos que el mesero mantiene HABILITAR (sin que nadie toque JUGAR) para
    # imprimir el inventario. None = gesto desactivado.
    pulsacion_larga_seg: float | None = 6.0


@dataclass(frozen=True)
class ConfigConsuelo:
    titulo: str = "SIGUE PARTICIPANDO"
    texto: str = "Por hoy se agotaron los premios. ¡Gracias por jugar!"
    # Papelitos del boleto de consuelo en la tómbola, igual que el 'peso' de un
    # premio. 0 = como antes de la Fase 4c: el consuelo solo sale cuando NINGÚN
    # premio está disponible. La regla del documento del evento (§2) es
    # peso = N - 33, con N = jugadas que se esperan en un día.
    peso: int = 0


@dataclass(frozen=True)
class ConfigHorario:
    """Horario del evento (pieza C, Fase 4d). Sin este bloque se juega todo el día."""
    abre: str = ""                    # "HH:MM"
    cierra: str = ""                  # "HH:MM", posterior a 'abre'
    # Qué pasa si alguien juega fuera del horario:
    #   "consuelo"  -> se imprime el boleto de consuelo (gasta folio). Lo que el
    #                  usuario decidió el 2026-09-16 para este evento.
    #   "no_jugar"  -> no se imprime nada y el log lo dice.
    fuera_de_horario: str = "consuelo"


@dataclass(frozen=True)
class ConfigJuego:
    espera_entre_jugadas_seg: float = 5.0
    hora_inicio_dia: int = 6          # a las 01:00 todavía cuenta como el día anterior
    imprimir_inventario_al_arrancar: bool = True
    intentos_inventario_arranque: int = 3
    # Minutos que deben pasar entre dos boletos CON PREMIO: decisión del usuario
    # del 2026-09-16, «los premios no deben salir seguidos». 0 = sin regla.
    separacion_min_entre_premios: float = 0.0
    # Segundos que el kiosco espera al arrancar a que la hora esté sincronizada
    # (pieza D). La Pi no lleva batería RTC y del reloj dependen los topes
    # diarios, las franjas y el reparto por horas. 0 = no esperar.
    espera_hora_seg: float = 0.0
    consuelo: ConfigConsuelo = field(default_factory=ConfigConsuelo)
    horario: ConfigHorario | None = None


@dataclass(frozen=True)
class Config:
    negocio: ConfigNegocio
    impresora: ConfigImpresora
    gpio: ConfigGPIO
    juego: ConfigJuego
    premios: list[Premio]
    carpeta_datos: Path
    ruta: Path | None = None          # de dónde se cargó, para resolver rutas relativas

    def ruta_logo(self) -> Path | None:
        if not self.negocio.logo:
            return None
        ruta = Path(self.negocio.logo)
        if not ruta.is_absolute() and self.ruta is not None:
            ruta = self.ruta.parent / ruta
        return ruta


# --------------------------------------------------------------------------- #
# Carga
# --------------------------------------------------------------------------- #

def cargar(ruta: str | Path) -> Config:
    ruta = Path(ruta)
    try:
        with open(ruta, encoding="utf-8") as f:
            crudo = json.load(f)
    except FileNotFoundError:
        raise ErrorConfig(f"No existe el archivo de configuración: {ruta}")
    except json.JSONDecodeError as e:
        raise ErrorConfig(f"config.json mal formado (línea {e.lineno}, columna {e.colno}): {e.msg}")
    cfg = desde_dict(crudo, ruta=ruta)
    return cfg


def desde_dict(crudo: dict[str, Any], ruta: Path | None = None) -> Config:
    if not isinstance(crudo, dict):
        raise ErrorConfig("La configuración debe ser un objeto JSON {...}")

    negocio = _construir(ConfigNegocio, crudo.get("negocio", {}), "negocio")
    impresora = _construir(ConfigImpresora, crudo.get("impresora", {}), "impresora")
    gpio = _construir(ConfigGPIO, crudo.get("gpio", {}), "gpio")

    juego_crudo = dict(crudo.get("juego", {}))
    consuelo = _construir(ConfigConsuelo, juego_crudo.pop("consuelo", {}), "juego.consuelo")
    # Sin la llave 'horario' no hay horario de evento: se juega todo el día, que
    # es como se comportaba el programa antes de la Fase 4d (2026-09-16).
    horario_crudo = juego_crudo.pop("horario", None)
    horario = None if horario_crudo is None else _construir(ConfigHorario, horario_crudo, "juego.horario")
    juego = _construir(ConfigJuego, juego_crudo, "juego", consuelo=consuelo, horario=horario)

    premios = [_premio(p, i) for i, p in enumerate(crudo.get("premios", []))]

    carpeta = Path(crudo.get("carpeta_datos", "datos"))
    if not carpeta.is_absolute() and ruta is not None:
        carpeta = ruta.parent / carpeta

    cfg = Config(negocio=negocio, impresora=impresora, gpio=gpio, juego=juego,
                 premios=premios, carpeta_datos=carpeta, ruta=ruta)
    validar(cfg)
    return cfg


def _construir(clase, datos: dict[str, Any], seccion: str, **extra):
    if not isinstance(datos, dict):
        raise ErrorConfig(f"La sección '{seccion}' debe ser un objeto {{...}}")
    permitidas = set(clase.__dataclass_fields__)
    desconocidas = set(datos) - permitidas
    if desconocidas:
        raise ErrorConfig(
            f"Llaves desconocidas en '{seccion}': {sorted(desconocidas)}. "
            f"Las válidas son: {sorted(permitidas)}")
    _verificar_tipos(clase, datos, seccion)
    try:
        return clase(**datos, **extra)
    except TypeError as e:
        raise ErrorConfig(f"Error en la sección '{seccion}': {e}")


def _premio(p: dict[str, Any], indice: int) -> Premio:
    if not isinstance(p, dict):
        raise ErrorConfig(f"El premio #{indice + 1} debe ser un objeto {{...}}")
    permitidas = set(Premio.__dataclass_fields__)
    desconocidas = set(p) - permitidas
    if desconocidas:
        raise ErrorConfig(f"Llaves desconocidas en el premio #{indice + 1}: {sorted(desconocidas)}")
    faltan = {"id", "nombre", "peso"} - set(p)
    if faltan:
        raise ErrorConfig(f"Al premio #{indice + 1} le faltan las llaves {sorted(faltan)}")
    datos = dict(p)
    donde = f"premio #{indice + 1} ('{p.get('id')}')"
    for llave in ("desde", "hasta"):
        if datos.get(llave) is not None:
            if not isinstance(datos[llave], str):
                raise ErrorConfig(f"{donde}.{llave} debe ser una fecha entre comillas con formato \"AAAA-MM-DD\"")
            datos[llave] = _fecha(datos[llave], f"{donde}.{llave}")
    if "franjas" in datos:
        # Las franjas llegan como lista de objetos crudos: hay que convertirlas
        # ANTES de verificar tipos, igual que las fechas, porque la anotación de
        # Premio.franjas pide objetos Franja y no diccionarios.
        datos["franjas"] = _franjas(datos["franjas"], donde)
    _verificar_tipos(Premio, datos, donde)
    return Premio(**datos)


def _franjas(crudo: Any, donde: str) -> list[Franja]:
    forma = ('{ "desde_hora": "HH:MM", "hasta_hora": "HH:MM", "tope": 1, '
             '"dias": ["AAAA-MM-DD"] }')
    if not isinstance(crudo, list):
        raise ErrorConfig(f"{donde}.franjas debe ser una lista de franjas {forma}")
    salida = []
    for i, f in enumerate(crudo, start=1):
        if not isinstance(f, dict):
            raise ErrorConfig(f"La franja #{i} del {donde} debe ser un objeto {forma}")
        desconocidas = set(f) - set(Franja.__dataclass_fields__)
        if desconocidas:
            raise ErrorConfig(
                f"Llaves desconocidas en la franja #{i} del {donde}: {sorted(desconocidas)}. "
                f"Las válidas son: {sorted(Franja.__dataclass_fields__)}")
        faltan = {"desde_hora", "hasta_hora"} - set(f)
        if faltan:
            raise ErrorConfig(f"A la franja #{i} del {donde} le faltan las llaves {sorted(faltan)}")
        datos = dict(f)
        if "dias" in datos:
            # Las fechas se convierten ANTES de verificar tipos, igual que las de
            # 'desde'/'hasta' en _premio(): la anotación de Franja.dias pide
            # objetos `date` y en el JSON llegan como texto "AAAA-MM-DD".
            datos["dias"] = _dias(datos["dias"], f"la franja #{i} del {donde}")
        _verificar_tipos(Franja, datos, f"franja #{i} del {donde}")
        salida.append(Franja(**datos))
    return salida


def _dias(crudo: Any, donde: str) -> list[date]:
    """Los días operativos en que existe una franja (día 2 paso 2, 2026-09-22).

    Lista vacía = todos los días. El mensaje de error **nombra la llave**
    `dias`, porque quien edita `config.json` es el personal del asadero.
    """
    if not isinstance(crudo, list):
        raise ErrorConfig(
            f"En {donde}, 'dias' debe ser una lista de fechas entre comillas "
            f"[\"AAAA-MM-DD\", ...]; se encontró {crudo!r}. Quítala —o déjala vacía— "
            f"para que la franja valga todos los días")
    salida = []
    for i, valor in enumerate(crudo, start=1):
        if not isinstance(valor, str):
            raise ErrorConfig(
                f"En {donde}, 'dias' #{i} debe ser una fecha entre comillas con formato "
                f"\"AAAA-MM-DD\"; se encontró {valor!r}")
        salida.append(_fecha(valor, f"'dias' #{i} de {donde}"))
    return salida


# --------------------------------------------------------------------------- #
# Verificación de tipos (el JSON lo edita gente, no programas)
# --------------------------------------------------------------------------- #

_NOMBRES_TIPO = {int: "un número entero (sin comillas)", float: "un número (sin comillas)",
                 str: "texto entre comillas", bool: "true o false (sin comillas)",
                 list: "una lista [...]", type(None): "null", date: "una fecha \"AAAA-MM-DD\""}


def _tipo_ok(valor: Any, anotacion: Any) -> bool:
    origen = typing.get_origin(anotacion)
    if origen is typing.Union or origen is types.UnionType:
        return any(_tipo_ok(valor, a) for a in typing.get_args(anotacion))
    if anotacion is type(None):
        return valor is None
    if anotacion is bool:
        return isinstance(valor, bool)
    if anotacion is int:
        return isinstance(valor, int) and not isinstance(valor, bool)
    if anotacion is float:
        return isinstance(valor, (int, float)) and not isinstance(valor, bool)
    if origen is list:
        (sub,) = typing.get_args(anotacion) or (typing.Any,)
        return isinstance(valor, list) and all(sub is typing.Any or _tipo_ok(v, sub) for v in valor)
    if isinstance(anotacion, type):
        return isinstance(valor, anotacion)
    return True


def _describir_tipo(anotacion: Any) -> str:
    origen = typing.get_origin(anotacion)
    if origen is typing.Union or origen is types.UnionType:
        return " o ".join(_describir_tipo(a) for a in typing.get_args(anotacion))
    if origen is list:
        (sub,) = typing.get_args(anotacion) or (typing.Any,)
        return f"una lista de {_describir_tipo(sub)}"
    return _NOMBRES_TIPO.get(anotacion, str(anotacion))


def _verificar_tipos(clase, datos: dict[str, Any], seccion: str) -> None:
    tipos = typing.get_type_hints(clase)
    for llave, valor in datos.items():
        anotacion = tipos.get(llave)
        if anotacion is None or _tipo_ok(valor, anotacion):
            continue
        raise ErrorConfig(
            f"{seccion}.{llave} debe ser {_describir_tipo(anotacion)}; se encontró {valor!r}")


def _fecha(valor: Any, donde: str) -> date:
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor))
    except ValueError:
        raise ErrorConfig(f"Fecha inválida en {donde}: '{valor}'. Usa el formato AAAA-MM-DD")


def _verificar_hora(valor: Any, donde: str) -> None:
    """Una hora del reloj de 24 horas, entre comillas y con formato HH:MM."""
    if not isinstance(valor, str) or not _HORA_RE.match(valor):
        raise ErrorConfig(
            f"Hora inválida en {donde}: {valor!r}. Debe ir entre comillas y con formato "
            "\"HH:MM\" en reloj de 24 horas (por ejemplo \"12:00\" o \"23:00\")")


# --------------------------------------------------------------------------- #
# Validación
# --------------------------------------------------------------------------- #

def validar(cfg: Config) -> None:
    imp = cfg.impresora
    if imp.tipo not in ("bluetooth", "archivo", "vista"):
        raise ErrorConfig("impresora.tipo debe ser 'bluetooth', 'archivo' o 'vista'")
    if imp.tipo == "bluetooth" and not _MAC_RE.match(imp.mac):
        raise ErrorConfig(
            f"impresora.mac inválida: '{imp.mac}'. Debe verse como 'AA:BB:CC:DD:EE:FF' "
            "(la obtienes con herramientas/emparejar.sh)")
    if not 1 <= imp.canal <= 30:
        raise ErrorConfig("impresora.canal debe estar entre 1 y 30 (normalmente 1)")
    if imp.ancho_puntos % 8 != 0 or imp.ancho_puntos <= 0:
        raise ErrorConfig("impresora.ancho_puntos debe ser múltiplo de 8 (576 para 80 mm, 384 para 58 mm)")
    if imp.chars_por_linea < 32:
        raise ErrorConfig("impresora.chars_por_linea debe ser al menos 32 (48 para 80 mm, 42 con el DIP 5, 32 para 58 mm)")
    if imp.timeout_seg <= 0:
        raise ErrorConfig("impresora.timeout_seg debe ser mayor que 0 (segundos que se espera la conexión)")
    if not 8 <= cfg.negocio.logo_ancho <= imp.ancho_puntos:
        raise ErrorConfig(f"negocio.logo_ancho debe estar entre 8 y {imp.ancho_puntos} píxeles")
    if not 0 <= imp.codepage_n <= 255:
        raise ErrorConfig("impresora.codepage_n debe estar entre 0 y 255")
    try:
        "ñ".encode(imp.codepage)
    except LookupError:
        raise ErrorConfig(f"impresora.codepage desconocido para Python: '{imp.codepage}' (usa cp850, cp858, cp437, cp1252...)")
    if imp.corte not in ("auto", "parcial", "completo", "ninguno"):
        raise ErrorConfig("impresora.corte debe ser 'auto', 'parcial', 'completo' o 'ninguno'")
    if imp.lineas_antes_corte is not None and not 0 <= imp.lineas_antes_corte <= 20:
        raise ErrorConfig("impresora.lineas_antes_corte debe estar entre 0 y 20 (o null)")
    if imp.juego_internacional is not None and not 0 <= imp.juego_internacional <= 255:
        raise ErrorConfig("impresora.juego_internacional debe estar entre 0 y 255 (o null para no enviarlo)")
    if imp.reintentos < 1:
        raise ErrorConfig("impresora.reintentos debe ser al menos 1")
    if not 1 <= imp.banda_imagen <= 255:
        raise ErrorConfig("impresora.banda_imagen debe estar entre 1 y 255")
    if imp.tamano_bloque < 16:
        raise ErrorConfig("impresora.tamano_bloque debe ser al menos 16")
    for nombre in ("pausa_bloque_seg", "pausa_inicial_seg", "pausa_final_seg", "espera_reintento_seg"):
        if getattr(imp, nombre) < 0:
            raise ErrorConfig(f"impresora.{nombre} no puede ser negativa")
    if imp.bytes_por_segundo < 0:
        raise ErrorConfig("impresora.bytes_por_segundo no puede ser negativo")

    g = cfg.gpio
    if g.modo_habilitar not in ("mantener", "siempre"):
        raise ErrorConfig("gpio.modo_habilitar debe ser 'mantener' o 'siempre'")
    if g.modo_habilitar == "mantener" and g.boton_habilitar is None:
        raise ErrorConfig("gpio.modo_habilitar='mantener' requiere gpio.boton_habilitar (o usa 'siempre')")
    pines = [("boton_jugar", g.boton_jugar), ("boton_habilitar", g.boton_habilitar), ("led", g.led)]
    usados: dict[int, str] = {}
    for nombre, pin in pines:
        if pin is None:
            continue
        if not isinstance(pin, int) or not 0 <= pin <= 27:
            raise ErrorConfig(f"gpio.{nombre}={pin!r} no es un número GPIO válido (0-27, numeración BCM)")
        if pin in usados:
            raise ErrorConfig(f"gpio.{nombre} y gpio.{usados[pin]} usan el mismo pin {pin}")
        usados[pin] = nombre
    if g.pulsacion_larga_seg is not None and g.pulsacion_larga_seg < 1.0:
        raise ErrorConfig("gpio.pulsacion_larga_seg debe ser al menos 1 segundo, o null para desactivar el gesto")
    if g.rebote_ms < 0 or g.rebote_ms > 500:
        raise ErrorConfig("gpio.rebote_ms debe estar entre 0 y 500")

    j = cfg.juego
    if not 0 <= j.hora_inicio_dia <= 23:
        raise ErrorConfig("juego.hora_inicio_dia debe estar entre 0 y 23")
    if j.espera_entre_jugadas_seg < 0:
        raise ErrorConfig("juego.espera_entre_jugadas_seg no puede ser negativa")
    if j.intentos_inventario_arranque < 1:
        raise ErrorConfig("juego.intentos_inventario_arranque debe ser al menos 1")
    if j.consuelo.peso < 0:
        raise ErrorConfig(
            f"juego.consuelo.peso no puede ser negativo (se encontró {j.consuelo.peso}): son los "
            "papelitos del boleto de consuelo en la tómbola. 0 = el consuelo solo sale cuando ya "
            "no queda ningún premio disponible")
    if j.separacion_min_entre_premios < 0:
        raise ErrorConfig(
            "juego.separacion_min_entre_premios no puede ser negativa: son los minutos que tienen "
            "que pasar entre dos boletos con premio. 0 = sin esa regla")
    if j.espera_hora_seg < 0:
        raise ErrorConfig(
            "juego.espera_hora_seg no puede ser negativa: son los segundos que el kiosco espera al "
            "arrancar a que la hora esté sincronizada. 0 = no esperar")
    if j.horario is not None:
        _verificar_hora(j.horario.abre, "juego.horario.abre")
        _verificar_hora(j.horario.cierra, "juego.horario.cierra")
        if minutos_del_dia(j.horario.abre) >= minutos_del_dia(j.horario.cierra):
            raise ErrorConfig(
                f"juego.horario: la hora de apertura ('{j.horario.abre}') tiene que ser anterior "
                f"a la de cierre ('{j.horario.cierra}')")
        if j.horario.fuera_de_horario not in FUERA_DE_HORARIO:
            raise ErrorConfig(
                f"juego.horario.fuera_de_horario debe ser 'consuelo' (imprime el boleto de "
                f"consuelo) o 'no_jugar' (no imprime nada); se encontró "
                f"'{j.horario.fuera_de_horario}'")
    if not cfg.negocio.nombre.strip():
        raise ErrorConfig("negocio.nombre no puede estar vacío")

    if not cfg.premios:
        raise ErrorConfig("Debes definir al menos un premio en 'premios'")
    ids: set[str] = set()
    for p in cfg.premios:
        if not p.id or not re.match(r"^[A-Za-z0-9_-]+$", p.id):
            raise ErrorConfig(f"El id de premio '{p.id}' solo puede tener letras, números, guion y guion bajo")
        if p.id in ids:
            raise ErrorConfig(f"Hay dos premios con el mismo id '{p.id}'")
        ids.add(p.id)
        if not p.nombre.strip():
            raise ErrorConfig(f"El premio '{p.id}' no tiene nombre")
        if not isinstance(p.peso, (int, float)) or p.peso <= 0:
            raise ErrorConfig(f"El peso del premio '{p.id}' debe ser un número mayor que 0")
        if p.stock is not None and (not isinstance(p.stock, int) or p.stock < 0):
            raise ErrorConfig(f"El stock del premio '{p.id}' debe ser un entero ≥ 0 o null (ilimitado)")
        if p.tope_diario is not None and (not isinstance(p.tope_diario, int) or p.tope_diario < 1):
            raise ErrorConfig(f"El tope_diario del premio '{p.id}' debe ser un entero ≥ 1 o null")
        if p.desde and p.hasta and p.desde > p.hasta:
            raise ErrorConfig(f"El premio '{p.id}' tiene 'desde' posterior a 'hasta'")
        for i, f in enumerate(p.franjas, start=1):
            donde = f"la franja #{i} del premio '{p.id}'"
            _verificar_hora(f.desde_hora, f"{donde} ('desde_hora')")
            _verificar_hora(f.hasta_hora, f"{donde} ('hasta_hora')")
            if minutos_del_dia(f.desde_hora) >= minutos_del_dia(f.hasta_hora):
                raise ErrorConfig(
                    f"En {donde}, 'desde_hora' ('{f.desde_hora}') tiene que ser anterior a "
                    f"'hasta_hora' ('{f.hasta_hora}')")
            if not isinstance(f.tope, int) or isinstance(f.tope, bool) or f.tope < 1:
                raise ErrorConfig(
                    f"El 'tope' de {donde} debe ser un entero ≥ 1: son las piezas que esa "
                    f"franja ABRE ese día, no un máximo por franja (lo que corta el día es el "
                    f"'tope_diario' del premio); se encontró {f.tope!r}")
