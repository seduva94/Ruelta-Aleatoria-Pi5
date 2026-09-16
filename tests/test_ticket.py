import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path

from PIL import Image

from ruleta import config as configmod, ticket
from ruleta.escpos import decodificar_vista
from ruleta.inventario import Boleto, Inventario


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

    def test_inventario_del_config_real_cabe_entero(self):
        """Vector real: el `config.json` del repositorio, con sus siete premios y su consuelo.

        La línea del consuelo con el título real ocupa **las 48 columnas justas**
        (29 + 2 + 17). Se ancla entera: si alguien alarga `juego.consuelo.titulo`,
        `_dos_columnas` lo recortaría **en silencio** y esta igualdad cae.
        """
        cfg = configmod.cargar(Path(__file__).resolve().parent.parent / "config.json")
        ancho = cfg.impresora.chars_por_linea
        with tempfile.TemporaryDirectory() as tmp:
            inv = Inventario(cfg.premios, tmp, hora_inicio_dia=cfg.juego.hora_inicio_dia,
                             peso_consuelo=cfg.juego.consuelo.peso)
            resumen = inv.resumen(self.ahora)
            datos = ticket.boleto_inventario(cfg, resumen, "arranque")
        lineas = [papel.rstrip() for _, papel, _ in lineas_vista(datos, ancho)]
        self.assertEqual([l for l in lineas if len(l) > ancho], [])
        fila = next(l for l in lineas if "(consuelo)" in l)
        self.assertEqual(fila,
                         f"{cfg.juego.consuelo.titulo} (consuelo)  "
                         f"peso {cfg.juego.consuelo.peso} -> {resumen.probabilidad_consuelo:.1f}%")
        self.assertEqual(len(fila), ancho)

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
