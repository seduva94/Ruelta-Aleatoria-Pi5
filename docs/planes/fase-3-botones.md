# Fase 3 · Botones (JUGAR y HABILITAR) · cableado y prueba en hardware

> **AVISO: este plan se escribió DESPUÉS de ejecutar la fase, el 2026-09-15, y
> no antes.** La Fase 3 se hizo **en vivo**, con el usuario delante del hardware
> y sin plan prescriptivo previo, a petición suya («Vamos a conectar cables»).
> Es una **desviación consciente del §2 del protocolo** (`CLAUDE.md`), decidida
> por el orquestador para no dejar al usuario esperando con la Pi y los botones
> en la mano. Por tanto **este documento no manda sobre lo que ya se hizo: lo
> describe**, y solo manda hacia adelante —para quien repita el cableado, lo
> reproduzca en otra Pi o lo revise antes del evento—. Todo lo que dice está
> medido y sale de `docs/actas/2026-09-15-hechos-medidos-fase-3.md`; lo que no
> se midió, se dice que no se midió.

**ESTADO GLOBAL (2026-09-15, 12:31 hora de la Pi).** **FASE 3 CERRADA EN
HARDWARE.** Los dos botones físicos están cableados al conector de 40 pines, el
servicio `ruleta` quedó `active` con `NRestarts=0` y **se imprimieron tres
boletos con jugadas reales** (00001 TEST 4, 00002 TEST 7, 00003 TEST 6). El
cooldown de 5 s y la compuerta del botón HABILITAR quedaron demostrados en el
journal. El usuario confirmó después: «todo conectado y en su caja, probado y
funcionando».

Lo que **no** cierra esta fase y hay que hacer antes del evento está en la
bitácora de la §0 con casilla vacía: **soldar o enrollar** las patitas del
pulsador HABILITAR, decidir qué se hace con `"led": 22` sin LED físico,
**reiniciar el inventario** (`python3 -m ruleta reiniciar --si`, que al cerrar el
día iba por el **folio 10**), la **pieza D** (esperar a que la hora esté
sincronizada antes de imprimir y de aceptar jugadas) y los **dos arreglos del
camino del papel**: el aviso falso de poco papel y, sobre todo, el que descubrió
la prueba sin papel de las 13:29 —**con el rollo agotado el kiosco emite,
descuenta y da por impreso un boleto que no sale** (fichas **F-091** y
**F-250**)—.

- **Acta de esta fase:** `docs/actas/2026-09-15-fase-3.md`.
- **Hechos medidos (copia literal):** `docs/actas/2026-09-15-hechos-medidos-fase-3.md`.
- **Diagrama de cableado:** `docs/cableado-botones.svg` (se abre con doble clic
  en cualquier navegador y se puede imprimir).
- **Fase anterior:** `docs/planes/fase-2-impresora.md` y `docs/actas/2026-09-11-fase-2.md`.
- **Documento del evento:** `docs/evento-2026-09-asadero-33.md`.

---

## 0. Bitácora

`[x]` = hecho **y** con su criterio de aceptación cumplido, con la hora medida
del reloj de la Pi (`America/Hermosillo`). `[ ]` = pendiente. Las casillas de
abajo se marcaron con la evidencia del archivo de hechos del 2026-09-15, nunca
de memoria.

| Nº | Paso | Quién | Estado | Hora / fecha | Evidencia |
|---|---|---|---|---|---|
| 1 | Detener el servicio `ruleta` antes de tocar los pines | agente | [x] | 11:47:03 | El servicio recibió `SIGTERM`. Medido a la vez: `is-enabled` → `enabled` (**no** se deshabilitó; ver §5 trampa 8 y las desviaciones del acta) |
| 2 | Monitor de los dos pines en reposo | agente | [x] | 11:56:24 y 12:02:20 | `/tmp/monitor-botones.py` (`Button` 17 y 27 con `pull_up`, LED 22 en `blink`): reposo `jugar=False habilitar=False`, y tres lecturas directas también `False/False` |
| 3 | Comprobar el botón JUGAR | usuario + agente | [x] | 12:04:16–12:04:36 y 12:05:42–12:06:02 | Pulsaciones registradas en **GPIO 17 (pin 11)**. Ninguna en GPIO 27 |
| 4 | Comprobar el botón HABILITAR — **falló** | usuario + agente | [x] | 12:06:00–12:09 | El usuario pulsó HABILITAR tres veces y **no entró nada**. La primera hipótesis (que HABILITAR estuviera en el pin 11) resultó **falsa** |
| 5 | Escáner de los GPIO libres, **todos como entrada** | agente | [x] | 12:11:08 | `/tmp/scan-pines.py` con 17 GPIO como entrada pull-up y **ningún pin como salida**: reposo todos `False`; 12:14:37 JUGAR → GPIO 17; tres pulsaciones de HABILITAR → nada |
| 6 | Prueba de juntar los dos cables de HABILITAR | usuario | [x] | 12:20 | Nada en los 17 pines vigilados: el problema no era el botón, era dónde iban los cables |
| 7 | Escáner ampliado a GPIO 2–27 y pruebas cruzadas | agente | [x] | 12:20:55–12:24:56 | 26 pines vigilados. Tocando el cable contra la señal o la tierra buena del microswitch de JUGAR salió «GPIO 11 (pin físico 23) presionado», y **GPIO 11 quedó en bajo continuo** (`pinctrl get 11` → `lo`) |
| 8 | Diagnóstico: el negro de HABILITAR estaba en el pin 23, no en el 25 | agente | [x] | 12:24:56 | El pin 23 es **GPIO 11**, una fila arriba del pin 25 (GND). Coincide con la foto del header que mandó el usuario |
| 9 | Mover el cable negro al pin 25 (GND) | usuario | [x] | 12:28:47 | A los ocho segundos el escáner ya registraba pulsaciones |
| 10 | Comprobar HABILITAR ya bien cableado | usuario + agente | [x] | 12:28:55–12:29:17 | Pulsaciones en **GPIO 27 (pin 13)** y el gesto combinado HABILITAR sostenido + JUGAR a las 12:29:09, :13 y :15 |
| 11 | Arrancar el servicio | agente | [x] | 12:29:57 | `sudo systemctl start --no-block ruleta` → `active`, `NRestarts=0`, journal con `GPIO listo: jugar=17 habilitar=27 led=22`, inventario de arranque impreso (folio 00000) y `Lista` |
| 12 | Jugadas reales con los botones, con boleto en papel | usuario | [x] | 12:30:25 / 12:30:32 / 12:30:38 | Boletos **00001 TEST 4**, **00002 TEST 7** y **00003 TEST 6** |
| 13 | Cooldown de 5 s demostrado | usuario + agente | [x] | entre las tres jugadas | En el journal: `Pulsación ignorada: faltan 2.0 s de espera` |
| 14 | Compuerta del mesero demostrada | usuario + agente | [x] | 12:30:42–12:30:47 | Nueve veces `Pulsación ignorada: el botón HABILITAR no está presionado` |
| 15 | Diagrama de cableado verificado e incorporado al repositorio | agente + ejecutor | [x] | 2026-09-15 | SVG generado en el scratchpad y **verificado por un agente** contra el pinout oficial J8, `config.json` y el README §2 (una corrección: etiquetas de los pines 11 y 13 encimadas). Copiado a `docs/cableado-botones.svg` |
| 16 | Cierre documental: plan retroactivo, acta, fichas, README y documento del evento | ejecutor | [x] | 2026-09-15 | Este documento, `docs/actas/2026-09-15-fase-3.md`, las fichas **F-239** a **F-250** y las notas del README §2 |
| 17 | **Soldar o enrollar** el cobre de las patitas del pulsador HABILITAR | usuario | [ ] | | Hoy las patitas delgadas van metidas en terminales de crimpar tipo cuchilla, que son para cuchillas anchas: funciona, pero el contacto es precario (ficha **F-239**) |
| 18 | Decidir qué se hace con `"led": 22` sin LED físico | usuario | [ ] | | O se pone `"led": null`, o se conecta un LED de verdad, o se deja como está a sabiendas (ficha **F-240**) |
| 19 | **Reiniciar el inventario antes del lunes 21** | usuario o agente | [ ] | | Las pruebas del día dejaron `estado.json` en el **folio 10** (`test4`=1, `test7`=4, `test6`=3, `test5`=2): `python3 -m ruleta reiniciar --si` (ficha **F-243**) |
| 20 | **Pieza D**: esperar a que la hora esté sincronizada antes de imprimir y de aceptar jugadas | fase de programación aparte | [ ] | | Sale de la decisión del usuario de ir **sin batería RTC y con internet del asadero** (ficha **F-241**) |
| 21 | Arreglo del **aviso falso de poco papel** | fase de programación aparte | [ ] | | Diagnóstico cerrado el 2026-09-13; el arreglo espera autorización del usuario. **No se tocó en esta fase** |
| 21-bis | **Prueba deliberada SIN PAPEL** | usuario + agente | [x] | 13:29:17 | Se ejerció por fin el camino que la **F-091** llevaba desde el 2026-09-11 sin probar, **y falló**: el boleto 00009 se emitió, se descontó el premio y se dio por impreso **sin que saliera papel**. Ver §7.7 |
| 21-ter | **Arreglo de la consulta de papel: leer la respuesta FRESCA** | fase de programación aparte (Fase 4) | [ ] | | Sale de la fila 21-bis. Espera autorización del usuario (ficha **F-250**) |
| 22 | Actualizar el «Contexto del producto» de `CLAUDE.md` (hoy dice «sin red» y «batería RTC necesaria») | **orquestador** | [ ] | | `CLAUDE.md` está **fuera** del conjunto de archivos que esta fase podía tocar (ficha **F-242**) |

---

## 1. Objetivo y alcance

**Objetivo.** Dejar los dos botones físicos del kiosco —**JUGAR**, que aprieta el
cliente, y **HABILITAR**, que mantiene presionado el mesero— cableados al
conector de 40 pines de la Raspberry Pi 5 y **demostrados con jugadas reales que
imprimen boleto en papel**.

**Dentro del alcance:**

- Cablear los dos botones contra los GPIO que ya están en `config.json`.
- Diagnosticar y corregir los errores de cableado con **herramientas de solo
  lectura de pines** (entradas, nunca salidas).
- Arrancar el servicio y comprobar en el journal: sorteo, impresión, cooldown y
  compuerta del mesero.
- Dejar el diagrama, el acta, las fichas y este plan.

**Fuera del alcance, y no se tocó nada de esto:**

- Cualquier cambio de **código**, de `config.json` o de los **tests**. Esta fase
  no escribió ni una línea de programa.
- El **LED**: no hay LED físico conectado.
- El **arreglo del camino del papel**: ni el aviso falso de poco papel —con su
  diagnóstico cerrado desde el 2026-09-13— ni el fallo que la prueba de las 13:29
  puso en evidencia (§7.7). Los dos son código y los dos esperan la autorización
  del usuario. Esta fase los **mide y los documenta**; no los toca.
- Los **premios reales**, el logo y el horario del evento: eso es la Fase 4 y el
  documento del evento.

---

## 2. Decisiones cerradas

Ya están tomadas. **Solo el usuario puede cambiarlas.** Un ejecutor que crea que
alguna está mal **se detiene y pregunta; no improvisa** (§10).

**D1 · Los números de GPIO los manda `config.json`, no el cable.** JUGAR es
**GPIO 17** y HABILITAR es **GPIO 27**, tal como están hoy en la sección `gpio`
del `config.json` del repositorio. Si un cable no llega, **se mueve el cable**;
no se edita la configuración para acomodarlo.
*Por qué:* el `config.json` del repositorio y el de la Pi tienen que ser el mismo
archivo —esa es la regla que cerró la Fase 2—, y cambiar un pin obliga a tocar el
repositorio, a desplegar y a volver a verificar. El header tiene pines de sobra.

**D2 · La tierra puede ser cualquier pin GND; en la instalación real son el 9 y
el 25.** Medido el 2026-09-15: el microswitch de JUGAR lleva **NO → pin 11
(GPIO 17)** y **COM → pin 9 (GND)**; el pulsador de HABILITAR lleva **señal →
pin 13 (GPIO 27)** y **negro → pin 25 (GND)**. Los ocho pines GND del conector
(6, 9, 14, 20, 25, 30, 34 y 39) son intercambiables.
*Por qué el 25 y no el 14, que es el que sugería el README:* así quedó
físicamente, y funciona. Todos los pines usados están en la **fila interior**
(los impares), que es lo que hace el cableado fácil de mirar y de contar.

**D3 · Esta fase va SIN LED.** No hay ningún LED conectado a la Pi. `config.json`
sigue diciendo `"led": 22`, y **eso no rompe nada**: `gpiozero` crea el objeto
`LED(22)` sin que haya nada enchufado en el pin 15, y el servicio arrancó
`active` con `GPIO listo: jugar=17 habilitar=27 led=22`.
*Consecuencia:* hoy el programa cree que tiene LED y no lo tiene, así que la
retroalimentación al mesero es **solo el papel y el zumbador**. La decisión entre
poner `"led": null`, conectar un LED de verdad o dejarlo así **es del usuario** y
está pendiente (ficha **F-240**).

**D4 · Antes de tocar los pines, el servicio se detiene.** Es la receta que la
Fase 2 dejó escrita (ficha **F-185**) y se cumplió: `SIGTERM` a las 11:47:03.
*Por qué:* con el servicio arriba y los botones cableados, **cada pulsación de
prueba gasta papel y consume un folio**.
*Lo que NO se hizo, y el acta lo dice:* el servicio **no se deshabilitó**
(`is-enabled` → `enabled` durante toda la sesión). Como la Pi no se apagó, el
arranque automático no llegó a molestar; si alguien **apaga** la Pi para cablear,
tiene que hacer también `sudo systemctl disable ruleta`, y `enable` al volver.

**D5 · Los escáneres de diagnóstico usan SOLO entradas. Nunca una salida.**
*Por qué:* el monitor inicial ponía **GPIO 22 como salida** (el LED). Con un
botón mal cableado en el **pin 15** —que es justo el de GPIO 22— habría habido un
**cortocircuito**: un pin de salida en alto conectado a tierra a través de un
botón es exactamente eso. Los escáneres del 2026-09-15 (`scan-pines.py`) no
declararon ni un solo pin como salida, a propósito.

**D6 · No habrá batería RTC. La Pi llevará el internet del asadero durante el
evento.** **Decisión del usuario, 2026-09-15:** no consigue la batería a tiempo.
*Qué cubre:* al arrancar, la Pi tiene red y **NTP le pone la hora**. Se midió
ese mismo día: la Pi arrancó a las **11:44:42** con el reloj en «Sep 13 17:09» y
**NTP no lo corrigió hasta las 11:47** —tres minutos con la fecha falsa, que es
lo que se ve en el journal—.
*Riesgo aceptado, escrito con todas sus letras:* en esos primeros minutos —los
**tres** que se midieron ese día, no uno— los boletos salen con **fecha vieja**, el «día operativo» se cuenta mal —los topes diarios y
los `desde`/`hasta` del evento dependen de la fecha— y el boleto de inventario de
arranque se imprime con una fecha que no es.
*Mitigación pendiente (**pieza D**, ficha **F-241**):* que el programa **espere
hasta unos 2 minutos** a que la hora esté sincronizada antes de imprimir el
inventario y antes de aceptar jugadas, y que **avise en el boleto** si no lo
consiguió.
*Regla práctica mientras la pieza D no exista:* **encender la Pi unos minutos
antes de abrir y mirar la fecha del boleto de inventario.**
*Ojo:* esta decisión **contradice** lo que dicen hoy el «Contexto del producto»
de `CLAUDE.md` y varios sitios del README («en producción la Pi va sin red», «la
batería RTC es necesaria»). El README se corrigió en esta misma pasada;
`CLAUDE.md` **lo actualiza el orquestador**, porque está fuera del conjunto de
archivos permitido (ficha **F-242**).

**D7 · El camino del papel se mide, pero no se arregla en esta fase.** El aviso
falso de «poco papel» sigue apareciendo en cada arranque. Su diagnóstico está
cerrado desde el 2026-09-13 —la impresora repite el último byte de estado y el
programa lee la respuesta a la **pregunta anterior**; la máscara es de un solo
bit— y el **arreglo de código espera autorización del usuario**.
*Lo que la tarde del 2026-09-15 añadió:* la prueba sin papel de las 13:29 demostró
que ese mismo desfase **derrota también a las dos guardias** —«sin papel» y
«fuera de línea»— y que **con el rollo agotado el kiosco emite el boleto,
descuenta el premio y lo da por impreso sin que salga papel** (§7.7, fichas
**F-091** y **F-250**). Sigue sin tocarse aquí: es código, y es de la Fase 4.

**D8 · El header se toca con la Pi apagada y sin corriente** (es lo que dice el
aviso 1 del propio diagrama).
*Lo que pasó de verdad, y por eso esto es una advertencia y no un acta:* el
2026-09-15 el cable negro se movió **a las 12:28:47 con la Pi en marcha**. Se
sabe porque el archivo de hechos registra **un solo arranque**, el de las
11:44:42 (`uptime -s`), y a las 12:28:55 —ocho segundos después— el escáner
seguía corriendo y registró la pulsación: no hubo reinicio en medio. Salió bien;
no es la manera de hacerlo.

---

## 3. Material

| Pieza | Lo que se usó el 2026-09-15 |
|---|---|
| Botón JUGAR | **Botón arcade amarillo** con microswitch de cuchillas. Dos cables, verde/teal y negro, con terminales de crimpar |
| Botón HABILITAR | **Pulsador chico metálico de tapa roja**, con **dos patitas delgadas**. Cables azul y negro, con terminales de crimpar **tipo cuchilla** — y ahí está el problema: son para cuchillas anchas (§5, trampa 4) |
| LED | **Ninguno** (D3) |
| Cables al header | Las terminales de crimpar, directamente sobre los pines |

---

## 4. Pasos, para quien repita el cableado

Escritos hacia adelante, con el orden que de verdad funcionó. Cada paso dice
**QUIÉN**, **QUÉ HACER** y **CRITERIO DE ACEPTACIÓN**.

### Paso 1 · Parar el kiosco

- **QUIÉN:** agente.
- **QUÉ HACER:** `sudo systemctl stop ruleta`. Si además se va a **apagar** la
  Pi para cablear, `sudo systemctl disable ruleta` (y `enable` al terminar).
- **CRITERIO:** `systemctl is-active ruleta` → `inactive`.

### Paso 2 · Cablear los dos botones

- **QUIÉN:** usuario, con la Pi apagada y sin corriente (D8).
- **QUÉ HACER:** seguir `docs/cableado-botones.svg`:
  - JUGAR: **NO → pin 11 (GPIO 17)** y **COM → pin 9 (GND)**. El contacto **NC**
    del microswitch **no se conecta**.
  - HABILITAR: **señal → pin 13 (GPIO 27)** y el otro cable **→ pin 25 (GND)**.
- **CRITERIO:** los cuatro cables en pines de la **fila interior** (los impares),
  y **ninguno** en los pines 1, 2, 4 ni 17, que son alimentación.

### Paso 3 · Comprobar los pines sin arrancar el kiosco

- **QUIÉN:** agente.
- **QUÉ HACER:** un escáner que declare **todos los pines como entrada con
  pull-up** y registre los flancos (D5). Primero en reposo, después pidiendo al
  usuario que pulse **un botón a la vez, diciendo cuál**.
- **CRITERIO:** en reposo, **todos** los pines leídos en `False`; JUGAR aparece
  **solo** en GPIO 17 y HABILITAR **solo** en GPIO 27.
- **SI FALLA:** ampliar el escáner a **todos** los GPIO 2–27 y hacer **pruebas
  cruzadas**: tocar el cable sospechoso contra la tierra o la señal *buena* del
  otro botón. Así salió el fallo de esta fase. Un pin que se queda en **bajo
  continuo** (`pinctrl get <n>` → `lo`) con todos los botones sueltos es un cable
  de tierra metido en un GPIO.

### Paso 4 · Arrancar el servicio y jugar de verdad

- **QUIÉN:** el agente arranca, el usuario pulsa.
- **QUÉ HACER:** `sudo systemctl start --no-block ruleta` y mirar el journal.
  **Cada pulsación imprime un boleto y gasta un folio**: para probar sin gastar,
  `python3 -m ruleta --impresora vista`.
- **CRITERIO:** los cuatro primeros de la §7.

### Paso 5 · Cierre

- **QUIÉN:** ejecutor y orquestador.
- **QUÉ HACER:** acta desde el archivo de hechos, fichas de lo residual, plan al
  día y **reiniciar el inventario** antes del evento.
- **CRITERIO:** §7.5 y §7.8, y las casillas 17 a 22 de la bitácora.

---

## 5. Trampas del entorno, de la sesión y del repositorio

Cosas que un ejecutor sin contexto **no puede adivinar**. Las siete primeras se
midieron el 2026-09-15; las cuatro últimas son del repositorio.

1. **`pkill -f "<patrón>"` dentro de un `ssh 'bash -c ...'` cuyo propio comando
   contiene el patrón literal SE MATA A SÍ MISMO.** El `bash` remoto coincide con
   el patrón, muere, y nada de lo que venía detrás se ejecuta. **Pasó tres
   veces** esa mañana. Salida: escribir el patrón como `[p]ython3` —los corchetes
   impiden que coincida consigo mismo— y **no repetir la ruta literal** en el
   mismo comando, sino guardarla en una variable (`M=...`).
2. **Un proceso lanzado por SSH en segundo plano deja la sesión colgada hasta el
   timeout**, aunque se use `setsid` + `nohup` + redirección de las tres salidas.
   **El proceso sí sobrevive**: la manera de comprobarlo es **abrir una conexión
   nueva** y mirar su archivo de log, no esperar a que la primera devuelva el
   control.
3. **Los escáneres de diagnóstico deben declarar SOLO entradas.** El monitor
   inicial ponía **GPIO 22 como salida** (el LED). Con un botón mal cableado en
   el **pin 15** eso es un **corto** (decisión D5).
4. **Las terminales de crimpar tipo cuchilla no sujetan patitas delgadas.** Las
   del pulsador de HABILITAR son delgadas y las terminales son para cuchillas
   anchas: el contacto **funcionó, pero es precario**. Hay que **soldar o
   enrollar el cobre** antes del evento (ficha **F-239**).
5. **El registro de un monitor no sabe qué botón CREE el usuario que está
   pulsando.** La hipótesis inicial fue «HABILITAR está en el pin 11», y quedó
   descartada enseguida, a las 12:07–12:09; lo que costó veinte minutos fue
   encontrar dónde estaba de verdad el cable. Lo que lo resolvió fueron las
   **pruebas cruzadas**: tocar un cable contra la tierra o la señal buena del
   *otro* botón, que sí dicen dónde está conectada cada cosa.
6. **Un cable de tierra metido en un GPIO se ve como un pin en bajo continuo.**
   El negro de HABILITAR estaba en el **pin 23 = GPIO 11**, una fila arriba del
   **pin 25 = GND**. Síntoma exacto: `pinctrl get 11` → `lo` con todos los
   botones sueltos.
7. **`/tmp` de la Pi es `tmpfs`: lo que se deja ahí desaparece al reiniciar.** Al
   cerrar la sesión quedaron `monitor-botones.py`, `.log` y `.out`, y
   `scan-pines.py`, `.log` y `.out`. No hay que borrarlos a mano, pero **tampoco
   se puede contar con ellos** como evidencia: lo que importe se copia al
   repositorio.
8. **La Fase 2 dejó el servicio `active` Y `enabled`** (ficha **F-185**), así que
   **la Pi arranca el kiosco sola cada vez que se enciende**. Detenerlo no basta
   si se va a apagar la Pi: hace falta `disable`.
9. **En esta PC el intérprete se llama `python`, no `python3`.** La suite se
   corre con `python -m unittest discover -s tests -t .` desde la raíz del
   repositorio. En la Pi sí es `python3`, y `python3 -m ruleta` **solo funciona
   desde `~/ruleta`**.
10. **`.gitattributes` no dice nada de `*.svg`**, y `core.autocrlf` está en
    `true` en esta PC. El diagrama se copió **byte a byte** (18 638 bytes,
    sha256 `b238da27…`, con finales de línea CRLF), pero **git normalizará esos
    CRLF a LF al guardarlo**. Para el SVG da igual —se dibuja idéntico—, pero
    quien compare hashes tiene que saberlo (ficha **F-248**, hermana de la
    **F-219**, la de `logo.png`).
11. **Muchas fichas antiguas remiten «a la Fase 3» para arreglos de CÓDIGO**
    (rechazar rutas inexistentes bajo `/dev/`, distinguir «papel: no contestó»
    de «papel: hay», los `beep`, los valores por defecto duplicados…). **La Fase
    3 que se ejecutó fue solo de cableado**: ninguna de esas fichas se resolvió
    aquí y **ninguna se cerró** (ficha **F-249**).

---

## 6. Mapa de anclas que derivan

Textos del repositorio de los que depende este plan, con la línea donde estaban
**el 2026-09-15**, medidas con `grep -n` **después** de las ediciones de esta
misma pasada (el árbol de trabajo sobre el commit
`c7b5aa07ea2122800c7cc3b213f9ed775576e600`, que era `HEAD` = `origin/main` al
empezar): son las líneas que verá quien lea el repositorio después del commit
de esta fase, no las de antes.
**Re-grep antes de cada edición**: si el texto ya no está donde dice esta tabla,
**detenerse y preguntar**, porque significa que alguien cambió el repositorio y
el plan quedó viejo.

| Ancla | Cómo encontrarla | Por qué deriva |
|---|---|---|
| Sección 2 del README, «Conexión eléctrica» | `grep -n "^## 2. Conexión eléctrica" README.md` → **33** | Es el texto que el usuario lee para cablear. Aquí se le añadieron el enlace al diagrama y las tres notas de esta fase |
| Tabla de pines del README | `grep -n "GPIO 17\|GPIO 27\|GPIO 22" README.md` → **44** (JUGAR), **45** (HABILITAR) y **46** (LED); la cuarta línea que devuelve, la **69**, es la nota nueva de esta fase | La fila de HABILITAR decía «GND (pin 9 o 14)» y la instalación real usa el **pin 25**. No era falso —cualquier GND sirve— pero no describía lo instalado |
| Los tres pines en `config.json` | `grep -n '"boton_jugar"\|"boton_habilitar"\|"led"' config.json` → **42**, **43** y **44** (`17`, `27`, `22`) | **Mandan sobre el cable** (D1). Que `"led"` siga siendo `22` sin LED físico es lo que discute la ficha **F-240** |
| Resto de la sección `gpio` | `grep -n '"modo_habilitar"\|"pull_up"\|"rebote_ms"\|"pulsacion_larga_seg"' config.json` → **45-48** | `"mantener"` es lo que obliga al mesero a **sostener** HABILITAR; `pull_up: true` es lo que permite cablear contra GND sin resistencias |
| Cooldown entre jugadas | `grep -n '"espera_entre_jugadas_seg"' config.json` → **52** (`5.0`) | Son los 5 s que el journal demostró con `faltan 2.0 s de espera` |
| Clase `EntradasGPIO` completa | `grep -n "class EntradasGPIO" ruleta/hardware.py` → **70** | De su cuerpo sale todo lo que este plan da por cierto sobre el hardware |
| Construcción de los tres objetos de `gpiozero` | `grep -n "Button(\|LED(" ruleta/hardware.py` → **79**, **80** y **81** | Las tres líneas reales: `self._jugar = Button(pin_jugar, pull_up=pull_up)`; `self._habilitar = Button(pin_habilitar, pull_up=pull_up) if pin_habilitar is not None else None`; `self._led = LED(pin_led) if pin_led is not None else None`. **Ahí se ve por qué no falla sin LED físico** (D3): se construye el objeto y no se comprueba nada |
| Mensaje de arranque del GPIO | `grep -n "GPIO listo" ruleta/hardware.py` → **83** | Es literalmente el golden de la §7.1: `log.info("GPIO listo: jugar=%s habilitar=%s led=%s", …)` |
| `habilitar_presionado` cuando no hay botón | `grep -n "def habilitar_presionado" -A 4 ruleta/hardware.py` → **tres** coincidencias: **32** (la clase base abstracta), **88-91** (la de `EntradasGPIO`, que es la que manda en la Pi) y **167** (la simulada). La de esta fila es la de **88** | Si `boton_habilitar` fuera `null`, **devuelve `True` siempre** y la compuerta del mesero desaparecería. Por eso D1 no permite tocar ese valor a la ligera |
| Dónde se construye `EntradasGPIO` | `grep -n "EntradasGPIO(" ruleta/__main__.py` → **128** | Le pasa `cfg.gpio.boton_jugar`, `cfg.gpio.boton_habilitar` y `cfg.gpio.led` tal cual salen del `config.json` |
| Validación de los pines | `grep -n "pines = \[" -A 10 ruleta/config.py` → **313** | Acepta 0-27 (numeración BCM), rechaza repetidos y admite `None` en `led` y en `boton_habilitar`. **`led: null` es legal**; `boton_habilitar: null` solo con `modo_habilitar: "siempre"` (líneas 311-312) |
| Los dos mensajes de pulsación ignorada | `grep -n "Pulsación ignorada" ruleta/app.py` → **177** (HABILITAR suelto) y **181** (cooldown) | Son los goldens §7.3 y §7.4, y los dos salieron en el journal |
| Mensajes de arranque del servicio | `grep -n "Lista. Esperando jugadas.\|Inventario impreso" ruleta/app.py` → **117** y **270** | Goldens §7.1: salieron a las 12:29:57 |
| Lo que la Fase 2 le encargó a la Fase 3 | `grep -n "^### Fase 3 · Botones y LED" docs/planes/fase-2-impresora.md` → **2741** | De ahí vienen la receta del `stop` + `disable` y los dos avisos sobre gastar papel y folio |
| Las tres piezas que faltan para el evento | `grep -n "^### Tres cosas que el programa TODAVÍA NO SABE HACER" docs/evento-2026-09-asadero-33.md` → **30** | A (peso del consuelo), B (franjas) y C (horario del evento). **La pieza D de esta fase —esperar la hora— se anotó en la bitácora del §7 de ese documento, no en esa tabla**: la tabla es del dictado del usuario y no se toca |

---

## 7. Criterios de aceptación de la fase

La fase está cerrada cuando **todos** estos criterios se cumplen. Los cuatro
primeros se midieron el 2026-09-15 y están **en verde**. El **§7.5** tiene
casilla abierta —falta reiniciar el inventario— y el **§7.7 salió en rojo**: es
la prueba sin papel, y su arreglo es de la Fase 4. Ninguno de los dos bloquea el
cierre de esta fase, porque **ninguno es cableado**; los dos están en la bitácora
con nombre y ficha.

### 7.1 El servicio arranca y ve los tres pines

```
sudo systemctl start --no-block ruleta
systemctl is-active ruleta          # active
systemctl show -p NRestarts ruleta  # NRestarts=0
journalctl -u ruleta | grep "GPIO listo"
# GPIO listo: jugar=17 habilitar=27 led=22
```

**Medido a las 12:29:57:** `active`, `NRestarts=0`, la línea de `GPIO listo`, el
inventario de arranque impreso con **folio 00000** y `Lista`.

### 7.2 Tres jugadas reales imprimen tres boletos

**Medido:** **00001 TEST 4** a las 12:30:25, **00002 TEST 7** a las 12:30:32 y
**00003 TEST 6** a las 12:30:38, **con los botones físicos** y papel en la mano.

### 7.3 El cooldown de 5 s muerde

**Medido:** entre las tres jugadas, `Pulsación ignorada: faltan 2.0 s de espera`.

### 7.4 La compuerta del mesero muerde

**Medido:** entre las 12:30:42 y las 12:30:47, **nueve** líneas
`Pulsación ignorada: el botón HABILITAR no está presionado`.

### 7.5 El inventario queda en cero antes del evento

Las tres jugadas de las 12:30 dejaron `estado.json` con **folio 3**, `test4`,
`test7` y `test6` entregados una vez cada uno y `boletos_por_dia` del 2026-09-15
en **3**; y `boletos.csv` con **6 líneas** (`emitido` + `impreso` por cada
boleto). **Al cerrar el día, después de la tarde de juego y de la prueba sin
papel, el estado real era folio 10**, con `test4`=1, `test7`=4, `test6`=3 y
`test5`=2.

```
sudo systemctl stop ruleta
python3 -m ruleta reiniciar --si
sudo systemctl start ruleta
```

**Pendiente** (casilla 19 de la bitácora, ficha **F-243**). Sin esto, los tres
boletos de prueba cuentan como premios ya entregados el día del evento.

### 7.6 El camino «sin papel», por fin ejercido — y en rojo

Ver §7.7. Se incluye aquí como criterio porque **es la única medición de esta
fase que salió mal**, y porque hasta el 2026-09-15 la ficha **F-091** la tenía
anotada como «lo único que sigue sin probarse».

### 7.7 Lo que midió la prueba sin papel (13:29:17)

Con el servicio `active` y el folio previo en 8, el usuario dejó la impresora
**sin papel** y jugó una vez. La impresora encendió su foco rojo de error y se
puso a pitar cada segundo, con el trabajo retenido en su búfer. El journal:

```
Boleto 00009 emitido: TEST 7
WARNING … reporta poco papel          <- el aviso rezagado de siempre
Boleto 00009 impreso: TEST 7
```

**No se detectó «sin papel» ni «fuera de línea».** `boletos.csv` registró el
00009 como `emitido` **e** `impreso`, `estado.json` pasó al folio 9 y el premio
**TEST 7 quedó descontado sin que saliera papel**. El proceso estaba sano
(`wchan` = `hrtimer_nanosleep`, `NRestarts=0`): la escritura al nodo `usblp` no
se bloqueó porque la impresora aceptó los bytes en su búfer.

Al reponer el papel (13:31–13:33) la impresora **soltó sola** el boleto retenido,
cortado. Eso **no** salva el caso: si se apaga la impresora o la Pi antes de
reponer, el trabajo se pierde y el programa ya lo dio por impreso; y si el papel
se acaba a media impresión, sale un boleto incompleto.

**Este criterio queda en rojo a propósito**, y no bloquea el cierre de la Fase 3
porque **no es una fase de código**: el arreglo —leer la respuesta **fresca** tras
el `DLE EOT`— es de la Fase 4 y espera la autorización del usuario (ficha
**F-250**).

### 7.8 La suite sigue en verde

```
python -m unittest discover -s tests -t .     # en esta PC; en la Pi, python3
```

**194 pruebas OK.** Esta fase no tocó código: el criterio es que **siga** dando
exactamente lo mismo que daba antes.

---

## 8. Prohibiciones

1. **No se cambian los números de GPIO** de `config.json` para acomodar un cable
   (D1). Se mueve el cable.
2. **No se conecta ningún botón a 5 V (pines 2 y 4) ni a 3V3 (pines 1 y 17).**
3. **No se declara ningún pin como salida** en una herramienta de diagnóstico
   (D5).
4. **No se prueban los botones con el servicio arriba «a ver si funciona»** sin
   contar los folios: cada pulsación imprime y gasta. Para eso está
   `--impresora vista`.
5. **No se arregla aquí el aviso de poco papel** (D7): tiene su diagnóstico
   cerrado y espera autorización del usuario.
6. **No se toca `CLAUDE.md`** desde esta fase: su «Contexto del producto» lo
   actualiza el orquestador (ficha **F-242**).
7. **No se da por buena una hipótesis de cableado sin prueba cruzada.** «Creo que
   pulsé HABILITAR» no es una medición (§5, trampa 5).
8. **No se deja evidencia solo en `/tmp` de la Pi**: es `tmpfs` (§5, trampa 7).
9. **No se escribe un acta de memoria.** Se escribe desde
   `docs/actas/2026-09-15-hechos-medidos-fase-3.md`.

---

## 9. Lo que esta fase entrega a la siguiente

- **Los dos botones cableados, probados y guardados en su caja**, con el servicio
  `active` y `enabled` y el kiosco operable de punta a punta.
- **El diagrama** `docs/cableado-botones.svg`, verificado contra el pinout
  oficial, para rehacer el cableado sin volver a diagnosticar nada.
- **Una decisión nueva del usuario que cambia el planteamiento del evento:** sin
  batería RTC y **con internet del asadero** (D6). Esto **deroga** lo que decían
  la Fase 1 y la Fase 2 sobre la batería RTC como «principal riesgo abierto» y lo
  sustituye por otro riesgo, más pequeño y con mitigación conocida: **los primeros
  minutos después de encender** —**unos tres** el 2026-09-15, de las 11:44:42 a
  las 11:47—.
- **Una pieza de programación nueva para la Fase 4: la pieza D** —esperar a que
  la hora esté sincronizada antes de imprimir el inventario y de aceptar jugadas,
  avisando en el boleto si no lo consiguió—, que se suma a las piezas A, B y C
  del documento del evento.
- **Una medición en rojo que la Fase 4 tiene que arreglar antes del evento:** con
  el rollo agotado, el kiosco **emite, descuenta y da por impreso un boleto que no
  sale** (§7.7). Es el riesgo abierto más grande que deja esta fase, y el único
  que puede costar premios de verdad durante la semana (fichas **F-091** y
  **F-250**).
- **Seis pendientes con nombre y ficha:** soldar HABILITAR (**F-239**), decidir
  el LED (**F-240**), la pieza D (**F-241**), `CLAUDE.md` (**F-242**), reiniciar
  el inventario antes del lunes 21 (**F-243**) y el arreglo de la consulta de
  papel (**F-250**).

---

## 10. Regla final

**Si el código real, el `README.md`, el `config.json` o la propia Raspberry Pi
contradicen este plan, el ejecutor se detiene y pregunta; no improvisa.**
