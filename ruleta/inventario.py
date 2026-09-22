"""Inventario de premios, sorteo ponderado y persistencia.

Estado en disco (carpeta_datos/):
  estado.json  - folio actual y contadores de premios entregados (total y por día).
                 Se escribe de forma atómica: primero a un .tmp y luego se
                 renombra, así un apagón a media escritura no lo corrompe.
  boletos.csv  - bitácora de eventos, solo se agrega al final:
                 emitido / impreso / error_conexion / incierto / liberado.
  ruleta.lock  - candado: solo un proceso escribe el inventario a la vez.

Reglas del sorteo:
  * Solo participan los premios que aún tienen stock, no han llegado a su
    tope del día, están dentro de sus fechas 'desde'/'hasta', están dentro del
    horario del evento y de su franja, y tienen alguna pieza YA LIBERADA por
    el reloj (ver «El reparto por horas»).
  * El boleto de consuelo participa como uno más, con 'peso_consuelo'
    papelitos (juego.consuelo.peso): una sola elección ponderada decide entre
    los premios disponibles y el consuelo. El consuelo NO consume stock ni
    tope diario, pero sí consume folio.
  * Con peso_consuelo = 0 el consuelo no entra en la tómbola y se sortea solo
    entre los premios, que es como se comportaba el programa antes de la
    Fase 4c (2026-09-16).
  * Si no hay ningún premio disponible, el sorteo devuelve None (boleto de
    consuelo), tenga el consuelo peso o no.
  * Si el último boleto CON PREMIO se imprimió hace menos de
    'separacion_min_entre_premios' minutos, el sorteo devuelve None sin
    tirar: los premios no deben salir seguidos.
  * Por encima de todo lo anterior mandan los premios FORZADOS (día 2 paso 2,
    decisión del usuario del 2026-09-22): un premio con 'forzado' en true y una
    pieza ya abierta se entrega a la SIGUIENTE jugada, sin tómbola y sin
    esperar la separación mínima. Si hay varios abiertos, primero el que
    empezó su franja antes.

El reparto por horas (Fase 4d, decisión del usuario del 2026-09-16):
  El usuario no puede saber cuántas jugadas habrá en un día, así que el cupo
  diario de cada premio NO está disponible entero desde el primer minuto: se
  abre poco a poco a lo largo de las horas. La pieza k de 'tope_diario' se
  libera en el PUNTO MEDIO de su tramo:

      abre + (k - 0.5) * (cierra - abre) / tope_diario

  Con el horario del evento (12:00 a 23:00) y 11 aguas al día, las aguas se
  liberan a las 12:30, 13:30, ..., 22:30. En un momento t están disponibles
  'liberadas(t) - entregadas_hoy' piezas: una pieza liberada y no ganada sigue
  disponible hasta el cierre (no se pierde), pero tampoco adelanta la
  siguiente. Un premio con 'franjas' solo existe dentro de ellas, y el reparto
  se hace sobre cada franja con su propio tope. Desde el día 2 paso 2
  (2026-09-22) una franja puede además traer 'dias': entonces solo existe en
  esos días operativos. Sin 'juego.horario', el tramo es el día operativo
  completo (hora_inicio_dia a hora_inicio_dia + 24 h), y un premio SIN
  tope_diario no tiene nada que repartir.

Ciclo de un boleto: emitir() consume folio y stock ANTES de imprimir (así un
apagón nunca regala el mismo premio dos veces). Después:
  confirmar()        salió el boleto                      -> 'impreso'
  revertir()         no se conectó, no se envió nada      -> 'error_conexion' (stock regresa)
  marcar_incierto()  se cortó a medio envío               -> 'incierto' (stock NO regresa)
  liberar(folio)     el personal comprobó que no salió    -> 'liberado' (stock regresa)
Los folios que quedaron en 'emitido' o 'incierto' aparecen en el reporte de
inventario como "REVISAR" para que el personal los coteje con el papel.
"""

from __future__ import annotations

import csv
import json
import logging
import os
import random
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterable

from .config import ConfigHorario, Franja, Premio, minutos_del_dia

log = logging.getLogger(__name__)

VERSION_ESTADO = 1
COLUMNAS_CSV = ["folio", "fecha_hora", "dia_operativo", "premio_id", "premio_nombre", "evento"]
EVENTOS_SIN_CIERRE = ("emitido", "incierto")
FORMATO_FECHA_CSV = "%Y-%m-%d %H:%M:%S"
FORMATO_HORA = "%H:%M"


# --------------------------------------------------------------------------- #
# El reparto por horas (funciones puras: la hora entra por parámetro)
# --------------------------------------------------------------------------- #

def instantes_de_liberacion(inicio: datetime, fin: datetime, cupo: int) -> list[datetime]:
    """Cuándo se abre cada una de las `cupo` piezas del tramo [inicio, fin).

    Puntos medios: la pieza k (k = 1..cupo) se libera en
    `inicio + (k - 0.5) * (fin - inicio) / cupo`. Así la primera no sale en el
    minuto de apertura ni la última en el de cierre, y quedan repartidas parejo.
    Decisión del usuario del 2026-09-16 («repartidos parejo de 12:00 a 23:00»).
    """
    if cupo <= 0 or fin <= inicio:
        return []
    segundos = (fin - inicio).total_seconds()
    return [inicio + timedelta(seconds=segundos * (k - 0.5) / cupo) for k in range(1, cupo + 1)]


def _a_la_hora(dia: date, hora: str) -> datetime:
    """El momento del `dia` a la hora "HH:MM" (ya validada por ruleta/config.py)."""
    minutos = minutos_del_dia(hora)
    return datetime.combine(dia, time(minutos // 60, minutos % 60))


class ErrorPersistencia(Exception):
    """No se pudo guardar estado.json (disco lleno, solo lectura, sin permiso)."""


class ErrorBloqueo(Exception):
    """Otro proceso (normalmente el servicio) ya tiene abierto el inventario."""


@dataclass
class Boleto:
    folio: int
    premio: Premio | None           # None = consuelo (no había premios disponibles)
    momento: datetime
    dia: date
    estado: str = "emitido"         # emitido | impreso | error_conexion | incierto | liberado

    @property
    def folio_texto(self) -> str:
        return f"{self.folio:05d}"


@dataclass(frozen=True)
class Pendiente:
    """Boleto cuyo último evento en la bitácora no confirma que saliera el papel."""
    folio: int
    premio_id: str
    premio_nombre: str
    fecha_hora: str
    dia_operativo: str
    evento: str

    @property
    def folio_texto(self) -> str:
        return f"{self.folio:05d}"


@dataclass(frozen=True)
class ResumenPremio:
    premio: Premio
    entregados: int
    restantes: int | None           # None = ilimitado
    hoy: int
    disponible: bool
    motivo: str                     # por qué no está disponible ("" si lo está)
    probabilidad: float             # 0..100, probabilidad actual de salir
    liberadas: int | None = None    # piezas que el reloj ya abrió hoy (None = sin reparto)
    proxima: datetime | None = None  # cuándo se abre la siguiente (None = ya no hay más hoy)


@dataclass(frozen=True)
class Resumen:
    momento: datetime
    dia: date
    premios: list[ResumenPremio]
    folio_actual: int
    boletos_hoy: int
    pendientes: list[Pendiente]
    peso_consuelo: int = 0          # papelitos del consuelo (0 = no entra en la tómbola)
    probabilidad_consuelo: float = 0.0   # 0..100, probabilidad actual de que no salga premio


class Inventario:
    def __init__(self, premios: Iterable[Premio], carpeta_datos: str | Path,
                 hora_inicio_dia: int = 6, rng: random.Random | None = None,
                 peso_consuelo: int = 0, horario: ConfigHorario | None = None,
                 separacion_min_entre_premios: float = 0.0):
        self.premios: dict[str, Premio] = {}
        for p in premios:
            if p.id in self.premios:
                raise ValueError(f"premio duplicado: {p.id}")
            self.premios[p.id] = p
        self.carpeta = Path(carpeta_datos)
        self.carpeta.mkdir(parents=True, exist_ok=True)
        self.ruta_estado = self.carpeta / "estado.json"
        self.ruta_log = self.carpeta / "boletos.csv"
        self.ruta_candado = self.carpeta / "ruleta.lock"
        self.hora_inicio_dia = hora_inicio_dia
        self.peso_consuelo = peso_consuelo
        self.horario = horario
        self.separacion_min_entre_premios = separacion_min_entre_premios
        self.rng = rng or random.SystemRandom()
        self._folio = 0
        self._entregados: dict[str, int] = {}
        self._por_dia: dict[str, dict[str, int]] = {}
        self._boletos_por_dia: dict[str, int] = {}
        self._ultimo_premio: datetime | None = None
        self._candado = None
        self._cargar()

    # ------------------------------------------------------------------ #
    # Candado entre procesos
    # ------------------------------------------------------------------ #

    def bloquear(self) -> None:
        """Toma el candado exclusivo de la carpeta; lanza ErrorBloqueo si ya está tomado.

        Solo aplica en Linux (fcntl). En otros sistemas no hace nada.
        """
        try:
            import fcntl
        except ImportError:  # Windows: no hay flock; la Pi siempre lo tiene
            return
        try:
            candado = open(self.ruta_candado, "a+")
            fcntl.flock(candado.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            raise ErrorBloqueo(
                "Otro proceso ya está usando el inventario (¿el servicio 'ruleta' está corriendo?). "
                "Deténlo primero: sudo systemctl stop ruleta") from e
        self._candado = candado

    def desbloquear(self) -> None:
        if self._candado is not None:
            try:
                self._candado.close()
            except OSError:
                pass
            self._candado = None

    # ------------------------------------------------------------------ #
    # Tiempo
    # ------------------------------------------------------------------ #

    def dia_operativo(self, momento: datetime) -> date:
        """El día de negocio: antes de hora_inicio_dia cuenta como el día anterior."""
        return (momento - timedelta(hours=self.hora_inicio_dia)).date()

    def dentro_del_horario(self, momento: datetime) -> bool:
        """¿El evento está abierto a esa hora? Sin `horario` configurado, siempre."""
        if self.horario is None:
            return True
        minutos = momento.hour * 60 + momento.minute
        # El cierre es exclusivo: a las 23:00 en punto ya no se juega.
        return minutos_del_dia(self.horario.abre) <= minutos < minutos_del_dia(self.horario.cierra)

    def ventana_del_dia(self, dia: date) -> tuple[datetime, datetime]:
        """El tramo sobre el que se reparte el cupo de ese día operativo.

        Con `juego.horario` es de la apertura al cierre. Sin él, el día operativo
        completo (hora_inicio_dia a hora_inicio_dia + 24 h), para que una
        instalación sin horario siga repartiendo sobre algo.
        """
        if self.horario is not None:
            return _a_la_hora(dia, self.horario.abre), _a_la_hora(dia, self.horario.cierra)
        inicio = datetime.combine(dia, time(self.hora_inicio_dia))
        return inicio, inicio + timedelta(hours=24)

    def franjas_del_dia(self, premio: Premio, dia: date) -> list[tuple[datetime, datetime, Franja]]:
        """Las franjas del premio que existen ESE día, en momentos de ese día operativo.

        Una franja con `dias` solo cuenta en los días que enumera (día 2 paso 2,
        decisión del usuario del 2026-09-22: «horas sueltas y distintas por
        día»); una franja sin `dias` cuenta todos los días, que es como se
        comportaba el programa antes. Este es el ÚNICO sitio que filtra por día:
        de aquí cuelgan `franja_activa`, `instantes_del_dia`, `liberadas`,
        `proxima_liberacion` y los motivos de `motivo_no_disponible`.
        """
        return [(_a_la_hora(dia, f.desde_hora), _a_la_hora(dia, f.hasta_hora), f)
                for f in premio.franjas if not f.dias or dia in f.dias]

    def franja_activa(self, premio: Premio, momento: datetime) -> Franja | None:
        """La franja del premio en la que cae `momento` (None si está fuera de todas)."""
        for inicio, fin, franja in self.franjas_del_dia(premio, self.dia_operativo(momento)):
            if inicio <= momento < fin:
                return franja
        return None

    def instantes_del_dia(self, premio: Premio, dia: date) -> list[datetime] | None:
        """Cuándo se abre cada pieza de ese premio ese día. None = sin reparto.

        Con `franjas`, una lista por franja: la franja de UNA pieza se abre al
        empezar (decisión del usuario del 2026-09-16: la silla se puede ganar a
        las 13:00 en punto), y la de varias se reparte parejo dentro del tramo.
        Sin franjas, el `tope_diario` se reparte sobre la ventana del día; un
        premio sin `tope_diario` no tiene nada que repartir.

        Un premio CON franjas pero ninguna de ese día (todas llevan `dias` y
        ninguno es hoy) no abre nada: devuelve la lista vacía, no se cae al
        reparto del `tope_diario`. Es lo correcto —ese día el premio no
        existe— y así lo dice también `motivo_no_disponible`.
        """
        if premio.franjas:
            instantes: list[datetime] = []
            for inicio, fin, franja in self.franjas_del_dia(premio, dia):
                if franja.tope <= 1:
                    instantes.append(inicio)
                else:
                    instantes.extend(instantes_de_liberacion(inicio, fin, franja.tope))
            return sorted(instantes)
        if premio.tope_diario is None:
            return None
        inicio, fin = self.ventana_del_dia(dia)
        return instantes_de_liberacion(inicio, fin, premio.tope_diario)

    def liberadas(self, premio: Premio, momento: datetime) -> int | None:
        """Piezas que el reloj ya abrió hoy. None = ese premio no se reparte."""
        instantes = self.instantes_del_dia(premio, self.dia_operativo(momento))
        if instantes is None:
            return None
        return sum(1 for i in instantes if i <= momento)

    def proxima_liberacion(self, premio: Premio, momento: datetime) -> datetime | None:
        """Cuándo se abre la siguiente pieza de hoy (None si ya no queda ninguna)."""
        instantes = self.instantes_del_dia(premio, self.dia_operativo(momento))
        if instantes is None:
            return None
        return next((i for i in instantes if i > momento), None)

    def espera_separacion(self, momento: datetime) -> float:
        """Minutos que faltan para poder dar otro premio (0.0 = ninguno).

        Decisión del usuario del 2026-09-16: «los premios no deben salir
        seguidos». Si el reloj se fue hacia atrás —la Pi no tiene batería RTC y
        la hora le llega por NTP al arrancar— el instante guardado queda en el
        futuro; eso NO bloquea el juego: se ignora.
        """
        if self.separacion_min_entre_premios <= 0 or self._ultimo_premio is None:
            return 0.0
        transcurridos = (momento - self._ultimo_premio).total_seconds()
        if transcurridos < 0:
            return 0.0
        faltan = self.separacion_min_entre_premios * 60.0 - transcurridos
        return max(0.0, faltan / 60.0)

    # ------------------------------------------------------------------ #
    # Consulta
    # ------------------------------------------------------------------ #

    @property
    def folio_actual(self) -> int:
        return self._folio

    def entregados(self, premio_id: str) -> int:
        return self._entregados.get(premio_id, 0)

    def entregados_en_dia(self, premio_id: str, dia: date) -> int:
        return self._por_dia.get(dia.isoformat(), {}).get(premio_id, 0)

    def boletos_en_dia(self, dia: date) -> int:
        return self._boletos_por_dia.get(dia.isoformat(), 0)

    def restantes(self, premio: Premio) -> int | None:
        if premio.stock is None:
            return None
        return max(0, premio.stock - self.entregados(premio.id))

    def motivo_no_disponible(self, premio: Premio, momento: datetime) -> str:
        """Cadena vacía si está disponible; si no, la razón en español."""
        dia = self.dia_operativo(momento)
        if premio.desde and dia < premio.desde:
            return f"desde {premio.desde.strftime('%d/%m')}"
        if premio.hasta and dia > premio.hasta:
            return "fecha vencida"
        restantes = self.restantes(premio)
        if restantes is not None and restantes <= 0:
            return "agotado"
        if premio.tope_diario is not None and self.entregados_en_dia(premio.id, dia) >= premio.tope_diario:
            return "tope de hoy"
        # --- lo que añadió la Fase 4d (reparto por horas, 2026-09-16) --------
        if not self.dentro_del_horario(momento):
            return "fuera de horario"
        if premio.franjas and self.franja_activa(premio, momento) is None:
            proxima = next((i for i, _, _ in self.franjas_del_dia(premio, dia) if i > momento), None)
            if proxima is None:
                return "franjas de hoy cerradas"
            return f"su franja abre a las {proxima.strftime(FORMATO_HORA)}"
        liberadas = self.liberadas(premio, momento)
        if liberadas is not None and liberadas - self.entregados_en_dia(premio.id, dia) <= 0:
            proxima = self.proxima_liberacion(premio, momento)
            if proxima is None:
                return "todo lo de hoy ya salió"
            return f"se libera a las {proxima.strftime(FORMATO_HORA)}"
        return ""

    def disponibles(self, momento: datetime) -> list[Premio]:
        return [p for p in self.premios.values() if not self.motivo_no_disponible(p, momento)]

    def forzados_abiertos(self, momento: datetime) -> list[Premio]:
        """Los premios FORZADOS que en ese momento tienen una pieza abierta.

        Día 2 paso 2, decisión del usuario del 2026-09-22 («después de tal hora,
        el próximo juego se la saca»): estos premios no se sortean, se entregan.
        El orden es el de entrega: primero el que lleva **más tiempo abierto**
        —el que empezó su franja antes— y, a igualdad, el orden de
        `config.json`, que `sorted` conserva por ser estable.

        Un premio forzado SIN franjas se considera abierto desde la apertura del
        día, así que va delante de los que abren más tarde.
        """
        dia = self.dia_operativo(momento)
        inicio_del_dia, _ = self.ventana_del_dia(dia)

        def cuando_abrio(premio: Premio) -> datetime:
            for inicio, fin, _ in self.franjas_del_dia(premio, dia):
                if inicio <= momento < fin:
                    return inicio
            return inicio_del_dia

        return sorted((p for p in self.disponibles(momento) if p.forzado), key=cuando_abrio)

    def probabilidades(self, momento: datetime) -> dict[str, float]:
        """Probabilidad (0..100) de cada premio disponible.

        El boleto de consuelo entra en el DENOMINADOR con sus papelitos, así que
        con peso_consuelo > 0 estos porcentajes ya no suman 100: lo que falta es
        `probabilidad_consuelo()`.
        """
        disp = self.disponibles(momento)
        total = sum(p.peso for p in disp) + self.peso_consuelo
        return {p.id: (100.0 * p.peso / total if total else 0.0) for p in disp}

    def probabilidad_consuelo(self, momento: datetime) -> float:
        """Probabilidad (0..100) de que la jugada NO dé premio."""
        total = sum(p.peso for p in self.disponibles(momento)) + self.peso_consuelo
        if total <= 0:
            return 100.0        # sin premios disponibles el consuelo es seguro
        return 100.0 * self.peso_consuelo / total

    def resumen(self, momento: datetime) -> Resumen:
        dia = self.dia_operativo(momento)
        probs = self.probabilidades(momento)
        filas = []
        for p in self.premios.values():
            motivo = self.motivo_no_disponible(p, momento)
            filas.append(ResumenPremio(
                premio=p,
                entregados=self.entregados(p.id),
                restantes=self.restantes(p),
                hoy=self.entregados_en_dia(p.id, dia),
                disponible=not motivo,
                motivo=motivo,
                probabilidad=probs.get(p.id, 0.0),
                liberadas=self.liberadas(p, momento),
                proxima=self.proxima_liberacion(p, momento),
            ))
        return Resumen(momento=momento, dia=dia, premios=filas,
                       folio_actual=self._folio, boletos_hoy=self.boletos_en_dia(dia),
                       pendientes=self.pendientes(),
                       peso_consuelo=self.peso_consuelo,
                       probabilidad_consuelo=self.probabilidad_consuelo(momento))

    # ------------------------------------------------------------------ #
    # Juego
    # ------------------------------------------------------------------ #

    def sortear(self, momento: datetime) -> Premio | None:
        """UNA sola elección ponderada entre los premios disponibles y el consuelo.

        Devuelve el premio que salió, o None si salió el boleto de consuelo.
        Fuera del horario del evento y durante la separación mínima entre
        premios (Fase 4d) ni siquiera se tira: el resultado es el consuelo.

        ANTES que todo eso van los premios FORZADOS (día 2 paso 2, decisión del
        usuario del 2026-09-22): si hay alguna pieza forzada abierta, la jugada
        se la lleva **sin tómbola** y **sin esperar la separación mínima**,
        porque lo que el usuario pidió es que se la saque *la siguiente jugada*,
        no la siguiente que pase el minuto. El horario del evento sigue
        mandando: fuera de él no hay nada disponible y tampoco hay forzados.
        """
        forzados = self.forzados_abiertos(momento)
        if forzados:
            return forzados[0]
        if self.espera_separacion(momento) > 0:
            return None
        disp = self.disponibles(momento)
        if not disp:
            return None
        poblacion: list[Premio | None] = list(disp)
        pesos: list[float] = [p.peso for p in disp]
        if self.peso_consuelo > 0:
            poblacion.append(None)
            pesos.append(self.peso_consuelo)
        return self.rng.choices(poblacion, weights=pesos, k=1)[0]

    def emitir(self, premio: Premio | None, momento: datetime) -> Boleto:
        """Consume folio y stock, guarda el estado y registra el evento 'emitido'.

        Se llama ANTES de imprimir: si la impresión falla sin haber enviado
        nada, `revertir()` regresa el premio al inventario (el folio no se reusa).
        Si no se puede guardar en disco, no se consume nada y se lanza
        ErrorPersistencia (el boleto no debe imprimirse).
        """
        dia = self.dia_operativo(momento)
        clave_dia = dia.isoformat()
        self._folio += 1
        self._boletos_por_dia[clave_dia] = self._boletos_por_dia.get(clave_dia, 0) + 1
        if premio is not None:
            self._sumar(premio.id, clave_dia, +1)
        boleto = Boleto(folio=self._folio, premio=premio, momento=momento, dia=dia)
        try:
            self._guardar()
        except OSError as e:
            # Deshacer en memoria: el boleto no existe.
            self._folio -= 1
            self._boletos_por_dia[clave_dia] = max(0, self._boletos_por_dia.get(clave_dia, 0) - 1)
            if premio is not None:
                self._sumar(premio.id, clave_dia, -1)
            log.error("No se pudo guardar %s: %s", self.ruta_estado, e)
            raise ErrorPersistencia(f"no se pudo guardar el inventario en {self.ruta_estado}: {e}") from e
        self._registrar(boleto, "emitido")
        log.info("Boleto %s emitido: %s", boleto.folio_texto, premio.nombre if premio else "consuelo")
        return boleto

    def confirmar(self, boleto: Boleto) -> None:
        boleto.estado = "impreso"
        if boleto.premio is not None:
            # Se apunta el instante del último premio que SALIÓ en papel, no el
            # del emitido: si la impresión falla, el premio vuelve al inventario
            # y no tiene por qué frenar al siguiente. Va a disco para que la
            # separación mínima sobreviva a un reinicio del servicio.
            self._ultimo_premio = boleto.momento
            try:
                self._guardar()
            except OSError as e:
                log.error("No se pudo guardar el instante del último premio: %s", e)
        self._registrar(boleto, "impreso")

    def revertir(self, boleto: Boleto) -> None:
        """La impresión falló sin enviar datos: el premio vuelve al inventario."""
        if boleto.estado != "emitido":
            return
        boleto.estado = "error_conexion"
        self._devolver(boleto.premio.id if boleto.premio else None, boleto.dia.isoformat())
        self._registrar(boleto, "error_conexion")
        log.warning("Boleto %s revertido por error de conexión", boleto.folio_texto)

    def marcar_incierto(self, boleto: Boleto) -> None:
        """Se enviaron datos pero la conexión falló: pudo imprimirse o no.

        El premio se queda como entregado (evita entregar el mismo premio dos
        veces); el personal decide con el boleto físico en la mano y, si no
        salió, lo libera con `liberar(folio)`.
        """
        boleto.estado = "incierto"
        self._registrar(boleto, "incierto")
        log.warning("Boleto %s incierto: la impresión pudo quedar incompleta", boleto.folio_texto)

    # ------------------------------------------------------------------ #
    # Reconciliación con la bitácora
    # ------------------------------------------------------------------ #

    def eventos(self) -> list[dict[str, str]]:
        """Filas de boletos.csv (lista vacía si no existe o no se puede leer)."""
        if not self.ruta_log.exists():
            return []
        try:
            with open(self.ruta_log, encoding="utf-8", newline="") as f:
                return [fila for fila in csv.DictReader(f) if fila.get("folio")]
        except (OSError, csv.Error) as e:
            log.error("No se pudo leer %s: %s", self.ruta_log, e)
            return []

    def ultimo_evento_por_folio(self) -> dict[int, dict[str, str]]:
        ultimo: dict[int, dict[str, str]] = {}
        for fila in self.eventos():
            try:
                ultimo[int(fila["folio"])] = fila
            except (TypeError, ValueError):
                continue
        return ultimo

    def pendientes(self) -> list[Pendiente]:
        """Folios cuyo último evento es 'emitido' o 'incierto' (sin premio de consuelo)."""
        salida = []
        for folio, fila in sorted(self.ultimo_evento_por_folio().items()):
            if fila.get("evento") in EVENTOS_SIN_CIERRE and fila.get("premio_id") != "consuelo":
                salida.append(Pendiente(
                    folio=folio, premio_id=fila.get("premio_id", ""),
                    premio_nombre=fila.get("premio_nombre", ""),
                    fecha_hora=fila.get("fecha_hora", ""),
                    dia_operativo=fila.get("dia_operativo", ""),
                    evento=fila.get("evento", "")))
        return salida

    def liberar(self, folio: int) -> Pendiente:
        """El personal comprobó que el boleto `folio` no salió: devuelve el premio.

        Solo se aceptan folios en 'emitido' o 'incierto'. Lanza ValueError si el
        folio no existe o ya está cerrado.
        """
        fila = self.ultimo_evento_por_folio().get(folio)
        if fila is None:
            raise ValueError(f"el folio {folio:05d} no aparece en {self.ruta_log}")
        evento = fila.get("evento", "")
        if evento not in EVENTOS_SIN_CIERRE:
            raise ValueError(f"el folio {folio:05d} ya está cerrado como '{evento}'; no se puede liberar")
        premio_id = fila.get("premio_id", "")
        dia = fila.get("dia_operativo", "")
        self._devolver(None if premio_id == "consuelo" else premio_id, dia)
        try:
            momento = datetime.strptime(fila.get("fecha_hora", ""), FORMATO_FECHA_CSV)
        except ValueError:
            momento = datetime.now()
        boleto = Boleto(folio=folio, premio=self.premios.get(premio_id), momento=momento,
                        dia=date.fromisoformat(dia) if dia else self.dia_operativo(momento),
                        estado="liberado")
        if boleto.premio is None and premio_id not in ("", "consuelo"):
            # El premio ya no está en la configuración: conservamos el nombre de la bitácora.
            boleto.premio = Premio(id=premio_id, nombre=fila.get("premio_nombre", premio_id), peso=1)
        self._registrar(boleto, "liberado")
        log.warning("Boleto %s liberado por el personal: %s vuelve al inventario", boleto.folio_texto, premio_id)
        return Pendiente(folio=folio, premio_id=premio_id, premio_nombre=fila.get("premio_nombre", ""),
                         fecha_hora=fila.get("fecha_hora", ""), dia_operativo=dia, evento="liberado")

    # ------------------------------------------------------------------ #
    # Mantenimiento
    # ------------------------------------------------------------------ #

    def reiniciar(self) -> None:
        """Borra contadores y folio (para un evento nuevo). No toca el CSV."""
        self._folio = 0
        self._entregados = {}
        self._por_dia = {}
        self._boletos_por_dia = {}
        self._ultimo_premio = None
        try:
            self._guardar()
        except OSError as e:
            raise ErrorPersistencia(f"no se pudo guardar {self.ruta_estado}: {e}") from e

    # ------------------------------------------------------------------ #
    # Internos
    # ------------------------------------------------------------------ #

    def _sumar(self, premio_id: str, clave_dia: str, delta: int) -> None:
        self._entregados[premio_id] = max(0, self.entregados(premio_id) + delta)
        del_dia = self._por_dia.setdefault(clave_dia, {})
        del_dia[premio_id] = max(0, del_dia.get(premio_id, 0) + delta)

    def _devolver(self, premio_id: str | None, clave_dia: str) -> None:
        """Resta un boleto (y un premio, si lo hubo) de los contadores y guarda."""
        if premio_id:
            self._sumar(premio_id, clave_dia, -1)
        self._boletos_por_dia[clave_dia] = max(0, self._boletos_por_dia.get(clave_dia, 0) - 1)
        try:
            self._guardar()
        except OSError as e:
            # La memoria ya quedó bien; en disco se corregirá en el siguiente guardado.
            log.error("No se pudo guardar el estado tras devolver un premio: %s", e)

    def _cargar(self) -> None:
        if not self.ruta_estado.exists():
            try:
                self._guardar()
            except OSError as e:
                log.error("No se pudo crear %s: %s", self.ruta_estado, e)
            return
        try:
            with open(self.ruta_estado, encoding="utf-8") as f:
                datos = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            respaldo = self.ruta_estado.with_suffix(".corrupto")
            log.error("estado.json ilegible (%s); se respalda en %s y se empieza en cero", e, respaldo)
            try:
                os.replace(self.ruta_estado, respaldo)
                self._guardar()
            except OSError as e2:
                log.error("Tampoco se pudo respaldar/recrear el estado: %s", e2)
            return
        self._folio = int(datos.get("folio", 0))
        self._entregados = {k: int(v) for k, v in datos.get("entregados", {}).items()}
        self._por_dia = {d: {k: int(v) for k, v in c.items()} for d, c in datos.get("por_dia", {}).items()}
        self._boletos_por_dia = {k: int(v) for k, v in datos.get("boletos_por_dia", {}).items()}
        # Llave nueva de la Fase 4d. Un estado.json escrito por una versión
        # anterior NO la trae, y eso significa «sin separación pendiente»: los
        # estados viejos se siguen cargando enteros.
        crudo_ultimo = datos.get("ultimo_premio")
        if crudo_ultimo:
            try:
                self._ultimo_premio = datetime.fromisoformat(str(crudo_ultimo))
            except (TypeError, ValueError):
                log.warning("estado.json trae un 'ultimo_premio' ilegible (%r); se ignora", crudo_ultimo)

    def _guardar(self) -> None:
        """Escritura atómica. Lanza OSError si el disco no coopera."""
        datos = {
            "version": VERSION_ESTADO,
            "folio": self._folio,
            "entregados": self._entregados,
            "por_dia": self._por_dia,
            "boletos_por_dia": self._boletos_por_dia,
            "ultimo_premio": (self._ultimo_premio.isoformat(timespec="seconds")
                              if self._ultimo_premio is not None else None),
            "actualizado": datetime.now().isoformat(timespec="seconds"),
        }
        tmp = self.ruta_estado.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, self.ruta_estado)

    def _registrar(self, boleto: Boleto, evento: str) -> None:
        try:
            nuevo = not self.ruta_log.exists() or self.ruta_log.stat().st_size == 0
            with open(self.ruta_log, "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                if nuevo:
                    w.writerow(COLUMNAS_CSV)
                w.writerow([
                    boleto.folio_texto,
                    boleto.momento.strftime(FORMATO_FECHA_CSV),
                    boleto.dia.isoformat(),
                    boleto.premio.id if boleto.premio else "consuelo",
                    boleto.premio.nombre if boleto.premio else "Sigue participando",
                    evento,
                ])
                f.flush()
                os.fsync(f.fileno())
        except OSError as e:
            # La bitácora es secundaria: nunca debe tirar el programa.
            log.error("No se pudo escribir en %s: %s", self.ruta_log, e)
