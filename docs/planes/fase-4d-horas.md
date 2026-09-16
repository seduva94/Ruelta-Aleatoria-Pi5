# Fase 4d · Los premios se reparten POR HORAS (piezas B, C y D)

Plan prescriptivo. Redactado el **2026-09-16**, **antes** de tocar una sola línea
de código. Esta fase programa las tres piezas que quedaban del documento del
evento —**B** (franjas), **C** (horario del evento) y **D** (esperar a que la
hora esté sincronizada)— y, encima de ellas, el **reparto automático del cupo
diario a lo largo de las horas**, que es lo que el usuario pidió el 2026-09-16.

**Desviación anotada del protocolo (§3 de `CLAUDE.md`):** esta fase se hace en
**una sola pasada** del ejecutor —plan, documento del evento, código, goldens,
mutaciones y docs en el mismo cambio— y el plan se commitea **junto con** el
código en vez de en un commit anterior. Motivo: **el usuario está probando el
kiosco en vivo hoy 2026-09-16** y el evento abre el **lunes 21**. Los eslabones
de revisión (lentes, escéptico, commit compuertado, deploy y verificación) **no
se saltan**: van después, como siempre.

**ESTADO GLOBAL (2026-09-16, tras el paso del ejecutor).** **PLAN, DOCUMENTO DEL
EVENTO, CÓDIGO, GOLDENS, MUTACIONES, FICHAS Y DOCS HECHOS; SIN COMMITEAR Y SIN
DESPLEGAR.** Las casillas **0 a 8** de la §0 están marcadas con su evidencia; las
**9 a 13** son de otros eslabones de la cadena. La suite pasó de **232** a
**268** pruebas en verde y **las catorce mutaciones del §5 quedaron en rojo**,
tres de ellas mutando **el documento del evento** o **`config.json`** y no el
código, que es lo que demuestra que los goldens **derivan** de verdad. **Lo que
esta fase promete sigue sin medirse contra la Pi:** hasta el Paso 12, lo único
demostrado es que en la PC el reloj reparte los premios como dice el §2 del
documento del evento.

**ESTADO GLOBAL (2026-09-16, al escribir el plan; se conserva).** **FASE 4d
ABIERTA, SIN EMPEZAR.** Árbol limpio en `main` sobre `d01a0ca` (Fase 4c, peso propio del
consuelo), `HEAD` = `origin/main`. Suite: **232 pruebas OK** en la PC
(`python -m unittest discover -s tests -t .`, medido hoy antes de empezar). En la
Pi corre `d01a0ca`; el inventario está **en uso** (el usuario prueba; el folio
**no** se reinicia en esta fase).

## Por qué existe esta fase

Dictado del usuario del **2026-09-16**, confirmado con «así va, apúntalo y lanza
la cadena»:

> **es imposible saber cuántas jugadas habrá.**

Todo el modelo del documento del evento colgaba de ese número: **N**, las jugadas
esperadas en un día, del que salía el peso del consuelo por la regla **N − 33**.
Si N no se puede saber, la regla no se puede calibrar: con N mal estimado o se
regalan los premios en la primera hora o no sale casi nada.

El usuario cambió el modelo entero: **en vez de repartir por jugadas, se reparte
por HORAS.** Cada premio tiene su cupo del día y ese cupo **se va abriendo poco a
poco** durante las once horas del evento. Si en una hora no juega nadie, la pieza
no se pierde; y si juegan doscientas personas en esa hora, tampoco salen
doscientos premios, porque **solo está liberado lo que el reloj ya abrió**.

## Fuente de verdad

`docs/evento-2026-09-asadero-33.md`. Manda sobre `config.json` y sobre este plan
(su §6, paso 1: «si los dos archivos dicen cosas distintas, gana este documento y
el otro se rehace»). **Esta fase también lo reescribe**, porque su §2 describe el
modelo viejo («el peso es el cupo, con N jugadas») que el usuario acaba de
derogar. Lo viejo **no se borra**: se conserva como nota histórica corta.

## Convención de comandos (idéntica a las Fases 1 a 4c; se repite porque muerde)

- En **esta PC** el intérprete se llama **`python`**. En la **Pi** se llama
  **`python3`**. Un `python3` tecleado en Windows abre la Tienda de Microsoft y
  se queda esperando.
- La suite se corre **desde la raíz del repositorio**:
  `python -m unittest discover -s tests -t .`
- **Un agente NO invoca el `ssh` de Git Bash.** Escribe siempre
  `/c/Windows/System32/OpenSSH/ssh.exe` con
  `-o BatchMode=yes -o ConnectTimeout=10` (ficha **F-257**).
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
| 1 | **D8** Documento del evento reescrito (§1, §2, §3, §4, §5.1, §5.2, §7) | ejecutor | `[x]` 2026-09-16 |
| 2 | **D1 D2 D4 D6** `ruleta/config.py` + `config.json`: horario, franjas, separación, espera de hora, consuelo 10 | ejecutor | `[x]` 2026-09-16 |
| 3 | **D2 D3 D4** `ruleta/inventario.py`: instantes de liberación, liberadas/disponibles, franjas, separación y persistencia | ejecutor | `[x]` 2026-09-16 |
| 4 | **D1 D6** `ruleta/app.py` + `ruleta/__main__.py`: fuera de horario, espera de la hora, cableado | ejecutor | `[x]` 2026-09-16 |
| 5 | **D5 D6** `ruleta/ticket.py`: renglón de liberación por premio y aviso de hora | ejecutor | `[x]` 2026-09-16 |
| 6 | **D9** Goldens nuevos, **por igualdad**, incluidos los **derivados del documento** | ejecutor | `[x]` 2026-09-16 (**232 → 268** pruebas OK) |
| 7 | **D9** Mutaciones **sobre copia**, mínimo 8, **todas en rojo** | ejecutor | `[x]` 2026-09-16 (**catorce**, las catorce en rojo: §5) |
| 8 | **D9** `README.md` §6 y §7 recalculados **por el programa**; fichas nuevas | ejecutor | `[x]` 2026-09-16 |
| 9 | Revisores en paralelo, correctivo y escéptico | revisores | `[ ]` |
| 10 | Commit compuertado (conjunto de archivos del §7 de este plan) | agente de commit | `[ ]` |
| 11 | Deploy en la Pi, **sin reiniciar el inventario y sin jugar** | agente de deploy | `[ ]` |
| 12 | Verificación en vivo contra lo desplegado | verificador | `[ ]` |
| 13 | Acta, fichas de cierre y memoria | escriba / orquestador | `[ ]` |

---

## 1. Objetivo

Que **el reloj**, y no el número de jugadas, reparta los premios:

1. El evento tiene **horario** (12:00 a 23:00). Fuera de él, la jugada imprime
   **boleto de consuelo**.
2. Cada premio **sin franjas** abre su cupo del día **poco a poco**: la pieza *k*
   de *tope_diario* se libera en el **punto medio** de su tramo de las once horas.
3. Los premios **con franjas** (hielera, silla, set BBQ) solo existen dentro de
   ellas, con su propio tope.
4. Dos premios **no salen seguidos**: hay una **separación mínima** de minutos
   entre dos boletos premiados.
5. El consuelo sigue compitiendo, ahora con **peso 10**, que es el que tiene
   sentido cuando lo que compite contra él son una o dos piezas liberadas.
6. Al arrancar, el kiosco **espera a que la hora esté sincronizada** (pieza D),
   porque todo lo anterior cuelga del reloj y la Pi **no tiene batería RTC**.

**Fuera de alcance, explícitamente:** las fechas `desde`/`hasta` de los premios
(ficha **F-259**; el usuario prueba **hoy 16** y con las fechas puestas no
saldría ni un premio), el reinicio del inventario (**F-243**, **F-262**) y
cualquier señal nueva de error para el personal (**F-240**, **F-256**).

---

## 2. Decisiones cerradas (no se discuten aquí; se implementan)

Todas vienen del dictado del usuario del **2026-09-16** y de las decisiones de
diseño que el orquestador cerró sobre él.

### La tabla que dictó el usuario

| # | Nombre en el boleto | Detalle | Piezas | Por día | Cuándo puede salir |
|---|---|---|---|---|---|
| 1 | HIELERA IGLOO | Premio mayor | 2 | 1 | jueves 24 y viernes 25, de 19:00 a 23:00 |
| 2 | SILLA DE PLAYA | Premio grande | 10 | 2 | una de 13:00 a 16:00 y otra de 19:00 a 22:00 |
| 3 | SET BBQ | Premio grande | 10 | 2 | una de 13:00 a 16:00 y otra de 19:00 a 22:00 |
| 4 | 3 TACOS DE PASTOR | Plato de 3 tacos de pastor | 20 | 4 | parejo de 12:00 a 23:00 |
| 5 | 2 TACOS DE PASTOR | Plato de 2 tacos de pastor | 20 | 4 | parejo de 12:00 a 23:00 |
| 6 | CERVEZA | Tecate Light, Tecate Roja o Indio | 50 | 10 | parejo de 12:00 a 23:00 |
| 7 | AGUA FRESCA | Horchata, Jamaica o Cebada | 55 | 11 | parejo de 12:00 a 23:00 |

Reglas dictadas, literales: una pieza liberada **no la gana forzosamente la
primera jugada**; las piezas **no se acumulan por adelantado**; los premios **no
deben salir seguidos**; **fuera de horario se imprime CONSUELO**; «todos los
demás deben ser de gracias por participar». Los `id` **no cambian**: `hielera`,
`silla`, `bbq`, `tacos3`, `tacos2`, `cerveza`, `agua`.

### D1 · Horario del evento (pieza C)

Llave nueva **`juego.horario`**:

```json
"horario": { "abre": "12:00", "cierra": "23:00", "fuera_de_horario": "consuelo" }
```

- Validación: `abre` y `cierra` con formato **`HH:MM`**, **`abre` < `cierra`**,
  `fuera_de_horario` ∈ `{"consuelo", "no_jugar"}`. Mensajes **en español** que
  nombren la llave.
- **Por omisión no hay horario**, y entonces todo se comporta **como hoy**: se
  juega a cualquier hora.
- Con `"consuelo"`: fuera de horario el sorteo devuelve `None` y se imprime el
  boleto de consuelo, que **consume folio** como cualquier consuelo.
- Con `"no_jugar"`: **no se imprime nada** y el log lo dice. Es la ruta que el
  documento preveía; **este evento no la usa**.

### D2 · Franjas explícitas por premio (pieza B)

Campo **opcional** `franjas` dentro de cada premio, lista de
`{ "desde_hora": "HH:MM", "hasta_hora": "HH:MM", "tope": n }`.

- Un premio **con** `franjas` **solo está disponible dentro de ellas**.
- `tope` es el máximo **de esa franja, ese día**; siguen mandando **`tope_diario`
  y `stock`**. **Cómo quedó (desviación anotada el 2026-09-16):** el programa **no
  lleva la cuenta franja por franja** —cuenta «piezas abiertas hoy menos entregadas
  hoy»—, así que lo que una franja abre y nadie gana **se arrastra a la siguiente
  franja del mismo día** y puede gastarse dentro de ella por encima de su `tope`.
  Lo único que corta es el `tope_diario`. Respetarlo al pie de la letra exigiría un
  contador por franja y por día en `estado.json`. Ficha **F-269**, abierta como
  confirmación del orquestador.
- La pieza de una franja se libera **al INICIO de la franja** cuando su `tope`
  es **1**, y **repartida parejo dentro de la franja** cuando es **mayor que 1**
  (la misma regla de **D3**, aplicada al tramo).
- En `config.json`: `hielera` con `[19:00–23:00, tope 1]`; `silla` y `bbq` con
  `[13:00–16:00, tope 1]` y `[19:00–22:00, tope 1]`.
- **Las fechas `desde`/`hasta` NO se cargan en esta fase** (ficha **F-259**).

### D3 · Reparto automático del cupo diario (premios SIN franjas)

Dentro del horario del evento, la pieza **k** (k = 1…`tope_diario`) se libera en:

```
abre + (k - 0.5) * (cierra - abre) / tope_diario
```

Puntos medios. Con 12:00–23:00: agua (11) a las 12:30, 13:30, …, 22:30; cerveza
(10) a las 12:33, 13:39, …; los tacos (4) a las 13:22, 16:07, 18:52 y 21:37.

- `liberadas(t)` = cuántos instantes de liberación **ya pasaron**.
- **Disponible para el sorteo** = `liberadas(t) − entregadas_hoy`, si es mayor
  que cero **y** queda `stock` **y** no se alcanzó `tope_diario`.
- Una pieza **liberada y no ganada sigue disponible hasta el cierre**: no se
  pierde, pero **tampoco adelanta** la siguiente.
- **Sin horario configurado**, el reparto se hace sobre el **día operativo
  completo** (`hora_inicio_dia` a `hora_inicio_dia` + 24 h), para que una
  instalación sin horario siga funcionando. **Esto cambia la conducta de un
  premio con `tope_diario` en una instalación sin horario**: antes su cupo estaba
  disponible entero desde el primer minuto del día y ahora se abre poco a poco.
  Se documenta en el `README.md` §6 y §7 y se anota como **ficha**.
- Un premio **sin `tope_diario`** no tiene nada que repartir: **no se le aplica
  el reparto** (sigue disponible siempre que tenga stock).

### D4 · Separación mínima entre premios

Llave nueva **`juego.separacion_min_entre_premios`**, en **minutos**, por omisión
**0** (= sin regla). En `config.json`: **3**.

- Si el **último boleto con premio que se imprimió** salió hace menos de esos
  minutos, la jugada **solo puede dar consuelo**.
- El instante de ese último premio se **persiste en `estado.json`** para
  sobrevivir a un reinicio, **sin romper la carga de estados viejos**: campo
  ausente = sin restricción.
- Se marca en **`confirmar()`** —el boleto salió— y no en `emitir()`.

### D5 · Peso del consuelo bajo el reparto por horas

`juego.consuelo.peso` pasa de **217** a **10**. Con una pieza de agua liberada
(peso 11) la jugada gana con **~52 %**; con solo la hielera liberada (peso 1),
**~9 %** por jugada.

El golden que **deriva** el peso del bloque del §5.2 A del documento **no se
debilita**: lo que cambia es **el bloque del documento**.

Además, el **inventario impreso** y el **reporte** muestran por premio:
**entregadas hoy / liberadas hasta ahora / próxima liberación HH:MM** (o su
franja), en texto corto que cabe en 48 columnas. La línea del consuelo se
mantiene.

### D6 · Pieza D · Hora sincronizada al arrancar

Llave nueva **`juego.espera_hora_seg`**, por omisión **0** (= no esperar). En
`config.json`: **120**.

- Al arrancar, el kiosco espera hasta ese tope a que la hora esté sincronizada,
  **comprobando cada 2 s**: existencia de `/run/systemd/timesync/synchronized`
  o, si no, `timedatectl show -p NTPSynchronized --value` == `yes`. **La que
  exista**, y **inyectable** para las pruebas.
- Si se agota el tiempo: **sigue igual**, pero imprime en el boleto de inventario
  de arranque la línea **`HORA SIN CONFIRMAR: revisar fecha`** y lo registra como
  **WARNING**.
- **Nada de esto bloquea las jugadas después del arranque.**

### D7 · Descripciones confirmadas

En `config.json`, en la tabla del §1 y en el bloque del §5.1 del documento:
`cerveza` → detalle **«Tecate Light, Tecate Roja o Indio»**; `agua` → detalle
**«Horchata, Jamaica o Cebada»**. Los demás nombres y detalles **quedan como
están**: el usuario los confirmó. Se **quita el asterisco** «a confirmar» de los
siete premios de la tabla del §1 y se anota la confirmación **con fecha**.

### D8 · Documento del evento

Se actualizan: §1 (descripciones, sin asteriscos, nota de confirmación), §2 (el
modelo ya **no** es «peso = cupo con N»: reparto por horas en lenguaje llano, con
la tabla de horas de liberación, el consuelo con peso 10 y la separación mínima;
la explicación vieja **se conserva como nota histórica corta**), §3 (franjas:
**decididas**), §4 (respondidas la 1, 2, 3, 4, 5 y 6; la **7 queda**), §5.1
(bloque de premios con las descripciones nuevas y las franjas, más un bloque de
`juego`), §5.2 (**B**, **C** y **D** construidas, con fecha y commit; **A** con
peso 10) y la bitácora del §7, más la cabecera «Última edición».

**No se inventa nada que no esté en estas decisiones.**

### D9 · Goldens y mutaciones

Funciones **puras** con **vectores reales**, **igualdad de conjuntos y de
listas**, y **mínimo 8 mutaciones por copia, todas en rojo** (§5 de este plan).
El `README.md` §7 se **recalcula con el programa**.

### D10 · Prohibiciones de higiene

**No se toca `CLAUDE.md` ni `ruleta/escpos.py`.** **Sin dependencias nuevas.**
Todo **en español**, **LF**, y los comentarios del código **citan la decisión del
usuario del 2026-09-16**. **El ejecutor no commitea** ni corre ningún `git` que
modifique.

---

## 3. Trampas de este repositorio (un ejecutor sin contexto no las adivina)

1. **Hay goldens que DERIVAN del documento del evento, no del `config.json`.**
   `tests/test_config.py::TestPremiosOficialesDelEvento` parsea los bloques
   ```` ```json ```` del documento y los compara campo por campo. Cambiar
   `config.json` sin cambiar el documento **pone la suite en rojo**, y está
   hecho a propósito. Los bloques se localizan **por su contenido**, no por el
   número de sección: si esta fase añade un bloque nuevo que también dice
   `"consuelo"`, el filtro viejo encuentra **dos** y el golden se cae. **Hay que
   afinar el filtro, no borrarlo.**
2. **`test_el_peso_del_documento_obedece_la_regla_N_menos_33…` da por cierto el
   modelo viejo.** Busca pares `N → peso` **en todo el documento** con
   `re.findall(r"(\d+)\s*→\s*(\d+)", texto)`. Con el modelo nuevo, ese test hay
   que **reescribirlo**, y además **cualquier flecha `→` entre números** que se
   escriba en el documento nuevo lo envenena. Se acota la búsqueda a la nota
   histórica.
3. **`tests/test_ticket.py` ancla CUERPOS ENTEROS por igualdad**, no fragmentos.
   `test_inventario_del_config_real_cabe_entero` compara la línea del consuelo
   **completa, con sus espacios**, y hoy da 48 columnas justas **porque el peso
   es 217**. Con peso **10** la línea es más corta y `_dos_columnas` reparte los
   espacios de otra forma: hay que **recalcular la esperada con la misma regla**,
   no aflojar el assert.
4. **`Inventario` se construye en muchos sitios de las pruebas** y en **uno solo**
   de producción: `ruleta/__main__.py::abrir_inventario`. Un censo derivado
   (`tests/test_instalacion.py::test_solo_hay_un_sitio_de_produccion_que_construye_el_inventario`)
   exige que siga habiendo **exactamente uno**. Los parámetros nuevos se cablean
   **ahí**, y hay que actualizar el golden que comprueba que los deriva del `cfg`.
5. **`python` en la PC, `python3` en la Pi.**
6. **LF siempre.** `.gitattributes` normaliza `*.py`, `*.md` y `*.json`, pero el
   árbol de trabajo en Windows puede quedar con CRLF; lo que se commitea es LF.
7. **La hora NUNCA se lee con `datetime.now()` dentro de una función pura.** El
   reloj entra por parámetro (`momento`) o por el reloj inyectable de
   `Ruleta` (`reloj=`). Es lo que permite que los goldens fijen «las 12:29».
8. **`tests/__init__.py` apaga el registro**, así que `assertLogs` no ve nada
   (ficha **F-253**): no se anclan mensajes de log, se anclan **conductas**.
9. **`Premio` es un dataclass `frozen`** y `_verificar_tipos` comprueba las
   anotaciones contra el JSON **crudo**: una lista de objetos hay que
   **convertirla antes** de verificar tipos, como ya se hace con `desde`/`hasta`.
10. **Anclas que DERIVAN: re-grep antes de cada edición.** Los números de línea
    de este plan son del 2026-09-16 y **se mueven**. Buscar por texto:
    `grep -n "tope_diario\|motivo_no_disponible" ruleta/inventario.py`,
    `grep -n "PENDIENTE" docs/evento-2026-09-asadero-33.md`,
    `grep -n "^## F-" docs/fichas.md | tail -5`.

---

## 4. Pasos, cada uno con su criterio de aceptación

**Paso 1 · Documento del evento (D7, D8).** Se escribe **antes** que el código,
porque el código **deriva** de él.
*Aceptación:* el §5.1 trae los siete premios con sus `franjas` y sus detalles
nuevos, y un bloque `"juego"` con horario, separación, espera de hora y consuelo
10; el §4 tiene marcadas las preguntas 1 a 6; el §2 explica el reparto por horas
y conserva la nota histórica.

**Paso 2 · `ruleta/config.py` y `config.json` (D1, D2, D4, D6, D7, D5).**
`ConfigHorario`, `Franja`, `Premio.franjas`, `juego.separacion_min_entre_premios`
y `juego.espera_hora_seg`, cada uno con su validación en español.
*Aceptación:* `cargar(config.json)` trae horario 12:00–23:00, separación 3,
espera 120, consuelo 10 y las cinco franjas; una hora mal escrita, un `abre`
posterior al `cierra` y un `fuera_de_horario` inventado dan `ErrorConfig` con la
llave en el mensaje.

**Paso 3 · `ruleta/inventario.py` (D2, D3, D4).** Función pura
`instantes_de_liberacion`, los instantes por premio y día, `liberadas`,
`proxima_liberacion`, el motivo nuevo de no disponible, la separación mínima en
`sortear` y el `ultimo_premio` persistido.
*Aceptación:* las listas de instantes salen **por igualdad** de `HH:MM`; a las
12:29 hay 0 aguas y a las 12:30 hay 1; a las 23:30 no hay nada; un `estado.json`
viejo (sin el campo) carga sin restricción.

**Paso 4 · `ruleta/app.py` y `ruleta/__main__.py` (D1, D6).** Fuera de horario
con `no_jugar` no se imprime; la espera de la hora con su comprobador
**inyectable**; `abrir_inventario` cablea horario y separación.
*Aceptación:* con `"no_jugar"` la app **no imprime nada**; con el comprobador
falso no/no/sí el arranque sigue a la tercera **sin** la línea de aviso.

**Paso 5 · `ruleta/ticket.py` (D5, D6).** Renglón de liberación por premio y
línea `HORA SIN CONFIRMAR: revisar fecha`.
*Aceptación:* las líneas nuevas **por igualdad**, y **ninguna** pasa de 48
columnas con el `config.json` real.

**Paso 6 · Goldens (D9) y mutaciones (§5).**
*Aceptación:* suite en verde con el conteo nuevo y **las catorce mutaciones en
rojo**, cada una con el test que dice la tabla.

**Paso 7 · `README.md` y fichas (D9).**
*Aceptación:* la tabla del §7 la **calcula el programa**, no la mano; las fichas
nuevas son consecutivas y sin repetidos.

---

## 5. Mutaciones que hay que poner en rojo (sobre copia, mínimo 8)

Se hacen **sobre una copia del repositorio**, nunca sobre el árbol de trabajo, y
se ejecutan de verdad. Cada una debe caer con **el test que dice la tabla**.

**Ejecutadas el 2026-09-16** con el arnés
`scratchpad/mutar.py`, que copia el repositorio a
`C:\Users\seduv\AppData\Local\Temp\mut4d\<Mn>` y corre la suite entera en cada
copia. **Copia limpia: 268 pruebas en verde. Las catorce mutaciones: ROJO, y en
las catorce cayó el test esperado.**

| # | Qué se muta | Dónde | Test que debe caer | Resultado |
|---|---|---|---|---|
| M1 | los instantes se reparten al **inicio** de cada tramo (`k - 1.0`) en vez del punto medio (`k - 0.5`) | `ruleta/inventario.py` | `test_instantes_de_liberacion_del_evento_real` | **ROJO** (y otros 7) |
| M2 | `liberadas` cuenta con `<` en vez de `<=`: la pieza no cuenta en su minuto exacto | `ruleta/inventario.py` | `test_liberadas_y_disponibles_a_horas_concretas` | **ROJO** (y otros 5) |
| M3 | se borra la comprobación del horario: fuera de él el premio **sigue disponible** | `ruleta/inventario.py` | `test_fuera_del_horario_no_hay_premios_y_el_sorteo_da_consuelo` | **ROJO** (y otros 2) |
| M4 | un premio con franjas está disponible **también fuera** de ellas | `ruleta/inventario.py` | `test_franjas_de_la_silla_del_evento_real` | **ROJO** (y 1 más) |
| M5 | la franja de `tope` 1 se libera en el **punto medio** y no al inicio | `ruleta/inventario.py` | `test_franjas_de_la_silla_del_evento_real` | **ROJO** (y otros 5) |
| M6 | la separación mínima **no** se aplica en `sortear` | `ruleta/inventario.py` | `test_separacion_minima_entre_premios` | **ROJO** (y 1 más) |
| M7 | el `ultimo_premio` se guarda siempre como `null` en `estado.json` | `ruleta/inventario.py` | `test_el_ultimo_premio_sobrevive_al_reinicio` | **ROJO** |
| M8 | `"fuera_de_horario": "no_jugar"` **imprime igual** | `ruleta/app.py` | `test_fuera_de_horario_con_no_jugar_no_imprime_nada` | **ROJO** |
| M9 | la espera de la hora **no reintenta**: una sola consulta y se rinde | `ruleta/app.py` | `test_arranque_espera_a_que_la_hora_se_sincronice` | **ROJO** |
| M10 | agotado el tope, el boleto de arranque **no avisa** de la hora | `ruleta/app.py` | `test_arranque_avisa_en_el_boleto_si_la_hora_no_se_confirma` | **ROJO** (y 1 más) |
| M11 | `abrir_inventario` **no** pasa el horario al motor | `ruleta/__main__.py` | `test_abrir_inventario_pasa_el_horario_y_la_separacion` | **ROJO** (y 1 más) |
| M12 | `"separacion_min_entre_premios": 3` → `0` | `config.json` | `test_config_json_lleva_el_bloque_de_juego_del_documento` | **ROJO** (y otros 3) |
| M13 | la franja de la hielera pasa a `18:00` **en el documento** | `docs/evento-2026-09-asadero-33.md` | `test_config_json_lleva_exactamente_los_premios_del_documento` | **ROJO** |
| M14 | en la tabla de la tómbola del §2, el consuelo pasa de `11 + 10 = 21 → 52.4 %` a `11 + 11 = 22 → 50.0 %` **en el documento** | `docs/evento-2026-09-asadero-33.md` | `test_las_probabilidades_del_2_las_calcula_el_programa` | **ROJO** |

**M13 y M14 son las que demuestran que los goldens DERIVAN** del documento y no
lo transcriben: mutando **solo el documento**, con `config.json` intacto, la
suite se pone en rojo. La **M12** lo demuestra por el otro lado: tocando **solo
`config.json`**, el golden del bloque `juego` del §5.1 cae.

---

## 6. Prohibiciones

- **No se toca `CLAUDE.md`.**
- **No se toca `ruleta/escpos.py`.** El papel está cerrado y verificado en
  hardware (Fase 4a).
- **No se cargan las fechas `desde`/`hasta`** de los premios: el usuario prueba
  **hoy 16** y con ellas puestas no saldría ni un premio (**F-259**).
- **No se cambian los `id`, los `stock`, los `tope_diario` ni los `peso` de los
  premios.** Son el dictado del usuario.
- **No se cambia el texto del boleto de consuelo** (`titulo` ni `texto`).
- **No se reinicia el inventario de la Pi** ni se juega en el deploy.
- **No se inventan valores.** Lo que no esté en el §2 de este plan, no entra.
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
ruleta/hardware.py
config.json
tests/test_config.py
tests/test_inventario.py
tests/test_app.py
tests/test_ticket.py
tests/test_instalacion.py
docs/planes/fase-4d-horas.md
docs/fichas.md
README.md
docs/evento-2026-09-asadero-33.md
```

---

## 8. Deploy, para el agente que lo ejecute

1. `git pull --ff-only` en `/home/asadero/ruleta`. **Lo único que puede aparecer
   sin seguimiento es `?? config.json.bak-2026-09-12`.** Si `config.json` aparece
   **modificado**, **NO se fuerza nada**: se **reporta** y se detiene.
2. Suite en la Pi: `python3 -m unittest discover -s tests -t .` desde `~/ruleta`.
3. `sudo -n systemctl restart --no-block ruleta`.
4. Verificar `active` y `NRestarts=0`, y en el journal las líneas de arranque.
   **Nuevo en esta fase:** si la hora no estaba sincronizada aparece
   `HORA SIN CONFIRMAR` como **WARNING** y la misma línea en el boleto.
5. **Cuidado con la hora de la prueba en vivo:** el 2026-09-16 el horario del
   evento ya está cargado. **Antes de las 12:00 o después de las 23:00 de
   Hermosillo, toda jugada sale de consuelo**, y eso **no es una avería**.
6. **NO** `python3 -m ruleta reiniciar` y **NO** jugar de más: la separación
   mínima de 3 minutos hace que dos jugadas seguidas **nunca** den dos premios.

---

## 9. Qué queda abierto al terminar esta fase

- **Fechas `desde`/`hasta`** sin cargar (**F-259**), obligatorias antes del
  lunes 21, y **reinicio del inventario** (**F-243**, **F-262**).
- **Pregunta 7 del §4** del documento (factor de holgura): se queda sin
  responder; con el reparto por horas ya no aplica igual y lo dice el documento.
- **Sin señal perceptible** cuando una jugada se rechaza (**F-240**, **F-256**).
- **El §5.1 del documento seguía diciendo que la Pi va sin red** (**F-266**):
  esta fase lo corrige, porque la pieza D nace justo de eso.
