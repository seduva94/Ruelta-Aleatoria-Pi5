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
    tope del día y están dentro de sus fechas 'desde'/'hasta'.
  * Entre los disponibles se elige al azar proporcionalmente a su 'peso'.
  * Si no hay ninguno disponible, el sorteo devuelve None (boleto de consuelo).

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
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

from .config import Premio

log = logging.getLogger(__name__)

VERSION_ESTADO = 1
COLUMNAS_CSV = ["folio", "fecha_hora", "dia_operativo", "premio_id", "premio_nombre", "evento"]
EVENTOS_SIN_CIERRE = ("emitido", "incierto")
FORMATO_FECHA_CSV = "%Y-%m-%d %H:%M:%S"


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


@dataclass(frozen=True)
class Resumen:
    momento: datetime
    dia: date
    premios: list[ResumenPremio]
    folio_actual: int
    boletos_hoy: int
    pendientes: list[Pendiente]


class Inventario:
    def __init__(self, premios: Iterable[Premio], carpeta_datos: str | Path,
                 hora_inicio_dia: int = 6, rng: random.Random | None = None):
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
        self.rng = rng or random.SystemRandom()
        self._folio = 0
        self._entregados: dict[str, int] = {}
        self._por_dia: dict[str, dict[str, int]] = {}
        self._boletos_por_dia: dict[str, int] = {}
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
        return ""

    def disponibles(self, momento: datetime) -> list[Premio]:
        return [p for p in self.premios.values() if not self.motivo_no_disponible(p, momento)]

    def probabilidades(self, momento: datetime) -> dict[str, float]:
        disp = self.disponibles(momento)
        total = sum(p.peso for p in disp)
        return {p.id: (100.0 * p.peso / total if total else 0.0) for p in disp}

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
            ))
        return Resumen(momento=momento, dia=dia, premios=filas,
                       folio_actual=self._folio, boletos_hoy=self.boletos_en_dia(dia),
                       pendientes=self.pendientes())

    # ------------------------------------------------------------------ #
    # Juego
    # ------------------------------------------------------------------ #

    def sortear(self, momento: datetime) -> Premio | None:
        disp = self.disponibles(momento)
        if not disp:
            return None
        pesos = [p.peso for p in disp]
        return self.rng.choices(disp, weights=pesos, k=1)[0]

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

    def _guardar(self) -> None:
        """Escritura atómica. Lanza OSError si el disco no coopera."""
        datos = {
            "version": VERSION_ESTADO,
            "folio": self._folio,
            "entregados": self._entregados,
            "por_dia": self._por_dia,
            "boletos_por_dia": self._boletos_por_dia,
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
