# Fase 4c · Pieza A: peso propio del boleto de consuelo

Plan prescriptivo **corto**. Redactado el **2026-09-16**, **antes** de tocar una
sola línea de código. Esta fase **sí programa**: toca el motor del sorteo
(`ruleta/inventario.py`), su configuración (`ruleta/config.py`), su cableado
(`ruleta/__main__.py`, `ruleta/app.py`) y el boleto de inventario
(`ruleta/ticket.py`). Todo lo que este plan da por cierto está **medido** o
citado de un archivo del repositorio; lo que no, lo dice.

**ESTADO GLOBAL (2026-09-16, tras el paso del ejecutor).** **CÓDIGO, GOLDENS,
MUTACIONES, FICHAS Y DOCUMENTOS HECHOS; SIN COMMITEAR Y SIN DESPLEGAR.** Las
casillas **0 a 7** de la §0 están marcadas con su evidencia; las **8 a 12** son
de otros eslabones de la cadena. La suite pasó de **216** a **232** pruebas en
verde y **las doce mutaciones del §5 quedaron en rojo**, una de ellas mutando
**el documento del evento** y no el `config.json`, que es lo que demuestra que el
golden **deriva** de verdad. **Lo que esta fase promete sigue sin medirse contra
la Pi:** hasta el Paso 10, lo único demostrado es que en la PC el sorteo mete el
consuelo en la tómbola y que el número sale del documento.

**ESTADO GLOBAL (2026-09-16, al escribir el plan; se conserva).** **FASE 4c ABIERTA, SIN
EMPEZAR.** Árbol limpio en `main` sobre `f810bc4` (Fase 4b, premios reales en
`config.json`), `HEAD` = `origin/main`. Suite: **216 pruebas OK** en la PC
(`python -m unittest discover -s tests -t .`, medido a las 2026-09-16). En la Pi
corre `f810bc4` con los siete premios reales y el inventario **en uso** (el
usuario está probando; el folio **no** se reinicia en esta fase).

## Por qué existe esta fase

Reporte del usuario del **2026-09-16**, probando el kiosco en vivo, literal:

> «no ha salido ningún boleto de gracias por participar, solo premios»

**No es una avería: es el comportamiento documentado.** `Inventario.sortear`
devuelve `None` (consuelo) **solo** cuando **ningún** premio está disponible.
Con los siete premios reales cargados en la Fase 4b —pesos 1, 2, 2, 4, 4, 10 y
11, **suma 34**, y **sin `desde`/`hasta`** (ficha **F-259**)— las primeras **34**
jugadas del día ganan premio, una tras otra, y solo después empieza el consuelo.
Está anotado como ficha **F-261** y medido el 2026-09-13 y el 2026-09-15.

El documento del evento lo llama, con esas palabras, **«lo más importante de
este documento»**: «**no se debe abrir el evento sin la pieza A**»
(`docs/evento-2026-09-asadero-33.md`, §5.2, PENDIENTE A).

## Fuente de verdad

`docs/evento-2026-09-asadero-33.md`. Manda sobre `config.json` y sobre este plan
(su §6, paso 1: «si los dos archivos dicen cosas distintas, gana este documento
y el otro se rehace»). Lo que esta fase usa de él:

- **§5.2, PENDIENTE A** — la forma exacta del campo nuevo:
  `"consuelo": { "titulo": "SIGUE PARTICIPANDO", "texto": "¡Gracias por jugar!", "peso": 217 }`
- **§2** — la regla «el peso es el cupo» y el significado de **N**:
  peso del consuelo = **N − 33**, con N = jugadas esperadas por día.
- **§4, pregunta 1** — **N por omisión = 250**, es decir **peso 217**. La
  pregunta sigue **sin marcar**: 217 es la propuesta por omisión del documento,
  no la respuesta del usuario (ficha nueva **F-263**).

## Convención de comandos (idéntica a las Fases 1 a 4b; se repite porque muerde)

- En **esta PC** el intérprete se llama **`python`**. En la **Pi** se llama
  **`python3`**. Un `python3` tecleado en Windows abre la Tienda de Microsoft y
  se queda esperando.
- La suite se corre **desde la raíz del repositorio**:
  `python -m unittest discover -s tests -t .`
- **Un agente NO invoca el `ssh` de Git Bash.** Escribe siempre
  `/c/Windows/System32/OpenSSH/ssh.exe` con
  `-o BatchMode=yes -o ConnectTimeout=10` (ficha **F-257**: la IP del punto de
  acceso cambia entre sesiones).
- En la Pi, `python3 -m ruleta` **solo funciona desde `~/ruleta`** y **nunca con
  `sudo`**.
- **Ningún agente teclea contraseñas.** Lo que exija una se reporta como
  **«requiere al usuario»**.

---

## 0. Bitácora

`[x]` = hecho **y** con su criterio de aceptación cumplido. `[~]` = hecho pero
sin verificar. `[ ]` = pendiente. **Las casillas se marcan desde salidas de
comando pegadas, nunca de memoria.**

| # | Paso | Quién | Estado |
|---|---|---|---|
| 0 | Este plan, escrito **antes** del código | ejecutor | `[x]` 2026-09-16 |
| 1 | **D1** `ruleta/config.py`: llave `juego.consuelo.peso` + validación; `config.json` con `"peso": 217` | ejecutor | `[x]` 2026-09-16 (`cargar(config.json).juego.consuelo.peso` = **217**) |
| 2 | **D2** `ruleta/inventario.py`: `peso_consuelo` y **una sola** elección ponderada; cableado en `__main__.py` y `app.py` | ejecutor | `[x]` 2026-09-16 |
| 3 | **D3** `resumen` con el consuelo en el denominador + línea del consuelo en el boleto de inventario y en `reporte` | ejecutor | `[x]` 2026-09-16 |
| 4 | **D4** Goldens nuevos, **por igualdad**, incluido el **derivado del §5.2 A** | ejecutor | `[x]` 2026-09-16 (**216 → 232** pruebas OK) |
| 5 | **D4** Mutaciones **sobre copia**, mínimo 6, **todas en rojo** | ejecutor | `[x]` 2026-09-16 (**doce**, las doce en rojo: §5) |
| 6 | **D5** Fichas nuevas y cierre con nota fechada de las que quedaron falsas | ejecutor | `[x]` 2026-09-16 (262 → **266**; F-261 **resuelta**, F-220 con nota fechada) |
| 7 | **D5** `README.md` §6 y §7; documento del evento §5.1, §5.2 y bitácora §7 | ejecutor | `[x]` 2026-09-16 |
| 8 | Revisores en paralelo, correctivo y escéptico | revisores | `[ ]` |
| 9 | Commit compuertado (conjunto de archivos del §7 de este plan) | agente de commit | `[ ]` |
| 10 | **D6** Deploy en la Pi, **sin reiniciar el inventario y sin jugar** | agente de deploy | `[ ]` |
| 11 | Verificación en vivo contra lo desplegado | verificador | `[ ]` |
| 12 | Acta, fichas de cierre y memoria | escriba / orquestador | `[ ]` |

---

## 1. Objetivo

Que el boleto de consuelo **compita en el sorteo** con un peso propio, en vez de
salir solo cuando ya no queda nada. Una sola llave nueva en `config.json`
(`juego.consuelo.peso`), **una sola** elección ponderada en el motor, y el
número visible en el inventario impreso.

**Fuera de alcance, explícitamente:** las piezas **B** (franjas horarias), **C**
(horario del evento) y **D** (esperar a que la hora esté sincronizada). Esta
fase construye **solo la A**.

---

## 2. Decisiones cerradas (no se discuten aquí; se implementan)

**D1 · Configuración.** Llave nueva **`juego.consuelo.peso`**, entero **≥ 0**.
**Por omisión `0`**, que es **exactamente el comportamiento de hoy**: el consuelo
solo sale cuando no hay ningún premio disponible. La validación va en
`ruleta/config.py` como todas las demás: tipo (lo hace `_verificar_tipos` con la
anotación `int`) y rango (mensaje en español que **nombra la llave**). En el
`config.json` del repositorio se carga **`"peso": 217`**, tal cual lo propone el
§5.2 A del documento (N = 250, la respuesta **por omisión** de la pregunta 1).
**Ninguna otra llave nueva.**

**D2 · Sorteo.** `Inventario.__init__` recibe **`peso_consuelo: int = 0`**.
`sortear(momento)` hace **UNA sola** elección ponderada entre los premios
disponibles **y** el consuelo:

- población = `disponibles + [None]`, pesos = `[p.peso …] + [peso_consuelo]`
  **cuando `peso_consuelo > 0`**;
- con `peso_consuelo == 0` se sortea **solo entre los premios**, como hoy;
- **sin premios disponibles devuelve `None` sin llamar a `choices`**, como hoy.

Los topes diarios y el stock **siguen mandando**: el consuelo **no** consume
stock ni tope, pero **sí** consume folio (como hoy).

**D3 · Resumen e inventario impreso.** Con `peso_consuelo > 0` el **denominador**
de las probabilidades **incluye al consuelo**: las de los premios bajan y aparece
la del consuelo. El boleto de inventario (`ticket.boleto_inventario`, que es
también lo que imprime `python3 -m ruleta reporte`) muestra **una línea** con el
peso del consuelo y su probabilidad **de ese momento**. Con peso `0` **esa línea
no aparece**.

**D4 · Goldens con mutaciones por copia.** Mínimo **6**, todas en rojo,
**ejecutadas de verdad** y reportadas con el test que cae. Detalle en el §5.

**D5 · Documentos.** Este plan (antes del código), fichas nuevas consecutivas,
cierre con **nota fechada** de las fichas que esta fase vuelve falsas, `README.md`
§6 y §7, y el documento del evento (§5.1, §5.2 y una línea en la bitácora del
§7).

**D6 · Deploy.** `git pull --ff-only` en la Pi, suite en la Pi, reinicio del
servicio y verificación. **NO se reinicia el inventario** (el usuario está
probando: el folio sigue) y **NO se juega**.

---

## 3. Trampas de este repositorio (un ejecutor sin contexto no las adivina)

1. **`Inventario` se construye en cuatro sitios, y solo uno es de producción.**
   Medido el 2026-09-16 con `grep -rn "Inventario(" ruleta tests`:
   - `ruleta/__main__.py:80`, dentro de `abrir_inventario(cfg, exclusivo=False)`
     — **el único de producción**. Lo usan **los seis** comandos que tocan el
     inventario: `jugar`, `vista-previa`, `reporte`, `liberar`, `reiniciar` y
     `diagnostico` (este último solo lee folio y pendientes).
   - `tests/test_app.py` (2 sitios), `tests/test_inventario.py` (9),
     `tests/test_ticket.py` (3).
   **`ruleta/app.py` NO construye ningún `Inventario`**: lo recibe ya hecho en
   `Ruleta.__init__`. La decisión D2 dice «app.py pasa `cfg.juego.consuelo.peso`
   al construir el Inventario»; el código real lo contradice, así que **el
   cableado va en `abrir_inventario`** y queda anotado como duda para el
   orquestador. **No se inventa una fábrica nueva en `app.py`.**
2. **Los goldens de `tests/test_ticket.py` anclan CUERPOS ENTEROS**, no líneas
   sueltas: `test_inventario`, `test_inventario_lista_pendientes` y
   `test_inventario_con_ancho_minimo` recorren **todas** las líneas impresas y
   comprueban que ninguna pase del ancho. Una línea nueva en
   `boleto_inventario` entra en ese recorrido: si se pasa de 48 (o de 32 en el
   ancho mínimo), **caen tres pruebas a la vez**.
3. **`tests/test_config.py` ancla `config.json` contra el DOCUMENTO**, no contra
   una copia: `TestPremiosOficialesDelEvento` **parsea el bloque ```json del
   §5.1** y compara campo por campo. El golden nuevo de esta fase hace lo mismo
   con el bloque del **§5.2 A**, así que **al editar el §5.2 no se puede añadir
   otro bloque ```json que contenga `"consuelo"`**: el golden exige que haya
   **exactamente uno**.
4. **`tests/__init__.py` hace `logging.disable(logging.CRITICAL)`**: `assertLogs`
   y `assertNoLogs` **no ven nada** (ficha **F-253**). **No se escriben goldens
   sobre mensajes de log.**
5. **`Resumen` y `ResumenPremio` son `@dataclass(frozen=True)`**: los campos
   nuevos van **al final y con valor por omisión**, o cualquier construcción
   posicional revienta.
6. **Finales de línea LF.** `.gitattributes` fija `text eol=lf` para `*.py`,
   `*.json` y `*.md`. Todo lo que esta fase escriba va en **LF**. (Ficha
   **F-248**: un SVG entró con CRLF porque `*.svg` no estaba declarado.)
7. **`python` en la PC, `python3` en la Pi.** Ver la convención de comandos.
8. **El valor por omisión del código y el de `config.json` no son el mismo
   archivo.** `ConfigConsuelo.texto` en `ruleta/config.py` todavía dice «Por hoy
   se agotaron los premios…» mientras `config.json` dice «¡Gracias por jugar!»
   (ficha **F-220**). El `peso` nuevo hereda ese patrón: **por omisión 0 en el
   código, 217 en `config.json`**, y eso es **a propósito** (un repositorio sin
   `juego.consuelo.peso` se comporta como antes de esta fase).
9. **Anclas que DERIVAN: re-grep antes de cada edición.** Los números de línea de
   este plan son del 2026-09-16 y **se mueven**. Buscar por texto:
   `grep -n "consuelo" ruleta/*.py tests/*.py README.md`,
   `grep -n "PENDIENTE A" docs/evento-2026-09-asadero-33.md`,
   `grep -n "^## F-" docs/fichas.md | tail -5`.

---

## 4. Pasos, cada uno con su criterio de aceptación

**Paso 1 · `ruleta/config.py` y `config.json` (D1).**
Campo `peso: int = 0` en `ConfigConsuelo`; en `validar()`, un `if` que rechace el
negativo con un mensaje que **nombre la llave**. En `config.json`, `"peso": 217`
dentro de `juego.consuelo`.
*Aceptación:* `cargar(config.json).juego.consuelo.peso == 217`; una config sin la
llave da `0`; `"217"` y `-1` dan `ErrorConfig` con «juego.consuelo.peso» en el
mensaje.

**Paso 2 · `ruleta/inventario.py` (D2).**
`peso_consuelo` en `__init__`, la elección única en `sortear`, el denominador en
`probabilidades`, un `probabilidad_consuelo(momento)` nuevo y los dos campos
nuevos de `Resumen`. Se corrige además la **cabecera del módulo**, que hoy
afirma «Si no hay ninguno disponible, el sorteo devuelve None (boleto de
consuelo)» — la frase que cita la ficha **F-261**.
*Aceptación:* con un `rng` falso, `sortear` pasa **exactamente**
`disponibles + [None]` y `[…pesos, 217]`; con peso 0, ni `None` ni el 217.

**Paso 3 · Cableado: `ruleta/__main__.py` y `ruleta/app.py` (D2).**
`abrir_inventario` pasa `peso_consuelo=cfg.juego.consuelo.peso`. En `app.py`, el
`log.warning("Sin premios disponibles: boleto de consuelo …")` **deja de ser
cierto** en cuanto el consuelo tiene peso: se parte en dos ramas, una para «el
sorteo cayó en el consuelo» y otra para «ya no quedan premios», que es la que
al operador le importa. En `vista-previa`, el rótulo «(sin premios disponibles)»
deja de ser cierto por lo mismo.
*Aceptación:* un golden comprueba que `abrir_inventario` **deriva** el peso del
`cfg` que recibe (dos valores distintos, dos inventarios distintos).

**Paso 4 · `ruleta/ticket.py` (D3).**
La línea del consuelo en `boleto_inventario`, solo si `peso_consuelo > 0`,
armada con `_dos_columnas` para que **nunca** pase del ancho.
*Aceptación:* la línea sale **por igualdad** a 48 columnas; a 32 columnas
también cabe; con peso 0 **no aparece**.

**Paso 5 · Goldens (D4) y mutaciones (§5).**
*Aceptación:* suite en verde con el conteo nuevo y **las doce mutaciones en
rojo**, cada una con el test que cae.

**Paso 6 · Documentos (D5).**
*Aceptación:* las probabilidades del `README.md` §7 **calculadas por el
programa**, no a mano; la pieza A marcada **CONSTRUIDA** en el §5.2 sin borrar
la propuesta; fichas nuevas consecutivas y sin repetidos.

---

## 5. Mutaciones que hay que poner en rojo (sobre copia, mínimo 6)

Se hacen **sobre una copia del repositorio**, nunca sobre el árbol de trabajo, y
se ejecutan de verdad. Cada una debe caer con **el test que dice la tabla**.

| # | Qué se muta | Dónde | Test que debe caer |
|---|---|---|---|
| M1 | `sortear` nunca añade `None` a la población | `ruleta/inventario.py` | `test_sortear_con_peso_de_consuelo_mete_none_en_la_tombola` |
| M2 | `sortear` añade `None` siempre, también con peso 0 | `ruleta/inventario.py` | `test_sin_peso_de_consuelo_la_tombola_es_solo_de_premios` |
| M3 | `probabilidades` no suma `peso_consuelo` al denominador | `ruleta/inventario.py` | `test_el_consuelo_entra_en_el_denominador_de_las_probabilidades` |
| M4 | `peso` por omisión = 217 en vez de 0 | `ruleta/config.py` | `test_consuelo_sin_peso_vale_cero` |
| M5 | se borra el rechazo del peso negativo | `ruleta/config.py` | `test_rangos` (`TestReglas`) |
| M6 | la línea del consuelo se imprime siempre | `ruleta/ticket.py` | `test_inventario_sin_peso_de_consuelo_no_menciona_el_consuelo` |
| M7 | `"peso": 217` → `117` | `config.json` | `test_config_json_lleva_el_peso_de_consuelo_del_documento` |
| M8 | `"peso": 217` → `267` **en el documento** | `docs/evento-2026-09-asadero-33.md` | `test_config_json_lleva_el_peso_de_consuelo_del_documento` |
| M9 | `abrir_inventario` no pasa `peso_consuelo` | `ruleta/__main__.py` | `test_abrir_inventario_pasa_el_peso_del_consuelo` |
| M10 | el consuelo descuenta el stock del primer premio | `ruleta/inventario.py` | `test_el_consuelo_no_toca_stock_ni_tope_pero_gasta_folio` |
| M11 | el consuelo no gasta folio | `ruleta/inventario.py` | `test_el_consuelo_no_toca_stock_ni_tope_pero_gasta_folio` |
| M12 | `probabilidad_consuelo` devuelve siempre 0 | `ruleta/inventario.py` | `test_el_consuelo_entra_en_el_denominador_de_las_probabilidades` |

**M8 es la que demuestra que el golden DERIVA** del documento y no lo transcribe:
mutando **solo el documento**, con `config.json` intacto, la suite tiene que
ponerse en rojo.

---

## 6. Prohibiciones

- **No se toca `CLAUDE.md`.**
- **No se toca `ruleta/escpos.py` ni `ruleta/hardware.py`.** El papel y los
  botones están cerrados y verificados en hardware (Fases 3 y 4a).
- **No se cambia el texto del boleto de consuelo** (`juego.consuelo.titulo` ni
  `juego.consuelo.texto`): son decisión del usuario del 2026-09-13 y están
  anclados por golden.
- **No se inventa N.** El único número que entra es **217**, que es lo que el
  §5.2 A del documento **ya trae escrito**. Si el usuario responde otra N, lo
  único que cambia es ese número, en el documento y en `config.json`.
- **No se construyen las piezas B, C ni D.**
- **No se tocan las tablas de premios del §1 ni las preguntas abiertas del §4**
  del documento del evento.
- **No se reinicia el inventario de la Pi** ni se juega en el deploy.
- **El ejecutor no commitea**, y no corre ningún `git` que modifique.

---

## 7. Conjunto de archivos permitido (compuerta del commit)

Exactamente estos, ni uno más:

```
ruleta/config.py
ruleta/inventario.py
ruleta/app.py
ruleta/ticket.py
ruleta/__main__.py
config.json
tests/test_config.py
tests/test_inventario.py
tests/test_app.py
tests/test_ticket.py
tests/test_instalacion.py
docs/planes/fase-4c-consuelo-peso.md
docs/fichas.md
README.md
docs/evento-2026-09-asadero-33.md
```

---

## 8. Deploy (D6), para el agente que lo ejecute

1. `git pull --ff-only` en `/home/asadero/ruleta`. **Lo único que puede aparecer
   sin seguimiento es `?? config.json.bak-2026-09-12`.** Si `config.json`
   aparece **modificado**, **NO se fuerza nada**: se **reporta** y se detiene
   (ahí puede haber cambios del usuario).
2. Suite en la Pi: `python3 -m unittest discover -s tests -t .` desde `~/ruleta`.
3. `sudo -n systemctl restart --no-block ruleta`.
4. Verificar `active` y `NRestarts=0`, y en el journal las dos líneas de
   arranque: `Ruleta arrancando. Premios: hielera, …` e
   `Inventario impreso (arranque)`.
5. **NO** `python3 -m ruleta reiniciar` y **NO** jugar.

---

## 9. Qué queda abierto al terminar esta fase

- **N sigue sin confirmar** (pregunta 1 del §4 del documento). Se construyó con
  **217 = 250 − 33**, la propuesta por omisión: ficha nueva **F-263**.
- **Piezas B, C y D**: franjas, horario del evento y espera de la hora
  sincronizada (fichas **F-241** y las del §5.2 del documento).
- **Fechas `desde`/`hasta`** sin cargar (**F-259**) y **reinicio del inventario**
  antes del lunes 21 (**F-243**, **F-262**).
- **Sin señal perceptible** cuando una jugada se rechaza (**F-240**, **F-256**).
