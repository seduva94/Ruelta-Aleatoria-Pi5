import json
import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

from ruleta import config as configmod
from ruleta.config import ErrorConfig, Franja

RAIZ = Path(__file__).resolve().parent.parent
RUTA_CONFIG = RAIZ / "config.json"
RUTA_EVENTO = RAIZ / "docs" / "evento-2026-09-asadero-33.md"

# Las llaves que la Fase 4b copió del documento del evento al config.json, más
# 'franjas', que añadió la Fase 4d (pieza B). NO están 'desde' ni 'hasta': se
# cargan en la pasada final antes del lunes 21 (ficha F-259). Lo ancla
# TestPremiosOficialesDelEvento.test_los_premios_del_config_todavia_no_traen_fechas.
CLAVES_OBLIGATORIAS = ("id", "nombre", "detalle", "stock", "tope_diario", "peso")
CLAVES_DEL_DOCUMENTO = CLAVES_OBLIGATORIAS + ("franjas",)

# Fila de la tabla de la tómbola del §2 del documento del evento, de la forma
#   | Una pieza de AGUA FRESCA (peso 11) | 11 + 10 = 21 | **52.4 %** |
# Se parsea en vez de transcribirse para que los números del documento los tenga
# que calcular el programa (golden test_las_probabilidades_del_2_las_calcula_el_programa).
FILA_TOMBOLA = re.compile(
    r"\|[^|\n]*?([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]*[A-ZÁÉÍÓÚÑ]) \(peso (\d+)\)[^|\n]*\|"
    r"\s*(\d+) \+ (\d+) = (\d+)\s*\|\s*\*\*([\d.]+) %\*\*\s*\|")


def como_dict(valor):
    """Las franjas del validador (objetos Franja) en la forma cruda del JSON."""
    if isinstance(valor, list):
        return [como_dict(v) for v in valor]
    if isinstance(valor, Franja):
        return {"desde_hora": valor.desde_hora, "hasta_hora": valor.hasta_hora, "tope": valor.tope}
    return valor


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

    def test_peso_de_consuelo_con_tipos_malos(self):
        """El peso del consuelo es un entero como los demás; el mensaje nombra la llave."""
        self.espera_error(base(juego={"consuelo": {"peso": "217"}}),
                          "juego.consuelo.peso", "sin comillas")
        self.espera_error(base(juego={"consuelo": {"peso": 2.5}}), "juego.consuelo.peso")
        self.espera_error(base(juego={"consuelo": {"peso": True}}), "juego.consuelo.peso")
        self.espera_error(base(juego={"consuelo": {"peso": None}}), "juego.consuelo.peso")

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
        self.espera_error(base(juego={"consuelo": {"peso": -1}}), "juego.consuelo.peso")
        self.espera_error(base(juego={"separacion_min_entre_premios": -1}),
                          "juego.separacion_min_entre_premios")
        self.espera_error(base(juego={"espera_hora_seg": -0.5}), "juego.espera_hora_seg")

    # -- horario del evento (pieza C, Fase 4d) ------------------------------- #

    def test_horario_del_evento_valido(self):
        cfg = configmod.desde_dict(base(juego={"horario": {"abre": "12:00", "cierra": "23:00",
                                                           "fuera_de_horario": "no_jugar"}}))
        self.assertEqual((cfg.juego.horario.abre, cfg.juego.horario.cierra,
                          cfg.juego.horario.fuera_de_horario), ("12:00", "23:00", "no_jugar"))
        # Sin la llave NO hay horario, y eso es «se juega a cualquier hora»: se
        # ancla por igualdad a None porque es lo único que separa una instalación
        # vieja de una nueva.
        self.assertIsNone(configmod.desde_dict(base()).juego.horario)
        self.assertIsNone(configmod.desde_dict(base(juego={"hora_inicio_dia": 6})).juego.horario)
        # Y por omisión, si el bloque existe, fuera de horario se da consuelo.
        con_bloque = configmod.desde_dict(base(juego={"horario": {"abre": "12:00", "cierra": "23:00"}}))
        self.assertEqual(con_bloque.juego.horario.fuera_de_horario, "consuelo")

    def test_horario_del_evento_invalido(self):
        def horario(**h):
            return base(juego={"horario": {"abre": "12:00", "cierra": "23:00", **h}})
        self.espera_error(horario(abre="25:00"), "juego.horario.abre")
        self.espera_error(horario(abre="12:60"), "juego.horario.abre")
        self.espera_error(horario(abre="9:00"), "juego.horario.abre")       # falta el cero
        self.espera_error(horario(cierra="mediodía"), "juego.horario.cierra")
        self.espera_error(horario(cierra=1200), "juego.horario.cierra")
        self.espera_error(horario(abre="23:00", cierra="12:00"), "anterior")
        self.espera_error(horario(abre="12:00", cierra="12:00"), "anterior")
        self.espera_error(horario(fuera_de_horario="apagar"), "fuera_de_horario")
        self.espera_error(base(juego={"horario": {"abre": "12:00", "cierra": "23:00", "todo": 1}}),
                          "juego.horario")
        self.espera_error(base(juego={"horario": "12:00-23:00"}), "juego.horario")

    # -- franjas por premio (pieza B, Fase 4d) ------------------------------- #

    def test_franjas_validas(self):
        cfg = configmod.desde_dict(base(premios=[{
            "id": "silla", "nombre": "Silla", "peso": 2, "tope_diario": 2,
            "franjas": [{"desde_hora": "13:00", "hasta_hora": "16:00", "tope": 1},
                        {"desde_hora": "19:00", "hasta_hora": "22:00"}]}]))
        self.assertEqual([como_dict(f) for f in cfg.premios[0].franjas],
                         [{"desde_hora": "13:00", "hasta_hora": "16:00", "tope": 1},
                          {"desde_hora": "19:00", "hasta_hora": "22:00", "tope": 1}])
        # Sin la llave, la lista está vacía: el premio vale a cualquier hora.
        self.assertEqual(configmod.desde_dict(base()).premios[0].franjas, [])

    def test_franjas_invalidas(self):
        def con_franjas(franjas):
            return base(premios=[{"id": "silla", "nombre": "Silla", "peso": 2, "franjas": franjas}])
        self.espera_error(con_franjas([{"desde_hora": "13:00", "hasta_hora": "25:00"}]), "hasta_hora")
        self.espera_error(con_franjas([{"desde_hora": "16:00", "hasta_hora": "13:00"}]), "anterior")
        self.espera_error(con_franjas([{"desde_hora": "13:00", "hasta_hora": "13:00"}]), "anterior")
        self.espera_error(con_franjas([{"desde_hora": "13:00", "hasta_hora": "16:00", "tope": 0}]), "tope")
        self.espera_error(con_franjas([{"desde_hora": "13:00", "hasta_hora": "16:00", "tope": "1"}]), "tope")
        self.espera_error(con_franjas([{"desde_hora": "13:00"}]), "faltan")
        self.espera_error(con_franjas([{"desde_hora": "13:00", "hasta_hora": "16:00", "peso": 12}]), "peso")
        self.espera_error(con_franjas([["13:00", "16:00"]]), "objeto")
        self.espera_error(con_franjas("13:00-16:00"), "lista")

    def test_consuelo_sin_peso_vale_cero(self):
        """Omitir la llave es el comportamiento de antes de la Fase 4c: consuelo sin papelitos.

        Se ancla **por igualdad** y en los dos caminos —sin bloque `consuelo` y
        con bloque pero sin `peso`— porque el valor por omisión del código es lo
        único que separa un `config.json` viejo de uno nuevo: si alguien pusiera
        217 como defecto, cualquier instalación sin la llave empezaría a repartir
        consuelo sin que nadie lo decidiera.
        """
        self.assertEqual(configmod.desde_dict(base()).juego.consuelo.peso, 0)
        con_bloque = base(juego={"consuelo": {"titulo": "SIGUE PARTICIPANDO",
                                              "texto": "¡Gracias por jugar!"}})
        self.assertEqual(configmod.desde_dict(con_bloque).juego.consuelo.peso, 0)
        self.assertEqual(configmod.desde_dict(base(juego={"consuelo": {"peso": 0}})).juego.consuelo.peso, 0)
        self.assertEqual(configmod.desde_dict(base(juego={"consuelo": {"peso": 217}})).juego.consuelo.peso, 217)

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
        cfg = configmod.cargar(RUTA_CONFIG)
        # Hasta el 2026-09-15 estas dos líneas anclaban los premios de relleno
        # (`len == 7` y `premios[2].stock == 1`, que era el TEST 3). La Fase 4b
        # cargó los siete premios reales del evento, así que ahora se anclan
        # CENSOS derivados de la tabla del §1 del documento del evento: los ids
        # en su orden y las dos sumas que ese §1 declara («167 piezas, 33 al día
        # más la hielera el jueves y el viernes» = 34 de tope diario sumado).
        # La igualdad campo por campo contra el documento vive en
        # TestPremiosOficialesDelEvento.
        self.assertEqual(len(cfg.premios), 7)
        self.assertEqual([p.id for p in cfg.premios],
                         ["hielera", "silla", "bbq", "tacos3", "tacos2", "cerveza", "agua"])
        por_id = {p.id: p for p in cfg.premios}
        self.assertEqual((por_id["hielera"].stock, por_id["agua"].stock), (2, 55))
        self.assertEqual(sum(p.stock for p in cfg.premios), 167)
        self.assertEqual(sum(p.tope_diario for p in cfg.premios), 34)
        # Decisión del usuario del 2026-09-13, viéndolo en la demo: el boleto de
        # consuelo NO dice que los premios se agotaron. Se ancla por igualdad y no
        # por presencia porque el valor por omisión del código (ruleta/config.py)
        # sigue siendo el texto viejo: borrar el bloque juego.consuelo del
        # config.json lo devolvería sin que nada más se queje.
        self.assertEqual(cfg.juego.consuelo.titulo, "SIGUE PARTICIPANDO")
        self.assertEqual(cfg.juego.consuelo.texto, "¡Gracias por jugar!")
        # El `peso` del consuelo (Fase 4c) NO se copia aquí a propósito: lo ancla
        # TestPremiosOficialesDelEvento.test_config_json_lleva_el_peso_de_consuelo_del_documento,
        # que lo DERIVA del §5.2 del documento del evento en vez de transcribirlo.
        self.assertGreater(cfg.juego.consuelo.peso, 0)
        # Censo derivado de las franjas (Fase 4d): las cinco del §3 del documento
        # del evento, y SOLO en los tres premios grandes. Los valores exactos los
        # compara TestPremiosOficialesDelEvento contra el documento.
        self.assertEqual({p.id: len(p.franjas) for p in cfg.premios if p.franjas},
                         {"hielera": 1, "silla": 2, "bbq": 2})
        self.assertEqual(sum(len(p.franjas) for p in cfg.premios), 5)
        self.assertIsNotNone(cfg.juego.horario)
        self.assertGreater(cfg.juego.separacion_min_entre_premios, 0)
        self.assertGreater(cfg.juego.espera_hora_seg, 0)

    def test_config_json_del_proyecto_apunta_a_la_impresora_usb(self):
        """Lo medido en la Pi el 2026-09-11: USB por /dev/ruleta-impresora, con pitido.

        La Pi se actualiza con `git pull`, así que este archivo es el que va a
        quedar allá: si alguien lo devuelve a Bluetooth, el kiosco arranca
        buscando una MAC de relleno y no imprime.
        """
        imp = configmod.cargar(RUTA_CONFIG).impresora
        self.assertEqual(
            (imp.tipo, imp.ruta, imp.beep, imp.consultar_estado, imp.mac, imp.canal,
             imp.codepage, imp.codepage_n, imp.chars_por_linea, imp.ancho_puntos, imp.corte),
            ("archivo", "/dev/ruleta-impresora", True, True, "00:00:00:00:00:00", 1,
             "cp858", 19, 48, 576, "auto"))


class TestPremiosOficialesDelEvento(unittest.TestCase):
    """Los premios de `config.json` se DERIVAN del documento del evento.

    La fuente de verdad NO es `config.json`: es
    `docs/evento-2026-09-asadero-33.md`, que lo dice con todas sus letras en su
    §6, paso 1 —«si los dos archivos dicen cosas distintas, gana este documento
    y el otro se rehace»— porque ese documento es el que el usuario edita a mano.

    Por eso estas pruebas **no copian** la tabla de premios: una copia se
    desincroniza en silencio el día en que alguien edita el documento y se olvida
    del `config.json` (o al revés). Lo que hacen es **parsear el bloque de código
    `json` del §5.1** —el que trae la lista `"premios"`— y compararlo **por
    igualdad**, campo por campo y en orden, con lo que el validador real carga de
    `config.json`.

    Cargado el 2026-09-15 (Fase 4b, plan `docs/planes/fase-4b-config-oficial.md`).
    """

    def bloque_del_documento(self, llave: str):
        """El único bloque ```json del documento que EMPIEZA por esa llave.

        Los bloques se localizan por su contenido y no por el número de sección,
        porque las secciones se mueven. Se busca por dónde EMPIEZA el bloque —y
        no por «lo menciona»— porque desde la Fase 4d hay bloques anidados: el
        `"juego"` del §5.1 lleva dentro un `"consuelo"` y un `"horario"` que
        también tienen bloque propio en el §5.2.
        """
        texto = RUTA_EVENTO.read_text(encoding="utf-8")
        bloques = re.findall(r"^```json\s*?\n(.*?)^```", texto, re.DOTALL | re.MULTILINE)
        empiezan = [b for b in bloques if b.lstrip().startswith(f'"{llave}"')]
        self.assertEqual(
            len(empiezan), 1,
            f"En {RUTA_EVENTO.name} debe haber EXACTAMENTE un bloque de código json que empiece "
            f"por \"{llave}\"; se encontraron {len(empiezan)} entre {len(bloques)} bloques json. "
            f"Si el documento cambió de forma, arregla este golden: NO lo borres.")
        # Es un fragmento de objeto ("premios": [...]), no un JSON completo: se
        # envuelve en llaves para parsearlo tal cual está escrito, sin retocarlo.
        return json.loads("{" + empiezan[0] + "}")[llave]

    def premios_del_documento(self):
        """La lista `premios` del §5.1, parseada del documento, no transcrita."""
        premios = self.bloque_del_documento("premios")
        self.assertEqual(len(premios), 7,
                         "La tabla del §1 del documento del evento fija SIETE premios.")
        for i, p in enumerate(premios, start=1):
            faltan = sorted(set(CLAVES_OBLIGATORIAS) - set(p))
            self.assertEqual(faltan, [],
                             f"Al premio #{i} del §5.1 le faltan las llaves {faltan}.")
        return premios

    def consuelo_del_documento(self):
        """El bloque `consuelo` del §5.2 (PENDIENTE A), parseado del documento."""
        consuelo = self.bloque_del_documento("consuelo")
        faltan = sorted({"titulo", "texto", "peso"} - set(consuelo))
        self.assertEqual(faltan, [],
                         f"Al bloque `consuelo` del §5.2 le faltan las llaves {faltan}.")
        return consuelo

    def juego_del_documento(self):
        """El bloque `juego` del §5.1, con horario, separación, espera y consuelo."""
        juego = self.bloque_del_documento("juego")
        faltan = sorted({"horario", "separacion_min_entre_premios", "espera_hora_seg",
                         "consuelo"} - set(juego))
        self.assertEqual(faltan, [],
                         f"Al bloque `juego` del §5.1 le faltan las llaves {faltan}.")
        return juego

    def test_config_json_lleva_el_peso_de_consuelo_del_documento(self):
        """Pieza A (Fase 4c): el `peso` del consuelo se DERIVA del §5.2, no se copia.

        Se comparan las tres llaves por igualdad y de una vez: si el usuario
        cambia N en el documento (150 → 117, 250 → 217, 400 → 367) y nadie
        rehace `config.json`, la suite se pone en rojo.
        """
        del_documento = self.consuelo_del_documento()
        cfg = configmod.cargar(RUTA_CONFIG)
        self.assertEqual(
            {"titulo": cfg.juego.consuelo.titulo, "texto": cfg.juego.consuelo.texto,
             "peso": cfg.juego.consuelo.peso},
            {k: del_documento[k] for k in ("titulo", "texto", "peso")},
            "config.json y el §5.2 (PENDIENTE A) de docs/evento-2026-09-asadero-33.md dicen "
            "cosas distintas. Gana el DOCUMENTO (§6, paso 1): corrige config.json, no el golden.")

    def test_config_json_lleva_el_bloque_de_juego_del_documento(self):
        """Piezas B, C y D (Fase 4d): el bloque `juego` del §5.1 manda sobre config.json.

        Se comparan **de una vez y por igualdad** el horario del evento, la
        separación mínima entre premios, la espera de la hora al arrancar y el
        consuelo entero: si el usuario cambia una hora en el documento y nadie
        rehace `config.json`, la suite se pone en rojo.
        """
        del_documento = self.juego_del_documento()
        j = configmod.cargar(RUTA_CONFIG).juego
        self.assertIsNotNone(j.horario, "config.json tiene que traer el bloque juego.horario.")
        del_config = {
            "horario": {"abre": j.horario.abre, "cierra": j.horario.cierra,
                        "fuera_de_horario": j.horario.fuera_de_horario},
            "separacion_min_entre_premios": j.separacion_min_entre_premios,
            "espera_hora_seg": j.espera_hora_seg,
            "consuelo": {"titulo": j.consuelo.titulo, "texto": j.consuelo.texto,
                         "peso": j.consuelo.peso},
        }
        self.assertEqual(
            del_config, del_documento,
            "config.json y el bloque \"juego\" del §5.1 de docs/evento-2026-09-asadero-33.md "
            "dicen cosas distintas. Gana el DOCUMENTO (§6, paso 1): corrige config.json, no el "
            "golden.")

    def test_el_5_2_dice_lo_mismo_que_el_5_1_en_los_tres_bloques_que_se_repiten(self):
        """El documento tiene que estar de acuerdo consigo mismo.

        El §5.2 vuelve a escribir, pieza por pieza, tres cosas que el §5.1 ya
        trae dentro de `"juego"`: el consuelo (A), el horario (C) y la espera de
        la hora (D). Están las dos veces a propósito —el §5.2 explica cada pieza
        por separado— y por eso hay que vigilar que no se separen: `config.json`
        se compara contra el §5.1, así que una pieza mal copiada en el §5.2
        pasaría en silencio.
        """
        juego = self.juego_del_documento()
        self.assertEqual(self.consuelo_del_documento(), juego["consuelo"],
                         "El bloque `consuelo` del §5.2 (A) no dice lo mismo que el del §5.1.")
        self.assertEqual(self.bloque_del_documento("horario"), juego["horario"],
                         "El bloque `horario` del §5.2 (C) no dice lo mismo que el del §5.1.")
        self.assertEqual(self.bloque_del_documento("espera_hora_seg"), juego["espera_hora_seg"],
                         "La `espera_hora_seg` del §5.2 (D) no dice lo mismo que la del §5.1.")

    def test_la_franja_de_ejemplo_del_5_2_B_es_la_de_la_hielera(self):
        """El §5.2 B dice ser «la franja de la hielera tal cual está cargada»: que lo sea."""
        cfg = configmod.cargar(RUTA_CONFIG)
        hielera = next(p for p in cfg.premios if p.id == "hielera")
        self.assertEqual(
            self.bloque_del_documento("franjas"), como_dict(hielera.franjas),
            "El ejemplo de `franjas` del §5.2 (PENDIENTE B) ya no es la franja real de la "
            "hielera. Gana el DOCUMENTO: si la franja cambió, cámbiala también en el §5.1 y en "
            "config.json.")

    def test_las_probabilidades_del_2_las_calcula_el_programa(self):
        """La tabla de la tómbola del §2 tiene que salir de los pesos reales.

        El §2 explica cuánto se gana con un par de ejemplos («una pieza de AGUA
        FRESCA abierta: 11 + 10 = 21 papelitos, gana el 52.4 %»). Esos números
        **no se transcriben**: se comprueban contra el `peso` que ese premio
        tiene en `config.json`, contra `juego.consuelo.peso` y contra la división
        hecha aquí. Cambiar un peso sin corregir el documento —o al revés— pone
        la suite en rojo. Es lo que sustituye al golden de la regla «N − 33»,
        que murió con el modelo viejo el 2026-09-16.
        """
        texto = RUTA_EVENTO.read_text(encoding="utf-8")
        filas = FILA_TOMBOLA.findall(texto)
        self.assertGreaterEqual(
            len(filas), 2,
            "No se encontró la tabla «Qué está abierto en ese momento | Papelitos | Gana» del §2 "
            "del documento del evento. Si el documento cambió de forma, arregla este golden: NO "
            "lo borres.")
        cfg = configmod.cargar(RUTA_CONFIG)
        por_nombre = {p.nombre: p for p in cfg.premios}
        for nombre, peso, sumando, consuelo, total, porcentaje in filas:
            with self.subTest(premio=nombre):
                premio = por_nombre.get(nombre)
                self.assertIsNotNone(premio, f"El §2 nombra un premio que no está en config.json: "
                                             f"{nombre!r}. Ids cargados: {sorted(por_nombre)}")
                self.assertEqual(int(peso), premio.peso,
                                 f"El §2 dice que {nombre} tiene peso {peso} y config.json dice "
                                 f"{premio.peso}.")
                self.assertEqual(int(sumando), premio.peso)
                self.assertEqual(int(consuelo), cfg.juego.consuelo.peso,
                                 f"El §2 suma {consuelo} papelitos de consuelo y config.json tiene "
                                 f"{cfg.juego.consuelo.peso}.")
                self.assertEqual(int(total), int(sumando) + int(consuelo),
                                 f"La suma del §2 para {nombre} no cuadra.")
                self.assertEqual(porcentaje, f"{100.0 * int(sumando) / int(total):.1f}",
                                 f"El porcentaje del §2 para {nombre} no es el que sale de "
                                 f"dividir {sumando} entre {total}.")

    def test_la_nota_historica_del_2_sigue_obedeciendo_su_regla_N_menos_33(self):
        """La nota histórica del §2 se conserva, y tiene que seguir siendo cierta.

        El modelo viejo («el peso es el cupo», peso del consuelo = **N − 33**)
        murió el 2026-09-16 con el reparto por horas, pero el §2 lo conserva
        como nota histórica porque hay fichas que razonan desde ahí y porque
        vuelve a valer si alguien quita el horario. La tabla de equivalencias se
        lee **solo dentro de esa nota** —leyéndola de todo el documento,
        cualquier flecha entre números la envenenaría— y tiene que cumplir la
        regla que la propia nota escribe.
        """
        texto = RUTA_EVENTO.read_text(encoding="utf-8")
        nota = re.search(r"### Nota histórica.*?(?=\n---|\n## )", texto, re.DOTALL)
        self.assertIsNotNone(
            nota, "No se encontró la «Nota histórica» del §2 del documento del evento. Si el "
                  "documento cambió de forma, arregla este golden: NO lo borres.")
        pares = [(int(n), int(peso)) for n, peso in re.findall(r"(\d+)\s*→\s*(\d+)", nota.group(0))]
        self.assertNotEqual(
            pares, [], "La nota histórica del §2 ya no trae la tabla «N → peso del consuelo».")
        self.assertEqual([(n, peso) for n, peso in pares if peso != n - 33], [],
                         f"La tabla «N → peso» de la nota histórica no obedece la regla N − 33 "
                         f"que la propia nota escribe: {pares}.")

    def test_config_json_lleva_exactamente_los_premios_del_documento(self):
        """Igualdad campo por campo y en orden, no «están todos los ids».

        Desde la Fase 4d se comparan también las `franjas` (pieza B), que es lo
        que decide a qué horas puede salir cada premio grande.
        """
        del_documento = [{k: como_dict(p.get(k, [])) if k == "franjas" else p[k]
                          for k in CLAVES_DEL_DOCUMENTO}
                         for p in self.premios_del_documento()]
        cfg = configmod.cargar(RUTA_CONFIG)
        del_config = [{k: como_dict(getattr(p, k)) for k in CLAVES_DEL_DOCUMENTO}
                      for p in cfg.premios]
        self.assertEqual(
            del_config, del_documento,
            "config.json y el §5.1 de docs/evento-2026-09-asadero-33.md dicen cosas "
            "distintas. Gana el DOCUMENTO (§6, paso 1): corrige config.json, no el golden.")

    def test_los_premios_del_config_todavia_no_traen_fechas(self):
        """Decisión D1 de la Fase 4b: `desde`/`hasta` se cargan en la pasada final.

        El bloque del §5.1 **sí** trae las fechas (21 al 25 de septiembre de
        2026), y por eso el golden de arriba compara solo las siete llaves de
        `CLAVES_DEL_DOCUMENTO`. Se cargaron los premios **sin** fechas a
        propósito, el 2026-09-15: con el `desde` puesto en el 21, **ningún premio
        estaría disponible** en las pruebas del usuario del día 16 y solo saldrían
        boletos de consuelo, que es lo contrario de lo que pidió.

        **Esta prueba está escrita para caerse** el día en que alguien cargue las
        fechas, que es antes del lunes 21 (ficha **F-259**). Cuando eso pase: se
        borra este test y se añaden "desde" y "hasta" a `CLAVES_DEL_DOCUMENTO`,
        con lo que el golden de arriba pasa a compararlas también contra el
        documento. Lo que NO se hace es relajar la comparación.
        """
        crudo = json.loads(RUTA_CONFIG.read_text(encoding="utf-8"))
        con_fechas = [p["id"] for p in crudo["premios"] if "desde" in p or "hasta" in p]
        self.assertEqual(
            con_fechas, [],
            "Se cargaron fechas en config.json: lee el docstring de esta prueba y añade "
            "'desde' y 'hasta' a CLAVES_DEL_DOCUMENTO en vez de borrar el assert.")
        # …y el documento sí las trae: si dejara de traerlas, la ficha F-259 se
        # quedaría sin fuente de dónde copiarlas.
        incompletos = [p["id"] for p in self.premios_del_documento()
                       if not p.get("desde") or not p.get("hasta")]
        self.assertEqual(incompletos, [],
                         "El §5.1 del documento del evento debe traer 'desde' y 'hasta' en los "
                         "siete premios: son los que faltan por cargar (ficha F-259).")


if __name__ == "__main__":
    unittest.main()
