import json
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from PIL import Image

from ruleta import config as configmod, ticket
from ruleta.escpos import decodificar_vista
from ruleta.inventario import Boleto, Inventario

RUTA_CONFIG = Path(__file__).resolve().parent.parent / "config.json"


def config_base(**extra):
    crudo = {
        "negocio": {"nombre": "Asadero 33", "logo": None},
        "impresora": {"tipo": "vista"},
        "gpio": {"boton_jugar": 17, "boton_habilitar": 27, "led": None},
        "premios": [
            {"id": "tacos", "nombre": "Orden de tacos al pastor", "peso": 5, "stock": 10, "detalle": "Incluye salsa"},
            {"id": "mayor", "nombre": "Premio Mayor", "peso": 1, "stock": 1},
            {"id": "largo", "nombre": "Un nombre de premio exageradamente largo para ver cómo se acomoda", "peso": 1},
        ],
    }
    crudo.update(extra)
    return configmod.desde_dict(crudo)


def lineas_vista(datos, ancho=48):
    """Por línea impresa: (multiplicador, texto como se ve en papel, texto original).

    Se omiten las marcas de corte/imagen/beep, que no son texto impreso.
    """
    salida = []
    for l in decodificar_vista(datos, "cp858", ancho).splitlines():
        prefijo, _, texto = l.partition("|")
        if any(marca in texto for marca in ("[CORTE]", "[IMAGEN", "[BEEP]")):
            continue
        mult = int(prefijo[1]) if prefijo[1].isdigit() else 1
        salida.append((mult, texto, texto[::mult] if mult > 1 else texto))


    return salida


class TestAjusteTextoGrande(unittest.TestCase):
    def test_corto_usa_el_maximo(self):
        self.assertEqual(ticket.ajustar_texto_grande("TACOS", 48), (4, ["TACOS"]))

    def test_tres_lineas_en_4x(self):
        mult, lineas = ticket.ajustar_texto_grande("ORDEN DE TACOS AL PASTOR", 48)
        self.assertEqual(mult, 4)
        self.assertEqual(lineas, ["ORDEN DE", "TACOS AL", "PASTOR"])
        self.assertTrue(all(len(l) <= 12 for l in lineas))

    def test_palabra_larga_baja_el_tamano(self):
        mult, lineas = ticket.ajustar_texto_grande("CONSTANTINOPLA", 48)
        self.assertEqual(mult, 3)
        self.assertEqual(lineas, ["CONSTANTINOPLA"])

    def test_texto_largo_cabe_en_2x(self):
        texto = "UNA CENA COMPLETA PARA DOS PERSONAS CON BEBIDA"
        mult, lineas = ticket.ajustar_texto_grande(texto, 48)
        self.assertEqual(mult, 2)
        self.assertLessEqual(len(lineas), 3)
        self.assertTrue(all(len(l) <= 24 for l in lineas))

    def test_texto_enorme_cae_a_1x_recortado(self):
        texto = " ".join(["PALABRA"] * 40)
        mult, lineas = ticket.ajustar_texto_grande(texto, 48)
        self.assertEqual(mult, 1)
        self.assertEqual(len(lineas), 3)

    def test_espacios_multiples_se_normalizan(self):
        self.assertEqual(ticket.ajustar_texto_grande("  A   B  ", 48), (4, ["A B"]))


class TestBoletos(unittest.TestCase):
    def setUp(self):
        self.cfg = config_base()
        self.ahora = datetime(2026, 9, 15, 20, 5)
        self.dia = date(2026, 9, 15)

    def boleto(self, premio_id, folio=42):
        premio = next(p for p in self.cfg.premios if p.id == premio_id)
        return Boleto(folio=folio, premio=premio, momento=self.ahora, dia=self.dia)

    def test_boleto_premio_contenido(self):
        datos = ticket.boleto_premio(self.cfg, self.boleto("tacos"))
        self.assertTrue(datos.startswith(b"\x1b@\x1c.\x1bR\x00\x1bt\x13"))
        self.assertTrue(datos.endswith(b"\x1bd\x01\x1dV\x42\x00"))
        vista = lineas_vista(datos)
        originales = [o.strip() for _, _, o in vista]
        self.assertIn("BOLETO 00042", originales)
        self.assertEqual(next(m for m, _, o in vista if o.strip() == "BOLETO 00042"), 2)
        self.assertIn("15/09/2026 20:05", originales)
        self.assertIn("Incluye salsa", originales)
        self.assertIn("Presenta este boleto en caja", originales)
        grandes = [o.strip() for m, _, o in vista if m == 4]
        self.assertEqual(grandes, ["ORDEN DE", "TACOS AL", "PASTOR"])
        self.assertIn("¡GANASTE!", originales)

    def test_titulo_ganaste_con_acentos(self):
        datos = ticket.boleto_premio(self.cfg, self.boleto("mayor"))
        self.assertIn(b"\xadGANASTE!", datos)   # ¡ en cp850 = 0xAD

    def test_ninguna_linea_excede_el_ancho(self):
        for pid in ("tacos", "mayor", "largo"):
            datos = ticket.boleto_premio(self.cfg, self.boleto(pid))
            for mult, papel, _ in lineas_vista(datos):
                self.assertLessEqual(len(papel.rstrip()), 48, f"{pid}: {papel!r}")

    def test_sin_logo_no_hay_raster(self):
        datos = ticket.boleto_premio(self.cfg, self.boleto("tacos"))
        self.assertNotIn(b"\x1dv0", datos)

    def test_con_logo_hay_raster_y_se_respeta_ancho(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "logo.png"
            Image.new("RGB", (1000, 200), (0, 0, 0)).save(ruta)
            cfg = config_base(negocio={"nombre": "Asadero 33", "logo": str(ruta), "logo_ancho": 384})
            datos = ticket.boleto_premio(cfg, self.boleto("tacos"))
            self.assertIn(b"\x1dv0\x00\x30\x00", datos)   # 384/8 = 48 = 0x30 bytes por fila
            self.assertIn("[IMAGEN 384x", decodificar_vista(datos))

    def test_logo_inexistente_o_corrupto_se_ignora(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "logo.png"
            ruta.write_bytes(b"esto no es una imagen")
            cfg = config_base(negocio={"nombre": "Asadero 33", "logo": str(ruta)})
            datos = ticket.boleto_premio(cfg, self.boleto("tacos"))
            self.assertNotIn(b"\x1dv0", datos)
            cfg2 = config_base(negocio={"nombre": "Asadero 33", "logo": str(Path(tmp) / "no_existe.png")})
            ticket.boleto_premio(cfg2, self.boleto("tacos"))

    def test_beep_y_corte_completo_configurables(self):
        cfg = config_base(impresora={"tipo": "vista", "beep": True, "corte": "completo", "lineas_antes_corte": 6})
        datos = ticket.boleto_premio(cfg, self.boleto("tacos"))
        self.assertTrue(datos.endswith(b"\x1bB\x02\x02\x1bd\x06\x1dV\x00"))

    def test_consuelo(self):
        b = Boleto(folio=7, premio=None, momento=self.ahora, dia=self.dia)
        datos = ticket.boleto_consuelo(self.cfg, b)
        vista = lineas_vista(datos)
        originales = [o.strip() for _, _, o in vista]
        # 18 caracteres no caben en 3x (16 por línea): se parte en dos líneas grandes
        grandes = [(m, o.strip()) for m, _, o in vista if m > 1]
        self.assertEqual(grandes, [(2, "Asadero 33"), (3, "SIGUE"), (3, "PARTICIPANDO")])
        self.assertTrue(any(o.startswith("BOLETO 00007") for o in originales))
        self.assertIn("Por hoy se agotaron los premios. ¡Gracias por", originales)
        for _, papel, _ in vista:
            self.assertLessEqual(len(papel.rstrip()), 48, papel)

    def test_inventario(self):
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(self.cfg.premios, tmp)
            inv.confirmar(inv.emitir(inv.premios["mayor"], self.ahora))
            datos = ticket.boleto_inventario(self.cfg, inv.resumen(self.ahora), "arranque")
        vista = lineas_vista(datos)
        originales = [o for _, _, o in vista]
        self.assertIn("INVENTARIO", [o.strip() for o in originales])
        self.assertTrue(any("(arranque)" in o for o in originales))
        fila_mayor = next(o for o in originales if o.startswith("Premio Mayor"))
        self.assertIn("0/1", fila_mayor)
        self.assertIn("--", fila_mayor)
        self.assertTrue(any("no disponible: agotado" in o for o in originales))
        fila_tacos = next(o for o in originales if o.startswith("Orden de tacos"))
        self.assertIn("10/10", fila_tacos)
        self.assertIn("83.3%", fila_tacos)
        self.assertTrue(any("Último folio:" in o and "00001" in o for o in originales))
        self.assertFalse(any("REVISAR" in o for o in originales))
        for _, papel, _ in vista:
            self.assertLessEqual(len(papel.rstrip()), 48, papel)

    def test_inventario_lista_pendientes(self):
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(self.cfg.premios, tmp)
            b = inv.emitir(inv.premios["mayor"], self.ahora)
            inv.marcar_incierto(b)
            inv.emitir(inv.premios["tacos"], self.ahora)   # 'emitido' sin cierre
            datos = ticket.boleto_inventario(self.cfg, inv.resumen(self.ahora), "reporte")
        vista = lineas_vista(datos)
        originales = [o for _, _, o in vista]
        self.assertTrue(any("REVISAR" in o for o in originales))
        self.assertTrue(any(o.strip().startswith("00001") and "incierto" in o and "Premio Mayor" in o for o in originales))
        self.assertTrue(any(o.strip().startswith("00002") and "emitido" in o for o in originales))
        self.assertTrue(any("liberar FOLIO" in o for o in originales))
        for _, papel, _ in vista:
            self.assertLessEqual(len(papel.rstrip()), 48, papel)

    def test_inventario_con_peso_de_consuelo(self):
        """Pieza A (Fase 4c): el consuelo aparece con su peso y su probabilidad de AHORA.

        La línea se ancla **entera y por igualdad**, y el porcentaje que lleva se
        comprueba contra el que calcula el programa (`probabilidad_consuelo`), no
        contra un número tecleado a mano.
        """
        anchos = {48: self.cfg, 32: config_base(impresora={"tipo": "vista", "chars_por_linea": 32})}
        for ancho, cfg in anchos.items():
            with self.subTest(ancho=ancho):
                with tempfile.TemporaryDirectory() as tmp:
                    inv = Inventario(cfg.premios, tmp, peso_consuelo=217)
                    resumen = inv.resumen(self.ahora)
                    datos = ticket.boleto_inventario(cfg, resumen, "reporte")
                # Pesos de los tres premios de prueba: 5 + 1 + 1 = 7, más 217 papelitos.
                self.assertAlmostEqual(resumen.probabilidad_consuelo, 100 * 217 / 224)
                self.assertEqual(resumen.peso_consuelo, 217)
                vista = lineas_vista(datos, ancho)
                originales = [o.rstrip() for _, _, o in vista]
                esperada = {48: "SIGUE PARTICIPANDO (consuelo)  peso 217 -> 96.9%",
                            32: "SIGUE PARTICIP peso 217 -> 96.9%"}[ancho]
                self.assertEqual([o for o in originales if "peso 217" in o], [esperada])
                self.assertIn(f"{resumen.probabilidad_consuelo:.1f}%", esperada)
                # Con el consuelo en el denominador, los premios bajan: 5/224 = 2.2 %.
                fila_tacos = next(o for o in originales if o.startswith("Orden"))
                self.assertIn("2.2%", fila_tacos)
                for _, papel, _ in vista:
                    self.assertLessEqual(len(papel.rstrip()), ancho, papel)
        # Y con OTRO peso la línea tiene que cambiar sola: si el número saliera
        # de una constante del código en vez del resumen, esto caería.
        with tempfile.TemporaryDirectory() as tmp:
            otro = Inventario(self.cfg.premios, tmp, peso_consuelo=117)
            datos = ticket.boleto_inventario(self.cfg, otro.resumen(self.ahora), "reporte")
        self.assertEqual(
            [o.rstrip() for _, _, o in lineas_vista(datos) if "(consuelo)" in o],
            ["SIGUE PARTICIPANDO (consuelo)  peso 117 -> 94.4%"])

    def inventario_del_config_real(self, momento=None, aviso_hora=False, emitir=None):
        """El boleto de inventario con el `config.json` real, cableado como en producción."""
        cfg = configmod.cargar(Path(__file__).resolve().parent.parent / "config.json")
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(cfg.premios, tmp, hora_inicio_dia=cfg.juego.hora_inicio_dia,
                             peso_consuelo=cfg.juego.consuelo.peso, horario=cfg.juego.horario,
                             separacion_min_entre_premios=cfg.juego.separacion_min_entre_premios)
            if emitir:
                inv.confirmar(inv.emitir(inv.premios[emitir], momento or self.ahora))
            resumen = inv.resumen(momento or self.ahora)
            datos = ticket.boleto_inventario(cfg, resumen, "arranque", aviso_hora=aviso_hora)
        lineas = [papel.rstrip() for _, papel, _ in lineas_vista(datos, cfg.impresora.chars_por_linea)]
        return cfg, resumen, lineas

    def test_inventario_del_config_real_cabe_entero(self):
        """Vector real: el `config.json` del repositorio, con sus siete premios y su consuelo.

        La línea del consuelo ocupa **las 48 columnas justas**, con los espacios
        que reparte `_dos_columnas`. Se ancla entera y con el relleno recalculado
        aquí: si alguien alarga `juego.consuelo.titulo` o cambia el peso, la
        columna derecha se movería **en silencio** y esta igualdad cae.
        """
        cfg, resumen, lineas = self.inventario_del_config_real()
        ancho = cfg.impresora.chars_por_linea
        self.assertEqual([l for l in lineas if len(l) > ancho], [])
        izquierda = f"{cfg.juego.consuelo.titulo} (consuelo)"
        derecha = f"peso {cfg.juego.consuelo.peso} -> {resumen.probabilidad_consuelo:.1f}%"
        fila = next(l for l in lineas if "(consuelo)" in l)
        self.assertEqual(fila, izquierda + " " * (ancho - len(izquierda) - len(derecha)) + derecha)
        self.assertEqual(len(fila), ancho)

    def test_inventario_del_config_real_trae_el_reparto_por_horas(self):
        """Pieza D5 (Fase 4d): entregadas hoy, piezas abiertas y la hora de la siguiente.

        Vector real a las 20:05 del **martes 22**, con un agua ya entregada. Las
        líneas se anclan **enteras y por igualdad**: los números y las horas
        salen del reparto que calcula el motor, no de constantes del `ticket.py`.

        La fecha dejó de ser el 15 de septiembre el 2026-09-22 (día 2, paso 2):
        con las horas por día, un día fuera del evento no abre **ninguna** franja
        y las cinco líneas de los grandes saldrían todas iguales, sin probar
        nada. El martes es el día con más piezas repartidas de todo el evento.
        """
        cfg, _, lineas = self.inventario_del_config_real(
            momento=datetime(2026, 9, 22, 20, 5), emitir="agua")
        ancho = cfg.impresora.chars_por_linea
        self.assertEqual([l for l in lineas if len(l) > ancho], [])
        nuevas = [l for l in lineas if l.startswith("  hoy ")]
        self.assertEqual(nuevas, [
            "  hoy 0 · liberadas 0 · sin más hoy",      # HIELERA IGLOO: el martes no tiene franja
            "  hoy 0 · liberadas 2 · sin más hoy",      # SILLA DE PLAYA, 13:17 y 19:23
            "  hoy 0 · liberadas 1 · sin más hoy",      # SILLA DE PLAYA (silla_extra), 16:08
            "  hoy 0 · liberadas 0 · sig 21:00",        # SILLA DE PLAYA (silla_extra2), la cuarta
            "  hoy 0 · liberadas 1 · sig 20:47",        # SET BBQ, abierta la de 14:41
            "  hoy 0 · liberadas 1 · sin más hoy",      # SET BBQ (bbq_extra), 17:34
            "  hoy 0 · liberadas 3 · sig 21:37",        # 3 TACOS DE PASTOR
            "  hoy 0 · liberadas 3 · sig 21:37",        # 2 TACOS DE PASTOR
            "  hoy 0 · liberadas 7 · sig 20:15",        # CERVEZA
            "  hoy 1 · liberadas 8 · sig 20:30",        # AGUA FRESCA, la entregada
        ])
        # Y cada premio lleva exactamente una: ni de más ni de menos.
        self.assertEqual(len(nuevas), len(cfg.premios))

    def test_el_inventario_marca_los_premios_forzados(self):
        """Día 2 paso 2 (2026-09-22): la señal de forzado, entera y a 48 columnas.

        Se anclan **las filas completas por igualdad**, no «aparece la palabra»:
        la señal va pegada al nombre y comparte renglón con las tres columnas de
        números, así que lo que hay que defender es que **quepa sin recortar
        ningún nombre** —«SILLA DE PLAYA *forzado» ocupa justo las 23 columnas
        del hueco— y que los premios chicos **no** la lleven.
        """
        cfg, _, lineas = self.inventario_del_config_real(momento=datetime(2026, 9, 22, 20, 5))
        ancho = cfg.impresora.chars_por_linea
        self.assertEqual([l for l in lineas if len(l) > ancho], [])
        self.assertEqual([l for l in lineas if ticket.MARCA_FORZADO in l], [
            "HIELERA IGLOO *forzado        2/2     0/1     --",
            "SILLA DE PLAYA *forzado     10/10     0/2  71.9%",
            "SILLA DE PLAYA *forzado       1/1     0/1     --",
            "SILLA DE PLAYA *forzado       1/1     0/1     --",
            "SET BBQ *forzado            10/10     0/2     --",
            "SET BBQ *forzado              1/1     0/1     --",
        ])
        self.assertEqual([l for l in lineas if l.startswith("* forzado")],
                         [ticket.LEYENDA_FORZADO])
        # Los seis nombres caben enteros: ni uno acabó en punto de recorte.
        # Eran cinco hasta la noche del 2026-09-22, cuando entró `silla_extra2`
        # (ficha F-288).
        forzados = [p.nombre for p in cfg.premios if p.forzado]
        self.assertEqual(len(forzados), 6)
        for nombre in forzados:
            self.assertTrue(any(l.startswith(nombre + ticket.MARCA_FORZADO) for l in lineas),
                            f"{nombre!r} no aparece entero con su señal")
        # Y la leyenda va después de los premios y antes del consuelo, donde se
        # lee junto a las filas que explica.
        i_leyenda = lineas.index(ticket.LEYENDA_FORZADO)
        self.assertLess(next(i for i, l in enumerate(lineas) if l.startswith("SET BBQ")), i_leyenda)
        self.assertLess(i_leyenda, next(i for i, l in enumerate(lineas) if "(consuelo)" in l))

    def test_sin_premios_forzados_el_inventario_sale_como_antes(self):
        """Los premios de prueba no llevan `forzado`: ni señal ni leyenda."""
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(self.cfg.premios, tmp)
            datos = ticket.boleto_inventario(self.cfg, inv.resumen(self.ahora), "reporte")
        originales = [o for _, _, o in lineas_vista(datos)]
        self.assertEqual([p.forzado for p in self.cfg.premios], [False, False, False])
        self.assertEqual([o for o in originales if "forzado" in o], [])

    def test_la_senal_de_forzado_no_desborda_un_papel_angosto(self):
        """A 32 columnas el hueco del nombre son 7 caracteres: se recorta, no se sale.

        Es la misma regla de siempre para los nombres largos, ahora con la señal
        pegada; lo que se ancla es que **ninguna fila de premio pase del ancho**,
        que es lo que rompería el boleto en un rollo de 58 mm.

        Los renglones `> no disponible: …` **sí** se pasan a 32 columnas, y eso
        es anterior a este cambio: nunca se han partido (ficha **F-286**). Se
        dejan fuera de esta comprobación a propósito, con la lista de los que se
        pasan anclada por igualdad para que crecer esa lista **no** pase en
        silencio.
        """
        crudo = json.loads(RUTA_CONFIG.read_text(encoding="utf-8"))
        crudo["impresora"] = {**crudo["impresora"], "tipo": "vista", "chars_por_linea": 32}
        cfg = configmod.desde_dict(crudo, ruta=RUTA_CONFIG)
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(cfg.premios, tmp, hora_inicio_dia=cfg.juego.hora_inicio_dia,
                             peso_consuelo=cfg.juego.consuelo.peso, horario=cfg.juego.horario)
            datos = ticket.boleto_inventario(cfg, inv.resumen(datetime(2026, 9, 22, 20, 5)))
        lineas = [papel.rstrip() for _, papel, _ in lineas_vista(datos, 32)]
        self.assertEqual([l for l in lineas if len(l) > 32],
                         ["  > no disponible: franjas de hoy cerradas",
                          "  > no disponible: su franja abre a las 21:00",
                          "  > no disponible: su franja abre a las 20:47",
                          "  > no disponible: franjas de hoy cerradas"])
        # Las filas de premio, que son las que llevan la señal, caben todas.
        self.assertEqual([l for l in lineas if "forzado" in l and len(l) > 32], [])
        # Y la leyenda sigue estando ENTERA, repartida en las líneas que hagan
        # falta: es lo que explica el recorte, así que no puede desaparecer.
        i = next(i for i, l in enumerate(lineas) if l.startswith("* forzado"))
        partes = []
        for l in lineas[i:]:
            partes.append(l)
            if " ".join(partes) == ticket.LEYENDA_FORZADO:
                break
        self.assertEqual(" ".join(partes), ticket.LEYENDA_FORZADO)
        self.assertGreater(len(partes), 1, "a 32 columnas la leyenda tiene que partirse")

    def test_inventario_avisa_cuando_la_hora_no_se_confirmo(self):
        """Pieza D (Fase 4d): la línea entera, por igualdad, y solo si toca."""
        _, _, con_aviso = self.inventario_del_config_real(aviso_hora=True)
        self.assertEqual([l.strip() for l in con_aviso if "HORA" in l],
                         ["HORA SIN CONFIRMAR: revisar fecha"])
        self.assertEqual([l.strip() for l in con_aviso if "HORA" in l], [ticket.AVISO_HORA])
        _, _, sin_aviso = self.inventario_del_config_real(aviso_hora=False)
        self.assertEqual([l for l in sin_aviso if "HORA" in l], [])
        # El aviso va arriba del todo, junto a la fecha: es lo que hay que mirar.
        i_aviso = next(i for i, l in enumerate(con_aviso) if "HORA" in l)
        i_fecha = next(i for i, l in enumerate(con_aviso) if "Día operativo" in l)
        self.assertEqual(i_aviso, i_fecha + 1)

    def test_un_premio_sin_reparto_no_lleva_renglon_de_liberacion(self):
        """Los premios de prueba no tienen tope diario: el boleto sale como antes."""
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(self.cfg.premios, tmp)
            datos = ticket.boleto_inventario(self.cfg, inv.resumen(self.ahora), "reporte")
        self.assertEqual([o for _, _, o in lineas_vista(datos) if o.startswith("  hoy ")], [])

    def test_inventario_sin_peso_de_consuelo_no_menciona_el_consuelo(self):
        """Con peso 0 el boleto sale exactamente como antes de la Fase 4c."""
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(self.cfg.premios, tmp)
            resumen = inv.resumen(self.ahora)
            datos = ticket.boleto_inventario(self.cfg, resumen, "reporte")
        self.assertEqual(resumen.peso_consuelo, 0)
        originales = [o for _, _, o in lineas_vista(datos)]
        self.assertEqual([o for o in originales if "consuelo" in o.lower()], [])
        self.assertEqual([o for o in originales if "PARTICIPANDO" in o], [])
        # Y los premios se reparten el 100 % entre ellos: 5/7 = 71.4 %.
        fila_tacos = next(o for o in originales if o.startswith("Orden"))
        self.assertIn("71.4%", fila_tacos)

    def test_inventario_con_ancho_minimo(self):
        cfg = config_base(impresora={"tipo": "vista", "chars_por_linea": 32})
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(cfg.premios, tmp)
            datos = ticket.boleto_inventario(cfg, inv.resumen(self.ahora))
        vista = lineas_vista(datos, 32)
        fila = next(o for _, _, o in vista if o.startswith("Orden"))
        self.assertIn("10/10", fila)                 # el nombre se recorta, las columnas no
        for _, papel, _ in vista:
            self.assertLessEqual(len(papel.rstrip()), 32, papel)

    def bloque_de_acentos(self, datos, ancho):
        """Las líneas que hay entre el título de los acentos y la de 'Configurado:'."""
        lineas = [papel.rstrip() for _, papel, _ in lineas_vista(datos, ancho)]
        i = lineas.index("Acentos con cada tabla de caracteres:")
        j = next(k for k, l in enumerate(lineas) if l.startswith("Configurado:"))
        return lineas[i + 1:j]

    def test_prueba_lineas_de_acentos_completas(self):
        # Etiqueta corta en una línea y la muestra en la siguiente: juntas pasaban
        # de 48 columnas y la impresora las partía a media palabra.
        muestra = "ñ Ñ á é í ó ú Á É Í Ó Ú ü ¿ ¡ º"
        datos = ticket.boleto_prueba(self.cfg, (0, 2, 16, 19))
        self.assertEqual(self.bloque_de_acentos(datos, 48), [
            "  ESC t 0 (cp437):", "ñ Ñ á é í ó ú A É I O U ü ¿ ¡ º",   # cp437 solo trae la É
            "  ESC t 2 (cp850):", muestra,
            "  ESC t 16 (cp1252):", muestra,
            "  ESC t 19 (cp858):", muestra,
        ])

    def test_prueba_ninguna_linea_excede_el_ancho(self):
        for ancho in (32, 42, 48):
            cfg = config_base(impresora={"tipo": "vista", "chars_por_linea": ancho})
            datos = ticket.boleto_prueba(cfg, (0, 2, 16, 19))
            largas = [l for l in self.bloque_de_acentos(datos, ancho) if len(l) > ancho]
            self.assertEqual(largas, [], f"ancho {ancho}")

    def test_prueba_del_config_real_cabe_entero(self):
        # Vector real: el config.json del repositorio, con su logo y sus 48 columnas.
        cfg = configmod.cargar(Path(__file__).resolve().parent.parent / "config.json")
        ancho = cfg.impresora.chars_por_linea
        datos = ticket.boleto_prueba(cfg, (0, 2, 16, 19))
        largas = [papel.rstrip() for _, papel, _ in lineas_vista(datos, ancho)
                  if len(papel.rstrip()) > ancho]
        self.assertEqual(largas, [])

    def test_prueba_rechaza_tablas_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            ticket.boleto_prueba(self.cfg, (0, 300))

    def test_prueba(self):
        datos = ticket.boleto_prueba(self.cfg, (0, 2))
        self.assertIn(b"\x1bt\x00", datos)
        self.assertIn(b"\x1bt\x02", datos)
        # Al final vuelve a la tabla configurada (19 = PC858)
        self.assertIn(b"\x1bt\x13Configurado", datos)
        self.assertIn(b"0123456789" * 4 + b"01234567\n", datos)


if __name__ == "__main__":
    unittest.main()
