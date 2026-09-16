import contextlib
import errno
import io
import logging
import os
import socket
import stat
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from PIL import Image

from ruleta import escpos
from ruleta.escpos import (Documento, ErrorConexion, ErrorEnvio, ImpresoraArchivo, ImpresoraBluetooth,
                           codificar, decodificar_vista, raster_gs_v0, transliterar)

# Las tres preguntas de estado, en el orden en que las manda verificar_estado.
COMANDOS_ESTADO = (escpos.CMD_ESTADO_PAPEL, escpos.CMD_ESTADO_CAUSA, escpos.CMD_ESTADO_IMPRESORA)
# Vectores MEDIDOS en la AOMU My-A1 el 2026-09-15 con la lectura fresca: con
# papel contesta 0x12 a DLE EOT 4, 0x12 a DLE EOT 2 y 0x16 a DLE EOT 1 (el bit 2
# es el pin 3 del cajón, no un aviso de nada). Sin papel y con la tapa cerrada,
# lo ÚNICO que cambia es DLE EOT 2, que pasa a 0x32.
ESTADOS_CON_PAPEL = {escpos.CMD_ESTADO_PAPEL: b"\x12", escpos.CMD_ESTADO_CAUSA: b"\x12",
                     escpos.CMD_ESTADO_IMPRESORA: b"\x16"}
FLUJO_CON_PAPEL = {escpos.CMD_ESTADO_PAPEL: 0x12, escpos.CMD_ESTADO_CAUSA: 0x12,
                   escpos.CMD_ESTADO_IMPRESORA: 0x16}
AVISO_POCO_PAPEL = "reporta poco papel: cambia el rollo pronto"


@contextlib.contextmanager
def registro_activo():
    """Vuelve a encender el registro mientras dura el bloque.

    `tests/__init__.py` hace `logging.disable(logging.CRITICAL)` para que las
    pruebas que provocan errores a propósito no ensucien la salida, y con eso
    puesto `assertLogs` y `assertNoLogs` no ven absolutamente nada: los dos
    pasarían (o fallarían) por el motivo equivocado. Se enciende solo aquí y se
    vuelve a apagar al salir, pase lo que pase.
    """
    logging.disable(logging.NOTSET)
    try:
        yield
    finally:
        logging.disable(logging.CRITICAL)


def con_papel(cambios=None):
    """Los tres bytes de una impresora sana, con los que se quieran cambiados."""
    return {**ESTADOS_CON_PAPEL, **(cambios or {})}


def flujo_con_papel(cambios=None):
    """Lo mismo para el doble de flujo, que repite un byte (int) por pregunta."""
    return {**FLUJO_CON_PAPEL, **(cambios or {})}


class TestCodificacion(unittest.TestCase):
    def test_cp850_tiene_todo_el_espanol(self):
        self.assertEqual(codificar("ñ", "cp850"), b"\xa4")
        self.assertEqual(codificar("Á", "cp850"), b"\xb5")
        self.assertEqual(codificar("¿¡", "cp850"), b"\xa8\xad")

    def test_cp437_translitera_lo_que_no_existe(self):
        # cp437 no tiene Á/Í/Ó/Ú mayúsculas: deben salir sin acento, no como '?'
        self.assertEqual(codificar("ÁREA", "cp437"), b"AREA")
        self.assertEqual(codificar("ñ", "cp437"), b"\xa4")

    def test_simbolos_raros(self):
        self.assertEqual(transliterar("¿Qué? — 5€ “ok”"), '?Que? - 5EUR "ok"')
        self.assertEqual(codificar("€", "cp437"), b"EUR")
        self.assertEqual(codificar("€", "cp858"), b"\xd5")

    def test_ascii_puro_no_cambia(self):
        texto = "ASADERO 33 - BOLETO 00042"
        self.assertEqual(codificar(texto, "cp850"), texto.encode("ascii"))


class TestDocumento(unittest.TestCase):
    def test_inicializar_prologo_completo(self):
        # ESC @, FS . (cancela modo chino), ESC R 0, ESC t 19
        doc = Documento().inicializar()
        self.assertEqual(doc.bytes(), b"\x1b@\x1c.\x1bR\x00\x1bt\x13")

    def test_inicializar_reactiva_tabla_configurada(self):
        doc = Documento(codepage="cp850", codepage_n=2, juego_internacional=7).inicializar()
        self.assertEqual(doc.bytes(), b"\x1b@\x1c.\x1bR\x07\x1bt\x02")

    def test_inicializar_minimo(self):
        doc = Documento(codepage_n=19, juego_internacional=None, cancelar_modo_chino=False).inicializar()
        self.assertEqual(doc.bytes(), b"\x1b@\x1bt\x13")

    def test_inicializar_reinicia_tamano(self):
        doc = Documento().tamano(3).inicializar()
        self.assertEqual(doc.chars_linea_actual, 48)

    def test_tamano(self):
        self.assertEqual(Documento().tamano(1, 1).bytes(), b"\x1d!\x00")
        self.assertEqual(Documento().tamano(2, 2).bytes(), b"\x1d!\x11")
        self.assertEqual(Documento().tamano(3, 3).bytes(), b"\x1d!\x22")
        self.assertEqual(Documento().tamano(4, 4).bytes(), b"\x1d!\x33")
        self.assertEqual(Documento().tamano(2, 1).bytes(), b"\x1d!\x10")
        with self.assertRaises(ValueError):
            Documento().tamano(9)

    def test_chars_por_linea_segun_tamano(self):
        doc = Documento(chars_por_linea=48)
        self.assertEqual(doc.chars_linea_actual, 48)
        doc.tamano(3)
        self.assertEqual(doc.chars_linea_actual, 16)
        self.assertEqual(doc.separador("-").bytes()[-17:], b"-" * 16 + b"\n")

    def test_alinear_negrita_fuente(self):
        doc = Documento().alinear("centro").negrita(True).negrita(False).fuente("B").fuente("A")
        self.assertEqual(doc.bytes(), b"\x1ba\x01\x1bE\x01\x1bE\x00\x1bM\x01\x1bM\x00")
        with self.assertRaises(ValueError):
            Documento().alinear("arriba")

    def test_texto_y_linea(self):
        doc = Documento(codepage="cp850").texto("año ").linea("¡ok!")
        self.assertEqual(doc.bytes(), b"a\xa4o \xadok!\n")

    def test_alimentar_divide_en_bloques_de_255(self):
        self.assertEqual(Documento().alimentar(3).bytes(), b"\x1bd\x03")
        self.assertEqual(Documento().alimentar(300).bytes(), b"\x1bd\xff\x1bd\x2d")

    def test_cortar(self):
        self.assertEqual(Documento().cortar().bytes(), b"\x1bd\x01\x1dV\x42\x00")
        self.assertEqual(Documento().cortar("auto", 0).bytes(), b"\x1dV\x42\x00")
        self.assertEqual(Documento().cortar("parcial").bytes(), b"\x1bd\x05\x1dV\x01")
        self.assertEqual(Documento().cortar("parcial", 4).bytes(), b"\x1bd\x04\x1dV\x01")
        self.assertEqual(Documento().cortar("completo", 0).bytes(), b"\x1dV\x00")
        self.assertEqual(Documento().cortar("ninguno", 5).bytes(), b"\x1bd\x05")
        self.assertEqual(Documento().cortar("ninguno", 0).bytes(), b"")
        with self.assertRaises(ValueError):
            Documento().cortar("laser")

    def test_beep_acotado(self):
        self.assertEqual(Documento().beep(2, 3).bytes(), b"\x1bB\x02\x03")
        self.assertEqual(Documento().beep(50, 0).bytes(), b"\x1bB\x09\x01")


class TestRaster(unittest.TestCase):
    def imagen(self, pixeles, ancho, alto):
        img = Image.new("L", (ancho, alto), 255)
        for x, y in pixeles:
            img.putpixel((x, y), 0)
        return img

    def test_bits_y_encabezado(self):
        # Fila 0 toda negra; fila 1 mitad izquierda negra
        negros = [(x, 0) for x in range(16)] + [(x, 1) for x in range(8)]
        cmds = list(raster_gs_v0(self.imagen(negros, 16, 2), ancho_max=576))
        self.assertEqual(len(cmds), 1)
        self.assertEqual(cmds[0], b"\x1dv0\x00" + b"\x02\x00" + b"\x02\x00" + b"\xff\xff\xff\x00")

    def test_relleno_a_multiplo_de_8_es_blanco(self):
        # 12 px de ancho, toda negra: los 4 bits de relleno deben ser 0 (blanco)
        negros = [(x, 0) for x in range(12)]
        cmds = list(raster_gs_v0(self.imagen(negros, 12, 1), ancho_max=576))
        self.assertEqual(cmds[0][-2:], b"\xff\xf0")

    def test_reduce_si_es_mas_ancha(self):
        img = Image.new("L", (1152, 100), 0)
        cmds = list(raster_gs_v0(img, ancho_max=576, banda=255))
        bpf = cmds[0][4] | (cmds[0][5] << 8)
        filas = cmds[0][6] | (cmds[0][7] << 8)
        self.assertEqual(bpf, 72)   # 576 / 8
        self.assertEqual(filas, 50)
        self.assertEqual(len(cmds[0]), 8 + 72 * 50)

    def test_no_agranda_imagenes_chicas(self):
        img = Image.new("L", (100, 10), 0)
        cmds = list(raster_gs_v0(img, ancho_max=576, banda=255))
        self.assertEqual(cmds[0][4], 13)  # 104 px / 8

    def test_bandas(self):
        img = Image.new("L", (8, 100), 0)
        cmds = list(raster_gs_v0(img, ancho_max=576, banda=64))
        self.assertEqual(len(cmds), 2)
        self.assertEqual(cmds[0][6], 64)
        self.assertEqual(cmds[1][6], 36)
        self.assertEqual(len(cmds[1]), 8 + 36)

    def test_transparente_se_vuelve_blanco(self):
        img = Image.new("RGBA", (8, 1), (0, 0, 0, 0))
        cmds = list(raster_gs_v0(img, ancho_max=576))
        self.assertEqual(cmds[0][-1:], b"\x00")

    def test_transparencia_por_color_clave_png(self):
        # PNG RGB o L con chunk tRNS: el color clave (negro) debe salir blanco
        for modo, color in (("RGB", (0, 0, 0)), ("L", 0)):
            buf = io.BytesIO()
            Image.new(modo, (8, 1), color).save(buf, format="PNG", transparency=color)
            buf.seek(0)
            img = Image.open(buf)
            self.assertIn("transparency", img.info)
            self.assertEqual(list(raster_gs_v0(img, 576))[0][-1], 0x00, modo)

    def test_gris_de_16_bits(self):
        oscuro = Image.new("I;16", (8, 1), 13107)     # ~20 % de blanco -> negro
        self.assertEqual(list(raster_gs_v0(oscuro, 576))[0][-1], 0xFF)
        claro = Image.new("I;16", (8, 1), 60000)
        self.assertEqual(list(raster_gs_v0(claro, 576))[0][-1], 0x00)

    def test_umbral_vs_tramado(self):
        gris = Image.new("L", (8, 1), 200)   # claro -> blanco con umbral
        self.assertEqual(list(raster_gs_v0(gris, 576))[0][-1], 0x00)
        oscuro = Image.new("L", (8, 1), 60)
        self.assertEqual(list(raster_gs_v0(oscuro, 576))[0][-1], 0xFF)

    def test_documento_imagen(self):
        doc = Documento(ancho_puntos=576).imagen(Image.new("L", (8, 1), 0))
        self.assertTrue(doc.bytes().startswith(b"\x1dv0\x00"))


class SocketFalso:
    """Simula un socket RFCOMM. Los parámetros controlan cuándo explota."""

    def __init__(self, registro, fallar_conexion=False, fallar_envio_en=None,
                 errno_conexion=errno.EHOSTDOWN, canales_abiertos=None, estados=None):
        self.registro = registro
        self.fallar_conexion = fallar_conexion
        self.fallar_envio_en = fallar_envio_en
        self.errno_conexion = errno_conexion
        self.canales_abiertos = canales_abiertos
        # Respuestas a DLE EOT: dict {comando: bytes}; sin entrada -> la impresora no contesta
        self.estados = estados or {}
        self._cola = bytearray()
        self.enviado = bytearray()
        self.consultas = []
        self.cerrado = False
        self.envios = 0
        self.timeout = None

    def settimeout(self, t):
        self.timeout = t

    def recv(self, n):
        if not self._cola:
            raise socket.timeout("timed out")
        dato = bytes(self._cola[:n])
        del self._cola[:n]
        return dato

    def connect(self, destino):
        self.registro.append(("connect", destino))
        if self.fallar_conexion:
            raise OSError(self.errno_conexion, "error simulado")
        if self.canales_abiertos is not None and destino[1] not in self.canales_abiertos:
            raise OSError(errno.ECONNREFUSED, "Connection refused")

    def shutdown(self, como):
        self.registro.append(("shutdown",))

    def sendall(self, datos):
        if datos in COMANDOS_ESTADO:
            self.consultas.append(datos)
            self._cola += self.estados.get(datos, b"")
            return
        if self.fallar_envio_en is not None and self.envios == self.fallar_envio_en:
            raise OSError(errno.ECONNRESET, "Connection reset by peer")
        self.envios += 1
        self.enviado += datos

    def close(self):
        self.cerrado = True
        self.registro.append(("close",))


class TestImpresoraBluetooth(unittest.TestCase):
    def setUp(self):
        self.registro = []
        self.pausas = []
        self.sockets = []

    def fabrica(self, **kw):
        def crear():
            s = SocketFalso(self.registro, **kw)
            self.sockets.append(s)
            return s
        return crear

    def impresora(self, pausa_inicial=0.0, bytes_por_segundo=0, consultar_estado=False, **kw):
        return ImpresoraBluetooth("aa:bb:cc:dd:ee:ff", canal=1, reintentos=3, espera_reintento=2.0,
                                  tamano_bloque=4, pausa_bloque=0.01, pausa_inicial=pausa_inicial,
                                  pausa_final=0.5, bytes_por_segundo=bytes_por_segundo,
                                  consultar_estado=consultar_estado,
                                  dormir=self.pausas.append, fabrica_socket=self.fabrica(**kw))

    # -- estado en tiempo real (papel / fuera de línea) -------------------------- #

    def test_sin_papel_no_envia_el_boleto(self):
        imp = self.impresora(consultar_estado=True, estados={escpos.CMD_ESTADO_PAPEL: b"\x72"})  # 0x12 | 0x60
        with self.assertRaises(ErrorConexion) as ctx:
            imp.imprimir(b"boleto")
        self.assertIn("no tiene papel", str(ctx.exception))
        self.assertEqual(bytes(self.sockets[0].enviado), b"")
        self.assertEqual(len(self.sockets), 1)          # sin papel no se reintenta a ciegas...
        self.assertTrue(self.sockets[0].cerrado)

    def test_fuera_de_linea_no_envia_el_boleto(self):
        imp = self.impresora(consultar_estado=True, estados=con_papel({escpos.CMD_ESTADO_IMPRESORA: b"\x1a"}))
        with self.assertRaises(ErrorConexion) as ctx:
            imp.imprimir(b"boleto")
        self.assertIn("fuera de línea", str(ctx.exception))
        self.assertEqual(bytes(self.sockets[0].enviado), b"")

    def test_fin_de_papel_por_causa_no_envia_el_boleto(self):
        # Vector medido el 2026-09-15: sin rollo y con la tapa cerrada, DLE EOT 2
        # contesta 0x32 y las otras dos preguntas siguen diciendo que todo va bien.
        imp = self.impresora(consultar_estado=True, estados=con_papel({escpos.CMD_ESTADO_CAUSA: b"\x32"}))
        with self.assertRaises(ErrorConexion) as ctx:
            imp.imprimir(b"boleto")
        self.assertIn("no tiene papel", str(ctx.exception))
        self.assertEqual(bytes(self.sockets[0].enviado), b"")
        self.assertEqual(self.sockets[0].consultas,
                         [escpos.CMD_ESTADO_PAPEL, escpos.CMD_ESTADO_CAUSA])

    def test_tapa_abierta_y_error_no_envian_el_boleto(self):
        casos = {b"\x16": "tiene la tapa abierta", b"\x52": "reporta un error"}
        dichos = {}
        for causa in casos:
            imp = self.impresora(consultar_estado=True, estados=con_papel({escpos.CMD_ESTADO_CAUSA: causa}))
            with self.assertRaises(ErrorConexion) as ctx:
                imp.imprimir(b"boleto")
            dichos[causa] = str(ctx.exception).replace("la impresora AA:BB:CC:DD:EE:FF ", "")
            self.assertEqual(bytes(self.sockets[-1].enviado), b"")
        self.assertEqual(dichos, casos)

    def test_con_papel_imprime_y_restaura_timeout(self):
        imp = self.impresora(consultar_estado=True, estados=con_papel())
        imp.imprimir(b"boleto")
        s = self.sockets[0]
        self.assertEqual(bytes(s.enviado), b"boleto")
        self.assertEqual(s.consultas, list(COMANDOS_ESTADO))
        self.assertEqual(s.timeout, 10.0)

    def test_poco_papel_solo_avisa(self):
        # El assert MUERDE: si se borra la rama del aviso (mutación M7) no hay
        # registro y esto cae. Hasta la Fase 4a el golden solo miraba lo escrito,
        # así que borrar la rama dejaba la suite en verde.
        imp = self.impresora(consultar_estado=True,
                             estados=con_papel({escpos.CMD_ESTADO_PAPEL: b"\x1e"}))   # 0x12 | 0x0C
        with registro_activo(), self.assertLogs("ruleta.escpos", level="WARNING") as cm:
            imp.imprimir(b"boleto")
        self.assertEqual(cm.output, [f"WARNING:ruleta.escpos:La impresora AA:BB:CC:DD:EE:FF {AVISO_POCO_PAPEL}"])
        self.assertEqual(bytes(self.sockets[0].enviado), b"boleto")

    def test_el_byte_medido_0x16_no_avisa_de_poco_papel(self):
        # 0x16 es la respuesta SANA de DLE EOT 1 (bit 2 = pin 3 del cajón). Leído
        # con la tabla de DLE EOT 4 tiene un solo bit de la pareja 2-3, y con la
        # máscara suelta disparaba el aviso falso que salió 15 veces en el log.
        imp = self.impresora(consultar_estado=True,
                             estados=con_papel({escpos.CMD_ESTADO_PAPEL: b"\x16"}))
        with registro_activo(), self.assertNoLogs("ruleta.escpos", level="WARNING"):
            imp.imprimir(b"boleto")
        self.assertEqual(bytes(self.sockets[0].enviado), b"boleto")

    def test_impresora_que_no_responde_al_estado_imprime_igual(self):
        imp = self.impresora(consultar_estado=True)
        imp.imprimir(b"boleto")
        self.assertEqual(bytes(self.sockets[0].enviado), b"boleto")

    def test_byte_de_estado_invalido_se_ignora(self):
        # 0xFF no cumple los bits fijos: no es un estado, se descarta y se imprime
        imp = self.impresora(consultar_estado=True, estados={escpos.CMD_ESTADO_PAPEL: b"\xff\xff"})
        imp.imprimir(b"boleto")
        self.assertEqual(bytes(self.sockets[0].enviado), b"boleto")

    def test_consulta_desactivada_no_pregunta(self):
        imp = self.impresora(consultar_estado=False, estados={escpos.CMD_ESTADO_PAPEL: b"\x72"})
        imp.imprimir(b"boleto")
        self.assertEqual(self.sockets[0].consultas, [])

    def test_timeout_cero_significa_sin_limite(self):
        imp = ImpresoraBluetooth("aa:bb:cc:dd:ee:ff", timeout=0, consultar_estado=False,
                                 dormir=self.pausas.append, fabrica_socket=self.fabrica())
        imp.imprimir(b"x")
        self.assertIsNone(self.sockets[0].timeout)

    def test_envio_exitoso_en_bloques(self):
        imp = self.impresora()
        imp.imprimir(b"0123456789")
        self.assertEqual(bytes(self.sockets[0].enviado), b"0123456789")
        self.assertEqual(self.sockets[0].envios, 3)
        self.assertTrue(self.sockets[0].cerrado)
        self.assertEqual(self.registro[0], ("connect", ("AA:BB:CC:DD:EE:FF", 1)))
        self.assertEqual(self.pausas, [0.01, 0.01, 0.01, 0.5])
        self.assertEqual(self.sockets[0].timeout, 10.0)

    def test_pausa_inicial_y_drenado_proporcional(self):
        imp = self.impresora(pausa_inicial=0.4, bytes_por_segundo=1000)
        imp.imprimir(b"x" * 500)   # 500 B a 1000 B/s = 0.5 s extra de drenado
        self.assertEqual(self.pausas[0], 0.4)
        self.assertAlmostEqual(self.pausas[-1], 0.5 + 0.5)
        self.assertEqual(len(self.pausas), 1 + 125 + 1)

    def test_conexion_fallida_reintenta_y_lanza_error_conexion(self):
        imp = self.impresora(fallar_conexion=True)
        with self.assertRaises(ErrorConexion) as ctx:
            imp.imprimir(b"hola")
        self.assertEqual(len(self.sockets), 3)
        self.assertEqual(self.pausas, [2.0, 2.0])   # no espera después del último intento
        self.assertIn("apagada", str(ctx.exception))
        self.assertTrue(all(s.cerrado for s in self.sockets))

    def test_corte_a_mitad_del_envio_es_error_envio_sin_reintento(self):
        imp = self.impresora(fallar_envio_en=1)
        with self.assertRaises(ErrorEnvio) as ctx:
            imp.imprimir(b"0123456789")
        self.assertEqual(ctx.exception.bytes_enviados, 4)
        self.assertEqual(len(self.sockets), 1)
        self.assertTrue(self.sockets[0].cerrado)

    def test_fallo_antes_del_primer_byte_cuenta_como_conexion(self):
        imp = self.impresora(fallar_envio_en=0)
        with self.assertRaises(ErrorConexion):
            imp.imprimir(b"0123456789")
        self.assertEqual(len(self.sockets), 3)

    def test_probar(self):
        self.impresora().probar()
        self.assertEqual(self.registro, [("connect", ("AA:BB:CC:DD:EE:FF", 1)), ("shutdown",), ("close",)])
        with self.assertRaises(ErrorConexion):
            self.impresora(fallar_conexion=True).probar()

    def test_errores_sin_reintento(self):
        casos = ((errno.EBUSY, "otro programa"), (errno.EACCES, "emparejar"), (errno.EPERM, "permiso"))
        for num, pista in casos:
            self.registro.clear()
            self.sockets.clear()
            self.pausas.clear()
            with self.assertRaises(ErrorConexion) as ctx:
                self.impresora(fallar_conexion=True, errno_conexion=num).imprimir(b"x")
            self.assertEqual(len(self.sockets), 1, f"errno {num} no debe reintentar")
            self.assertEqual(self.pausas, [])
            self.assertIn(pista, str(ctx.exception))

    def test_explicaciones(self):
        self.assertIn("rechazó", escpos._explicar_error_bt(OSError(errno.ECONNREFUSED, "Connection refused"), "M"))
        self.assertIn("no respondió", escpos._explicar_error_bt(socket.timeout("timed out"), "M"))
        self.assertIn("adaptador", escpos._explicar_error_bt(OSError(errno.ENETDOWN, "Network is down"), "M"))
        self.assertIn("apagada", escpos._explicar_error_bt(OSError(errno.EHOSTDOWN, "Host is down"), "M"))
        self.assertEqual(escpos._explicar_error_bt(None, "M"), "error desconocido")
        self.assertEqual(escpos._explicar_error_bt(OSError(9999, "raro"), "M"), "[Errno 9999] raro")

    def test_buscar_canal(self):
        imp = self.impresora(canales_abiertos={3})
        self.assertEqual(imp.buscar_canal(), 3)
        intentos = [r[1][1] for r in self.registro if r[0] == "connect"]
        self.assertEqual(intentos, [1, 2, 3])
        self.assertTrue(all(s.cerrado for s in self.sockets))

    def test_buscar_canal_sin_resultado(self):
        imp = self.impresora(canales_abiertos=set())
        self.assertIsNone(imp.buscar_canal(range(1, 4)))

    def test_buscar_canal_otro_error_se_propaga(self):
        imp = self.impresora(fallar_conexion=True, errno_conexion=errno.EHOSTDOWN)
        with self.assertRaises(ErrorConexion):
            imp.buscar_canal()
        self.assertEqual(len(self.sockets), 1)

    def test_sin_soporte_bluetooth_da_error_claro(self):
        imp = ImpresoraBluetooth("aa:bb:cc:dd:ee:ff", reintentos=1, dormir=lambda s: None)
        with mock.patch("ruleta.escpos.soporte_bluetooth", return_value=False):
            with self.assertRaises(ErrorConexion) as ctx:
                imp.imprimir(b"x")
        self.assertIn("Bluetooth", str(ctx.exception))


class ArchivoFalso:
    """Dispositivo que acepta `acepta` bytes por escritura y falla tras `limite`."""

    def __init__(self, acepta=4, limite=None):
        self.acepta = acepta
        self.limite = limite
        self.escrito = bytearray()

    def write(self, datos):
        if self.limite is not None and len(self.escrito) >= self.limite:
            raise OSError(errno.EIO, "Input/output error")
        trozo = bytes(datos[: self.acepta])
        self.escrito += trozo
        return len(trozo)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class DispositivoFalso:
    """Doble del nodo usblp de una impresora EPSON normal: contesta UN byte por pregunta.

    `estados` es {comando DLE EOT: bytes de respuesta}; la pregunta que no
    tenga entrada se queda sin contestar. No suelta NADA hasta que se le escribe
    un comando, que es justo lo que hace un firmware que responde y se calla:
    con ese doble, la lectura fresca drena el vacío, pregunta, lee ese único
    byte y el resultado es el de siempre. `acepta` limita cuántos bytes toma por
    escritura y `limite` simula que el dispositivo se atraganta tras N bytes.
    """

    def __init__(self, estados=None, acepta=None, limite=None):
        self.estados = dict(estados or {})
        self.pendiente = bytearray()
        self.escrito = bytearray()
        self.consultas = []
        self.acepta = acepta
        self.limite = limite
        self.lecturas = 0
        self.esperas = []
        self.cerrado = False

    def write(self, datos):
        if self.limite is not None and len(self.escrito) >= self.limite:
            raise OSError(errno.EIO, "Input/output error")
        trozo = bytes(datos if self.acepta is None else datos[: self.acepta])
        self.escrito += trozo
        cola = bytes(self.escrito[-3:])          # el comando puede llegar partido en varias escrituras
        if cola in COMANDOS_ESTADO:
            self.consultas.append(cola)
            self.pendiente += self.estados.get(cola, b"")
        return len(trozo)

    def read(self, n):
        self.lecturas += 1
        dato = bytes(self.pendiente[:n])
        del self.pendiente[:n]
        return dato

    def hay_datos(self, f, timeout):
        self.esperas.append(timeout)
        return bool(self.pendiente)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.cerrado = True
        return False


class DispositivoFlujo:
    """Doble de la AOMU My-A1: repite SIN PARAR el último byte de estado.

    Es la impresora que midió la sonda del 2026-09-15: por el endpoint de
    lectura salen ~21 kB/s del último byte que fijó el firmware, y tras un
    DLE EOT el flujo todavía suelta unos cuantos bytes VIEJOS antes de cambiar
    al valor nuevo (la sonda vio el cambio entre el byte 1 y el 22). Por eso una
    lectura de un solo byte devuelve la respuesta a la pregunta ANTERIOR.

    - `atraso`: bytes viejos YA encolados antes de preguntar. Tiene que ser
      mayor que `_MAX_BYTES_RESPUESTA`, o el golden no distinguiría «con
      drenado» de «sin drenado» y la mutación M1 sobreviviría en verde.
    - `viejos`: los que siguen saliendo con el valor anterior tras el comando.
      Son 21, el peor caso MEDIDO (la sonda vio el cambio en el byte 22 como muy
      tarde), para que cualquier `_MAX_BYTES_RESPUESTA` por debajo de 22 deje el
      golden en rojo. Con uno bastaría para separar «quedarse con el primero»
      (M2) de «quedarse con el último», pero no sujetaría el tope de lectura.
    - `inicial`: dónde estaba aparcado el flujo, 0x16 en la sonda.

    `read` NUNCA devuelve vacío y `hay_datos` SIEMPRE dice que sí: el único
    freno son los topes de `leer_estado_fresco`.
    """

    def __init__(self, respuestas=None, inicial=0x16, atraso=200, viejos=21,
                 acepta=None, limite=None):
        self.respuestas = dict(respuestas or {})
        self.actual = inicial
        self.viejos = viejos
        self.cola = bytearray([inicial]) * atraso
        self.escrito = bytearray()
        self.consultas = []
        self.acepta = acepta
        self.limite = limite
        self.lecturas = 0
        self.esperas = []
        self.cerrado = False

    def write(self, datos):
        if self.limite is not None and len(self.escrito) >= self.limite:
            raise OSError(errno.EIO, "Input/output error")
        trozo = bytes(datos if self.acepta is None else datos[: self.acepta])
        self.escrito += trozo
        cola = bytes(self.escrito[-3:])
        if cola in COMANDOS_ESTADO:
            self.consultas.append(cola)
            self.cola += bytes([self.actual]) * self.viejos   # el firmware tarda en cambiar
            self.actual = self.respuestas.get(cola, self.actual)
        return len(trozo)

    def read(self, n):
        self.lecturas += 1
        if self.cola:
            dato = bytes(self.cola[:n])
            del self.cola[:n]
            return dato
        return bytes([self.actual] * n)          # el flujo no se acaba nunca

    def hay_datos(self, f, timeout):
        self.esperas.append(timeout)
        return True

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.cerrado = True
        return False


class TestImpresoraArchivoUSB(unittest.TestCase):
    """Consulta de papel por USB (DLE EOT) en ImpresoraArchivo, sin hardware."""

    def setUp(self):
        self.aperturas = []

    def impresora(self, disp, consultar_estado=True, dispositivo=True, anexar=True):
        def abrir(ruta, modo, buffering=0):
            self.aperturas.append((ruta, modo, buffering))
            return disp
        return ImpresoraArchivo("/dev/ruleta-impresora", anexar=anexar, abrir=abrir,
                                consultar_estado=consultar_estado, timeout_estado=1.0,
                                es_dispositivo=lambda ruta: dispositivo,
                                esperar_lectura=disp.hay_datos)

    def test_sin_papel_no_envia_el_boleto(self):
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_PAPEL: b"\x72"}))   # 0x12 | 0x60
        with self.assertRaises(ErrorConexion) as ctx:
            self.impresora(disp).imprimir(b"boleto")
        self.assertIn("no tiene papel", str(ctx.exception))
        self.assertEqual(bytes(disp.escrito), escpos.CMD_ESTADO_PAPEL)   # solo la primera pregunta
        self.assertEqual(self.aperturas, [("/dev/ruleta-impresora", "r+b", 0)])
        self.assertTrue(disp.cerrado)

    def test_con_papel_escribe_todo(self):
        # Golden (e) del plan: una EPSON normal, que contesta un byte por pregunta
        # y se calla, se comporta EXACTAMENTE igual que antes de la lectura fresca.
        disp = DispositivoFalso(con_papel())
        self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")
        self.assertEqual(disp.consultas, list(COMANDOS_ESTADO))
        self.assertEqual(disp.lecturas, 3)            # un byte por pregunta, ni uno más

    def test_fuera_de_linea_no_envia_el_boleto(self):
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_IMPRESORA: b"\x1a"}))   # 0x12 | 0x08
        with self.assertRaises(ErrorConexion) as ctx:
            self.impresora(disp).imprimir(b"boleto")
        self.assertIn("fuera de línea", str(ctx.exception))
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO))

    def test_fin_de_papel_por_causa_no_envia_el_boleto(self):
        # Vector medido el 2026-09-15: DLE EOT 2 = 0x32 con el rollo fuera.
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_CAUSA: b"\x32"}))
        with self.assertRaises(ErrorConexion) as ctx:
            self.impresora(disp).imprimir(b"boleto")
        self.assertIn("no tiene papel", str(ctx.exception))
        self.assertEqual(bytes(disp.escrito),
                         escpos.CMD_ESTADO_PAPEL + escpos.CMD_ESTADO_CAUSA)

    def test_poco_papel_solo_avisa(self):
        # Estrena vector: con la máscara estricta, el 0x16 de antes ya no avisa.
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_PAPEL: b"\x1e"}))   # 0x12 | 0x0C
        with registro_activo(), self.assertLogs("ruleta.escpos", level="WARNING") as cm:
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(cm.output,
                         [f"WARNING:ruleta.escpos:La impresora /dev/ruleta-impresora {AVISO_POCO_PAPEL}"])
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")

    def test_el_byte_medido_0x16_no_avisa_de_poco_papel(self):
        # El aviso falso que salió 15 veces en el log del kiosco desde el
        # 2026-09-11: 0x16 tiene UN bit de la pareja 2-3, y con uno no basta.
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_PAPEL: b"\x16"}))
        with registro_activo(), self.assertNoLogs("ruleta.escpos", level="WARNING"):
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")

    def test_sin_respuesta_imprime_igual(self):
        disp = DispositivoFalso()                             # firmware que no contesta
        self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")
        self.assertEqual(disp.lecturas, 0)

    def test_cada_lectura_tiene_limite_de_tiempo(self):
        # Sin límite, una lectura sobre usblp cuelga el servicio para siempre.
        # Por pregunta: una espera de drenado (que se corta en la primera lectura
        # vacía) y una del primer byte de la respuesta. Ninguna pasa del tope.
        disp = DispositivoFalso()
        imp = self.impresora(disp)
        imp.imprimir(b"boleto")
        self.assertEqual(disp.esperas, [escpos._ESPERA_DRENADO_SEG, 1.0] * len(COMANDOS_ESTADO))
        self.assertLessEqual(max(disp.esperas), imp.timeout_estado)

    def test_bytes_invalidos_se_descartan_e_imprime(self):
        # Una impresora que habla sin parar y NUNCA contesta un estado válido:
        # los topes cortan (drenado y respuesta), las tres preguntas dan None y
        # se imprime igual, que es la política de siempre.
        disp = DispositivoFlujo(inicial=0x00)                 # 0x00 no cumple los bits fijos
        self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")
        self.assertEqual(disp.lecturas,
                         len(COMANDOS_ESTADO) * (escpos._MAX_BYTES_DRENADO + escpos._MAX_BYTES_RESPUESTA))

    def test_consultar_estado_false_no_pregunta(self):
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_PAPEL: b"\x72"}))   # diría que no hay papel...
        self.impresora(disp, consultar_estado=False).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"boleto")      # ...pero no se le pregunta
        self.assertEqual(disp.lecturas, 0)
        self.assertEqual(self.aperturas, [("/dev/ruleta-impresora", "ab", 0)])

    def test_archivo_normal_no_pregunta_aunque_este_activado(self):
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_PAPEL: b"\x72"}))
        self.impresora(disp, dispositivo=False).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"boleto")
        self.assertEqual(disp.lecturas, 0)
        self.assertEqual(self.aperturas, [("/dev/ruleta-impresora", "ab", 0)])

    def test_fallo_a_mitad_no_cuenta_la_consulta(self):
        disp = DispositivoFalso(con_papel(), acepta=4, limite=10)   # 9 de consultas + 4 de boleto
        with self.assertRaises(ErrorEnvio) as ctx:
            self.impresora(disp).imprimir(b"0123456789")
        self.assertEqual(ctx.exception.bytes_enviados, 4)

    def test_consultar_papel_devuelve_los_tres_bytes(self):
        disp = DispositivoFalso(con_papel({escpos.CMD_ESTADO_IMPRESORA: b"\x1e"}))
        self.assertEqual(self.impresora(disp).consultar_papel(), (0x12, 0x12, 0x1e))
        self.assertEqual(disp.consultas, list(COMANDOS_ESTADO))
        self.assertEqual(self.aperturas, [("/dev/ruleta-impresora", "r+b", 0)])

    def test_consultar_papel_sin_respuesta(self):
        self.assertEqual(self.impresora(DispositivoFalso()).consultar_papel(), (None, None, None))

    def test_consultar_papel_no_se_puede_abrir(self):
        def abrir(*a, **k):
            raise PermissionError(13, "Permission denied")
        with self.assertRaises(ErrorConexion):
            ImpresoraArchivo("/dev/ruleta-impresora", abrir=abrir).consultar_papel()

    def test_archivo_de_verdad_con_consulta_activada_se_comporta_igual(self):
        # Vector real: salida_impresora.bin con consultar_estado=True no cambia nada.
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "salida.bin")
            ImpresoraArchivo(ruta, anexar=True, consultar_estado=True).imprimir(b"uno")
            ImpresoraArchivo(ruta, anexar=True, consultar_estado=True).imprimir(b"dos")
            with open(ruta, "rb") as f:
                self.assertEqual(f.read(), b"unodos")

    def test_solo_un_dispositivo_de_caracteres_es_dispositivo(self):
        # El caso POSITIVO no se puede tener de verdad en esta PC, y sin él la
        # prueba pasaría igual con un es_dispositivo_caracteres que devolviera
        # siempre False: la consulta de papel por USB quedaría muerta en la Pi
        # con la suite en verde. Se compara el censo entero por igualdad.
        modos = {"/dev/ruleta-impresora": stat.S_IFCHR | 0o660,
                 "salida_impresora.bin": stat.S_IFREG | 0o644,
                 "/dev/mmcblk0": stat.S_IFBLK | 0o660,
                 "/dev": stat.S_IFDIR | 0o755}
        stat_fn = lambda ruta: SimpleNamespace(st_mode=modos[ruta])
        self.assertEqual({r: escpos.es_dispositivo_caracteres(r, stat_fn=stat_fn) for r in modos},
                         {"/dev/ruleta-impresora": True, "salida_impresora.bin": False,
                          "/dev/mmcblk0": False, "/dev": False})
        self.assertFalse(escpos.es_dispositivo_caracteres("/ruta/que/no/existe/lp0"))
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "salida.bin")
            with open(ruta, "wb"):
                pass
            self.assertFalse(escpos.es_dispositivo_caracteres(ruta))


class TestLecturaFrescaAOMU(unittest.TestCase):
    """Goldens contra el doble de la impresora que habla sin parar (AOMU My-A1).

    Es la que tiene el kiosco. Los vectores MEDIDOS el 2026-09-15 son los de «con
    papel» (0x12 / 0x12 / 0x16) y el de «sin papel» (DLE EOT 2 = 0x32); los de
    sin-papel por sensor (0x72), fuera de línea (0x1e), poco papel (0x1e), error
    (0x52) y tapa abierta (bit 2) NO están medidos en este clon: son vectores de
    la tabla EPSON, no bytes que haya contestado esta impresora. El caso (b) es
    exactamente el que el 2026-09-15 a las 13:29 regaló el boleto
    00009: rollo agotado, tapa cerrada, DLE EOT 2 contestando 0x32 mientras las
    otras dos preguntas seguían diciendo que todo estaba bien.
    """

    def setUp(self):
        self.aperturas = []

    def impresora(self, disp):
        def abrir(ruta, modo, buffering=0):
            self.aperturas.append((ruta, modo, buffering))
            return disp
        return ImpresoraArchivo("/dev/ruleta-impresora", anexar=True, abrir=abrir,
                                consultar_estado=True, timeout_estado=1.0,
                                es_dispositivo=lambda ruta: True, esperar_lectura=disp.hay_datos)

    @staticmethod
    def lecturas_de(preguntas):
        """Censo DERIVADO: por pregunta, el drenado topa en su límite (este flujo
        no se vacía nunca) y la respuesta se lee hasta el suyo."""
        return preguntas * (escpos._MAX_BYTES_DRENADO + escpos._MAX_BYTES_RESPUESTA)

    def test_el_tramo_empieza_viejo_y_acaba_con_la_respuesta_nueva(self):
        # Sonda del 2026-09-15, 13:43:44: se escribió DLE EOT 4 y el tramo empezó
        # en 0x32 (el eco del DLE EOT 2 anterior) y acabó en 0x12, que sí era su
        # respuesta. Aquí, con el flujo aparcado en 0x16 como lo encontró la
        # sonda, el primer byte del tramo es el eco viejo y el último la
        # respuesta al comando recién escrito.
        disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_CAUSA: 0x32}))
        leidos = []

        def leer_byte(espera):
            dato = disp.read(1)
            leidos.append(dato[0])
            return dato

        byte = escpos.leer_estado_fresco(disp.write, leer_byte, escpos.CMD_ESTADO_CAUSA, 1.0)
        self.assertEqual(byte, 0x32)
        tramo = leidos[escpos._MAX_BYTES_DRENADO:]
        self.assertEqual(len(tramo), escpos._MAX_BYTES_RESPUESTA)
        self.assertEqual((tramo[0], tramo[-1]), (0x16, 0x32))
        self.assertEqual(set(tramo), {0x16, 0x32})

    def test_el_tramo_se_corta_por_tiempo_aunque_el_flujo_siga(self):
        # El otro tope del tramo, el de TIEMPO: con una impresora que no se calla
        # nunca, lo que corta la lectura puede ser el reloj antes que los 64
        # bytes. Con un reloj falso para no dormir de verdad en la suite.
        disp = DispositivoFlujo(flujo_con_papel())
        tiempos = [0.0, 0.0, 0.10, 0.19, escpos._MAX_SEG_RESPUESTA]
        reloj = iter(tiempos)
        with mock.patch("ruleta.escpos.time.monotonic", lambda: next(reloj, tiempos[-1])):
            byte = escpos.leer_estado_fresco(disp.write, lambda espera: disp.read(1),
                                             escpos.CMD_ESTADO_PAPEL, 1.0)
        # Cuatro bytes leídos, no 64: el reloj llegó al tope antes que el conteo.
        self.assertEqual(disp.lecturas, escpos._MAX_BYTES_DRENADO + 4)
        self.assertEqual(byte, 0x16)      # cortar pronto devuelve el eco viejo, y eso es lo esperable

    def test_con_papel_no_avisa_y_escribe_el_boleto_entero(self):
        # (a) Con papel: 0x12 / 0x12 / 0x16, los tres medidos.
        disp = DispositivoFlujo(flujo_con_papel())
        with registro_activo(), self.assertNoLogs("ruleta.escpos", level="WARNING"):
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")
        self.assertEqual(disp.consultas, list(COMANDOS_ESTADO))
        self.assertEqual(disp.lecturas, self.lecturas_de(3))
        self.assertEqual(self.aperturas, [("/dev/ruleta-impresora", "r+b", 0)])

    def test_fin_de_papel_por_causa_no_escribe_ni_un_byte_del_boleto(self):
        # (b) El boleto 00009: DLE EOT 2 = 0x32 y las otras dos sanas.
        disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_CAUSA: 0x32}))
        with self.assertRaises(ErrorConexion) as ctx:
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(str(ctx.exception), "la impresora /dev/ruleta-impresora no tiene papel")
        self.assertEqual(bytes(disp.escrito), escpos.CMD_ESTADO_PAPEL + escpos.CMD_ESTADO_CAUSA)
        self.assertEqual(disp.lecturas, self.lecturas_de(2))

    def test_sin_papel_por_sensor_no_escribe_ni_un_byte_del_boleto(self):
        # (c) Los bits 5-6 de DLE EOT 4, que en este clon no se encienden nunca
        # pero en otra impresora sí: se corta en la PRIMERA pregunta.
        disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_PAPEL: 0x72}))
        with self.assertRaises(ErrorConexion) as ctx:
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(str(ctx.exception), "la impresora /dev/ruleta-impresora no tiene papel")
        self.assertEqual(bytes(disp.escrito), escpos.CMD_ESTADO_PAPEL)
        self.assertEqual(disp.lecturas, self.lecturas_de(1))

    def test_fuera_de_linea_no_escribe_ni_un_byte_del_boleto(self):
        # (d) Bit 3 de DLE EOT 1: se pregunta la tercera y se corta ahí.
        disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_IMPRESORA: 0x1e}))
        with self.assertRaises(ErrorConexion) as ctx:
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(str(ctx.exception),
                         "la impresora /dev/ruleta-impresora está fuera de línea "
                         "(tapa abierta, sin papel o error)")
        self.assertEqual(bytes(disp.escrito), b"".join(COMANDOS_ESTADO))
        self.assertEqual(disp.lecturas, self.lecturas_de(3))

    def test_tapa_abierta_y_error_de_impresora_no_escriben_el_boleto(self):
        # Las otras dos ramas de DLE EOT 2. La tapa abierta NO está medida en
        # esta impresora (el bit 2 nunca se vio encendido); se programa porque
        # otra sí lo reporta. El censo de textos se compara entero, por igualdad.
        casos = {0x16: "la impresora /dev/ruleta-impresora tiene la tapa abierta",
                 0x52: "la impresora /dev/ruleta-impresora reporta un error"}
        dichos = {}
        for causa in casos:
            disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_CAUSA: causa}))
            with self.assertRaises(ErrorConexion) as ctx:
                self.impresora(disp).imprimir(b"boleto")
            dichos[causa] = str(ctx.exception)
            self.assertEqual(bytes(disp.escrito), escpos.CMD_ESTADO_PAPEL + escpos.CMD_ESTADO_CAUSA)
        self.assertEqual(dichos, casos)

    def test_poco_papel_de_verdad_avisa_y_el_byte_medido_no(self):
        # (g) en la impresora que habla sin parar: solo la pareja 2-3 entera
        # avisa. 0x16, el byte que disparó 15 avisos falsos, no dice nada.
        disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_PAPEL: 0x1e}))
        with registro_activo(), self.assertLogs("ruleta.escpos", level="WARNING") as cm:
            self.impresora(disp).imprimir(b"boleto")
        self.assertEqual(cm.output,
                         [f"WARNING:ruleta.escpos:La impresora /dev/ruleta-impresora {AVISO_POCO_PAPEL}"])
        sano = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_PAPEL: 0x16}))
        with registro_activo(), self.assertNoLogs("ruleta.escpos", level="WARNING"):
            self.impresora(sano).imprimir(b"boleto")
        self.assertEqual(bytes(sano.escrito), b"".join(COMANDOS_ESTADO) + b"boleto")

    def test_ninguna_espera_pasa_del_tope(self):
        # El servicio no puede colgarse leyendo usblp: las únicas esperas que se
        # piden son las tres del diseño, y la mayor es timeout_estado.
        disp = DispositivoFlujo(flujo_con_papel())
        imp = self.impresora(disp)
        imp.imprimir(b"boleto")
        self.assertEqual(set(disp.esperas),
                         {escpos._ESPERA_DRENADO_SEG, imp.timeout_estado,
                          escpos._ESPERA_SIGUIENTE_BYTE_SEG})
        self.assertEqual(len(disp.esperas), self.lecturas_de(3))
        self.assertEqual(max(disp.esperas), imp.timeout_estado)

    def test_consultar_papel_devuelve_los_tres_frescos(self):
        # El diagnóstico ve lo mismo que la impresión: sin papel, DLE EOT 2 es
        # el único que se entera (0x32) y los otros dos siguen igual de sanos.
        disp = DispositivoFlujo(flujo_con_papel({escpos.CMD_ESTADO_CAUSA: 0x32}))
        self.assertEqual(self.impresora(disp).consultar_papel(), (0x12, 0x32, 0x16))
        self.assertEqual(disp.consultas, list(COMANDOS_ESTADO))


class TestImpresoraArchivo(unittest.TestCase):
    def test_anexa_o_trunca(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "salida.bin")
            ImpresoraArchivo(ruta, anexar=True).imprimir(b"uno")
            ImpresoraArchivo(ruta, anexar=True).imprimir(b"dos")
            with open(ruta, "rb") as f:
                self.assertEqual(f.read(), b"unodos")
            ImpresoraArchivo(ruta, anexar=False).imprimir(b"tres")
            with open(ruta, "rb") as f:
                self.assertEqual(f.read(), b"tres")

    def test_no_se_puede_abrir_es_error_conexion(self):
        with self.assertRaises(ErrorConexion):
            ImpresoraArchivo("/ruta/que/no/existe/lp0").imprimir(b"x")

    def test_escrituras_parciales_se_completan(self):
        disp = ArchivoFalso(acepta=3)
        ImpresoraArchivo("dev", abrir=lambda *a, **k: disp).imprimir(b"0123456789")
        self.assertEqual(bytes(disp.escrito), b"0123456789")

    def test_fallo_a_mitad_es_error_envio(self):
        disp = ArchivoFalso(acepta=4, limite=4)
        with self.assertRaises(ErrorEnvio) as ctx:
            ImpresoraArchivo("dev", abrir=lambda *a, **k: disp).imprimir(b"0123456789")
        self.assertEqual(ctx.exception.bytes_enviados, 4)

    def test_fallo_antes_del_primer_byte_es_error_conexion(self):
        disp = ArchivoFalso(acepta=4, limite=0)
        with self.assertRaises(ErrorConexion):
            ImpresoraArchivo("dev", abrir=lambda *a, **k: disp).imprimir(b"0123456789")


class TestVista(unittest.TestCase):
    def test_decodifica_texto_tamano_y_corte(self):
        doc = (Documento(codepage="cp850", chars_por_linea=16).inicializar().alinear("centro")
               .tamano(2, 2).linea("Hola").tamano(1, 1).linea("año").cortar("parcial", 1))
        salida = decodificar_vista(doc.bytes(), "cp850", 16)
        lineas = salida.splitlines()
        self.assertIn("HHoollaa", lineas[0])
        self.assertTrue(lineas[0].startswith(" 2x|"))
        self.assertIn("año", lineas[1])
        self.assertIn("[CORTE]", lineas[-1])
        self.assertNotIn(".", lineas[0])   # FS . no debe aparecer como texto

    def test_decodifica_corte_auto(self):
        salida = decodificar_vista(Documento().linea("x").cortar("auto", 0).bytes())
        self.assertEqual(salida.splitlines()[-1].count("[CORTE]"), 1)
        self.assertEqual(len(salida.splitlines()), 2)

    def test_cambio_de_tabla_a_media_linea(self):
        datos = (b"\x1bt\x13" + "ñ1 ".encode("cp858") + b"\x1bt\x10" + "ñ2".encode("cp1252") + b"\n"
                 + "ñ3".encode("cp1252") + b"\n\x1b@" + "ñ4".encode("cp858") + b"\n")
        lineas = decodificar_vista(datos, "cp858").splitlines()
        self.assertIn("ñ1 ñ2", lineas[0])
        self.assertIn("ñ3", lineas[1])          # la tabla se mantiene entre líneas
        self.assertIn("ñ4", lineas[2])          # ESC @ vuelve a la tabla configurada
        self.assertEqual(len(lineas), 3)

    def test_imagen_se_salta_y_anuncia(self):
        doc = Documento().imagen(Image.new("L", (16, 3), 0)).linea("fin")
        salida = decodificar_vista(doc.bytes())
        self.assertIn("[IMAGEN 16x3 px]", salida)
        self.assertIn("fin", salida)

    def test_impresora_memoria_falla_a_pedido(self):
        imp = escpos.ImpresoraMemoria()
        imp.imprimir(b"a")
        imp.fallar = ErrorConexion("x")
        with self.assertRaises(ErrorConexion):
            imp.imprimir(b"b")
        self.assertEqual(imp.trabajos, [b"a"])


if __name__ == "__main__":
    unittest.main()
