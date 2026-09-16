# Fase 4b · Cargar en `config.json` los premios oficiales del evento

Plan prescriptivo **corto**. Redactado el **2026-09-15, de noche**, después de
cerrar la Fase 4a y **antes** de tocar `config.json`. Esta fase **no programa
nada**: cambia **configuración** y los documentos que la describen. Todo lo que
da por cierto está medido o citado de un archivo del repositorio; lo que no,
este plan dice que no.

**ESTADO GLOBAL (2026-09-16). FASE 4b CERRADA.** Las **doce** casillas de la §0
están marcadas. Commit **`f810bc4d039b97127670b46f9aa6b8371a8db22a`** (base
`9afdd9c`, **16** commits en `main`), con las **seis** rutas del Paso 8 y ni una
más; push verificado contra el remoto por un agente distinto del que commiteó.
Desplegado en la Pi entre las **00:10** y las **00:11** del 2026-09-16: **216
pruebas OK allá**, inventario reiniciado de **folio 16 a 00000** con sus dos
respaldos, servicio `active` con `NRestarts=0`, el journal con los **siete
premios reales** y **cero avisos de poco papel**. Acta:
`docs/actas/2026-09-16-fase-4bcd.md` (una sola acta para las Fases 4b, 4c y 4d);
hechos medidos: `docs/actas/2026-09-16-hechos-medidos-fase-4bcd.md`.

**ESTADO GLOBAL (2026-09-15, tras el paso del ejecutor; se conserva).** **CONFIGURACIÓN,
GOLDENS, MUTACIONES, FICHAS Y DOCUMENTOS HECHOS; SIN COMMITEAR Y SIN
DESPLEGAR.** Las casillas **0 a 6** de la §0 están marcadas con su evidencia; las
**7 a 11** son de otros eslabones de la cadena. La suite pasó de **214** a
**216** pruebas en verde (los dos goldens nuevos del §5.1) y **las siete
mutaciones del §5 quedaron en rojo**, dos de ellas mutando **el documento** y no
el `config.json`, que es lo que demuestra que el golden **deriva** de verdad.
**Lo que esta fase promete sigue sin medirse contra la Pi:** hasta el Paso 10, lo
único demostrado es que el `config.json` y el documento coinciden campo por campo
en la PC.

**ESTADO GLOBAL (2026-09-15, al escribir el plan; se conserva).** **FASE 4b
ABIERTA, SIN EMPEZAR.** El árbol estaba limpio en `main` sobre `9afdd9c` (cierre
documental de la Fase 4a) y la suite daba **214 pruebas OK** en la PC. En la Pi
corre el código de la Fase 4a (`2a0aba3`, papel agotado) con los **premios de
relleno `TEST 1`…`TEST 7`** y el inventario de pruebas en **folio 16**.

**Desviación menor, anotada a propósito.** El §3 del protocolo de `CLAUDE.md`
separa el commit del plan del commit del cambio. Aquí **el plan y el cambio van
en una sola pasada y en un solo commit**, por tres razones: (1) no se toca ni
una línea de código, solo configuración y documentos; (2) la fuente de verdad ya
está escrita, revisada y commiteada desde el 2026-09-13
(`docs/evento-2026-09-asadero-33.md` §5.1), así que el plan no descubre nada;
(3) el usuario quiere probar **mañana 2026-09-16** sobre la Pi y el evento abre
el **lunes 21**. Queda escrito aquí para que un verificador futuro lo lea como
una decisión y no como un descuido.

## Por qué existe esta fase

Petición del usuario del **2026-09-15 por la noche**, literal: «cambiar la Pi al
programa oficial que usaremos; haré pruebas en ese mañana para hacer algunos
cambios y que quede todo listo para el lunes».

Es decir: la Pi deja de jugar con premios de relleno y pasa a los **siete
premios reales** del documento del evento, para que **mañana** el usuario vea en
papel los nombres, los detalles y el inventario que va a usar, y corrija lo que
no le guste **antes** del lunes 21.

## Convención de comandos (idéntica a las Fases 1 a 4a; se repite porque muerde)

- En **esta PC** el intérprete se llama **`python`**. En la **Pi** se llama
  **`python3`**. Un `python3` tecleado en Windows abre la Tienda de Microsoft y
  se queda esperando.
- La suite se corre **desde la raíz del repositorio**:
  `python -m unittest discover -s tests -t .`
- **Un agente NO invoca el `ssh` de Git Bash.** Escribe siempre
  `/c/Windows/System32/OpenSSH/ssh.exe` con
  `-o BatchMode=yes -o ConnectTimeout=10`. Si el alias `ruleta` cuelga, forzar
  IPv4 con llave e IP explícitas (ficha **F-257**): la IP del punto de acceso
  **cambia** entre sesiones.
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
| 0 | Este plan escrito **antes** de tocar `config.json` | ejecutor | `[x]` 2026-09-15 |
| 1 | `config.json`: los 7 premios del §5.1, **sin** `desde`/`hasta` | ejecutor | `[x]` 2026-09-15 (suma de `stock` 167, de `tope_diario` 34) |
| 2 | Golden **derivado** del documento + goldens de relleno actualizados | ejecutor | `[x]` 2026-09-15 (**216** pruebas OK, antes 214) |
| 3 | Mutaciones sobre copia, mínimo 4, **todas en rojo** | ejecutor | `[x]` 2026-09-15 (**siete**, las siete en rojo: §5) |
| 4 | Fichas nuevas (F-259 a F-262) | ejecutor | `[x]` 2026-09-15 (258 → **262**, sin repetidos) |
| 5 | `README.md` §7, §6 y §4 (paso 6): corregir lo que ya es falso | ejecutor | `[x]` 2026-09-15 (**el §4 quedó fuera del alcance literal de D5**: se corrigió porque su paso 6 decía en presente «cambia los `test1`…`test7` por tus premios reales» y apuntaba al §7 ya corregido; se anota aquí para que el orquestador lo confirme o lo revierta) |
| 6 | Documento del evento: una línea de bitácora §7 y la cabecera | ejecutor | `[x]` 2026-09-15 |
| 7 | Revisores en paralelo, correctivo y escéptico | revisores | `[x]` 2026-09-15 (lentes **9** + **2** correcciones; escéptico **2**, las dos por sobreafirmar que el documento y `config.json` «no se pueden desincronizar») |
| 8 | Commit compuertado (conjunto de archivos del Paso 8) | agente de commit | `[x]` 2026-09-16 (**`f810bc4`**, las **seis** rutas y ni una más; push verificado: `HEAD` = `origin/main`, árbol limpio) |
| 9 | Deploy en la Pi y reinicio del inventario | agente de deploy | `[x]` 2026-09-16 00:10–00:11 (`pull` `2a0aba3` → `f810bc4`, **17** archivos según el agente de deploy —el **diff real** entre esos dos commits toca **12**, ver §3.4 del acta—; **216 OK** en la Pi; `reiniciar --si`: «Folio actual: 00016 … Respaldo: `datos/estado_20260916_001053.json` / `datos/boletos_20260916_001053.csv` … Folio en 00000.») |
| 10 | Verificación en vivo contra lo desplegado | verificador | `[x]` 2026-09-16 00:11:02 (`active`, `NRestarts=0`; journal con los siete premios reales y `Inventario impreso (arranque). Folio actual 00000`; **0** avisos de poco papel) |
| 11 | Acta, fichas de cierre y memoria | escriba / orquestador | `[x]` 2026-09-16 (`docs/actas/2026-09-16-fase-4bcd.md`, una acta para las tres fases) |

---

## 1. Objetivo

Que `config.json` lleve **exactamente** los siete premios de la tabla del §1 del
documento del evento, en la forma del bloque `"premios"` del §5.1, y que un
golden **lo derive del propio documento** para que los dos no puedan
desincronizarse en silencio.

**Lo que esta fase NO hace, a propósito:**

- **No construye las piezas A, B, C ni D** (peso del consuelo, franjas horarias,
  horario del evento, espera a que la hora esté sincronizada). Siguen pendientes
  y siguen documentadas en el §5.2 del documento del evento.
- **No carga `desde`/`hasta`** (decisión **D1**, abajo).
- **No toca ni una línea de `ruleta/`.**
- **No decide los nombres.** Los siete llevan asterisco en el documento: son
  propuesta a confirmar, y los confirma el usuario mañana.

---

## 2. Decisiones cerradas

Las tomó el orquestador antes de abrir la fase. **El ejecutor no las
reinterpreta: si el código o el documento las contradicen, se detiene y
pregunta.**

### D1 · `config.json`: los 7 premios reales, sin fechas

Se reemplaza la lista `premios` de relleno por los **siete** premios del bloque
JSON del §5.1 de `docs/evento-2026-09-asadero-33.md`, con `id`, `nombre`,
`detalle`, `stock`, `tope_diario` y `peso` **idénticos** al bloque.

**SIN los campos `desde`/`hasta` por ahora.** Razón: el bloque del documento los
trae del **21 al 25 de septiembre**, y **mañana es 16**. Con esas fechas puestas,
**ningún premio estaría disponible** y el usuario solo vería boletos de consuelo
en todas sus pruebas: exactamente lo contrario de lo que pidió. Las fechas se
cargan en la **pasada final antes del lunes** (ficha **F-259**).

**Nada más cambia en `config.json`:** `negocio`, `impresora`, `gpio` y `juego`
quedan idénticos, incluido `"led": 22` (que sigue sin LED conectado: ficha
**F-240**).

### D2 · Golden que **deriva** del documento

Un golden nuevo en `tests/test_config.py` **parsea** el bloque de código `json`
del §5.1 que contiene `"premios"`, lo convierte a lista y lo compara **por
igualdad** con los premios de `config.json` en las seis llaves de D1. Mientras
D1 omita `desde`/`hasta`, el golden los ignora **y dice en el propio test por
qué**, además de anclar que hoy están ausentes.

Se actualizan también los dos goldens que anclaban los premios de relleno
(`len == 7` y `premios[2].stock == 1`) a la tabla real, **derivando censos** en
vez de enumerar: ids en orden, suma de `stock` = 167, suma de `tope_diario` = 34.

### D3 · Este plan

Se escribe **antes** de tocar `config.json` y se commitea junto con el cambio
(desviación menor, ya anotada arriba).

### D4 · Fichas nuevas

Cuatro, con numeración consecutiva a la última existente (**re-grep antes de
escribir**, no de memoria):

- **(a)** cargar `desde`/`hasta` en la pasada final antes del lunes;
- **(b)** los nombres y detalles con asterisco quedan a confirmar por el usuario;
- **(c)** el motor actual **nunca** da consuelo mientras haya premio disponible
  (pieza A pendiente): con `peso = cupo`, **las primeras 33 jugadas del día ganan
  seguro**;
- **(d)** el inventario de pruebas (**folio 16**) se reinicia en esta fase y
  **hay que volver a reiniciarlo el lunes** antes de abrir, si mañana se juega.

### D5 · Documentos

- `README.md` §7 («Premios y probabilidades») y §6 **solo si** describen los
  premios de relleno como si fueran los actuales: se **corrigen las afirmaciones
  falsas**, no se reescribe la sección.
- `docs/evento-2026-09-asadero-33.md`: **una sola línea fechada** en la bitácora
  del §7 y la cabecera «Última edición» puesta al día. **Ninguna tabla, ningún
  cupo y ninguna probabilidad se tocan.**

### D6 · Deploy

En la Pi, en este orden y sin saltarse un paso:

1. `git status` limpio **salvo** `config.json.bak-2026-09-12` (residuo conocido).
2. `git pull --ff-only` (**nunca** un pull que fusione o rebase).
3. La suite **en la Pi**: `python3 -m unittest discover -s tests -t .`
4. `sudo -n systemctl stop ruleta`.
5. `cd /home/asadero/ruleta && python3 -m ruleta reiniciar --si`, copiando la
   salida entera: folio actual, los respaldos creados y la línea
   `Inventario reiniciado. Folio en 00000.`
6. `sudo -n systemctl start --no-block ruleta`.
7. **Desde una conexión nueva**, verificación en vivo (Paso 10).

**No se juega ni se imprime nada más.** El único papel que sale es el boleto de
inventario de arranque.

---

## 3. Trampas del repo (lo que un ejecutor sin contexto no puede adivinar)

1. **`tests/test_config.py` ancla el `config.json` real del proyecto.** Las dos
   pruebas `test_config_json_del_proyecto_*` lo cargan desde el disco
   (`Path(__file__).resolve().parent.parent / "config.json"`). Cambiar los
   premios **pone la suite en rojo** hasta que se actualicen esos goldens. Es a
   propósito: así funciona la red.
2. **El documento del evento es la fuente, no `config.json`.** Lo dice el §6
   paso 1 del propio documento: «si los dos archivos dicen cosas distintas, gana
   este documento y el otro se rehace». Un nombre que no esté en el documento
   **no se inventa**.
3. **Sin fechas por decisión, no por olvido.** Quien vea `config.json` sin
   `desde`/`hasta` y crea que falta algo: está en D1 y en la ficha **F-259**.
4. **El motor actual solo da consuelo cuando no queda ningún premio
   disponible.** Está escrito en el propio código (`ruleta/inventario.py`,
   cabecera: «Si no hay ninguno disponible, el sorteo devuelve None (boleto de
   consuelo)»). **La pieza A no existe.** Con `peso = cupo` y **34** cupos al día
   —los 33 del documento **más la hielera**, que sin `desde`/`hasta` entra todos
   los días—, **las primeras 34 jugadas del día ganan premio, una tras otra**, y
   **33** en cuanto salgan las 2 hieleras (medido el 2026-09-15 con el sorteo
   real sobre este `config.json`: 34, 34, 33, 33 y 33). Mañana, en las pruebas, eso se
   va a ver: es lo esperado, no un defecto nuevo.
5. **`peso = cupo` es la regla del documento** (§2, «La regla que propongo: el
   peso es el cupo»), no una coincidencia: los pesos del §5.1 son los cupos
   diarios. Quien toque un `peso` sin tocar el `tope_diario` rompe la cuenta del
   §2 y las tablas de probabilidad del documento.
6. **`python3 -m ruleta reiniciar` respalda `estado.json` y `boletos.csv`**, los
   dos de `datos/` (medido en `ruleta/__main__.py`, `cmd_reiniciar`). **No toca
   `ruleta.log`**, que es otro archivo (el log rotativo del programa). Además
   **se niega a correr con el servicio activo**: por eso el `stop` va antes.
7. **Finales de línea.** `.gitattributes` fija `eol=lf` para `*.md`, `*.json` y
   `*.py`. Todo lo que esta fase escriba va en **LF**.
8. **`config.json.bak-2026-09-12` existe en la Pi** y no está en el repositorio:
   `git status` allá **no** estará totalmente limpio, y eso es lo esperado.

---

## 4. Pasos, con criterio de aceptación

Cada paso dice **QUIÉN**, **QUÉ HACER**, **CRITERIO DE ACEPTACIÓN** y **SI
FALLA**.

> **Nota fechada (2026-09-16, al cerrar la fase). Los doce criterios de esta
> sección se cumplieron, y esto es lo que se midió de cada uno.** **Paso 1:**
> `git diff config.json` tocó **solo** la lista `premios`; el validador real
> carga **7** premios, con suma de `stock` **167** y suma de `tope_diario`
> **34**. **Paso 2:** suite de **214** a **216** OK, el conteo que el propio
> criterio pedía anotar. **Paso 3:** **siete** mutaciones sobre copia limpia,
> **las siete en rojo**, con el test que cae anotado en el §5; **M6 y M7 mutan el
> DOCUMENTO**, que es lo que demuestra que el golden deriva. **Paso 4:**
> `grep -c "^## F-" docs/fichas.md` subió de **258** a **262**, exactamente 4 y
> sin repetidos. **Paso 5:** ninguna afirmación en presente del `README.md` dice
> ya que el `config.json` traiga premios de prueba (re-grepeado el 2026-09-16 al
> cerrar: `TEST 1`, `test1` y `folio 16` **no aparecen**, salvo la nota fechada
> del §4 que documenta la corrección). **Paso 6:** el diff del documento del
> evento tocó **solo** la cabecera y la bitácora del §7. **Pasos 7 a 11:** lo que
> dicen las casillas 7 a 11 de la §0, con su hora y su salida.
>
> **Lo que NO se cumplió tal y como está escrito:** el **Paso 9** de este plan
> reinició el inventario a **folio 00000**, y el **Paso 10** lo verificó allí;
> pero **el usuario siguió jugando el 2026-09-16**, así que ese cero duró lo que
> duró. Cuando se desplegó la Fase 4c el folio iba en **5**. **No es un fallo del
> plan**: es el precio conocido de probar en vivo, y por eso existen las fichas
> **F-262** y **F-243**, que siguen abiertas con fecha límite el **lunes 21**.
> Evidencia de todo esto: `docs/actas/2026-09-16-fase-4bcd.md`.

### Paso 0 · Este plan · QUIÉN: ejecutor

**QUÉ HACER:** escribirlo antes de tocar `config.json`.
**CRITERIO:** el archivo existe y un ejecutor sin contexto puede seguirlo sin
preguntar nada que no esté aquí.
**SI FALLA:** no se continúa.

### Paso 1 · `config.json` · QUIÉN: ejecutor

**QUÉ HACER:** reemplazar la lista `premios` por los siete de D1.
**CRITERIO:**

- `git diff config.json` toca **solo** la lista `premios`; ninguna otra llave
  aparece en el diff.
- El archivo carga sin error y devuelve **7** premios con el validador real
  (`ruleta/config.py`).

**SI FALLA:** se corrige el JSON; no se relaja el validador.

### Paso 2 · Goldens · QUIÉN: ejecutor

**QUÉ HACER:** el golden derivado de D2 y la actualización de los dos goldens de
relleno.
**CRITERIO:** `python -m unittest discover -s tests -t .` **en verde**, con el
conteo de pruebas **anotado**: de **214** a **216** (medido el 2026-09-15).
**SI FALLA:** se arregla el golden o el `config.json`, nunca se borra el assert.

### Paso 3 · Mutaciones · QUIÉN: ejecutor

**QUÉ HACER:** las **siete** del §5, **cada una sobre una copia limpia del
repositorio**, nunca sobre el árbol de trabajo.
**CRITERIO:** **las siete en rojo**, con el nombre de la prueba que cae
anotado. Una mutación que no pone nada en rojo es un golden que no muerde.
**SI FALLA:** se refuerza el golden hasta que muerda, y se anota.

### Paso 4 · Fichas · QUIÉN: ejecutor

**QUÉ HACER:** las cuatro de D4, con el número **re-grepeado**.
**CRITERIO:** `grep -c "^## F-" docs/fichas.md` sube exactamente **4**, sin
números repetidos.

### Paso 5 · `README.md` · QUIÉN: ejecutor

**QUÉ HACER:** corregir en el §7 (y en el §6 solo si hace falta) lo que afirme
que los premios cargados son `test1`…`test7`.
**CRITERIO:** ninguna afirmación en presente del `README.md` dice que el
`config.json` del repositorio trae premios de prueba.

### Paso 6 · Documento del evento · QUIÉN: ejecutor

**QUÉ HACER:** una línea nueva en la bitácora del §7 y la cabecera «Última
edición» coherente.
**CRITERIO:** `git diff docs/evento-2026-09-asadero-33.md` toca **solo** la
cabecera y la bitácora del §7. Ninguna tabla del §1, §2 o §3 aparece en el diff.

### Paso 7 · Revisión · QUIÉN: revisores

Dos lentes en paralelo, correctivo acotado y escéptico independiente, como en
todas las fases. **Parada escrita:** solo se pide corregir por defecto de
conducta, assert que no muerde, golden en rojo o afirmación de doc falsa; lo
residual va a ficha.

### Paso 8 · Commit · QUIÉN: agente de commit

**Conjunto de archivos permitido, fijado por adelantado (exactamente seis):**

- `config.json`
- `tests/test_config.py`
- `docs/planes/fase-4b-config-oficial.md`
- `docs/fichas.md`
- `README.md`
- `docs/evento-2026-09-asadero-33.md`

**CRITERIO:** `git status --porcelain` muestra **solo** esas seis rutas; `git add`
por rutas explícitas; nada pendiente de push antes de commitear; compuerta por
conjunto de hashes (exactamente uno, igual a `HEAD`) antes del push; sin saltarse
hooks.

### Paso 9 · Deploy · QUIÉN: agente de deploy

Los siete puntos de **D6**, en ese orden.
**CRITERIO:** `git pull --ff-only` avanza sin fusionar; la suite **en la Pi** en
verde; `reiniciar --si` imprime los dos respaldos y
`Inventario reiniciado. Folio en 00000.`
**SI FALLA:** se reporta; **no se fuerza el pull** ni se resuelve un conflicto a
mano en la Pi.

### Paso 10 · Verificación en vivo · QUIÉN: verificador (agente distinto)

**Desde una conexión nueva**, contra lo desplegado:

- `systemctl is-active ruleta` da `active`, y `NRestarts=0`.
- El journal del arranque contiene, literalmente:
  - `Ruleta arrancando. Premios: hielera, silla, bbq, tacos3, tacos2, cerveza, agua`
  - `Inventario impreso (arranque). Folio actual 00000`
  - `Lista. Esperando jugadas.`
- **Cero** avisos de poco papel.
- Sale **un** boleto de inventario de arranque, con los **siete premios reales**
  y **folio 00000**.

**SI FALLA:** se reporta con la salida pegada; no se parchea en caliente.

### Paso 11 · Cierre · QUIÉN: escriba / orquestador

Acta desde el archivo de hechos medidos, fichas cerradas y memoria al día.

---

## 5. Mutaciones (la red que muerde)

Cada una **sobre una copia limpia del repositorio** (nunca sobre el árbol de
trabajo), corriendo la suite entera. **D2 pedía cuatro; el §5 de `CLAUDE.md`
pide media docena, así que se corrieron siete.** Las tres de más (M5, M6 y M7)
existen por una razón concreta: **M6 y M7 mutan el DOCUMENTO, no el
`config.json`**, y son las únicas que demuestran que el golden **deriva** del
documento en vez de comparar contra una copia escrita a mano dentro del test.

Corrida del **2026-09-15**, suite de **216** pruebas en cada copia:

| # | Mutación | Resultado | Qué cayó |
|---|---|---|---|
| **M1** | `config.json`: cambiar un `stock` (`agua` 55 → 54) | **ROJO** (2 fallos) | `TestCargar.test_config_json_del_proyecto_es_valido` · `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` |
| **M2** | `config.json`: cambiar un `nombre` (`CERVEZA` → `CHELA`) | **ROJO** (1 fallo) | `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` |
| **M3** | `config.json`: quitar un premio entero (`bbq`) | **ROJO** (2 fallos) | `TestCargar.test_config_json_del_proyecto_es_valido` · `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` |
| **M4** | `config.json`: cambiar un `peso` (`agua` 11 → 12) | **ROJO** (1 fallo) | `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` |
| **M5** | `config.json`: cambiar un `detalle` (`Una cerveza` → `Una chela`) | **ROJO** (1 fallo) | `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` |
| **M6** | **DOCUMENTO**: cambiar el `stock` del agua en el bloque del §5.1 (55 → 54) | **ROJO** (1 fallo) | `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` |
| **M7** | **DOCUMENTO**: romper la valla del bloque del §5.1 (` ```json ` → ` ```jsonc `) | **ROJO** (2 fallos) | `TestPremiosOficialesDelEvento.test_config_json_lleva_exactamente_los_premios_del_documento` · `…test_los_premios_del_config_todavia_no_traen_fechas` |

**Las siete en rojo.** Ninguna quedó verde, así que no hay golden que no muerda.

---

## 6. Prohibiciones

1. **No se toca ni una línea de `ruleta/`.** Esta fase es configuración y
   documentos. Cualquier necesidad de código es otra fase.
2. **No se toca `CLAUDE.md`.**
3. **No se inventan nombres, detalles, stocks, cupos ni pesos.** Todo sale del
   §5.1 del documento del evento, literal.
4. **No se cargan `desde`/`hasta`** en esta pasada (D1).
5. **No se fuerza el `git pull`** en la Pi, ni se resuelve un conflicto allá a
   mano.
6. **No se juega ni se imprime** nada más que el boleto de inventario de
   arranque.
7. **Ningún agente teclea credenciales.**
8. **El ejecutor no commitea.** Git que modifica, solo el agente de commit.

---

## 7. Fichas que abre esta fase

**F-259** (cargar `desde`/`hasta` antes del lunes), **F-260** (nombres y
detalles a confirmar), **F-261** (pieza A: las primeras 33 jugadas del día ganan
seguro) y **F-262** (reiniciar otra vez el inventario el lunes).

Fichas relacionadas que **siguen abiertas** y esta fase **no** cierra:
**F-240** (`"led": 22` sin LED), **F-241** (pieza D, la hora), **F-243**
(reiniciar el inventario antes del lunes; esta fase lo reinicia una vez, pero no
la cierra), **F-256** (el rechazo por falta de papel es invisible).
