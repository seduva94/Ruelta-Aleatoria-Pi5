"""Punto de entrada: `python3 -m ruleta [opciones] [comando]`.

Sin comando arranca la ruleta (modo kiosco). Comandos adicionales:

  probar-impresora   imprime un boleto de diagnóstico (acentos, tamaños, logo, corte)
  vista-previa       muestra en consola cómo se verán los boletos, sin hardware
  reporte            muestra (y opcionalmente imprime) el inventario actual
  liberar FOLIO      devuelve al inventario el premio de un boleto que no salió
  reiniciar          pone folio y contadores en cero para un evento nuevo
  diagnostico        revisa dependencias, emparejamiento y conexión con la impresora

Opciones globales útiles:
  --config RUTA          otro archivo de configuración
  --impresora TIPO       fuerza bluetooth | archivo | vista (vista = consola)
  --simular              botones por teclado en lugar de GPIO
"""

from __future__ import annotations

import argparse
import logging
import os
import shutil
import signal
import stat
import subprocess
import sys
from datetime import datetime
from importlib import metadata
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Callable

from . import __version__, config as configmod, escpos, ticket
from .app import Ruleta, crear_impresora
from .config import Config, ErrorConfig
from .escpos import ErrorImpresora, ImpresoraVista, soporte_bluetooth
from .hardware import EntradasGPIO, EntradasSimuladas, teclado_simulado
from .inventario import Boleto, ErrorBloqueo, ErrorPersistencia, Inventario

RAIZ = Path(__file__).resolve().parent.parent
CONFIG_DEFECTO = RAIZ / "config.json"

log = logging.getLogger("ruleta")


# --------------------------------------------------------------------------- #
# Infraestructura
# --------------------------------------------------------------------------- #

def configurar_logging(carpeta: Path, verboso: bool) -> None:
    nivel = logging.DEBUG if verboso else logging.INFO
    formato = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    raiz = logging.getLogger()
    raiz.setLevel(nivel)
    for h in list(raiz.handlers):
        raiz.removeHandler(h)
    consola = logging.StreamHandler(sys.stdout)
    consola.setFormatter(formato)
    raiz.addHandler(consola)
    try:
        carpeta.mkdir(parents=True, exist_ok=True)
        archivo = RotatingFileHandler(carpeta / "ruleta.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        archivo.setFormatter(formato)
        raiz.addHandler(archivo)
    except OSError as e:
        log.warning("No se pudo abrir el archivo de log en %s: %s", carpeta, e)


def cargar_config(args) -> Config:
    try:
        return configmod.cargar(args.config)
    except ErrorConfig as e:
        print(f"ERROR de configuración: {e}", file=sys.stderr)
        sys.exit(2)


def abrir_inventario(cfg: Config, exclusivo: bool = False) -> Inventario:
    """Abre el inventario; con exclusivo=True toma el candado (falla si el servicio corre).

    Es el ÚNICO sitio de producción que construye un `Inventario`: todo lo que el
    motor necesita de `config.json` —la hora en que cambia el día, el peso del
    consuelo y, desde la Fase 4d, el horario del evento y la separación mínima
    entre premios— se cablea aquí y en ningún otro lado.
    """
    inv = Inventario(cfg.premios, cfg.carpeta_datos, hora_inicio_dia=cfg.juego.hora_inicio_dia,
                     peso_consuelo=cfg.juego.consuelo.peso, horario=cfg.juego.horario,
                     separacion_min_entre_premios=cfg.juego.separacion_min_entre_premios)
    if exclusivo:
        try:
            inv.bloquear()
        except ErrorBloqueo as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    return inv


def servicio_activo() -> bool:
    """True si systemd reporta el servicio 'ruleta' corriendo (False si no hay systemd)."""
    if not shutil.which("systemctl"):
        return False
    try:
        return subprocess.run(["systemctl", "is-active", "--quiet", "ruleta"], timeout=10).returncode == 0
    except (subprocess.SubprocessError, OSError):
        return False


def impresora_desde_args(cfg: Config, args):
    tipo = getattr(args, "impresora", None)
    try:
        return crear_impresora(cfg, tipo)
    except ErrorConfig as e:
        print(f"ERROR de configuración: {e}", file=sys.stderr)
        sys.exit(2)


def _confirmar(pregunta: str, saltar: bool) -> bool:
    if saltar:
        return True
    respuesta = input(pregunta + " [s/N] ")
    return respuesta.strip().lower() in ("s", "si", "sí")


# --------------------------------------------------------------------------- #
# Comandos
# --------------------------------------------------------------------------- #

def cmd_jugar(cfg: Config, args) -> int:
    impresora = impresora_desde_args(cfg, args)
    inventario = abrir_inventario(cfg, exclusivo=True)

    if args.simular:
        entradas = EntradasSimuladas(salida=lambda s: print(s, flush=True),
                                     habilitar_inicial=(cfg.gpio.modo_habilitar == "siempre"))
    else:
        entradas = EntradasGPIO(cfg.gpio.boton_jugar, cfg.gpio.boton_habilitar, cfg.gpio.led,
                                pull_up=cfg.gpio.pull_up)

    ruleta = Ruleta(cfg, inventario, impresora, entradas)

    def terminar(*_):
        log.info("Señal de apagado recibida; cerrando.")
        ruleta.detener()

    signal.signal(signal.SIGTERM, terminar)
    signal.signal(signal.SIGINT, terminar)

    if args.simular:
        teclado_simulado(entradas, ruleta.detener, cfg.gpio.pulsacion_larga_seg)
        if cfg.gpio.modo_habilitar == "mantener":
            print("Recuerda: presiona 'h' + Enter para simular el botón HABILITAR antes de 'j'.", flush=True)

    log.info("Ruleta v%s | impresora=%s | datos=%s", __version__, impresora.nombre, cfg.carpeta_datos)
    try:
        ruleta.arrancar()
        ruleta.correr()
    finally:
        ruleta.cerrar()
        inventario.desbloquear()
    log.info("Ruleta detenida. Boletos impresos en esta sesión: %d", ruleta.boletos_impresos)
    return 0


def cmd_probar_impresora(cfg: Config, args) -> int:
    impresora = impresora_desde_args(cfg, args)
    try:
        tablas = tuple(int(x) for x in args.tablas.split(",")) if args.tablas else (0, 2, 16, 19)
        if any(not 0 <= t <= 255 for t in tablas):
            raise ValueError("fuera de rango")
    except ValueError:
        print("--tablas debe ser una lista de números entre 0 y 255 separados por coma, p. ej. 0,2,16,19",
              file=sys.stderr)
        return 2
    datos = ticket.boleto_prueba(cfg, tablas)
    print(f"Enviando boleto de prueba ({len(datos)} bytes) por {impresora.nombre}...")
    try:
        impresora.imprimir(datos)
    except ErrorImpresora as e:
        print(f"FALLÓ: {e}", file=sys.stderr)
        return 1
    print("Listo. Revisa qué línea de acentos salió bien y pon ese número en impresora.codepage_n.")
    return 0


def cmd_vista_previa(cfg: Config, args) -> int:
    vista = ImpresoraVista(codepage=cfg.impresora.codepage, chars_por_linea=cfg.impresora.chars_por_linea)
    inventario = abrir_inventario(cfg)
    ahora = datetime.now()
    folio = inventario.folio_actual + 1
    premios = cfg.premios
    if args.premio:
        premios = [p for p in cfg.premios if p.id == args.premio]
        if not premios:
            print(f"No existe el premio '{args.premio}'. Ids: {[p.id for p in cfg.premios]}", file=sys.stderr)
            return 2
    elif not args.todos:
        premios = premios[:1]
    for p in premios:
        boleto = Boleto(folio=folio, premio=p, momento=ahora, dia=inventario.dia_operativo(ahora))
        print(f"\n=== Boleto de premio: {p.id} ===")
        vista.imprimir(ticket.boleto_premio(cfg, boleto))
    consuelo = Boleto(folio=folio, premio=None, momento=ahora, dia=inventario.dia_operativo(ahora))
    print("\n=== Boleto de consuelo (la jugada no dio premio) ===")
    vista.imprimir(ticket.boleto_consuelo(cfg, consuelo))
    print("\n=== Reporte de inventario ===")
    vista.imprimir(ticket.boleto_inventario(cfg, inventario.resumen(ahora), "vista previa"))
    return 0


def cmd_reporte(cfg: Config, args) -> int:
    inventario = abrir_inventario(cfg)
    ahora = datetime.now()
    resumen = inventario.resumen(ahora)
    datos = ticket.boleto_inventario(cfg, resumen, "reporte")
    ImpresoraVista(codepage=cfg.impresora.codepage, chars_por_linea=cfg.impresora.chars_por_linea).imprimir(datos)
    print(f"\nBitácora de boletos: {inventario.ruta_log}")
    print(f"Estado: {inventario.ruta_estado}")
    if resumen.pendientes:
        print(f"Boletos sin confirmar: {', '.join(p.folio_texto for p in resumen.pendientes)} "
              f"(si alguno no salió: python3 -m ruleta liberar FOLIO)")
    if args.imprimir:
        if servicio_activo():
            print("El servicio 'ruleta' está corriendo y la impresora acepta una sola conexión: "
                  "usa el gesto del botón HABILITAR o detén el servicio primero.", file=sys.stderr)
            return 1
        impresora = impresora_desde_args(cfg, args)
        try:
            impresora.imprimir(datos)
            print("Reporte enviado a la impresora.")
        except ErrorImpresora as e:
            print(f"No se pudo imprimir: {e}", file=sys.stderr)
            return 1
    return 0


def cmd_liberar(cfg: Config, args) -> int:
    """Devuelve al inventario el premio de un boleto que el personal comprobó que no salió."""
    if servicio_activo():
        print("Detén el servicio primero (sudo systemctl stop ruleta); si no, el cambio se perdería "
              "en la siguiente jugada. Vuelve a arrancarlo al terminar.", file=sys.stderr)
        return 1
    inventario = abrir_inventario(cfg, exclusivo=True)
    try:
        pendientes = inventario.pendientes()
        if args.folio is None:
            if not pendientes:
                print("No hay boletos sin confirmar.")
                return 0
            print("Boletos sin confirmar (último evento 'emitido' o 'incierto'):")
            for p in pendientes:
                print(f"  {p.folio_texto}  {p.fecha_hora}  {p.evento:<8}  {p.premio_nombre}")
            print("Para devolver un premio: python3 -m ruleta liberar FOLIO")
            return 0
        folio = args.folio
        fila = next((p for p in pendientes if p.folio == folio), None)
        if fila is None:
            print(f"El folio {folio:05d} no está pendiente. Pendientes: "
                  f"{', '.join(p.folio_texto for p in pendientes) or 'ninguno'}", file=sys.stderr)
            return 1
        print(f"Boleto {fila.folio_texto} · {fila.fecha_hora} · {fila.evento} · {fila.premio_nombre}")
        if not _confirmar("¿Confirmas que este boleto NO salió impreso y el premio debe regresar al inventario?",
                          args.si):
            print("Cancelado.")
            return 1
        try:
            inventario.liberar(folio)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print(f"Listo: el premio '{fila.premio_nombre}' volvió al inventario (folio {fila.folio_texto} liberado).")
        return 0
    finally:
        inventario.desbloquear()


def cmd_reiniciar(cfg: Config, args) -> int:
    if servicio_activo():
        print("El servicio 'ruleta' está corriendo: deténlo primero con  sudo systemctl stop ruleta  "
              "y vuelve a arrancarlo al terminar (sudo systemctl start ruleta).", file=sys.stderr)
        return 1
    inventario = abrir_inventario(cfg, exclusivo=True)
    try:
        resumen = inventario.resumen(datetime.now())
        entregados = sum(f.entregados for f in resumen.premios)
        print(f"Folio actual: {resumen.folio_actual:05d}. Premios entregados registrados: {entregados}.")
        if not _confirmar("¿Poner TODO en cero para un evento nuevo? Se respaldan los archivos actuales.", args.si):
            print("Cancelado.")
            return 1
        marca = datetime.now().strftime("%Y%m%d_%H%M%S")
        for ruta in (inventario.ruta_estado, inventario.ruta_log):
            if ruta.exists():
                respaldo = ruta.with_name(f"{ruta.stem}_{marca}{ruta.suffix}")
                shutil.copy2(ruta, respaldo)
                print(f"Respaldo: {respaldo}")
        try:
            inventario.reiniciar()
        except ErrorPersistencia as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        if inventario.ruta_log.exists():
            os.remove(inventario.ruta_log)
        print("Inventario reiniciado. Folio en 00000.")
        return 0
    finally:
        inventario.desbloquear()


# --------------------------------------------------------------------------- #
# Revisiones del diagnóstico (funciones puras, para poder probarlas)
# --------------------------------------------------------------------------- #

def version_modulo(nombre: str, modulo=None,
                   version_fn: Callable[[str], str] = metadata.version) -> str:
    """Versión instalada de una librería, para el diagnóstico.

    `gpiozero` y `lgpio` NO exponen `__version__` (salían en blanco), así que se
    pregunta primero a los metadatos de la distribución —que sirven igual si la
    instaló apt o pip— y solo después al módulo. Si no hay ni una cosa ni la
    otra, se dice «instalado», que es lo único que se sabe con certeza.
    """
    try:
        version = version_fn(nombre)
    except Exception:       # PackageNotFoundError y cualquier rareza de los metadatos
        version = ""
    if not version:
        version = str(getattr(modulo, "__version__", "") or "")
    return version or "instalado"


def revisar_ruta_impresora(ruta: str, stat_fn: Callable = os.stat,
                           access_fn: Callable = os.access) -> tuple[bool, str]:
    """Revisa la `ruta` de impresora.tipo='archivo': (¿todo bien?, línea del diagnóstico)."""
    try:
        modo = stat_fn(ruta).st_mode
    except OSError as e:
        return False, (f"  [!!] no existe la ruta de la impresora: {ruta} ({e.strerror}). "
                       "Revisa el cable USB y que la impresora esté encendida; el nombre "
                       "/dev/ruleta-impresora lo crea la regla udev que pone instalar.sh")
    escribible = bool(access_fn(ruta, os.W_OK))
    if stat.S_ISCHR(modo):
        if escribible:
            return True, f"  [ok] impresora conectada en {ruta} (dispositivo, se puede escribir)"
        return False, (f"  [!!] sin permiso para escribir en {ruta}: falta la regla udev "
                       "/etc/udev/rules.d/61-ruleta-impresora-usb.rules o el usuario no está en el "
                       "grupo lp (sudo usermod -aG lp $USER y vuelve a entrar)")
    if stat.S_ISREG(modo):
        if escribible:
            return True, (f"  [??] {ruta} es un archivo normal, no la impresora: sirve para pruebas, "
                          "pero no va a salir papel")
        return False, f"  [!!] no se puede escribir en el archivo {ruta}"
    return False, f"  [!!] {ruta} no es un dispositivo ni un archivo normal: revisa impresora.ruta"


def interpretar_estado_papel(papel: int | None, causa: int | None,
                             estado: int | None) -> tuple[bool, str]:
    """Traduce las tres respuestas DLE EOT de la impresora a una línea del diagnóstico.

    `papel` es DLE EOT 4, `causa` es DLE EOT 2 y `estado` es DLE EOT 1, tal y
    como los devuelve `ImpresoraArchivo.consultar_papel()`. El ORDEN de las
    ramas manda: «sin papel» se decide antes que «poco papel», porque un byte
    con los bits 5-6 y los 2-3 encendidos a la vez es un rollo agotado, no un
    rollo por acabarse. Cada condición se evalúa solo si su byte llegó.
    """
    if papel is None and causa is None and estado is None:
        return True, ("  [??] la impresora no contestó a la consulta de estado; se imprimirá igual "
                      "(no todos los firmwares contestan)")
    if ((papel is not None and papel & escpos.BITS_SIN_PAPEL)
            or (causa is not None and causa & escpos.BIT_FIN_DE_PAPEL)):
        return False, "  [!!] la impresora reporta SIN PAPEL: pon un rollo nuevo"
    if causa is not None and causa & escpos.BIT_TAPA_ABIERTA:
        return False, "  [!!] la impresora tiene la tapa abierta: ciérrala bien"
    if causa is not None and causa & escpos.BIT_ERROR_IMPRESORA:
        return False, "  [!!] la impresora reporta un error: revisa el papel, la tapa y la cuchilla"
    if estado is not None and estado & escpos.BIT_FUERA_DE_LINEA:
        return False, "  [!!] la impresora está fuera de línea: tapa abierta, sin papel o con error"
    if papel is not None and (papel & escpos.BITS_POCO_PAPEL) == escpos.BITS_POCO_PAPEL:
        return True, "  [??] la impresora reporta poco papel: ten listo el rollo de repuesto"
    return True, "  [ok] la impresora contesta: hay papel y está en línea"


def cmd_diagnostico(cfg: Config, args) -> int:
    """Revisa dependencias, GPIO, Bluetooth y la impresora; sugiere correcciones."""
    ok = True
    en_linux = sys.platform.startswith("linux")
    print(f"Ruleta v{__version__} | Python {sys.version.split()[0]} | {sys.platform}")
    print(f"Configuración: {args.config}")
    print(f"Carpeta de datos: {cfg.carpeta_datos}")

    try:
        cfg.carpeta_datos.mkdir(parents=True, exist_ok=True)
        prueba = cfg.carpeta_datos / ".prueba_escritura"
        prueba.write_text("ok", encoding="utf-8")
        prueba.unlink()
        print("  [ok] la carpeta de datos se puede escribir")
    except OSError as e:
        ok = False
        print(f"  [!!] no se puede escribir en la carpeta de datos: {e}")

    for modulo, paquete in (("PIL", "python3-pil"), ("gpiozero", "python3-gpiozero"), ("lgpio", "python3-lgpio")):
        try:
            m = __import__(modulo)
            print(f"  [ok] {modulo} {version_modulo(modulo, m)}")
        except ImportError:
            if modulo == "PIL" or en_linux:
                ok = False
                print(f"  [!!] falta {modulo}: sudo apt install {paquete}")
            else:
                print(f"  [--] {modulo} no está (solo hace falta en la Raspberry)")

    logo = cfg.ruta_logo()
    if logo is None:
        print("  [--] sin logo configurado")
    elif logo.exists():
        print(f"  [ok] logo: {logo}")
    else:
        print(f"  [!!] el logo no existe: {logo} (el boleto saldrá sin logo)")

    try:
        inventario = abrir_inventario(cfg)
        pendientes = inventario.pendientes()
        print(f"  [ok] inventario: folio {inventario.folio_actual:05d}"
              + (f", {len(pendientes)} boleto(s) sin confirmar (python3 -m ruleta liberar)" if pendientes else ""))
    except Exception as e:  # pragma: no cover
        ok = False
        print(f"  [!!] no se pudo abrir el inventario: {e}")

    if cfg.impresora.tipo == "archivo":
        # Camino USB: la impresora es un dispositivo del sistema. Lo que puede
        # fallar de verdad es que la ruta no exista (cable suelto, impresora
        # apagada) o que no se pueda escribir (regla udev o grupo lp).
        bien, linea = revisar_ruta_impresora(cfg.impresora.ruta)
        print(linea)
        ok = ok and bien
        if bien and escpos.es_dispositivo_caracteres(cfg.impresora.ruta):
            if not cfg.impresora.consultar_estado:
                print("  [--] consultar_estado está en false: no se le pregunta a la impresora "
                      "si tiene papel (ni aquí ni antes de cada boleto)")
            elif servicio_activo():
                print("  [--] el servicio 'ruleta' está corriendo; no se consulta el estado de la impresora "
                      "para no interferir (deténlo con sudo systemctl stop ruleta si quieres consultarlo)")
            else:
                try:
                    papel, causa, estado = escpos.ImpresoraArchivo(cfg.impresora.ruta).consultar_papel()
                except ErrorImpresora as e:
                    bien, linea = False, f"  [!!] no se pudo consultar el estado de la impresora: {e}"
                else:
                    bien, linea = interpretar_estado_papel(papel, causa, estado)
                print(linea)
                ok = ok and bien
        return 0 if ok else 1

    if cfg.impresora.tipo != "bluetooth":
        print(f"  [--] impresora tipo '{cfg.impresora.tipo}': los boletos salen por la consola, "
              "no hay impresora que probar")
        return 0 if ok else 1

    if not soporte_bluetooth():
        print("  [!!] este Python no tiene soporte Bluetooth (socket.AF_BLUETOOTH): solo funciona en Linux")
        return 1

    mac = cfg.impresora.mac
    try:
        impresora = crear_impresora(cfg)
    except ErrorConfig as e:
        print(f"  [!!] {e}")
        return 1

    if shutil.which("bluetoothctl"):
        try:
            r = subprocess.run(["bluetoothctl", "info", mac], capture_output=True, text=True, timeout=20)
            salida = r.stdout + r.stderr
            for linea in salida.splitlines():
                if any(k in linea for k in ("Name", "Paired", "Trusted", "Connected", "Serial Port", "not available")):
                    print("     ", linea.strip())
            if "Paired: yes" not in salida:
                print(f"  [!!] la impresora {mac} no está emparejada: corre herramientas/emparejar.sh")
                ok = False
            elif "Trusted: yes" not in salida:
                print(f"  [!!] la impresora no está marcada como confiable: bluetoothctl trust {mac}")
            if "Serial Port" not in salida and "Paired: yes" in salida:
                print("  [??] no anuncia el perfil 'Serial Port' (SPP); si la conexión falla, la impresora podría ser solo BLE")
        except (subprocess.SubprocessError, OSError) as e:
            print(f"  [??] no se pudo consultar bluetoothctl: {e}")

    if servicio_activo():
        print("  [--] el servicio 'ruleta' está corriendo; no se prueba la conexión para no interferir "
              "(deténlo con sudo systemctl stop ruleta si quieres probarla)")
        return 0 if ok else 1

    print(f"Probando conexión RFCOMM a {mac} canal {cfg.impresora.canal}...")
    try:
        impresora.probar()
        print("  [ok] la impresora acepta conexiones")
    except ErrorImpresora as e:
        ok = False
        print(f"  [!!] {e}")
        print("  Buscando en qué canal RFCOMM escucha (1-30)...")
        try:
            canal = impresora.buscar_canal()
        except ErrorImpresora as e2:
            print(f"  [!!] no se pudo buscar: {e2}")
        else:
            if canal is None:
                print("  [!!] ningún canal aceptó la conexión: revisa que esté encendida y emparejada")
            else:
                print(f"  [ok] la impresora escucha en el canal {canal}: pon \"canal\": {canal} en config.json")
    return 0 if ok else 1


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python3 -m ruleta", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", default=str(CONFIG_DEFECTO), help=f"ruta de config.json (defecto: {CONFIG_DEFECTO})")
    p.add_argument("--impresora", choices=("bluetooth", "archivo", "vista"), default=None,
                   help="fuerza el tipo de impresora (vista = mostrar en consola)")
    p.add_argument("--simular", action="store_true", help="botones por teclado en vez de GPIO")
    p.add_argument("-v", "--verboso", action="store_true", help="log detallado")
    p.add_argument("--version", action="version", version=f"ruleta {__version__}")

    sub = p.add_subparsers(dest="comando")
    sub.add_parser("jugar", help="arranca la ruleta (es el comando por defecto)")

    pp = sub.add_parser("probar-impresora", help="imprime un boleto de diagnóstico")
    pp.add_argument("--tablas", default=None,
                    help="números ESC t a probar, separados por coma (defecto: 0,2,16,19)")

    pv = sub.add_parser("vista-previa", help="muestra los boletos en consola sin hardware")
    pv.add_argument("--premio", default=None, help="id del premio a mostrar")
    pv.add_argument("--todos", action="store_true", help="muestra un boleto por cada premio")

    pr = sub.add_parser("reporte", help="muestra el inventario; --imprimir lo manda a la impresora")
    pr.add_argument("--imprimir", action="store_true")

    pl = sub.add_parser("liberar", help="devuelve al inventario el premio de un boleto que no salió")
    pl.add_argument("folio", nargs="?", type=int, default=None, help="número de boleto (sin él, lista los pendientes)")
    pl.add_argument("--si", action="store_true", help="no pedir confirmación")

    pz = sub.add_parser("reiniciar", help="pone folio y contadores en cero (respalda los archivos)")
    pz.add_argument("--si", action="store_true", help="no pedir confirmación")

    sub.add_parser("diagnostico", help="revisa dependencias, emparejamiento y conexión con la impresora")
    return p


def main(argv: list[str] | None = None) -> int:
    for flujo in (sys.stdout, sys.stderr):
        # En consolas Windows la codificación por defecto no es UTF-8 y los acentos salen mal.
        if hasattr(flujo, "reconfigure"):
            try:
                flujo.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass
    parser = construir_parser()
    args = parser.parse_args(argv)
    cfg = cargar_config(args)
    configurar_logging(cfg.carpeta_datos, args.verboso)

    comandos = {
        None: cmd_jugar,
        "jugar": cmd_jugar,
        "probar-impresora": cmd_probar_impresora,
        "vista-previa": cmd_vista_previa,
        "reporte": cmd_reporte,
        "liberar": cmd_liberar,
        "reiniciar": cmd_reiniciar,
        "diagnostico": cmd_diagnostico,
    }
    try:
        return comandos[args.comando](cfg, args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
