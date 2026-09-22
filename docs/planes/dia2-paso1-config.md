# Día 2 · Paso 1 · Reajuste del reparto en `config.json`

**Fecha:** 2026-09-22 (martes), por la mañana.
**Autor del plan:** Claude (ejecutor), del dictado del usuario de esta mañana
(«así va»).
**Fecha límite dura:** desplegado **antes de las 13:00**; el evento abre a las
12:00 y la primera franja nueva de la silla se abre a las **13:17**.

---

## 0. Bitácora

| Casilla | Qué | Estado |
|---|---|---|
| [x] | Plan corto escrito | hecho |
| [x] | `config.json`: D1 a D6 | hecho |
| [x] | Comprobaciones con el motor real (D6) | hecho |
| [x] | Documento del evento (§1, §2, §3, §5.1, §7 y cabecera) | hecho |
| [x] | Goldens actualizados + golden nuevo (D7) | hecho |
| [x] | Mutaciones por copia del golden nuevo (mínimo 6, todas en rojo) | hecho |
| [x] | Fichas nuevas (D8) | hecho |
| [x] | README, solo lo que quedó falso | hecho |
| [ ] | Commit (agente de commit) y **deploy antes de las 13:00** (D9) | pendiente |

---

## 1. Objetivo

El lunes 21 se jugó y **sobraron los premios grandes**: 55 jugadas, y de ellas
**silla 0 de 2** y **set BBQ 1 de 2**. Dos causas medidas:

1. **Poca gente en sus franjas.** Entre 13:00 y 16:00 hubo **9 jugadas**, y
   entre 19:00 y 20:00, **ninguna**.
2. **Peso 2 contra todo lo demás abierto.** Con agua (11), cerveza (10), tacos
   (4 + 4) y consuelo (10) abiertos a la vez, una silla abierta salía en
   **≈ 5 %** de las jugadas.

Este paso hace **tres cosas y nada más**, todas dentro de `config.json`:

- **baja la separación** entre premios de 3 minutos a **1**;
- **sube el peso** de silla, BBQ y hielera a **100**, para que salgan casi
  seguro en cuanto el reloj los abre;
- **repone** lo que no salió el lunes y **mueve las franjas a horas sueltas**,
  repartidas por la tarde y la noche.

**Lo que este paso NO hace:** forzar la salida del premio grande por código. Eso
es el **paso 2** y **no** entra en esta cadena.

---

## 2. Decisiones cerradas

Las dicta el usuario (separación, pesos altos, horas sueltas, reposición,
hielera el jueves y el viernes). Las traduce el orquestador a `config.json`,
porque **la configuración de hoy solo admite un juego de franjas para todos los
días y un `tope_diario` único por premio**: las piezas de más del martes y el
miércoles van como **entradas aparte con fechas**.

- **D1.** `juego.separacion_min_entre_premios`: **3 → 1**.
- **D2.** Pesos: `silla` 2 → **100**, `bbq` 2 → **100**, `hielera` 1 → **100**.
  Los demás pesos y el consuelo (**10**) **no cambian**. Con todo lo del martes
  abierto a la vez: **100 de 239 ≈ 42 %** por jugada cada uno; a solas contra el
  consuelo, **100 de 110 ≈ 91 %**.
- **D3.** `silla`: stock 10, `tope_diario` **2**, franjas **13:17–15:17** (tope 1)
  y **19:23–21:23** (tope 1). Entrada nueva **`silla_extra`**: nombre
  `SILLA DE PLAYA`, detalle `Premio grande`, stock **2**, `tope_diario` 1, peso
  100, `desde` 2026-09-22, `hasta` 2026-09-23, franja **16:08–18:08** (tope 1).
  Total posible: 2 × 4 días + 2 = **10** = todo el stock.
- **D4.** `bbq`: stock 10, `tope_diario` **2**, franjas **14:41–16:41** (tope 1)
  y **20:47–22:47** (tope 1). Entrada nueva **`bbq_extra`**: nombre `SET BBQ`,
  detalle `Premio grande`, stock **1**, `tope_diario` 1, peso 100, `desde` y
  `hasta` 2026-09-22, franja **17:34–19:34** (tope 1). Total posible: 8 + 1 =
  **9** = lo que queda (ya salió 1 el lunes).
- **D5.** `hielera`: franja **19:36–23:00** (tope 1), peso 100, fechas 24 y 25
  **sin cambio**. (El paso 2 pondrá el jueves a las 19:36 y el viernes a las
  20:04; con la configuración de hoy **no se puede**: solo hay un juego de
  franjas para todos los días.)
- **D6.** **Nada más cambia** en `config.json`: tacos, cerveza, agua, consuelo,
  horario, `espera_hora_seg`, `negocio`, `impresora` y `gpio` quedan igual.
- **D7.** Goldens por **igualdad**, con mutaciones por copia.
- **D8.** Documentación: este plan, el documento del evento, fichas y el README
  **solo si algo quedó falso**.
- **D9.** Deploy a la Pi **sin reiniciar el inventario**.

### Lo que queda repartido por día

| Día | Sillas | Sets BBQ | De dónde salen |
|---|---|---|---|
| martes 22 | **3** | **3** | 2 de `silla`/`bbq` + 1 de `silla_extra`/`bbq_extra` |
| miércoles 23 | **3** | **2** | 2 de `silla`/`bbq` + 1 de `silla_extra` |
| jueves 24 | **2** | **2** | solo `silla`/`bbq` |
| viernes 25 | **2** | **2** | solo `silla`/`bbq` |
| **Total** | **10** | **9** | = el stock que queda de cada uno |

---

## 3. Trampas de este repo (un ejecutor sin contexto no las adivina)

1. **Los goldens DERIVAN del documento del evento, no de `config.json`.**
   `tests/test_config.py::TestPremiosOficialesDelEvento` parsea el bloque de
   código json del **§5.1** que empieza por la llave `premios` y lo compara
   **campo por campo y en orden** con lo que carga `config.json`. Si se cambia
   uno y no el otro, la suite se pone en rojo. Manda el **documento** (§6,
   paso 1). Lo mismo con el bloque `juego`.
2. **Hay censos escritos a mano que hay que mover**: `len(cfg.premios) == 7`,
   la lista de ids en orden, `sum(stock) == 167`, `sum(tope_diario) == 34`, el
   censo de franjas (hielera 1, silla 2, bbq 2) y `sum(franjas) == 5`, el censo
   de fechas por id, el calendario del jueves de `tests/test_instalacion.py` y
   el `len(premios) == 7` de `premios_del_documento()`. **Todos por igualdad**:
   hay que actualizarlos, no aflojarlos.
3. **Las entradas extra llevan el MISMO nombre visible** que su premio
   principal (`SILLA DE PLAYA`, `SET BBQ`): el cliente no debe notar el apaño.
   Ojo con el diccionario por nombre del golden de la tabla del §2: con nombres
   repetidos gana el último. Por eso ese golden solo nombra `AGUA FRESCA` y
   `HIELERA IGLOO`, que son únicos.
4. **El id nuevo tiene que pasar la validación** de `ruleta/config.py`
   (solo letras, números, guion y guion bajo; re-grep antes de editar):
   `silla_extra` y `bbq_extra` la pasan.
5. **`estado.json` guarda los entregados POR ID.** Lo que se entregue como
   `silla_extra` **no descuenta** del stock de `silla`. Al quitar las entradas
   extra en el futuro hay que descontarlo a mano (ficha **F-281**).
6. **En el deploy se hace `restart`, NUNCA `reiniciar`.** El inventario del
   evento está **vivo**: folio 55 y premios entregados del lunes.
   `python3 -m ruleta reiniciar` los borraría.
7. **LF en todos los archivos** (`.gitattributes`). En la PC el intérprete es
   `python`; en la Pi, `python3`.
8. **Una franja de `tope` 1 abre su pieza al EMPEZAR la franja**, no a la mitad
   (`instantes_del_dia`). Por eso las horas sueltas son horas de apertura.

---

## 4. Anclas que derivan (re-grep antes de editar)

| Qué | Cómo encontrarlo |
|---|---|
| Censos de `config.json` | `grep -n "len(cfg.premios)" tests/test_config.py` |
| Censo de franjas | `grep -n "len(p.franjas)" tests/test_config.py` |
| Censo de fechas | `grep -n "2026-09-24" tests/test_config.py` |
| Calendario del evento | `grep -n "test_las_fechas_del_evento_deciden" tests/test_instalacion.py` |
| Bloques del documento | `grep -n "^.\`\`json" docs/evento-2026-09-asadero-33.md` |
| Última ficha | `grep -n "^## F-" docs/fichas.md | tail -1` |
| README que queda falso | `grep -n "3 minutos" README.md` |

---

## 5. Criterios de aceptación

- `python -m unittest discover -s tests -t .` en verde, con **más** pruebas que
  las 273 de ayer.
- `git status --porcelain` **solo** con: `config.json`, `tests/test_config.py`,
  `tests/test_instalacion.py`, `tests/test_inventario.py`,
  `tests/test_ticket.py`, `docs/planes/dia2-paso1-config.md`, `docs/fichas.md`,
  `README.md` y `docs/evento-2026-09-asadero-33.md`. **Nueve rutas, no ocho:**
  `tests/test_ticket.py` entró porque
  `test_inventario_del_config_real_trae_el_reparto_por_horas` ancla por igualdad
  las líneas «hoy N · liberadas N · sig HH:MM» del boleto de inventario, que se
  derivan del `config.json` real; con nueve premios pasa de 7 líneas a 9 y sin
  ese cambio la suite queda en rojo. **Lo aprueba el orquestador antes del
  commit.**
- Las cinco comprobaciones de D6 con el motor real, con su salida pegada en el
  informe.
- Mutaciones del golden nuevo: **mínimo 6, todas en rojo**.
- En la Pi: `active`, `NRestarts=0`, el journal con los **nueve** ids y
  `Folio actual 00055`, y `datos/estado.json` idéntico a `/tmp/estado-antes.json`
  salvo la marca `actualizado`.

---

## 6. Prohibiciones

- **No se toca código** (`ruleta/*.py`): este paso es configuración y
  documentación. El forzado del premio grande es el **paso 2**.
- **No se toca `CLAUDE.md`.**
- **Nunca** `python3 -m ruleta reiniciar` en la Pi: el inventario del evento
  está vivo.
- **Nunca** `git` que modifique desde el ejecutor: commit y push los hace el
  agente de commit.
- **No se toca** `datos/` del repo ni el `estado.json` de la Pi.
- No se añade nada fuera de D1–D9.
