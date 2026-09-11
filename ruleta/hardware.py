"""Botones y LED: implementación real con gpiozero y una simulada por teclado.

La aplicación solo usa la interfaz `Entradas` (dos lecturas booleanas y un
LED con cuatro estados), así se prueba sin Raspberry y se puede correr en
modo simulación en cualquier PC.

Conexión física (numeración BCM, pull-up interno activado):
  botón JUGAR      -> GPIO 17 y GND      (presionado = el pin cae a 0 V)
  botón HABILITAR  -> GPIO 27 y GND
  LED (opcional)   -> GPIO 22 -> resistencia 330 Ω -> LED -> GND
"""

from __future__ import annotations

import logging
import sys
import threading
import time
from typing import Callable

log = logging.getLogger(__name__)

ESTADOS_LED = ("apagado", "listo", "ocupado", "error")


class Entradas:
    """Interfaz que la aplicación consume."""

    def jugar_presionado(self) -> bool:
        raise NotImplementedError

    def habilitar_presionado(self) -> bool:
        raise NotImplementedError

    def led(self, estado: str) -> None:
        """apagado | listo (fijo) | ocupado (parpadeo lento) | error (parpadeo rápido)."""

    def cerrar(self) -> None:
        pass


class Antirrebote:
    """Filtra rebotes mecánicos: el estado cambia solo si se mantiene `estable_seg`."""

    def __init__(self, estable_seg: float = 0.03, inicial: bool = False):
        self.estable_seg = estable_seg
        self.estado = inicial
        self._candidato = inicial
        self._desde: float | None = None

    def actualizar(self, lectura: bool, ahora: float) -> bool:
        if lectura == self.estado:
            self._candidato = lectura
            self._desde = None
            return self.estado
        if lectura != self._candidato or self._desde is None:
            self._candidato = lectura
            self._desde = ahora
            return self.estado
        if ahora - self._desde >= self.estable_seg:
            self.estado = lectura
            self._desde = None
        return self.estado


# --------------------------------------------------------------------------- #
# Raspberry Pi (gpiozero)
# --------------------------------------------------------------------------- #

class EntradasGPIO(Entradas):
    def __init__(self, pin_jugar: int, pin_habilitar: int | None, pin_led: int | None,
                 pull_up: bool = True):
        try:
            from gpiozero import LED, Button
        except ImportError as e:  # pragma: no cover - solo en la Pi
            raise RuntimeError(
                "No está instalado gpiozero. En la Raspberry ejecuta: "
                "sudo apt install python3-gpiozero python3-lgpio") from e
        self._jugar = Button(pin_jugar, pull_up=pull_up)
        self._habilitar = Button(pin_habilitar, pull_up=pull_up) if pin_habilitar is not None else None
        self._led = LED(pin_led) if pin_led is not None else None
        self._estado_led = ""
        log.info("GPIO listo: jugar=%s habilitar=%s led=%s", pin_jugar, pin_habilitar, pin_led)

    def jugar_presionado(self) -> bool:
        return bool(self._jugar.is_pressed)

    def habilitar_presionado(self) -> bool:
        if self._habilitar is None:
            return True
        return bool(self._habilitar.is_pressed)

    def led(self, estado: str) -> None:
        if estado == self._estado_led or self._led is None:
            self._estado_led = estado
            return
        self._estado_led = estado
        if estado == "apagado":
            self._led.off()
        elif estado == "listo":
            self._led.on()
        elif estado == "ocupado":
            self._led.blink(on_time=0.3, off_time=0.3, background=True)
        elif estado == "error":
            self._led.blink(on_time=0.08, off_time=0.08, background=True)

    def cerrar(self) -> None:
        for dispositivo in (self._jugar, self._habilitar, self._led):
            if dispositivo is not None:
                try:
                    if dispositivo is self._led:
                        dispositivo.off()
                    dispositivo.close()
                except Exception:  # pragma: no cover
                    pass


# --------------------------------------------------------------------------- #
# Simulación (PC o Raspberry sin cablear)
# --------------------------------------------------------------------------- #

class EntradasSimuladas(Entradas):
    """Estados controlados por código o por teclado; sirve para pruebas."""

    def __init__(self, reloj: Callable[[], float] = time.monotonic,
                 salida: Callable[[str], None] | None = None, habilitar_inicial: bool = False):
        self._reloj = reloj
        self._salida = salida
        self._lock = threading.Lock()
        self._jugar_hasta = float("-inf")
        self._jugar_fijo = False
        self._habilitar = habilitar_inicial
        self._habilitar_hasta = float("-inf")
        self.estado_led = "apagado"
        self.historial_led: list[str] = []

    # -- control ----------------------------------------------------------- #

    def pulsar_jugar(self, duracion: float = 0.15) -> None:
        with self._lock:
            self._jugar_hasta = self._reloj() + duracion

    def fijar_jugar(self, presionado: bool) -> None:
        with self._lock:
            self._jugar_fijo = presionado

    def fijar_habilitar(self, presionado: bool) -> None:
        with self._lock:
            self._habilitar = presionado

    def mantener_habilitar(self, duracion: float) -> None:
        """HABILITAR presionado durante `duracion` segundos (gesto de inventario)."""
        with self._lock:
            self._habilitar_hasta = self._reloj() + duracion

    def alternar_habilitar(self) -> bool:
        with self._lock:
            self._habilitar = not self._habilitar
            return self._habilitar

    # -- interfaz Entradas -------------------------------------------------- #

    def jugar_presionado(self) -> bool:
        with self._lock:
            return self._jugar_fijo or self._reloj() < self._jugar_hasta

    def habilitar_presionado(self) -> bool:
        with self._lock:
            return self._habilitar or self._reloj() < self._habilitar_hasta

    def led(self, estado: str) -> None:
        if estado == self.estado_led:
            return
        self.estado_led = estado
        self.historial_led.append(estado)
        if self._salida:
            self._salida(f"[LED] {estado}")


AYUDA_TECLADO = """\
Modo simulación (sin GPIO). Teclas + Enter:
  j  pulsar el botón JUGAR (el cliente)
  h  alternar el botón HABILITAR del mesero (mantenido / suelto)
  i  gesto de inventario: HABILITAR mantenido {seg} s sin tocar JUGAR
  q  salir
"""


def teclado_simulado(entradas: EntradasSimuladas, al_salir: Callable[[], None],
                     pulsacion_larga_seg: float | None = 6.0) -> threading.Thread:
    """Hilo que traduce teclas de la consola a pulsaciones simuladas."""
    ayuda = AYUDA_TECLADO.format(seg=pulsacion_larga_seg if pulsacion_larga_seg is not None else "(desactivado)")

    def bucle():
        print(ayuda, flush=True)
        for linea in sys.stdin:
            tecla = linea.strip()
            if tecla == "j":
                entradas.pulsar_jugar(0.15)
            elif tecla == "i":
                if pulsacion_larga_seg is None:
                    print("[HABILITAR] el gesto de inventario está desactivado (pulsacion_larga_seg = null)", flush=True)
                else:
                    entradas.mantener_habilitar(pulsacion_larga_seg + 0.5)
                    print(f"[HABILITAR] mantenido {pulsacion_larga_seg + 0.5:.1f} s", flush=True)
            elif tecla == "h":
                estado = entradas.alternar_habilitar()
                print(f"[HABILITAR] {'presionado' if estado else 'suelto'}", flush=True)
            elif tecla == "q":
                al_salir()
                return
            elif tecla:
                print(ayuda, flush=True)
        al_salir()

    hilo = threading.Thread(target=bucle, name="teclado", daemon=True)
    hilo.start()
    return hilo
