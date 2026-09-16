import json
import re
import tempfile
import unittest
from datetime import date
from pathlib import Path

from ruleta import config as configmod
from ruleta.config import ErrorConfig

RAIZ = Path(__file__).resolve().parent.parent
RUTA_CONFIG = RAIZ / "config.json"
RUTA_EVENTO = RAIZ / "docs" / "evento-2026-09-asadero-33.md"

# Las llaves que la Fase 4b copió del documento del evento al config.json.
# NO están 'desde' ni 'hasta': se cargan en la pasada final antes del lunes 21
# (decisión D1 del plan, ficha F-259). Lo ancla
# TestPremiosOficialesDelEvento.test_los_premios_del_config_todavia_no_traen_fechas.
CLAVES_DEL_DOCUMENTO = ("id", "nombre", "detalle", "stock", "tope_diario", "peso")


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

    def premios_del_documento(self):
        """La lista `premios` del §5.1, parseada del documento, no transcrita."""
        texto = RUTA_EVENTO.read_text(encoding="utf-8")
        bloques = re.findall(r"^```json\s*?\n(.*?)^```", texto, re.DOTALL | re.MULTILINE)
        con_premios = [b for b in bloques if '"premios"' in b]
        self.assertEqual(
            len(con_premios), 1,
            f"En {RUTA_EVENTO.name} debe haber EXACTAMENTE un bloque de código json con la "
            f"lista \"premios\" (el del §5.1); se encontraron {len(con_premios)} entre "
            f"{len(bloques)} bloques json. Si el documento cambió de forma, arregla este "
            f"golden: NO lo borres.")
        # El bloque es un fragmento de objeto ("premios": [...]), no un JSON
        # completo; se envuelve en llaves para poder parsearlo tal cual está
        # escrito en el documento, sin retocarlo.
        premios = json.loads("{" + con_premios[0] + "}")["premios"]
        self.assertEqual(len(premios), 7,
                         "La tabla del §1 del documento del evento fija SIETE premios.")
        for i, p in enumerate(premios, start=1):
            faltan = sorted(set(CLAVES_DEL_DOCUMENTO) - set(p))
            self.assertEqual(faltan, [],
                             f"Al premio #{i} del §5.1 le faltan las llaves {faltan}.")
        return premios

    def consuelo_del_documento(self):
        """El bloque `consuelo` del §5.2 (PENDIENTE A), parseado del documento.

        Es el bloque que la Fase 4c construyó: `titulo`, `texto` y el `peso`
        nuevo. Se busca por contenido —el único bloque ```json que menciona
        `"consuelo"`— y no por número de sección, porque las secciones se mueven.
        """
        texto = RUTA_EVENTO.read_text(encoding="utf-8")
        bloques = re.findall(r"^```json\s*?\n(.*?)^```", texto, re.DOTALL | re.MULTILINE)
        con_consuelo = [b for b in bloques if '"consuelo"' in b]
        self.assertEqual(
            len(con_consuelo), 1,
            f"En {RUTA_EVENTO.name} debe haber EXACTAMENTE un bloque de código json con "
            f"\"consuelo\" (el del §5.2, PENDIENTE A); se encontraron {len(con_consuelo)} entre "
            f"{len(bloques)} bloques json. Si el documento cambió de forma, arregla este "
            f"golden: NO lo borres.")
        # Igual que el del §5.1, es un fragmento de objeto: se envuelve en llaves
        # para parsearlo tal cual está escrito, sin retocarlo.
        consuelo = json.loads("{" + con_consuelo[0] + "}")["consuelo"]
        faltan = sorted({"titulo", "texto", "peso"} - set(consuelo))
        self.assertEqual(faltan, [],
                         f"Al bloque `consuelo` del §5.2 le faltan las llaves {faltan}.")
        return consuelo

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

    def test_el_peso_del_documento_obedece_la_regla_N_menos_33_del_su_propio_2(self):
        """El documento tiene que estar de acuerdo consigo mismo: §5.2 contra §2.

        El §2 («Cómo cambiar N») escribe la regla **N − 33** y su tabla de
        equivalencias (150 → 117 · 200 → 167 · 250 → 217 · 300 → 267 · 400 →
        367). Esto comprueba dos cosas por igualdad: (a) que esa tabla obedezca
        la regla, y (b) que el `peso` del §5.2 sea una de sus entradas. Así un
        peso tecleado a mano —218, 271— se pone en rojo, y a la vez el usuario
        puede responder la **pregunta 1 del §4** con CUALQUIERA de las N
        tabuladas sin que la suite se queje: es el cambio que el propio documento
        manda hacer, y **no debe obligar a tocar la tabla de escenarios del §2**.
        """
        texto = RUTA_EVENTO.read_text(encoding="utf-8")
        # Lista, NO diccionario: el documento escribe esa tabla DOS veces (§2 y
        # §5.2), y con un dict la segunda tapaba a la primera, así que un error
        # en la del §2 pasaba en verde.
        pares = [(int(n), int(peso)) for n, peso in re.findall(r"(\d+)\s*→\s*(\d+)", texto)]
        self.assertNotEqual(
            pares, [], "No se encontró en el documento del evento la tabla de equivalencias "
                       "«N → peso del consuelo» del §2. Si el documento cambió de forma, arregla "
                       "este golden: NO lo borres.")
        self.assertEqual([(n, peso) for n, peso in pares if peso != n - 33], [],
                         f"La tabla «N → peso» del documento del evento no obedece su propia "
                         f"regla N − 33: {pares}.")
        # «Las N que el §2 tabula» hay que leerlas del §2 y de ningún otro sitio:
        # leyéndolas de todo el documento, añadir la N solo al §5.2 bastaba para
        # pasar en verde.
        parrafo = re.search(r"\*\*Cómo cambiar N:\*\*(.*?)\n\n", texto, re.DOTALL)
        self.assertIsNotNone(
            parrafo, "No se encontró el párrafo «Cómo cambiar N» del §2 (Aviso 2) del documento "
                     "del evento. Si el documento cambió de forma, arregla este golden: NO lo "
                     "borres.")
        del_2 = {int(peso) for _, peso in re.findall(r"(\d+)\s*→\s*(\d+)", parrafo.group(1))}
        self.assertIn(self.consuelo_del_documento()["peso"], del_2,
                      f"El `peso` del consuelo del §5.2 no es ninguna de las N tabuladas en el "
                      f"§2 ({sorted(del_2)}). Si el usuario eligió otra N, añádela allí "
                      f"con su N − 33; NO toques la tabla de escenarios del §2.")

    def test_config_json_lleva_exactamente_los_premios_del_documento(self):
        """Igualdad campo por campo y en orden, no «están todos los ids»."""
        del_documento = [{k: p[k] for k in CLAVES_DEL_DOCUMENTO}
                         for p in self.premios_del_documento()]
        cfg = configmod.cargar(RUTA_CONFIG)
        del_config = [{k: getattr(p, k) for k in CLAVES_DEL_DOCUMENTO} for p in cfg.premios]
        self.assertEqual(
            del_config, del_documento,
            "config.json y el §5.1 de docs/evento-2026-09-asadero-33.md dicen cosas "
            "distintas. Gana el DOCUMENTO (§6, paso 1): corrige config.json, no el golden.")

    def test_los_premios_del_config_todavia_no_traen_fechas(self):
        """Decisión D1 de la Fase 4b: `desde`/`hasta` se cargan en la pasada final.

        El bloque del §5.1 **sí** trae las fechas (21 al 25 de septiembre de
        2026), y por eso el golden de arriba compara solo las seis llaves de
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
