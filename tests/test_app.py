import contextlib
import logging
import random
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock

from ruleta import config as configmod, ticket
from ruleta.app import Ruleta, crear_impresora
from ruleta.config import ErrorConfig
from ruleta.escpos import ErrorConexion, ErrorEnvio, ImpresoraMemoria
from ruleta.hardware import Antirrebote, EntradasSimuladas
from ruleta.inventario import Inventario

# Horario que deja FUERA la hora del reloj de prueba (19:00): así una jugada cae
# antes de la apertura sin tener que mover el reloj de todas las demás pruebas.
HORARIO_CERRADO = {"abre": "20:00", "cierra": "23:00"}


@contextlib.contextmanager
def registro_activo():
    """Vuelve a encender el registro mientras dura el bloque.

    Mismo patrón que `tests/test_escpos.py` y por el mismo motivo (ficha F-253):
    `tests/__init__.py` hace `logging.disable(logging.CRITICAL)` para que las
    pruebas que provocan errores a propósito no ensucien la salida, y con eso
    puesto `assertLogs` y `assertNoLogs` no ven absolutamente nada. Se replica
    aquí —en vez de importarlo— para que este módulo de pruebas no dependa de
    otro. Se enciende solo dentro del bloque y se vuelve a apagar al salir, pase
    lo que pase.
    """
    logging.disable(logging.NOTSET)
    try:
        yield
    finally:
        logging.disable(logging.CRITICAL)


class RngSiempreConsuelo:
    """`rng` falso que siempre elige el ÚLTIMO papelito de la tómbola.

    Con `peso_consuelo` > 0 ese último es el consuelo (None), así que la jugada
    sale sin premio **aunque queden premios disponibles**, que es justo lo que la
    pieza A tiene que permitir.
    """

    def __init__(self):
        self.llamadas: list[tuple[list, list]] = []

    def choices(self, population, weights=None, k=1):
        self.llamadas.append((list(population), list(weights)))
        return [population[-1]]


class Reloj:
    """Tiempo controlado: monotónico y de pared avanzan juntos."""

    def __init__(self):
        self.t = 1000.0
        self.pared = datetime(2026, 9, 15, 19, 0, 0)

    def monotonico(self):
        return self.t

    def ahora(self):
        return self.pared

    def avanzar(self, seg):
        self.t += seg
        self.pared += timedelta(seconds=seg)


def config_prueba(**extra):
    crudo = {
        "negocio": {"nombre": "Asadero 33", "logo": None},
        "impresora": {"tipo": "vista"},
        "gpio": {"boton_jugar": 17, "boton_habilitar": 27, "led": 22, "rebote_ms": 30, "pulsacion_larga_seg": 3.0},
        "juego": {"espera_entre_jugadas_seg": 5.0, "imprimir_inventario_al_arrancar": True,
                  "intentos_inventario_arranque": 2},
        "premios": [
            {"id": "unico", "nombre": "Premio único", "peso": 1, "stock": 1},
            {"id": "tacos", "nombre": "Tacos", "peso": 1000, "stock": 100},
        ],
    }
    for k, v in extra.items():
        if isinstance(v, dict) and isinstance(crudo.get(k), dict):
            crudo[k].update(v)
        else:
            crudo[k] = v
    return configmod.desde_dict(crudo)


class TestAntirrebote(unittest.TestCase):
    def test_ignora_rebotes_cortos(self):
        d = Antirrebote(0.03)
        self.assertFalse(d.actualizar(True, 0.000))
        self.assertFalse(d.actualizar(True, 0.010))
        self.assertFalse(d.actualizar(False, 0.020))   # rebote
        self.assertFalse(d.actualizar(True, 0.030))    # reinicia la cuenta
        self.assertFalse(d.actualizar(True, 0.050))
        self.assertTrue(d.actualizar(True, 0.061))
        self.assertTrue(d.actualizar(False, 0.070))
        self.assertTrue(d.actualizar(False, 0.090))
        self.assertFalse(d.actualizar(False, 0.101))


class TestRuleta(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.reloj = Reloj()
        self.cfg = config_prueba()
        self.inv = Inventario(self.cfg.premios, Path(self.tmp.name), rng=random.Random(3),
                              peso_consuelo=self.cfg.juego.consuelo.peso)
        self.imp = ImpresoraMemoria()
        self.ent = EntradasSimuladas(reloj=self.reloj.monotonico)
        self.dormidas = []
        self.ruleta = self.nueva_ruleta(self.cfg, self.inv)

    def tearDown(self):
        self.tmp.cleanup()

    # -- ayudantes ------------------------------------------------------------ #

    def nueva_ruleta(self, cfg, inv, hora_sincronizada=None):
        extra = {} if hora_sincronizada is None else {"hora_sincronizada": hora_sincronizada}
        return Ruleta(cfg, inv, self.imp, self.ent, reloj=self.reloj.ahora,
                      monotonico=self.reloj.monotonico, dormir=self.dormidas.append, **extra)

    def ruleta_con_horario(self, fuera_de_horario="consuelo", **horario):
        """Una ruleta cuyo `config.json` trae horario de evento (pieza C, Fase 4d)."""
        cfg = config_prueba(juego={"horario": {**HORARIO_CERRADO, **horario,
                                               "fuera_de_horario": fuera_de_horario}})
        carpeta = Path(self.tmp.name) / f"h{fuera_de_horario}{len(self.imp.trabajos)}{len(horario)}"
        inv = Inventario(cfg.premios, carpeta,
                         rng=random.Random(3), peso_consuelo=cfg.juego.consuelo.peso,
                         horario=cfg.juego.horario,
                         separacion_min_entre_premios=cfg.juego.separacion_min_entre_premios)
        self.ruleta = self.nueva_ruleta(cfg, inv)
        return inv

    def reloj_que_avanza(self):
        """`dormir` que además mueve el reloj: hace falta para esperar de verdad."""
        def dormir(seg):
            self.dormidas.append(seg)
            self.reloj.avanzar(seg)
        return dormir

    def ticks(self, seg, paso=0.01):
        n = int(round(seg / paso))
        for _ in range(n):
            self.ruleta.paso()
            self.reloj.avanzar(paso)

    def pulsar(self, duracion=0.15, habilitar=True):
        self.ent.fijar_habilitar(habilitar)
        self.ent.fijar_jugar(True)
        self.ticks(duracion)
        self.ent.fijar_jugar(False)
        self.ticks(0.1)

    def trabajos_texto(self):
        return [t.decode("cp858", errors="replace") for t in self.imp.trabajos]

    def entregados_total(self):
        return self.inv.entregados("tacos") + self.inv.entregados("unico")

    # -- arranque ----------------------------------------------------------- #

    def test_arranque_imprime_inventario(self):
        self.ruleta.arrancar()
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertIn("INVENTARIO", self.trabajos_texto()[0])
        self.assertIn("(arranque)", self.trabajos_texto()[0])
        self.assertEqual(self.ruleta.reportes_impresos, 1)
        self.assertEqual(self.ent.estado_led, "apagado")  # habilitar suelto

    def test_arranque_reintenta_y_sigue_aunque_falle(self):
        self.imp.fallar = ErrorConexion("apagada")
        self.ruleta.arrancar()
        self.assertEqual(self.imp.trabajos, [])
        self.assertEqual(len(self.dormidas), 1)    # 2 intentos -> 1 espera entre ellos
        self.assertEqual(self.ent.estado_led, "error")

    def test_arranque_respeta_detener(self):
        self.imp.fallar = ErrorConexion("apagada")
        self.ruleta.detener()
        self.ruleta.arrancar()
        self.assertEqual(self.imp.trabajos, [])
        self.assertEqual(self.dormidas, [])

    # -- jugada -------------------------------------------------------------- #

    def test_pulsacion_sin_habilitar_se_ignora(self):
        self.pulsar(habilitar=False)
        self.assertEqual(self.imp.trabajos, [])
        self.assertEqual(self.inv.folio_actual, 0)

    def test_pulsacion_corta_imprime_un_boleto(self):
        self.pulsar()
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertIn("BOLETO 00001", self.trabajos_texto()[0])
        self.assertEqual(self.inv.folio_actual, 1)
        self.assertEqual(self.ruleta.boletos_impresos, 1)
        self.assertEqual(self.entregados_total(), 1)
        self.assertIn("ocupado", self.ent.historial_led)
        self.assertEqual(self.ent.estado_led, "listo")

    def test_pulsacion_larga_de_jugar_tambien_es_una_jugada(self):
        # El botón del cliente nunca imprime el inventario, aunque lo sostenga.
        self.pulsar(duracion=4.0)
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertIn("BOLETO 00001", self.trabajos_texto()[0])
        self.assertNotIn("INVENTARIO", self.trabajos_texto()[0])

    def test_soltar_habilitar_antes_de_soltar_jugar_sigue_valiendo(self):
        self.ent.fijar_habilitar(True)
        self.ent.fijar_jugar(True)
        self.ticks(0.1)
        self.ent.fijar_habilitar(False)
        self.ticks(0.05)
        self.ent.fijar_jugar(False)
        self.ticks(0.1)
        self.assertEqual(len(self.imp.trabajos), 1)

    def test_habilitar_despues_de_jugar_no_vale(self):
        # El cliente ya tiene JUGAR presionado cuando el mesero habilita: no cuenta.
        self.ent.fijar_jugar(True)
        self.ticks(0.2)
        self.ent.fijar_habilitar(True)
        self.ticks(0.2)
        self.ent.fijar_jugar(False)
        self.ticks(0.1)
        self.assertEqual(self.imp.trabajos, [])
        # Al presionar de nuevo con HABILITAR ya sostenido, sí juega.
        self.pulsar()
        self.assertEqual(len(self.imp.trabajos), 1)

    def test_espera_entre_jugadas(self):
        self.pulsar()
        self.pulsar()                       # dentro de los 5 s -> ignorada
        self.assertEqual(len(self.imp.trabajos), 1)
        self.ticks(5.0)
        self.pulsar()
        self.assertEqual(len(self.imp.trabajos), 2)
        self.assertEqual(self.inv.folio_actual, 2)

    def test_mantener_presionado_no_imprime_varias_veces(self):
        self.ent.fijar_habilitar(True)
        self.ent.fijar_jugar(True)
        self.ticks(1.0)
        self.assertEqual(self.imp.trabajos, [])      # la jugada ocurre al soltar
        self.ent.fijar_jugar(False)
        self.ticks(0.1)
        self.assertEqual(len(self.imp.trabajos), 1)

    def test_rebote_no_dispara(self):
        self.ent.fijar_habilitar(True)
        self.ent.fijar_jugar(True)
        self.ticks(0.02)                 # menos que el antirrebote (30 ms)
        self.ent.fijar_jugar(False)
        self.ticks(0.2)
        self.assertEqual(self.imp.trabajos, [])

    # -- gesto de inventario (botón del mesero) -------------------------------- #

    def test_habilitar_sostenido_imprime_inventario(self):
        self.ent.fijar_habilitar(True)
        self.ticks(3.0)
        self.assertEqual(self.imp.trabajos, [])
        self.ticks(0.2)
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertIn("INVENTARIO", self.trabajos_texto()[0])
        self.assertIn("(solicitado)", self.trabajos_texto()[0])
        self.assertEqual(self.inv.folio_actual, 0)
        # Seguir sosteniendo no imprime más; hay que soltar y volver a presionar.
        self.ticks(5.0)
        self.assertEqual(len(self.imp.trabajos), 1)
        self.ent.fijar_habilitar(False)
        self.ticks(0.2)
        self.ent.fijar_habilitar(True)
        self.ticks(3.3)
        self.assertEqual(len(self.imp.trabajos), 2)

    def test_una_jugada_cancela_el_gesto_de_inventario(self):
        self.ent.fijar_habilitar(True)
        self.ticks(1.0)
        self.pulsar()                    # el cliente juega mientras el mesero habilita
        self.ticks(4.0)                  # el mesero sigue sosteniendo mucho tiempo
        textos = self.trabajos_texto()
        self.assertEqual(len(textos), 1)
        self.assertIn("BOLETO 00001", textos[0])

    def test_gesto_de_inventario_funciona_durante_la_espera(self):
        self.pulsar()                    # boleto -> empieza la espera de 5 s
        self.ent.fijar_habilitar(False)  # el mesero suelta y vuelve a presionar
        self.ticks(0.2)
        self.ent.fijar_habilitar(True)
        self.ticks(3.3)
        self.assertEqual(len(self.imp.trabajos), 2)
        self.assertIn("INVENTARIO", self.trabajos_texto()[1])
        self.assertEqual(self.inv.folio_actual, 1)

    def test_gesto_desactivado_con_null(self):
        cfg = config_prueba(gpio={"pulsacion_larga_seg": None})
        self.ruleta = self.nueva_ruleta(cfg, self.inv)
        self.ent.fijar_habilitar(True)
        self.ticks(10.0)
        self.assertEqual(self.imp.trabajos, [])

    # -- fallos -------------------------------------------------------------- #

    def test_error_conexion_revierte_el_premio(self):
        # Este es el golden que sostiene la mitad del arreglo de la Fase 4a: la
        # detección de papel (ruleta/escpos.py) solo sirve si el ErrorConexion
        # que lanza devuelve el premio al inventario. Quitar el
        # `self.inv.revertir(boleto)` de ruleta/app.py (mutación M10) lo pone en
        # rojo. La política de app.py NO la cambió la Fase 4a: solo consiguió
        # que el ErrorConexion se lance cuando debe.
        self.imp.fallar = ErrorConexion("apagada")
        self.pulsar()
        self.assertEqual(self.inv.folio_actual, 1)          # el folio se consume
        self.assertEqual(self.entregados_total(), 0)
        self.assertEqual(self.ent.estado_led, "error")
        self.ticks(7.0)
        self.assertEqual(self.ent.estado_led, "listo")
        self.imp.fallar = None
        self.pulsar()
        self.assertEqual(self.inv.folio_actual, 2)
        self.assertEqual(len(self.imp.trabajos), 1)

    def test_error_envio_conserva_el_premio_y_queda_pendiente(self):
        self.imp.fallar = ErrorEnvio("se cortó", 300)
        self.pulsar()
        self.assertEqual(self.entregados_total(), 1)
        self.assertEqual(self.ruleta.boletos_impresos, 0)
        self.assertEqual(self.ent.estado_led, "error")
        self.assertEqual([p.folio for p in self.inv.pendientes()], [1])

    def test_fallo_al_guardar_no_emite_ni_mata_el_ciclo(self):
        with mock.patch.object(Inventario, "_guardar", side_effect=OSError(30, "Read-only file system")):
            self.pulsar()
        self.assertEqual(self.imp.trabajos, [])
        self.assertEqual(self.inv.folio_actual, 0)
        self.assertEqual(self.entregados_total(), 0)
        self.assertEqual(self.ent.estado_led, "error")
        self.assertEqual(self.ruleta.errores, 1)
        self.ticks(12.0)
        self.pulsar()                                    # el disco volvió: funciona
        self.assertEqual(len(self.imp.trabajos), 1)

    def test_error_al_construir_el_boleto_devuelve_el_premio(self):
        with mock.patch("ruleta.ticket.boleto_premio", side_effect=ValueError("logo roto")):
            self.pulsar()
        self.assertEqual(self.imp.trabajos, [])
        self.assertEqual(self.inv.folio_actual, 1)
        self.assertEqual(self.entregados_total(), 0)
        self.assertEqual(self.ent.estado_led, "error")

    def test_correr_sobrevive_a_una_excepcion_en_paso(self):
        llamadas = []

        def paso_roto():
            llamadas.append(1)
            if len(llamadas) == 1:
                raise RuntimeError("gpio raro")
            if len(llamadas) >= 3:
                self.ruleta.detener()

        self.ruleta.paso = paso_roto
        self.ruleta.correr(periodo=0.01)
        self.assertEqual(len(llamadas), 3)
        self.assertEqual(self.ruleta.errores, 1)

    def test_el_consuelo_con_peso_sale_aunque_queden_premios(self):
        """Pieza A (Fase 4c): el consuelo compite; no espera a que se agote todo.

        Es el otro caso del de abajo (`test_sin_premios_imprime_consuelo`), que
        cubre el consuelo por agotamiento con `peso` 0.
        """
        cfg = config_prueba(juego={"consuelo": {"peso": 217}})
        rng = RngSiempreConsuelo()
        inv = Inventario(cfg.premios, Path(self.tmp.name) / "peso", rng=rng,
                         peso_consuelo=cfg.juego.consuelo.peso)
        self.ruleta = self.nueva_ruleta(cfg, inv)
        self.pulsar()
        textos = self.trabajos_texto()
        self.assertEqual(len(textos), 1)
        self.assertIn("PARTICIPANDO", textos[0])
        self.assertNotIn("GANASTE", textos[0])
        self.assertIn("BOLETO 00001", textos[0])
        self.assertEqual(self.ruleta.boletos_impresos, 1)
        self.assertEqual(self.ent.estado_led, "listo")
        # El folio avanza y el premio NO se toca: los dos siguen enteros y en juego.
        self.assertEqual(inv.folio_actual, 1)
        self.assertEqual(inv.entregados("unico") + inv.entregados("tacos"), 0)
        self.assertEqual([p.id for p in inv.disponibles(self.reloj.ahora())], ["unico", "tacos"])
        self.assertEqual(inv.pendientes(), [])       # un consuelo nunca queda 'para revisar'
        # Y el papelito que se eligió era de verdad el del consuelo, con su peso.
        poblacion, pesos = rng.llamadas[0]
        self.assertEqual(poblacion[-1], None)
        self.assertEqual(pesos, [1, 1000, 217])

    def test_sin_premios_imprime_consuelo(self):
        cfg = config_prueba(premios=[{"id": "unico", "nombre": "Premio único", "peso": 1, "stock": 1}])
        self.assertEqual(cfg.juego.consuelo.peso, 0)   # aquí el consuelo sale por agotamiento
        inv = Inventario(cfg.premios, Path(self.tmp.name) / "c",
                         peso_consuelo=cfg.juego.consuelo.peso)
        self.ruleta = self.nueva_ruleta(cfg, inv)
        self.pulsar()
        self.ticks(5)
        self.pulsar()
        textos = self.trabajos_texto()
        self.assertEqual(len(textos), 2)
        self.assertIn("GANASTE", textos[0])
        self.assertNotIn("PARTICIPANDO", textos[0])
        self.assertEqual(inv.entregados("unico"), 1)
        self.assertEqual(inv.restantes(inv.premios["unico"]), 0)
        self.assertIn("PARTICIPANDO", textos[1])
        self.assertNotIn("GANASTE", textos[1])
        self.assertEqual(inv.folio_actual, 2)

    # -- horario del evento (pieza C, Fase 4d) -------------------------------- #

    def test_fuera_de_horario_con_consuelo_imprime_consuelo(self):
        """Respuesta del usuario a la pregunta 5 del §4: que se lleve algo."""
        inv = self.ruleta_con_horario("consuelo")
        self.pulsar()
        textos = self.trabajos_texto()
        self.assertEqual(len(textos), 1)
        self.assertIn("PARTICIPANDO", textos[0])
        self.assertNotIn("GANASTE", textos[0])
        self.assertEqual(inv.folio_actual, 1)                    # el consuelo gasta folio
        self.assertEqual(inv.entregados("unico") + inv.entregados("tacos"), 0)
        self.assertEqual(self.ruleta.boletos_impresos, 1)
        self.assertEqual(self.ruleta.errores, 0)
        self.assertEqual(self.ent.estado_led, "listo")

    def test_fuera_de_horario_con_no_jugar_no_imprime_nada(self):
        """La otra ruta del documento: ni papel ni folio, solo el LED."""
        inv = self.ruleta_con_horario("no_jugar")
        self.pulsar()
        self.assertEqual(self.imp.trabajos, [])
        self.assertEqual(inv.folio_actual, 0)
        self.assertEqual(self.ruleta.boletos_impresos, 0)
        self.assertEqual(self.ruleta.errores, 0)                 # no es una avería
        self.assertEqual(self.ent.estado_led, "error")           # lo único que avisa
        self.ticks(7.0)
        self.assertEqual(self.ent.estado_led, "listo")

    def test_dentro_del_horario_se_juega_normal(self):
        """Control: con el mismo código y el reloj dentro, sale el premio."""
        inv = self.ruleta_con_horario("no_jugar", abre="12:00", cierra="23:00")
        self.pulsar()
        textos = self.trabajos_texto()
        self.assertEqual(len(textos), 1)
        self.assertIn("GANASTE", textos[0])
        self.assertEqual(inv.folio_actual, 1)

    # -- espera de la hora al arrancar (pieza D, Fase 4d) --------------------- #

    def arrancar_esperando_hora(self, respuestas, espera_hora_seg):
        """Arranca la ruleta con un comprobador de hora falso; devuelve las consultas."""
        pendientes = list(respuestas)
        consultas = []

        def comprobador():
            consultas.append(self.reloj.monotonico())
            return pendientes.pop(0) if pendientes else False

        cfg = config_prueba(juego={"espera_hora_seg": espera_hora_seg,
                                   "intentos_inventario_arranque": 1})
        self.ruleta = self.nueva_ruleta(cfg, self.inv, hora_sincronizada=comprobador)
        self.ruleta.dormir = self.reloj_que_avanza()
        self.ruleta.arrancar()
        return consultas

    def test_arranque_espera_a_que_la_hora_se_sincronice(self):
        """No, no, sí: arranca a la tercera consulta y el boleto NO lleva aviso."""
        consultas = self.arrancar_esperando_hora([False, False, True], 120)
        self.assertEqual(len(consultas), 3)
        self.assertEqual(self.dormidas, [2.0, 2.0])              # cada 2 s, como dice el plan
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertIn("INVENTARIO", self.trabajos_texto()[0])
        self.assertNotIn(ticket.AVISO_HORA, self.trabajos_texto()[0])

    def test_arranque_avisa_en_el_boleto_si_la_hora_no_se_confirma(self):
        """Nunca llega la hora: arranca IGUAL, pero el boleto lo dice."""
        consultas = self.arrancar_esperando_hora([], 0.1)
        self.assertGreaterEqual(len(consultas), 1)
        self.assertEqual(len(self.imp.trabajos), 1)              # nunca se queda colgado
        self.assertIn(ticket.AVISO_HORA, self.trabajos_texto()[0])
        self.assertIn("INVENTARIO", self.trabajos_texto()[0])

    def test_sin_espera_configurada_no_se_pregunta_la_hora(self):
        """Por omisión (0 s) nada cambia respecto de antes de la Fase 4d."""
        self.assertEqual(config_prueba().juego.espera_hora_seg, 0.0)
        consultas = self.arrancar_esperando_hora([False], 0)
        self.assertEqual(consultas, [])
        self.assertEqual(self.dormidas, [])
        self.assertNotIn(ticket.AVISO_HORA, self.trabajos_texto()[0])

    # -- la espera de la hora, vista desde el journal (Fase 4e) -------------- #

    def ruleta_que_espera_la_hora(self, respuestas, espera_hora_seg):
        """Ruleta con comprobador de hora falso y un reloj que avanza al dormir.

        No arranca nada: la espera se llama sola, para que lo que quede en el
        registro sean SOLO sus líneas y se puedan anclar por igualdad de lista.
        """
        pendientes = list(respuestas)

        def comprobador():
            return pendientes.pop(0) if pendientes else False

        cfg = config_prueba(juego={"espera_hora_seg": espera_hora_seg})
        ruleta = self.nueva_ruleta(cfg, self.inv, hora_sincronizada=comprobador)
        ruleta.dormir = self.reloj_que_avanza()
        return ruleta

    def test_la_espera_de_la_hora_se_ve_en_el_journal(self):
        """Ficha F-273: cada línea, entera y en orden, con el reloj falso.

        Doce consultas separadas 2 s: la hora llega a los **22 s**. Los avisos
        periódicos caen a los **10** y a los **20**, ni uno más ni uno menos, y
        el último dice **cuánto costó**. Se ancla la lista COMPLETA porque lo que
        esta prueba defiende es justo eso: que una espera de medio minuto deje
        rastro y no silencio.
        """
        ruleta = self.ruleta_que_espera_la_hora([False] * 11 + [True], 300)
        with registro_activo(), self.assertLogs("ruleta.app", level="INFO") as cm:
            self.assertTrue(ruleta.esperar_hora_sincronizada())
        self.assertEqual(cm.output, [
            "INFO:ruleta.app:Esperando a que la hora se sincronice (hasta 300 s)…",
            "INFO:ruleta.app:Sigo esperando la hora: llevo 10 s de 300 s",
            "INFO:ruleta.app:Sigo esperando la hora: llevo 20 s de 300 s",
            "INFO:ruleta.app:Hora sincronizada tras 22 s",
        ])
        self.assertEqual(self.dormidas, [2.0] * 11)   # la cadencia de consulta no cambió

    def test_la_hora_que_ya_estaba_puesta_tambien_deja_su_linea(self):
        """El caso normal en la Pi: la hora ya está y la espera dura 0 s.

        Es el que más se va a ver en el journal, y el que hoy no dejaba nada.
        """
        ruleta = self.ruleta_que_espera_la_hora([True], 300)
        with registro_activo(), self.assertLogs("ruleta.app", level="INFO") as cm:
            self.assertTrue(ruleta.esperar_hora_sincronizada())
        self.assertEqual(cm.output, [
            "INFO:ruleta.app:Esperando a que la hora se sincronice (hasta 300 s)…",
            "INFO:ruleta.app:Hora sincronizada tras 0 s",
        ])
        self.assertEqual(self.dormidas, [])

    def test_el_tope_agotado_se_ve_en_el_journal(self):
        """Si la hora no llega: el aviso del principio y el WARNING de siempre."""
        ruleta = self.ruleta_que_espera_la_hora([], 6)
        with registro_activo(), self.assertLogs("ruleta.app", level="INFO") as cm:
            self.assertFalse(ruleta.esperar_hora_sincronizada())
        self.assertEqual(cm.output, [
            "INFO:ruleta.app:Esperando a que la hora se sincronice (hasta 6 s)…",
            "WARNING:ruleta.app:HORA SIN CONFIRMAR: el sistema no sincronizó la hora en 6 s. "
            "Revisa la fecha del boleto de inventario antes de abrir: si está mal, NO reinicies, "
            "espera y pide otro inventario",
        ])
        self.assertEqual(self.dormidas, [2.0, 2.0, 2.0])

    def test_sin_espera_configurada_no_se_registra_nada(self):
        """Con 0 s no se espera, así que tampoco se registra: sería ruido.

        Cualquier instalación que no use la pieza D arranca con `espera_hora_seg`
        en 0; una línea de log ahí saldría en **cada** arranque sin decir nada.
        """
        ruleta = self.ruleta_que_espera_la_hora([False], 0)
        with registro_activo(), self.assertNoLogs("ruleta.app", level="DEBUG"):
            self.assertTrue(ruleta.esperar_hora_sincronizada())
        self.assertEqual(self.dormidas, [])

    def test_un_comprobador_de_hora_que_falla_no_tira_el_arranque(self):
        def revienta():
            raise OSError("timedatectl no está")

        cfg = config_prueba(juego={"espera_hora_seg": 120, "intentos_inventario_arranque": 1})
        self.ruleta = self.nueva_ruleta(cfg, self.inv, hora_sincronizada=revienta)
        self.ruleta.dormir = self.reloj_que_avanza()
        self.ruleta.arrancar()
        self.assertEqual(self.dormidas, [])                      # no se queda dando vueltas
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertIn(ticket.AVISO_HORA, self.trabajos_texto()[0])

    def test_modo_siempre_no_necesita_habilitar_y_no_tiene_gesto(self):
        cfg = config_prueba(gpio={"modo_habilitar": "siempre", "boton_habilitar": None, "led": None})
        self.ruleta = self.nueva_ruleta(cfg, self.inv)
        self.ticks(10.0)                                 # nada se imprime solo
        self.assertEqual(self.imp.trabajos, [])
        self.pulsar(habilitar=False)
        self.assertEqual(len(self.imp.trabajos), 1)
        self.assertEqual(self.ent.estado_led, "listo")

    def test_led_sigue_al_boton_habilitar(self):
        self.ticks(0.1)
        self.assertEqual(self.ent.estado_led, "apagado")
        self.ent.fijar_habilitar(True)
        self.ticks(0.1)
        self.assertEqual(self.ent.estado_led, "listo")
        self.ent.fijar_habilitar(False)
        self.ticks(0.1)
        self.assertEqual(self.ent.estado_led, "apagado")

    def test_correr_y_detener(self):
        pasos = []

        def dormir(s):
            pasos.append(s)
            if len(pasos) >= 3:
                self.ruleta.detener()

        self.ruleta.dormir = dormir
        self.ruleta.correr(periodo=0.01)
        self.assertEqual(len(pasos), 3)
        self.ruleta.cerrar()
        self.assertEqual(self.ent.estado_led, "apagado")


class TestEntradasSimuladas(unittest.TestCase):
    def test_mantener_habilitar_es_temporal(self):
        reloj = Reloj()
        ent = EntradasSimuladas(reloj=reloj.monotonico)
        self.assertFalse(ent.habilitar_presionado())
        ent.mantener_habilitar(2.0)
        self.assertTrue(ent.habilitar_presionado())
        reloj.avanzar(2.5)
        self.assertFalse(ent.habilitar_presionado())


class TestCrearImpresora(unittest.TestCase):
    def test_bluetooth_sin_mac_configurada(self):
        cfg = config_prueba(impresora={"tipo": "bluetooth", "mac": "00:00:00:00:00:00"})
        with self.assertRaises(ErrorConfig):
            crear_impresora(cfg)

    def test_tipos(self):
        cfg = config_prueba(impresora={"tipo": "bluetooth", "mac": "AA:BB:CC:DD:EE:01", "canal": 2,
                                       "consultar_estado": False})
        imp = crear_impresora(cfg)
        self.assertEqual((imp.mac, imp.canal, imp.consultar_estado), ("AA:BB:CC:DD:EE:01", 2, False))
        self.assertEqual(crear_impresora(cfg, "vista").nombre, "vista")
        self.assertEqual(crear_impresora(cfg, "archivo").nombre, "archivo")

    def test_archivo_recibe_la_consulta_de_estado(self):
        """Por USB también hay que preguntar si hay papel (solo si está activada)."""
        cfg = config_prueba(impresora={"tipo": "archivo", "ruta": "/dev/ruleta-impresora",
                                       "consultar_estado": True})
        imp = crear_impresora(cfg)
        self.assertEqual((imp.nombre, imp.ruta, imp.anexar, imp.consultar_estado),
                         ("archivo", "/dev/ruleta-impresora", True, True))
        apagada = config_prueba(impresora={"tipo": "archivo", "ruta": "salida_impresora.bin",
                                           "consultar_estado": False})
        self.assertFalse(crear_impresora(apagada).consultar_estado)


if __name__ == "__main__":
    unittest.main()
