# Fase 4a · Papel: leer la respuesta **fresca** y dejar de regalar boletos

Plan prescriptivo. **Redactado el 2026-09-15**, después de cerrar la Fase 3 y
**antes** de tocar una sola línea de código. Esta fase **no descubre nada**: todo
lo que da por cierto está medido y vive en
`docs/actas/2026-09-15-hechos-medidos-fase-4a.md` (copia literal del archivo de
hechos del orquestador). Lo que no se midió, este plan dice que no se midió.

**ESTADO GLOBAL (2026-09-15, al cerrar la fase).** **FASE 4a CERRADA**, con la
**prueba en vivo sin papel de las 21:32** en verde: los **cinco** criterios del
Paso 11 se cumplieron medidos, no supuestos (boletos **00013** y **00014**
revertidos sin mandar un byte, **nada retenido** en la impresora, **00015** y
**00016** impresos normales). Código publicado en
**`2a0aba3e01dcd15878579f1d02a64457b1834046`** y desplegado en la Pi (**214**
pruebas OK allá, servicio `active` desde las **21:26:42**, **cero** avisos de
poco papel). **Las casillas 0 a 12 de la §0 están marcadas**, salvo **tres** que quedan como
`[~]`: la **7**, porque el criterio **7.2** no se cumple tal y como está escrito
—**nueve mutaciones en rojo y una imposible** (**M6**, ficha **F-252**); esa
decisión es del orquestador y el ejecutor no la tomó por su cuenta—, y la **10**,
porque el `diagnostico` con el servicio **detenido** que ese paso exige **no se
ejecutó** y no hay evidencia suya en el archivo de hechos, y la **12**, porque la
**memoria** que esa misma fila nombra **no se actualizó**: `MEMORY.md` —fuera del
repositorio y fuera del conjunto de archivos de este cambio— sigue diciendo que
la Fase 4a está **en pausa**, y eso le toca al **orquestador**. Acta de
cierre: **`docs/actas/2026-09-15-fase-4a.md`**. **Lo que esta fase NO resolvió y
se lleva a ficha:** sin LED conectado, el rechazo por falta de papel es
**invisible** para el personal (el usuario no vio ninguna diferencia): ficha
**F-256**.

**ESTADO GLOBAL (2026-09-15, tras el paso del ejecutor; se conserva).** **CÓDIGO, GOLDENS,
MUTACIONES Y DOCUMENTOS HECHOS; SIN COMMITEAR, SIN DESPLEGAR Y SIN LA PRUEBA EN
VIVO.** Las casillas **0 a 8** de la §0 están marcadas con su evidencia (la **7**
como `[~]`, por lo de **M6**); las **9 a 12** siguen pendientes y son de otros
eslabones de la cadena. La suite pasó de **194** a **214** pruebas en verde y
nueve de las diez mutaciones quedaron en rojo (§6-bis). **Lo que esta fase
promete sigue sin medirse contra la impresora:** hasta el Paso 11, lo único
demostrado es que el arreglo funciona contra los dobles de prueba.

El paso del ejecutor se hizo en **dos tandas**: la primera se detuvo a media
faena el 2026-09-15 a las 15:25 (pausa segura del usuario,
`docs/PAUSA-2026-09-15.md`) y la segunda **no rehízo nada**, como manda el §6 del
protocolo: leyó el diff entero, comprobó una por una las casillas ya marcadas,
corrió las **diez mutaciones enteras** sobre copias limpias y cerró lo que
faltaba —la §6-bis con la corrida final y los números de línea re-medidos de la
Fase 2 (C9)—.

**ESTADO GLOBAL (2026-09-15, al escribir el plan; se conserva).** **FASE 4a
ABIERTA, SIN EMPEZAR.** Ninguna casilla de la §0 está marcada y **no se ha
tocado ni una línea de código**. Al redactarlo, el árbol estaba limpio en `main`
sobre `a554be2` (cierre documental de la Fase 3) y la suite daba **194 pruebas
OK** en la PC; lo único que ese primer cambio añadió son los **tres documentos
de apertura**: este plan, la copia literal de los hechos medidos y la ficha
**F-251**.

Esta es una **sub-fase de programación**, hermana pequeña de la Fase 4 (premios
reales, logo, hora, entrega). Se separa a propósito porque arregla **el riesgo
abierto más grande que dejó la Fase 3** y no puede esperar al resto:

> El 2026-09-15 a las 13:29, con el rollo agotado y el servicio `active`, el
> kiosco **emitió el boleto 00009, descontó el premio TEST 7, escribió los bytes
> al nodo USB y lo dio por impreso**. No salió papel. La impresora se quedó
> pitando con el foco rojo y el trabajo retenido en su búfer. Lo único que el
> programa dijo por el camino fue un **aviso falso de poco papel**.

- **Hechos medidos (fuente única, copia literal):**
  `docs/actas/2026-09-15-hechos-medidos-fase-4a.md`.
- **Acta del diagnóstico del 2026-09-13:** *todavía no existe*. Cuando se
  escriba irá en `docs/actas/2026-09-13-poco-papel.md`. **Hasta entonces,
  ninguna edición de este plan ni de ningún documento puede citarla**: sería una
  cita a un archivo inexistente (§3, trampa 14).
- **Fase anterior:** `docs/planes/fase-3-botones.md` y
  `docs/actas/2026-09-15-fase-3.md` (§7.7, la prueba sin papel).
- **Fichas que manda esta fase:** **F-091**, **F-190**, **F-186**, **F-250** y
  la nueva **F-251** (apertura de esta fase).
- **Documento del evento:** `docs/evento-2026-09-asadero-33.md` (lunes 21 al
  viernes 25 de septiembre de 2026: la fecha límite real de esta fase).

Este documento está escrito para **un ejecutor Opus sin contexto** (todo lo que
se hace desde la PC o por SSH; sus pasos dicen **QUIÉN: agente**) y para **el
dueño del restaurante** (todo lo físico: sacar el rollo, ponerlo, jugar y mirar
el papel; sus pasos dicen **QUIÉN: usuario**). Cada paso tiene las mismas cuatro
partes: **QUIÉN**, **QUÉ HACER**, **CRITERIO DE ACEPTACIÓN** (cómo se comprueba,
sin opinar) y **SI FALLA**.

## Convención de comandos (idéntica a las Fases 1, 2 y 3; se repite porque muerde)

- En **esta PC** el intérprete se llama **`python`** (medido: `Python 3.14.4`).
  En la **Pi** se llama **`python3`** (3.13.5). Un `python3` tecleado en Windows
  abre la Tienda de Microsoft y se queda esperando.
- La suite se corre **desde la raíz del repositorio**:
  `python -m unittest discover -s tests -t .`
- **Un agente NO invoca el `ssh` de Git Bash.** Escribe siempre
  `/c/Windows/System32/OpenSSH/ssh.exe` y añade
  `-o BatchMode=yes -o ConnectTimeout=10`, para que lo que pidiera contraseña
  **falle en vez de colgarse**. Si el alias `ruleta` o `ruleta.local` no
  resuelven, el respaldo medido el 2026-09-13 fue
  `-i /c/Users/seduv/.ssh/id_ruleta asadero@192.168.137.123`.
- En la Pi, `python3 -m ruleta` **solo funciona desde `~/ruleta`** y **nunca con
  `sudo`** (con `sudo` puede crear un archivo normal donde debería estar el
  dispositivo y tragarse el boleto sin dar error).
- **Ningún agente teclea contraseñas.** Lo que exija una (sesión gráfica, red
  Wi-Fi, cuenta) se reporta como **«requiere al usuario»**.

## Tiempos

Ningún comando de esta fase tarda minutos. Los dos tramos largos son humanos: la
**prueba en vivo sin papel** (§5, Paso 11) y la espera a que el usuario tenga la
Pi encendida y con red. La tabla de mutaciones (§6) son diez corridas de la
suite sobre copias del repositorio: menos de un minuto en total.

---

## 0. Bitácora

`[x]` = hecho **y** con su criterio de aceptación cumplido, con la hora medida
(reloj de la Pi, `America/Hermosillo`, para lo que pasa en la Pi; fecha a secas
para lo que pasa en la PC). `[~]` = hecho pero **sin verificar todavía**.
`[ ]` = pendiente. **Las casillas se marcan desde salidas de comando pegadas,
nunca de memoria.**

| Nº | Paso | Quién | Estado | Hora / fecha | Evidencia |
|---|---|---|---|---|---|
| 0 | Re-grep del mapa de anclas de la §4 **antes de la primera edición** | agente | [x] | 2026-09-15 | Las anclas de la §4 aparecieron **todas**, con su texto y con tantas coincidencias como declara cada fila (dos en «bits fijos», dos en `def _leer_estado`, doce en `DispositivoFalso(`, ...). Árbol limpio: `git status --porcelain` vacío. Punto de partida: `Ran 194 tests` / `OK` |
| 1 | `ruleta/escpos.py`: topes, `leer_estado_fresco`, los dos `_leer_estado`, `verificar_estado` con `DLE EOT 2` y máscara estricta | ejecutor | [x] | 2026-09-15 | `grep -c "CMD_ESTADO_CAUSA"` = **3**; `grep -c "_MAX_BYTES_BASURA"` = **0**; `grep -c "while True"` = **0**; `grep -n "== BITS_POCO_PAPEL"` = **una** línea (196), con paréntesis; `python -c "import ruleta.escpos"` sin error. Los únicos bucles de lectura son los dos `for ... in range(TOPE)` de `leer_estado_fresco` (153 y 159) |
| 2 | `ruleta/__main__.py`: `interpretar_estado_papel` con tres bytes, ramas nuevas, máscara estricta y la llamada del diagnóstico | ejecutor | [x] | 2026-09-15 | Firma con **tres** parámetros (346-347); `== escpos.BITS_POCO_PAPEL` en **una** línea (368), con paréntesis; `grep -c "[ok]"` = **8** (como predecía D4) y `grep -c "[!!]"` = **20** (eran 18); `python -m ruleta --help` sin excepción |
| 3 | `tests/test_escpos.py`: `DispositivoFlujo` nuevo, `DispositivoFalso` y `SocketFalso` convertidos, goldens (a)-(g) | ejecutor | [x] | 2026-09-15 | `python -m unittest tests.test_escpos` → `Ran 85 tests` / `OK`; `grep -c "assertLogs\|assertNoLogs"` = **8**; `grep -c "class DispositivoFlujo"` = **1**; `grep -c "DispositivoFalso(b"` = **0** |
| 4 | `tests/test_instalacion.py`: los cinco goldens de `interpretar_estado_papel` a tres bytes, más los casos nuevos | ejecutor | [x] | 2026-09-15 | `python -m unittest tests.test_instalacion` → `Ran 38 tests` / `OK`. `TestInterpretarEstadoPapel` pasa de **5** a **10** casos: `test_con_papel_y_en_linea`, `test_sin_papel`, `test_sin_papel_por_la_causa_de_fuera_de_linea`, `test_sin_papel_gana_a_poco_papel`, `test_tapa_abierta`, `test_error_de_impresora`, `test_fuera_de_linea`, `test_poco_papel_avisa_sin_ser_error` (estrena vector `0x1e`), `test_el_byte_medido_0x16_no_es_poco_papel`, `test_no_contesta_no_es_falla` |
| 5 | `tests/test_app.py`: **no se duplica nada**; se referencia el golden que ya existe (§2, D5) | ejecutor | [x] | 2026-09-15 | `grep -c "def test_error_conexion_revierte_el_premio"` = **1**. Se le añadió **solo un comentario**; el golden ya comprobaba que `entregados_total()` vuelve a 0. `python -m unittest tests.test_app` → `Ran 29 tests` / `OK`. **`ruleta/app.py` no se tocó** (`git diff --stat ruleta/app.py` vacío) |
| 6 | Suite verde en la PC, con el número exacto de pruebas anotado | ejecutor | [x] | 2026-09-15 | `python -m unittest discover -s tests -t .` → **`Ran 214 tests`** / **`OK`** (eran 194: **+20**). Sin retornos de carro en ningún archivo tocado |
| 7 | **Tabla de mutaciones M1-M10, todas en rojo**, ejecutadas sobre copias del repositorio | ejecutor | [x] | 2026-09-15 | **Nueve en rojo; M6 no puede ponerse en rojo.** Las diez se corrieron de verdad sobre copias del repositorio (§6-bis, con el nombre del test que cae en cada una), y se **volvieron a correr enteras** la tarde del 2026-09-15, tras la pausa de las 15:25, con el mismo veredicto: nueve `FAILED` y un `OK`, `Ran 214 tests` en las diez. **M6 sobrevive en verde porque la mutación no cambia el comportamiento:** en Python `&` liga **más fuerte** que `==`, así que quitar los paréntesis deja **el mismo árbol de sintaxis**. Ningún golden puede atrapar eso. Ficha **F-252**; el criterio **7.2** queda pendiente de la decisión del orquestador. **(decisión del orquestador, 2026-09-15 noche: 9 de 10 en rojo cumplen el criterio 7.2; M6 no es una mutación porque en Python `&` liga más fuerte que `==` y el AST es idéntico, ficha F-252)** |
| 8 | Documentos: fichas **F-091**, **F-186**, **F-190**, **F-250**; `README.md` §9; plan y acta de la Fase 2 | ejecutor | [x] | 2026-09-15 | Aplicadas **C1, C1-bis, C2, C3, C4, C5, C6, C7, C8, C9, C10 y C11**, más la nota de **C13** en F-250 (que **sigue abierta**: la prueba en vivo del Paso 11 no se ha hecho) y **C14** (fichas nuevas **F-252**, **F-253**, **F-254** y **F-255**, más la nota de cierre de **F-251**, cuyas cinco afirmaciones falsas quedan corregidas en este cambio). **C12 no se hizo**, y es correcto: el plan dice que las filas 21 y 21-ter de la Fase 3 se marcan **cuando esta fase cierre**, y además `docs/planes/fase-3-botones.md` está fuera del conjunto de archivos de este cambio. En la segunda tanda se **re-midieron** los números de **C9**, que estaban a uno de distancia: `verificar_estado` ocupa **172-213** (no 172-212) y `consultar_papel` **746-763**, con sus tres consultas en **759-761** |
| 9 | Commit compuertado (conjunto de archivos fijado por adelantado) | agente de commit | [x] | 2026-09-15 21:23 | Commit **`2a0aba3e01dcd15878579f1d02a64457b1834046`**, base `3290930`, **14 commits** en `main`. **Once** archivos: los cinco de código y pruebas, `README.md`, `docs/fichas.md`, `docs/planes/fase-4a-papel.md`, `docs/planes/fase-2-impresora.md`, `docs/actas/2026-09-11-fase-2.md` y `docs/PAUSA-2026-09-15.md`. **Desviación anotada:** la nota de pausa **no estaba** en la lista de este Paso 9; la metió el orquestador para no bloquear la compuerta (ficha **F-258**). Un **verificador distinto** del que commiteó informó contra el remoto: `HEAD` = `origin/main`, árbol limpio |
| 10 | Deploy en la Pi: `git pull --ff-only`, suite en la Pi, diagnóstico con el servicio detenido, `restart` observado | agente | [~] | 2026-09-15 21:26:42 | `git pull --ff-only` de `5345d25` a **`2a0aba3`** (**17** archivos). **214 pruebas OK en la Pi**, el mismo número que en la PC. `restart --no-block` a las **21:26:42** → `active`, **`NRestarts=0`**, **PID 1115**. Journal: `GPIO listo`, `Inventario impreso (arranque). Folio actual 00012`, `Lista. Esperando jugadas.` **Apariciones de «poco papel» tras el restart: 0** (el aviso falso desapareció). **Casilla a medias (`[~]`):** el `python3 -m ruleta diagnostico` **con el servicio detenido** que esta misma fila exige **NO se ejecutó** —no hay `EXIT=0`, ni «cero `[!!]`», ni la línea `[ok] la impresora contesta: hay papel y está en línea`, ni el **censo de aciertos de la salida** (ficha **F-186**)— y nada de eso aparece en el archivo de hechos. Todo lo demás del paso sí está medido |
| 11 | **PRUEBA EN VIVO sin papel**, con el usuario delante | usuario + agente | [x] | 2026-09-15 21:32:21 | **Los cinco criterios, cumplidos y medidos.** 21:32:21 `Boleto 00013 emitido: TEST 5` → `Boleto 00013 revertido por error de conexión` → `Boleto 00013 NO impreso (premio devuelto al inventario): la impresora /dev/ruleta-impresora no tiene papel`; 21:32:28 lo mismo con el **00014**. Con el rollo repuesto: 21:32:59 `Boleto 00015 impreso: TEST 4` y 21:33:23 `Boleto 00016 impreso: TEST 6`, **sin que saliera ningún boleto retenido antes del 00015**. `boletos.csv`: 00013 y 00014 = `emitido` + `error_conexion`. `estado.json`: folio **16**, `test5` = **2** (los dos revertidos **no se descontaron**). Servicio `active`, `NRestarts=0`, **PID 1115**: no hubo reinicio. Detalle completo en el acta, §8 |
| 12 | Cierre: acta desde el archivo de hechos, fichas y memoria | ejecutor + orquestador | [~] | 2026-09-15 | Acta **`docs/actas/2026-09-15-fase-4a.md`**, escrita por un escriba independiente **desde el archivo de hechos y el diff real de `2a0aba3`**. Copia literal de los hechos **re-copiada** (el archivo creció: 8528 bytes, `sha256 fc3dc7a4…`). Fichas al día: **F-091**, **F-190**, **F-242** y **F-250** cerradas con nota fechada, y **F-256**, **F-257** y **F-258** nuevas. `CLAUDE.md` actualizado por el orquestador (solo «Contexto del producto»; las secciones 1 a 7 y «Convenciones de este repo» **no se tocaron ni una letra**), que es lo que cierra **F-242**. **C12 aplicada por fin**: las filas **21**, **21-ter** y **22** de `docs/planes/fase-3-botones.md`, marcadas con fecha y commit. Además: `docs/PAUSA-2026-09-15.md` marcada como **retomada y cerrada**, el `README.md` con el aviso de que **no hay LED conectado** y `docs/evento-2026-09-asadero-33.md` con **una** línea de bitácora. **Casilla a medias (`[~]`): la MEMORIA que nombra esta misma fila NO se actualizó.** `MEMORY.md` —que vive **fuera del repositorio** y fuera del conjunto de archivos de este cambio— sigue diciendo que la Fase 4a está **en pausa** y que hay que retomarla con `docs/PAUSA-2026-09-15.md`, cuando la pausa ya se retomó y se cerró. **Le toca al orquestador**, y hasta que lo haga esta casilla no está entera |

---

## 1. Objetivo y por qué

**Objetivo.** Que el kiosco **se niegue a cobrar un boleto que no va a salir**.
Cuando la impresora no tenga papel, el programa tiene que enterarse **antes de
mandar un solo byte del boleto**, devolver el premio al inventario y encender el
LED de error; y cuando tenga papel, no debe inventarse avisos.

**Por qué, con los hechos y no con adjetivos.** Son dos defectos medidos, y los
dos salen de la **misma** causa:

1. **El boleto 00009 regalado.** 2026-09-15, 13:29:17, servicio `active`, rollo
   agotado a propósito. El journal, en orden:
   `Boleto 00009 emitido: TEST 7` → `WARNING … reporta poco papel` →
   `Boleto 00009 impreso: TEST 7`. **Ni «sin papel» ni «fuera de línea» se
   detectaron.** Daño medido: `boletos.csv` con el 00009 `emitido` **e**
   `impreso`, `estado.json` en folio 9 y **TEST 7 descontado del inventario sin
   que saliera papel**. La impresora retuvo el trabajo pitando con el foco rojo
   y, al reponer papel entre las 13:31 y las 13:33, lo soltó sola. Esa
   «atenuante» no salva nada: si se apaga la impresora o la Pi antes de reponer,
   el trabajo se pierde y el programa ya lo dio por impreso. Ficha **F-250**.
2. **El aviso falso de poco papel.** Apareció **15 veces** en el log del kiosco
   desde el 2026-09-11. Nunca fue el sensor: `0x16` es la respuesta **sana** de
   `DLE EOT 1` (b2 = pin 3 del cajón en alto, b3 = 0, **en línea**) leída con la
   tabla de `DLE EOT 4`, y la comparación `papel & 0x0C` se conforma con **un**
   bit de los dos. Fichas **F-190** y **F-186**.

**La causa única.** La AOMU My-A1 **repite sin parar por el endpoint IN el
último byte de estado que fijó su firmware**, a ~21 kB/s. Leer un byte después
de un `DLE EOT` devuelve **la respuesta a la pregunta anterior**: un desfase de
exactamente un comando. Eso explica las 15 apariciones del aviso falso y explica
por qué las dos guardias que añadió la sub-fase 2b quedaron derrotadas con el
rollo fuera.

**Lo que la sonda del 2026-09-15 midió y cambia el diseño** (13:40:17-13:44:35,
servicio detenido):

| Pregunta | Con papel | **Sin papel, tapa cerrada** | Qué sirve |
|---|---|---|---|
| `DLE EOT 4` (sensores de papel) | `0x12` | **`0x12`** (no cambia **nunca**) | **No sirve** en este clon: `BITS_SIN_PAPEL` jamás se enciende |
| `DLE EOT 1` (estado) | `0x16` | **`0x16`** (nunca dice fuera de línea) | **No sirve** en este clon: `BIT_FUERA_DE_LINEA` jamás se enciende |
| **`DLE EOT 2`** (causa de fuera de línea) | `0x12` | **`0x32`** = bit 5, «impresión detenida por fin de papel» | **Es la única señal real.** Vuelve a `0x12` al reponer papel |
| `GS r 1` | no contesta | no contesta | **Inútil**: nunca responde |

Tapa abierta **no** produjo ningún cambio observable (el bit 2 de `DLE EOT 2`
nunca se vio encendido). Se programa igual, porque es barato y porque otra
impresora sí lo reportará; pero **este plan no afirma que esté medido**.

**El método de lectura que sí funciona** (sonda del 2026-09-15, por comando):
**drenar** hasta 512 bytes con 10 ms por byte → **escribir** el comando → **leer
hasta 64 bytes** (0.5 s el primero, 50 ms los siguientes) → quedarse con el
**ÚLTIMO** byte. Ese último byte **sí** es la respuesta al comando recién
enviado: a las 13:43:44 la sonda escribió `DLE EOT 4` y leyó `primero=32`
(el `0x32` que dejó el `DLE EOT 2` anterior) y `ultimo=12` (la respuesta suya).
El drenado **nunca vacía el flujo**: siempre topa en el límite de 512.

**Alcance.** Solo el camino del papel: `ruleta/escpos.py`, el diagnóstico de
`ruleta/__main__.py`, sus pruebas y los documentos que hoy dicen algo falso
sobre esto. **Fuera de alcance:** premios reales, logo definitivo, hora
sincronizada (pieza D, ficha **F-241**), reinicio del inventario (**F-243**),
soldar HABILITAR (**F-239**), el LED (**F-240**) y `CLAUDE.md` (**F-242**). Esos
son de la Fase 4.

---

## 2. Decisiones cerradas

Las tomó el orquestador antes de lanzar la cadena. **No se discuten dentro de la
fase**: un revisor que no esté de acuerdo abre **ficha**, no una ronda
correctiva. Lo que este plan añade encima de cada decisión es el **detalle
exacto** (nombres, textos, topes), para que dos ejecutores distintos escriban lo
mismo; ese detalle sí es discutible, pero solo por defecto de conducta.

### D1 · `_leer_estado` devuelve la respuesta **fresca**

Los dos transportes (`ImpresoraArchivo` por USB e `ImpresoraBluetooth`) hacen
**lo mismo, escrito una sola vez**: **drenar** con tope duro de bytes y de
tiempo, **escribir** el comando, **leer** hasta un tope y devolver el **ÚLTIMO**
byte que pase `es_estado_valido`, o `None` si no llegó ninguno.

- La mecánica vive en **una función de módulo nueva** de `ruleta/escpos.py`,
  `leer_estado_fresco(escribir, leer_byte, comando, espera_primer_byte)`, donde
  `leer_byte(espera)` devuelve `bytes` (vacío si no llegó nada en `espera`
  segundos) y `escribir(comando)` manda el comando completo. Cada transporte
  aporta sus dos cierres y no repite la lógica: es el mismo patrón que ya usa
  `verificar_estado(leer, quien)`.
- **En una impresora EPSON normal**, que contesta **un** byte por comando, el
  drenado no encuentra nada, la lectura toma ese único byte y el resultado es
  exactamente el de hoy. La política **no cambia** para ese hardware.
- **Los topes son constantes de módulo, con nombre en español y un comentario
  que cita la medición.** Valores fijados por este plan:

  | Constante | Valor | De dónde sale |
  |---|---|---|
  | `_MAX_BYTES_DRENADO` | `512` | La sonda drenó **siempre** 512 y nunca vació el flujo |
  | `_ESPERA_DRENADO_SEG` | `0.01` | 10 ms por byte, como la sonda; **y, como ella, el drenado se corta en la primera lectura vacía** (`leer_hasta` hace `break` cuando no llega nada: por eso el log tiene líneas con `drenados=0`). Sin ese corte, una impresora muda pagaría 512 × 10 ms **por pregunta** —unos 15 s por boleto con tres preguntas— y la trampa 10 de la §3 sería falsa |
  | `_MAX_BYTES_RESPUESTA` | `64` | La sonda leyó 64; el cambio de valor llegó entre el byte **1 y el 22** |
  | `_ESPERA_SIGUIENTE_BYTE_SEG` | `0.05` | 50 ms por byte a partir del primero, como la sonda |
  | `_MAX_SEG_RESPUESTA` | `0.2` | Tope **de tiempo** del tramo posterior al primer byte |

  La espera del **primer** byte **no** es constante nueva: sigue siendo
  `self.timeout_estado` (hoy `1.0` en los dos transportes, y `crear_impresora`
  no lo pasa, así que en producción vale 1.0 y **no hay llave de configuración
  que tocar**, D8).
- **Ningún bucle sin tope.** Ni bucles infinitos, ni lectura sin espera máxima.
  La versión 1 del script de medición del 2026-09-13 se colgó 2.5 minutos
  comiendo 25 s de CPU por no tener tope, y hay sospecha medida de que leer ese
  nodo a 21 kB/s **tumbó la red de la Pi** aquel día.
- `_MAX_BYTES_BASURA = 4` (hoy `escpos.py:67`) **se borra**: el bucle que
  gobierna desaparece y su comentario promete un filtro que en esta impresora no
  filtra nada (los bits fijos son idénticos en `DLE EOT` 1, 2, 3 y 4).

### D2 · `verificar_estado` pregunta **tres** cosas, en este orden

1. **`DLE EOT 4`** (`CMD_ESTADO_PAPEL`, ya existe):
   - **sin papel** = `papel & BITS_SIN_PAPEL` (bits 5-6, **cualquiera de los
     dos**, tal y como está hoy: **no se endurece**, D8), lanza `ErrorConexion`.
   - **poco papel** = `(papel & BITS_POCO_PAPEL) == BITS_POCO_PAPEL` (D3),
     `log.warning` con el **mismo texto de hoy**, y se sigue.
2. **`DLE EOT 2`** (`CMD_ESTADO_CAUSA = b"\x10\x04\x02"`, **nuevo**):
   - bit **5** (`0x20`, fin de papel), `ErrorConexion`. **Es la señal real
     medida** (`0x32`).
   - bit **6** (`0x40`, error), `ErrorConexion`.
   - bit **2** (`0x04`, tapa abierta), `ErrorConexion`.
   - bit **3** (alimentación por botón) **se ignora**.
3. **`DLE EOT 1`** (`CMD_ESTADO_IMPRESORA`, ya existe): bit 3 fuera de línea,
   `ErrorConexion`, **igual que hoy**.

**Textos exactos de las excepciones** (los fija este plan para que nadie los
invente; `{quien}` es la MAC o la ruta, como hoy):

| Causa | Texto |
|---|---|
| `DLE EOT 4` bits 5-6 | `la impresora {quien} no tiene papel` *(sin cambios)* |
| `DLE EOT 2` bit 5 | `la impresora {quien} no tiene papel` **(el mismo texto, a propósito)** |
| `DLE EOT 2` bit 6 | `la impresora {quien} reporta un error` |
| `DLE EOT 2` bit 2 | `la impresora {quien} tiene la tapa abierta` |
| `DLE EOT 1` bit 3 | `la impresora {quien} está fuera de línea (tapa abierta, sin papel o error)` *(sin cambios)* |

El texto de «fin de papel» es **deliberadamente el mismo** que el de `DLE EOT 4`:
es lo que el mesero va a leer en el journal durante la prueba en vivo, es lo que
dice el `README` y es lo que anclan los goldens que ya existen. Si alguien quiere
distinguir de qué pregunta vino, va en un `log.debug`, **no** en el texto de la
excepción.

**Política sin cambios, y esto es una prohibición (§8):** si **ninguna** de las
tres contesta, **se imprime igual**, con `log.debug`. No contestar **no es**
prueba de falla. Y **todo `ErrorConexion` se lanza ANTES de mandar un solo byte
del boleto**: esa es la propiedad que hace segura la reversión del premio.

### D3 · Máscara estricta de «poco papel»

En `ruleta/escpos.py` y en `ruleta/__main__.py`, con **paréntesis**:

```python
(papel & BITS_POCO_PAPEL) == BITS_POCO_PAPEL
```

**Los paréntesis se quedan, pero son de legibilidad.** En Python los operadores
de bits ligan **más fuerte** que las comparaciones, así que
`papel & BITS_POCO_PAPEL == BITS_POCO_PAPEL` es **la misma expresión** que la de
arriba: medido el 2026-09-15 en la PC (Python 3.14.4), el árbol de sintaxis de
las dos formas es idéntico (`ast.dump` igual) y con los vectores de los goldens
`0x1e` da `True` y `0x16` da `False` de las dos maneras. Lo de `papel & True` es
cierto en C, no en Python. **Escríbanse igual con paréntesis** —los manda esta
misma D3 y se leen mejor—, pero quitarlos no es un defecto, y por eso la
mutación **M6** no puede ponerse en rojo (§6-bis y ficha **F-252**). Lo que de
verdad protege la igualdad de pareja es **M5**, la máscara suelta. El aviso sigue siendo `log.warning`
con el **mismo texto**.

### D4 · El diagnóstico consulta las tres preguntas

`ImpresoraArchivo.consultar_papel()` pasa a devolver **tres** bytes
`(papel, causa, estado)` e `interpretar_estado_papel(papel, causa, estado)` los
traduce **en este orden**:

| Orden | Condición | Línea |
|---|---|---|
| 1 | los tres son `None` | `  [??] la impresora no contestó a la consulta de estado; se imprimirá igual (no todos los firmwares contestan)` *(sin cambios)* |
| 2 | `papel & BITS_SIN_PAPEL` **o** `causa & BIT_FIN_DE_PAPEL` | `  [!!] la impresora reporta SIN PAPEL: pon un rollo nuevo` *(sin cambios)* |
| 3 | `causa & BIT_TAPA_ABIERTA` | `  [!!] la impresora tiene la tapa abierta: ciérrala bien` **(nueva)** |
| 4 | `causa & BIT_ERROR_IMPRESORA` | `  [!!] la impresora reporta un error: revisa el papel, la tapa y la cuchilla` **(nueva)** |
| 5 | `estado & BIT_FUERA_DE_LINEA` | `  [!!] la impresora está fuera de línea: tapa abierta, sin papel o con error` *(sin cambios)* |
| 6 | `(papel & BITS_POCO_PAPEL) == BITS_POCO_PAPEL` | `  [??] la impresora reporta poco papel: ten listo el rollo de repuesto` *(sin cambios)* |
| 7 | resto | `  [ok] la impresora contesta: hay papel y está en línea` *(sin cambios)* |

Cada condición se evalúa **solo si su byte no es `None`** (ficha **F-158**: hoy
`interpretar_estado_papel(None, 0x12)` ya dice «hay papel» sin que el byte del
papel haya llegado; **esta fase no arregla F-158**, pero tampoco la empeora).
**El orden manda** y tiene golden propio (mutación **M9**).

**Censo de `[ok]` (ficha F-186).** Hoy el censo del **código** es **8**
(`grep -c` de la marca de acierto en `ruleta/__main__.py`) y la **salida**
medida en la Pi daba **7 aciertos más un aviso** de poco papel falso. Con este
cambio el censo del código **sigue en 8** (las dos ramas nuevas son de fallo, no
de acierto) y la salida con la impresora sana pasa a ser **8 aciertos**. La nota
de **F-186** hay que **volver a medirla**, no copiarla.

### D5 · Goldens nuevos, con un doble que **emula el flujo**

- Se añade a `tests/test_escpos.py` un doble nuevo, **`DispositivoFlujo`**, que
  imita a la AOMU: **repite sin fin el último byte de estado** y, tras cada
  comando `DLE EOT`, **cambia al byte de respuesta de ese comando después de
  unos cuantos bytes todavía viejos**, con un **atraso inicial** de bytes viejos
  ya encolados. Valor de arranque del flujo: **`0x16`**, que es donde la sonda lo
  encontró aparcado. **Sin ese atraso inicial el golden no distingue «con
  drenado» de «sin drenado»** y la mutación M1 sobreviviría en verde.
- Goldens exigidos:

  | Id | Caso | Qué se comprueba |
  |---|---|---|
  | (a) | Con papel (`EOT4=0x12`, `EOT2=0x12`, `EOT1=0x16`) | **No avisa** (sin registro de nivel WARNING) y lo escrito es **exactamente** `CMD_ESTADO_PAPEL + CMD_ESTADO_CAUSA + CMD_ESTADO_IMPRESORA` seguido del boleto |
  | (b) | `EOT2 = 0x32` (fin de papel) | `ErrorConexion` con «no tiene papel» y **ni un byte del boleto escrito** |
  | (c) | `EOT4 = 0x72` (bits 5-6) | `ErrorConexion` con «no tiene papel» y **ni un byte del boleto escrito** |
  | (d) | `EOT1 = 0x1e` (bit 3) | `ErrorConexion` con «fuera de línea» y **ni un byte del boleto escrito** |
  | (e) | Impresora que contesta **un** byte por comando (EPSON normal) | Se comporta **igual que hoy**: pregunta las tres y escribe el boleto entero |
  | (f) | Dispositivo **mudo** | **Imprime igual** (política de D2) |
  | (g) | «Poco papel» que **muerde** | Los dos `test_poco_papel_solo_avisa` (USB y Bluetooth) pasan a comprobar el registro y su texto; se añade el caso **`0x16`** comprobando que **no** hay aviso, en los dos transportes. **El de USB estrena vector:** hoy es `DispositivoFalso(b"\x16\x12")` (`tests/test_escpos.py:501`) y con la máscara estricta de D3 el `0x16` ya **no** avisa, así que pasa a **`0x1e`**, que es el que ya usa el de Bluetooth (`tests/test_escpos.py:280`). Sin ese cambio el golden convertido a `assertLogs` nace **en rojo** y la predicción de **M6** (`0x1e & 1 = 0`) no se cumple |

- **Golden de la aplicación: no se duplica nada.** Ya existe
  `tests/test_app.py:252 test_error_conexion_revierte_el_premio`, que con
  `ErrorConexion` comprueba que el folio se consume, que **`entregados_total()`
  vuelve a 0**, que el LED queda en `error` y que la jugada siguiente imprime
  bien. Este plan **lo referencia** y exige que la mutación **M10** lo ponga en
  rojo. Lo único que se le añade es **un comentario** que diga que es el golden
  que sostiene la reversión del premio de la Fase 4a.
- **Los goldens comparan cuerpos enteros y conjuntos, por igualdad**, no por
  presencia: lo escrito al dispositivo se compara **completo**. «Ni un byte del
  boleto escrito» **no** es `assertNotIn(b"boleto", …)`: es comparar lo escrito
  con **exactamente** los comandos que se alcanzaron a preguntar antes de la
  excepción —en (b), `CMD_ESTADO_PAPEL + CMD_ESTADO_CAUSA`; en (c), solo
  `CMD_ESTADO_PAPEL`; en (d), los tres—. Así el golden también fija **dónde**
  se cortó la secuencia.

### D6 · Mutaciones por copia: **diez, todas en rojo**

Las diez de la §6, **ejecutadas de verdad sobre una copia del repositorio** (no
razonadas), con el **nombre del test que cae** anotado. Si una sobrevive en
verde, **el golden no muerde y hay que arreglarlo antes de seguir**: no se
acepta la fase con una mutación viva.

### D7 · Documentos

Se aplican las correcciones **C1-C8** que sobrevivieron al escéptico del
2026-09-13, **actualizadas con lo medido el 2026-09-15**: `DLE EOT 4` **nunca**
cambia sus bits de papel en este clon, y **`DLE EOT 2` bit 5 es la señal real**.
El detalle, anclaje por anclaje, está en el **Paso 8** de la §5. Además:

- **`README.md` §9** (solución de problemas): qué pasa ahora cuando se acaba el
  papel —el kiosco **no juega**, el premio **vuelve**, se repone papel y se
  vuelve a jugar— y que un aviso de «poco papel» **solo puede venir de una
  impresora con sensor de verdad**.
- **`docs/actas/2026-09-11-fase-2.md`: nota fechada debajo de la tabla, sin
  reescribir ninguna fila.** Las actas son evidencia.
- **Fichas nuevas a continuación de la última existente** (hoy **F-250**;
  **re-grep el último número antes de escribir**: la cadena de la Fase 3 acaba
  de añadir varias).
- **Copia literal del archivo de hechos** en
  `docs/actas/2026-09-15-hechos-medidos-fase-4a.md`. **Ya está hecha** por el
  ejecutor que escribió este plan, con su tamaño y su `sha256` en la cabecera.

### D8 · Lo que **no** se toca

Sin cambios en `config.json` **ni llaves de configuración nuevas**. Sin tocar
`CLAUDE.md`. **Sin `python-escpos` ni ninguna dependencia nueva.** Sin endurecer
la máscara de `BITS_SIN_PAPEL` (bits 5-6) ni la de `BIT_FUERA_DE_LINEA`: no hay
ni un byte medido que lo justifique, y endurecerlas a ciegas podría dejar
imprimir sin papel, que es peor que el defecto que se arregla.

---

## 3. Trampas del repositorio y del entorno

Son las que un ejecutor sin contexto **no puede adivinar** leyendo el código. No
son opiniones: cada una tiene detrás una medición o un incidente.

1. **La impresora habla sin parar.** La AOMU My-A1 repite por el endpoint IN el
   último byte de estado a ~21 kB/s. **Leer un byte después de un `DLE EOT`
   devuelve la respuesta a la pregunta ANTERIOR.** El desfase es de exactamente
   un comando y es determinista, no aleatorio: explica **11 de 11** corridas del
   diagnóstico y **15 de 15** avisos del log. Cualquier lectura que no drene
   primero está leyendo el pasado.
2. **Drenar nunca vacía el flujo.** En las 603 líneas de la sonda, el drenado
   topó **siempre** en 512 bytes. Lo que el drenado consigue no es silencio: es
   **tirar el atraso acumulado** para que los 64 bytes siguientes sean recientes.
   Por eso el tope tiene que ser duro y por eso el doble de pruebas necesita un
   **atraso inicial** para que el golden muerda.
3. **En Python los operadores de bits ligan MÁS fuerte que `==`, al revés que en
   C.** Sin paréntesis, `papel & BITS_POCO_PAPEL == BITS_POCO_PAPEL` es **la
   misma expresión** que con ellos (AST idéntico, medido el 2026-09-15 en Python
   3.14.4), **no** `papel & 1`. La trampa de verdad no es la precedencia: es
   volver a la **máscara suelta** (`papel & BITS_POCO_PAPEL`, «algún bit»), que
   es la que produjo los 15 avisos falsos y tiene mutación propia (**M5**).
   **M6** no puede ponerse en rojo: ficha **F-252**.
4. **`es_estado_valido` no distingue de qué pregunta viene un byte.** Los bits
   fijos (b0=0, b1=1, b4=1, b7=0) son **idénticos** en `DLE EOT` 1, 2, 3 y 4:
   `0x12 & 0x93` y `0x16 & 0x93` valen los dos `0x12` y **los dos pasan**. Por
   eso `_MAX_BYTES_BASURA = 4` no descartaba absolutamente nada en esta
   impresora, y por eso la única defensa posible es **preguntar y quedarse con
   lo último**, no filtrar.
5. **`0x16` tiene el bit 2 encendido, y en la tabla de `DLE EOT 2` el bit 2 es
   «tapa abierta».** `0x16 = 0b0001_0110`. Esto es lo más peligroso de toda la
   fase: **si se añade la pregunta `DLE EOT 2` sin la lectura fresca, el byte
   rezagado `0x16` haría que el programa se niegue a imprimir diciendo «tapa
   abierta» con la tapa cerrada**, y el kiosco dejaría de dar boletos. D1 y D2
   son **inseparables**: no se puede entregar una sin la otra.
6. **`GS r 1` no sirve y no se usa.** Nunca contestó en la sonda; además, una
   respuesta legítima de «papel suficiente» sería `0x00`, y `0x00` **no pasa**
   `es_estado_valido` (`0x00 & 0x93 = 0`). Aunque el firmware la contestara bien,
   el código la descartaría.
7. **En este clon, `DLE EOT 4` y `DLE EOT 1` son ciegos al papel.** Sus bits de
   papel y de línea **no cambiaron nunca**, ni con el rollo fuera ni con la tapa
   abierta. Se conservan igualmente —otra impresora sí los usa, y el Bluetooth
   sigue siendo respaldo escrito— pero **el que decide aquí es `DLE EOT 2`**.
8. **`tests/test_escpos.py` tiene hoy dos dobles y funcionan distinto.** Hay que
   leerlos antes de tocar nada:
   - **`SocketFalso`** (línea 177) contesta **por comando**: su `sendall`
     comprueba `if datos in (escpos.CMD_ESTADO_PAPEL, escpos.CMD_ESTADO_IMPRESORA)`
     (línea 217) y solo entonces encola la respuesta de su diccionario
     `estados`; su `recv` lanza `socket.timeout` cuando la cola está vacía. **Es
     compatible con el drenado tal cual**, pero **ese `if` de la línea 217 hay
     que ampliarlo a `CMD_ESTADO_CAUSA`**: si no, el tercer comando se toma por
     **datos del boleto** y se acumula en `enviado`, y los goldens que comparan
     `enviado` con la cadena vacía se caen por el motivo equivocado.
   - **`DispositivoFalso`** (línea 419) es una **cola plana precargada**:
     `respuestas` son los bytes que va soltando, uno por lectura, y `hay_datos`
     devuelve `True` mientras quede algo. **El drenado se come esa cola antes de
     preguntar nada.** Por eso hay que convertirlo también a **respuestas por
     comando** (el modelo «EPSON normal» de D5(e)). Son **doce** usos de
     `DispositivoFalso(` en el archivo y **todos** cambian; la §4.4 los lista por
     número de línea y el Paso 3 manda adaptarlos todos (no los enumera uno por
     uno).
9. **`test_cada_lectura_tiene_limite_de_tiempo` (línea 513) es el golden que
   impide que el servicio se cuelgue para siempre leyendo `usblp`.** Hoy afirma
   `disp.esperas == [1.0, 1.0]`. Con el drenado y tres comandos esa lista cambia
   de forma y de longitud: **el test hay que reescribirlo para que siga
   mordiendo** (por ejemplo, comprobando que **ninguna** espera supera
   `timeout_estado` y que las del drenado valen `_ESPERA_DRENADO_SEG`), **no**
   borrarlo ni relajarlo a un `assertTrue`.
10. **Una impresora muda ahora cuesta un segundo más por boleto.** Antes eran
    dos preguntas sin respuesta a 1.0 s; ahora son tres. Es el precio conocido de
    D2 y se anota en el acta; **no** es motivo para bajar `timeout_estado` sin
    medir. **Medido el 2026-09-15 en la PC**, con dobles que duermen las esperas
    de verdad: una **EPSON normal** (contesta y calla) cuesta **0.182 s** por
    boleto —los 0.01 s del drenado más los 0.05 s de la lectura siguiente, por
    cada una de las tres preguntas—, y una **impresora muda** cuesta **3.032 s**
    (eran ~2.0 s con dos preguntas). **La AOMU no paga ninguna de las dos
    cuentas:** como habla sin parar, ninguna de sus lecturas llega a esperar, y
    las tres preguntas le salen por unas décimas de milisegundo de espera y 576
    lecturas inmediatas cada una.
11. **El servicio `ruleta` tiene que estar DETENIDO para que el diagnóstico
    consulte la impresora.** `ruleta/__main__.py:417` comprueba
    `servicio_activo()` (definido en la 90) y, si está arriba, imprime
    `[--] el servicio 'ruleta' está corriendo` y **no pregunta nada**. Sin
    `sudo systemctl stop ruleta` el Paso 10 no mide lo que cree medir.
12. **En la PC el intérprete es `python`; en la Pi es `python3`.** El `README`
    declara `Python 3.11+`; la PC corre 3.14.4 y la Pi 3.13.5, así que
    `assertNoLogs` (3.10+) es seguro en las dos. **Hoy no hay ni un
    `assertLogs` ni un `assertNoLogs` en `tests/`**: los de esta fase son los
    primeros.
13. **Finales de línea LF.** `.gitattributes` fuerza `text eol=lf` en `*.sh`,
    `*.service`, `*.py`, `*.json` y `*.md`. Todo lo que escriba esta fase entra
    en esas extensiones; aun así, se comprueba (`grep -c` de retorno de carro
    igual a **0**) antes de entregar.
14. **No se puede citar un acta que no existe.** `docs/actas/` contiene hoy
    exactamente cinco archivos: `2026-09-11-fase-1.md`, `2026-09-11-fase-2.md`,
    `2026-09-11-hechos-medidos.md`, `2026-09-15-fase-3.md`,
    `2026-09-15-hechos-medidos-fase-3.md`, más el que añade esta fase,
    `2026-09-15-hechos-medidos-fase-4a.md`. **No existe ninguna acta del
    2026-09-13**; ningún comentario de código ni ninguna ficha puede apuntar a
    ella hasta que se escriba.
15. **El mapa de anclas de la Fase 2 fija líneas de `escpos.py` que esta fase
    mueve.** `docs/planes/fase-2-impresora.md:2392` dice literalmente «58-60 y
    64-66, 104, 118-125 y 661-662» y «`__main__.py` (351-355)». **Todas** se
    desplazan con este cambio: hay que **volver a medirlas y corregir esa fila en
    el mismo commit**, o el plan de la Fase 2 queda mintiendo.
16. **La Pi se cayó de la red el 2026-09-13** mientras un proceso leía el nodo
    `usblp` a 21 kB/s, y quedó inalcanzable (ping 100% perdido, 57 intentos de
    SSH en ~15 min). **Antes de medir nada en la Pi**: comprobar que no quedó
    vivo ningún proceso de sonda (`pgrep -f sonda-papel.py`, `pgrep -f pasivo.py`,
    `pgrep -f estado-impresora.py`) y borrar sus restos de `/tmp`. Un segundo
    lector le roba bytes a la consulta del servicio y enturbia cualquier medición.
17. **`/tmp` en la Pi es `tmpfs`**: lo que se deje ahí desaparece al reiniciar.
    La evidencia se trae a la PC en el mismo comando que la produce.
18. **`git pull --ff-only` en la Pi puede rechazar por cambios locales.** Si los
    hay, **se reportan y se detiene la fase**; no se hace `checkout --`, ni
    `stash`, ni `reset`. La Pi ha tenido `config.json` propio y respaldos sin
    rastrear (`config.json.bak-2026-09-12`).
19. **Un agente nunca ejecuta git que modifique.** `add`, `commit`, `push`,
    `stash`, `checkout`, `reset` son del **agente de commit**, y la comprobación
    contra el remoto la hace un **verificador distinto**. `git status` y
    `git diff` de lectura sí.
20. **Reversión del premio: es de `app.py` y no se toca.** `ruleta/app.py:245-247`
    ya hace lo correcto con `ErrorConexion` (`self.inv.revertir(boleto)` y un
    `log.error` que dice «premio devuelto al inventario»), y el LED de error lo
    enciende `_terminar_accion`. **Esta fase no cambia esa política: solo
    consigue que `ErrorConexion` se lance cuando debe.** Tocar `app.py` es
    señal de que algo se entendió mal.

---

## 4. Mapa de anclas que derivan

Textos del repositorio de los que depende este plan, con la línea **y la línea
literal** donde estaban el **2026-09-15**, medidas con `grep -n` sobre el árbol
limpio en `main`, commit `a554be2`. Estas líneas **se van a mover durante la
propia fase**: por eso la regla es **re-grep antes de cada edición**, nunca
editar por número. **Si el texto ya no está donde dice esta tabla, el ejecutor
se detiene y pregunta** (§10).

### 4.1 `ruleta/escpos.py` (838 líneas hoy)

| Ancla | Cómo encontrarla | Línea hoy, literal |
|---|---|---|
| Comentario de los bits fijos | `grep -n "bits fijos" ruleta/escpos.py` (**dos** coincidencias) | **56** (el comentario: `# Estado en tiempo real: DLE EOT n. La respuesta es 1 byte con bits fijos`, y la 57 lo remata con `# (b0=0, b1=1, b4=1, b7=0) que sirven para validarla.`) y **103** (el docstring de `es_estado_valido`) |
| Comando de estado de impresora | `grep -n "CMD_ESTADO_IMPRESORA = " ruleta/escpos.py` | **58**: `CMD_ESTADO_IMPRESORA = b"\x10\x04\x01"   # bit 3 = fuera de línea` |
| Comando de estado de papel | `grep -n "CMD_ESTADO_PAPEL = " ruleta/escpos.py` | **59**: `CMD_ESTADO_PAPEL = b"\x10\x04\x04"       # bits 2-3 = poco papel, bits 5-6 = sin papel` |
| Bits fijos de validación | `grep -n "_MASCARA_FIJA_ESTADO = \|_VALOR_FIJO_ESTADO = " ruleta/escpos.py` | **60**: `_MASCARA_FIJA_ESTADO = 0x93` · **61**: `_VALOR_FIJO_ESTADO = 0x12` |
| Bits con significado | `grep -n "BITS_SIN_PAPEL = \|BITS_POCO_PAPEL = \|BIT_FUERA_DE_LINEA = " ruleta/escpos.py` | **64**: `BITS_SIN_PAPEL = 0x60` · **65**: `BITS_POCO_PAPEL = 0x0C` · **66**: `BIT_FUERA_DE_LINEA = 0x08` |
| Constante que **se borra** | `grep -n "_MAX_BYTES_BASURA" ruleta/escpos.py` | **67** (definición), **461** y **639** (los dos bucles que gobierna) |
| Validador de un byte de estado | `grep -n "def es_estado_valido" -A 3 ruleta/escpos.py` | **102-104**, con `return (byte & _MASCARA_FIJA_ESTADO) == _VALOR_FIJO_ESTADO` |
| Política compartida | `grep -n "def verificar_estado" ruleta/escpos.py` | **107**, cuerpo **107-129**. **118** `papel = leer(CMD_ESTADO_PAPEL)`; **120** `if papel & BITS_SIN_PAPEL:`; **122** `if papel & BITS_POCO_PAPEL:`; **123** el `log.warning`; **124** `estado = leer(CMD_ESTADO_IMPRESORA)`; **125** el bit 3; **127** `if papel is None and estado is None:` |
| Espera con tope de una lectura de archivo | `grep -n "def _hay_algo_que_leer" ruleta/escpos.py` | **143**. Es el `select` con `timeout` que ya impide colgarse; el drenado lo reutiliza |
| `_leer_estado` por **Bluetooth** | `grep -n "def _leer_estado" ruleta/escpos.py` (primera coincidencia) | **456**, bucle **461-467** (`for _ in range(_MAX_BYTES_BASURA)`, `sock.recv(1)`, devuelve el **primer** válido) |
| Llamada Bluetooth a la política | `grep -n "_verificar_lista" ruleta/escpos.py` | **476** (definición) y **482**: `verificar_estado(lambda comando: self._leer_estado(sock, comando), self.mac)` |
| `_leer_estado` por **USB** | `grep -n "def _leer_estado" ruleta/escpos.py` (segunda coincidencia) | **631**, escritura del comando **633-638**, bucle **639-647** |
| Consulta del diagnóstico | `grep -n "def consultar_papel" ruleta/escpos.py` | **649**, firma `-> tuple[int \| None, int \| None]`; el `return` de dos bytes en **661-662** |
| `imprimir` por USB | `grep -n "def imprimir" ruleta/escpos.py` (la de `ImpresoraArchivo`) | **666**; la llamada a la política en **680**: `verificar_estado(lambda comando: self._leer_estado(f, comando), self.ruta)` |

### 4.2 `ruleta/__main__.py` (558 líneas hoy)

| Ancla | Cómo encontrarla | Línea hoy, literal |
|---|---|---|
| Detector del servicio | `grep -n "def servicio_activo" ruleta/__main__.py` | **90** |
| Traductor del diagnóstico | `grep -n "def interpretar_estado_papel" ruleta/__main__.py` | **346**: `def interpretar_estado_papel(papel: int \| None, estado: int \| None) -> tuple[bool, str]:` |
| Rama «no contestó» | `grep -n "no contestó a la consulta" ruleta/__main__.py` | **348-350** |
| Rama «sin papel» | `grep -n "BITS_SIN_PAPEL" ruleta/__main__.py` | **351**: `if papel is not None and papel & escpos.BITS_SIN_PAPEL:` |
| Rama «fuera de línea» | `grep -n "BIT_FUERA_DE_LINEA" ruleta/__main__.py` | **353** |
| Rama «poco papel» **suelta** | `grep -n "BITS_POCO_PAPEL" ruleta/__main__.py` | **355**: `if papel is not None and papel & escpos.BITS_POCO_PAPEL:` |
| Rama final | `grep -n "hay papel y está en línea" ruleta/__main__.py` | **357** |
| Compuerta del servicio en el diagnóstico | `grep -n "no se consulta el estado de la impresora" ruleta/__main__.py` | **418**; el `elif servicio_activo():` que la gobierna está en la **417** |
| Llamada real | `grep -n "consultar_papel()" ruleta/__main__.py` | **422**: `papel, estado = escpos.ImpresoraArchivo(cfg.impresora.ruta).consultar_papel()` |
| Uso del traductor | `grep -n "interpretar_estado_papel(" ruleta/__main__.py` | **426**: `bien, linea = interpretar_estado_papel(papel, estado)` |
| Censo de aciertos | `grep -c "\[ok\]" ruleta/__main__.py` | **8** (en el **código**; en la **salida** son otra cosa, ver D4) |

### 4.3 `ruleta/app.py` (277 líneas hoy) — **solo lectura en esta fase**

| Ancla | Cómo encontrarla | Línea hoy, literal |
|---|---|---|
| Construcción del transporte USB | `grep -n 'tipo == "archivo"' -A 3 ruleta/app.py` | **56-59**; la 59 pasa `consultar_estado=imp.consultar_estado` y **no** pasa `timeout_estado` |
| Envío del boleto | `grep -n "self.impresora.imprimir(datos)" ruleta/app.py` | **240** |
| **Reversión del premio** | `grep -n "except ErrorConexion" -A 2 ruleta/app.py` | **245-247**: `self.inv.revertir(boleto)` y `log.error("Boleto %s NO impreso (premio devuelto al inventario): %s", …)` |

### 4.4 Pruebas

| Ancla | Cómo encontrarla | Línea hoy |
|---|---|---|
| Doble de socket Bluetooth | `grep -n "class SocketFalso" tests/test_escpos.py` | **177**; el `if` que hay que ampliar, en **217** |
| Pruebas de estado por Bluetooth | `grep -n "def test_sin_papel_no_envia_el_boleto\|def test_fuera_de_linea_no_envia_el_boleto\|def test_con_papel_imprime_y_restaura_timeout\|def test_poco_papel_solo_avisa\|def test_impresora_que_no_responde_al_estado_imprime_igual\|def test_byte_de_estado_invalido_se_ignora\|def test_consulta_desactivada_no_pregunta" tests/test_escpos.py` | **253**, **262**, **270**, **279**, **284**, **289**, **295** en la clase de **Bluetooth**; ese mismo `grep` devuelve además **476**, **492** y **500**, los homónimos de la clase de **USB** (`test_sin_papel_no_envia_el_boleto`, `test_fuera_de_linea_no_envia_el_boleto` y `test_poco_papel_solo_avisa`, este último con el vector **`0x16`** en la **501**, frente al `0x1e` del de Bluetooth en la **280**) |
| Doble del nodo `usblp` | `grep -n "class DispositivoFalso" tests/test_escpos.py` | **419**; constructor **427**, `read` **443**, `hay_datos` **449** |
| Clase de pruebas por USB | `grep -n "class TestImpresoraArchivoUSB" tests/test_escpos.py` | **461**; fábrica `impresora()` en **467-474** |
| Los **doce** usos del doble | `grep -n "DispositivoFalso(" tests/test_escpos.py` | **477**, **486**, **493**, **501**, **507**, **515**, **520**, **527**, **534**, **541**, **547**, **552** |
| Golden **anti-cuelgue** | `grep -n "def test_cada_lectura_tiene_limite_de_tiempo" -A 4 tests/test_escpos.py` | **513-517**, con `self.assertEqual(disp.esperas, [1.0, 1.0])` |
| Goldens del traductor | `grep -n "class TestInterpretarEstadoPapel" tests/test_instalacion.py` | **392**; los cinco casos en **393**, **397**, **401**, **406** y **410** |
| Golden que **hoy consagra la lectura equivocada** | `grep -n "def test_poco_papel_avisa_sin_ser_error" -A 3 tests/test_instalacion.py` | **406-408**, con el vector `cli.interpretar_estado_papel(0x16, 0x12)` |
| **Golden de la reversión del premio** | `grep -n "def test_error_conexion_revierte_el_premio" tests/test_app.py` | **252**, cuerpo **252-263** |
| Censo total de la suite | `python -m unittest discover -s tests -t .` | **`Ran 194 tests` / `OK`** |

### 4.5 Documentos

| Ancla | Cómo encontrarla | Línea hoy |
|---|---|---|
| `README` §9, solución de problemas | `grep -n "^## 9. Solución de problemas" README.md` | **462**; la viñeta del papel, en **472-477** |
| `README` §5, punto 8 «Se acabó el papel» | `grep -n "Se acabó el papel" README.md` | **287-293** |
| Ficha **F-091** | `grep -n "^## F-091" docs/fichas.md` | **1123**; su línea de **Estado**, en **1158** (una sola línea larguísima, ya actualizada el 2026-09-15 con la prueba de las 13:29) |
| Ficha **F-186** | `grep -n "^## F-186" docs/fichas.md` | **2895**; su **Estado** en **2917-2923** |
| Ficha **F-190** | `grep -n "^## F-190" docs/fichas.md` | **3015** (título), **3024** («Qué pasa», con el sensor *near-end* que resultó falso) y **3036** (**Estado**, ya con una nota del 2026-09-15) |
| **Última ficha existente** | `grep -n "^## F-" docs/fichas.md \| tail -1` | Antes de esta fase era la **F-250** (línea 4929, «Con el rollo agotado el kiosco emite, descuenta y da por impreso un boleto que no sale», con el archivo acabando en la 4979). **Con la ficha de apertura ya añadida, la última es la F-251, en la 4981, y el archivo acaba en la 5040.** Toda ficha nueva va **detrás**, y el número se vuelve a re-grepear |
| Mapa de anclas de la Fase 2 (**queda falso**) | `grep -n "Bytes y bits del estado en tiempo real" docs/planes/fase-2-impresora.md` | **2392** |
| Pendientes de la Fase 2 | `grep -n "Aviso de «sin papel» por USB\|Cambiar el rollo de papel" docs/planes/fase-2-impresora.md` | **2734** y **2739** |
| Capacitación del personal, Fase 4 | `grep -n "qué avisa y qué no avisa el programa" docs/planes/fase-2-impresora.md` | **2774** |
| Acta de la Fase 2, tabla de cierre | `grep -n "avisando de \*\*poco papel\*\*" docs/actas/2026-09-11-fase-2.md` (**dos** coincidencias: **100** y **395**) | La de esta fila es la **395**: `\| Impresora \| por **cable USB**, avisando de **poco papel** (sensor *near-end*) \|`; la fila del repuesto es la **396**. La **100** es la bitácora y **tampoco se reescribe** |
| Bitácora de la Fase 3 | `grep -n "aviso falso de poco papel\|leer la respuesta FRESCA" docs/planes/fase-3-botones.md` (**cuatro** coincidencias: 28, 71, 73 y 99) | Las casillas que esta fase cierra son la **71** (fila 21) y la **73** (fila 21-ter). La **28** es el estado global y la **99** la §1 del mismo plan |

---

## 5. Pasos

### Paso 0 · Re-grep del mapa de anclas

**QUIÉN:** agente.

**QUÉ HACER.** Antes de la primera edición, correr **todos** los `grep -n` de la
§4 y pegar la salida en el archivo de hechos de la sesión (scratchpad), no en el
repositorio.

**CRITERIO DE ACEPTACIÓN.** Cada ancla de la §4 aparece **con tantas coincidencias como declara su fila** (varias declaran dos, cuatro o doce) y con
el **texto** que la tabla dice (el número de línea puede haber cambiado; el
texto no). Además, sobre el árbol limpio:

```bash
git status --porcelain          # vacío
python -m unittest discover -s tests -t .   # Ran 194 tests ... OK
```

**SI FALLA.** Si un texto cambió o desapareció, **detenerse y preguntar** (§10).
Que la suite no dé 194 antes de empezar significa que el punto de partida no es
el que dice este plan: tampoco se sigue.

---

### Paso 1 · `ruleta/escpos.py`

**QUIÉN:** ejecutor.

**QUÉ HACER.**

1. **Constantes.** Añadir `CMD_ESTADO_CAUSA = b"\x10\x04\x02"` junto a las otras
   dos, con comentario de sus bits. Añadir `BIT_TAPA_ABIERTA = 0x04`,
   `BIT_FIN_DE_PAPEL = 0x20` y `BIT_ERROR_IMPRESORA = 0x40` junto a los otros
   bits. Corregir el comentario de `CMD_ESTADO_PAPEL` para que diga que los bits
   2-3 solo son legales **en pareja** (`00` u `11`) y el de `BITS_POCO_PAPEL`
   para que diga que hacen falta **los dos** bits. Añadir los cinco topes de D1
   con un comentario que cite la medición del **2026-09-15**. **Borrar**
   `_MAX_BYTES_BASURA`.
2. **`leer_estado_fresco`** (función de módulo nueva, junto a `es_estado_valido`
   y `verificar_estado`, con docstring en español que explique **por qué** el
   último y no el primero). Drena, escribe, lee y devuelve el último válido o
   `None`. Topes duros de bytes **y** de tiempo.
3. **Los dos `_leer_estado`** pasan a delegar en ella: el de Bluetooth con
   `sock.sendall` y un `recv(1)` con `settimeout` por espera; el de USB con la
   escritura completa que ya tiene (el bucle `while pendiente:`) y
   `self._esperar(f, espera)` + `f.read(1)`. El `finally` que restaura el
   `timeout` del socket en Bluetooth **se conserva**.
4. **`verificar_estado`** pasa a preguntar las tres cosas en el orden de D2, con
   los textos de D2 y la máscara estricta de D3. El `log.debug` final se
   dispara cuando **las tres** son `None`. **El docstring se actualiza** para que
   describa la política real (hoy dice «Pregunta por el papel y por la línea»).
5. **Propiedad que hay que conservar sin tocarla:** si la **escritura** del
   comando falla, el `OSError` **sigue subiendo**, para que lo conviertan en
   `ErrorConexion` los dos sitios que ya lo hacen —`consultar_papel` en su
   `except OSError` y `imprimir` con `enviados == 0`—. `leer_estado_fresco`
   **no** captura el error de escritura; solo devuelve `None` cuando nadie
   contesta.

**CRITERIO DE ACEPTACIÓN.**

```bash
grep -c "CMD_ESTADO_CAUSA" ruleta/escpos.py            # >= 2 (definición y uso)
grep -c "_MAX_BYTES_BASURA" ruleta/escpos.py           # 0
grep -n "== BITS_POCO_PAPEL" ruleta/escpos.py          # 1 línea, con paréntesis
grep -c "while True" ruleta/escpos.py                  # 0
python -c "import ruleta.escpos"                       # sin error
```

Y, leído a ojo: **ningún** bucle de lectura sin tope de bytes **y** de tiempo.

**SI FALLA.** Si al escribirlo aparece que `verificar_estado` la usa alguien más
(hoy solo `ImpresoraBluetooth._verificar_lista` y `ImpresoraArchivo.imprimir`),
**detenerse y preguntar**: el plan da por cierto que son dos.

---

### Paso 2 · `ruleta/__main__.py`

**QUIÉN:** ejecutor.

**QUÉ HACER.**

1. `ImpresoraArchivo.consultar_papel()` (en `escpos.py`, pero es el mismo
   cambio) devuelve **tres** bytes, preguntando en el orden de D2 y con la firma
   anotada `-> tuple[int | None, int | None, int | None]`. Su docstring sigue
   diciendo que **no interpreta nada**.
2. `interpretar_estado_papel(papel, causa, estado)` con las **siete** ramas de
   D4, en ese orden, cada una protegida por su `is not None`, y la máscara
   estricta con paréntesis.
3. La llamada del diagnóstico (hoy `__main__.py:422` y `:426`) desempaqueta y
   pasa los tres.

**CRITERIO DE ACEPTACIÓN.**

```bash
grep -n "def interpretar_estado_papel" ruleta/__main__.py   # firma con tres parámetros
grep -n "== escpos.BITS_POCO_PAPEL" ruleta/__main__.py      # 1 línea, con paréntesis
grep -c "\[ok\]" ruleta/__main__.py                         # sigue siendo 8
grep -c "\[!!\]" ruleta/__main__.py                         # hoy 18; tras el cambio, 20
python -m ruleta --help                                     # sin excepción
```

**SI FALLA.** Si `consultar_papel` tiene más llamadores de los dos conocidos
(`__main__.py:422` y las pruebas), **detenerse y preguntar**.

---

### Paso 3 · `tests/test_escpos.py`

**QUIÉN:** ejecutor.

**QUÉ HACER.**

1. **`SocketFalso`**: ampliar el `if` de la línea 217 para que
   `CMD_ESTADO_CAUSA` cuente como **consulta** y no como datos del boleto.
2. **`DispositivoFalso`**: convertirlo a **respuestas por comando** (diccionario
   `{comando: bytes}`, como `SocketFalso`), de modo que **no suelte nada hasta
   que se le escriba un `DLE EOT`**. Es el doble de la «EPSON normal» de D5(e).
   Conservar `acepta`, `limite`, `escrito`, `lecturas`, `esperas` y `cerrado`,
   que los usan otros goldens. Adaptar **los doce** usos listados en la §4.4.
3. **`DispositivoFlujo`** (nuevo): el doble de la AOMU descrito en D5, con
   `atraso` inicial de bytes viejos y `viejos` bytes de transición tras cada
   comando; su `read` **nunca** devuelve vacío y su `hay_datos` **siempre**
   devuelve `True` (y anota la espera recibida).
4. **Goldens (a) a (g)** de D5, con los vectores medidos. Los que comparan lo
   escrito lo comparan **entero**.
5. **`test_cada_lectura_tiene_limite_de_tiempo`**: reescrito para que siga
   mordiendo con el drenado y las tres preguntas (§3, trampa 9).
6. **`test_bytes_invalidos_se_descartan_e_imprime`** (línea 519, hoy anclado a
   `_MAX_BYTES_BASURA = 4` con `disp.lecturas == 4`): re-anclarlo a
   `_MAX_BYTES_RESPUESTA`, comprobando que con un flujo de bytes que **nunca**
   pasan `es_estado_valido` la función devuelve `None`, **imprime igual** y
   **no lee más de `_MAX_BYTES_RESPUESTA` bytes por comando**.
7. **`test_consultar_papel_devuelve_los_dos_bytes`** (línea 546): pasa a
   comprobar **tres** bytes, con el nombre cambiado en consecuencia.

**CRITERIO DE ACEPTACIÓN.**

```bash
python -m unittest tests.test_escpos -v 2>&1 | tail -3     # OK
grep -c "assertLogs\|assertNoLogs" tests/test_escpos.py    # >= 4 (los de D5(g))
grep -c "class DispositivoFlujo" tests/test_escpos.py      # 1
grep -c "DispositivoFalso(b" tests/test_escpos.py          # 0  (ya no hay cola plana)
```

**SI FALLA.** Si un golden solo pasa **relajando** un assert (cambiar una
igualdad por un `assertIn`, o quitar una comprobación), **no se relaja**: se
arregla el código o se detiene y se pregunta.

---

### Paso 4 · `tests/test_instalacion.py`

**QUIÉN:** ejecutor.

**QUÉ HACER.** Los **cinco** goldens de `TestInterpretarEstadoPapel` pasan a
tres bytes. Además:

- `test_poco_papel_avisa_sin_ser_error` cambia su vector de **`0x16` a `0x1e`**
  (es el único golden de todo el repositorio que hoy se pone en rojo con la
  máscara estricta, y hoy **consagra la lectura equivocada**).
- Se añade el caso del byte **realmente medido**: `0x16` en la ranura del papel
  ya **no** es poco papel, y con `causa` y `estado` sanos la línea es la de
  acierto.
- Se añaden los casos nuevos de D4: **fin de papel por `DLE EOT 2`** (`0x32`),
  **tapa abierta** (`0x16` en la ranura de la causa, que es justo el byte
  rezagado que este arreglo evita) y **error de impresora**.
- Se añade el golden del **orden de las ramas** (mutación **M9**): con
  `papel = 0x7e` —bits 5-6 **y** bits 2-3 encendidos a la vez— la línea tiene que
  ser la de **SIN PAPEL**, no la de poco papel.

**CRITERIO DE ACEPTACIÓN.**

```bash
python -m unittest tests.test_instalacion 2>&1 | tail -3   # OK
# El golden que hoy consagra la lectura equivocada tiene que estrenar vector:
grep -n "def test_poco_papel_avisa_sin_ser_error" -A 3 tests/test_instalacion.py
#   -> el byte del papel es 0x1e, NO 0x16
# Y ninguna llamada puede quedarse con la firma vieja de dos argumentos:
grep -n "interpretar_estado_papel(" tests/test_instalacion.py ruleta/__main__.py
#   -> todas con tres argumentos (o tres parámetros, en la definición)
```

Y el **censo por igualdad** de los nombres de `TestInterpretarEstadoPapel`
escrito en el acta: los cinco de hoy más los nuevos, uno por uno.

**SI FALLA.** Si algún golden de este archivo distinto de
`test_poco_papel_avisa_sin_ser_error` se pone en rojo **por el cambio de
código** (no por el cambio de firma), es que el comportamiento cambió más de lo
que dice este plan: **detenerse y preguntar**.

---

### Paso 5 · `tests/test_app.py`

**QUIÉN:** ejecutor.

**QUÉ HACER.** **Nada de código nuevo.** Añadir al golden que ya existe,
`test_error_conexion_revierte_el_premio` (línea 252), **un comentario** que diga
que es el que sostiene la reversión del premio de la Fase 4a y que la mutación
**M10** lo pone en rojo. **No se duplica** el caso.

**CRITERIO DE ACEPTACIÓN.**

```bash
grep -c "def test_error_conexion_revierte_el_premio" tests/test_app.py   # 1, no 2
python -m unittest tests.test_app 2>&1 | tail -3                        # OK
```

**SI FALLA.** Si al leerlo resulta que **no** comprueba que el premio vuelve al
inventario, entonces sí hay que escribir el golden, y hay que decirlo en el acta
como desviación del plan.

---

### Paso 6 · Suite verde en la PC

**QUIÉN:** ejecutor.

**QUÉ HACER.**

```bash
python -m unittest discover -s tests -t .
```

**CRITERIO DE ACEPTACIÓN.** Termina en **`OK`**, con **cero** `FAILED`, y el
número de pruebas es **estrictamente mayor que 194**. El ejecutor **escribe el
número exacto** en el archivo de hechos y en el acta; este plan **no lo predice**
a propósito, porque un número inventado se convierte en un golden falso.
Comprobar también que no quedaron finales de línea de Windows:

```bash
grep -lc $'\r' ruleta/*.py tests/*.py docs/planes/fase-4a-papel.md   # sin resultados
```

**SI FALLA.** Un fallo **se diagnostica, no se parchea en caliente**: se lee el
`traceback` entero, se decide si el equivocado es el código o el golden y, si es
el golden, se comprueba primero que su versión nueva **sigue mordiendo**.

---

### Paso 7 · Mutaciones M1-M10, **todas en rojo**

**QUIÉN:** ejecutor.

**QUÉ HACER.** Una por una, **sobre una copia del repositorio**, nunca sobre el
árbol de trabajo:

```bash
# desde la raíz del repositorio, en Git Bash
cp -r . /tmp/mut-M1 && cd /tmp/mut-M1     # o la carpeta del scratchpad de la sesión
# aplicar la mutación con un editor o con sed, correr la suite y anotar
python -m unittest discover -s tests -t . 2>&1 | tail -20
cd - && rm -rf /tmp/mut-M1
```

Se anota, para cada una: **qué se cambió**, **cuántas pruebas fallaron** y **el
nombre exacto** de al menos una que cae.

**CRITERIO DE ACEPTACIÓN.** Las **diez** de la §6 terminan en `FAILED`, y para
cada una se conoce el nombre del test que cae. **Cero supervivientes.**

**SI FALLA.** Una mutación que sobrevive en verde **no se acepta**: significa que
el golden correspondiente no muerde. Se arregla el golden y se repite la
mutación. Si tras arreglarlo sigue sobreviviendo, **detenerse y preguntar**.

---

### Paso 8 · Documentos

**QUIÉN:** ejecutor.

**QUÉ HACER.** En el **mismo cambio** que el código. Cada edición se hace
**re-grepeando** su ancla (§4.5), nunca por número de línea.

| Id | Dónde | Qué tiene que quedar dicho |
|---|---|---|
| **C1** | `docs/fichas.md`, **F-091**, su línea de **Estado** | El fragmento «así que la consulta funciona de verdad por cable y lanzada desde systemd» **es falso y hay que corregirlo**: lo único demostrado por cable es que el **nodo acepta la escritura del comando**, no que la respuesta leída sea la suya. **Ojo:** esa línea **ya no termina ahí** (el 2026-09-15 se le añadió la prueba de las 13:29): hay que **re-grepear el fragmento**, no cortar por el final |
| **C1-bis** | La misma línea de **F-091** | Añadir el cierre: el camino «sin papel» **ya está medido** (falló el 2026-09-15) y **queda arreglado en esta fase**, con el commit y la fecha reales. La parte de `reintentos`, `timeout_seg` y las llaves de ritmo **sigue abierta** |
| **C2** | `docs/fichas.md`, **F-190**, título (línea 3015) | El título de hoy afirma un hecho falso. Tiene que decir que **el aviso de «poco papel» del 2026-09-11 era falso** y que el programa leía la respuesta de otra pregunta |
| **C3** | `docs/fichas.md`, **F-190**, «Qué pasa» (línea 3024) | **No fue el sensor.** Corrección fechada **encima** de la redacción original, que **se conserva**: flujo continuo, respuesta de la pregunta anterior, `0x16` es la respuesta sana de `DLE EOT 1`, y **lo medido el 2026-09-15**: `DLE EOT 4` contesta `0x12` **incluso con el rollo fuera**, así que en este clon **no** hay sensor de papel útil en esa pregunta |
| **C4** | `docs/fichas.md`, **F-190**, **Estado** (línea 3036) | Ya tiene una nota del 2026-09-15; **se le añade** —sin borrar nada— que el diagnóstico quedó cerrado y que lo único vivo es **tener un rollo de repuesto junto a la Pi** |
| **C5** | `docs/planes/fase-2-impresora.md`, tabla de pendientes, fila «Cambiar el rollo de papel» (2739) | Pasa a ser **«Tener un rollo de repuesto»**: el aviso del 2026-09-11 al 2026-09-13 se midió **falso** y el rollo puesto sirve |
| **C6** | `docs/planes/fase-2-impresora.md`, fila «Aviso de «sin papel» por USB» (2734) | Hoy dice que funciona en hardware real. Es **falso**: lo que se probó es que el nodo acepta la consulta. Y el caso extremo **ya se probó, el 2026-09-15, y falló** (**F-091**, **F-250**); esta fase lo arregla |
| **C7** | `docs/actas/2026-09-11-fase-2.md` | **La fila 395 NO se toca.** Se añade una **nota fechada** inmediatamente **debajo** de esa tabla (después de la 396) diciendo que aquel «poco papel (sensor *near-end*)» era falso y remitiendo a **F-190** y a esta fase. Las actas son evidencia: **no se reescriben** |
| **C8** | `docs/fichas.md`, **F-186**, al final de su **Estado** | Con la lectura estricta, el camino «poco papel» **ya no se dispara** en esta impresora. **El censo hay que volver a medirlo** (§5, Paso 10), no copiarlo: se escribe el número que salga del diagnóstico real en la Pi |
| **C9** | `docs/planes/fase-2-impresora.md`, §6, fila «Bytes y bits del estado en tiempo real» (2392) | **Re-medir** los números de línea de `escpos.py` y de `__main__.py` **después** de las ediciones de esta fase y escribirlos. Hoy dice «58-60 y 64-66, 104, 118-125 y 661-662» y «(351-355)», y esta fase los mueve **todos** |
| **C10** | `README.md` §9 | **Viñeta nueva**, para personal no técnico: **si se acaba el papel, el kiosco no juega**: el LED parpadea rápido, no sale boleto y **el premio vuelve al inventario**; se pone el rollo, se cierra bien la tapa y se vuelve a jugar. Y: **un aviso de «poco papel» solo puede venir de una impresora con sensor de verdad**; esta no lo tiene, así que si aparece, **no hay que comprar rollo**: hay que abrir la tapa y mirar |
| **C11** | `README.md` §5, punto 8 | Ponerlo al día con lo mismo, sin contradecir al §9 |
| **C12** | `docs/planes/fase-3-botones.md`, bitácora, filas **21** y **21-ter** | Marcarlas cuando esta fase cierre, con la fecha y el commit reales. **Mientras la fase no esté cerrada, no se marcan** |
| **C13** | `docs/fichas.md`, **F-250** | Su **Estado** pasa a **resuelta**, con la fecha, el commit y **la evidencia de la prueba en vivo del Paso 11**. Si la prueba en vivo no llega a hacerse, **se queda abierta** y se dice por qué |
| **C14** | `docs/fichas.md`, fichas **nuevas** | A continuación de la última existente (**re-grep**: hoy la última es **F-250**). Como mínimo: la ficha de **apertura de esta fase** (**F-251**, ya escrita al redactar el plan) y las que salgan de la cadena |

**CRITERIO DE ACEPTACIÓN.**

```bash
# Hoy hay 3 menciones de "sensor *near-end*" en docs/fichas.md: la de F-190:3024
# (la afirmación falsa que hay que corregir) y las dos de F-251, que ya dicen que
# es falsa. Tras C3 no puede quedar ninguna que lo afirme como cierto.
grep -n "sensor \*near-end\*" docs/fichas.md
grep -n "^## F-" docs/fichas.md | tail -1             # la última ficha, con su número
# El acta del 2026-09-13 no existe. Las únicas menciones legítimas son las de
# este plan, que hablan de que NO existe; fuera de él, ninguna:
grep -rn "2026-09-13-poco-papel" --include=*.md --include=*.py . \
  | grep -v "docs/planes/fase-4a-papel.md"            # sin resultados
```

Y la comprobación que de verdad importa: **cada afirmación editada tiene detrás
una medición pegada en el archivo de hechos**, con su fecha.

**SI FALLA.** Si al re-grepear un ancla el texto ya no está, **detenerse y
preguntar**. Si una corrección exigiera reescribir una fila de un acta,
**no se hace**: va como nota fechada.

---

### Paso 9 · Commit compuertado

**QUIÉN:** **agente de commit** (nadie más toca git que modifique).

**QUÉ HACER.** Conjunto de archivos **permitido por adelantado**:

```
ruleta/escpos.py
ruleta/__main__.py
tests/test_escpos.py
tests/test_instalacion.py
tests/test_app.py
docs/planes/fase-4a-papel.md
docs/actas/2026-09-15-hechos-medidos-fase-4a.md
docs/fichas.md
docs/planes/fase-2-impresora.md
docs/planes/fase-3-botones.md
docs/actas/2026-09-11-fase-2.md
README.md
```

**Nada más.** `git add` **solo por rutas explícitas**; nada pendiente de push
antes de commitear; compuerta por conjunto de hashes (exactamente uno, igual a
`HEAD`) antes del push; **nunca** con un deploy en vuelo; **nunca** saltándose
hooks.

**CRITERIO DE ACEPTACIÓN.** Un **verificador de push distinto** del que
commiteó informa, contra el remoto: hash, rama, **conjunto de archivos por
igualdad** con la lista de arriba y árbol limpio. **Nada se da por publicado
hasta ese informe.**

**SI FALLA.** Se reporta y se detiene. No se reintenta a ciegas ni se fuerza.

---

### Paso 10 · Deploy en la Pi

**QUIÉN:** agente (y el usuario, para encender la Pi y el punto de acceso).

**QUÉ HACER.** Con la Pi encendida y alcanzable:

```bash
# 0. Que no haya sondas vivas del 2026-09-13 robando bytes (§3, trampa 16)
ssh ruleta 'pgrep -af "sonda-papel.py|pasivo.py|estado-impresora.py" ; echo FIN'
ssh ruleta 'rm -f /tmp/sonda-papel.py /tmp/pasivo.py /tmp/estado-impresora.py /tmp/*.log'

# 1. Parar el kiosco y traer el código
ssh ruleta 'sudo systemctl stop ruleta'
ssh ruleta 'cd ~/ruleta && git status --porcelain && git pull --ff-only && git rev-parse HEAD'

# 2. La suite, en la Pi
ssh ruleta 'cd ~/ruleta && python3 -m unittest discover -s tests -t . 2>&1 | tail -3'

# 3. El diagnóstico, CON EL SERVICIO DETENIDO (si no, no pregunta nada)
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico ; echo EXIT=$?'

# 4. Arrancar y observar
ssh ruleta 'sudo systemctl restart ruleta ; sleep 5 ; systemctl is-active ruleta'
ssh ruleta 'journalctl -u ruleta -n 40 --no-pager'
```

**CRITERIO DE ACEPTACIÓN**, todo por igualdad:

1. `git status --porcelain` en la Pi **sin cambios locales** que impidan el
   `pull`, y `git rev-parse HEAD` **igual** al hash que publicó el Paso 9.
2. La suite en la Pi termina en **`OK`**, con **el mismo número** de pruebas que
   en la PC.
3. El diagnóstico sale con **`EXIT=0`**, **cero `[!!]`**, **cero avisos de poco
   papel** y la línea `[ok] la impresora contesta: hay papel y está en línea`.
   Se **cuentan** los aciertos de la salida y el número se escribe en **F-186**
   (C8) y en el acta.
4. El servicio queda **`active`**, con **`NRestarts=0`**, el journal con
   `Inventario impreso`, `GPIO listo: jugar=17 habilitar=27 led=22` y
   `Lista. Esperando jugadas.`, y **cero** `ERROR`, `Traceback` y **cero**
   `reporta poco papel`.

**SI FALLA.**

- `git pull --ff-only` rechazado por cambios locales: **se reporta y se
  detiene**. **No** se hace `checkout --`, `stash` ni `reset` (§8).
- La Pi inalcanzable: **requiere al usuario** (encender la Pi y el punto de
  acceso móvil de Windows). No se toca nada más mientras tanto.
- El diagnóstico con `[!!]`: se lee **cuál**, y si dice «tapa abierta» con la
  tapa cerrada, es exactamente la trampa 5 de la §3: el drenado no está
  funcionando. **Detenerse y preguntar.**

---

### Paso 11 · **PRUEBA EN VIVO sin papel**, con el usuario

**QUIÉN:** **usuario** (el papel) + agente (el journal). Es el criterio que de
verdad cierra la fase: es el mismo experimento que el 2026-09-15 salió en rojo.

**QUÉ HACER.**

1. **Usuario:** con el servicio `active`, **sacar el rollo** de la impresora y
   **cerrar la tapa**. Anotar la hora.
2. **Usuario:** una jugada normal (mesero sostiene HABILITAR, cliente pulsa
   JUGAR).
3. **Agente:** leer el journal y los datos:
   ```bash
   ssh ruleta 'journalctl -u ruleta --since "-3 min" --no-pager'
   ssh ruleta 'cd ~/ruleta && tail -5 datos/boletos.csv && cat datos/estado.json'
   ```
4. **Usuario:** **reponer el rollo**, cerrar la tapa y **jugar otra vez**.
5. **Agente:** volver a leer journal y datos.

**CRITERIO DE ACEPTACIÓN** (los cinco, y los cinco se miden, no se suponen):

1. El journal dice **`Boleto NNNNN NO impreso (premio devuelto al inventario): la impresora /dev/ruleta-impresora no tiene papel`**. Nada de `poco papel`.
2. **No aparece** ninguna línea `Boleto NNNNN impreso`.
3. `datos/boletos.csv` **no** marca ese folio como impreso, y **el premio vuelve
   al inventario** (se compara el conteo del premio antes y después, por
   igualdad).
4. **Nada queda retenido en la impresora**: al reponer el papel **no sale ningún
   boleto solo**. Este es el punto que distingue el arreglo del comportamiento
   del 2026-09-15, donde la impresora soltó el 00009 al reponer.
5. La jugada del punto 4, con papel, **imprime un boleto normal**, y el journal
   dice `Boleto NNNNN impreso`.

**SI FALLA.**

- Si sale el aviso de «tapa abierta» con la tapa cerrada: el drenado no muerde
  en hardware real. **Se reporta con el journal entero y se detiene**; no se
  parchea en caliente.
- Si el boleto se vuelve a dar por impreso: el arreglo **no funciona en
  hardware**, aunque la suite esté verde. **Se reporta, no se rehace**: se
  diagnostica primero, con el mismo método de la sonda del 2026-09-15.
- Si la impresora retiene el trabajo (punto 4 en rojo) pero el resto está bien,
  es una **victoria parcial** y se anota como tal: quiere decir que algún byte
  llegó al nodo antes de la excepción.

**Coste en papel y folios.** La jugada en rojo **no** debe consumir folio útil
(el folio se gasta, el premio vuelve); la jugada con papel gasta un boleto de
verdad. Las dos se anotan para el reinicio del inventario de la Fase 4
(**F-243**).

---

### Paso 12 · Cierre

**QUIÉN:** ejecutor (documentos) + orquestador (memoria).

**QUÉ HACER.** Acta `docs/actas/2026-09-15-fase-4a.md` **escrita desde el
archivo de hechos de la sesión, nunca de memoria**, con: las salidas reales del
Paso 10, el journal del Paso 11, la **tabla de mutaciones con sus resultados
medidos**, el número exacto de pruebas y las desviaciones. Fichas al día
(**F-091**, **F-186**, **F-190**, **F-250**, más las nuevas). Bitácora de la §0
marcada con evidencia. Memoria del proyecto: la actualiza el orquestador.

**CRITERIO DE ACEPTACIÓN.** El acta existe, la bitácora no tiene ninguna casilla
marcada sin evidencia pegada, y un **agente distinto** (escriba) confirma que
cada cambio del diff real está enrutado a su documento. Y el cierre entra en un
**segundo commit, solo de documentos**, con su conjunto de archivos fijado por
adelantado —`docs/actas/2026-09-15-fase-4a.md`, `docs/fichas.md`,
`docs/planes/fase-4a-papel.md` (la bitácora de la §0) y
`docs/planes/fase-3-botones.md` (filas 21 y 21-ter)—, hecho por el **agente de
commit** con los mismos gates del Paso 9 y comprobado contra el remoto por un
**verificador distinto**: hasta ese informe, el cierre no está publicado.

**SI FALLA.** Si al escribir el acta aparece una casilla marcada sin evidencia,
**se desmarca**.

---

## 6. Tabla de mutaciones

**Diez mutaciones, todas por copia, todas en rojo antes de aceptar la fase**
(D6). La columna «Qué debería caer» es una **predicción del plan, no una
medición**: el ejecutor la comprueba corriendo la suite de verdad y **escribe el
nombre real** del test que cae. Si cae otro, se anota el que cayó; si **no cae
ninguno**, la fase se detiene (§5, Paso 7).

| Id | Mutación (sobre una copia) | Qué debería caer, y por qué |
|---|---|---|
| **M1** | **Quitar el drenado** de `leer_estado_fresco` (escribir y leer directamente) | Los goldens con `DispositivoFlujo`, empezando por el de **«con papel»**: sin drenar, los 64 bytes salen del **atraso** y todos valen `0x16`; `0x16` tiene el **bit 2** encendido, que en `DLE EOT 2` es «tapa abierta», así que el boleto **no se imprimiría** con la tapa cerrada. Es la trampa 5 de la §3, convertida en golden |
| **M2** | Devolver el **primer** byte válido en vez del **último** | Los mismos goldens de flujo: el primero es siempre el de la pregunta **anterior**. Es exactamente el defecto que esta fase arregla |
| **M3** | **Quitar la consulta `DLE EOT 2`** de `verificar_estado` | El golden **(b)**, `EOT2 = 0x32`: sin esa pregunta, `DLE EOT 4` contesta `0x12` y `DLE EOT 1` contesta `0x16`, así que el boleto se imprimiría **sin papel**. Es, literalmente, el boleto 00009 |
| **M4** | `BIT_FIN_DE_PAPEL` de `0x20` a `0x10` | **Ojo, y por eso está escrito:** `0x10` es uno de los **bits fijos** de toda respuesta `DLE EOT`, así que el golden (b) seguiría pasando *por el motivo equivocado*. El que cae es el de **«con papel»**: `0x12 & 0x10` también vale `0x10`, y el kiosco se negaría a imprimir siempre |
| **M5** | Volver a la máscara **suelta** de poco papel en `escpos.py` (`papel & BITS_POCO_PAPEL`) | Los goldens del byte medido **`0x16`** que comprueban que **no** hay aviso, en los **dos** transportes (USB y Bluetooth) |
| **M6** | **Quitar los paréntesis** de la máscara estricta | **MEDIDO el 2026-09-15: no cae ninguna prueba, y no puede caer** (las **214** pasan). En Python `&` liga más fuerte que `==`, así que la mutación deja el **mismo árbol de sintaxis** y **no cambia el comportamiento**; no es que el assert no muerda. Lo que M6 quería proteger lo protege **M5**. Ver §6-bis y ficha **F-252**; si esta tabla se retoca, lo decide el orquestador |
| **M7** | **Borrar entera** la rama del aviso de poco papel (`escpos.py`, las dos líneas del `if` y su `log.warning`) | `test_poco_papel_solo_avisa` en los dos transportes. **Es la mutación que HOY sobrevive en verde** (medido el 2026-09-13: con la rama borrada, 194 pruebas OK). Que caiga es la prueba de que el assert pasó a morder |
| **M8** | `_MAX_BYTES_RESPUESTA` de `64` a `1` | Los goldens con `DispositivoFlujo`: con un solo byte se lee el de la transición (todavía viejo) y se vuelve al defecto de siempre |
| **M9** | En `interpretar_estado_papel`, **mover la rama de poco papel por delante** de la de sin papel | El golden nuevo del **orden**, con `papel = 0x7e` (bits 5-6 **y** 2-3 encendidos): tiene que decir **SIN PAPEL**, no «poco papel» |
| **M10** | En `ruleta/app.py`, **no revertir** el boleto ante `ErrorConexion` (quitar `self.inv.revertir(boleto)`) | `tests/test_app.py::test_error_conexion_revierte_el_premio`. **No se toca `app.py` en la fase**: esta mutación existe para demostrar que la reversión del premio **está protegida por un golden que muerde**, que es la mitad del valor de todo este arreglo |

### 6-bis · Lo que salió **medido** (2026-09-15, PC, Python 3.14.4)

Las diez se corrieron **de verdad**, cada una sobre una copia limpia del
repositorio (`shutil.copytree` sin `.git` ni `__pycache__`), con la suite entera
(`python -m unittest discover -s tests -t .`) y borrando la copia después. La
columna de la izquierda es la de la tabla de arriba; esta es la **medición**, no
la predicción.

**La corrida que manda es la de la tarde del 2026-09-15**, después de la pausa
de las 15:25 y con el árbol ya completo: las diez se volvieron a correr enteras
en vez de dar por buena una tabla que nadie podía comprobar. El script vive en
el scratchpad de la sesión (`mutaciones_fase4a.py`), aplica cada mutación como
una **sustitución de texto única** —si el ancla aparece dos veces **aborta** en
vez de mutar a ciegas— y anota el nombre de todas las pruebas que caen. En las
diez corren las **214** pruebas: ninguna mutación rompe la recolección, así que
lo que cae, cae por conducta. Dos detalles que cambian el conteo y por eso se
escriben: **M2** se aplicó como `if es_estado_valido(dato[0]) and ultimo is
None:` —leer el tramo entero y quedarse con el **primero** válido—, que mide
«primero contra último» sin tocar el número de lecturas; y **M10** se ancló al
`except ErrorConexion as e:` que la precede, porque `self.inv.revertir(boleto)`
aparece **dos** veces en `ruleta/app.py` (la otra es la del `except Exception`
de antes de mandar nada, y mutarla sería otra cosa).

| Id | ¿En rojo? | Pruebas que caen | Una de ellas, con su nombre exacto |
|---|---|---|---|
| **M1** | **sí** | 12 | `TestLecturaFrescaAOMU.test_con_papel_no_avisa_y_escribe_el_boleto_entero` (falla con «tiene la tapa abierta»: el byte rezagado `0x16` tiene el bit 2, que en `DLE EOT 2` es la tapa. Es la trampa 5 de la §3, medida) |
| **M2** | **sí** | 7 | `TestLecturaFrescaAOMU.test_el_tramo_empieza_viejo_y_acaba_con_la_respuesta_nueva` (y las seis que dependen del veredicto: con el primer byte se lee la respuesta de la pregunta **anterior** y el kiosco decide por el byte equivocado) |
| **M3** | **sí** | 17 | `TestLecturaFrescaAOMU.test_fin_de_papel_por_causa_no_escribe_ni_un_byte_del_boleto` (el boleto 00009, convertido en golden) |
| **M4** | **sí** | 21 | `TestLecturaFrescaAOMU.test_con_papel_no_avisa_y_escribe_el_boleto_entero` — **tal y como predecía el plan**: el que cae es el de «con papel», porque `0x12 & 0x10` también vale `0x10` |
| **M5** | **sí** | 3 | `TestImpresoraArchivoUSB.test_el_byte_medido_0x16_no_avisa_de_poco_papel` (y su gemelo de Bluetooth, y `test_poco_papel_de_verdad_avisa_y_el_byte_medido_no`) |
| **M6** | **NO, y no puede** | 0 | **Ninguna: la suite entera pasa (214 OK).** La mutación **no cambia el comportamiento**: en Python `&` liga **más fuerte** que `==`, de modo que `papel & BITS_POCO_PAPEL == BITS_POCO_PAPEL` tiene **el mismo árbol de sintaxis** que la versión con paréntesis (medido con `ast.dump`, 2026-09-15). La trampa 3 de la §3 y la justificación de **D3** afirmaban lo contrario —eso es C, no Python— y **quedan corregidas en este mismo cambio**, igual que la predicción de la fila **M6** de la tabla del §6, que decía «`papel & 1`, y `0x1e & 1 = 0`» y ahora dice lo medido; lo que **no** se ha decidido, porque son decisiones cerradas del orquestador, es si **M6 se retira o se sustituye** y qué pasa con el criterio **7.2**. Los paréntesis **se quedan** —los manda D3 y se leen mejor—, pero son de legibilidad. Lo que M6 quería proteger lo protege **M5**. Ficha **F-252** |
| **M7** | **sí** | 3 | `TestImpresoraBluetooth.test_poco_papel_solo_avisa` — la que **hoy sobrevivía en verde**; con el `assertLogs` ya muerde |
| **M8** | **sí** | 9 | `TestLecturaFrescaAOMU.test_el_tramo_empieza_viejo_y_acaba_con_la_respuesta_nueva` |
| **M9** | **sí** | 1 | `TestInterpretarEstadoPapel.test_sin_papel_gana_a_poco_papel` |
| **M10** | **sí** | 1 | `TestRuleta.test_error_conexion_revierte_el_premio` (`tests/test_app.py`; `ruleta/app.py` **no se tocó** en la fase) |

**Recuento: nueve en rojo y una imposible.** El criterio **7.2** («las diez en
rojo, cero supervivientes») **no se cumple tal y como está escrito**, y el
ejecutor **no lo arregló por su cuenta**: M6 es una decisión cerrada del §6 y el
plan manda **detenerse y preguntar** (§10). Lo decide el orquestador.

---

## 7. Criterios de aceptación de la fase

La Fase 4a está cerrada cuando **todos** estos se cumplen, medidos y pegados en
el acta. Comparación **por igualdad**, no «parecido».

> **NOTA DEL 2026-09-15 (cierre de la fase). Resultado medido, criterio por
> criterio.** Nada de esta sección se reescribe: esto es lo que salió.
>
> - **7.1 Código y pruebas, en la PC: CUMPLIDO.** `Ran 214 tests` / `OK`
>   (eran 194). `grep -c "_MAX_BYTES_BASURA" ruleta/escpos.py` → **0**;
>   `grep -c "while True" ruleta/escpos.py` → **0**; sin retornos de carro en
>   ningún archivo tocado.
> - **7.2 Mutaciones: NO CUMPLIDO tal y como está escrito.** **Nueve en rojo y
>   una imposible.** **M6** no puede ponerse en rojo porque **no cambia el
>   comportamiento**: en Python `&` liga más fuerte que `==` y el árbol de
>   sintaxis es idéntico (medido con `ast.dump`). No es que el assert no muerda;
>   es que no hay nada que morder. Lo que M6 quería proteger lo protege **M5**,
>   que sí cayó. El ejecutor **no lo arregló por su cuenta**: es una decisión
>   cerrada del §6 y el plan manda detenerse y preguntar. Ficha **F-252**;
>   **la decisión de retirar o sustituir M6 sigue siendo del orquestador**.
> - **7.3 Publicación: CUMPLIDO.** Commit
>   **`2a0aba3e01dcd15878579f1d02a64457b1834046`**, verificado contra el remoto
>   por un agente distinto del que commiteó. Con **una desviación anotada**: el
>   conjunto de archivos llevó además `docs/PAUSA-2026-09-15.md`, que no estaba
>   en la lista del Paso 9 (ficha **F-258**).
> - **7.4 En la Pi: CUMPLIDO A MEDIAS.** `HEAD` en la Pi = el hash publicado;
>   **214** pruebas OK, el mismo número que en la PC; servicio `active`,
>   `NRestarts=0`, journal de arranque limpio y **cero** líneas
>   `reporta poco papel`. **Lo que NO se midió es el TERCER PUNTO ENTERO de esta
>   §7.4:** el `python3 -m ruleta diagnostico` con el servicio **detenido** **no
>   se ejecutó**, así que no hay `EXIT=0`, ni «cero `[!!]`», ni la línea
>   `[ok] la impresora contesta: hay papel y está en línea`, ni el **censo de
>   aciertos de la salida** (el de la ficha **F-186**): **nada de eso aparece en
>   el archivo de hechos**. Lo único medido es el censo del **código** (**8**
>   `[ok]` y **20** `[!!]`), que **no** es lo que pide este criterio. Por eso la
>   casilla **10** de la §0 queda en `[~]` y **F-186 no se tocó**.
> - **7.5 La prueba en vivo: CUMPLIDO, los cinco puntos.** 2026-09-15, 21:32.
>   Está detallada en la fila 11 de la §0 y en el §8 del acta.
> - **7.6 Documentos: CUMPLIDO.** En el commit de código entraron **C1, C1-bis,
>   C2 a C11 y C14**, más una nota de **C13** que dejaba **F-250 abierta** a
>   propósito, porque la prueba en vivo aún no se había hecho. **C13 se cierra
>   ahora**: el 7.5 salió en verde, así que **F-250 queda resuelta**. **C12
>   también se hace ahora**, que es justo cuando su propia celda manda hacerlo
>   («marcarlas cuando esta fase cierre»): las filas **21** y **21-ter** de
>   `docs/planes/fase-3-botones.md` quedan marcadas con la fecha y el commit
>   reales, y con ellas la **22** —el «Contexto del producto» de `CLAUDE.md`—,
>   que esta misma pasada cierra. **Comprobado el 2026-09-15 por la noche: C12
>   ya NO queda pendiente.** Las filas **21** y **21-ter** de
>   `docs/planes/fase-3-botones.md` están marcadas `[x]` —21 con
>   **2026-09-15 21:26:42** y 21-ter con **2026-09-15 21:32:21**—, cada una con
>   su nota fechada, el commit
>   `2a0aba3e01dcd15878579f1d02a64457b1834046` y la cita del acta
>   `docs/actas/2026-09-15-fase-4a.md`; con ellas quedó marcada también la
>   **22**. **Con eso la lista C1–C14 queda entera**; lo
>   único que sigue sin hacerse de toda la §7 es el **tercer punto del 7.4**, el
>   `diagnostico` con el servicio detenido, que no se midió.
>
> **Lo que la fase NO resolvió, y no era un criterio de esta sección:** sin LED
> conectado, el rechazo por falta de papel es **invisible** para el personal. El
> usuario, delante de la prueba, dijo «no vi ninguna diferencia realmente».
> Ficha **F-256**.

### 7.1 Código y pruebas, en la PC
- `python -m unittest discover -s tests -t .` termina en **`OK`**, con más de
  **194** pruebas y el número exacto anotado.
- `grep -c "_MAX_BYTES_BASURA" ruleta/escpos.py` → **0**.
- `grep -c "while True" ruleta/escpos.py` → **0**.
- Sin retornos de carro en ningún archivo tocado.

### 7.2 Mutaciones
- Las **diez** de la §6 en **rojo**, con el nombre del test que cae anotado para
  cada una. **Cero supervivientes.**

> **NOTA DEL 2026-09-15 (noche).** El criterio se da por cumplido: **(decisión
> del orquestador, 2026-09-15 noche: 9 de 10 en rojo cumplen el criterio 7.2; M6
> no es una mutación porque en Python `&` liga más fuerte que `==` y el AST es
> idéntico, ficha F-252)**. El texto del criterio **no se reescribe**; se marca
> con esta nota, y la casilla **7** de la §0 queda en `[x]`.

### 7.3 Publicación
- Commit con **exactamente** el conjunto de archivos del Paso 9, verificado
  contra el remoto por un **agente distinto** del que commiteó.

### 7.4 En la Pi
- `git rev-parse HEAD` en la Pi **igual** al hash publicado.
- Suite en la Pi: **`OK`**, **mismo número** de pruebas que en la PC.
- `python3 -m ruleta diagnostico` con el servicio **detenido**: `EXIT=0`, **cero
  `[!!]`**, **cero avisos de poco papel**, y `[ok] la impresora contesta: hay
  papel y está en línea`. El **censo de aciertos de la salida** se mide y se
  escribe (no se copia del plan: ficha **F-186**).
- Servicio **`active`**, `NRestarts=0`, journal de arranque limpio y **sin** la
  línea `reporta poco papel`.

### 7.5 La prueba en vivo (la que de verdad cierra la fase)
Los cinco puntos del Paso 11, medidos con el usuario delante:

1. journal con **«no tiene papel»** y **«premio devuelto al inventario»**;
2. **ninguna** línea «impreso» para ese folio;
3. el **premio vuelve** al inventario (conteo antes = conteo después);
4. **nada retenido** en la impresora al reponer el papel;
5. la jugada siguiente, **con papel, imprime normal**.

### 7.6 Documentos
- Las correcciones **C1-C14** del Paso 8 aplicadas, cada una con su medición
  detrás.
- El acta `docs/actas/2026-09-15-fase-4a.md` escrita **desde el archivo de
  hechos**, y `docs/actas/2026-09-15-hechos-medidos-fase-4a.md` **ya está** en el
  repositorio como copia literal.
- **F-250** cerrada **solo si** el 7.5 salió en verde.

---

## 8. Prohibiciones

1. **No se toca `config.json` ni se añade ninguna llave de configuración.**
2. **No se toca `CLAUDE.md`** (ficha **F-242**: lo actualiza el orquestador).
3. **No se cambia la política de imprimir cuando la impresora no contesta.** Si
   las tres preguntas devuelven `None`, **se imprime**, con `log.debug`. No
   contestar no es prueba de falla, y un kiosco que deja de dar boletos porque
   un firmware calla es peor que el defecto que se arregla.
4. **No se endurece** `BITS_SIN_PAPEL` ni `BIT_FUERA_DE_LINEA` a igualdad de
   pareja: no hay byte medido que lo justifique y podría dejar imprimir sin
   papel.
5. **No se reescriben las actas.** Lo que cambie va como **nota fechada**
   debajo, nunca sustituyendo una fila.
6. **No se fuerza el `pull` en la Pi.** Si hay cambios locales: **se reportan y
   se detiene**. Nada de `checkout --`, `stash` ni `reset`.
7. **No se relaja un assert para que pase.** Cambiar una igualdad por un
   `assertIn`, quitar una comprobación o borrar un caso está prohibido; si un
   golden estorba, o el código está mal o el golden estaba mal, y eso se
   pregunta.
8. **No se añaden dependencias** (`python-escpos` incluida) ni se toca
   `ruleta/app.py`.
9. **No se cita `docs/actas/2026-09-13-poco-papel.md`** mientras no exista.
10. **Ningún agente ejecuta git que modifique** (`add`, `commit`, `push`,
    `stash`, `checkout`, `reset`): eso es del agente de commit, y la
    verificación contra el remoto la hace un agente distinto.
11. **Ningún agente teclea credenciales.** Lo que las exija se reporta como
    «requiere al usuario».
12. **No se parchea en caliente un fallo del deploy ni de la prueba en vivo.**
    Se diagnostica, se reporta y se relanza el mismo paso con el estado previo
    descrito.

---

## 9. Lo que esta fase entrega a la Fase 4

- Un kiosco que, **con el rollo agotado, no cobra el boleto**: ni folio impreso,
  ni premio descontado, ni trabajo retenido en la impresora.
- El **aviso falso de poco papel** apagado, y la máscara escrita de forma que
  solo una impresora con sensor de verdad pueda dispararlo.
- Un **diagnóstico que distingue cuatro fallos** (sin papel, tapa abierta, error
  de impresora, fuera de línea) en vez de dos.
- **Dos dobles de prueba** que describen dos impresoras reales: la que contesta
  un byte (`DispositivoFalso`) y la que habla sin parar (`DispositivoFlujo`).
  Cualquier trabajo futuro sobre el estado en tiempo real tiene ya con qué
  probarse sin hardware.
- Las fichas **F-091**, **F-190**, **F-186** y **F-250** al día, y el mapa de
  anclas de la Fase 2 re-medido.
- **Lo que esta fase NO resuelve y sigue en pie para la Fase 4:** los premios
  reales, el logo definitivo, la **pieza D** (esperar a que la hora esté
  sincronizada, **F-241**), el **reinicio del inventario** antes del lunes 21
  (**F-243**), **soldar** las patitas de HABILITAR (**F-239**), decidir el LED
  (**F-240**), `CLAUDE.md` (**F-242**) y la ficha **F-158**
  (`interpretar_estado_papel` dice «hay papel» cuando el byte del papel nunca
  llegó).

---

## 10. Regla final

**Si el código real, el `README.md`, el `config.json` o la propia Raspberry Pi
contradicen este plan, el ejecutor se detiene y pregunta; no improvisa.**

Y una más, porque esta fase nació de creer una lectura que no estaba ganada:
**ningún criterio de esta fase se da por cumplido «porque tiene sentido».** Se
mide, se pega la salida, y si no se pudo medir, se escribe que no se midió.
