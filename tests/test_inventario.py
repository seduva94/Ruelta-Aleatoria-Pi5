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
        # Los de franja se abren AL EMPEZAR su franja, no a la mitad.
        self.assertEqual(self.horas("hielera"), ["19:00"])
        self.assertEqual(self.horas("silla"), ["13:00", "19:00"])
        self.assertEqual(self.horas("bbq"), ["13:00", "19:00"])
        # Y cada premio abre exactamente su cupo del día, ni una pieza más.
        self.assertEqual({p.id: len(self.horas(p.id)) for p in self.inv.premios.values()},
                         {p.id: p.tope_diario for p in self.inv.premios.values()})

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
                self.assertEqual({f.motivo for f in inv.resumen(t).premios}, {"fuera de horario"})
                self.assertIsNone(inv.sortear(t))
        self.assertEqual(espia.llamadas, [], "fuera de horario no se debe tirar la tómbola")
        # Y dentro sí: a las 12:30 el agua ya está abierta.
        self.assertTrue(inv.dentro_del_horario(self.en(12, 30)))
        self.assertEqual([p.id for p in inv.disponibles(self.en(12, 30))], ["agua"])
        self.assertEqual(inv.probabilidad_consuelo(self.en(23, 30)), 100.0)

    # -- (c) franjas --------------------------------------------------------- #

    def test_franjas_de_la_silla_del_evento_real(self):
        """Pieza B: la silla solo existe en la comida y en la cena."""
        silla = self.inv.premios["silla"]
        dentro = [(13, 0), (15, 59), (19, 0), (21, 59)]
        fuera = [(12, 59), (16, 0), (16, 1), (18, 59), (22, 0), (22, 30)]
        self.assertEqual([(h, m) for h, m in dentro
                          if self.inv.motivo_no_disponible(silla, self.en(h, m)) != ""], [])
        self.assertEqual([(h, m) for h, m in fuera
                          if self.inv.motivo_no_disponible(silla, self.en(h, m)) == ""], [])
        # Y el motivo dice a qué hora vuelve, o que ya no vuelve hoy.
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(12, 59)),
                         "su franja abre a las 13:00")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(16, 1)),
                         "su franja abre a las 19:00")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(22, 30)),
                         "franjas de hoy cerradas")

    def test_el_tope_de_una_franja_se_respeta(self):
        """Ganada la silla de la comida, no sale otra hasta la franja de la cena."""
        silla = self.inv.premios["silla"]
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(13, 30)), "")
        self.inv.emitir(silla, self.en(13, 30))
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(13, 31)),
                         "se libera a las 19:00")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(15, 59)),
                         "se libera a las 19:00")
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(19, 0)), "")
        # Y con las dos del día entregadas, manda el tope diario.
        self.inv.emitir(silla, self.en(19, 0))
        self.assertEqual(self.inv.motivo_no_disponible(silla, self.en(20, 0)), "tope de hoy")

    def test_la_hielera_solo_de_siete_a_once_de_la_noche(self):
        hielera = self.inv.premios["hielera"]
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(18, 59)),
                         "su franja abre a las 19:00")
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(19, 0)), "")
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(22, 59)), "")
        # A las 23:00 cierra el evento entero, así que gana ese motivo.
        self.assertEqual(self.inv.motivo_no_disponible(hielera, self.en(23, 0)),
                         "fuera de horario")

    # -- (e) separación mínima entre premios --------------------------------- #

    def test_separacion_minima_entre_premios(self):
        """Dictado del 2026-09-16: «los premios no deben salir seguidos»."""
        agua = self.inv.premios["agua"]
        self.assertEqual(self.inv.separacion_min_entre_premios, 3)
        self.inv.confirmar(self.inv.emitir(agua, self.en(14, 0)))
        espia = RngEspia()
        self.inv.rng = espia
        self.assertEqual(self.inv.espera_separacion(self.en(14, 2)), 1.0)
        self.assertIsNone(self.inv.sortear(self.en(14, 2)))
        self.assertEqual(espia.llamadas, [], "durante la separación ni se tira la tómbola")
        self.assertEqual(self.inv.espera_separacion(self.en(14, 3)), 0.0)
        self.assertIsNotNone(self.inv.sortear(self.en(14, 3)))
        self.assertEqual(len(espia.llamadas), 1)
        # Los premios NO dejan de estar disponibles: lo que se frena es el sorteo.
        self.assertEqual(self.inv.motivo_no_disponible(agua, self.en(14, 2)), "")

    def test_la_separacion_solo_la_marca_un_boleto_impreso(self):
        """Si el boleto no salió, el premio vuelve y no frena al siguiente."""
        agua = self.inv.premios["agua"]
        b = self.inv.emitir(agua, self.en(14, 0))
        self.assertEqual(self.inv.espera_separacion(self.en(14, 1)), 0.0)   # aún no confirmado
        self.inv.revertir(b)
        self.assertEqual(self.inv.espera_separacion(self.en(14, 1)), 0.0)
        # Un consuelo confirmado tampoco frena nada: no es un premio.
        self.inv.confirmar(self.inv.emitir(None, self.en(14, 1)))
        self.assertEqual(self.inv.espera_separacion(self.en(14, 2)), 0.0)

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

    # -- (f) persistencia del último premio ---------------------------------- #

    def test_el_ultimo_premio_sobrevive_al_reinicio(self):
        self.inv.confirmar(self.inv.emitir(self.inv.premios["agua"], self.en(14, 0)))
        guardado = json.loads(self.inv.ruta_estado.read_text(encoding="utf-8"))
        self.assertEqual(guardado["ultimo_premio"], "2026-09-24T14:00:00")
        otro = inventario_del_evento(self.carpeta)
        self.assertEqual(otro.espera_separacion(self.en(14, 2)), 1.0)
        self.assertIsNone(otro.sortear(self.en(14, 2)))
        self.assertEqual(otro.espera_separacion(self.en(14, 3)), 0.0)
        # Y reiniciar el inventario para un evento nuevo lo borra.
        otro.reiniciar()
        self.assertEqual(otro.espera_separacion(self.en(14, 2)), 0.0)
        self.assertIsNone(json.loads(otro.ruta_estado.read_text(encoding="utf-8"))["ultimo_premio"])

    def test_un_estado_viejo_sin_la_llave_carga_igual(self):
        """Un estado.json escrito antes de la Fase 4d no tiene 'ultimo_premio'."""
        viejo = {"version": 1, "folio": 16, "entregados": {"agua": 3},
                 "por_dia": {"2026-09-24": {"agua": 3}}, "boletos_por_dia": {"2026-09-24": 9},
                 "actualizado": "2026-09-24T14:00:00"}
        (self.carpeta / "estado.json").write_text(json.dumps(viejo), encoding="utf-8")
        inv = inventario_del_evento(self.carpeta)
        self.assertEqual((inv.folio_actual, inv.entregados("agua"), inv.boletos_en_dia(self.dia)),
                         (16, 3, 9))
        self.assertEqual(inv.espera_separacion(self.en(14, 0)), 0.0)
        # Y un valor ilegible tampoco tira el programa ni bloquea el juego.
        (self.carpeta / "estado.json").write_text(
            json.dumps({**viejo, "ultimo_premio": "ayer por la tarde"}), encoding="utf-8")
        roto = inventario_del_evento(self.carpeta)
        self.assertEqual(roto.folio_actual, 16)
        self.assertEqual(roto.espera_separacion(self.en(14, 0)), 0.0)

    # -- el resumen que imprime el boleto ------------------------------------ #

    def test_el_resumen_trae_las_liberadas_y_la_proxima(self):
        self.inv.emitir(self.inv.premios["agua"], self.en(14, 0))
        por_id = {f.premio.id: f for f in self.inv.resumen(self.en(14, 0)).premios}
        self.assertEqual((por_id["agua"].liberadas, por_id["agua"].hoy), (2, 1))
        self.assertEqual(por_id["agua"].proxima, self.en(14, 30))
        self.assertEqual((por_id["hielera"].liberadas, por_id["hielera"].proxima),
                         (0, self.en(19, 0)))
        self.assertEqual(por_id["silla"].liberadas, 1)
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
