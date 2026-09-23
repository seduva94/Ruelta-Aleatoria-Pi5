"""Goldens de la instalación en la Pi: `instalar.sh`, `ruleta.service` y las
revisiones del diagnóstico que comprueban justo eso (la ruta del dispositivo,
los permisos y las versiones de las librerías).

Estas pruebas LEEN los archivos del repositorio; no ejecutan nada ni tocan
hardware. Comparan **cuerpos enteros por igualdad** (el bloque de la regla
udev, la unidad de systemd completa, el conjunto de grupos que se agregan), no
líneas sueltas: así una regla con un dígito cambiado, un paso mal renumerado o
un `RestartPreventExitStatus` perdido salen en rojo.
"""

import io
import json
import logging
import re
import stat
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from importlib import metadata
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import PIL

from ruleta import __main__ as cli, config as configmod

RAIZ = Path(__file__).resolve().parent.parent
INSTALADOR = (RAIZ / "instalar.sh").read_text(encoding="utf-8")
SERVICIO = (RAIZ / "ruleta.service").read_text(encoding="utf-8")

# La línea exacta que se aplicó a mano en la Pi la noche del 2026-09-11 y que
# el instalador tiene que dejar escrita (VID:PID medidos con lsusb: 0418:5011).
REGLA_IMPRESORA = (
    'SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*", ATTRS{idVendor}=="0418", '
    'ATTRS{idProduct}=="5011", MODE="0660", GROUP="lp", SYMLINK+="ruleta-impresora"\n'
)
REGLA_GPIO = 'SUBSYSTEM=="gpio", KERNEL=="gpiochip*", DRIVERS=="pinctrl-rp1", SYMLINK+="gpiochip4"\n'


# --------------------------------------------------------------------------- #
# Utilidades: derivar lo que hace el instalador y leer la unidad de systemd
# --------------------------------------------------------------------------- #

def cuerpo_heredoc(texto: str, archivo: str) -> str:
    """Cuerpo escrito con  cat > <archivo> <<'EOF' ... EOF  (entero, con su salto final)."""
    patron = re.compile(r"^cat > " + re.escape(archivo) + r" <<'EOF'\n(.*?)^EOF$\n", re.S | re.M)
    encontrados = patron.findall(texto)
    if len(encontrados) != 1:
        raise AssertionError(f"se esperaba un solo bloque para {archivo}, hay {len(encontrados)}")
    return encontrados[0]


def archivos_de_reglas(texto: str) -> set[str]:
    """Conjunto derivado de archivos de /etc/udev/rules.d que el instalador escribe."""
    return set(re.findall(r"/etc/udev/rules\.d/[^\s]+", texto))


def grupos_que_agrega(texto: str) -> set[str]:
    """Conjunto derivado de los grupos de cada  usermod -aG <grupo>."""
    return set(re.findall(r"usermod -aG (\S+)", texto))


def pasos_del_instalador(texto: str) -> list[str]:
    """Lista derivada de los encabezados  == n/N titulo  en el orden en que salen."""
    return re.findall(r'^echo "== (\d+/\d+ .*)"$', texto, re.M)


def ordenes_udevadm(texto: str) -> list[str]:
    """Lista derivada de las llamadas a udevadm, sin la parte de redirección."""
    return [linea.split(" 2>")[0].strip()
            for linea in texto.splitlines() if linea.strip().startswith("udevadm ")]


def paquetes_apt(texto: str) -> list[str]:
    encontrados = re.findall(r"^apt-get install -y (.*)$", texto, re.M)
    if len(encontrados) != 1:
        raise AssertionError(f"se esperaba un solo apt-get install, hay {len(encontrados)}")
    return encontrados[0].split()


def leer_unidad(texto: str) -> dict[str, list[tuple[str, str]]]:
    """Parsea el .service a {sección: [(llave, valor), ...]}.

    Se guarda como lista de pares porque systemd admite llaves repetidas
    (`Environment=`) y el orden importa para leerlo.
    """
    unidad: dict[str, list[tuple[str, str]]] = {}
    seccion = None
    for cruda in texto.splitlines():
        linea = cruda.strip()
        if not linea or linea.startswith("#"):
            continue
        if linea.startswith("[") and linea.endswith("]"):
            seccion = linea[1:-1]
            unidad[seccion] = []
            continue
        llave, sep, valor = linea.partition("=")
        if not sep or seccion is None:
            raise AssertionError(f"línea que no es 'llave=valor' en ruleta.service: {cruda!r}")
        unidad[seccion].append((llave.strip(), valor.strip()))
    return unidad


UNIDAD = leer_unidad(SERVICIO)


# --------------------------------------------------------------------------- #
# instalar.sh
# --------------------------------------------------------------------------- #

class TestInstalador(unittest.TestCase):
    def test_regla_udev_de_la_impresora_exacta(self):
        # Cuerpo entero, no "contiene": un dígito distinto en el VID:PID, otro
        # grupo o el SYMLINK borrado dejan la impresora sin permisos.
        self.assertEqual(cuerpo_heredoc(INSTALADOR, "/etc/udev/rules.d/61-ruleta-impresora-usb.rules"),
                         REGLA_IMPRESORA)

    def test_regla_udev_del_gpio_intacta(self):
        self.assertEqual(cuerpo_heredoc(INSTALADOR, "/etc/udev/rules.d/60-ruleta-rp1-gpiochip4.rules"),
                         REGLA_GPIO)

    def test_reglas_udev_declaradas(self):
        self.assertEqual(archivos_de_reglas(INSTALADOR),
                         {"/etc/udev/rules.d/60-ruleta-rp1-gpiochip4.rules",
                          "/etc/udev/rules.d/61-ruleta-impresora-usb.rules"})

    def test_grupos_que_agrega_el_instalador(self):
        self.assertEqual(grupos_que_agrega(INSTALADOR), {"gpio", "bluetooth", "lp"})

    def test_pasos_numerados_completos_y_en_orden(self):
        self.assertEqual(pasos_del_instalador(INSTALADOR), [
            "1/7 Paquetes del sistema",
            "2/7 Grupos del usuario (gpio para los botones)",
            "3/7 Bluetooth encendido y habilitado al arranque (impresora de respaldo)",
            "4/7 Regla udev para el chip GPIO de la Pi 5",
            "5/7 Impresora USB (permisos y nombre fijo del dispositivo)",
            "6/7 Carpeta de datos y permisos",
            "7/7 Servicio systemd",
        ])

    def test_udevadm_recarga_las_dos_reglas(self):
        self.assertEqual(ordenes_udevadm(INSTALADOR), [
            "udevadm control --reload",
            "udevadm trigger --subsystem-match=gpio",
            "udevadm control --reload-rules",
            "udevadm trigger --subsystem-match=usbmisc",
        ])

    def test_sigue_instalando_los_mismos_paquetes(self):
        self.assertEqual(paquetes_apt(INSTALADOR),
                         ["python3", "python3-gpiozero", "python3-lgpio", "python3-pil",
                          "bluez", "bluez-tools", "rfkill"])

    def test_sigue_registrando_y_habilitando_el_servicio(self):
        # El Bluetooth (respaldo) y el servicio no se tocaron al meter la impresora USB.
        for orden in ("systemctl enable --now bluetooth",
                      "systemctl daemon-reload",
                      "systemctl enable ruleta.service"):
            self.assertIn(orden, INSTALADOR)

    def test_el_instalador_es_idempotente_en_lo_que_escribe(self):
        # Todo lo que crea usa 'cat >' (sobrescribe) o '-aG' (agrega sin quitar):
        # volver a correrlo no duplica reglas ni saca al usuario de un grupo.
        self.assertEqual(re.findall(r"^cat >> ", INSTALADOR, re.M), [])
        self.assertEqual(re.findall(r"usermod -G ", INSTALADOR), [])


# --------------------------------------------------------------------------- #
# ruleta.service
# --------------------------------------------------------------------------- #

class TestServicio(unittest.TestCase):
    def test_unidad_completa(self):
        self.assertEqual(UNIDAD, {
            "Unit": [
                ("Description", "Ruleta de premios Asadero 33 (boton -> boleto en impresora USB o Bluetooth)"),
                ("After", "bluetooth.service network.target"),
                ("Wants", "bluetooth.service"),
                ("StartLimitIntervalSec", "0"),
            ],
            "Service": [
                ("Type", "simple"),
                ("User", "@USUARIO@"),
                ("SupplementaryGroups", "gpio lp"),
                ("WorkingDirectory", "@DIR@"),
                ("Environment", "GPIOZERO_PIN_FACTORY=lgpio"),
                ("Environment", "PYTHONUNBUFFERED=1"),
                ("Environment", "PYTHONIOENCODING=utf-8"),
                ("ExecStart", "/usr/bin/python3 -m ruleta"),
                ("Restart", "always"),
                ("RestartSec", "3"),
                ("RestartPreventExitStatus", "2"),
                ("KillSignal", "SIGTERM"),
                ("TimeoutStopSec", "60"),
            ],
            "Install": [("WantedBy", "multi-user.target")],
        })

    def test_los_errores_de_configuracion_no_se_reintentan(self):
        servicio = dict(UNIDAD["Service"])
        self.assertEqual(servicio["Restart"], "always")
        self.assertEqual(servicio["RestartPreventExitStatus"], "2")

    def test_el_servicio_puede_escribir_en_la_impresora_usb(self):
        self.assertEqual(dict(UNIDAD["Service"])["SupplementaryGroups"], "gpio lp")


# --------------------------------------------------------------------------- #
# Códigos de salida: son el contrato con RestartPreventExitStatus
# --------------------------------------------------------------------------- #

CODIGO_CONFIG = int(dict(UNIDAD["Service"])["RestartPreventExitStatus"])


def escribir_config(carpeta: Path, impresora: dict, crudo_texto: str | None = None) -> str:
    ruta = carpeta / "config.json"
    if crudo_texto is not None:
        ruta.write_text(crudo_texto, encoding="utf-8")
    else:
        ruta.write_text(json.dumps({
            "negocio": {"nombre": "Asadero 33", "logo": None},
            "impresora": impresora,
            "premios": [{"id": "a", "nombre": "A", "peso": 1}],
            "carpeta_datos": "datos",
        }), encoding="utf-8")
    return str(ruta)


class TestCodigosDeSalida(unittest.TestCase):
    """El servicio solo deja de reintentar con el código que dice la unidad."""

    @staticmethod
    def cerrar_log():
        """`main` monta el log dentro de la carpeta temporal: hay que soltar el archivo."""
        raiz = logging.getLogger()
        for h in list(raiz.handlers):
            raiz.removeHandler(h)
            try:
                h.close()
            except (OSError, ValueError):
                pass

    def tearDown(self):
        self.cerrar_log()

    def correr(self, ruta_config: str):
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                return cli.main(["--config", ruta_config])
        finally:
            self.cerrar_log()

    def test_config_mal_formada_sale_con_el_codigo_de_configuracion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_config(Path(tmp), {}, crudo_texto='{"negocio": {"nombre": "X",}}')
            with self.assertRaises(SystemExit) as ctx:
                self.correr(ruta)
        self.assertEqual(ctx.exception.code, CODIGO_CONFIG)

    def test_llave_desconocida_sale_con_el_codigo_de_configuracion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_config(Path(tmp), {"tipo": "vista", "velocidad": 9})
            with self.assertRaises(SystemExit) as ctx:
                self.correr(ruta)
        self.assertEqual(ctx.exception.code, CODIGO_CONFIG)

    def test_mac_de_relleno_sale_con_el_codigo_de_configuracion(self):
        # Es el caso medido en la Pi: 118 reinicios en bucle por esta MAC.
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_config(Path(tmp), {"tipo": "bluetooth", "mac": "00:00:00:00:00:00"})
            with self.assertRaises(SystemExit) as ctx:
                self.correr(ruta)
        self.assertEqual(ctx.exception.code, CODIGO_CONFIG)

    def test_inventario_ocupado_no_usa_el_codigo_de_configuracion(self):
        # Ese sí es transitorio (el servicio ya corría): systemd debe reintentarlo.
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_config(Path(tmp), {"tipo": "vista"})
            with mock.patch.object(cli.Inventario, "bloquear",
                                   side_effect=cli.ErrorBloqueo("candado tomado")):
                with self.assertRaises(SystemExit) as ctx:
                    self.correr(ruta)
        self.assertEqual(ctx.exception.code, 1)
        self.assertNotEqual(ctx.exception.code, CODIGO_CONFIG)

    def test_fallo_de_gpio_no_usa_el_codigo_de_configuracion(self):
        # Un error no controlado sale con 1 (lo que hace Python), no con 2.
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_config(Path(tmp), {"tipo": "vista"})
            with mock.patch.object(cli.Inventario, "bloquear"), \
                 mock.patch.object(cli, "EntradasGPIO", side_effect=OSError("no hay gpiochip")):
                with self.assertRaises(OSError):
                    self.correr(ruta)


# --------------------------------------------------------------------------- #
# Revisiones del diagnóstico (funciones puras)
# --------------------------------------------------------------------------- #

class StatFalso:
    def __init__(self, modo):
        self.st_mode = modo


def stat_de(modo):
    return lambda ruta: StatFalso(modo)


def stat_que_no_existe(ruta):
    raise FileNotFoundError(2, "No such file or directory")


DISPOSITIVO = stat.S_IFCHR | 0o660
ARCHIVO = stat.S_IFREG | 0o644
CARPETA = stat.S_IFDIR | 0o755


class TestRevisarRutaImpresora(unittest.TestCase):
    def test_dispositivo_escribible(self):
        self.assertEqual(
            cli.revisar_ruta_impresora("/dev/ruleta-impresora", stat_fn=stat_de(DISPOSITIVO),
                                       access_fn=lambda ruta, modo: True),
            (True, "  [ok] impresora conectada en /dev/ruleta-impresora (dispositivo, se puede escribir)"))

    def test_dispositivo_sin_permiso_menciona_la_regla_y_el_grupo(self):
        bien, linea = cli.revisar_ruta_impresora("/dev/ruleta-impresora", stat_fn=stat_de(DISPOSITIVO),
                                                 access_fn=lambda ruta, modo: False)
        self.assertEqual(
            (bien, linea),
            (False, "  [!!] sin permiso para escribir en /dev/ruleta-impresora: falta la regla udev "
                    "/etc/udev/rules.d/61-ruleta-impresora-usb.rules o el usuario no está en el "
                    "grupo lp (sudo usermod -aG lp $USER y vuelve a entrar)"))
        # Las dos salidas reales tienen que estar en el mensaje, no una sola.
        self.assertIn("61-ruleta-impresora-usb.rules", linea)
        self.assertIn("grupo lp", linea)

    def test_la_ruta_no_existe(self):
        self.assertEqual(
            cli.revisar_ruta_impresora("/dev/ruleta-impresora", stat_fn=stat_que_no_existe,
                                       access_fn=lambda ruta, modo: True),
            (False, "  [!!] no existe la ruta de la impresora: /dev/ruleta-impresora "
                    "(No such file or directory). Revisa el cable USB y que la impresora esté "
                    "encendida; el nombre /dev/ruleta-impresora lo crea la regla udev que pone instalar.sh"))

    def test_archivo_normal_avisa_pero_no_es_error(self):
        self.assertEqual(
            cli.revisar_ruta_impresora("salida_impresora.bin", stat_fn=stat_de(ARCHIVO),
                                       access_fn=lambda ruta, modo: True),
            (True, "  [??] salida_impresora.bin es un archivo normal, no la impresora: "
                   "sirve para pruebas, pero no va a salir papel"))

    def test_archivo_normal_sin_permiso_si_es_error(self):
        self.assertEqual(
            cli.revisar_ruta_impresora("salida_impresora.bin", stat_fn=stat_de(ARCHIVO),
                                       access_fn=lambda ruta, modo: False),
            (False, "  [!!] no se puede escribir en el archivo salida_impresora.bin"))

    def test_una_carpeta_no_sirve(self):
        self.assertEqual(
            cli.revisar_ruta_impresora("/dev", stat_fn=stat_de(CARPETA), access_fn=lambda ruta, modo: True),
            (False, "  [!!] /dev no es un dispositivo ni un archivo normal: revisa impresora.ruta"))


class TestInventarioDeProduccion(unittest.TestCase):
    """`abrir_inventario` es el único sitio de producción que construye un `Inventario`.

    Importa porque todo lo que el motor necesita de `config.json` —la hora en que
    cambia el día y, desde la Fase 4c, el **peso del boleto de consuelo**— entra
    por ahí. Si alguien añade una segunda fábrica y se olvida de un parámetro, el
    kiosco arranca con un motor a medio configurar y no se queja.
    """

    @staticmethod
    def config_con(carpeta: Path, peso=None, juego=None):
        crudo = {
            "negocio": {"nombre": "Asadero 33", "logo": None},
            "impresora": {"tipo": "vista"},
            "premios": [{"id": "a", "nombre": "A", "peso": 1}],
            "carpeta_datos": str(carpeta),          # absoluta: no toca el repositorio
        }
        if peso is not None:
            crudo["juego"] = {"consuelo": {"peso": peso}}
        if juego is not None:
            crudo["juego"] = {**crudo.get("juego", {}), **juego}
        return configmod.desde_dict(crudo)

    def test_abrir_inventario_pasa_el_horario_y_la_separacion(self):
        """Piezas B, C y D (Fase 4d): el motor tiene que recibir el reloj del evento.

        Sin esto el kiosco arrancaría repartiendo sobre el día entero y jugando
        a cualquier hora, con el `config.json` correcto y sin una sola queja.
        """
        with tempfile.TemporaryDirectory() as tmp:
            cfg = self.config_con(Path(tmp) / "con", juego={
                "horario": {"abre": "12:00", "cierra": "23:00", "fuera_de_horario": "consuelo"},
                "separacion_min_entre_premios": 3})
            inventario = cli.abrir_inventario(cfg)
            self.assertEqual(inventario.horario, cfg.juego.horario)
            self.assertEqual(inventario.separacion_min_entre_premios, 3)
            # Y con OTROS valores, otro motor: si estuvieran quemados en el
            # código en vez de derivarse del cfg, esto pasaría igual.
            otro_cfg = self.config_con(Path(tmp) / "otro", juego={
                "horario": {"abre": "08:30", "cierra": "14:00", "fuera_de_horario": "no_jugar"},
                "separacion_min_entre_premios": 7})
            otro = cli.abrir_inventario(otro_cfg)
            self.assertEqual((otro.horario.abre, otro.horario.cierra, otro.horario.fuera_de_horario),
                             ("08:30", "14:00", "no_jugar"))
            self.assertEqual(otro.separacion_min_entre_premios, 7)
            # Sin las llaves, el motor queda como antes de la Fase 4d.
            vacio = cli.abrir_inventario(self.config_con(Path(tmp) / "sin"))
            self.assertIsNone(vacio.horario)
            self.assertEqual(vacio.separacion_min_entre_premios, 0.0)

    def test_el_config_json_de_produccion_llega_entero_al_motor(self):
        """Vector real: lo que el kiosco va a cargar en la Pi, sin retocar nada."""
        cfg = configmod.cargar(RAIZ / "config.json")
        with tempfile.TemporaryDirectory() as tmp:
            crudo = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
            crudo["carpeta_datos"] = tmp
            inventario = cli.abrir_inventario(configmod.desde_dict(crudo))
        self.assertEqual(
            (inventario.hora_inicio_dia, inventario.peso_consuelo,
             inventario.separacion_min_entre_premios, inventario.horario),
            (cfg.juego.hora_inicio_dia, cfg.juego.consuelo.peso,
             cfg.juego.separacion_min_entre_premios, cfg.juego.horario))
        self.assertEqual(sorted(inventario.premios), sorted(p.id for p in cfg.premios))

    def test_las_fechas_del_evento_deciden_que_dias_hay_premios(self):
        """D1 de la Fase 4e: el calendario del evento, con el motor de PRODUCCIÓN.

        Vector real: `config.json` tal cual, cableado por `abrir_inventario`, a
        las **20:10** de siete días distintos. Se ancla el censo de ids
        disponibles **por igualdad y en orden**, porque es la promesa que el §5.1
        del documento del evento y el §5 del README le hacen al personal:

        * **antes del lunes 21 no puede salir un solo premio** —toda jugada sale
          de consuelo, y eso NO es una avería—;
        * la **hielera** no existe hasta el **jueves 24**, aunque le sobre stock;
        * **después del viernes 25** tampoco queda nada.

        Sin las fechas cargadas, el lunes 21 saldrían los siete y la hielera —dos
        piezas, las más caras del evento— podría irse el primer día (ficha F-259).

        La hora cambió de las 19:00 a las 19:40 el 2026-09-22 por la mañana, y a
        las **20:10** esa misma tarde, con las horas por día del paso 2: a esa
        hora **los dos días de la hielera la tienen abierta** —el jueves desde
        las 19:36 y el viernes desde las 20:04—, que es lo que hace falta para
        que este censo distinga la FECHA de la franja y no la franja misma. A
        las 19:40 ya no valdría: el viernes la hielera todavía no ha abierto. Lo que estas fechas
        dejan fuera **de más** —`silla_extra` y `bbq_extra`, que solo existen el
        martes y el miércoles— lo ancla, con sus propias horas,
        `test_el_reparto_del_dia_2_abre_las_piezas_a_sus_horas`.
        """
        with tempfile.TemporaryDirectory() as tmp:
            crudo = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
            crudo["carpeta_datos"] = tmp
            inventario = cli.abrir_inventario(configmod.desde_dict(crudo))
            censo = {dia: [p.id for p in inventario.disponibles(datetime(2026, 9, dia, 20, 10))]
                     for dia in (19, 21, 22, 23, 24, 25, 26)}
        chicos = ["tacos3", "tacos2", "cerveza", "agua"]
        self.assertEqual(censo, {
            19: [],                                    # sábado: el evento no ha empezado
            21: chicos,                                # lunes: ya no tiene franjas de grandes
            22: ["silla"] + chicos,                    # martes: la silla de las 19:23
            23: ["silla"] + chicos,                    # miércoles: la de las 19:38
            24: ["hielera", "silla"] + chicos,         # jueves: se suma el premio mayor
            25: ["hielera", "silla"] + chicos,         # viernes: último día
            26: [],                                    # sábado: fecha vencida
        })
        # Y el motivo es la FECHA, no la franja ni el stock: si algún día alguien
        # mueve la franja de la hielera, este mensaje sigue diciendo la verdad.
        hielera = inventario.premios["hielera"]
        self.assertEqual(inventario.motivo_no_disponible(hielera, datetime(2026, 9, 21, 20, 10)),
                         "desde 24/09")
        self.assertEqual(inventario.motivo_no_disponible(hielera, datetime(2026, 9, 26, 20, 10)),
                         "fecha vencida")
        # El lunes 21 los grandes ya no tienen franja: sus horas viejas se fueron
        # con el paso 2 y el día está cerrado para ellos. Es lo correcto —el
        # lunes ya pasó— y se ancla para que nadie devuelva por error una franja
        # sin `dias`, que valdría los cinco días.
        self.assertEqual(
            {pid: inventario.motivo_no_disponible(inventario.premios[pid],
                                                  datetime(2026, 9, 21, 20, 10))
             for pid in ("silla", "bbq")},
            {"silla": "franjas de hoy cerradas", "bbq": "franjas de hoy cerradas"})


    def test_el_reparto_del_dia_2_abre_las_piezas_a_sus_horas(self):
        """Día 2 (2026-09-22): el reparto nuevo, con el estado REAL del lunes.

        Vector real doble: el `config.json` del repositorio cableado por
        `abrir_inventario`, y encima el `estado.json` **medido** al cerrar el
        lunes 21 —folio **55**, con 11 aguas, 8 cervezas, 4 y 3 tacos y **1 set
        BBQ** entregados, y **ninguna silla**—. Sobre eso se ancla **por
        igualdad y en orden** qué piezas tiene abiertas el reloj en los once
        instantes que decidieron este cambio. **Las horas son distintas cada
        día desde el paso 2 de esa tarde**, así que cada día trae las suyas:

        * **martes 13:20** la `silla` está abierta (13:17) y `silla_extra` **no**
          (abre a las 16:08): las dos sillas del martes NO salen a la vez;
        * **martes 16:10** sí está `silla_extra`, y además el `bbq` de las 14:41;
        * **martes 17:40** entra `bbq_extra` (17:34), el tercer set del martes,
          **con `silla_extra` todavía abierta**: son los dos forzados a la vez
          que anclan la ficha **F-283**;
        * **martes 19:25** ya está la silla de la noche (19:23) y sigue el
          `bbq_extra`; **martes 19:34** el `bbq_extra` cierra **en ese minuto**;
        * **martes 20:50** entra el `bbq` de la noche (20:47);
        * **martes 21:05** entra `silla_extra2` (21:00), la **cuarta silla del
          martes** que el usuario ordenó esa noche («eran 4»), forzada hasta el
          cierre y detrás de la silla y el set que ya estaban abiertos (ficha
          **F-288**);
        * **miércoles 13:12** la silla abre a las **13:09**, que es una hora que
          el martes no existe: es el instante que separa un día de otro;
        * **jueves 17:40** —la MISMA hora del martes a la que salen las dos
          entradas de reposición— no hay **ninguna de las dos**: el jueves están
          fuera de fechas (`silla_extra`, `silla_extra2` y `bbq_extra` acaban el 22);
        * **jueves 19:40** la hielera (19:36) y la silla del jueves (19:11), que
          el martes abría a las 19:23;
        * **jueves 22:52** el `bbq` de la noche cierra **en ese minuto** y la
          hielera se queda sola hasta el cierre;
        * **viernes 20:06** la hielera del viernes, que abre a las **20:04** y no
          a las 19:36: es el instante que ancla la hora por día del premio mayor.

        Y se ancla **por igualdad** la tómbola del peso 100 (decisión del usuario
        del 2026-09-22 por la mañana): con todo lo del martes abierto a la vez,
        cada premio grande se lleva **29.50 %** de las jugadas desde que a las
        21:00 se suma `silla_extra2` (eran **41.84 %** con dos). Esa tabla sigue
        siendo la de la tómbola, pero desde el paso 2 **ya no decide** cuando hay
        una pieza forzada abierta: entonces manda `forzados_abiertos`, y por eso
        se ancla también ahí (ficha **F-285**).
        """
        lunes = {
            "version": 1, "folio": 55,
            "entregados": {"agua": 11, "cerveza": 8, "tacos2": 3, "tacos3": 4, "bbq": 1},
            "por_dia": {"2026-09-21": {"agua": 11, "cerveza": 8, "tacos2": 3,
                                       "tacos3": 4, "bbq": 1}},
            "boletos_por_dia": {"2026-09-21": 54},
            "ultimo_premio": "2026-09-21T22:46:51",
        }
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "estado.json").write_text(json.dumps(lunes), encoding="utf-8")
            crudo = json.loads((RAIZ / "config.json").read_text(encoding="utf-8"))
            crudo["carpeta_datos"] = tmp
            inventario = cli.abrir_inventario(configmod.desde_dict(crudo))
            # El estado del lunes se cargó de verdad: si no, el censo de abajo
            # saldría igual por casualidad y no probaría nada.
            self.assertEqual((inventario.folio_actual, inventario.entregados("bbq"),
                              inventario.entregados("silla")), (55, 1, 0))
            instantes = ((22, 13, 20), (22, 16, 10), (22, 17, 40), (22, 19, 25),
                         (22, 19, 34), (22, 20, 50), (22, 21, 5), (23, 13, 12), (24, 17, 40),
                         (24, 19, 40), (24, 22, 52), (25, 20, 6))
            abierto = {
                f"{d}-{h:02d}:{mi:02d}":
                    [p.id for p in inventario.disponibles(datetime(2026, 9, d, h, mi))]
                for d, h, mi in instantes}
            forzado = {
                f"{d}-{h:02d}:{mi:02d}":
                    [p.id for p in inventario.forzados_abiertos(datetime(2026, 9, d, h, mi))]
                for d, h, mi in instantes}
            martes_noche = datetime(2026, 9, 22, 21, 0)
            probabilidades = {p: round(v, 2)
                              for p, v in inventario.probabilidades(martes_noche).items()}
            probabilidades["consuelo"] = round(
                inventario.probabilidad_consuelo(martes_noche), 2)
            manda_el_forzado = inventario.sortear(martes_noche)
        self.assertEqual(abierto, {
            "22-13:20": ["silla", "cerveza", "agua"],
            "22-16:10": ["silla_extra", "bbq", "tacos3", "tacos2", "cerveza", "agua"],
            "22-17:40": ["silla_extra", "bbq_extra", "tacos3", "tacos2", "cerveza", "agua"],
            "22-19:25": ["silla", "bbq_extra", "tacos3", "tacos2", "cerveza", "agua"],
            "22-19:34": ["silla", "tacos3", "tacos2", "cerveza", "agua"],
            "22-20:50": ["silla", "bbq", "tacos3", "tacos2", "cerveza", "agua"],
            "22-21:05": ["silla", "silla_extra2", "bbq", "tacos3", "tacos2", "cerveza", "agua"],
            "23-13:12": ["silla", "cerveza", "agua"],
            "24-17:40": ["tacos3", "tacos2", "cerveza", "agua"],
            "24-19:40": ["hielera", "silla", "tacos3", "tacos2", "cerveza", "agua"],
            "24-22:52": ["hielera", "tacos3", "tacos2", "cerveza", "agua"],
            "25-20:06": ["hielera", "silla", "tacos3", "tacos2", "cerveza", "agua"],
        })
        # Y de esas piezas, cuáles se entregan SIN sorteo y en qué orden: primero
        # la que lleva más tiempo abierta. Es el censo del campo `forzado`.
        self.assertEqual(forzado, {
            "22-13:20": ["silla"],
            "22-16:10": ["bbq", "silla_extra"],
            "22-17:40": ["silla_extra", "bbq_extra"],
            "22-19:25": ["bbq_extra", "silla"],
            "22-19:34": ["silla"],
            "22-20:50": ["silla", "bbq"],
            "22-21:05": ["silla", "bbq", "silla_extra2"],
            "23-13:12": ["silla"],
            "24-17:40": [],
            "24-19:40": ["silla", "hielera"],
            "24-22:52": ["hielera"],
            "25-20:06": ["silla", "hielera"],
        })
        self.assertEqual(probabilidades, {
            "silla": 29.5, "silla_extra2": 29.5, "bbq": 29.5, "tacos3": 1.18,
            "tacos2": 1.18, "cerveza": 2.95, "agua": 3.24, "consuelo": 2.95,
        })
        # …y aun con esas probabilidades, el martes a las 21:00 la jugada se
        # lleva la silla seguro: hay tres piezas forzadas abiertas y manda la
        # primera. La tabla de arriba describe la tómbola, no el resultado.
        self.assertEqual(manda_el_forzado.id, "silla")

    def test_abrir_inventario_pasa_el_peso_del_consuelo(self):
        with tempfile.TemporaryDirectory() as tmp:
            for i, peso in enumerate((0, 217, 42)):
                with self.subTest(peso=peso):
                    cfg = self.config_con(Path(tmp) / f"d{i}", peso)
                    self.assertEqual(cli.abrir_inventario(cfg).peso_consuelo, peso)
            # Y sin la llave en el archivo, el motor queda como antes de la Fase 4c.
            cfg = self.config_con(Path(tmp) / "sin", None)
            inventario = cli.abrir_inventario(cfg)
            self.assertEqual(inventario.peso_consuelo, 0)
            self.assertEqual(inventario.hora_inicio_dia, cfg.juego.hora_inicio_dia)

    def test_solo_hay_un_sitio_de_produccion_que_construye_el_inventario(self):
        """Censo DERIVADO del paquete, no una lista escrita a mano."""
        sitios = {}
        for modulo in sorted((RAIZ / "ruleta").glob("*.py")):
            cuantos = len(re.findall(r"\bInventario\(", modulo.read_text(encoding="utf-8")))
            if cuantos:
                sitios[modulo.name] = cuantos
        self.assertEqual(
            sitios, {"__main__.py": 1},
            "Apareció otro sitio en ruleta/ que construye un Inventario. Si es legítimo, "
            "compruébalo: tiene que pasar hora_inicio_dia, juego.consuelo.peso, juego.horario y "
            "juego.separacion_min_entre_premios, como hace abrir_inventario. Después actualiza "
            "este censo.")


class TestVersionModulo(unittest.TestCase):
    @staticmethod
    def sin_metadatos(nombre):
        raise metadata.PackageNotFoundError(nombre)

    def test_version_de_los_metadatos(self):
        self.assertEqual(cli.version_modulo("gpiozero", None, version_fn=lambda n: "2.0.1"), "2.0.1")

    def test_cae_al_dunder_version_del_modulo(self):
        modulo = SimpleNamespace(__version__="11.1.0")
        self.assertEqual(cli.version_modulo("PIL", modulo, version_fn=self.sin_metadatos), "11.1.0")

    def test_metadatos_vacios_no_ganan_al_modulo(self):
        modulo = SimpleNamespace(__version__="0.2.2.0")
        self.assertEqual(cli.version_modulo("lgpio", modulo, version_fn=lambda n: ""), "0.2.2.0")

    def test_sin_version_por_ningun_lado_dice_instalado(self):
        # Es el caso medido de gpiozero y lgpio antes de este cambio: salían en blanco.
        self.assertEqual(cli.version_modulo("lgpio", object(), version_fn=self.sin_metadatos), "instalado")

    def test_pil_de_esta_maquina_trae_numero(self):
        # Vector real: PIL no tiene distribución llamada 'PIL', así que solo pasa
        # si el respaldo por __version__ sigue en su sitio.
        self.assertEqual(cli.version_modulo("PIL", PIL), PIL.__version__)


class TestInterpretarEstadoPapel(unittest.TestCase):
    """Los tres bytes son (DLE EOT 4, DLE EOT 2, DLE EOT 1), como los devuelve
    `ImpresoraArchivo.consultar_papel()`. Vectores medidos en la AOMU My-A1 el
    2026-09-15: con papel contesta (0x12, 0x12, 0x16) y sin papel, con la tapa
    cerrada, lo único que cambia es el de en medio, que pasa a 0x32."""

    def test_con_papel_y_en_linea(self):
        self.assertEqual(cli.interpretar_estado_papel(0x12, 0x12, 0x16),
                         (True, "  [ok] la impresora contesta: hay papel y está en línea"))

    def test_sin_papel(self):
        self.assertEqual(cli.interpretar_estado_papel(0x72, 0x12, 0x16),
                         (False, "  [!!] la impresora reporta SIN PAPEL: pon un rollo nuevo"))

    def test_sin_papel_por_la_causa_de_fuera_de_linea(self):
        # El vector real del rollo agotado: DLE EOT 4 y DLE EOT 1 siguen sanos y
        # el único que se entera es DLE EOT 2 con su bit 5.
        self.assertEqual(cli.interpretar_estado_papel(0x12, 0x32, 0x16),
                         (False, "  [!!] la impresora reporta SIN PAPEL: pon un rollo nuevo"))

    def test_sin_papel_gana_a_poco_papel(self):
        # 0x7e trae los bits 5-6 Y la pareja 2-3 encendidos: un rollo agotado no
        # es un rollo por acabarse. El ORDEN de las ramas es lo que se ancla.
        self.assertEqual(cli.interpretar_estado_papel(0x7e, 0x12, 0x16),
                         (False, "  [!!] la impresora reporta SIN PAPEL: pon un rollo nuevo"))

    def test_tapa_abierta(self):
        self.assertEqual(cli.interpretar_estado_papel(0x12, 0x16, 0x16),
                         (False, "  [!!] la impresora tiene la tapa abierta: ciérrala bien"))

    def test_error_de_impresora(self):
        self.assertEqual(
            cli.interpretar_estado_papel(0x12, 0x52, 0x16),
            (False, "  [!!] la impresora reporta un error: revisa el papel, la tapa y la cuchilla"))

    def test_fuera_de_linea(self):
        self.assertEqual(
            cli.interpretar_estado_papel(0x12, 0x12, 0x1a),
            (False, "  [!!] la impresora está fuera de línea: tapa abierta, sin papel o con error"))

    def test_poco_papel_avisa_sin_ser_error(self):
        # Estrena vector: 0x1e tiene la pareja 2-3 entera. El de antes era 0x16,
        # que consagraba la lectura equivocada (ver la prueba de abajo).
        self.assertEqual(cli.interpretar_estado_papel(0x1e, 0x12, 0x16),
                         (True, "  [??] la impresora reporta poco papel: ten listo el rollo de repuesto"))

    def test_el_byte_medido_0x16_no_es_poco_papel(self):
        # 0x16 es la respuesta SANA de DLE EOT 1 (bit 2 = pin 3 del cajón). Con
        # la máscara suelta de antes salía un aviso de poco papel que no existía:
        # 15 veces en el log del kiosco desde el 2026-09-11.
        self.assertEqual(cli.interpretar_estado_papel(0x16, 0x12, 0x16),
                         (True, "  [ok] la impresora contesta: hay papel y está en línea"))

    def test_no_contesta_no_es_falla(self):
        self.assertEqual(
            cli.interpretar_estado_papel(None, None, None),
            (True, "  [??] la impresora no contestó a la consulta de estado; se imprimirá igual "
                   "(no todos los firmwares contestan)"))


if __name__ == "__main__":
    unittest.main()
