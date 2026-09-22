import csv
import json
import random
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest import mock

from ruleta import config as configmod
from ruleta.config import ConfigHorario, Franja, Premio
from ruleta.inventario import ErrorPersistencia, Inventario, instantes_de_liberacion

RUTA_CONFIG = Path(__file__).resolve().parent.parent / "config.json"
HORARIO_EVENTO = ConfigHorario(abre="12:00", cierra="23:00", fuera_de_horario="consuelo")


def inventario_del_evento(carpeta, rng=None):
    """Vector real: el `config.json` del repositorio, cableado como en producción.

    Se construye con los mismos parámetros que `ruleta/__main__.py::abrir_inventario`,
    que es el único sitio de producción que crea un Inventario.
    """
    cfg = configmod.cargar(RUTA_CONFIG)
    return Inventario(cfg.premios, carpeta, hora_inicio_dia=cfg.juego.hora_inicio_dia,
                      peso_consuelo=cfg.juego.consuelo.peso, horario=cfg.juego.horario,
                      separacion_min_entre_premios=cfg.juego.separacion_min_entre_premios,
                      rng=rng)


class RngEspia:
    """`rng` falso que GUARDA la llamada a `choices` tal cual la recibió.

    Así el golden compara la tómbola **por igualdad de listas** (población y
    pesos, en orden) en vez de inferirla de la distribución de mil sorteos.
    `indice` elige qué elemento devuelve: 0 = el primer premio, -1 = el último
    de la población, que con peso de consuelo es el propio consuelo (None).
    """

    def __init__(self, indice: int = 0):
        self.llamadas: list[tuple[list, list, int]] = []
        self.indice = indice

    def choices(self, population, weights=None, k=1):
        self.llamadas.append((list(population), list(weights), k))
        return [population[self.indice]]


def premios_prueba():
    return [
        Premio(id="grande", nombre="Premio grande", peso=1, stock=2, tope_diario=1),
        Premio(id="mayor", nombre="Premio mayor", peso=1, stock=1),
        Premio(id="tacos", nombre="Tacos", peso=10, stock=None),
        Premio(id="futuro", nombre="Solo el finde", peso=1, stock=5,
               desde=date(2026, 9, 19), hasta=date(2026, 9, 20)),
    ]


class TestInventario(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self.tmp.name)
        self.inv = Inventario(premios_prueba(), self.carpeta, hora_inicio_dia=6, rng=random.Random(1))
        self.t = datetime(2026, 9, 15, 20, 30)

    def tearDown(self):
        self.tmp.cleanup()

    # -- día operativo ------------------------------------------------------ #

    def test_dia_operativo_antes_de_la_hora_de_inicio_es_el_dia_anterior(self):
        self.assertEqual(self.inv.dia_operativo(datetime(2026, 9, 16, 1, 30)), date(2026, 9, 15))
        self.assertEqual(self.inv.dia_operativo(datetime(2026, 9, 16, 6, 0)), date(2026, 9, 16))
        self.assertEqual(self.inv.dia_operativo(datetime(2026, 9, 16, 23, 59)), date(2026, 9, 16))

    # -- disponibilidad ---------------------------------------------------- #

    def test_fechas_desde_hasta(self):
        self.assertEqual(self.inv.motivo_no_disponible(self.inv.premios["futuro"], self.t), "desde 19/09")
        self.assertEqual(self.inv.motivo_no_disponible(self.inv.premios["futuro"], datetime(2026, 9, 19, 12)), "")
        # La madrugada del 21 sigue siendo día operativo 20 -> disponible
        self.assertEqual(self.inv.motivo_no_disponible(self.inv.premios["futuro"], datetime(2026, 9, 21, 2)), "")
        self.assertEqual(self.inv.motivo_no_disponible(self.inv.premios["futuro"], datetime(2026, 9, 21, 12)), "fecha vencida")

    def test_stock_y_tope_diario(self):
        grande = self.inv.premios["grande"]
        self.inv.emitir(grande, self.t)
        self.assertEqual(self.inv.motivo_no_disponible(grande, self.t), "tope de hoy")
        # SIN horario configurado, la Fase 4d reparte el cupo del día sobre el día
        # operativo completo (06:00 a 06:00): la única pieza de 'grande' se abre
        # en el punto medio, a las 18:00. Antes del 2026-09-16 estaba disponible
        # desde el primer minuto del día; esta es la conducta nueva y se ancla por
        # igualdad para que nadie la cambie sin darse cuenta.
        self.assertEqual(self.inv.motivo_no_disponible(grande, datetime(2026, 9, 16, 12)),
                         "se libera a las 18:00")
        manana = datetime(2026, 9, 16, 18, 30)
        self.assertEqual(self.inv.motivo_no_disponible(grande, manana), "")
        self.inv.emitir(grande, manana)
        self.assertEqual(self.inv.restantes(grande), 0)
        self.assertEqual(self.inv.motivo_no_disponible(grande, datetime(2026, 9, 17, 18, 30)),
                         "agotado")

    def test_ilimitado_nunca_se_agota(self):
        tacos = self.inv.premios["tacos"]
        for _ in range(50):
            self.inv.emitir(tacos, self.t)
        self.assertIsNone(self.inv.restantes(tacos))
        self.assertEqual(self.inv.motivo_no_disponible(tacos, self.t), "")

    def test_probabilidades_suman_100_y_respetan_pesos(self):
        probs = self.inv.probabilidades(self.t)
        self.assertNotIn("futuro", probs)
        self.assertAlmostEqual(sum(probs.values()), 100.0)
        self.assertAlmostEqual(probs["tacos"], 100 * 10 / 12)
        self.assertAlmostEqual(probs["grande"], 100 * 1 / 12)

    # -- sorteo --------------------------------------------------------------- #

    def test_sortear_devuelve_none_sin_disponibles(self):
        inv = Inventario([Premio(id="u", nombre="Único", peso=1, stock=1)], self.carpeta / "b")
        self.assertEqual(inv.sortear(self.t).id, "u")
        inv.emitir(inv.premios["u"], self.t)
        self.assertIsNone(inv.sortear(self.t))

    def test_distribucion_aproximada(self):
        inv = Inventario([
            Premio(id="a", nombre="A", peso=1),
            Premio(id="b", nombre="B", peso=3),
        ], self.carpeta / "d", rng=random.Random(42))
        conteo = {"a": 0, "b": 0}
        for _ in range(4000):
            conteo[inv.sortear(self.t).id] += 1
        proporcion = conteo["b"] / 4000
        self.assertGreater(proporcion, 0.70)
        self.assertLess(proporcion, 0.80)

    # -- peso propio del boleto de consuelo (pieza A, Fase 4c) ---------------- #

    def test_sortear_con_peso_de_consuelo_mete_none_en_la_tombola(self):
        """UNA sola elección ponderada: premios disponibles + [None], pesos + [peso].

        Se ancla la llamada a `choices` **por igualdad de listas**, no por
        presencia: si el consuelo se sorteara aparte (dos tiradas) o entrara con
        otro peso, esta igualdad cae.
        """
        espia = RngEspia()
        inv = Inventario(premios_prueba(), self.carpeta / "peso", hora_inicio_dia=6,
                         rng=espia, peso_consuelo=217)
        disponibles = inv.disponibles(self.t)
        self.assertEqual([p.id for p in disponibles], ["grande", "mayor", "tacos"])
        inv.sortear(self.t)
        self.assertEqual(len(espia.llamadas), 1)
        poblacion, pesos, k = espia.llamadas[0]
        self.assertEqual(poblacion, disponibles + [None])
        self.assertEqual(pesos, [p.peso for p in disponibles] + [217])
        self.assertEqual(k, 1)
        # Y si la elección cae en ese último papelito, el sorteo devuelve el consuelo.
        espia.indice = -1
        self.assertIsNone(inv.sortear(self.t))

    def test_sin_peso_de_consuelo_la_tombola_es_solo_de_premios(self):
        """Con `peso_consuelo` = 0 (el valor por omisión) nada cambia."""
        espia = RngEspia()
        inv = Inventario(premios_prueba(), self.carpeta / "sinpeso", hora_inicio_dia=6, rng=espia)
        self.assertEqual(inv.peso_consuelo, 0)
        disponibles = inv.disponibles(self.t)
        inv.sortear(self.t)
        poblacion, pesos, _ = espia.llamadas[0]
        self.assertEqual(poblacion, disponibles)
        self.assertEqual(pesos, [p.peso for p in disponibles])
        self.assertTrue(all(p is not None for p in poblacion))

    def test_sin_premios_disponibles_devuelve_consuelo_sin_sortear(self):
        """Agotado todo, el consuelo es seguro y no se llama a `choices`."""
        espia = RngEspia()
        inv = Inventario([Premio(id="u", nombre="Único", peso=1, stock=1)],
                         self.carpeta / "vacio", rng=espia, peso_consuelo=217)
        self.assertEqual(inv.sortear(self.t).id, "u")
        inv.emitir(inv.premios["u"], self.t)
        self.assertIsNone(inv.sortear(self.t))
        self.assertEqual(len(espia.llamadas), 1)        # la segunda no pasó por el rng
        self.assertEqual(inv.probabilidad_consuelo(self.t), 100.0)

    def test_el_consuelo_entra_en_el_denominador_de_las_probabilidades(self):
        """Los pesos de los premios no cambian; el denominador sí, y suma 100 con el consuelo."""
        inv = Inventario(premios_prueba(), self.carpeta / "probs", hora_inicio_dia=6,
                         peso_consuelo=217)
        probs = inv.probabilidades(self.t)                # pesos disponibles: 1 + 1 + 10 = 12
        self.assertAlmostEqual(probs["tacos"], 100 * 10 / 229)
        self.assertAlmostEqual(probs["grande"], 100 * 1 / 229)
        self.assertAlmostEqual(inv.probabilidad_consuelo(self.t), 100 * 217 / 229)
        self.assertAlmostEqual(sum(probs.values()) + inv.probabilidad_consuelo(self.t), 100.0)
        # Lo mismo, visto desde el resumen que imprime el boleto de inventario.
        r = inv.resumen(self.t)
        self.assertEqual(r.peso_consuelo, 217)
        self.assertAlmostEqual(r.probabilidad_consuelo, 100 * 217 / 229)
        self.assertAlmostEqual(
            sum(f.probabilidad for f in r.premios) + r.probabilidad_consuelo, 100.0)

    def test_el_consuelo_no_toca_stock_ni_tope_pero_gasta_folio(self):
        dia = self.inv.dia_operativo(self.t)
        antes_restantes = {p.id: self.inv.restantes(p) for p in self.inv.premios.values()}
        antes_hoy = {p.id: self.inv.entregados_en_dia(p.id, dia) for p in self.inv.premios.values()}
        b = self.inv.emitir(None, self.t)
        self.assertIsNone(b.premio)
        self.assertEqual(b.folio, 1)
        self.assertEqual({p.id: self.inv.restantes(p) for p in self.inv.premios.values()},
                         antes_restantes)
        self.assertEqual({p.id: self.inv.entregados_en_dia(p.id, dia) for p in self.inv.premios.values()},
                         antes_hoy)
        self.assertEqual(self.inv.boletos_en_dia(dia), 1)
        # Y así queda en disco: un folio gastado y cero premios entregados.
        otro = Inventario(premios_prueba(), self.carpeta)
        self.assertEqual(otro.folio_actual, 1)
        self.assertEqual({p.id: otro.entregados(p.id) for p in otro.premios.values()},
                         {p.id: 0 for p in otro.premios.values()})
        self.assertEqual(otro.boletos_en_dia(dia), 1)

    def test_distribucion_aproximada_con_peso_de_consuelo(self):
        """Con el rng de verdad: 3 papelitos de premio contra 7 de consuelo."""
        inv = Inventario([Premio(id="a", nombre="A", peso=1), Premio(id="b", nombre="B", peso=2)],
                         self.carpeta / "dist", rng=random.Random(7), peso_consuelo=7)
        consuelos = sum(1 for _ in range(4000) if inv.sortear(self.t) is None)
        self.assertGreater(consuelos / 4000, 0.66)
        self.assertLess(consuelos / 4000, 0.74)

    def test_sorteo_nunca_da_premio_no_disponible(self):
        # El 'mayor' solo tiene 1: tras emitirlo, no debe volver a salir jamás.
        mayor = self.inv.premios["mayor"]
        self.inv.emitir(mayor, self.t)
        for _ in range(500):
            p = self.inv.sortear(self.t)
            self.assertIsNotNone(p)
            self.assertNotEqual(p.id, "mayor")

    # -- emisión y persistencia ------------------------------------------------ #

    def test_emitir_incrementa_folio_y_persiste(self):
        b1 = self.inv.emitir(self.inv.premios["tacos"], self.t)
        b2 = self.inv.emitir(None, self.t)  # consuelo también consume folio
        self.assertEqual((b1.folio, b2.folio), (1, 2))
        self.assertEqual(b1.folio_texto, "00001")
        self.assertEqual(self.inv.boletos_en_dia(b1.dia), 2)

        otro = Inventario(premios_prueba(), self.carpeta)
        self.assertEqual(otro.folio_actual, 2)
        self.assertEqual(otro.entregados("tacos"), 1)
        self.assertEqual(otro.boletos_en_dia(b1.dia), 2)

    def test_revertir_regresa_stock_pero_no_reusa_folio(self):
        mayor = self.inv.premios["mayor"]
        b = self.inv.emitir(mayor, self.t)
        self.assertEqual(self.inv.restantes(mayor), 0)
        self.inv.revertir(b)
        self.assertEqual(b.estado, "error_conexion")
        self.assertEqual(self.inv.restantes(mayor), 1)
        self.assertEqual(self.inv.entregados_en_dia("mayor", b.dia), 0)
        self.assertEqual(self.inv.boletos_en_dia(b.dia), 0)
        siguiente = self.inv.emitir(mayor, self.t)
        self.assertEqual(siguiente.folio, 2)
        # Revertir dos veces no duplica la devolución
        self.inv.revertir(b)
        self.assertEqual(self.inv.restantes(mayor), 0)

    def test_confirmar_no_se_puede_revertir(self):
        b = self.inv.emitir(self.inv.premios["mayor"], self.t)
        self.inv.confirmar(b)
        self.inv.revertir(b)
        self.assertEqual(b.estado, "impreso")
        self.assertEqual(self.inv.restantes(self.inv.premios["mayor"]), 0)

    def test_incierto_conserva_el_premio_como_entregado(self):
        b = self.inv.emitir(self.inv.premios["mayor"], self.t)
        self.inv.marcar_incierto(b)
        self.assertEqual(b.estado, "incierto")
        self.assertEqual(self.inv.restantes(self.inv.premios["mayor"]), 0)

    def test_bitacora_csv(self):
        b = self.inv.emitir(self.inv.premios["tacos"], self.t)
        self.inv.confirmar(b)
        c = self.inv.emitir(None, self.t)
        self.inv.revertir(c)
        with open(self.inv.ruta_log, encoding="utf-8", newline="") as f:
            filas = list(csv.DictReader(f))
        self.assertEqual([r["evento"] for r in filas], ["emitido", "impreso", "emitido", "error_conexion"])
        self.assertEqual(filas[0]["folio"], "00001")
        self.assertEqual(filas[0]["premio_id"], "tacos")
        self.assertEqual(filas[2]["premio_id"], "consuelo")
        self.assertEqual(filas[0]["dia_operativo"], "2026-09-15")

    def test_estado_corrupto_se_respalda_y_arranca_en_cero(self):
        self.inv.emitir(self.inv.premios["tacos"], self.t)
        self.inv.ruta_estado.write_text("{esto no es json", encoding="utf-8")
        otro = Inventario(premios_prueba(), self.carpeta)
        self.assertEqual(otro.folio_actual, 0)
        self.assertTrue((self.carpeta / "estado.corrupto").exists())

    def test_guardado_atomico_no_deja_tmp(self):
        self.inv.emitir(self.inv.premios["tacos"], self.t)
        self.assertFalse((self.carpeta / "estado.tmp").exists())
        datos = json.loads(self.inv.ruta_estado.read_text(encoding="utf-8"))
        self.assertEqual(datos["folio"], 1)
        self.assertEqual(datos["entregados"]["tacos"], 1)

    def test_premio_nuevo_en_config_arranca_en_cero(self):
        self.inv.emitir(self.inv.premios["tacos"], self.t)
        nuevos = premios_prueba() + [Premio(id="nuevo", nombre="Nuevo", peso=1, stock=3)]
        otro = Inventario(nuevos, self.carpeta)
        self.assertEqual(otro.restantes(otro.premios["nuevo"]), 3)
        self.assertEqual(otro.entregados("tacos"), 1)

    def test_resumen(self):
        self.inv.emitir(self.inv.premios["grande"], self.t)
        r = self.inv.resumen(self.t)
        por_id = {f.premio.id: f for f in r.premios}
        self.assertEqual(r.folio_actual, 1)
        self.assertEqual(r.boletos_hoy, 1)
        self.assertEqual(por_id["grande"].hoy, 1)
        self.assertEqual(por_id["grande"].restantes, 1)
        self.assertFalse(por_id["grande"].disponible)
        self.assertEqual(por_id["grande"].motivo, "tope de hoy")
        self.assertEqual(por_id["grande"].probabilidad, 0.0)
        self.assertTrue(por_id["tacos"].disponible)
        self.assertIsNone(por_id["tacos"].restantes)

    def test_reiniciar(self):
        self.inv.emitir(self.inv.premios["mayor"], self.t)
        self.inv.reiniciar()
        self.assertEqual(self.inv.folio_actual, 0)
        self.assertEqual(self.inv.restantes(self.inv.premios["mayor"]), 1)
        otro = Inventario(premios_prueba(), self.carpeta)
        self.assertEqual(otro.folio_actual, 0)

    # -- disco que falla ------------------------------------------------------- #

    def test_emitir_sin_disco_no_consume_nada(self):
        mayor = self.inv.premios["mayor"]
        with mock.patch("ruleta.inventario.os.replace", side_effect=OSError(28, "No space left on device")):
            with self.assertRaises(ErrorPersistencia):
                self.inv.emitir(mayor, self.t)
        self.assertEqual(self.inv.folio_actual, 0)
        self.assertEqual(self.inv.restantes(mayor), 1)
        self.assertEqual(self.inv.boletos_en_dia(self.inv.dia_operativo(self.t)), 0)
        self.assertFalse(self.inv.ruta_log.exists())
        # Cuando el disco vuelve, todo sigue funcionando y el folio empieza en 1.
        self.assertEqual(self.inv.emitir(mayor, self.t).folio, 1)

    def test_revertir_sin_disco_no_lanza(self):
        b = self.inv.emitir(self.inv.premios["mayor"], self.t)
        with mock.patch("ruleta.inventario.os.replace", side_effect=OSError(30, "Read-only")):
            self.inv.revertir(b)
        self.assertEqual(self.inv.restantes(self.inv.premios["mayor"]), 1)

    def test_bitacora_que_no_se_puede_escribir_no_lanza(self):
        self.inv.ruta_log.mkdir()      # abrirla como archivo falla con OSError
        b = self.inv.emitir(self.inv.premios["tacos"], self.t)
        self.inv.confirmar(b)
        self.assertEqual(b.folio, 1)
        self.assertEqual(self.inv.entregados("tacos"), 1)
        self.assertEqual(self.inv.pendientes(), [])   # leerla tampoco tira el programa

    # -- pendientes y liberar --------------------------------------------------- #

    def test_pendientes_y_liberar(self):
        mayor, tacos = self.inv.premios["mayor"], self.inv.premios["tacos"]
        b1 = self.inv.emitir(tacos, self.t)
        self.inv.confirmar(b1)
        b2 = self.inv.emitir(mayor, self.t)
        self.inv.marcar_incierto(b2)
        b3 = self.inv.emitir(tacos, self.t)            # se queda en 'emitido' (apagón)
        b4 = self.inv.emitir(None, self.t)             # consuelo: nunca es pendiente
        pend = self.inv.pendientes()
        self.assertEqual([(p.folio, p.evento) for p in pend], [(2, "incierto"), (3, "emitido")])
        self.assertEqual(pend[0].premio_nombre, "Premio mayor")
        self.assertEqual(self.inv.restantes(mayor), 0)

        liberado = self.inv.liberar(2)
        self.assertEqual(liberado.evento, "liberado")
        self.assertEqual(self.inv.restantes(mayor), 1)
        self.assertEqual(self.inv.entregados_en_dia("mayor", b2.dia), 0)
        self.assertEqual(self.inv.boletos_en_dia(b2.dia), 3)
        self.assertEqual([p.folio for p in self.inv.pendientes()], [3])
        # Persistió y la bitácora lo registra
        otro = Inventario(premios_prueba(), self.carpeta)
        self.assertEqual(otro.restantes(mayor), 1)
        with open(self.inv.ruta_log, encoding="utf-8", newline="") as f:
            eventos = [(r["folio"], r["evento"]) for r in csv.DictReader(f)]
        self.assertEqual(eventos[-1], ("00002", "liberado"))
        # No se puede liberar dos veces ni liberar uno impreso o inexistente
        with self.assertRaises(ValueError):
            self.inv.liberar(2)
        with self.assertRaises(ValueError):
            self.inv.liberar(1)
        with self.assertRaises(ValueError):
            self.inv.liberar(99)
        self.assertEqual(b4.folio, 4)

    def test_liberar_premio_que_ya_no_esta_en_config(self):
        b = self.inv.emitir(self.inv.premios["mayor"], self.t)
        self.inv.marcar_incierto(b)
        sin_mayor = [p for p in premios_prueba() if p.id != "mayor"]
        otro = Inventario(sin_mayor, self.carpeta)
        self.assertEqual(otro.entregados("mayor"), 1)
        otro.liberar(1)
        self.assertEqual(otro.entregados("mayor"), 0)

    def test_resumen_incluye_pendientes(self):
        b = self.inv.emitir(self.inv.premios["tacos"], self.t)
        self.inv.marcar_incierto(b)
        r = self.inv.resumen(self.t)
        self.assertEqual([p.folio for p in r.pendientes], [1])


class TestRepartoPorHoras(unittest.TestCase):
    """El cupo del día se abre poco a poco (Fase 4d, dictado del 2026-09-16).

    Todos los vectores salen del `config.json` real del repositorio: los siete
    premios del evento, el horario 12:00–23:00, las franjas y la separación
    mínima. Nada de horas inventadas: la hora entra siempre por parámetro, así
    que estas pruebas no dependen del reloj de la máquina.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.carpeta = Path(self.tmp.name)
        self.inv = inventario_del_evento(self.carpeta, rng=random.Random(5))
        self.dia = date(2026, 9, 24)

    def tearDown(self):
        self.tmp.cleanup()

    def horas(self, premio_id, dia=None):
        instantes = self.inv.instantes_del_dia(self.inv.premios[premio_id], dia or self.dia)
        return None if instantes is None else [i.strftime("%H:%M") for i in instantes]

    def ventanas(self, premio_id, dia):
        """Las franjas de ese premio ESE día, como texto "HH:MM-HH:MM"."""
        return [f"{i:%H:%M}-{f:%H:%M}"
                for i, f, _ in self.inv.franjas_del_dia(self.inv.premios[premio_id], dia)]

    def cupo_que_abre_el_dia(self, premio, dia=None):
        """Lo que el reloj DEBE abrir ese día: la suma de los topes de sus franjas.

        Derivado, no escrito a mano: un premio sin franjas abre su `tope_diario`
        y uno con franjas abre lo que suman las de ESE día (cero si no tiene
        ninguna, como `silla_extra` el jueves).
        """
        dia = dia or self.dia
        if not premio.franjas:
            return premio.tope_diario
        return sum(f.tope for _, _, f in self.inv.franjas_del_dia(premio, dia))

    def en(self, hora, minuto):
        return datetime(self.dia.year, self.dia.month, self.dia.day, hora, minuto)

    # -- (a) las horas de liberación ---------------------------------------- #

    def test_instantes_de_liberacion_del_evento_real(self):
        """Igualdad de LISTAS, no «hay once»: el orden y cada hora importan.

        Son los puntos medios de cada tramo de las once horas del evento, que es
        lo que el §2 del documento del evento publica en su tabla.
        """
        self.assertEqual(self.horas("agua"),
                         ["12:30", "13:30", "14:30", "15:30", "16:30", "17:30",
                          "18:30", "19:30", "20:30", "21:30", "22:30"])
        self.assertEqual(self.horas("cerveza"),
                         ["12:33", "13:39", "14:45", "15:51", "16:57",
                          "18:03", "19:09", "20:15", "21:21", "22:27"])
        self.assertEqual(self.horas("tacos3"), ["13:22", "16:07", "18:52", "21:37"])
        self.assertEqual(self.horas("tacos2"), self.horas("tacos3"))
        # Los de franja se abren AL EMPEZAR su franja, no a la mitad. Horas
        # SUELTAS desde el 2026-09-22 (día 2, paso 1) y DISTINTAS POR DÍA desde
        # el paso 2 de esa tarde: estas son las del **jueves 24**, y no las del
        # martes. Las dos entradas de reposición no abren nada ese día —sus
        # franjas son del martes y el miércoles—, así que devuelven lista vacía.
        self.assertEqual(self.horas("hielera"), ["19:36"])
        self.assertEqual(self.horas("silla"), ["13:26", "19:11"])
        self.assertEqual(self.horas("silla_extra"), [])
        self.assertEqual(self.horas("bbq"), ["14:37", "20:52"])
        self.assertEqual(self.horas("bbq_extra"), [])
        # Y cada premio abre exactamente el cupo que le toca ESE día, ni una
        # pieza más: el `tope_diario` si no lleva franjas, y lo que suman las
        # franjas de ese día si las lleva.
        self.assertEqual({p.id: len(self.horas(p.id)) for p in self.inv.premios.values()},
                         {p.id: self.cupo_que_abre_el_dia(p) for p in self.inv.premios.values()})

    def test_las_franjas_de_cada_dia_del_evento(self):
        """Día 2 paso 2 (2026-09-22): cada día tiene SUS horas, y solo las suyas.

        Es el golden del campo `dias`. Se ancla el **mapa entero por igualdad**
        —los cuatro días que quedan del evento, con las ventanas de los cinco
        premios grandes en orden— y, sobre todo, que el **lunes 21** y el
        **sábado 26** no tengan **ninguna**: el lunes ya pasó y sus horas viejas
        no deben resucitar, y el sábado el evento ya cerró.

        Las horas las dictó el usuario el 2026-09-22 por la tarde; la ventana de
        cada pieza dura dos horas, menos las que llegan al cierre.
        """
        grandes = ("hielera", "silla", "silla_extra", "bbq", "bbq_extra")
        mapa = {dia: {pid: self.ventanas(pid, date(2026, 9, dia)) for pid in grandes
                      if self.ventanas(pid, date(2026, 9, dia))}
                for dia in (21, 22, 23, 24, 25, 26)}
        self.assertEqual(mapa, {
            21: {},
            22: {"silla": ["13:17-15:17", "19:23-21:23"],
                 "silla_extra": ["16:08-18:08"],
                 "bbq": ["14:41-16:41", "20:47-22:47"],
                 "bbq_extra": ["17:34-19:34"]},
            23: {"silla": ["13:09-15:09", "19:38-21:38"],
                 "silla_extra": ["16:21-18:21"],
                 "bbq": ["14:52-16:52", "20:19-22:19"]},
            24: {"hielera": ["19:36-23:00"],
                 "silla": ["13:26-15:26", "19:11-21:11"],
                 "bbq": ["14:37-16:37", "20:52-22:52"]},
            25: {"hielera": ["20:04-23:00"],
                 "silla": ["13:04-15:04", "19:31-21:31"],
                 "bbq": ["14:58-16:58", "21:06-23:00"]},
            26: {},
        })
        # El reparto por día cuadra con lo que dictó el usuario: 10 sillas y 9
        # sets entre el martes y el viernes, que es lo que queda en la bodega.
        # Es un censo DERIVADO de las franjas, no una lista copiada.
        por_dia = {dia: (len(self.ventanas("silla", date(2026, 9, dia)))
                         + len(self.ventanas("silla_extra", date(2026, 9, dia))),
                         len(self.ventanas("bbq", date(2026, 9, dia)))
                         + len(self.ventanas("bbq_extra", date(2026, 9, dia))))
                   for dia in (22, 23, 24, 25)}
        self.assertEqual(por_dia, {22: (3, 3), 23: (3, 2), 24: (2, 2), 25: (2, 2)})
        self.assertEqual((sum(s for s, _ in por_dia.values()),
                          sum(b for _, b in por_dia.values())), (10, 9))
        # Y un premio con franjas pero NINGUNA de ese día no existe ese día: no
        # se cae al reparto del tope_diario, que lo dejaría abierto todo el rato.
        lunes = datetime(2026, 9, 21, 20, 10)
        self.assertEqual(self.inv.instantes_del_dia(self.inv.premios["silla"], date(2026, 9, 21)), [])
        self.assertEqual(self.inv.liberadas(self.inv.premios["silla"], lunes), 0)
        self.assertEqual(self.inv.motivo_no_disponible(self.inv.premios["silla"], lunes),
                         "franjas de hoy cerradas")

    def test_una_franja_sin_dias_vale_todos_los_dias(self):
        """La promesa hacia atrás del campo `dias` (día 2 paso 2, 2026-09-22).

        Un `config.json` escrito antes de ese día **no trae `dias` en ninguna
        franja**, y eso tiene que seguir queriendo decir «todos los días». Si
        alguna vez pasara a querer decir «ningún día», una instalación vieja
        dejaría de dar premios **en silencio**: las franjas existirían, el stock
        estaría entero y ninguna pieza se abriría jamás.

        Se prueba con un inventario propio —no con el `config.json` del evento,
        que sí lleva días en todas— y en **cinco días distintos**, dentro y fuera
        de la ventana, por igualdad.
        """
        silla = Premio(id="silla", nombre="Silla", peso=100, stock=10, tope_diario=1,
                       franjas=[Franja(desde_hora="13:00", hasta_hora="16:00", tope=1)])
        vacia = Premio(id="vacia", nombre="Con lista vacía", peso=100, stock=10, tope_diario=1,
                       franjas=[Franja(desde_hora="13:00", hasta_hora="16:00", tope=1, dias=[])])
        inv = Inventario([silla, vacia], self.carpeta / "sindias", horario=HORARIO_EVENTO)
        for dia in (14, 15, 16, 22, 26):
            with self.subTest(dia=dia):
                d = date(2026, 9, dia)
                self.assertEqual(
                    {p.id: [f"{i:%H:%M}-{f:%H:%M}" for i, f, _ in inv.franjas_del_dia(p, d)]
                     for p in (silla, vacia)},
                    {"silla": ["13:00-16:00"], "vacia": ["13:00-16:00"]})
                dentro = datetime(2026, 9, dia, 14, 0)
                self.assertEqual({p.id: inv.motivo_no_disponible(p, dentro) for p in (silla, vacia)},
                                 {"silla": "", "vacia": ""})
                fuera = datetime(2026, 9, dia, 12, 30)
                self.assertEqual({p.id: inv.motivo_no_disponible(p, fuera) for p in (silla, vacia)},
                                 {"silla": "su franja abre a las 13:00",
                                  "vacia": "su franja abre a las 13:00"})

    def test_instantes_de_liberacion_es_una_funcion_pura(self):
        """Puntos medios, con igualdad de listas y los casos degenerados."""
        inicio, fin = datetime(2026, 9, 24, 12), datetime(2026, 9, 24, 23)
        self.assertEqual([i.strftime("%H:%M") for i in instantes_de_liberacion(inicio, fin, 1)],
                         ["17:30"])
        self.assertEqual([i.strftime("%H:%M") for i in instantes_de_liberacion(inicio, fin, 2)],
                         ["14:45", "20:15"])
        self.assertEqual(instantes_de_liberacion(inicio, fin, 0), [])
        self.assertEqual(instantes_de_liberacion(inicio, fin, -3), [])
        self.assertEqual(instantes_de_liberacion(fin, inicio, 4), [])
        self.assertEqual(instantes_de_liberacion(inicio, inicio, 4), [])

    # -- (b) liberadas y disponibles a horas concretas ----------------------- #

    def test_liberadas_y_disponibles_a_horas_concretas(self):
        agua = self.inv.premios["agua"]
        self.assertEqual(self.inv.liberadas(agua, self.en(12, 29)), 0)
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(12, 29)),
                         "se libera a las 12:30")
        self.assertEqual(self.inv.liberadas(agua, self.en(12, 30)), 1)
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(12, 30)), "")
        # A las 14:00 hay dos abiertas; con una entregada, queda una.
        self.inv.emitir(agua, self.en(12, 45))
        self.assertEqual(self.inv.liberadas(agua, self.en(14, 0)), 2)
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(14, 0)), "")
        # Entregadas las dos, hay que esperar a la tercera: no se adelanta nada.
        self.inv.emitir(agua, self.en(14, 0))
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(14, 0)),
                         "se libera a las 14:30")
        self.assertEqual(self.inv.proxima_liberacion(agua, self.en(14, 0)), self.en(14, 30))
        # Y a las 22:31 ya no queda ninguna por abrir.
        self.assertEqual(self.inv.proxima_liberacion(agua, self.en(22, 31)), None)
        self.assertEqual(self.inv.liberadas(agua, self.en(22, 31)), 11)

    def test_lo_abierto_y_no_ganado_no_se_pierde_pero_no_adelanta(self):
        """Regla dictada el 2026-09-16, anclada por igualdad de conjuntos."""
        agua = self.inv.premios["agua"]
        # Nadie juega en toda la tarde: a las 17:00 hay cinco aguas esperando
        # (12:30, 13:30, 14:30, 15:30 y 16:30).
        self.assertEqual(self.inv.liberadas(agua, self.en(17, 0)), 5)
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(17, 0)), "")
        # Se ganan las cinco y la sexta NO se adelanta: toca a las 17:30.
        for _ in range(5):
            self.inv.emitir(agua, self.en(17, 0))
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(17, 0)),
                         "se libera a las 17:30")
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(17, 30)), "")

    def test_fuera_del_horario_no_hay_premios_y_el_sorteo_da_consuelo(self):
        """Pieza C: antes de las 12:00 y desde las 23:00 en punto, nada."""
        espia = RngEspia()
        inv = inventario_del_evento(self.carpeta / "horario", rng=espia)
        for hora, minuto in ((11, 59), (6, 0), (23, 0), (23, 30)):
            with self.subTest(hora=f"{hora:02d}:{minuto:02d}"):
                t = self.en(hora, minuto)
                self.assertFalse(inv.dentro_del_horario(t))
                self.assertEqual(inv.disponibles(t), [])
                # El jueves 24 las dos entradas de reposición ya están vencidas
                # (`silla_extra` acaba el 23 y `bbq_extra` el 22), y la fecha se
                # mira ANTES que el horario: por eso son dos motivos y no uno.
                self.assertEqual({f.motivo for f in inv.resumen(t).premios},
                                 {"fuera de horario", "fecha vencida"})
                self.assertEqual({f.premio.id for f in inv.resumen(t).premios
                                  if f.motivo == "fecha vencida"},
                                 {"silla_extra", "bbq_extra"})
                self.assertIsNone(inv.sortear(t))
        self.assertEqual(espia.llamadas, [], "fuera de horario no se debe tirar la tómbola")
        # Y dentro sí: a las 12:30 el agua ya está abierta.
        self.assertTrue(inv.dentro_del_horario(self.en(12, 30)))
        self.assertEqual([p.id for p in inv.disponibles(self.en(12, 30))], ["agua"])
        self.assertEqual(inv.probabilidad_consuelo(self.en(23, 30)), 100.0)

    # -- (c) franjas --------------------------------------------------------- #

    def test_franjas_de_la_silla_del_evento_real(self):
        """Pieza B: la silla solo existe en la comida y en la cena.

        Las horas son las del **jueves 24** (`self.dia`), que desde el día 2
        paso 2 ya no son las del martes: 13:26 y 19:11.
        """
        silla = self.inv.premios["silla"]
        dentro = [(13, 26), (15, 25), (19, 11), (21, 10)]
        fuera = [(13, 25), (15, 26), (16, 0), (19, 10), (21, 11), (22, 30)]
        self.assertEqual([(h, m) for h, m in dentro
                          if self.inv.motivo_no_disponible(silla, self.en(h, m)) != ""], [])
        self.assertEqual([(h, m) for h, m in fuera
                          if self.inv.motivo_no_disponible(silla, self.en(h, m)) == ""], [])
        # Y el motivo dice a qué hora vuelve, o que ya no vuelve hoy.
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(13, 25)),
                         "su franja abre a las 13:26")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(15, 26)),
                         "su franja abre a las 19:11")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(22, 30)),
                         "franjas de hoy cerradas")
        # Las horas del MARTES no valen el jueves: es lo que trajo el campo
        # `dias`. A las 13:17 (martes) y a las 19:23 (martes) aquí no hay nada.
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(13, 17)),
                         "su franja abre a las 13:26")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(21, 20)),
                         "franjas de hoy cerradas")

    def test_el_tope_de_una_franja_se_respeta(self):
        """Ganada la silla de la comida, no sale otra hasta la franja de la cena."""
        silla = self.inv.premios["silla"]
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(13, 30)), "")
        self.inv.emitir(silla, self.en(13, 30))
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(13, 31)),
                         "se libera a las 19:11")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(15, 25)),
                         "se libera a las 19:11")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(19, 11)), "")
        # Y con las dos del día entregadas, manda el tope diario.
        self.inv.emitir(silla, self.en(19, 11))
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(20, 0)), "tope de hoy")

    def test_la_hielera_solo_desde_las_19_36_hasta_el_cierre(self):
        """Franja movida el 2026-09-22 (día 2, paso 1): era de 19:00 a 23:00."""
        hielera = self.inv.premios["hielera"]
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(19, 35)),
                         "su franja abre a las 19:36")
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(19, 36)), "")
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(22, 59)), "")
        # A las 23:00 cierra el evento entero, así que gana ese motivo.
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(23, 0)),
                         "fuera de horario")

    # -- (e) separación mínima entre premios --------------------------------- #

    def test_separacion_minima_entre_premios(self):
        """Dictado del 2026-09-16: «los premios no deben salir seguidos».

        A las **17:00 del jueves**, que desde el día 2 paso 2 es la hora que hay
        que usar para probar esto con el `config.json` real: entre las 16:37 y
        las 19:11 no hay ninguna pieza **forzada** abierta, y el forzado se salta
        la separación a propósito (`test_una_pieza_forzada_se_salta_la_separacion`).
        """
        agua = self.inv.premios["agua"]
        # Bajada de 3 minutos a 1 el 2026-09-22 (día 2, paso 1): el lunes 21 seis
        # de las 55 jugadas salieron de consuelo solo por esta regla.
        self.assertEqual(self.inv.separacion_min_entre_premios, 1)
        self.assertEqual(self.inv.forzados_abiertos(self.en(17, 0)), [])
        self.inv.confirmar(self.inv.emitir(agua, self.en(17, 0)))
        espia = RngEspia()
        self.inv.rng = espia
        self.assertEqual(self.inv.espera_separacion(self.en(17, 0)), 1.0)
        self.assertIsNone(self.inv.sortear(self.en(17, 0)))
        self.assertEqual(espia.llamadas, [], "durante la separación ni se tira la tómbola")
        self.assertEqual(self.inv.espera_separacion(self.en(17, 1)), 0.0)
        self.assertIsNotNone(self.inv.sortear(self.en(17, 1)))
        self.assertEqual(len(espia.llamadas), 1)
        # Los premios NO dejan de estar disponibles: lo que se frena es el sorteo.
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(17, 0)), "")

    def test_la_separacion_solo_la_marca_un_boleto_impreso(self):
        """Si el boleto no salió, el premio vuelve y no frena al siguiente."""
        agua = self.inv.premios["agua"]
        b = self.inv.emitir(agua, self.en(17, 0))
        self.assertEqual(self.inv.espera_separacion(self.en(17, 1)), 0.0)   # aún no confirmado
        self.inv.revertir(b)
        self.assertEqual(self.inv.espera_separacion(self.en(17, 1)), 0.0)
        # Un consuelo confirmado tampoco frena nada: no es un premio.
        self.inv.confirmar(self.inv.emitir(None, self.en(17, 1)))
        self.assertEqual(self.inv.espera_separacion(self.en(17, 2)), 0.0)

    def test_sin_separacion_configurada_no_hay_regla(self):
        inv = Inventario(list(self.inv.premios.values()), self.carpeta / "sinsep",
                         horario=HORARIO_EVENTO)
        self.assertEqual(inv.separacion_min_entre_premios, 0.0)
        inv.confirmar(inv.emitir(inv.premios["agua"], self.en(14, 0)))
        self.assertEqual(inv.espera_separacion(self.en(14, 0)), 0.0)

    def test_un_reloj_que_se_va_hacia_atras_no_bloquea_el_juego(self):
        """La Pi no tiene RTC: al arrancar puede creer que es otro día.

        Con el instante guardado en el FUTURO respecto de la hora actual, la
        resta da negativa; si eso contara como «faltan minutos», el kiosco se
        quedaría sin poder dar un solo premio.
        """
        self.inv.confirmar(self.inv.emitir(self.inv.premios["agua"], self.en(20, 0)))
        self.assertEqual(self.inv.espera_separacion(self.en(13, 0)), 0.0)
        espia = RngEspia()
        self.inv.rng = espia
        self.inv.sortear(self.en(13, 0))
        self.assertEqual(len(espia.llamadas), 1, "la tómbola sí se tiró")

    # -- (g) premios FORZADOS (día 2 paso 2, 2026-09-22) --------------------- #

    def test_una_pieza_forzada_se_la_lleva_la_siguiente_jugada_sin_tombola(self):
        """Dictado del usuario: «después de tal hora, el próximo juego se la saca».

        A las 14:00 del jueves la silla lleva abierta desde las 13:26. La jugada
        se la lleva **sin pasar por la tómbola**: se ancla que `choices` **no se
        llama** —por igualdad de la lista de llamadas, no «se llamó poco»— y que
        el premio devuelto es la silla.
        """
        espia = RngEspia()
        self.inv.rng = espia
        silla = self.inv.premios["silla"]
        self.assertTrue(silla.forzado)
        self.assertEqual([p.id for p in self.inv.forzados_abiertos(self.en(14, 0))], ["silla"])
        self.assertEqual(self.inv.sortear(self.en(14, 0)), silla)
        self.assertEqual(espia.llamadas, [], "una pieza forzada no se sortea, se entrega")
        # Y en cuanto se entrega deja de estar abierta: la siguiente jugada
        # vuelve a la tómbola de siempre (aquí, frenada por la separación).
        self.inv.confirmar(self.inv.emitir(silla, self.en(14, 0)))
        self.assertEqual(self.inv.forzados_abiertos(self.en(14, 1)), [])
        self.assertIsNotNone(self.inv.sortear(self.en(14, 1)))
        self.assertEqual(len(espia.llamadas), 1)

    def test_una_pieza_forzada_se_salta_la_separacion(self):
        """Decisión del usuario del 2026-09-22: la SIGUIENTE jugada, no la siguiente
        que pase el minuto. Es lo único que el forzado se salta a propósito."""
        espia = RngEspia()
        self.inv.rng = espia
        self.inv.confirmar(self.inv.emitir(self.inv.premios["agua"], self.en(14, 0)))
        self.assertEqual(self.inv.espera_separacion(self.en(14, 0)), 1.0)
        # Con la separación mordiendo, un premio NO forzado daría consuelo…
        self.assertEqual(self.inv.forzados_abiertos(self.en(14, 0)),
                         [self.inv.premios["silla"]])
        # …y aun así sale la silla, sin tirar la tómbola.
        self.assertEqual(self.inv.sortear(self.en(14, 0)).id, "silla")
        self.assertEqual(espia.llamadas, [])

    def test_con_dos_piezas_forzadas_abiertas_sale_primero_la_que_abrio_antes(self):
        """A las 19:40 del jueves están abiertas la silla (19:11) y la hielera (19:36).

        Se ancla **la ráfaga entera, jugada a jugada y por igualdad**, que es el
        riesgo que hay que tener escrito (ficha **F-283**): si nadie ha jugado en
        toda la tarde, **tres jugadas seguidas se llevan tres premios grandes**,
        una detrás de otra y **con la separación mínima mordiendo**.

        Son tres y no dos porque la silla del mediodía (13:26) **no se perdió**:
        lo que una franja abre y nadie gana se arrastra a la siguiente del mismo
        día (ficha F-269), así que a las 19:40 la silla tiene DOS piezas abiertas
        y su `tope_diario` es 2. El orden es el de apertura: la silla (19:11)
        antes que la hielera (19:36).
        """
        espia = RngEspia()
        self.inv.rng = espia
        t = self.en(19, 40)
        self.assertEqual([p.id for p in self.inv.forzados_abiertos(t)], ["silla", "hielera"])
        self.assertEqual(self.inv.liberadas(self.inv.premios["silla"], t), 2)
        salieron = []
        for _ in range(4):
            premio = self.inv.sortear(t)
            salieron.append(premio.id if premio else None)
            if premio is None:
                break
            self.inv.confirmar(self.inv.emitir(premio, t))
        self.assertEqual(salieron, ["silla", "silla", "hielera", None])
        # Y las tres salieron con la separación mínima pendiente desde la primera.
        self.assertEqual(self.inv.espera_separacion(t), 1.0)
        self.assertEqual(espia.llamadas, [], "ninguna de las tres pasó por la tómbola")

    def test_sin_piezas_forzadas_abiertas_la_tombola_es_la_de_siempre(self):
        """Control: a las 12:31 solo hay un agua abierta y NADA forzado.

        La llamada a `choices` se ancla **por igualdad de listas** —población y
        pesos, en orden—: si el forzado se colara aquí, o si cambiara el peso del
        consuelo, esta igualdad cae.
        """
        espia = RngEspia()
        self.inv.rng = espia
        t = self.en(12, 31)
        self.assertEqual(self.inv.forzados_abiertos(t), [])
        disponibles = self.inv.disponibles(t)
        self.assertEqual([p.id for p in disponibles], ["agua"])
        self.assertEqual(self.inv.sortear(t).id, "agua")
        self.assertEqual(espia.llamadas, [(disponibles + [None], [11, 10], 1)])

    def test_fuera_del_horario_no_hay_piezas_forzadas(self):
        """El horario del evento manda también sobre el forzado.

        A las 23:00 en punto la franja de la hielera sigue viva en el papel
        —acaba justo ahí— pero el evento ya cerró, así que no hay nada abierto y
        la jugada sale de consuelo.
        """
        espia = RngEspia()
        self.inv.rng = espia
        for hora, minuto in ((11, 59), (23, 0), (23, 30)):
            with self.subTest(hora=f"{hora:02d}:{minuto:02d}"):
                t = self.en(hora, minuto)
                self.assertEqual(self.inv.forzados_abiertos(t), [])
                self.assertIsNone(self.inv.sortear(t))
        self.assertEqual(espia.llamadas, [])

    def test_un_premio_sin_forzado_nunca_entra_por_esa_puerta(self):
        """Los cuatro premios chicos siguen sorteándose, estén abiertos o no."""
        chicos = [p for p in self.inv.premios.values() if not p.forzado]
        self.assertEqual([p.id for p in chicos], ["tacos3", "tacos2", "cerveza", "agua"])
        t = self.en(22, 0)      # los chicos abiertos, la hielera y el set BBQ de la noche
        self.assertEqual([p.id for p in self.inv.disponibles(t)],
                         ["hielera", "bbq", "tacos3", "tacos2", "cerveza", "agua"])
        self.assertEqual([p.id for p in self.inv.forzados_abiertos(t)], ["hielera", "bbq"])
        # Entregadas las piezas grandes, lo que queda es tómbola pura. Son TRES
        # boletos y no dos: el set BBQ tiene dos piezas abiertas a esa hora (la
        # de las 14:37, que nadie ganó, y la de las 20:52).
        for premio in (self.inv.premios["hielera"], self.inv.premios["bbq"],
                       self.inv.premios["bbq"]):
            self.inv.emitir(premio, t)
        espia = RngEspia()
        self.inv.rng = espia
        self.assertEqual(self.inv.forzados_abiertos(t), [])
        self.assertEqual(self.inv.sortear(t).id, "tacos3")
        poblacion, pesos, _ = espia.llamadas[0]
        self.assertEqual([getattr(p, "id", None) for p in poblacion],
                         ["tacos3", "tacos2", "cerveza", "agua", None])
        self.assertEqual(pesos, [4, 4, 10, 11, 10])

    # -- (f) persistencia del último premio ---------------------------------- #

    def test_el_ultimo_premio_sobrevive_al_reinicio(self):
        self.inv.confirmar(self.inv.emitir(self.inv.premios["agua"], self.en(17, 0)))
        guardado = json.loads(self.inv.ruta_estado.read_text(encoding="utf-8"))
        self.assertEqual(guardado["ultimo_premio"], "2026-09-24T17:00:00")
        otro = inventario_del_evento(self.carpeta)
        self.assertEqual(otro.espera_separacion(self.en(17, 0)), 1.0)
        self.assertIsNone(otro.sortear(self.en(17, 0)))
        self.assertEqual(otro.espera_separacion(self.en(17, 1)), 0.0)
        # Y reiniciar el inventario para un evento nuevo lo borra.
        otro.reiniciar()
        self.assertEqual(otro.espera_separacion(self.en(17, 0)), 0.0)
        self.assertIsNone(json.loads(otro.ruta_estado.read_text(encoding="utf-8"))["ultimo_premio"])

    def test_un_estado_viejo_sin_la_llave_carga_igual(self):
        """Un estado.json escrito antes de la Fase 4d no tiene 'ultimo_premio'."""
        viejo = {"version": 1, "folio": 16, "entregados": {"agua": 3},
                 "por_dia": {"2026-09-24": {"agua": 3}}, "boletos_por_dia": {"2026-09-24": 9},
                 "actualizado": "2026-09-24T17:00:00"}
        (self.carpeta / "estado.json").write_text(json.dumps(viejo), encoding="utf-8")
        inv = inventario_del_evento(self.carpeta)
        self.assertEqual((inv.folio_actual, inv.entregados("agua"), inv.boletos_en_dia(self.dia)),
                         (16, 3, 9))
        self.assertEqual(inv.espera_separacion(self.en(17, 0)), 0.0)
        # Y un valor ilegible tampoco tira el programa ni bloquea el juego.
        (self.carpeta / "estado.json").write_text(
            json.dumps({**viejo, "ultimo_premio": "ayer por la tarde"}), encoding="utf-8")
        roto = inventario_del_evento(self.carpeta)
        self.assertEqual(roto.folio_actual, 16)
        self.assertEqual(roto.espera_separacion(self.en(17, 0)), 0.0)

    # -- el resumen que imprime el boleto ------------------------------------ #

    def test_el_resumen_trae_las_liberadas_y_la_proxima(self):
        self.inv.emitir(self.inv.premios["agua"], self.en(14, 0))
        por_id = {f.premio.id: f for f in self.inv.resumen(self.en(14, 0)).premios}
        self.assertEqual((por_id["agua"].liberadas, por_id["agua"].hoy), (2, 1))
        self.assertEqual(por_id["agua"].proxima, self.en(14, 30))
        self.assertEqual((por_id["hielera"].liberadas, por_id["hielera"].proxima),
                         (0, self.en(19, 36)))
        self.assertEqual(por_id["silla"].liberadas, 1)
        # El set BBQ del jueves abre a las 14:37: a las 14:00 no hay ninguno.
        self.assertEqual((por_id["bbq"].liberadas, por_id["bbq"].proxima),
                         (0, self.en(14, 37)))
        # Y las dos entradas de reposición no abren NADA el jueves: sus franjas
        # son del martes y del miércoles, así que ni tienen piezas abiertas ni
        # tienen una siguiente hora que anunciar.
        self.assertEqual((por_id["silla_extra"].liberadas, por_id["silla_extra"].proxima),
                         (0, None))
        self.assertEqual((por_id["bbq_extra"].liberadas, por_id["bbq_extra"].proxima),
                         (0, None))
        # A las 22:45 ya no queda nada por abrir en todo el día.
        self.assertEqual([f.premio.id for f in self.inv.resumen(self.en(22, 45)).premios
                          if f.proxima is not None], [])

    def test_un_premio_sin_tope_ni_franjas_no_se_reparte(self):
        inv = Inventario([Premio(id="libre", nombre="Libre", peso=1)], self.carpeta / "libre",
                         horario=HORARIO_EVENTO)
        t = self.en(12, 1)
        self.assertIsNone(inv.liberadas(inv.premios["libre"], t))
        self.assertIsNone(inv.proxima_liberacion(inv.premios["libre"], t))
        self.assertEqual(inv.motivo_no_disponible(inv.premios["libre"], t), "")
        self.assertIsNone(inv.resumen(t).premios[0].liberadas)


if __name__ == "__main__":
    unittest.main()
