import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from ruleta import config as configmod
from ruleta.config import ErrorConfig


def base(**extra):
    crudo = {
        "negocio": {"nombre": "Asadero 33", "logo": None},
        "impresora": {"tipo": "vista"},
        "premios": [{"id": "a", "nombre": "A", "peso": 1}],
    }
    for k, v in extra.items():
        if isinstance(v, dict) and isinstance(crudo.get(k), dict):
            crudo[k].update(v)
        else:
            crudo[k] = v
    return crudo


class TestTipos(unittest.TestCase):
    def espera_error(self, crudo, *fragmentos):
        with self.assertRaises(ErrorConfig) as ctx:
            configmod.desde_dict(crudo)
        for f in fragmentos:
            self.assertIn(f, str(ctx.exception))

    def test_numero_entre_comillas(self):
        self.espera_error(base(impresora={"tipo": "vista", "canal": "1"}), "impresora.canal", "sin comillas")
        self.espera_error(base(gpio={"rebote_ms": "30"}), "gpio.rebote_ms")
        self.espera_error(base(juego={"espera_entre_jugadas_seg": "5"}), "juego.espera_entre_jugadas_seg")
        self.espera_error(base(negocio={"nombre": "Asadero 33", "logo": None, "logo_ancho": "384"}), "logo_ancho")

    def test_booleanos_y_textos(self):
        self.espera_error(base(impresora={"tipo": "vista", "beep": "no"}), "impresora.beep", "true o false")
        self.espera_error(base(impresora={"tipo": "vista", "beep": 1}), "impresora.beep")
        self.espera_error(base(negocio={"nombre": 33, "logo": None}), "negocio.nombre", "texto")
        self.espera_error(base(negocio={"nombre": "X", "logo": None, "pie": "una sola línea"}), "negocio.pie", "lista")

    def test_null_donde_no_va(self):
        self.espera_error(base(gpio={"boton_jugar": None}), "gpio.boton_jugar")
        self.espera_error(base(juego={"hora_inicio_dia": None}), "juego.hora_inicio_dia")

    def test_null_donde_si_va(self):
        cfg = configmod.desde_dict(base(gpio={"led": None, "pulsacion_larga_seg": None},
                                        impresora={"tipo": "vista", "lineas_antes_corte": None}))
        self.assertIsNone(cfg.gpio.led)
        self.assertIsNone(cfg.gpio.pulsacion_larga_seg)

    def test_entero_donde_va_float_es_valido(self):
        cfg = configmod.desde_dict(base(juego={"espera_entre_jugadas_seg": 5}))
        self.assertEqual(cfg.juego.espera_entre_jugadas_seg, 5)

    def test_premio_con_tipos_malos(self):
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": "4"}]), "peso", "sin comillas")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "stock": 2.5}]), "stock")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "desde": 20260919}]), "desde", "AAAA-MM-DD")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "desde": "19/09/2026"}]), "AAAA-MM-DD")

    def test_premio_fechas_validas(self):
        cfg = configmod.desde_dict(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "desde": "2026-09-19"}]))
        self.assertEqual(cfg.premios[0].desde, date(2026, 9, 19))


class TestReglas(unittest.TestCase):
    def espera_error(self, crudo, fragmento):
        with self.assertRaises(ErrorConfig) as ctx:
            configmod.desde_dict(crudo)
        self.assertIn(fragmento, str(ctx.exception))

    def test_defectos_son_validos(self):
        cfg = configmod.desde_dict(base())
        self.assertEqual(cfg.impresora.codepage, "cp858")
        self.assertEqual(cfg.impresora.codepage_n, 19)
        self.assertEqual(cfg.impresora.corte, "auto")
        self.assertEqual(cfg.gpio.pulsacion_larga_seg, 6.0)
        self.assertTrue(cfg.impresora.consultar_estado)

    def test_llaves_desconocidas(self):
        self.espera_error(base(impresora={"tipo": "vista", "velocidad": 9}), "velocidad")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "precio": 3}]), "precio")

    def test_mac_invalida_solo_importa_en_bluetooth(self):
        self.espera_error(base(impresora={"tipo": "bluetooth", "mac": "no-es-mac"}), "impresora.mac")
        configmod.desde_dict(base(impresora={"tipo": "vista", "mac": "no-es-mac"}))

    def test_rangos(self):
        self.espera_error(base(impresora={"tipo": "vista", "chars_por_linea": 24}), "al menos 32")
        self.espera_error(base(impresora={"tipo": "vista", "timeout_seg": 0}), "timeout_seg")
        self.espera_error(base(impresora={"tipo": "vista", "ancho_puntos": 570}), "múltiplo de 8")
        self.espera_error(base(impresora={"tipo": "vista", "corte": "laser"}), "corte")
        self.espera_error(base(impresora={"tipo": "vista", "codepage": "klingon"}), "codepage")
        self.espera_error(base(negocio={"nombre": "X", "logo": None, "logo_ancho": 0}), "logo_ancho")
        self.espera_error(base(negocio={"nombre": "X", "logo": None, "logo_ancho": 600}), "logo_ancho")
        self.espera_error(base(negocio={"nombre": "  ", "logo": None}), "negocio.nombre")
        self.espera_error(base(gpio={"pulsacion_larga_seg": 0.5}), "pulsacion_larga_seg")
        self.espera_error(base(gpio={"boton_jugar": 40}), "GPIO")
        self.espera_error(base(gpio={"boton_jugar": 17, "boton_habilitar": 17}), "mismo pin")
        self.espera_error(base(gpio={"modo_habilitar": "mantener", "boton_habilitar": None}), "modo_habilitar")
        self.espera_error(base(juego={"hora_inicio_dia": 24}), "hora_inicio_dia")
        self.espera_error(base(juego={"intentos_inventario_arranque": 0}), "intentos_inventario_arranque")

    def test_premios(self):
        self.espera_error(base(premios=[]), "al menos un premio")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 0}]), "peso")
        self.espera_error(base(premios=[{"id": "con espacio", "nombre": "A", "peso": 1}]), "id")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1}, {"id": "a", "nombre": "B", "peso": 1}]), "mismo id")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "stock": -1}]), "stock")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "tope_diario": 0}]), "tope_diario")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A", "peso": 1, "desde": "2026-09-20", "hasta": "2026-09-19"}]), "posterior")
        self.espera_error(base(premios=[{"id": "a", "nombre": "A"}]), "faltan")


class TestCargar(unittest.TestCase):
    def test_archivo_inexistente_y_json_roto(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ErrorConfig) as ctx:
                configmod.cargar(Path(tmp) / "nada.json")
            self.assertIn("No existe", str(ctx.exception))
            roto = Path(tmp) / "roto.json"
            roto.write_text('{"negocio": {"nombre": "X",}}', encoding="utf-8")
            with self.assertRaises(ErrorConfig) as ctx:
                configmod.cargar(roto)
            self.assertIn("mal formado", str(ctx.exception))
            self.assertIn("línea", str(ctx.exception))

    def test_rutas_relativas_al_archivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "config.json"
            ruta.write_text(json.dumps(base(negocio={"nombre": "X", "logo": "logo.png"},
                                            carpeta_datos="misdatos")), encoding="utf-8")
            cfg = configmod.cargar(ruta)
            self.assertEqual(cfg.ruta_logo(), Path(tmp) / "logo.png")
            self.assertEqual(cfg.carpeta_datos, Path(tmp) / "misdatos")

    def test_config_json_del_proyecto_es_valido(self):
        cfg = configmod.cargar(Path(__file__).resolve().parent.parent / "config.json")
        self.assertEqual(len(cfg.premios), 7)
        self.assertEqual(cfg.premios[2].stock, 1)


if __name__ == "__main__":
    unittest.main()
