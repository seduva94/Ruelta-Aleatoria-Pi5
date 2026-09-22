# Día 2 · Paso 2 · Horas por día y premio forzado (esto SÍ toca el programa)

**Fecha:** 2026-09-22 (martes), por la tarde.
**Autor del plan:** Claude (ejecutor), del dictado del usuario de esta tarde y de
las decisiones de diseño cerradas por el orquestador.
**Fecha límite dura:** el brief decía «antes de las **19:23**», por la silla de
la noche. **Medido con el motor real y el estado de hoy —folio 61, con una silla
y un set BBQ ya entregados— la primera pieza forzada de la tarde es la
`silla_extra` de las 16:08**, no la de las 19:23: a esa hora la silla del
mediodía ya está entregada y el set de la tarde también. Así que **el límite
útil es las 16:08**; después de esa hora el despliegue sigue valiendo, solo que
la silla de reposición se habrá repartido por tómbola durante el rato que falte.
El evento está **en marcha** y el inventario de la Pi es el real.

**Lo que abre hoy, tras desplegar** (medido, con el estado de las 15:15):
16:08 `silla_extra` · 17:34 `bbq_extra` (los dos a la vez hasta las 18:08) ·
19:23 `silla` · 20:47 `bbq` · nada grande desde las 22:47.

---

## 0. Bitácora

| Casilla | Qué | Estado |
|---|---|---|
| [x] | Plan escrito **antes** del código | hecho |
| [x] | Suite verde medida antes de empezar (**274**) | hecho |
| [x] | D1 · `Franja.dias` en `ruleta/config.py` | hecho |
| [x] | D2 · `Premio.forzado` en el motor, en el log y en el boleto | hecho |
| [x] | D3 · `config.json` con las horas por día | hecho |
| [x] | D4 · goldens por igualdad | hecho |
| [x] | D4 · mutaciones por copia (mínimo 8, todas en rojo) | hecho |
| [x] | D5 · documento del evento, README y fichas | hecho |
| [ ] | Commit (agente de commit) y **deploy antes de las 19:23** (D7) | pendiente |

---

## 1. Objetivo

El **paso 1** de esta mañana (`310e51f`) hizo lo que se podía hacer **sin tocar
código**: bajó la separación a 1 minuto, subió los tres grandes a **peso 100** y
movió las franjas a horas sueltas. Dejó dos cosas fuera, y las dos son de
programa:

1. **Horas distintas por día.** `config.json` no sabe de días: un premio tiene un
   solo juego de franjas para los cinco. Por eso las horas del martes rigen
   también el miércoles, el jueves y el viernes, y la hielera queda a las 19:36
   los dos días que sale (ficha **F-281**).
2. **Forzar la salida del premio grande.** Con peso 100 una silla abierta se
   lleva **≈ 42 %** de las jugadas con todo lo demás abierto: sigue siendo un
   sorteo, y puede no salir (ficha **F-280**).

Este paso construye las dos: **`dias` por franja** y **`forzado` por premio**.

---

## 2. Decisiones cerradas

Las de **conducta** (1 y 2) son del usuario, del 2026-09-22 por la tarde. Las de
**diseño** (D1 a D7) las cerró el orquestador.

### Lo que dictó el usuario

1. **FORZADO.** Para la silla, el set BBQ y la hielera: «después de tal hora, el
   próximo juego se la saca». La siguiente jugada **gana la pieza abierta, sin
   sorteo**.
2. **HORAS SUELTAS Y DISTINTAS POR DÍA**, ventana de **2 horas** desde cada hora,
   y lo que una ventana abre y nadie gana **pasa a la siguiente ventana del
   mismo día**:

| Día | Sillas | Sets BBQ | Hielera |
|---|---|---|---|
| **martes 22** | 13:17 · 16:08 · 19:23 | 14:41 · 17:34 · 20:47 | — |
| **miércoles 23** | 13:09 · 16:21 · 19:38 | 14:52 · 20:19 | — |
| **jueves 24** | 13:26 · 19:11 | 14:37 · 20:52 | **19:36** (hasta el cierre) |
| **viernes 25** | 13:04 · 19:31 | 14:58 · **21:06** (hasta 23:00) | **20:04** (hasta el cierre) |

Totales entre martes y viernes: **10 sillas** y **9 sets BBQ**, que es lo que
queda en la bodega.

### D1 · `dias` dentro de cada franja

- `Franja` gana el campo **opcional** `dias`: lista de fechas `"AAAA-MM-DD"`.
  **Ausente o vacía = todos los días** (la conducta de hoy, para no romper
  ninguna instalación).
- `franjas_del_dia`, y por tanto `franja_activa`, `instantes_del_dia`,
  `liberadas`, `proxima_liberacion` y `motivo_no_disponible`, **solo consideran
  las franjas cuyo `dias` incluya la fecha del día operativo** (o que no lo
  traigan).
- Validación en `ruleta/config.py` **como las fechas `desde`/`hasta`**: mensaje
  en español que **nombre la llave** `dias`.
- Una franja con `hasta_hora` **23:00** y cierre **23:00** tiene que seguir
  siendo **válida** (la hielera y el set BBQ del viernes la usan).

### D2 · `forzado` por premio

- `Premio` gana el campo **opcional** `forzado`: booleano, **por omisión
  `false`**.
- En `sortear(momento)`: **si hay piezas abiertas de premios forzados, la jugada
  gana UNA de ellas sin tómbola**. Si hay varias, la del premio **cuya franja
  activa empezó antes**; a igualdad, **el orden de `config.json`**.
- El forzado **IGNORA la separación mínima** entre premios: el usuario quiere que
  se la lleve **la siguiente jugada**, no la siguiente que pase el minuto.
- **Si no hay forzadas abiertas, todo sigue igual que hoy**: separación, tómbola
  con pesos y consuelo.
- **El horario del evento sigue mandando**: fuera de él no hay ningún premio
  disponible, así que tampoco hay forzados.
- El **`peso`** de un premio forzado **deja de importar** mientras esté forzado,
  pero **se conserva** en `config.json` (es lo que vale si alguien quita
  `forzado`).
- **Log** (INFO): `Boleto NNNNN: pieza forzada de NOMBRE`.
- El **boleto de inventario** marca los premios forzados con una señal corta
  junto al nombre, **sin pasar de 48 columnas**.

### D3 · `config.json`

`silla`, `silla_extra`, `bbq`, `bbq_extra` y `hielera` con `"forzado": true`, y
sus franjas con `dias` según la tabla de arriba. **Se conservan** las entradas
`silla_extra` y `bbq_extra` tal cual (ficha **F-284**). **Nada más cambia.**

### D4 · Goldens

Por **igualdad**, con **mutaciones por copia** (mínimo 8, todas en rojo,
ejecutadas de verdad y reportadas).

### D5 · Documentación

Este plan (escrito **antes** del código), el documento del evento (§1, §3, §5.1,
§5.2, §7 y cabecera), el README (§6 y §7) y las fichas.

### D6 · Prohibiciones

Sin dependencias nuevas; sin tocar `ruleta/escpos.py`, `ruleta/hardware.py` ni
`CLAUDE.md`. Todo en español, LF, comentarios que citen la decisión del usuario
del 2026-09-22.

### D7 · Deploy

`git pull --ff-only`, suite en la Pi, respaldo de `datos/estado.json` y
`restart` del servicio. **NUNCA `reiniciar`** y **sin jugar**.

---

## 3. Trampas de este repo (un ejecutor sin contexto no las adivina)

1. **Los goldens DERIVAN del documento del evento, no de `config.json`.**
   `tests/test_config.py::TestPremiosOficialesDelEvento` parsea el bloque de
   código `json` del **§5.1** que empieza por la llave `premios` y lo compara
   **campo por campo y en orden** con lo que carga `config.json`. Manda el
   **documento** (§6, paso 1). Lo mismo con el bloque `juego`, con el `consuelo`
   del §5.2 y con el ejemplo de `franjas` del §5.2 B, que tiene que ser **la
   franja real de la hielera**: al ponerle dos franjas a la hielera, ese ejemplo
   pasa a tener **dos**.
2. **Las entradas extra se CONSERVAN.** `datos/estado.json` guarda los entregados
   **por id**: quitar `silla_extra` a mitad del evento descontaría mal y el
   kiosco creería que le quedan más sillas de las que hay (fichas **F-281** y
   **F-284**).
3. **Las pruebas corren con el registro apagado.** `tests/__init__.py` hace
   `logging.disable(logging.CRITICAL)`; para usar `assertLogs` hay que encenderlo
   dentro del bloque, como hace `registro_activo()` en `tests/test_app.py`
   (ficha **F-253**).
4. **LF en todos los archivos** (`.gitattributes`). En esta PC el intérprete es
   `py -3`; en la Pi, `python3`.
5. **Una franja de `tope` 1 abre su pieza al EMPEZAR la franja**, no a la mitad
   (`instantes_del_dia`): por eso las horas sueltas son horas de apertura.
6. **Hay censos escritos a mano que hay que mover, no aflojar**: las horas de
   liberación del jueves en `tests/test_inventario.py`, el censo de franjas y el
   de fechas en `tests/test_config.py`, el calendario del evento y el reparto del
   día 2 en `tests/test_instalacion.py`, y las líneas «hoy N · liberadas N» del
   boleto en `tests/test_ticket.py`.
7. **Cuidado con los tests de separación mínima**: están escritos a las **14:00
   del jueves 24**, y con las horas nuevas a esa hora hay una **silla forzada
   abierta**, que se salta la separación a propósito. Hay que moverlos a una hora
   del jueves **sin** forzados abiertos (16:37–19:11).
8. **El `dia` de las franjas es el DÍA OPERATIVO** (cambia a las 06:00), igual
   que `desde`/`hasta`.

---

## 4. Anclas que derivan (re-grep antes de editar)

| Qué | Cómo encontrarlo |
|---|---|
| Franjas del motor | `grep -n "def franjas_del_dia" ruleta/inventario.py` |
| Sorteo | `grep -n "def sortear" ruleta/inventario.py` |
| Fila del inventario impreso | `grep -n "col_nombre" ruleta/ticket.py` |
| Censos de `config.json` | `grep -n "len(p.franjas)" tests/test_config.py` |
| Claves comparadas con el documento | `grep -n "CLAVES_DEL_DOCUMENTO" tests/test_config.py` |
| Reparto del día 2 | `grep -n "test_el_reparto_del_dia_2" tests/test_instalacion.py` |
| Bloques del documento | `grep -n '^```json' docs/evento-2026-09-asadero-33.md` |
| Última ficha | `grep -n "^## F-" docs/fichas.md \| tail -1` |

---

## 5. Criterios de aceptación

- Suite en verde, con **más** pruebas que las **274** de antes de empezar.
- `git status --porcelain` solo con: `ruleta/config.py`, `ruleta/inventario.py`,
  `ruleta/app.py`, `ruleta/ticket.py`, `config.json`, `tests/test_config.py`,
  `tests/test_inventario.py`, `tests/test_app.py`, `tests/test_ticket.py`,
  `tests/test_instalacion.py`, `docs/planes/dia2-paso2-forzado.md`,
  `docs/fichas.md`, `README.md` y `docs/evento-2026-09-asadero-33.md`.
- Comprobaciones con el **motor real**: las piezas abiertas a las horas de D4(b)
  y el forzado con un `rng` espía, con su salida pegada en el informe.
- Mutaciones: **mínimo 8, todas en rojo**.
- En la Pi: `active`, `NRestarts=0`, journal con `Premios`, `Inventario impreso`
  con el folio del momento, `Lista` y **cero** `ERROR`; `datos/estado.json`
  idéntico al respaldo salvo la marca `actualizado`.

---

## 6. Prohibiciones

- **Nunca** `python3 -m ruleta reiniciar`: el inventario del evento está vivo.
- **Nunca** `git` que modifique desde el ejecutor.
- **No se toca** `ruleta/escpos.py`, `ruleta/hardware.py` ni `CLAUDE.md`.
- **No se juega** en la Pi durante la verificación: el evento está abierto y
  cada jugada gasta folio y premios de verdad.
- No se añade nada fuera de D1–D7.
