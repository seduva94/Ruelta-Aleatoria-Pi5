"""Ciclo principal de la ruleta.

Máquina de estados que se ejecuta por sondeo (~100 veces por segundo):

  * El botón HABILITAR debe estar presionado (modo 'mantener') en el momento
    en que el cliente presiona JUGAR; si no, la pulsación se ignora.
  * Al soltar JUGAR se sortea e imprime un boleto (corta o larga, da igual:
    el botón del cliente solo sirve para jugar).
  * Tras cada boleto hay una espera (espera_entre_jugadas_seg) en la que se
    ignoran pulsaciones; además hay que soltar el botón antes de jugar de nuevo.
  * Fuera del horario del evento (juego.horario, Fase 4d) la jugada sale de
    consuelo; con "fuera_de_horario": "no_jugar" no se imprime nada y solo
    avisa el LED.
  * Si hay una pieza de un premio FORZADO abierta (día 2 paso 2, 2026-09-22),
    la jugada se la lleva sin sorteo y se anota en el registro.
  * Al arrancar, y solo al arrancar, se espera hasta juego.espera_hora_seg a
    que la hora del sistema esté sincronizada: el reparto por horas depende
    del reloj y la Pi no tiene batería RTC.
  * Gesto del personal: mantener HABILITAR presionado pulsacion_larga_seg
    segundos SIN que nadie toque JUGAR imprime el reporte de inventario.
    Si durante ese tiempo alguien juega, el gesto se cancela.

LED: apagado = no habilitado · fijo = listo · parpadeo lento = imprimiendo ·
parpadeo rápido = error (durante unos segundos).

Nada de lo que pase en una jugada debe tirar el ciclo: cualquier excepción se
registra, se enciende el LED de error y se sigue esperando pulsaciones.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Callable

from . import escpos, ticket
from .config import Config, ErrorConfig
from .escpos import ErrorConexion, ErrorEnvio, ErrorImpresora, Impresora
from .hardware import Antirrebote, Entradas
from .inventario import ErrorPersistencia, Inventario

log = logging.getLogger(__name__)

SEGUNDOS_LED_ERROR = 6.0
# Cada cuánto se le vuelve a preguntar al sistema si ya tiene la hora (pieza D).
PERIODO_CONSULTA_HORA = 2.0
# Cada cuánto se anota en el registro que se SIGUE esperando la hora (Fase 4e).
# No es la frecuencia de las consultas: solo la del aviso que deja rastro en el
# journal, para que una espera larga no parezca silencio (ficha F-273).
PERIODO_AVISO_HORA = 10.0
MARCA_TIMESYNC = Path("/run/systemd/timesync/synchronized")


def hora_sincronizada_del_sistema() -> bool:
    """¿El sistema ya puso la hora en hora? (pieza D, Fase 4d).

    La Pi del asadero NO lleva batería RTC: al encender cree que es el día en
    que se apagó, y la hora real le llega por NTP cuando entra a la red del
    restaurante. Del día y de la hora dependen los topes diarios, las fechas
    'desde'/'hasta', las franjas y el reparto por horas, así que el kiosco
    espera un poco antes de imprimir nada.

    Se usa la señal que exista: primero el archivo que crea systemd-timesyncd
    al sincronizar; si no está, `timedatectl`. En una máquina sin ninguna de las
    dos (una PC de desarrollo, por ejemplo) se contesta que sí, para no quedarse
    esperando algo que nadie va a contestar.
    """
    try:
        if MARCA_TIMESYNC.exists():
            return True
    except OSError:      # pragma: no cover - rutas raras del sistema de archivos
        pass
    if not shutil.which("timedatectl"):
        return True
    try:
        r = subprocess.run(["timedatectl", "show", "-p", "NTPSynchronized", "--value"],
                           capture_output=True, text=True, timeout=10)
    except (subprocess.SubprocessError, OSError) as e:
        log.warning("No se pudo preguntar a timedatectl si la hora está sincronizada: %s", e)
        return False
    return r.stdout.strip() == "yes"


def crear_impresora(cfg: Config, tipo: str | None = None,
                    salida: Callable[[str], None] = print) -> Impresora:
    """Construye el transporte indicado en config (o el forzado por `tipo`)."""
    imp = cfg.impresora
    tipo = tipo or imp.tipo
    if tipo == "bluetooth":
        if imp.mac.replace(":", "").strip("0") == "":
            raise ErrorConfig(
                "Falta la dirección Bluetooth de la impresora: pon la MAC real en impresora.mac "
                "de config.json (la obtienes con herramientas/emparejar.sh)")
        return escpos.ImpresoraBluetooth(
            mac=imp.mac, canal=imp.canal, reintentos=imp.reintentos,
            espera_reintento=imp.espera_reintento_seg, timeout=imp.timeout_seg,
            tamano_bloque=imp.tamano_bloque, pausa_bloque=imp.pausa_bloque_seg,
            pausa_inicial=imp.pausa_inicial_seg, pausa_final=imp.pausa_final_seg,
            bytes_por_segundo=imp.bytes_por_segundo, consultar_estado=imp.consultar_estado)
    if tipo == "archivo":
        # consultar_estado solo actúa si la ruta es un dispositivo (la impresora
        # por USB); con un archivo de pruebas no hay a quién preguntarle.
        return escpos.ImpresoraArchivo(imp.ruta, anexar=True, consultar_estado=imp.consultar_estado)
    if tipo == "vista":
        return escpos.ImpresoraVista(codepage=imp.codepage, chars_por_linea=imp.chars_por_linea,
                                     salida=salida)
    raise ValueError(f"tipo de impresora desconocido: {tipo}")


class Ruleta:
    def __init__(self, cfg: Config, inventario: Inventario, impresora: Impresora,
                 entradas: Entradas, reloj: Callable[[], datetime] = datetime.now,
                 monotonico: Callable[[], float] = time.monotonic,
                 dormir: Callable[[float], None] = time.sleep,
                 hora_sincronizada: Callable[[], bool] = hora_sincronizada_del_sistema):
        self.cfg = cfg
        self.inv = inventario
        self.impresora = impresora
        self.entradas = entradas
        self.reloj = reloj
        self.monotonico = monotonico
        self.dormir = dormir
        self.hora_sincronizada = hora_sincronizada

        rebote = cfg.gpio.rebote_ms / 1000.0
        self._deb_jugar = Antirrebote(rebote)
        self._deb_habilitar = Antirrebote(rebote)
        self._jugar_prev = False
        self._jugar_atendida = True     # la pulsación actual de JUGAR ya produjo su acción
        self._hab_prev = False
        self._t_hab = 0.0
        self._hab_atendida = True       # la pulsación actual de HABILITAR ya se usó (jugada o gesto)
        self._fin_espera = float("-inf")
        self._error_hasta = float("-inf")
        self._detener = False
        self.boletos_impresos = 0
        self.reportes_impresos = 0
        self.errores = 0

    # ------------------------------------------------------------------ #
    # Ciclo de vida
    # ------------------------------------------------------------------ #

    def esperar_hora_sincronizada(self) -> bool:
        """Espera hasta `juego.espera_hora_seg` a que el sistema ponga la hora.

        Devuelve True si la hora quedó confirmada. Con el tope en 0 (el valor
        por omisión) no se espera nada, no se registra nada y se da por buena,
        que es como se comportaba el programa antes de la Fase 4d. Esto SOLO
        ocurre al arrancar: una vez arriba, ninguna jugada vuelve a esperar.

        Desde la Fase 4e la espera **se ve en el registro** (ficha F-273): una
        línea al empezar, otra cada PERIODO_AVISO_HORA segundos mientras espera
        y una última con lo que costó. Sin ellas, medio minuto de espera es
        indistinguible en el journal de no haber esperado nada, y en una Pi sin
        batería RTC eso es lo primero que hay que saber el día que un boleto
        salga con la fecha mal. La política no cambia: mismo tope, mismas
        consultas y el mismo aviso en el boleto de inventario.
        """
        tope = self.cfg.juego.espera_hora_seg
        if tope <= 0:
            return True
        inicio = self.monotonico()
        siguiente_aviso = PERIODO_AVISO_HORA
        log.info("Esperando a que la hora se sincronice (hasta %.0f s)…", tope)
        while True:
            try:
                if self.hora_sincronizada():
                    log.info("Hora sincronizada tras %.0f s", self.monotonico() - inicio)
                    return True
            except Exception:
                log.exception("Falló la consulta de la hora del sistema; se sigue sin confirmarla")
                return False
            transcurrido = self.monotonico() - inicio
            restante = tope - transcurrido
            if restante <= 0 or self._detener:
                log.warning("HORA SIN CONFIRMAR: el sistema no sincronizó la hora en %.0f s. "
                            "Revisa la fecha del boleto de inventario antes de abrir: si está "
                            "mal, NO reinicies, espera y pide otro inventario", tope)
                return False
            if transcurrido >= siguiente_aviso:
                log.info("Sigo esperando la hora: llevo %.0f s de %.0f s", transcurrido, tope)
                # El siguiente múltiplo que todavía no ha pasado: si una consulta
                # se atasca, al volver no se sueltan de golpe los avisos que se
                # saltó; se retoma la cadencia donde toca.
                siguiente_aviso = (int(transcurrido // PERIODO_AVISO_HORA) + 1) * PERIODO_AVISO_HORA
            self.dormir(min(PERIODO_CONSULTA_HORA, restante))

    def arrancar(self) -> None:
        """Imprime el inventario inicial (con reintentos) y deja todo listo."""
        log.info("Ruleta arrancando. Premios: %s", ", ".join(self.inv.premios))
        pendientes = self.inv.pendientes()
        if pendientes:
            log.warning("Hay %d boleto(s) sin confirmar en la bitácora: %s",
                        len(pendientes), ", ".join(p.folio_texto for p in pendientes))
        aviso_hora = not self.esperar_hora_sincronizada()
        if self.cfg.juego.imprimir_inventario_al_arrancar:
            intentos = max(1, self.cfg.juego.intentos_inventario_arranque)
            for i in range(1, intentos + 1):
                if self._detener:
                    break
                if self.imprimir_inventario("arranque", aviso_hora=aviso_hora):
                    break
                log.error("Inventario de arranque: intento %d/%d falló", i, intentos)
                if i < intentos and not self._detener:
                    self.dormir(self.cfg.impresora.espera_reintento_seg * 2)
        t = self.monotonico()
        self._actualizar_led(t, habilitado=self._leer_habilitar(t))
        log.info("Lista. Esperando jugadas.")

    def correr(self, periodo: float = 0.01) -> None:
        while not self._detener:
            try:
                self.paso()
            except Exception:  # red de seguridad: el kiosco no debe morir por una jugada
                self.errores += 1
                log.exception("Error inesperado en el ciclo; se sigue esperando pulsaciones")
                t = self.monotonico()
                self._error_hasta = t + SEGUNDOS_LED_ERROR
                self._jugar_atendida = True
                self._hab_atendida = True
                try:
                    self._actualizar_led(t, self._leer_habilitar(t))
                except Exception:
                    pass
            self.dormir(periodo)

    def detener(self) -> None:
        self._detener = True

    def cerrar(self) -> None:
        try:
            self.entradas.led("apagado")
            self.entradas.cerrar()
        finally:
            self.impresora.cerrar()

    # ------------------------------------------------------------------ #
    # Un paso del sondeo
    # ------------------------------------------------------------------ #

    def _leer_habilitar(self, t: float) -> bool:
        if self.cfg.gpio.modo_habilitar == "siempre":
            return True
        return self._deb_habilitar.actualizar(self.entradas.habilitar_presionado(), t)

    def paso(self) -> None:
        t = self.monotonico()
        habilitado = self._leer_habilitar(t)
        jugar = self._deb_jugar.actualizar(self.entradas.jugar_presionado(), t)

        # --- botón HABILITAR (mesero) --------------------------------------
        if habilitado and not self._hab_prev:
            self._t_hab = t
            self._hab_atendida = False
        if jugar:
            # Si alguien juega mientras el mesero habilita, no es un gesto de inventario.
            self._hab_atendida = True
        if (habilitado and not self._hab_atendida and self._gesto_inventario_activo()
                and t - self._t_hab >= self.cfg.gpio.pulsacion_larga_seg):
            self._hab_atendida = True
            self.imprimir_inventario("solicitado")
        self._hab_prev = habilitado

        # --- botón JUGAR (cliente) ------------------------------------------
        if jugar and not self._jugar_prev:
            self._jugar_atendida = not habilitado
            if not habilitado:
                log.info("Pulsación ignorada: el botón HABILITAR no está presionado")
        if not jugar and self._jugar_prev and not self._jugar_atendida:
            self._jugar_atendida = True
            if t < self._fin_espera:
                log.info("Pulsación ignorada: faltan %.1f s de espera", self._fin_espera - t)
            else:
                self.jugar()
        self._jugar_prev = jugar

        self._actualizar_led(t, habilitado)

    def _gesto_inventario_activo(self) -> bool:
        return (self.cfg.gpio.modo_habilitar == "mantener"
                and self.cfg.gpio.pulsacion_larga_seg is not None)

    def _actualizar_led(self, t: float, habilitado: bool) -> None:
        if t < self._error_hasta:
            self.entradas.led("error")
        else:
            self.entradas.led("listo" if habilitado else "apagado")

    def _terminar_accion(self, exito: bool, con_espera: bool, contar_error: bool = True) -> None:
        t = self.monotonico()
        if con_espera:
            self._fin_espera = t + self.cfg.juego.espera_entre_jugadas_seg
        if not exito:
            # `contar_error` en False: el LED avisa, pero no es una avería. Lo
            # usa la jugada rechazada por estar fuera del horario del evento.
            if contar_error:
                self.errores += 1
            self._error_hasta = t + SEGUNDOS_LED_ERROR
        self._actualizar_led(t, self._leer_habilitar(t))

    # ------------------------------------------------------------------ #
    # Acciones
    # ------------------------------------------------------------------ #

    def jugar(self) -> bool:
        """Sortea, emite e imprime un boleto. Devuelve True si se imprimió."""
        self.entradas.led("ocupado")
        ahora = self.reloj()
        horario = self.cfg.juego.horario
        fuera_de_horario = not self.inv.dentro_del_horario(ahora)
        if fuera_de_horario and horario is not None and horario.fuera_de_horario == "no_jugar":
            # Ruta prevista por el documento del evento y NO usada por el evento
            # de septiembre de 2026, que eligió "consuelo": no se gasta ni papel
            # ni folio, y lo único que avisa es el LED de error.
            log.warning("Jugada fuera del horario del evento (%s a %s): no se imprime nada",
                        horario.abre, horario.cierra)
            self._terminar_accion(exito=False, con_espera=True, contar_error=False)
            return False
        premio = self.inv.sortear(ahora)

        try:
            boleto = self.inv.emitir(premio, ahora)
        except ErrorPersistencia as e:
            log.error("Boleto NO emitido, no se pudo guardar el inventario (¿SD llena o solo lectura?): %s", e)
            self._terminar_accion(exito=False, con_espera=True)
            return False

        try:
            if premio is None:
                # Desde la Fase 4c el consuelo tiene peso propio: que salga es lo
                # normal, no un aviso. Lo que sí importa al operador es el otro
                # caso, cuando ya NO queda ningún premio que pudiera salir.
                espera = self.inv.espera_separacion(ahora)
                if fuera_de_horario:
                    log.info("Boleto %s: fuera del horario del evento, boleto de consuelo",
                             boleto.folio_texto)
                elif espera > 0:
                    log.info("Boleto %s: consuelo obligado, faltan %.1f min de separación "
                             "desde el último premio", boleto.folio_texto, espera)
                elif self.inv.disponibles(ahora):
                    log.info("Boleto %s: el sorteo cayó en el consuelo (peso %d)",
                             boleto.folio_texto, self.inv.peso_consuelo)
                else:
                    log.warning("Sin premios disponibles: boleto de consuelo %s", boleto.folio_texto)
                datos = ticket.boleto_consuelo(self.cfg, boleto)
            else:
                if premio.forzado:
                    # Día 2 paso 2 (decisión del usuario del 2026-09-22): este
                    # premio NO salió de la tómbola, se lo llevó la jugada por
                    # estar abierto. Se deja dicho en el registro porque desde el
                    # journal es lo único que distingue un premio forzado de uno
                    # sorteado: en el papel salen idénticos.
                    log.info("Boleto %s: pieza forzada de %s", boleto.folio_texto, premio.nombre)
                datos = ticket.boleto_premio(self.cfg, boleto)
        except Exception:
            # Nada se ha enviado a la impresora: devolver el premio es seguro.
            self.inv.revertir(boleto)
            log.exception("Boleto %s: no se pudo construir el boleto; premio devuelto al inventario",
                          boleto.folio_texto)
            self._terminar_accion(exito=False, con_espera=True)
            return False

        exito = False
        try:
            self.impresora.imprimir(datos)
            self.inv.confirmar(boleto)
            self.boletos_impresos += 1
            exito = True
            log.info("Boleto %s impreso: %s", boleto.folio_texto, premio.nombre if premio else "consuelo")
        except ErrorConexion as e:
            self.inv.revertir(boleto)
            log.error("Boleto %s NO impreso (premio devuelto al inventario): %s", boleto.folio_texto, e)
        except ErrorEnvio as e:
            self.inv.marcar_incierto(boleto)
            log.error("Boleto %s pudo quedar incompleto (%d bytes enviados); revísalo y, si no salió, "
                      "libéralo con: python3 -m ruleta liberar %d  (%s)",
                      boleto.folio_texto, e.bytes_enviados, boleto.folio, e)
        except ErrorImpresora as e:
            self.inv.marcar_incierto(boleto)
            log.error("Boleto %s: error de impresión inesperado: %s", boleto.folio_texto, e)
        finally:
            self._terminar_accion(exito, con_espera=True)
        return exito

    def imprimir_inventario(self, motivo: str = "", aviso_hora: bool = False) -> bool:
        self.entradas.led("ocupado")
        ahora = self.reloj()
        exito = False
        try:
            resumen = self.inv.resumen(ahora)
            datos = ticket.boleto_inventario(self.cfg, resumen, motivo, aviso_hora=aviso_hora)
            self.impresora.imprimir(datos)
            self.reportes_impresos += 1
            exito = True
            log.info("Inventario impreso (%s). Folio actual %05d", motivo, resumen.folio_actual)
        except ErrorImpresora as e:
            log.error("No se pudo imprimir el inventario (%s): %s", motivo, e)
        except Exception:
            log.exception("Error inesperado al preparar el inventario (%s)", motivo)
        finally:
            self._terminar_accion(exito, con_espera=False)
        return exito
