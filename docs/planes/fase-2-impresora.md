# Fase 2 · Impresora (USB primero, Bluetooth de respaldo)

Plan prescriptivo. **Redactado el 2026-09-11** (después de cerrar la Fase 1) e
incorporando los hechos que el orquestador y sus agentes midieron **ese mismo
día**, incluida la **ejecución adelantada de la noche del 2026-09-11**, y que
están en la **§0-bis**. Esta fase **no descubre: reverifica** con los comandos
escritos aquí, reconcilia lo que se hizo a mano con lo que dice este plan, y
deja el acta y los goldens que aquella noche no se escribieron. **La bitácora de
la §0 sí está marcada** con la evidencia de aquella noche, pegada en
`docs/actas/2026-09-11-hechos-medidos.md`: se decidió así al lanzar la sub-fase
2b y cada casilla dice qué evidencia la sostiene (ver «De dónde salen las
marcas de abajo», al principio de la §0).

**ESTADO GLOBAL (actualizado el 2026-09-11 ~23:20, tras la reprueba post-2b y
la confirmación del usuario).** **FASE 2 CERRADA.** Cerrada **en papel**: el
usuario volvió a correr las pruebas con el papel delante y confirmó en chat
«todas las pruebas salieron y se escucharon los beeps» —boleto de prueba con las
cuatro tablas de acentos **en dos renglones, sin líneas partidas**, boleto de
inventario de arranque y **un pitido al final de cada boleto**—. El acta lo
recoge en su §10. La impresora imprime por USB; la sub-fase **2b** está
implementada, commiteada (`61adf9676b1072115c5fd64e6a28f6bef5454a54`), publicada, desplegada
en la Pi y verificada por un agente independiente. Medido tras el deploy: HEAD
de la Pi = HEAD remoto = `61adf96`, `instalar.sh` con código 0, **194 pruebas
OK** en la Pi, diagnóstico `EXIT=0` **sin ningún `[!!]`** y con
`[ok] impresora conectada en /dev/ruleta-impresora`, servicio
`active`/`enabled`/`running` con **`NRestarts=0`** (se acabó el bucle de 118
reinicios) e inventario impreso por USB a las 22:32:48 MST sin un solo `ERROR`
ni `Traceback` en el journal. Los tres pendientes que este bloque tenía antes
de la reprueba quedaron así:

1. **El servicio quedó `active`** — **SUPERADO POR DECISIÓN del orquestador**:
   **el kiosco se queda corriendo por USB**, con el servicio `active` y
   `enabled`. El final del Paso 13, que pedía devolverlo a `enabled` +
   `inactive`, **ya no aplica** (ficha **F-185**, cerrada). Lo que sigue en pie
   es la receta de la Fase 3: `stop` **y** `disable` antes de apagar la Pi para
   cablear los botones.
2. **Nadie había vuelto a correr `probar-impresora` después de 2b** — **HECHO y
   confirmado en papel** el 2026-09-11 ~23:20: las líneas de acentos salieron
   partidas en dos renglones, sonó un pitido por boleto y el usuario dio por
   bueno también el boleto de inventario (ficha **F-188**, cerrada).
3. **Tres goldens de la §7 y la medición de grupos del Paso 13 no se midieron**
   en el deploy (ficha **F-187**), y la reprueba tampoco los midió: **sigue
   abierto**, sin bloquear nada. El acta dice cuáles, uno por uno.

Acta de esta fase: `docs/actas/2026-09-11-fase-2.md`.

Plan de la fase anterior: `docs/planes/fase-1-preparar-pi.md` (su **§0-bis** dice
qué resultó falso al medirlo y su **§9** anuncia esta fase). Acta de la Fase 1:
`docs/actas/2026-09-11-fase-1.md`. Hechos crudos:
`docs/actas/2026-09-11-hechos-medidos.md`. Pausa y cómo se retomó:
`docs/PAUSA-2026-09-11.md`.

Este documento se escribió para **dos lectores**:

- **El dueño del restaurante** (todo lo físico y todo lo que exija teclear una
  contraseña: encender, poner papel, activar el punto de acceso de Windows,
  mirar el papel impreso y decidir). Sus pasos dicen **QUIÉN: usuario**.
- **Un ejecutor Opus sin contexto** (todo lo que se hace desde la PC por
  terminal o por SSH). Sus pasos dicen **QUIÉN: agente** y traen comandos
  exactos, copiables tal cual.

Cada paso tiene siempre las mismas cuatro partes: **QUIÉN**, **QUÉ HACER**,
**CRITERIO DE ACEPTACIÓN** (cómo se comprueba, sin opinar) y **SI FALLA**
(diagnóstico y salida). Nada se da por hecho hasta que su criterio se cumple.

## Convención de comandos (idéntica a la Fase 1, se repite porque muerde)

- Los comandos que empiezan con `ssh ruleta ...` se corren **desde la PC
  Windows, en Git Bash**, con el alias creado en la Fase 1.
- **Un agente NO invoca el `ssh` de Git Bash.** Escribe siempre la ruta completa
  del cliente nativo de Windows, `/c/Windows/System32/OpenSSH/ssh.exe`, en lugar
  de `ssh` (Fase 1, §0-bis D8 y §5 trampa 17: Git Bash monta `C:` con `noacl`,
  ve la llave privada como `644` y puede rechazarla con `UNPROTECTED PRIVATE KEY
  FILE`). En los ejemplos de este plan se escribe `ssh` corto por legibilidad;
  el agente lo sustituye siempre.
- Un agente añade siempre `-o BatchMode=yes -o ConnectTimeout=10`, para que si
  algo pidiera contraseña el comando **falle en vez de colgarse**:

  ```bash
  /c/Windows/System32/OpenSSH/ssh.exe -o BatchMode=yes -o ConnectTimeout=10 ruleta 'hostname'
  ```

- **El PATH de una sesión SSH no interactiva NO incluye `/usr/sbin` ni
  `/sbin`** (Fase 1, §0-bis D7): `PATH=/usr/local/bin:/usr/bin:/bin:/usr/games`.
  Los binarios de administración se llaman **por ruta absoluta** o detrás de
  `sudo` (que arma su propio PATH). En esta fase eso afecta a
  `/usr/sbin/usermod`, `/usr/sbin/modprobe` y `/usr/sbin/rfkill`.
- **`python3 -m ruleta` solo funciona desde `~/ruleta`** (Fase 1, §5 trampa 3) y
  siempre con `PYTHONIOENCODING=utf-8` delante cuando su salida se va a leer.
- **Nunca se pone `sudo` delante de `python3 -m ruleta`.** Ver §5, trampa 4: con
  `sudo`, el programa puede crear un archivo normal donde debería estar el
  dispositivo y **tragarse el boleto sin dar error**, además de dejar `datos/`
  con archivos de root que luego el servicio no puede escribir.

## Tiempos

Ningún comando de esta fase tarda minutos. Los dos más lentos son la búsqueda
Bluetooth del respaldo (unos 20 s por barrido, Paso 10) y el `git pull` inicial.
El límite de 2 minutos de la herramienta de terminal **sobra**; solo hay que
subirlo (a `600000`) en el bucle de espera del Paso 13 si hubiera que reiniciar
la Pi.

---

## 0. Bitácora

Se marca `[x]` **solo** cuando el criterio de aceptación del paso se cumplió,
con la fecha y la evidencia real (salida de comando o foto del papel, nunca de
memoria). `[~]` = hecho pero **sin verificar todavía en la Pi**. La columna
«Quién» se rellena con quien lo hizo **de verdad**.

**De dónde salen las marcas de abajo.** El preámbulo de este plan decía que la
bitácora se marcaría con la evidencia del día en que se corriera el plan y nunca
con la de la noche del 2026-09-11. Se cambió a propósito, por decisión del
orquestador al lanzar la sub-fase 2b: repetir a ciegas lo que ya está medido y
pegado en `docs/actas/2026-09-11-hechos-medidos.md` (sección «Noche del
2026-09-11») no añade información y sí gasta papel. Cada casilla marcada dice
**qué evidencia** la sostiene; las que no tienen evidencia siguen vacías.

| Nº | Paso | Quién | Estado | Fecha | Evidencia |
|---|---|---|---|---|---|
| 0 | Red de laboratorio (punto de acceso móvil de Windows) | usuario + agente | [x] | 2026-09-11 | Punto de acceso de Windows con el SSID y la contraseña del asadero; la Pi entró sola en `192.168.137.95/24` (la PC en `.1`), `ruleta.local` resuelve, internet OK y `sudo -n` OK |
| 1 | Poner la Pi en estado de trabajo (servicio detenido y **deshabilitado**, `git pull`) | agente | [~] | 2026-09-11 | **A medias.** Del deploy de 2b sí salió la parte del repositorio: respaldo `~/config.json.pi-antes-deploy`, `git checkout --` de los tres archivos locales, `git pull --ff-only` `2052e47..61adf96` y `git rev-parse HEAD` → `61adf96`. **Lo que falta y por eso no va [x]:** el servicio **nunca se deshabilitó** (el verificador en vivo midió `systemctl is-enabled ruleta` → `enabled` durante todo el deploy, ficha **F-185**). Matiz medido aparte: la Pi venía de `2052e47`, **no** de `601c4c2` como pedía la tabla de criterios (ficha **F-098**) |
| 2 | Impresora encendida, con papel, y página de autoprueba | usuario | [ ] | | La impresora estuvo encendida y con papel toda la noche; la **autoprueba** no se intentó |
| 3 | Detección del dispositivo USB (`lsusb`, `dmesg`, `/dev/usb/lp*`, `udevadm`) | agente | [x] | 2026-09-11 | `0418:5011`, clase 7 subclase 1 **protocolo 2 (bidireccional)**, driver `usblp`, `/dev/usb/lp0` `crw-rw---- root:lp` 180,0, `ieee1284_id = MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1` |
| 4 | Permisos: regla udev por VID:PID medido + grupo | agente | [x] | 2026-09-11 | Regla escrita a mano en `/etc/udev/rules.d/61-ruleta-impresora-usb.rules` (md5 `2c2c308b…`), `usermod -aG lp asadero` (`getent group lp` → `lp:x:7:asadero`), enlace `/dev/ruleta-impresora` creado a la primera y `test -w` → ESCRIBIBLE. **Con otros nombres que los de este plan**: ver la nota de 2b, abajo |
| 5 | `config.json` de la Pi: `tipo: archivo` y **añadir** `ruta` | agente | [x] | 2026-09-11 | En la Pi: `tipo: "archivo"` y `ruta: "/dev/ruleta-impresora"` (no `/dev/usb/lp0`: ver la nota de 2b) |
| 6 | `python3 -m ruleta diagnostico` | agente | [x] | 2026-09-11 | Dos veces. **Antes de 2b:** `EXIT=0` y sin `[!!]`, pero con la salida temprana `[--] impresora tipo 'archivo': no se prueba Bluetooth`, que es justo lo que arregla el cambio (c). **Después del deploy:** `EXIT=0`, cero `[!!]`, con `[ok] impresora conectada en /dev/ruleta-impresora`, las versiones reales de PIL, gpiozero y lgpio, y un `[??] la impresora reporta poco papel` —siete `[ok]`, no ocho: ver la §7.5 y la ficha **F-186** |
| 7 | `python3 -m ruleta probar-impresora` y **lectura del papel** | agente + usuario | [x] | 2026-09-11 | Boleto de prueba impreso a las 19:25 (foto del usuario): `ESC t 19` (cp858) y `ESC t 2` correctos, `ESC t 0` sin mayúsculas acentuadas y **`ESC t 16` basura**; 48 columnas exactas; tamaños 1x-4x y negrita bien; logo nítido; corte automático limpio. Antes, a las 19:22, el servicio ya había impreso el **inventario de arranque** por USB |
| 8 | Ajustes iterativos en el `config.json` de la Pi | agente + usuario | [x] | 2026-09-11 | Nada que cambiar: el papel confirma `codepage_n: 19` (cp858) y `chars_por_linea: 48`. **Zumbador medido** por USB: `ESC B` suena, pero da un pitido corto por comando e ignora `n` y `t`; el usuario decidió `"beep": true`. Cosmético anotado: las líneas de acentos del boleto de prueba se partían (lo arregla el cambio (f) de 2b) |
| 9 | `python3 -m ruleta vista-previa --todos` (pendiente de la Fase 1) | agente | [ ] | | |
| 10 | Respaldo Bluetooth — **solo si el USB no es viable** | agente + usuario | [ ] | | Se salta con razón: el USB funcionó (Paso 7) |
| 11 | Sincronizar el `config.json` final al repositorio (por la cadena) | ejecutor + agente de commit | [x] | 2026-09-11 | El `config.json` del repositorio trae `tipo: "archivo"`, `ruta: "/dev/ruleta-impresora"` y `"beep": true`, con golden en `tests/test_config.py`. Tras el `git pull` el verificador en vivo leyó **en la Pi** `archivo /dev/ruleta-impresora True`, y `git status --porcelain` allá solo muestra el respaldo `?? config.json.bak-2026-09-12` sin rastrear: los dos archivos son el mismo |
| 12 | Sub-fase **2b**: cambios de código (a)(b)(c)(d) con goldens | cadena completa | [x] | 2026-09-11 | Commit `61adf9676b1072115c5fd64e6a28f6bef5454a54`, publicado y verificado contra el remoto por un agente distinto del que commiteó. Suite completa en verde: **194 pruebas OK** en la PC y **194 pruebas OK** en la Pi. Cadena: ejecutor → 2 rondas de lentes → escéptico (fichas F-141 a F-184) |
| 13 | Arranque del servicio y verificación en vivo | agente + usuario | [x] | 2026-09-11 | **Arrancado, verificado y cerrado.** Medido a las 22:32:48 MST con la unidad nueva: `active`/`running`/`enabled`, `NRestarts=0`, journal con `impresora=archivo`, `Inventario impreso (arranque). Folio actual 00000` y `Lista. Esperando jugadas.`, cero `ERROR`/`Traceback`/`exception`. El **boleto** lo confirmó el usuario a las ~23:20 (fila 13-bis). El final del paso —**devolver el servicio a `enabled` + `inactive`**— queda **SUPERADO por decisión del orquestador**: el kiosco se queda corriendo, `active` y `enabled` (ficha **F-185**, cerrada). **Lo único que no se midió:** los grupos del proceso (`/proc/<pid>/status`, ficha **F-187**, abierta) |
| 13-bis | **Reprueba post-2b y confirmación en papel del usuario** | usuario + agente | [x] | 2026-09-11 ~23:20 | Cita literal del archivo de hechos: «todas las pruebas salieron y se escucharon los beeps». Cubre el **boleto de prueba con las cuatro tablas de acentos en dos renglones, sin líneas partidas** (cambio (f) de 2b), el **boleto de inventario de arranque** y **un pitido al final de cada boleto** (`"beep": true` por USB). Estado de la Pi al cerrar: servicio `active`/`enabled`, `NRestarts=0`, HEAD `61adf96`; la impresora sigue avisando de **poco papel** y el rollo de repuesto sigue pendiente (ficha **F-190**) |
| 14 | Cierre: acta desde hechos medidos, fichas y memoria | agente | [x] | 2026-09-11 | Acta escrita desde los hechos medidos y los informes: `docs/actas/2026-09-11-fase-2.md`, **cerrada en papel en su §10**. Fichas al día (nuevas **F-185** a **F-190**; cerradas el ~23:20 las **F-140**, **F-169**, **F-180**, **F-185**, **F-186** y **F-188**). Documentos vecinos puestos al día en la misma pasada: `CLAUDE.md` §«Contexto del producto» con la realidad medida, y **notas fechadas** sobre los `[ok]` en la §7 del plan de la Fase 1 y en su acta, sin borrar el `6` histórico. **Siguen fuera de alcance y viejos:** README §8 (F-167) y `docs/PAUSA-2026-09-11.md` (F-170). La **memoria del proyecto** la actualiza el orquestador |

### Nota de la sub-fase 2b (2026-09-11): qué se implementó y en qué se aparta de este plan

Implementado en la PC con sus goldens y sus mutaciones —y **ya desplegado y
verificado en la Pi**, ver el bloque del deploy al final de esta nota—,
en `instalar.sh`, `ruleta.service`, `config.json`, `ruleta/escpos.py`,
`ruleta/app.py`, `ruleta/__main__.py`, `ruleta/ticket.py`, `README.md` y las
pruebas. **Ojo con las letras:** las de esta lista son las del brief de 2b y
**no** coinciden con las del Paso 12 de este plan, que solo tiene cuatro. La
equivalencia: brief (a) = Paso 12 (a); brief (d) = Paso 12 (b); brief (e) =
Paso 12 (c); brief (g) = Paso 12 (d); brief (b), (c) y (f) son cambios que este
plan no había previsto como apartados propios.

- **(a)** paso nuevo `5/7 Impresora USB` en `instalar.sh` —los pasos se
  renumeraron a `n/7`—, con la regla `udev`, el `usermod -aG lp` y la recarga de
  `udev`.
- **(b)** `RestartPreventExitStatus=2` y `SupplementaryGroups=gpio lp` en
  `ruleta.service`, y su `Description` ahora dice «impresora USB o Bluetooth».
  Con goldens que comprueban que los errores de configuración salen con **2** y
  que lo demás (inventario ocupado, GPIO) **no**, para que systemd sí los
  reintente.
- **(c)** `config.json` del repositorio con `tipo: "archivo"`,
  `ruta: "/dev/ruleta-impresora"` y `"beep": true`.
- **(d)** consulta `DLE EOT` en `ImpresoraArchivo`, solo cuando la ruta es un
  dispositivo de caracteres y `consultar_estado` está activo, con la
  interpretación de los bits **compartida** con el transporte Bluetooth.
- **(e)** el diagnóstico revisa la ruta del tipo `archivo`, consulta el papel y
  muestra las versiones reales de PIL, gpiozero y lgpio.
- **(f)** el boleto de prueba parte cada línea de acentos en dos (etiqueta y
  muestra) para que quepa en 48 columnas.
- **(g)** `README.md` reescrito con el USB de primera clase, con el visto bueno
  explícito del usuario (decisión D12).

**Dos nombres se apartan de lo que dicen los Pasos 4 y 5 y los goldens §7.3 y
§7.4, y se hizo a propósito:** este plan pedía renombrar la regla a
`61-ruleta-impresora.rules`, el enlace a `/dev/impresora-ruleta` y la ruta a
`/dev/usb/lp0`. La sub-fase 2b conserva **los nombres que ya están funcionando
en la Pi** —`61-ruleta-impresora-usb.rules` y `/dev/ruleta-impresora`— porque el
despliegue es un `git pull` sobre esa misma Pi y renombrar obligaría a tocar a
mano `udev`, el `config.json` de allá y el enlace, sin ganar nada a cambio. Las
§7.3 y §7.4 quedan corregidas más abajo con esos nombres. **Si el orquestador
prefiere los nombres originales, hay que decirlo antes del deploy**: son tres
líneas (la regla, su `SYMLINK+=` y la `ruta`), pero se cambian las tres a la vez
o no se cambia ninguna. **El orquestador no pidió el cambio y el deploy salió
con los nombres de 2b**, así que la duda queda cerrada: los nombres buenos son
`61-ruleta-impresora-usb.rules` y `/dev/ruleta-impresora` (ficha **F-139**,
cerrada).

### Deploy de 2b y verificación en vivo (2026-09-11, noche)

Lo hicieron dos agentes distintos: uno desplegó y otro —que no vio al primero—
volvió a medir contra la Pi. Todo lo de esta lista está **medido**, no contado:

- `git pull --ff-only` `2052e47..61adf96` y `git rev-parse HEAD` en la Pi =
  `git ls-remote --heads origin main` = `61adf9676b1072115c5fd64e6a28f6bef5454a54`.
- `sudo ./instalar.sh` → **código 0**, con sus pasos `1/7` … `7/7`.
- Regla `udev`: el verificador leyó
  `/etc/udev/rules.d/61-ruleta-impresora-usb.rules` y coincide **carácter por
  carácter** con la del repositorio (`0418:5011`, `MODE="0660"`, `GROUP="lp"`,
  `SYMLINK+="ruleta-impresora"`). `getent group lp` incluye `asadero` y
  `/dev/ruleta-impresora` existe.
- `grep -c RestartPreventExitStatus=2 /etc/systemd/system/ruleta.service` → **1**:
  `instalar.sh` sí volvió a copiar la unidad (un `git pull` solo no lo habría
  hecho; ficha **F-176**, cerrada).
- `python3 -m unittest discover -s tests -t .` en la Pi → **`Ran 194 tests` /
  `OK`** (mismo número que en la PC).
- Diagnóstico en la Pi: `EXIT=0`, **cero `[!!]`**, con
  `[ok] impresora conectada en /dev/ruleta-impresora (dispositivo, se puede
  escribir)`, `[ok] gpiozero 2.0.1`, `[ok] lgpio 0.2.2.0` (ficha **F-051**
  confirmada en hardware) y un `[??] la impresora reporta poco papel`.
- Servicio: `is-active=active`, `is-enabled=enabled`, `SubState=running`,
  **`NRestarts=0`**. El journal del arranque de las 22:32:48 MST trae la unidad
  nueva («impresora USB o Bluetooth»), `impresora=archivo`,
  `Inventario impreso (arranque). Folio actual 00000`,
  `Lista. Esperando jugadas.` y **cero** coincidencias de
  `error|traceback|exception`. El único `WARNING` es el de poco papel.
- **La consulta `DLE EOT` por USB funciona en hardware real:** ese `WARNING` lo
  escribe `escpos.verificar_estado` **antes** de mandar el boleto, así que la
  impresora contestó de verdad por el nodo `usblp` y el servicio pudo abrirlo en
  `r+b` (ficha **F-091**).

**Lo que el deploy NO midió** (ficha **F-187**): los grupos del proceso
(`/proc/<pid>/status`) del Paso 13, y tres goldens de la §7 —
`ls /etc/udev/rules.d/ | grep -c impresora` → 1, `stat -c "%a %U %G"` del nodo e
`ieee1284_id`—. **Y el servicio quedó `active`**, no `enabled` + `inactive` como
mandaba el final del Paso 13 (ficha **F-185**) — **ver la nota siguiente: eso
último dejó de ser un pendiente y pasó a ser una decisión**.

### Reprueba post-2b y cierre en papel (2026-09-11, ~23:20)

Esto **no** lo midió un agente: lo confirmó **el usuario**, con el papel en la
mano, y así quedó escrito en `docs/actas/2026-09-11-hechos-medidos.md`:

> **Confirmación del usuario (2026-09-11 ~23:20, en chat, tras la reprueba
> post-2b):** «**todas las pruebas salieron y se escucharon los beeps**».

Qué cubre, según esa misma entrada: el **boleto de prueba con las cuatro tablas
de acentos en dos renglones, sin líneas partidas** (el cambio (f) de 2b, visto
por fin en papel), el **boleto de inventario de arranque**, y **un pitido al
final de cada boleto** (`"beep": true` operativo por USB). La hora es
**aproximada**: la anotó el orquestador al recibir el mensaje.

Estado de la Pi al cerrar, tal como lo registra el archivo de hechos: servicio
`ruleta` **`active` y `enabled`** con `NRestarts=0`, HEAD del clon `61adf96`
(el repositorio de la PC en `6ab9680`, ya con el acta), impresora por USB
avisando de **poco papel** y **rollo de repuesto pendiente** (ficha **F-190**).

**DECISIÓN DEL ORQUESTADOR, la que cierra la fase: el kiosco queda corriendo
por USB.** El servicio se deja **`active` y `enabled`** a propósito. Por tanto
**el final del Paso 13 —«Al terminar, devolver el servicio al estado en que lo
dejó la Fase 1», con su criterio `enabled` + `inactive`— queda SUPERADO**, igual
que el golden de la §7.9. No es un incumplimiento: es una decisión tomada
**después** de ver el servicio imprimir en hardware real. Ficha **F-185**,
cerrada. **Lo que la decisión no cambia:** antes de apagar la Pi para cablear
los botones de la Fase 3, `sudo systemctl stop ruleta` **y**
`sudo systemctl disable ruleta`, y `enable` al volver.

**Pasos que se pueden saltar, y solo esos:**

- **Paso 10** se salta si el Paso 7 salió bien: el Bluetooth es respaldo, no un
  segundo camino que haya que probar «por si acaso».
- **Paso 12 (2b)** se puede posponer **entero** si el evento llega antes de que
  la cadena tenga tiempo: la fase queda cerrada con papel en la mano y con las
  fichas abiertas. Lo que **no** se puede hacer es ejecutar 2b a medias, sin
  goldens o sin revisión.
- Cualquier otro paso que se salte **invalida la fase**.

---

## 0-bis. Hechos medidos que cambian el punto de partida (2026-09-11)

Los midieron el orquestador y sus agentes el **2026-09-11** (H1 a H8 por la
tarde; **H9 por la noche, con la impresora delante**) y están pegados en
`docs/actas/2026-09-11-hechos-medidos.md`. **No vienen de memoria.** Lo que no
se midió, se dice que no se midió.

**H1 · La Pi y el usuario están en OTRA UBICACIÓN, con otro Wi-Fi.**
La PC está conectada a la red `FDA806_5G`. **La Pi solo conoce el Wi-Fi del
asadero** (su nombre y su contraseña los conoce únicamente el usuario, que los
tecleó en Imager en la Fase 1), así que **sin el punto de acceso del Paso 0
`ruleta.local` no responde** (con el punto de acceso encendido, la noche del
2026-09-11 sí respondió y la Pi tomó `192.168.137.95/24`: §0-bis H9). La
PC **no tiene puerto Ethernet** (solo Wi-Fi Intel AX211 y adaptadores de VPN) y
**no tiene WSL**. Consecuencia: **la fase no puede empezar por el Paso 1;
empieza por el Paso 0**, que crea la red de laboratorio.

**H2 · La impresora ya está conectada por cable USB y tiene corriente.**
Está enchufada a uno de los puertos **USB 3.0 (azules)** de la Pi. Las pruebas
de impresora son posibles **hoy mismo** en cuanto la Pi esté en red. **Y ya
está todo medido** (noche del 2026-09-11, §0-bis H9): el kernel **sí** creó
`/dev/usb/lp0` (`crw-rw---- root:lp`, 180,0) con el driver `usblp`; el
dispositivo enumera como **`0418:5011`** (`Bus 001 Device 002: ID 0418:5011 AST
Research USB Printer Port`); la interfaz es **clase 7, subclase 1, protocolo 2
(bidireccional)**, con `EP 0x81 IN` y `0x01 OUT` de 64 bytes. El Paso 3 **no
descubre nada nuevo: vuelve a medirlo, pega la salida en el acta y, si algún
valor difiere de estos, se detiene y pregunta.**

**H3 · La impresora es una Zjiang ZJ-80250.**
El PPD del driver Linux del fabricante (que el usuario descargó y que se
desempacó **sin ejecutarlo**) dice: `MFG:Zijiang;CMD:Zijiang;MDL:ZJ-80250;
CLS:PRINTER;`, `Manufacturer "Zijiang"`, `ModelName "ZJ-80250"`. Es decir: la
«AOMU My-A1» es una **Zjiang ZJ-80250**, familia POS-80 (80 mm, 250 mm/s). Tres
consecuencias:

1. **`CLS:PRINTER`**: la clase USB es «impresora», así que en Linux el driver
   `usblp` **debería** reclamarla y crear `/dev/usb/lp0`. «Debería» no es «está
   medido»: el Paso 3 lo mide.
2. **Tiene cortador y zumbador** (opciones `Cutting` y `Beeper` del PPD; sus
   valores de fábrica son «cortar al final de página» y «pitar antes de cada
   página»). O sea: `"corte": "auto"` y `"beep": true` son viables; el zumbador
   depende además del interruptor **DIP 2** de la impresora.
3. **El filtro del fabricante usa `DLE EOT 1`** (estado en tiempo real). Eso
   respalda que la impresora **sí contesta** a la consulta de papel que este
   programa ya hace por Bluetooth, y que tendría sentido hacer también por USB
   (cambio (b) de la sub-fase 2b).

**H4 · Los binarios del driver del fabricante son x86: NO sirven en la Pi.**
`rastertozj` y `rastertozj58` son ELF x86 (32 y 64 bits) y la Pi es `aarch64`.
**El driver del fabricante no se puede usar aquí**, y no hace falta: este
programa habla ESC/POS directo, que es justo lo que la impresora entiende.
**Prohibido** intentar instalarlo (§8, prohibición 12).

**H5 · Por USB, hoy el programa NO consulta si hay papel.**
Medido en el código: `crear_impresora` (`ruleta/app.py`, línea 56) construye
`ImpresoraArchivo(imp.ruta, anexar=True)` y **no le pasa `consultar_estado`**;
`ImpresoraArchivo` (`ruleta/escpos.py`, línea 546) **no implementa** la consulta
`DLE EOT` que sí tiene `ImpresoraBluetooth`. Consecuencia real para el evento:
**por USB, si se acaba el rollo, el programa descuenta el premio igual y el
boleto no sale.** Eso es lo que arregla el cambio (b) de la sub-fase 2b; si 2b
no se hace a tiempo, **hay que decírselo al personal en la capacitación** y
apoyarse en el `README` §5 punto 8 (cotejar `datos/boletos.csv` y liberar).

**H6 · Por USB tampoco hay reintentos ni control de ritmo.**
`ImpresoraArchivo` escribe de una sola vez: sin `reintentos`, sin
`espera_reintento_seg`, sin `tamano_bloque` ni `pausa_bloque_seg`. Con un cable
eso es razonable (no hay enlace que se caiga a media frase), pero significa que
esas llaves de `config.json` **no hacen nada** con `tipo: archivo`: solo aplican
al Bluetooth. Ficha **F-091**.

**H7 · Estado de la Pi al empezar.**
Usuario `asadero`, `sudo` sin contraseña, `~/ruleta` clonado en `2052e47` (se
actualizará con `git pull` al commit de cierre de la Fase 1, `601c4c2`),
servicio `ruleta` **`enabled`** y, cuando se apagó, `inactive`. Grupos medidos
de `asadero`: `asadero adm dialout cdrom sudo audio video plugdev games users
input render netdev bluetooth spi i2c gpio lpadmin`. **No incluye `lp`** (sí
`lpadmin`, que no es lo mismo): ficha **F-052**.

**H8 · El servicio quedó `enabled`, así que ya se arrancó solo.**
`ruleta.service` trae `WantedBy=multi-user.target`, `Restart=always` y
`StartLimitIntervalSec=0`. Como la Pi se apagó y se volvió a encender en la
ubicación nueva, **lo esperable es que systemd ya lo haya arrancado** —esto es
una deducción de las tres líneas anteriores, **no** una medición: el Paso 1 lo
mide—. **OJO: eso YA NO es el bucle de la MAC de relleno.** El `config.json` de
la Pi quedó en `"tipo": "archivo"` la noche del 2026-09-11 (§0-bis H9), y con
`tipo: archivo` `crear_impresora` (`ruleta/app.py`, línea 46) **ni siquiera mira
la MAC**: el servicio arranca **bien**. Medido esa noche: 118 reinicios en bucle
mientras la configuración era Bluetooth, y `active` estable desde las 19:22:22
en cuanto pasó a USB, **imprimiendo el inventario de arranque**. Consecuencia
**de hoy, no futura**: mientras el servicio siga `enabled`, **cada encendido de
la Pi imprime el inventario de premios de prueba y gasta papel sin que nadie lo
pida**; si la impresora quedó encendida y con papel, eso ya pasó antes de que
empiece esta fase. Por eso el **Paso 1 detiene y DESHABILITA el servicio**, y el
**Paso 13** lo vuelve a habilitar cuando ya se sabe que todo funciona.

**H9 · La noche del 2026-09-11 esta fase YA SE EJECUTÓ a mano, y la impresora
YA IMPRIMIÓ.** Está medido y pegado en
`docs/actas/2026-09-11-hechos-medidos.md`, sección «Noche del 2026-09-11 …
ejecucion adelantada de la Fase 2». Qué quedó hecho:

1. **Paso 0:** punto de acceso móvil de Windows con el mismo SSID y contraseña;
   la Pi entró sola en `192.168.137.95/24` (la PC en `192.168.137.1`),
   `ruleta.local` resuelve, hay internet y `sudo -n` funciona.
2. **Paso 3:** medido todo lo de H2, más `ieee1284_id =
   MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1`.
3. **Paso 4, pero con OTROS NOMBRES:** en la Pi hay una regla escrita a mano,
   `/etc/udev/rules.d/61-ruleta-impresora-usb.rules`, con
   `SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*", ATTRS{idVendor}=="0418",
   ATTRS{idProduct}=="5011", MODE="0660", GROUP="lp",
   SYMLINK+="ruleta-impresora"`, y `asadero` **ya está en `lp`**
   (`getent group lp` → `lp:x:7:asadero`), con `/dev/usb/lp0` **ESCRIBIBLE**.
   Este plan usa `61-ruleta-impresora.rules` y `SYMLINK+="impresora-ruleta"`:
   el Paso 4 **borra primero la regla vieja** para no dejar dos reglas
   compitiendo por el mismo dispositivo.
4. **Paso 5, con OTRA RUTA:** el `config.json` **de la Pi** ya trae
   `"tipo": "archivo"` y `"ruta": "/dev/ruleta-impresora"`. El Paso 5 lo lleva a
   `/dev/usb/lp0`, que es lo que dicen este plan, el README y el golden §7.4.
5. **Pasos 6, 7 y 13:** `diagnostico` dio código 0 sin `[!!]`; el servicio
   arrancó e **imprimió el inventario** por USB (foto del usuario, 19:22), y
   `probar-impresora` sacó el boleto de prueba (19:25). Del papel:
   **`ESC t 19` (cp858) correcto**, `ESC t 2` también, `ESC t 0` sin mayúsculas
   acentuadas y **`ESC t 16` basura** (la tabla 16 de esta unidad no es CP1252);
   **48 columnas exactas**; corte automático limpio; logo nítido. **Conclusión:
   `codepage_n` se queda en 19 y `chars_por_linea` en 48; el Paso 8 no tiene
   nada que cambiar salvo que el papel diga otra cosa.** Cosmético anotado: las
   líneas de acentos del boleto de prueba pasan de 48 caracteres y se parten.
6. **Zumbador:** medido por USB con el servicio detenido: `ESC B` suena, pero
   emite **un pitido corto por comando** e **ignora los parámetros** `n` y `t`.
   `"beep": true` es viable; la decisión sigue siendo del usuario.
7. **Basura pendiente:** dentro de `~/ruleta` quedó el respaldo
   `config.json.bak-2026-09-12` (con la fecha equivocada). **Hay que sacarlo del
   repositorio** (`ssh ruleta 'mv ~/ruleta/config.json.bak-2026-09-12 ~/'`) o el
   criterio de árbol limpio del Paso 1 y el golden §7.2 no se cumplen (§5,
   trampa 13).

**Consecuencia para todo el plan:** ningún paso se salta —hay que volver a
correr cada comando y pegar su salida real en el acta—, pero **el resultado
esperado de los Pasos 3 a 7 es el de esta H9**, y cualquier diferencia es motivo
de **detenerse y preguntar**, no de improvisar.

---

## 1. Objetivo y alcance

**Objetivo.** Dejar la impresora **conectada por cable USB**, imprimiendo
boletos legibles, con los acentos correctos, el ancho correcto y el corte
correcto; con esos valores escritos en el `config.json` **del repositorio**; y
con el servicio `ruleta` demostrado en vivo: arranca, imprime el inventario en
papel y queda esperando jugadas.

**Qué queda DENTRO de esta fase**

- La red de laboratorio que permite trabajar fuera del asadero (Paso 0).
- Detectar el dispositivo USB y resolver sus permisos de forma **reproducible**
  (regla `udev`, no un `chmod` a mano que se pierde al desconectar el cable).
- Elegir, **leyendo el papel**, la tabla de acentos, el ancho, el modo de corte
  y si hay zumbador.
- Dejar `config.json` sincronizado entre la Pi y el repositorio, de modo que un
  `git pull` futuro no choque.
- La **vista previa** que la Fase 1 dejó pendiente (Fase 1, §0-bis D14).
- El respaldo Bluetooth, **solo si el USB no es viable**.
- La sub-fase **2b**: los cambios de código que esta fase demuestre necesarios,
  cada uno con sus goldens y por la cadena completa.
- Arrancar el servicio **una vez**, verificarlo en vivo y volver a dejarlo
  parado.

**Qué queda explícitamente FUERA**

- **Los botones y el LED.** No se cablea nada al header de 40 pines: eso es la
  Fase 3. El arranque del Paso 13 se hace **sin botones conectados**, y eso es
  seguro (se explica en el propio Paso 13).
- **Los premios reales, el logo definitivo y `reiniciar --si`.** Eso es la
  Fase 4.
- **La batería RTC** y `/boot/firmware/config.txt`. Sigue siendo el principal
  riesgo abierto de la Fase 1 (su Paso 12) y **aquí no se toca** (§8).
- **Instalar `pyusb`, `python-escpos`, CUPS o el driver del fabricante.** Si el
  camino `usblp` no existe, se pasa al respaldo Bluetooth; no se escribe un
  transporte USB nuevo a días de un evento (§2, decisión D10).
- **Dejar la Pi con red para producción.** El punto de acceso del Paso 0 es de
  laboratorio; en el evento la Pi va **aislada** (Fase 1, §0-bis D9).

---

## 2. Decisiones cerradas

Ya están tomadas. **Solo el usuario puede cambiarlas.** Un ejecutor que crea que
alguna está mal **se detiene y pregunta; no improvisa** (§10).

**D1 · La conexión primaria es USB. El Bluetooth queda como respaldo
documentado, y no se elimina.**
*Por qué:* es un kiosco de **una semana, sin vigilancia y sin red**. El cable
elimina de un golpe el emparejamiento, el reposo del módulo, el celular que le
roba la conexión a la impresora, la búsqueda de canal RFCOMM y las heurísticas
de ritmo (`tamano_bloque`, `pausa_bloque_seg`, `pausa_final_seg`) que existen
precisamente porque el enlace Bluetooth es frágil. Menos piezas que se pueden
romper solas un martes a las dos de la tarde. El Bluetooth se queda escrito y
disponible como salida de emergencia: `herramientas/emparejar.sh` y
`"tipo": "bluetooth"` siguen funcionando y **no se borran**.

**D2 · Por USB se usa el transporte que ya existe: `"tipo": "archivo"` con
`"ruta": "/dev/usb/lp0"` (clase `ImpresoraArchivo`). No se escribe código nuevo
para conectar.**
*Por qué:* el programa ya sabe escribir el flujo ESC/POS a un dispositivo, y el
kernel de Linux ya sabe hablar USB con una impresora de clase PRINTER (driver
`usblp`). Meter `pyusb` en medio añadiría una dependencia, permisos nuevos y
código sin probar para hacer exactamente lo mismo. Lo que sí falta —consultar el
papel— es un añadido de la sub-fase 2b, no un transporte distinto.

**D3 · La red de laboratorio es el «Punto de acceso móvil» de Windows en la PC
del usuario, configurado con EXACTAMENTE el mismo nombre de red y la misma
contraseña del Wi-Fi del asadero, en banda 2.4 GHz.**
*Decisión del orquestador, **sujeta a que el usuario la confirme** al ejecutarla*
(es su PC y son sus credenciales).
*Por qué:* la Pi solo conoce esa red y **no se puede tocar sin red** (círculo
vicioso). Si la PC se hace pasar por esa red, **la Pi se conecta sola, sin que
nadie la toque, sin escribir contraseñas nuevas en ningún lado y sin regrabar
nada**. Además la Pi obtiene internet a través de la PC (para el `git pull`) y
`ruleta.local` sigue resolviendo, ahora dentro de `192.168.137.x`. Y funciona en
**cualquier ubicación**: en casa, en el asadero o en una mesa prestada. En
producción esto desaparece: la Pi va sin red.
*Quién teclea qué:* **el usuario** escribe el nombre y la contraseña en
Configuración → Red e Internet → Punto de acceso móvil. **Ningún agente ve, pide
ni escribe esa contraseña** (§8, prohibición 4).

**D4 · Los permisos del dispositivo se resuelven con una regla `udev` por VID:PID
medido, con `GROUP="lp"` y `MODE="0660"`, más `usermod -aG lp asadero`. Si —y
solo si— se mide que el *servicio* no puede abrir el nodo, esa misma regla pasa a
`MODE="0666"`.**
*Por qué una regla y no un `chmod`:* un `chmod` sobre `/dev/usb/lp0` se pierde en
cuanto se desconecta el cable o se reinicia la Pi, y esta fase tiene que dejar
algo que sobreviva una semana y un corte de luz. La regla `udev` se aplica sola
cada vez que aparece el dispositivo, y en 2b se mete en `instalar.sh` para que
una reinstalación no la olvide.
*Por qué `0660` + grupo y no `0666` desde el principio:* `0660 root:lp` es la
convención que ya usa Debian para las impresoras; da acceso a quien debe tenerlo
y a nadie más. `0666` es la salida de emergencia porque **no depende de cómo
systemd resuelve los grupos suplementarios de un servicio**, que es justo lo que
puede sorprender. En un kiosco de un solo usuario y sin red, `0666` no es un
riesgo real; es simplemente menos limpio, y por eso es el plan B, no el A.
*Ojo:* el VID:PID **se mide antes de escribir la regla** (Paso 3). Escribir una
regla con un VID:PID inventado es peor que no tenerla: parece que está puesta y
no hace nada.

**D5 · Durante los experimentos, `config.json` se edita EN LA PI. Al cerrar la
fase, los valores medidos se llevan al repositorio y la Pi vuelve a quedar
idéntica al repositorio.**
*Por qué:* probar una tabla de acentos son quince segundos y un boleto; hacerlo
por la cadena completa (ejecutor, dos lentes, escéptico, commit, deploy) son
horas. Pero dejar la Pi y el repositorio distintos es la forma más segura de que
un `git pull` de la Fase 3 pise la configuración buena. Por eso el Paso 11
existe y **no es opcional**: cierra el círculo y deja `git status` limpio.
*Regla dura mientras tanto:* **la única copia viva de `config.json` es la de la
Pi.** Nadie edita el `config.json` de la PC hasta el Paso 11 (§8, prohibición 6).

**D6 · El servicio `ruleta` se detiene y se DESHABILITA en el Paso 1, y no
vuelve hasta el Paso 13.**
*Por qué:* quedó `enabled` desde la Fase 1 y arranca solo en cada encendido
(§0-bis H8). Mientras se experimenta, un arranque automático (a) compite por el
mismo `/dev/usb/lp0`, (b) toma el candado del inventario, y (c) en cuanto la
configuración sea correcta, **imprime el inventario de premios de prueba y gasta
papel sin avisar**. Deshabilitarlo es reversible con un comando y es exactamente
lo que ya hace el Paso 12 del plan de la Fase 1 antes de reiniciar.

**D7 · El criterio de éxito del camino USB es PAPEL EN LA MANO, no el código de
salida del diagnóstico.**
*Por qué (medido en el código, ANTES de la sub-fase 2b):* con
`"tipo": "archivo"`, `cmd_diagnostico` imprimía
`[--] impresora tipo 'archivo': no se prueba Bluetooth` y **devolvía 0 sin
abrir siquiera la ruta**. Salía verde con la impresora apagada, con el cable
desconectado y con `Permission denied`.
*Qué cambió con 2b (y por qué la decisión sigue en pie):* hoy el diagnóstico sí
abre la ruta, comprueba que sea un dispositivo escribible y —con el servicio
parado— le pregunta por el papel; esa salida temprana ya no existe para
`archivo`. Aun así **el criterio de la fase no cambia**: el diagnóstico puede
decir `[ok] impresora conectada` y el boleto salir ilegible, torcido o sin
cortar. Lo único que cierra la fase es un boleto físico y legible.

**D8 · Los valores de impresora se deciden LEYENDO EL PAPEL, no por teoría.**
Se arranca con lo que ya trae `config.json` —`codepage_n: 19` (`cp858`),
`chars_por_linea: 48`, `corte: "auto"`, `beep: false`— y se cambia **solo** lo
que el papel demuestre que está mal.
*Qué decidió el papel (2026-09-11):* `codepage_n: 19`, `chars_por_linea: 48` y
`corte: "auto"` se confirmaron y **no se tocaron**. El único valor que cambió es
`beep`, que pasó a **`true`** por decisión del usuario después de oír el
zumbador por USB (un pitido corto por comando; ignora `n` y `t`). Es decir: la
decisión se aplicó tal cual, y por eso el `config.json` del repositorio ya no
coincide con la lista de arranque de arriba en esa llave (ficha **F-160**).
*Por qué esos valores de arranque:* la investigación verificada dice que en esta
familia (Xprinter / Zjiang, 576 puntos, 48 columnas en fuente A) la tabla
**19 = PC858** es la única que trae `á é í ó ú ñ Ñ ¿ ¡ Á É Í Ó Ú ü` completa y
es consistente en todos los manuales encontrados, mientras que el **16** no
siempre es CP1252 según el firmware. `GS V 66 0` (nuestro `corte: "auto"`) es el
corte más fiable de la familia porque la propia impresora avanza hasta su
cuchilla. Son buenas apuestas, **no** hechos medidos en esta unidad: por eso
existe el Paso 7.

**D9 · Los cambios de código van en la sub-fase 2b, cada uno por la cadena
completa y con goldens. El ejecutor que está experimentando NO toca código.**
*Por qué:* `CLAUDE.md` §3 y §5. Un parche en caliente mientras se prueba
hardware es la forma clásica de romper las 141 pruebas verdes y no enterarse
hasta el evento.

**D10 · Si el nodo `usblp` no existe (dispositivo «vendor-specific»), NO se
escribe un transporte USB nuevo: se pasa al respaldo Bluetooth.**
*Por qué:* con `CLS:PRINTER` en el PPD del fabricante (§0-bis H3), lo esperable
es que `usblp` funcione. Si aun así no funcionara, la alternativa técnica
(`pyusb`, reclamar la interfaz, otra regla `udev` y código nuevo sin pruebas) es
mucho más riesgo del que aporta, a días de un evento y existiendo ya un camino
probado y escrito. Se anota como ficha y se resuelve después del evento.

**D11 · El arranque del servicio se adelanta a esta fase, en contra de lo que
decían la §9 del plan de la Fase 1 y la §7 de su acta.**
Aquellos documentos colocaban `systemctl start ruleta` en la Fase 4.
*Por qué se cambia:* el arranque del servicio es **la única prueba de que el
servicio —que corre como `asadero`, no como la persona que está dentro del
SSH— puede abrir `/dev/usb/lp0` e imprimir de verdad**. Es exactamente lo que
esta fase existe para demostrar; dejarlo para la Fase 4 sería descubrir un
problema de permisos tres días después y con los premios reales puestos. Se
arranca **una vez**, se verifica, y se vuelve a dejar el servicio **parado y
habilitado**, que es el estado en que lo dejó la Fase 1.
*Consecuencia:* el pendiente **6** de la §7 del acta de la Fase 1 queda
desactualizado en ese punto concreto. El pendiente 5 (premios reales y
`reiniciar --si`) **no cambia**: sigue siendo de la Fase 4, tal como dice la §1
de este plan. Se anota en el acta de esta fase.

**D12 · Nada de esta fase toca el `README.md` sin visto bueno explícito del
usuario.**
El README contradice hoy varias decisiones (fichas F-001, F-002, F-003, F-052,
F-053, F-088 y F-089). La corrección va **entera y de una sola pasada** en el
punto (d) de la sub-fase 2b, y **solo** si el usuario la autoriza. Si no la
autoriza, las fichas siguen abiertas y así se anota en el acta.

---

## 3. Material necesario

- [ ] **La Raspberry Pi 5** encendida, con su fuente de 27 W.
- [ ] **La impresora AOMU My-A1 (= Zjiang ZJ-80250)** con su **cable de
      corriente** (el que faltó el 2026-09-11) y su **cable USB A-B**.
      *Medido el 2026-09-11: ya está conectada a un puerto USB 3.0 (azul) de la
      Pi, con corriente, con papel y **ya imprimió** (§0-bis H9).*
- [ ] **Un rollo de papel térmico de 80 mm** y, de preferencia, **uno de
      repuesto**. Las pruebas de esta fase gastan entre 60 cm y 1.5 m: cada
      `probar-impresora` son unos 30 cm y se corre dos o tres veces.
- [ ] **La PC Windows 11 del usuario**, con su Wi-Fi (Intel AX211) y su **punto
      de acceso móvil**. *(Esta PC no tiene Ethernet ni WSL: medido.)*
- [ ] **El nombre y la contraseña del Wi-Fi del asadero**, que **solo el usuario
      conoce y solo él teclea** (Paso 0).
- [ ] *(Solo para el respaldo, Paso 10)* nada extra: la Fase 1 ya dejó `bluez`,
      `bluez-tools`, el adaptador `hci0` sin bloqueos y el servicio `bluetooth`
      activo y habilitado.
- [ ] *(Opcional, muy recomendable)* **monitor HDMI y teclado USB** para la Pi.
      No hacen falta si el Paso 0 sale bien; son el único camino de vuelta si la
      Pi se queda sin red y sin SSH (Paso 0, SI FALLA, rama C).

**No hace falta** desarmar nada, ni soldar, ni tocar el header de 40 pines.

---

## 4. Pasos

### Paso 0 · Red de laboratorio: el punto de acceso móvil de Windows

**QUIÉN:** usuario (activa el punto de acceso) + agente (comprueba).
**POR QUÉ EXISTE ESTE PASO:** hoy la Pi **no responde** (§0-bis H1). Solo conoce
el Wi-Fi del asadero, y no se puede cambiar lo que no se puede alcanzar. La
salida es hacer que la PC **se llame igual** que esa red.

**QUÉ HACER — usuario**

1. En la PC: **Configuración → Red e Internet → Punto de acceso móvil**.
2. **«Compartir mi conexión a Internet desde»**: el adaptador **Wi-Fi** (el que
   está conectado a `FDA806_5G`).
3. **«Compartir a través de»**: **Wi-Fi**.
4. **Editar** y escribir:
   - **Nombre de la red:** *exactamente* el mismo del Wi-Fi del asadero.
     Exactamente quiere decir exactamente: mayúsculas, minúsculas, espacios,
     guiones y acentos igual que allá. Una letra distinta y la Pi no entra.
   - **Contraseña de red:** *exactamente* la misma del Wi-Fi del asadero.
   - **Banda de red:** **2.4 GHz**.
5. **Guardar** y encender el interruptor del punto de acceso.
6. Encender la Pi (si estaba apagada) y **esperar de uno a dos minutos**.
7. En la misma pantalla de Windows aparece la lista de **dispositivos
   conectados**: ahí debe salir un equipo llamado `ruleta` con su dirección IP.

> **La contraseña la teclea el usuario, en su propia PC.** Ningún agente la ve,
> la pide, la escribe ni la anota en el acta (§8, prohibición 4). En el acta se
> escribe «el usuario activó el punto de acceso con las credenciales del
> asadero», nunca las credenciales.

**QUÉ HACER — agente**

```bash
ssh ruleta 'hostname'
ssh ruleta 'ip -4 -o addr show scope global'
ssh ruleta 'ping -c 1 -W 3 1.1.1.1 >/dev/null 2>&1 && echo INTERNET_OK || echo SIN_INTERNET'
```

**CRITERIO DE ACEPTACIÓN**

1. `ssh ruleta 'hostname'` imprime exactamente `ruleta`, sin preguntas y sin
   pedir contraseña.
2. `ip -4 -o addr show scope global` muestra una dirección dentro de
   **`192.168.137.0/24`** sobre `wlan0` (el punto de acceso de Windows reparte
   esa red y la PC se queda con `192.168.137.1`). Por ejemplo:

   ```
   2: wlan0    inet 192.168.137.42/24 brd 192.168.137.255 scope global dynamic noprefixroute wlan0
   ```

   *(Si esta versión de Windows repartiera otro rango, **no es un fallo**: se
   anota el rango real en el acta y se ajusta el golden de la §7.1. Lo que
   importa es que la Pi tenga dirección en la red de la PC y que el SSH
   funcione.)*

3. `INTERNET_OK`. *(Si sale `SIN_INTERNET` el paso **no** se da por fallido: la
   impresora se puede probar igual. Lo único que se pierde es el `git pull` del
   Paso 1; se anota y se sigue con el repositorio en `2052e47`.)*

**SI FALLA**

- **`ssh: Could not resolve hostname ruleta.local`** (mDNS no resolvió en la red
  del punto de acceso). La Pi puede estar conectada igual. Buscar su IP desde
  Git Bash:

  ```bash
  ipconfig | grep -A 5 -i "punto de acceso\|Local Area Connection"
  arp -a | grep 192.168.137
  ```

  y conectarse **sin editar ningún archivo**, sobrescribiendo solo el nombre:

  ```bash
  ssh -o HostName=192.168.137.42 ruleta 'hostname'
  ```

  Si eso funciona, **todos los comandos de este plan se corren añadiendo esa
  misma opción** y se anota la IP en el acta. También sirve la lista de
  «dispositivos conectados» de la ventana de Windows.

- **La Pi no aparece en la lista de dispositivos conectados de Windows.** Tres
  causas, en orden de probabilidad:
  1. **El nombre o la contraseña no son idénticos** a los del asadero. Volver a
     escribirlos con cuidado (es lo más común: un espacio final, una mayúscula).
  2. **La contraseña del asadero tiene menos de 8 caracteres.** Windows exige 8
     o más para su punto de acceso, así que **este camino es imposible** con esa
     contraseña: ir a la rama C.
  3. La Pi está apagada, o tardó más de dos minutos. Esperar y reintentar.

- **Rama C · Añadir otra red a la Pi con `nmcli`.** Sirve para dos casos: (a)
  ya hay SSH y se quiere que la Pi también conozca el Wi-Fi del sitio nuevo, o
  (b) no hay SSH y hay que hacerlo desde la consola local de la Pi (monitor HDMI
  y teclado USB, entrando como `asadero` con la contraseña que el usuario anotó
  en papel). **Este comando lo corre el USUARIO en su propia terminal**, no un
  agente, porque hay que teclear una contraseña:

  ```bash
  ssh -t ruleta 'sudo nmcli --ask device wifi connect "NOMBRE_DE_LA_RED_NUEVA"'
  ```

  - `NOMBRE_DE_LA_RED_NUEVA` es un **marcador**: el usuario lo sustituye por el
    nombre real de la red. **El agente prepara el comando con el marcador y no
    lo ejecuta.**
  - `--ask` hace que `nmcli` **pregunte** la contraseña y no la deje escrita en
    el historial ni visible en la lista de procesos. Por eso se usa `--ask` y no
    `password ...`.
  - `ssh -t` hace falta porque `--ask` necesita una terminal de verdad. Un
    agente con `BatchMode=yes` **no puede** correr esto.
  - Desde la consola local de la Pi es el mismo comando sin el `ssh -t`:
    `sudo nmcli --ask device wifi connect "NOMBRE_DE_LA_RED_NUEVA"`.
  - Añadir una red **no borra** la del asadero: la Pi seguirá entrando allá
    cuando vuelva.

- **Último recurso:** regrabar la microSD con Imager. Eso **rehace la Fase 1
  entera** (llave SSH, instalación, servicio) y solo se hace si el usuario lo
  pide expresamente.

**AL TERMINAR LA JORNADA**, si el equipo vuelve al asadero: **apagar el punto de
acceso de la PC**. Si no, en el restaurante habrá dos redes con el mismo nombre
y la Pi puede engancharse a la PC en vez de al router del negocio (§5, trampa
19).

---

### Paso 1 · Poner la Pi en estado de trabajo

**QUIÉN:** agente.

**QUÉ HACER**

1. **Ver en qué estado quedó el servicio** (§0-bis H8: lleva reiniciándose solo
   desde que se encendió la Pi):

   ```bash
   ssh ruleta 'systemctl is-enabled ruleta; systemctl is-active ruleta || true'
   ssh ruleta 'journalctl -u ruleta -n 5 --no-pager'
   ```

   Lo esperable, con el `config.json` de la Pi ya en `"tipo": "archivo"`
   (§0-bis H9), es `enabled` y **`active`**, y en el log
   `Ruleta v1.0.0 | impresora=archivo | datos=...`,
   `Inventario impreso (arranque). Folio actual 00000` y
   `Lista. Esperando jugadas.` —es decir, **la Pi ya imprimió un boleto de
   inventario sola**, que es justamente el motivo del punto 2. **Eso no es una
   avería: es lo previsto.** Solo si alguien devolvió el `config.json` de la Pi
   a `"tipo": "bluetooth"` se verá en su lugar `activating`/`failed` con
   `ERROR de configuración: Falta la dirección Bluetooth de la impresora...`
   repetido cada 3 s; también es lo previsto, se anota y se sigue igual.

2. **Detenerlo y deshabilitarlo** (decisión D6):

   ```bash
   ssh ruleta 'sudo systemctl stop ruleta; sudo systemctl disable ruleta'
   ssh ruleta 'systemctl is-enabled ruleta; systemctl is-active ruleta || true'
   ```

3. **Medir, de paso, los tres goldens que la Fase 1 dejó sin medir** (su §0-bis
   D12 y su acta §3):

   ```bash
   ssh ruleta 'systemctl show -p SubState --value ruleta'
   ssh ruleta 'timedatectl show -p Timezone --value'
   ssh ruleta 'timedatectl show -p NTP --value'
   ssh ruleta 'timedatectl show -p NTPSynchronized --value'
   ssh ruleta 'timedatectl show -p LocalRTC --value'
   ssh ruleta 'date'
   ```

4. **Actualizar el repositorio de la Pi** al commit de cierre de la Fase 1:

   ```bash
   ssh ruleta 'cd ~/ruleta && git status --porcelain'
   ssh ruleta 'cd ~/ruleta && git diff --stat -- instalar.sh herramientas/emparejar.sh'
   # PARADA antes de la línea siguiente: `git checkout --` DESCARTA sin copia
   # lo que haya en esos dos archivos. Solo se corre si los dos comandos de
   # arriba muestran exactamente el estado que describe la §0-bis H9: en
   # `git status --porcelain`, TRES líneas " M" (config.json, instalar.sh y
   # herramientas/emparejar.sh) y, mientras no se saque, la línea
   # "?? config.json.bak-2026-09-12"; y en el `git diff --stat` de esos dos
   # scripts, CERO inserciones y borrados (un cambio de modo no cambia
   # contenido). Si aparece cualquier OTRO archivo, o si esos dos scripts
   # tienen alguna línea añadida o quitada, DETENERSE Y PREGUNTAR: alguien
   # editó la Pi fuera de este plan. El `git checkout --` toca SOLO esos dos
   # scripts: `config.json` NO se toca aquí, porque es la configuración
   # medida la noche del 2026-09-11 y se conserva hasta el Paso 11.
   ssh ruleta 'cd ~/ruleta && git checkout -- instalar.sh herramientas/emparejar.sh'
   ssh ruleta 'cd ~/ruleta && git pull --ff-only'
   ssh ruleta 'cd ~/ruleta && git rev-parse HEAD'
   ssh ruleta 'cd ~/ruleta && git status --porcelain | wc -l'
   ssh ruleta 'cd ~/ruleta && chmod +x instalar.sh herramientas/*.sh'
   ```

   El `git checkout --` de antes del `pull` **no borra trabajo de nadie**:
   deshace únicamente los dos cambios de **modo** `644 → 755` que dejó el Paso 8
   de la Fase 1 (§5, trampa 12), y el `pull` los vuelve a traer, ahora sí
   commiteados. El `chmod +x` final ya es inocuo: el bit viene en el repositorio
   desde `601c4c2`.

5. **Comprobar que el programa sigue sano** antes de tocar hardware:

   ```bash
   ssh ruleta 'cd ~/ruleta && python3 -m unittest discover -s tests -t . 2>&1 | tail -n 3'
   ```

**CRITERIO DE ACEPTACIÓN**

| Comando | Salida esperada |
|---|---|
| `systemctl is-enabled ruleta` | `disabled` |
| `systemctl is-active ruleta \|\| true` | `inactive` |
| `systemctl show -p SubState --value ruleta` | `dead` |
| `timedatectl show -p Timezone --value` | `America/Hermosillo` |
| `timedatectl show -p LocalRTC --value` | `no` |
| `git rev-parse HEAD` | `601c4c2b64fc93e2a76b539f2b79fee9e1f91843` |
| `git status --porcelain \| wc -l` | `1`: solo ` M config.json`, la configuración USB medida la noche del 2026-09-11, que se conserva hasta el Paso 11 (§0-bis H9). Si sale `2`, dentro del repositorio sigue el respaldo `config.json.bak-2026-09-12`: sacarlo con `ssh ruleta 'mv ~/ruleta/config.json.bak-2026-09-12 ~/'` y volver a contar (§5, trampa 13). Si sale `0`, alguien deshizo la configuración de la Pi: detenerse y preguntar |
| `unittest ... \| tail -n 1` | `OK` |

`timedatectl show -p NTP --value` y `-p NTPSynchronized --value` se **anotan
tal como salgan**: si la Pi lleva rato sin internet pueden salir `yes`/`no`, y
eso es información, no un fallo de esta fase (la hora se resuelve con la batería
RTC, Fase 1 Paso 12).

**SI FALLA**

- **`git pull` responde `Your local changes to the following files would be
  overwritten by merge: instalar.sh`**: es el cambio de modo de la Fase 1
  (§0-bis D15 de aquel plan). El `git checkout --` del punto 4 lo resuelve; si
  aun así insiste, `ssh ruleta 'cd ~/ruleta && git -c core.fileMode=false pull
  --ff-only'`.
- **`Could not resolve host: github.com`**: la Pi no tiene internet a través del
  punto de acceso (Paso 0, criterio 3). **No bloquea la fase**: se sigue con la
  Pi en `2052e47`, se anota, y **el `chmod +x` vuelve a ser obligatorio**.
- **Las pruebas fallan**: **detenerse y reportar**, pegando la salida completa.
  Esta fase no cambia código; si las pruebas están rojas antes de empezar, algo
  pasó fuera de este plan.
- **`sudo systemctl disable ruleta` responde `Failed to disable unit`**: leer el
  mensaje entero. Si dice que la unidad no existe, alguien borró
  `/etc/systemd/system/ruleta.service`: **detenerse y preguntar** (habría que
  volver a correr `instalar.sh`, y eso no está en esta fase).

---

### Paso 2 · Impresora encendida, con papel, y su página de autoprueba

**QUIÉN:** usuario.
*(Medido el 2026-09-11: la impresora ya está conectada por USB a un puerto azul
de la Pi, tiene corriente y **ya imprimió con papel puesto** el inventario y el
boleto de prueba, §0-bis H9. Lo único que sigue sin hacerse de este paso es la
**página de autoprueba** —con sus DIP y su ancho— y comprobar que queda rollo
suficiente.)*

**QUÉ HACER**

1. Abrir la tapa, poner el **rollo de 80 mm** con el papel saliendo **por
   encima** del rollo, dejar un dedo de papel fuera y cerrar la tapa hasta oír
   el clic. *(El papel térmico solo imprime por una cara: si se pone al revés no
   sale nada, aunque todo lo demás esté bien.)*
2. Encender la impresora. El indicador de encendido queda **fijo**. Si parpadea,
   casi siempre es falta de papel o la tapa mal cerrada.
3. Presionar **FEED** una vez: el papel debe avanzar.
4. **Página de autoprueba** (sale de la propia impresora, sin computadora):
   **apagar** la impresora, **mantener presionado FEED**, **encender** sin
   soltar y **soltar FEED a los 3 a 5 segundos**.
5. **Guardar esa hoja** (o una foto) y anotar de ella, para el acta:
   - **puntos por línea** (debe decir 576 en una de 80 mm),
   - **columnas** de la fuente A (48, o 42 si el DIP 5 está activo),
   - **posición de los interruptores DIP**, sobre todo **DIP 1** (cortador),
     **DIP 2** (zumbador) y **DIP 5** (42 columnas),
   - **nombre Bluetooth, MAC y PIN**, si los imprime: eso ahorra la búsqueda del
     Paso 10 si algún día hace falta el respaldo.
6. Dejar la impresora **encendida, con papel y con el cable USB puesto** durante
   toda la fase. **No apagarla ni desconectarla entre los Pasos 3 y 8** (§8,
   prohibición 14).

**CRITERIO DE ACEPTACIÓN**

- El papel avanza con FEED.
- La página de autoprueba salió y se puede leer, y sus datos están anotados.
- La impresora queda encendida.

**SI FALLA**

- **No sale nada con FEED:** papel al revés (darle la vuelta al rollo), tapa mal
  cerrada, o la impresora no tiene corriente.
- **La autoprueba no sale** aunque la impresora funcione: no todas las unidades
  la sacan con la misma combinación. **No bloquea la fase**: se sigue al Paso 3
  y los datos (ancho, DIP) se deducen del papel del Paso 7. Se anota como «sin
  autoprueba».
- **Sale la autoprueba en chino o con símbolos raros:** es normal y no dice nada
  malo; el idioma de fábrica de estas impresoras es chino. Lo que importa es que
  imprima.

---

### Paso 3 · Detección del dispositivo USB

**QUIÉN:** agente. **Este paso solo mide; no cambia nada en la Pi.**

**QUÉ HACER — medición común (siempre)**

```bash
ssh ruleta 'lsusb'
ssh ruleta 'ls -l /dev/usb/ 2>/dev/null || echo NO_HAY_CARPETA_DEV_USB'
ssh ruleta 'grep -c "^usblp " /proc/modules'   # 1 = cargado; 0 = NO cargado (rama B1)
ssh ruleta 'sudo dmesg | tail -n 30'
```

En `lsusb` la impresora aparece como una línea con su **VID:PID** (ocho dígitos
hexadecimales separados por dos puntos), por ejemplo
`Bus 001 Device 004: ID 0483:5743 ...`. **Ese par de números es el dato que hace
falta para el Paso 4 y hay que copiarlo tal cual.** No se inventa ni se toma de
la investigación: los valores típicos de la familia (`0483:5743`, `0416:5011`,
`0fe6:811e`) son **pistas para reconocer la línea correcta**, no la respuesta.

En `dmesg` lo esperable, si todo va bien, son líneas como
`usb 1-1: new full-speed USB device number 4 using xhci_hcd` y
`usblp0: USB Bidirectional printer dev 4 if 0 alt 0 proto 2 vid 0x... pid 0x...`.
**Esa línea `usblp0: ...` es la confirmación de que el kernel reconoció una
impresora**, y su `proto` dice si es bidireccional (ver más abajo).

---

**CAMINO A — existe `/dev/usb/lp0` (es lo esperado, §0-bis H3)**

```bash
ssh ruleta 'ls -l /dev/usb/lp0'
ssh ruleta 'udevadm info -q property -n /dev/usb/lp0 | grep -E "^(SUBSYSTEM|DEVNAME|ID_VENDOR_ID|ID_MODEL_ID|ID_SERIAL|ID_USB_INTERFACES)="'
ssh ruleta 'cat /sys/class/usbmisc/lp0/device/ieee1284_id'
ssh ruleta 'udevadm info -a -n /dev/usb/lp0 | grep -m 2 -E "ATTRS\{idVendor\}|ATTRS\{idProduct\}"'
ssh ruleta 'for d in $(grep -lx 07 /sys/bus/usb/devices/*/bInterfaceClass); do i=$(dirname $d); echo "$i clase=$(cat $i/bInterfaceClass) subclase=$(cat $i/bInterfaceSubClass) protocolo=$(cat $i/bInterfaceProtocol)"; done'
```

Qué se saca de cada uno, y para qué sirve después:

| Comando | Qué da | Para qué |
|---|---|---|
| `ls -l /dev/usb/lp0` | dueño, grupo y permisos actuales | Paso 4 |
| `udevadm info -q property` | `SUBSYSTEM=` (normalmente `usbmisc`) y `DEVNAME=`. **Medido la noche del 2026-09-11: para `usbmisc` udev NO expone `ID_VENDOR_ID` ni `ID_MODEL_ID`** (§0-bis H9), así que ese `grep` puede devolver solo esas dos líneas y **eso no es un fallo**: el VID:PID sale de `lsusb` y de `udevadm info -a` (fila siguiente) | escribir la regla del Paso 4 con el `SUBSYSTEM` **medido**, no supuesto |
| `ieee1284_id` | la cadena que declara la impresora | **medido la noche del 2026-09-11: `MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1`** (§0-bis H9). Es decir, la unidad **no** declara el `MDL:ZJ-80250` del PPD del fabricante: el PPD describe el driver, no lo que anuncia esta impresora, y eso **no** cambia nada (sigue siendo clase PRINTER y sigue hablando ESC/POS). Se pega tal cual salga y solo se detiene la fase si difiere de esa cadena. Si esa ruta de `/sys` no existe, buscarla con `ssh ruleta 'ls /sys/class/usbmisc/'` y repetir con el nombre real |
| `udevadm info -a` | `ATTRS{idVendor}`, `ATTRS{idProduct}` | son **exactamente** los valores que van en la regla |
| el bucle de `bInterfaceClass` | `clase=07` (impresora) y `protocolo=` | **`protocolo=02`** = bidireccional (se puede preguntar por el papel: habilita el cambio (b) de 2b). **`protocolo=01`** = unidireccional: por USB **nunca** se podrá saber si hay papel, y eso hay que escribirlo en el README y en la capacitación |

**CRITERIO DE ACEPTACIÓN del camino A**

1. `ssh ruleta 'test -c /dev/usb/lp0 && echo NODO_OK'` imprime `NODO_OK`.
   *(`test -c` comprueba que es un **dispositivo de caracteres**, no un archivo
   normal. Esa distinción importa: ver §5, trampa 4.)*
2. El VID:PID quedó anotado, con sus cuatro dígitos hexadecimales cada uno.
3. El `ieee1284_id` quedó pegado en el acta **tal cual salga**, diga lo que
   diga.
4. El protocolo de la interfaz (`01` o `02`) quedó anotado.

---

**CAMINO B — NO existe `/dev/usb/lp*`**

Diagnóstico, en este orden. Cada rama dice qué hacer:

```bash
ssh ruleta 'lsusb -t'
ssh ruleta 'systemctl is-active cups 2>/dev/null; systemctl is-active cups-browsed 2>/dev/null; true'
```

- **B1 · `usblp` no está cargado.** Cargarlo y volver a mirar:

  ```bash
  ssh ruleta 'sudo /usr/sbin/modprobe usblp && sleep 1 && ls -l /dev/usb/ 2>/dev/null || echo SIGUE_SIN_NODO'
  ```

  Si con eso aparece el nodo, **hay que hacerlo permanente** (si no, se pierde
  al reiniciar):

  ```bash
  ssh ruleta 'echo usblp | sudo tee /etc/modules-load.d/ruleta-usblp.conf'
  ```

  y **anotarlo para el cambio (a) de 2b**, porque `instalar.sh` tendrá que
  hacerlo también.

- **B2 · CUPS está activo y se quedó con el dispositivo.** El backend USB de
  CUPS desprende a `usblp` y el nodo desaparece. Se quita de en medio (esta Pi
  no imprime por CUPS, imprime ESC/POS directo):

  ```bash
  ssh ruleta 'sudo systemctl disable --now cups cups-browsed 2>/dev/null; true'
  ssh ruleta 'sudo /usr/sbin/modprobe -r usblp; sudo /usr/sbin/modprobe usblp; sleep 1; ls -l /dev/usb/'
  ```

  *(Pista de que puede pasar: el usuario `asadero` está en el grupo `lpadmin`,
  que viene con CUPS.)*

- **B3 · La interfaz NO es de clase impresora.** Comprobarlo con el VID:PID
  medido:

  ```bash
  ssh ruleta 'lsusb -v -d VID:PID 2>/dev/null | grep -E "bInterfaceClass|bInterfaceProtocol|iProduct"'
  ```

  Si `bInterfaceClass` es `255 Vendor Specific Class` en vez de
  `7 Printer`, **`usblp` nunca la va a reclamar**. Aquí manda la decisión
  **D10**: no se escribe un transporte USB nuevo. Se **abre una ficha**, se
  anota en el acta y **se pasa al Paso 10 (respaldo Bluetooth)**.

- **B4 · `lsusb` ni siquiera lista la impresora.** No es un problema de Linux:
  es cable, puerto o corriente. Probar (por este orden) otro cable USB, un
  puerto **USB 2.0 (negro)** de la Pi, y comprobar que la impresora está
  encendida. Algunas unidades solo enumeran cuando están encendidas y con la
  tapa cerrada.

**SI FALLA todo el Paso 3** (ninguna rama produce nodo ni explicación):
**detenerse y reportar** con la salida completa de `lsusb`, `lsusb -t` y
`dmesg | tail -n 30`. No seguir al Paso 4 «a ver si suena la flauta»: sin nodo
no hay nada que configurar.

---

### Paso 4 · Permisos: regla `udev` por VID:PID y grupo

> **YA HECHO Y SUPERADO (2026-09-11). NO SE VUELVE A CORRER TAL CUAL.** Los
> permisos se aplicaron a mano esa noche y desde el deploy de 2b los deja
> `instalar.sh` solo, en su paso `5/7`. **Los nombres buenos son los de 2b, no
> los del punto 2 de abajo:** el archivo es
> `/etc/udev/rules.d/61-ruleta-impresora-usb.rules` y el enlace
> `/dev/ruleta-impresora`. El punto **2.a de abajo (borrar esa regla) y el 2.b
> (escribir `61-ruleta-impresora.rules` con `SYMLINK+="impresora-ruleta"`) están
> **derogados**: correrlos hoy dejaría a la Pi sin el enlace que usa
> `config.json` y crearía una segunda regla para el mismo dispositivo. El texto
> se conserva porque explica **por qué** la regla es como es (ficha **F-139**,
> cerrada). Lo único que se sigue usando de este paso son sus comandos de
> **medición** (puntos 1, 3 y 5).

**QUIÉN:** agente. **Requiere haber medido el VID:PID en el Paso 3.**

**QUÉ HACER**

1. **Medir el estado actual** (para poder demostrar después que cambió):

   ```bash
   ssh ruleta 'stat -c "%n %F %a %U %G" /dev/usb/lp0'
   ssh ruleta 'id -nG'
   ssh ruleta 'test -w /dev/usb/lp0 && echo ESCRIBIBLE || echo NO_ESCRIBIBLE'
   ```

   Lo esperado **hoy**, porque la noche del 2026-09-11 los permisos ya se
   aplicaron a mano (§0-bis H9): `/dev/usb/lp0 character special file 660 root
   lp`, los grupos **con `lp`** y `ESCRIBIBLE`. *(Si salieran los grupos **sin
   `lp`** y `NO_ESCRIBIBLE`, sería el estado virgen que describen la §0-bis H7 y
   la ficha F-052; este paso lo arregla igual.)* Hay que mirar además la regla
   que ya existe, porque el punto 2 la sustituye:

   ```bash
   ssh ruleta 'ls -l /etc/udev/rules.d/'
   ssh ruleta 'cat /etc/udev/rules.d/61-ruleta-impresora-usb.rules 2>/dev/null || echo NO_ESTA'
   ssh ruleta 'getent group lp'
   ```

2. **Escribir la regla, sustituyendo `@VID@` y `@PID@` por lo medido** (cuatro
   dígitos hexadecimales **en minúsculas** cada uno; `udev` compara texto, así
   que `0483` y `0483` sí, pero `483` no), y `usbmisc` por el `SUBSYSTEM` que
   haya reportado `udevadm` en el Paso 3:

> **Ojo al copiar este comando:** el texto del `<<"EOF"` y la línea `EOF'` que
> lo cierra van **pegados al margen izquierdo, sin un solo espacio delante**. Si
> se indentan, el intérprete nunca encuentra el final y el comando se queda
> colgado. Por eso el bloque siguiente no está sangrado.

```bash
# 2.a Borrar la regla que se escribio a mano la noche del 2026-09-11 (S0-bis H9).
# Se llama distinto (61-ruleta-impresora-usb.rules) y crea otro enlace
# (/dev/ruleta-impresora). Dejar las dos deja dos enlaces vivos y rompe el
# golden de 2b que deriva el conjunto de archivos de reglas del instalador.
# El servicio esta parado desde el Paso 1, asi que quitar ese enlace no rompe
# nada; el Paso 5 repunta "ruta" a /dev/usb/lp0 acto seguido.
ssh ruleta 'sudo rm -f /etc/udev/rules.d/61-ruleta-impresora-usb.rules'

# 2.b Escribir la regla canonica. Medido la noche del 2026-09-11: @VID@=0418 y
# @PID@=5011. Si el Paso 3 midio otra cosa, manda el Paso 3.
ssh ruleta 'sudo tee /etc/udev/rules.d/61-ruleta-impresora.rules >/dev/null <<"EOF"
# Impresora termica de la ruleta (AOMU My-A1, familia POS-80).
# Da acceso al grupo lp y un nombre estable que no depende del numero de nodo.
SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*", ATTRS{idVendor}=="@VID@", ATTRS{idProduct}=="@PID@", GROUP="lp", MODE="0660", SYMLINK+="impresora-ruleta"
EOF'
```

3. **Aplicarla** (no hace falta desconectar el cable):

   ```bash
   ssh ruleta 'sudo udevadm control --reload && sudo udevadm trigger --subsystem-match=usbmisc'
   ssh ruleta 'ls -l /dev/usb/lp0 /dev/impresora-ruleta'
   ```

4. **Meter al usuario en el grupo `lp`:**

   ```bash
   ssh ruleta 'sudo /usr/sbin/usermod -aG lp asadero'
   ssh ruleta 'id -nG'
   ssh ruleta 'test -w /dev/usb/lp0 && echo ESCRIBIBLE || echo NO_ESCRIBIBLE'
   ```

   *(No hay que «cerrar sesión y volver a entrar»: **cada `ssh ruleta '...'` es
   una sesión nueva**, así que el grupo ya aparece en el comando siguiente. Lo
   que sí sigue valiendo es la trampa 5 de la Fase 1 para una sesión
   interactiva que estuviera abierta desde antes.)*

**CRITERIO DE ACEPTACIÓN**

| Comando | Salida esperada |
|---|---|
| `stat -c "%a %U %G" /dev/usb/lp0` | `660 root lp` |
| `id -nG \| tr " " "\n" \| grep -cx lp` | `1` |
| `test -w /dev/usb/lp0 && echo ESCRIBIBLE` | `ESCRIBIBLE` |
| `test -c /dev/impresora-ruleta && echo ENLACE_OK` | `ENLACE_OK` |
| `grep -c "idVendor" /etc/udev/rules.d/61-ruleta-impresora.rules` | `1` |

**Y una advertencia que no es un criterio pero evita una sorpresa en el Paso
13:** que **`asadero` por SSH** pueda escribir **no demuestra** que **el
servicio** pueda. El servicio lo lanza systemd, y qué grupos suplementarios
recibe se mide en el Paso 13 leyendo `/proc/<pid>/status`. Si ahí falta `lp`,
hay dos salidas y las dos están decididas (D4): la inmediata es cambiar
`MODE="0660"` por `MODE="0666"` en esta misma regla; la limpia es añadir
`SupplementaryGroups=gpio lp` a `ruleta.service`, que es un cambio de código y
va en 2b.

**SI FALLA**

- **El enlace `/dev/impresora-ruleta` no aparece y los permisos no cambian:** la
  regla no está casando. Verlo con:

  ```bash
  ssh ruleta 'sudo udevadm test $(udevadm info -q path -n /dev/usb/lp0) 2>&1 | tail -n 25'
  ```

  Causas frecuentes: el `SUBSYSTEM` real no es `usbmisc` (usar el medido);
  `idVendor`/`idProduct` en mayúsculas o con menos de cuatro dígitos; el archivo
  guardado con otro nombre. **Regla de emergencia sin VID:PID** (vale porque en
  esta Pi hay una sola impresora, y hay que anotarla como tal en el acta):

  ```
  SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*", GROUP="lp", MODE="0660", SYMLINK+="impresora-ruleta"
  ```

- **`test -w` sigue diciendo `NO_ESCRIBIBLE` después del `usermod`:** comprobar
  `ssh ruleta 'getent group lp'` (debe listar a `asadero`) y volver a mirar
  `ls -l`. Si el grupo está bien y el nodo también, y aun así no deja escribir,
  **detenerse y preguntar**. `MODE="0666"` deja el dispositivo escribible por
  cualquier usuario de la Pi, y tanto la decisión **D4** como la **prohibición
  13** lo reservan para **una sola** medición: la del Paso 13, cuando se
  demuestre que **el servicio** no puede abrir el nodo. Aquí esa medición aún no
  existe, así que la decisión no es del ejecutor. Si el usuario autoriza el
  `0666`, se aplica en esta misma regla, se recarga y **se anota en el acta**
  como desviación aceptada.

- **`udevadm: command not found`:** el PATH de SSH no interactivo. Usar
  `sudo udevadm ...` (como en los comandos de arriba) o la ruta absoluta que
  devuelva `ssh ruleta 'command -v udevadm || ls -l /usr/bin/udevadm /sbin/udevadm 2>/dev/null'`.

---

### Paso 5 · `config.json` de la Pi: `tipo: archivo` y **añadir** `ruta`

**QUIÉN:** agente. **Solo en la Pi** (decisión D5).

**QUÉ HACER**

1. **Re-grep antes de editar** (§6): comprobar que el archivo sigue como este
   plan supone.

   ```bash
   ssh ruleta 'cd ~/ruleta && grep -n "\"tipo\"\|\"ruta\"" config.json'
   ```

   Esperado **en la Pi** (§0-bis H9): **dos** líneas, `"tipo": "archivo",` y
   `"ruta": "/dev/ruleta-impresora",`, porque el archivo ya se editó a mano la
   noche del 2026-09-11. Lo único que hace este paso entonces es **repuntar la
   `ruta`** a `/dev/usb/lp0`, que es el nombre que crea la regla del Paso 4.
   En el **repositorio** sigue habiendo **una** sola línea, la 16, con
   `"tipo": "bluetooth",` y **ninguna** de `"ruta"` (ficha F-077): por eso el
   Paso 11 no es opcional. Si el archivo de la Pi estuviera todavía en
   `"tipo": "bluetooth",` sin `"ruta"`, también vale: el punto 3 cubre los dos
   casos. Cualquier **tercer** estado (otra `ruta`, otro `tipo`): **detenerse y
   preguntar**.

2. **Respaldar el archivo fuera del repositorio** (si se guarda dentro, `git
   status` deja de estar limpio y el Paso 11 falla):

   ```bash
   ssh ruleta 'cp -n ~/ruleta/config.json ~/config.json.antes-de-fase2'
   ```

3. **Editar conservando el formato** (una sustitución exacta; si no encuentra
   exactamente una coincidencia, **falla y no escribe nada**):

> **Ojo al copiar:** el cuerpo del `<<"PY"` y la línea `PY'` que lo cierra van
> **pegados al margen izquierdo**. Si se indentan, pasan dos cosas y las dos son
> malas: el intérprete no encuentra el final del bloque, y Python recibe el
> programa sangrado y contesta `IndentationError`.

```bash
ssh ruleta 'cd ~/ruleta && python3 - <<"PY"
import pathlib
p = pathlib.Path("config.json")
t = p.read_text(encoding="utf-8")
nuevo = "    \"tipo\": \"archivo\",\n    \"ruta\": \"/dev/usb/lp0\",\n"
noche = "    \"tipo\": \"archivo\",\n    \"ruta\": \"/dev/ruleta-impresora\",\n"
bluetooth = "    \"tipo\": \"bluetooth\",\n"
if t.count(nuevo) == 1:
    print("ya estaba como lo quiere el plan: no se toca")
elif t.count(noche) == 1:
    p.write_text(t.replace(noche, nuevo, 1), encoding="utf-8")
    print("editado: venia de la noche del 2026-09-11")
elif t.count(bluetooth) == 1:
    p.write_text(t.replace(bluetooth, nuevo, 1), encoding="utf-8")
    print("editado: venia del repositorio")
else:
    raise SystemExit("config.json no esta en ninguno de los tres estados previstos: parar y preguntar")
PY'
```

   Se edita así, y no con `nano` ni reescribiendo el JSON entero, por dos
   razones: (a) un agente no puede usar `nano`; (b) volcar el JSON con
   `json.dump` **reformatea el archivo completo** (es lo que hace
   `emparejar.sh`) y convierte el commit del Paso 11 en un diff ilegible.

4. **Comando de resumen** (se va a usar varias veces; conviene tenerlo a mano):

```bash
ssh ruleta 'cd ~/ruleta && python3 - <<"PY"
import json
imp = json.load(open("config.json", encoding="utf-8"))["impresora"]
print(imp["tipo"], imp["ruta"], imp["codepage"], imp["codepage_n"],
      imp["chars_por_linea"], imp["corte"], imp["beep"])
PY'
```

**CRITERIO DE ACEPTACIÓN**

| Comando | Salida esperada |
|---|---|
| el comando de resumen | `archivo /dev/usb/lp0 cp858 19 48 auto False` |
| `cd ~/ruleta && git diff --numstat config.json` | `2	1	config.json` (dos líneas añadidas, una quitada: nada más) |

**SI FALLA**

- **El script termina con `config.json no esta en ninguno de los tres estados previstos: parar y preguntar`**: el
  archivo no es el que este plan describe. **Detenerse y preguntar.** No
  «arreglarlo» a mano: significa que alguien tocó `config.json` fuera de este
  plan, y hay que saber quién y por qué antes de seguir.
- **`git diff --numstat` da otros números:** el editor tocó más de lo previsto.
  Restaurar con `ssh ruleta 'cd ~/ruleta && git checkout -- config.json'` y
  volver a empezar el paso (el respaldo del punto 2 sigue ahí por si acaso).
- **`KeyError: 'ruta'` en el comando de resumen:** la edición no se aplicó.
  Repetir el punto 3.

---

### Paso 6 · `python3 -m ruleta diagnostico`

**QUIÉN:** agente.

**QUÉ HACER**

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico; echo "codigo=$?"'
```

**CRITERIO DE ACEPTACIÓN**

**Cero `[!!]` y código 0.** La salida cambió con la sub-fase 2b; esto es lo
**medido en la Pi el 2026-09-11 después del deploy**, con la impresora
conectada, con papel (poco) y con el servicio parado:

```
Ruleta v1.0.0 | Python 3.13.5 | linux
Configuración: /home/asadero/ruleta/config.json
Carpeta de datos: /home/asadero/ruleta/datos
  [ok] la carpeta de datos se puede escribir
  [ok] PIL 11.1.0
  [ok] gpiozero 2.0.1
  [ok] lgpio 0.2.2.0
  [ok] logo: /home/asadero/ruleta/logo.png
  [ok] inventario: folio 00000
  [ok] impresora conectada en /dev/ruleta-impresora (dispositivo, se puede escribir)
  [??] la impresora reporta poco papel: ten listo el rollo de repuesto
codigo=0
```

Son **siete `[ok]` y un `[??]`**. Antes de 2b eran seis `[ok]` y un
`[--] impresora tipo 'archivo': no se prueba Bluetooth`, y `gpiozero` y `lgpio`
salían **sin número de versión** (ficha F-051, resuelta por el punto (c)/(e) de
2b). El conteo exacto depende de la impresora y del servicio: ver la §7.5, que
lista los cuatro casos posibles.

> **Este paso ya dice algo sobre la impresora, pero no lo suficiente**
> (decisión D7). Demuestra que la ruta existe, que es un dispositivo, que se
> puede escribir en él y —con el servicio parado— que contesta. **No demuestra
> que el boleto salga legible, derecho y cortado**: eso solo lo dice el papel
> del Paso 7.

**SI FALLA**

- **`[!!] no se puede escribir en la carpeta de datos`:** casi seguro alguien
  corrió el programa con `sudo` y dejó archivos de root en `datos/` (§5, trampa
  4). Arreglo: `ssh ruleta 'sudo chown -R asadero: ~/ruleta/datos'` — y no
  volver a usar `sudo` con `python3 -m ruleta`.
- **`ERROR de configuración: ...`** y código 2: el `config.json` quedó inválido
  en el Paso 5. El mensaje dice exactamente qué llave corregir. Si no está
  claro, restaurar con `git checkout -- config.json` y repetir el Paso 5.
- **Un `[!!]` que hable de la impresora:** desde 2b **sí puede pasar, y es la
  gracia del cambio**. Son tres, y cada uno trae su arreglo en el propio
  mensaje: `no existe la ruta de la impresora` (cable suelto o impresora
  apagada), `sin permiso para escribir` (falta la regla `udev` o el grupo `lp`)
  y `la impresora reporta SIN PAPEL` / `está fuera de línea`. Se atiende lo que
  diga y se repite el diagnóstico; no hay que detenerse ni preguntar.

---

### Paso 7 · `probar-impresora` y lectura del papel

**QUIÉN:** agente (lanza) + **usuario (lee el papel y decide)**.
**Este es el paso que de verdad cierra la fase.**

**ANTES DE LANZARLO**, comprobar que el servicio sigue parado. **`probar-
impresora` es el único comando que imprime y NO avisa si el servicio está
corriendo** (§5, trampa 2; ficha F-089):

```bash
ssh ruleta 'systemctl is-active ruleta || true'
```

Debe decir `inactive`. Si dice otra cosa, volver al Paso 1.

**QUÉ HACER**

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta probar-impresora; echo "codigo=$?"'
```

En la consola debe salir:

```
Enviando boleto de prueba (NNNN bytes) por archivo...
Listo. Revisa qué línea de acentos salió bien y pon ese número en impresora.codepage_n.
codigo=0
```

**Y, sobre todo, tiene que salir papel.**

**QUÉ MIRA EL USUARIO EN EL PAPEL** (esta tabla es el corazón del paso):

| Qué mirar | Qué debe verse | Si no se ve así |
|---|---|---|
| Las cuatro líneas `ESC t 0`, `ESC t 2`, `ESC t 16`, `ESC t 19` | **una** de ellas muestra bien `ñ Ñ á é í ó ú Á É Í Ó Ú ü ¿ ¡ º`. Lo esperado es la de `19 (cp858)` | anotar **cuál** salió bien y aplicar su pareja en el Paso 8 |
| Si **todas** salen como ideogramas chinos | — | `cancelar_modo_chino` ya es `true`, así que el `FS .` se está mandando; probar el **DIP 4** de la impresora («sin caracteres chinos»). Ver §5, trampa 17 |
| La regla `012345678901234...` | llena la línea **exacta**: ni se corta ni sobra espacio | si se corta a la derecha, la impresora está en **42 columnas** (DIP 5): `chars_por_linea: 42` (o cambiar el DIP) |
| Los bloques `Tamaño 1x` a `4x` y `Negrita` | legibles y sin cortarse por la derecha | mismo caso que el ancho |
| El logo | nítido, centrado, sin bandas movidas ni basura | Paso 8, apartado «logo» |
| El corte final | cortó solo, dejando una pestaña pequeña sin cortar | si **no** cortó: `corte: "parcial"` y revisar el **DIP 1**. Si cortó **a mitad del texto**: subir `lineas_antes_corte` |
| La frase final | `Si esto se cortó solo, el cortador funciona.` | si esa frase quedó dentro del rollo, el papel no avanzó bastante: subir `lineas_antes_corte` |

**CRITERIO DE ACEPTACIÓN**

1. `codigo=0`.
2. **Papel en la mano**: boleto completo, legible, con el logo, y cortado.
3. Al menos una de las cuatro líneas de acentos se ve **perfecta** (con `ñ`,
   `á`, `¿` y `¡`), y está anotado cuál.
4. Hay **foto del papel** guardada para el acta.

**SI FALLA**

- **`FALLÓ: no se pudo abrir /dev/usb/lp0: [Errno 13] Permission denied`**: el
  Paso 4 no quedó. Volver a él (`test -w`, `stat`, `getent group lp`).
- **`FALLÓ: no se pudo abrir /dev/usb/lp0: [Errno 2] No such file or
  directory`**: el nodo desapareció. Alguien apagó o desconectó la impresora.
  Volver al Paso 3.
- **`codigo=0` pero NO sale papel.** Es la falla más engañosa de toda la fase.
  Comprobar en este orden:
  1. **¿A dónde se fue el boleto?** Correr el comando de resumen del Paso 5. Si
     `ruta` no es `/dev/usb/lp0`, el boleto se escribió en un archivo:
     `ssh ruleta 'ls -l ~/ruleta/salida_impresora.bin 2>/dev/null'`. (§5,
     trampa 5.)
  2. **¿`/dev/usb/lp0` es de verdad un dispositivo?**
     `ssh ruleta 'ls -l /dev/usb/lp0 2>/dev/null || echo NO_EXISTE'` (la primera
     letra debe ser una `c`, de «dispositivo de caracteres»; si es un `-`, es un
     archivo normal).
     Si es un archivo normal, alguien corrió el programa con `sudo` estando
     el nodo ausente y **creó un archivo que ahora tapa el dispositivo** (§5,
     trampa 4). Arreglo: `ssh ruleta 'sudo rm -f /dev/usb/lp0'`, desconectar y
     volver a conectar el cable USB, y repetir el Paso 3.
  3. **¿La impresora está en pausa?** Apagarla y encenderla, comprobar papel y
     tapa, y repetir.
- **Sale papel pero con caracteres sueltos o basura:** es la tabla de
  caracteres o el ritmo; ir al Paso 8. Por cable el ritmo casi nunca es el
  problema (§0-bis H6).
- **Sale papel en blanco:** el rollo está al revés (Paso 2) o es papel normal,
  no térmico.

---

### Paso 8 · Ajustes iterativos en el `config.json` de la Pi

**QUIÉN:** agente (aplica) + usuario (decide, mirando el papel).

**QUÉ HACER**

Se cambia **una cosa a la vez**, se vuelve a correr `probar-impresora` y se
vuelve a mirar el papel. **Máximo tres vueltas**: si a la tercera el papel sigue
mal, **detenerse y preguntar** (algo no encaja con lo que este plan supone).

**Herramienta de edición** (conserva el formato del archivo y falla si no
encuentra exactamente una coincidencia). Se editan las llaves que hagan falta
poniendo el valor **tal como se escribe en JSON**: los números sin comillas, el
texto con comillas, y `true` / `false` en minúsculas:

```bash
ssh ruleta 'cd ~/ruleta && python3 - <<"PY"
import re, pathlib
CAMBIOS = {
    # EJEMPLO A SUSTITUIR por lo que pida el papel (ver la tabla de parejas de
    # abajo). Se dejan aquí los valores que el archivo YA tiene, para que un
    # pegado sin sustituir no cambie nada: la tabla 16 está MEDIDA como basura
    # en esta unidad (§0-bis H9), así que no se pone salvo que el papel lo diga.
    "codepage_n": "19",
    "codepage": "\"cp858\"",
}
p = pathlib.Path("config.json")
t = p.read_text(encoding="utf-8")
for clave, valor in CAMBIOS.items():
    patron = re.compile(r"(\"" + clave + r"\"\s*:\s*)[^,\n]+")
    t, n = patron.subn(lambda m: m.group(1) + valor, t, count=1)
    assert n == 1, "no encontre exactamente una vez la llave " + clave
p.write_text(t, encoding="utf-8")
print("aplicado:", CAMBIOS)
PY'
```

**Tabla de acentos.** La pareja `codepage_n` / `codepage` va **siempre junta**:
el número es lo que se le manda a la impresora (`ESC t n`) y el nombre es con lo
que Python codifica el texto. Si se cambian por separado, el papel sale peor que
antes. Las parejas válidas salen de `CODECS_TABLA` (`ruleta/escpos.py`, línea
50):

| Línea que salió bien en el papel | `codepage_n` | `codepage` |
|---|---|---|
| `ESC t 0` | `0` | `"cp437"` |
| `ESC t 2` | `2` | `"cp850"` |
| `ESC t 16` | `16` | `"cp1252"` |
| `ESC t 19` | `19` | `"cp858"` (lo que ya está puesto) |

*(`cp437` no tiene `Á Í Ó Ú`: el programa las imprime sin acento en vez de con
un `?`, así que si la línea 0 es la única buena, se acepta sabiendo que las
mayúsculas acentuadas se pierden.)*

**Ancho.** Si la regla se corta: `"chars_por_linea": 42`. **No** tocar
`ancho_puntos` (576 es el ancho físico del cabezal de 80 mm y solo cambia si la
impresora fuera de 58 mm).

**Corte.** Si no cortó: `"corte": "parcial"`. Si corta a mitad del texto:
`"lineas_antes_corte": 3` (y subir de uno en uno). Con `corte: "auto"` el valor
por defecto es **1** línea, porque `auto` (`GS V 66 0`) hace que la impresora
avance sola hasta su cuchilla; con los demás modos el defecto es **5**
(`ruleta/escpos.py`, `lineas_antes_corte_por_defecto`).

**Zumbador.** El PPD confirma que esta impresora tiene zumbador (§0-bis H3),
pero además hace falta el **DIP 2**. Se queda en `"beep": false` **salvo que el
usuario lo pida**: suena en **cada** boleto y en un restaurante lleno eso cansa
rápido. Si lo pide: `"beep": true`, probar, y si no suena es el DIP, no el
programa.

**Logo.** Si sale con bandas movidas, basura o incompleto:
`"banda_imagen": 32`, y si aún así, `"logo_ancho": 320`. Si sale todo negro o
todo blanco, el problema es el PNG (rehacerlo de 8 bits con fondo blanco), no la
configuración. *(Por cable, `tamano_bloque` y `pausa_bloque_seg` **no hacen
nada**: §0-bis H6.)*

**Después de cada cambio:**

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta probar-impresora; echo "codigo=$?"'
```

No hace falta reiniciar nada: el servicio está parado y el programa lee
`config.json` en cada arranque.

**CRITERIO DE ACEPTACIÓN**

1. El **último** boleto de prueba cumple las siete filas de la tabla del Paso 7.
2. El comando de resumen del Paso 5 devuelve los valores finales, y quedan
   **copiados literalmente en el acta** (son los que se llevan al repositorio en
   el Paso 11).
3. `ssh ruleta 'cd ~/ruleta && git diff --stat config.json'` muestra que **solo**
   cambió `config.json` y solo en las llaves esperadas.

**SI FALLA**

- **El `assert` de la herramienta se dispara:** la llave no está escrita en una
  sola línea, o no existe. Mirar el archivo con
  `ssh ruleta 'cd ~/ruleta && grep -n LLAVE config.json'` y **preguntar** antes
  de forzar nada.
- **Tres vueltas y el papel sigue mal:** detenerse y reportar con las fotos de
  los tres intentos y el `config.json` de cada uno. Puede ser una unidad con
  firmware distinto al de la familia; esa decisión no es del ejecutor.

---

### Paso 9 · Vista previa de los boletos (lo que quedó pendiente de la Fase 1)

**QUIÉN:** agente. **No gasta papel.**

**QUÉ HACER**

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta vista-previa --todos'
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta vista-previa --todos | grep -c "=== Boleto de premio:"'
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta vista-previa --todos | grep -c "\[CORTE\]"'
```

**CRITERIO DE ACEPTACIÓN**

1. `grep -c "=== Boleto de premio:"` → **7** (uno por premio de prueba; el
   número **se deriva** de la lista `premios` de `config.json`: si alguien la
   cambió, cambia el número, y entonces hay que revisar por qué).
2. `grep -c "\[CORTE\]"` → **9** = 7 boletos de premio + 1 de consuelo + 1 de
   inventario. Cada documento termina con su corte.
3. En la salida se leen bien los acentos y signos: `¡GANASTE!` con su `¡`,
   `Válido únicamente el día de hoy.` con sus tildes.
4. Las líneas grandes salen con los caracteres **repetidos** (`AAssaaddeerroo
   3333`, `¡¡GGAANNAASSTTEE!!`, `TTTTEEEESSSSTTTT    1111`). **Eso es correcto,
   no es basura**: la consola imita el doble y el cuádruple ancho de la
   impresora.

**SI FALLA**

- **Salen `Ã¡`, `Ã±` o signos de interrogación:** falta `PYTHONIOENCODING=utf-8`
  delante del comando (Fase 1, §5 trampa 6). No es un problema de la impresora.
- **`No module named ruleta`:** faltó el `cd ~/ruleta` (Fase 1, §5 trampa 3).
- **Los conteos no dan 7 y 9:** alguien cambió la lista de premios. No es un
  fallo de esta fase, pero **hay que anotarlo**: los premios reales son de la
  Fase 4.

---

### Paso 10 · Respaldo Bluetooth — **solo si el USB no es viable**

**QUIÉN:** agente + usuario.
**CUÁNDO SE HACE ESTE PASO:** solo si el Paso 3 acabó en la rama **B3**
(dispositivo «vendor-specific», sin nodo posible) o si el Paso 7 falló de forma
irrecuperable. **Si el USB funcionó, este paso se salta** y se anota «no
aplicó». El Bluetooth no se prueba «por si acaso»: cada prueba gasta papel y
tiempo, y el camino ya está escrito para el día que haga falta.

**ANTES:** anotar en el acta **por qué** se abandona el USB, con la salida
concreta que lo demuestra.

**QUÉ HACER**

1. **Respaldar la configuración**, porque `emparejar.sh` la va a reescribir
   (§5, trampa 10):

   ```bash
   ssh ruleta 'cp ~/ruleta/config.json ~/config.json.antes-de-bluetooth'
   ```

2. **Comprobar el adaptador** (la Fase 1 lo dejó listo):

   ```bash
   ssh ruleta 'systemctl is-active bluetooth; bluetoothctl show | grep -c "Powered: yes"'
   ssh ruleta 'systemctl is-active ModemManager 2>/dev/null; true'
   ```

   Si `ModemManager` está `active`, quitarlo de en medio: abre los dispositivos
   serie nuevos y les manda comandos `AT`, **que la impresora imprime como
   texto**:

   ```bash
   ssh ruleta 'sudo systemctl disable --now ModemManager'
   ```

3. **Buscar la impresora sin interactividad** (con la impresora encendida):

   ```bash
   ssh ruleta 'timeout 30 bluetoothctl --timeout 20 scan on >/dev/null 2>&1; bluetoothctl devices'
   ```

   Identificar la línea de la impresora: el nombre suele ser del estilo
   `XPrinter_XXXX`, `ZJ-80250`, `Printer001` o `BlueTooth Printer`. **Si la
   página de autoprueba del Paso 2 trajo la MAC, usar esa y ahorrarse la
   búsqueda.**

4. **Emparejar pasando la MAC como argumento.** **Sin argumento el script es
   interactivo** (`read -rp`, línea 55) y por SSH no interactivo muere con
   `MAC inválida: ''` (ficha F-078):

   ```bash
   ssh ruleta 'cd ~/ruleta && ./herramientas/emparejar.sh AA:BB:CC:DD:EE:FF'
   ```

   El script prueba solo los PIN `0000` y `1234` con `bt-agent` leyéndolos de un
   archivo temporal. **Ningún agente y ninguna persona teclea un PIN** (§8,
   prohibición 4). Al terminar, el script escribe `impresora.mac` y **pone
   `impresora.tipo` en `"bluetooth"`**, reformateando el archivo entero.

5. **Comprobar el emparejamiento y el perfil serie:**

   ```bash
   ssh ruleta 'bluetoothctl info AA:BB:CC:DD:EE:FF | grep -E "Name|Paired|Trusted|Serial Port"'
   ```

   Debe decir `Paired: yes`, `Trusted: yes` y aparecer `Serial Port` (el perfil
   SPP). *(Que `bluetoothctl connect` conteste `NotAvailable` es **normal** en
   una impresora solo-SPP: la conexión la abre el programa, no `bluetoothctl`.)*

6. **Diagnóstico y prueba.** Por Bluetooth el diagnóstico **sí** prueba la
   conexión de verdad, así que aquí sí vale como criterio:

   ```bash
   ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico; echo "codigo=$?"'
   ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta probar-impresora; echo "codigo=$?"'
   ```

   Si el diagnóstico dice `la impresora escucha en el canal N`, poner ese
   `"canal": N` en `config.json` con la herramienta del Paso 8 y repetir.

7. **Volver al Paso 7** (lectura del papel) y al Paso 8 (ajustes): la tabla de
   acentos, el ancho y el corte son los mismos por cable que por radio.

**CRITERIO DE ACEPTACIÓN**

1. `bluetoothctl info MAC` muestra `Paired: yes` y `Trusted: yes`.
2. `python3 -m ruleta diagnostico` termina con **cero** `[!!]` y **código 0**.
3. **Papel en la mano** con `probar-impresora`.
4. El acta explica **por qué** se descartó el USB.

**SI FALLA**

- **La impresora no aparece en la búsqueda:** apagarla y encenderla (algunas
  dejan de anunciarse a los pocos minutos), acercarla, y comprobar que ningún
  celular esté conectado a ella.
- **No aparece `Serial Port` en `bluetoothctl info`:** la unidad podría ser
  **solo BLE**, y entonces **ni USB ni Bluetooth clásico sirven** con este
  programa. **Detenerse y preguntar**: esa decisión (otra impresora, u otro
  desarrollo) no es del ejecutor.
- **`rechazó la conexión` (ECONNREFUSED):** canal equivocado (el diagnóstico lo
  busca solo) u otro dispositivo conectado a la impresora.
- **El emparejamiento no toma ninguno de los dos PIN:** la página de autoprueba
  del Paso 2 trae el PIN real. Si es otro, **lo teclea el usuario** siguiendo
  las instrucciones que el propio script imprime al fallar (`bluetoothctl`,
  `agent on`, `pair`, `trust`), en su propia terminal.

---

### Paso 11 · Sincronizar el `config.json` final al repositorio

**QUIÉN:** ejecutor de la cadena (edita en la PC) + agente de commit (commitea)
+ agente (despliega y verifica). **El ejecutor no commitea** (§8, prohibición 7).

**POR QUÉ NO SE PUEDE SALTAR:** hasta aquí, la configuración buena vive **solo**
en la Pi. Si se queda así, el primer `git pull` de la Fase 3 la pisa sin avisar
y el evento arranca con `tipo: bluetooth` y la MAC de relleno.

**QUÉ HACER — en este orden exacto**

1. **Traer el archivo de la Pi como evidencia** (a la carpeta temporal de la
   sesión, **no** al repositorio). En los dos comandos siguientes,
   `<scratchpad>` es un **marcador**: se sustituye por la carpeta temporal que
   el ejecutor tenga asignada en esa sesión. **Lo que no puede es caer dentro de
   `~/ruleta` ni dentro del repositorio de la PC** (§5, trampa 13):

   ```bash
   /c/Windows/System32/OpenSSH/scp.exe ruleta:ruleta/config.json "<scratchpad>/config-pi.json"
   ```

2. **Aplicar los valores medidos al `config.json` DEL REPOSITORIO, a mano y
   conservando el formato original.** Solo las llaves que cambiaron: `tipo`, la
   nueva `ruta`, y las que el Paso 8 haya tocado. **No** se copia el archivo de
   la Pi encima del del repositorio: se copian los **valores**, para que el
   commit tenga un diff de tres o cuatro líneas y no del archivo entero.

3. **Comprobar que los dos archivos dicen lo mismo** (comparación por igualdad
   del documento completo, no «se parecen»). **Este bloque corre en la PC, no en
   la Pi, y en esta PC el intérprete se llama `python`, no `python3`:** medido en
   Git Bash, `python3` es el atajo de la Microsoft Store y contesta `Python was
   not found; run without arguments to install from the Microsoft Store...` sin
   ejecutar nada, mientras que `python` es `C:/Python314/python` (Python 3.14.4):

```bash
python - <<"PY"
import json
a = json.load(open("config.json", encoding="utf-8"))
b = json.load(open("<scratchpad>/config-pi.json", encoding="utf-8"))
print("IGUALES" if a == b else "DISTINTOS")
for k in sorted(set(a) | set(b)):
    if a.get(k) != b.get(k):
        print("difiere:", k, "->", a.get(k), "|", b.get(k))
PY
```

   Tiene que imprimir **`IGUALES`** y nada más. Si imprime `difiere: ...`, el
   punto 2 quedó incompleto: corregirlo y repetir.

4. **Pasar por la cadena**: lentes en paralelo → correctivo → escéptico →
   **agente de commit** con la lista de rutas acordada por adelantado (§8,
   prohibición 8: nunca `git add .`) → push → **verificador de push**
   independiente.

5. **Guardar una copia de seguridad en la Pi y solo entonces desplegar.** El
   `git checkout --` de la línea siguiente **descarta** la copia local de la Pi:
   se hace **después** de que el commit esté publicado y verificado, nunca
   antes.

   ```bash
   ssh ruleta 'cp ~/ruleta/config.json ~/config.json.medido-fase2'
   ssh ruleta 'cd ~/ruleta && git checkout -- config.json && git pull --ff-only'
   ```

6. **Verificar que la Pi y el repositorio son idénticos, byte a byte:**

   ```bash
   ssh ruleta 'cd ~/ruleta && sha256sum config.json'
   sha256sum config.json
   ssh ruleta 'cd ~/ruleta && git status --porcelain | wc -l'
   ```

**CRITERIO DE ACEPTACIÓN**

| Comprobación | Resultado esperado |
|---|---|
| comparación JSON del punto 3 | `IGUALES` |
| `sha256sum config.json` en la Pi y en la PC | **el mismo hash** |
| `git status --porcelain \| wc -l` en la Pi | `0` |
| el comando de resumen del Paso 5 | los mismos valores finales del Paso 8 |
| `python3 -m ruleta diagnostico` en la Pi | 0 `[!!]`, código 0 |

**SI FALLA**

- **`git pull --ff-only` responde que las ramas divergen:** alguien commiteó
  otra cosa en medio. **Detenerse y preguntar**; no hacer `merge` ni `rebase` en
  la Pi.
- **Los hashes no coinciden** aunque el JSON sea igual: hay una diferencia de
  formato (un espacio, una línea en blanco, el salto de línea final). Verlo con
  `diff` entre la copia de la Pi y la del repositorio, y **corregir en el
  repositorio**, por la cadena. **Nunca** se parchea la Pi para que cuadre: la
  fuente de verdad es el repositorio.
- **Se perdió la configuración de la Pi por un `checkout` prematuro:** están las
  copias `~/config.json.medido-fase2` y `~/config.json.antes-de-fase2`. Y, en el
  peor caso, las fotos del papel dicen qué valores eran.

---

### Paso 12 · Sub-fase 2b · Cambios de código, con goldens

**QUIÉN:** la cadena completa, un pase por cambio (o un pase con los cuatro, lo
decide el orquestador): ejecutor con goldens → dos lentes en paralelo →
correctivo → escéptico → agente de commit → deploy observado → verificador en
vivo → extractor y escriba.

**QUIÉN NO:** el ejecutor que está probando la impresora (decisión D9). Mientras
se experimenta **no se toca código**: se anota qué haría falta y se hace aquí.

**Reglas para los goldens de esta sub-fase** (`CLAUDE.md` §5): ejecutan
funciones puras con vectores reales, **comparan por igualdad y no por
presencia**, anclan **cuerpos enteros** en vez de líneas sueltas, **derivan
censos** en lugar de enumerar a mano, y cada golden nuevo se prueba con **al
menos seis mutaciones por copia, todas en rojo**.

---

#### (a) La regla `udev` de la impresora dentro de `instalar.sh`

> **HECHO el 2026-09-11; desplegado y verificado en la Pi esa misma noche.** Es el paso nuevo `5/7 Impresora
> USB` de `instalar.sh`, con la regla, `usermod -aG lp` y la recarga de `udev`;
> el `SupplementaryGroups=gpio lp` del punto 4 también entró. Con dos
> diferencias respecto a lo que se lee abajo: el archivo se llama
> `61-ruleta-impresora-usb.rules` y el enlace `/dev/ruleta-impresora` (los que
> ya funcionan en la Pi), y los goldens están en `tests/test_instalacion.py`, no
> en `tests/test_instalador.py`. El punto 3 (`/etc/modules-load.d`) no aplicó:
> `usblp` cargó solo.

**QUÉ.** Que una reinstalación desde cero deje la impresora funcionando sin que
nadie recuerde el Paso 4. Se añade a `instalar.sh`:

1. en el bloque `== 2/6 Grupos del usuario` (líneas 36-38 hoy), un
   `usermod -aG lp "${USUARIO}"` protegido con `getent group lp`, igual que el
   que ya existe para `bluetooth`;
2. un bloque nuevo que escriba
   `/etc/udev/rules.d/61-ruleta-impresora.rules` con **la regla exacta que
   funcionó en el Paso 4** (con el VID:PID medido) y haga
   `udevadm control --reload` + `udevadm trigger`;
3. **solo si el Paso 3 acabó en la rama B1**, el
   `/etc/modules-load.d/ruleta-usblp.conf` con `usblp`;
4. **solo si se quedó la ruta del grupo** (y no `MODE="0666"`),
   `SupplementaryGroups=gpio lp` en `ruleta.service` (hoy, línea 13, dice
   `SupplementaryGroups=gpio`).

**POR QUÉ.** Sin esto, el `instalar.sh` que se corra el día que haya que
reinstalar deja una Pi que no imprime, y el motivo (una regla `udev` que alguien
escribió a mano un jueves) no está en ninguna parte del repositorio.

**GOLDENS** (archivo nuevo `tests/test_instalador.py`; leen los archivos del
repositorio, no ejecutan nada):

- `test_regla_udev_impresora_exacta`: extrae el bloque entre
  `cat > /etc/udev/rules.d/61-ruleta-impresora.rules <<'EOF'` y el `EOF`
  siguiente, y lo compara **entero** con el texto esperado (`assertEqual` de
  cuerpo completo, no `assertIn`).
- `test_reglas_udev_declaradas`: **deriva** el conjunto de archivos de reglas que
  el instalador escribe (una expresión regular sobre
  `/etc/udev/rules.d/[^ ]+`) y lo compara por igualdad con
  `{"60-ruleta-rp1-gpiochip4.rules", "61-ruleta-impresora.rules"}`.
- `test_grupos_que_agrega_el_instalador`: **deriva** el conjunto de
  `usermod -aG <grupo>` y lo compara por igualdad con
  `{"gpio", "bluetooth", "lp"}`.
- `test_grupos_del_servicio` (solo si aplica el punto 4): compara la línea
  `SupplementaryGroups=` de `ruleta.service` con `gpio lp`.

**Mutaciones que deben poner los goldens en rojo** (mínimo seis): cambiar un
dígito del VID; cambiar el PID; `MODE="0660"` → `MODE="0666"`; `GROUP="lp"` →
`GROUP="plugdev"`; borrar el `SYMLINK+=`; renombrar el archivo a
`62-...rules`; borrar el `usermod -aG lp`; dejar `SupplementaryGroups=gpio`.

**CRITERIO DE ACEPTACIÓN.** Los goldens pasan; `sudo ./instalar.sh` se vuelve a
correr en la Pi **sin romper nada** (es idempotente) y, tras correrlo, el Paso 4
sigue cumpliendo todos sus criterios.

**OJO, y no es opcional:** `instalar.sh` hace `systemctl enable ruleta.service`
(hoy, línea 67; y `systemctl restart` si el servicio estuviera activo), así que
**después de correrlo el servicio queda `enabled` otra vez**. Si el Paso 13
todavía no se ha hecho, eso contradice la decisión **D6** y la **prohibición 1**,
y con el `config.json` ya apuntando a la impresora **un corte de luz arrancaría
el servicio solo y gastaría papel**. Hay que devolverlo al estado del Paso 1 y
comprobarlo:

```bash
ssh ruleta 'sudo systemctl disable ruleta'
ssh ruleta 'systemctl is-enabled ruleta'   # disabled
```

---

#### (b) Consulta del papel (`DLE EOT`) en `ImpresoraArchivo`

> **HECHO el 2026-09-11; desplegado y verificado en la Pi esa misma noche.** La condición previa se cumple:
> la interfaz es **bidireccional** (protocolo 02, §0-bis H9). `crear_impresora`
> ya le pasa `consultar_estado` al tipo `archivo`; la consulta se hace solo si
> la ruta es un dispositivo de caracteres; el modo de apertura pasa a `r+b`
> **solo** en ese caso; la lectura tiene límite de tiempo con `select`; y la
> interpretación de los bits vive en `escpos.verificar_estado`, compartida con
> el Bluetooth. Goldens en `tests/test_escpos.py`
> (`TestImpresoraArchivoUSB`), con los nombres en español que usa el archivo.

**QUÉ.** Que por USB el programa pregunte «¿tienes papel? ¿estás en línea?»
antes de mandar el boleto, como ya hace por Bluetooth, **respetando la llave
`consultar_estado`**.

**POR QUÉ.** Hoy no lo hace (§0-bis H5): si el rollo se acaba a media semana, el
premio se descuenta y el boleto no sale. El PPD del fabricante confirma que la
impresora entiende `DLE EOT 1` (§0-bis H3).

**CONDICIÓN PREVIA MEDIBLE.** Solo tiene sentido si la interfaz es
**bidireccional** (`protocolo=02` en la medición del Paso 3). **Si es `01`
(unidireccional), este cambio NO se hace**: en su lugar se documenta, en el
`README` y en la capacitación, que **por USB el programa no puede saber si hay
papel**, y se deja `consultar_estado` sin efecto para `tipo: archivo`.

**CÓMO, sin romper lo que ya funciona** (esto no es opcional, es el contrato):

- `crear_impresora` (`ruleta/app.py`, línea 56) le pasa `consultar_estado` a
  `ImpresoraArchivo`, igual que ya hace con `ImpresoraBluetooth`.
- La consulta se intenta **solo** cuando la ruta es un **dispositivo de
  caracteres**. Con un archivo normal (`salida_impresora.bin`, las pruebas) el
  comportamiento actual **no cambia en nada**, incluido `anexar`.
- El modo de apertura de hoy es `"ab"`, que no permite leer. Para el
  dispositivo hay que abrir en lectura/escritura; **el modo `"ab"` se conserva
  para el resto de los casos**.
- La lectura debe tener **límite de tiempo** (`select` con el mismo
  `timeout_estado` de 1 s). Una lectura sin límite sobre `usblp` puede colgar el
  servicio para siempre: eso sería mucho peor que la falla que se intenta
  arreglar.
- **La política es idéntica a la del Bluetooth y no se cambia**: si la impresora
  **no contesta**, se imprime igual («no responder no es prueba de falla»). Solo
  se aborta con `ErrorConexion` si contesta y dice «sin papel» o «fuera de
  línea».
- La interpretación de los bits (máscara `0x93` / valor `0x12`, `0x60` sin
  papel, `0x0C` poco papel, `0x08` fuera de línea) **se comparte** con
  `ImpresoraBluetooth` en una función común; no se copian los números en dos
  sitios.

**GOLDENS** (en `tests/test_escpos.py`, con un doble de dispositivo que anota lo
escrito y cuenta las lecturas):

| Prueba | Respuesta simulada | Se espera (igualdad exacta) |
|---|---|---|
| `test_archivo_sin_papel_no_envia` | `0x72` | `ErrorConexion` y lo escrito == `b"\x10\x04\x04"` (solo la pregunta) |
| `test_archivo_con_papel_escribe_todo` | `0x12`, `0x12` | escrito == `CMD_ESTADO_PAPEL + CMD_ESTADO_IMPRESORA + datos` |
| `test_archivo_fuera_de_linea_no_envia` | `0x12`, `0x1a` | `ErrorConexion` y escrito == las dos preguntas, **sin** los datos |
| `test_archivo_poco_papel_solo_avisa` | `0x16`, `0x12` | imprime igual; escrito termina en `datos` |
| `test_archivo_sin_respuesta_imprime_igual` | nada / expira | escrito == `preguntas + datos` |
| `test_archivo_byte_invalido_se_ignora` | `0x00` ×4 | se descartan y se imprime igual |
| `test_archivo_consultar_estado_false` | — | `lecturas == 0` y escrito == `datos` |
| `test_archivo_normal_no_pregunta` | archivo temporal real | `lecturas == 0`, y `test_anexa_o_trunca` sigue verde |

**Mutaciones obligatorias** (mínimo seis, todas en rojo): invertir la máscara
`0x60`; quitar la validación de bits fijos; preguntar **después** de escribir;
ignorar `consultar_estado`; tratar «no contesta» como fallo; abrir con `"ab"` y
perder la lectura; tratar `0x0C` (poco papel) como error fatal; quitar el
límite de tiempo de la lectura.

---

#### (c) `diagnostico`: que también revise el tipo `archivo`, y versiones reales

> **HECHO el 2026-09-11; desplegado y verificado en la Pi esa misma noche.** Tres funciones puras en
> `ruleta/__main__.py` —`revisar_ruta_impresora`, `version_modulo` e
> `interpretar_estado_papel`— y `cmd_diagnostico` solo las llama e imprime. El
> diagnóstico además **consulta el papel** cuando la ruta es un dispositivo y el
> servicio no está corriendo. Goldens (tuplas completas, por igualdad) en
> `tests/test_instalacion.py`. Consecuencia para la §7.5: los `[ok]` de la
> **salida** dejan de ser 6 y pasan a **8 con papel de sobra**, **7 más un
> `[??]`** si la impresora avisa de poco papel o no contesta, y **7 más un
> `[--]`** con el servicio corriendo. Lo **medido en la Pi** el 2026-09-11 fue
> **7 `[ok]` y un `[??]` de poco papel** (fichas F-140, F-178 y F-186).

**QUÉ.** Dos cosas pequeñas en el mismo cambio:

1. Con `tipo: archivo`, que el diagnóstico **mire la ruta**: que exista, que sea
   un dispositivo y que se pueda escribir. Hoy sale por la puerta de atrás con
   `[--] ... no se prueba Bluetooth` y devuelve 0 sin abrir nada: decisión D7.
   *(Esto describe el estado ANTERIOR a 2b. Hoy ese texto ya no existe para el
   tipo `archivo`: `grep -n "no se prueba Bluetooth" ruleta/__main__.py` no
   devuelve nada.)*
2. Que `[ok] gpiozero` y `[ok] lgpio` muestren su versión real, con
   `importlib.metadata`, en vez de salir vacías (ficha F-051).

**POR QUÉ.** Porque el comando que el personal va a correr cuando algo falle
(`python3 -m ruleta diagnostico`, es el que dice el README §9) hoy **no detecta
la falla más probable del evento**: el cable suelto o el permiso perdido.

**CÓMO.** Dos funciones **puras** (fáciles de probar), y `cmd_diagnostico` solo
las llama e imprime:

```python
def revisar_ruta_impresora(ruta, stat_fn=os.stat, access_fn=os.access) -> tuple[bool, str]
def version_modulo(nombre: str) -> str
```

**GOLDENS** (comparación por igualdad de la tupla completa que devuelve la
función, no de un trozo del mensaje):

| Caso | Resultado esperado |
|---|---|
| la ruta no existe | `(False, "  [!!] ...")` con el texto exacto que se acuerde |
| dispositivo de caracteres y se puede escribir | `(True, "  [ok] ...")` |
| dispositivo de caracteres sin permiso de escritura | `(False, "  [!!] ...")` que **mencione la regla udev y el grupo lp** |
| archivo normal (p. ej. `salida_impresora.bin`) | `(True, "  [??] ...")`: aviso, **no** error: es legítimo para pruebas |
| `version_modulo` con metadatos simulados | la cadena exacta de la versión |

**CONSECUENCIA QUE HAY QUE ESCRIBIR EN EL ACTA:** este cambio **rompe a
propósito** un golden de la Fase 1. Su §7 dice
`diagnostico | grep -c "\[ok\]"` → **6**; al añadir la comprobación de la ruta
pasará a **7**. No es una regresión: es el golden el que se actualiza, y el
cambio queda anotado en el acta de esta fase y en la §6 (mapa de anclas).

---

#### (d) `README.md`: el USB de primera clase y las correcciones pendientes

> **HECHO el 2026-09-11 y desplegado, con el visto bueno explícito del
> usuario** (requisito de la decisión D12). Conteos medidos después de la
> reescritura: `scp -r` → 0, `America/Mexico_City` → 0, `usuario@ruleta.local`
> → 0, `comandos lo detectan` → 0, `/dev/usb/lp0` → 4 (ahora es el nodo real que
> hay detrás del nombre fijo) y `/dev/ruleta-impresora` → 5.

**QUÉ.** Una sola pasada al README que arregle, a la vez:

| Dónde | Qué dice hoy | Qué debe decir | Ficha |
|---|---|---|---|
| §4 paso 1 (líneas 84-93) | `scp -r "Ruleta Asadero" usuario@ruleta.local:~/ruleta` | `git clone`, usuario `asadero` | F-001, F-002 |
| §3 (líneas 69-78) | «activa SSH», `ssh usuario@ruleta.local` | autenticación **solo por llave** y usuario `asadero` | F-002 |
| §4 pasos 3-4 | emparejar Bluetooth primero | **USB primero**: cable, `tipo: archivo`, `ruta`, regla `udev`, grupo `lp`; Bluetooth como respaldo | F-052 |
| §4 paso 7 (línea 153) | `set-timezone America/Mexico_City` | `America/Hermosillo` | F-053 |
| §5 (líneas 222-225) | «Los comandos lo detectan y te lo recuerdan» | **falso para `probar-impresora`**, que no comprueba el servicio | F-089 |
| §6 tabla, fila `ruta` (línea 255) | «p. ej. `/dev/usb/lp0` si algún día va por USB» | es **el camino normal**, con su valor real | F-088 |
| §9 (línea 429) | «usa el cable USB … (agrega tu usuario al grupo `lp`)» | la regla `udev` real y el grupo, ya medidos | F-052, F-088 |
| §6, `consultar_estado` | «antes de cada boleto pregunta si hay papel» | decir **si eso vale por USB** según cómo acabe (b) | H5 |

**POR QUÉ.** Porque el README es lo que va a leer el usuario a las once de la
noche cuando algo no imprima, y hoy le manda por el camino equivocado.

**REQUISITO PREVIO, SIN EXCEPCIÓN:** **visto bueno explícito del usuario**
(decisión D12). Si no lo da, este punto **no se hace** y las fichas siguen
abiertas; así se anota en el acta.

**GOLDENS** (comparación por igualdad sobre conteos):

```bash
grep -c "scp -r" README.md                 # 0
grep -c "America/Mexico_City" README.md    # 0
grep -c "usuario@ruleta.local" README.md   # 0
grep -c "comandos lo detectan" README.md    # 0   (hoy da 1: la frase esta partida entre las lineas 224 y 225, asi que con la cadena larga "Los comandos lo detectan" el conteo ya vale 0 sin haber corregido nada)
```

y un conteo positivo, cuyo número exacto fija el ejecutor de 2b y comprueba el
revisor: `grep -c "/dev/usb/lp0" README.md`.

---

### Paso 13 · Arranque del servicio y verificación en vivo

**QUIÉN:** agente (lanza y mide) + usuario (recoge el boleto).
**REQUISITO:** el Paso 7 salió bien (papel en la mano) y el `config.json` de la
Pi ya tiene la configuración final.

**POR QUÉ SE HACE AQUÍ Y NO EN LA FASE 4** (decisión D11): es la única prueba de
que **el servicio**, que corre como `asadero` lanzado por systemd —no como la
persona que está dentro del SSH—, puede abrir el dispositivo e imprimir.

**POR QUÉ ES SEGURO HACERLO SIN BOTONES CABLEADOS:** `config.json` trae
`modo_habilitar: "mantener"`, así que **sin el botón HABILITAR presionado no se
juega nada**. Con los pines al aire y `pull_up: true`, gpiozero los lee como
«no presionado». El servicio arranca, imprime el inventario y se queda
esperando. No sortea, no gasta folios y no toca el inventario.

**QUÉ HACER**

```bash
ssh ruleta 'sudo systemctl enable ruleta'
ssh ruleta 'sudo systemctl start ruleta'
ssh ruleta 'sleep 8; systemctl is-active ruleta'
ssh ruleta 'journalctl -u ruleta -n 40 --no-pager'
```

*(`journalctl` funciona sin `sudo` porque `asadero` está en el grupo `adm`.)*

En el log deben aparecer, en este orden:

```
Ruleta v1.0.0 | impresora=archivo | datos=/home/asadero/ruleta/datos
Ruleta arrancando. Premios: test1, test2, test3, test4, test5, test6, test7
GPIO listo: jugar=17 habilitar=27 led=22
Inventario impreso (arranque). Folio actual 00000
Lista. Esperando jugadas.
```

**Y el boleto de inventario tiene que salir por la impresora**, con los siete
premios de prueba y sus probabilidades.

**Medir los grupos que systemd le dio de verdad al servicio** (la pregunta que
quedó abierta en el Paso 4):

```bash
ssh ruleta 'systemctl show -p MainPID --value ruleta'
ssh ruleta 'grep -E "^(Uid|Gid|Groups):" /proc/$(systemctl show -p MainPID --value ruleta)/status'
ssh ruleta 'getent group lp'
```

El número de grupo de `lp` (tercer campo de `getent group lp`) **debería**
aparecer en la línea `Groups:`. Se anote lo que se anote, **queda medido**, que
es lo que hacía falta.

**Al terminar, devolver el servicio al estado en que lo dejó la Fase 1:**

> **SUPERADO POR DECISIÓN DEL ORQUESTADOR (2026-09-11, ~23:20).** Este bloque y
> su fila del criterio de aceptación (`enabled` + `inactive`) **ya no aplican**:
> tras la reprueba post-2b y la confirmación del usuario se decidió que **el
> kiosco queda corriendo por USB**, con el servicio **`active` y `enabled`**.
> **No se ejecuta este `stop`.** El texto se conserva porque es lo que este plan
> pedía cuando se escribió. Ficha **F-185**, cerrada; ver la nota «Reprueba
> post-2b y cierre en papel» de la §0. **Lo que sí sigue en pie:** antes de
> apagar la Pi para cablear los botones de la Fase 3, `sudo systemctl stop
> ruleta` **y** `sudo systemctl disable ruleta`.

```bash
ssh ruleta 'sudo systemctl stop ruleta'
ssh ruleta 'systemctl is-enabled ruleta; systemctl is-active ruleta || true'
```

**CRITERIO DE ACEPTACIÓN**

| Comprobación | Resultado esperado |
|---|---|
| `systemctl is-active ruleta` (con el servicio arriba) | `active` |
| `journalctl -u ruleta -n 60 --no-pager \| grep -c "Lista. Esperando jugadas."` | `1` |
| `journalctl -u ruleta -n 60 --no-pager \| grep -c "Inventario impreso (arranque)"` | `1` |
| `journalctl -u ruleta -n 60 --no-pager \| grep -c "No se pudo imprimir el inventario"` | `0` |
| **El boleto de inventario** | **en la mano, legible, cortado** (foto para el acta) |
| al cerrar: `systemctl is-enabled ruleta` / `is-active` | **SUPERADO el 2026-09-11:** el plan pedía `enabled` / `inactive`; por decisión del orquestador queda `enabled` / **`active`**, con el kiosco corriendo (ficha **F-185**) |

**AVISO PARA LA FASE 3, que hay que escribir en el acta:** el servicio queda
**habilitado**, así que **cualquier reinicio o corte de luz lo arranca solo**.
Antes de apagar la Pi para cablear los botones: `sudo systemctl disable ruleta`,
y al volver, `sudo systemctl enable ruleta` (es la misma receta del Paso 12 del
plan de la Fase 1).

**SI FALLA**

- **En el log: `no se pudo abrir /dev/usb/lp0: [Errno 13] Permission denied`.**
  El servicio no tiene el grupo, aunque `asadero` por SSH sí lo tenga. Salida
  inmediata **ya decidida** (D4): cambiar `MODE="0660"` por `MODE="0666"` en
  `/etc/udev/rules.d/61-ruleta-impresora.rules`, recargar
  (`sudo udevadm control --reload && sudo udevadm trigger --subsystem-match=usbmisc`),
  reiniciar el servicio y volver a verificar. **Anotarlo en el acta** y llevarlo
  al punto (a) de 2b. La salida limpia (`SupplementaryGroups=gpio lp`) es un
  cambio de código y va por la cadena, no aquí.
- **`No se pudo imprimir el inventario (arranque)` tres veces y luego
  `Lista. Esperando jugadas.`:** el servicio arranca igual, pero **no imprimió**.
  El mensaje de error dice el motivo. No se da el paso por bueno sin papel.
- **El servicio muere antes de imprimir, con un error de `gpiozero` / `lgpio` /
  `gpiochip`:** es un problema de la **Fase 3** que aparece antes de tiempo.
  Anotarlo, **no parchear**, y demostrar el camino de impresión por el otro
  lado: `sudo systemctl stop ruleta` y
  `cd ~/ruleta && python3 -m ruleta reporte --imprimir` (ese sí comprueba que el
  servicio esté parado antes de imprimir).
- **El servicio entra en bucle de reinicio** (`activating` una y otra vez):
  `journalctl -u ruleta -n 100 --no-pager`. Si es `ERROR de configuración`
  (código 2), el `config.json` quedó mal en el Paso 8 o el Paso 11.
- **Sale el boleto pero con los premios `TEST 1`…`TEST 7`:** **es lo correcto en
  esta fase.** Los premios reales son la Fase 4.

---

### Paso 14 · Cierre de fase

**QUIÉN:** agente ejecutor. **PROHIBIDO:** commitear (eso es del agente de
commit, §8 prohibición 7).

**QUÉ HACER**

1. **Escribir el acta** en `docs/actas/<AAAA-MM-DD>-fase-2.md` —con la fecha del
   día en que de verdad se ejecutó; si es el 2026-09-12, entonces
   `docs/actas/2026-09-12-fase-2.md`—, **desde el archivo de hechos medidos de
   la sesión, nunca de memoria** (`CLAUDE.md` §6). Debe contener, como mínimo:
   - la salida real, pegada, de **cada golden de la §7**, o la marca **«no
     medido»** si no se corrió (nunca inventado);
   - el **VID:PID** medido, el `ieee1284_id` completo y el protocolo de la
     interfaz (`01` o `02`);
   - el **contenido exacto** del archivo `/etc/udev/rules.d/61-ruleta-impresora.rules`
     que quedó en la Pi, y si se usó `MODE="0660"` o `MODE="0666"`;
   - los **valores finales** de la sección `impresora` de `config.json`;
   - **qué dijo el papel** en cada vuelta del Paso 8 (con fotos), incluida la
     tabla de acentos elegida y por qué;
   - la línea `Groups:` del proceso del servicio (Paso 13);
   - si se usó el camino USB o el respaldo Bluetooth, y **por qué**;
   - qué pasos se saltaron y con qué justificación;
   - **toda desviación respecto a este plan**, en una sección propia, con el
     mismo espíritu que la §0-bis del plan de la Fase 1: qué decía el plan, qué
     pasó de verdad, y qué consecuencia tiene para la Fase 3.
2. **Marcar las casillas de la §0** de este plan, con fecha y evidencia.
3. **Corregir en este plan, en su sitio, lo que haya resultado falso**, dejando
   escrito que se corrigió y por qué (como hizo la Fase 1).
4. **Anotar en `docs/fichas.md`** todo hallazgo residual que no justificara
   detener la fase.
5. **Actualizar la memoria del proyecto**: cómo quedó conectada la impresora,
   los valores de la impresora, si hizo falta la regla `udev` o `0666`, y qué
   queda pendiente de 2b.

**CRITERIO DE ACEPTACIÓN**

- El acta existe y cada golden de la §7 aparece con su salida real o marcado
  como no medido.
- Todas las casillas de la §0 están marcadas, o justificadas por escrito.
- Las fotos del papel están guardadas.

**SI FALLA**

- Si falta la salida de algún golden, **no se inventa**: se vuelve a correr el
  comando contra la Pi y se pega lo que salga. Si ya no se puede (la Pi está
  apagada o sin red), se escribe **«no medido»**.

---

## 5. Trampas del entorno y del repositorio

Cosas que un ejecutor sin contexto **no puede adivinar**. Todas están medidas
contra el código o contra la Pi; cada una dice dónde comprobarla.

1. **ANTES de la sub-fase 2b el diagnóstico NO probaba la impresora cuando
   `tipo` es `archivo`.** `cmd_diagnostico` imprimía
   `[--] impresora tipo 'archivo': no se prueba Bluetooth` y **devolvía 0 sin
   abrir la ruta**: salía verde con el cable desconectado, con la impresora
   apagada y con `Permission denied`. **Con 2b ya en el repositorio eso cambió**:
   el diagnóstico revisa la ruta (que exista, que sea dispositivo, que se pueda
   escribir) y, si el servicio está parado y `consultar_estado` está activo,
   pregunta por el papel; esa salida temprana ya no existe para `archivo`. Aun
   así el criterio de esta fase sigue siendo **papel en la mano** (decisión D7):
   el diagnóstico no demuestra que el boleto salga legible. Por Bluetooth es
   igual que siempre: ahí el diagnóstico sí conecta de verdad. La nota de 2b en
   la §0, el Paso 12 (c) y la §7.5 lo detallan: los `[ok]` del diagnóstico pasan
   de 6 a 8.

2. **`probar-impresora` es el ÚNICO comando que imprime y NO avisa si el
   servicio está corriendo.** `servicio_activo()` se llama en
   `reporte --imprimir`, `liberar`, `reiniciar` y `diagnostico` (desde 2b, dos
   veces dentro del diagnóstico: una en la rama del tipo `archivo` y otra en la
   del Bluetooth) — **y no en `cmd_probar_impresora`**. El `README.md` §5 ya
   **no** dice «los comandos lo detectan y te lo recuerdan»: la sub-fase 2b lo
   corrigió y ahora nombra los tres que sí avisan y advierte de que
   `probar-impresora` no lo hace (ficha F-089, resuelta a medias: falta la parte
   de código). Por eso el Paso 1 detiene el servicio a mano y el Paso 7 lo
   vuelve a comprobar.

3. **El servicio quedó `enabled` desde la Fase 1 y arranca solo en cada
   encendido.** `ruleta.service` trae `WantedBy=multi-user.target`,
   `Restart=always` y `StartLimitIntervalSec=0`. Hoy muere con código 2 cada
   3 segundos porque la MAC es la de relleno (`crear_impresora`, `ruleta/app.py`
   línea 46). **En cuanto `config.json` sea correcto, ese arranque automático
   imprime el inventario y gasta papel sin que nadie lo pida.** Se deshabilita
   en el Paso 1 y se rehabilita en el Paso 13.

4. **`ImpresoraArchivo` puede abrir con modo `"ab"`, que incluye `O_CREAT`: en
   ese caso puede CREAR un archivo donde debería estar el dispositivo.**
   (`ruleta/escpos.py`, líneas 671-673: desde 2b el modo es `"r+b"` —que **no**
   crea nada— cuando toca preguntar por el papel, y sigue siendo
   `"ab"`/`"wb"` en los demás casos, entre ellos **la impresora con
   `consultar_estado: false`**.) Como `asadero` no puede escribir en `/dev` ni en `/dev/usb`, el
   intento falla con `Permission denied`, **que es lo deseable**. Pero **con
   `sudo` sí lo crearía**: quedaría un archivo normal llamado `/dev/usb/lp0` que
   **se traga los boletos sin dar error** y que además impide que el nodo real
   aparezca. Por eso: **jamás `sudo python3 -m ruleta ...`** (§8, prohibición
   3). Se detecta con `test -c /dev/usb/lp0` y se arregla con
   `sudo rm -f /dev/usb/lp0` y reconectando el cable. Ficha **F-090**.

5. **La `ruta` se resuelve contra el directorio actual del proceso, no contra
   `config.json`.** Y su valor por defecto es `salida_impresora.bin`
   (`ruleta/config.py`, línea 57). Si `ruta` queda mal escrita o relativa,
   **todo «funciona», el código de salida es 0 y no sale papel**: el boleto está
   en un archivo dentro de `~/ruleta`. Usar **siempre** la ruta absoluta.

6. **Lo esperado es que `/dev/usb/lp0` sea `root:lp` con permisos `0660`** (es
   la regla por defecto de Debian para `SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*"`),
   **y así se midió la noche del 2026-09-11**: `/dev/usb/lp0` existe como
   `crw-rw---- root:lp` 180,0 (§0-bis H2 y H9). El Paso 3 lo vuelve a medir y se
   detiene si difiere. En la **Fase 1** se midió que `asadero` **NO estaba en el
   grupo `lp`** (sí en `lpadmin`, que sirve para administrar CUPS y **no** da
   acceso al dispositivo); ficha **F-052**. Esa parte **ya se resolvió a mano** la
   noche del 2026-09-11 (`getent group lp` → `lp:x:7:asadero`, §0-bis H9), y el
   Paso 4 la deja hecha de forma reproducible.

7. **El PATH de una sesión SSH no interactiva no incluye `/usr/sbin` ni
   `/sbin`.** `usermod`, `modprobe` y `rfkill` dan `command not found` aunque
   estén instalados. Se llaman por ruta absoluta (`/usr/sbin/usermod`) o detrás
   de `sudo`, que arma su propio PATH. Un ejecutor que lea «command not found»
   como «falta el paquete» instalará cosas que ya están (Fase 1, §0-bis D7).

8. **`dmesg` puede no dejarse leer por un usuario normal.** Se usa siempre
   `sudo dmesg`, que en esta Pi no pide contraseña.

9. **CUPS puede quitarle el dispositivo a `usblp` y hacer desaparecer
   `/dev/usb/lp0`.** Su backend USB desprende el driver del kernel. Pista de que
   puede estar instalado: `asadero` pertenece a `lpadmin`. Si estorba:
   `sudo systemctl disable --now cups cups-browsed`. Esta Pi **no imprime por
   CUPS**: manda ESC/POS directo al dispositivo.

10. **`herramientas/emparejar.sh` reescribe `config.json` entero y lo deja en
    `tipo: bluetooth`.** Líneas 124-136: carga el JSON, pone `impresora.mac` y
    **`impresora.tipo = "bluetooth"`**, y lo vuelca con `json.dump(indent=2)`,
    **reformateando todo el archivo** (los premios pasan de una línea cada uno a
    varias). Consecuencia: si se corre el respaldo Bluetooth **después** de
    haber configurado el USB, el `tipo` se pierde y el diff del Paso 11 se
    vuelve ilegible. Por eso el Paso 10 hace copia antes.

11. **`emparejar.sh` sin argumento es interactivo.** Línea 55: `read -rp
    "Escribe la MAC..."`. Lanzado por SSH no interactivo lee EOF y muere con
    `MAC inválida: ''`, un error que **parece** de la impresora y no lo es
    (ficha F-078). Se le pasa siempre la MAC como argumento.

12. **`git pull --ff-only` en la Pi puede fallar por dos cambios de MODO, no de
    contenido.** El Paso 8 de la Fase 1 hizo `chmod +x` sobre `instalar.sh` y
    `herramientas/emparejar.sh` contra un índice que los tenía en `100644`; el
    commit `601c4c2` ya los publica en `100755`. Solución medida:
    `git checkout -- instalar.sh herramientas/emparejar.sh` y después el `pull`;
    alternativa, `git -c core.fileMode=false pull --ff-only`.

13. **Los respaldos se guardan en `~`, NUNCA dentro de `~/ruleta`.** Un
    `config.json.bak` dentro del repositorio aparece como `?? ` en
    `git status --porcelain` y **rompe el criterio de «árbol limpio»** del Paso
    11.

14. **El número del nodo puede cambiar.** Si se desconecta y reconecta la
    impresora mientras algo mantiene abierto el nodo anterior, el kernel puede
    crear `/dev/usb/lp1`. Por eso la regla del Paso 4 añade
    `SYMLINK+="impresora-ruleta"`: si algún día `lp0` deja de ser el bueno, se
    cambia `ruta` a `/dev/impresora-ruleta` y se acabó. **Mientras `lp0`
    funcione, `config.json` apunta a `/dev/usb/lp0`**, que es lo que dice el
    README y lo que menos sorprende.

15. **Por USB no hay reintentos ni control de ritmo.** `ImpresoraArchivo`
    escribe de una vez: `reintentos`, `espera_reintento_seg`, `tamano_bloque`,
    `pausa_bloque_seg`, `pausa_inicial_seg`, `pausa_final_seg` y
    `bytes_por_segundo` **solo aplican al Bluetooth** (§0-bis H6, ficha F-091).
    Cambiarlas «para que imprima mejor» por cable no hace absolutamente nada.

16. **Por USB no hay consulta de papel** hasta que se haga el cambio (b) de 2b
    (§0-bis H5). Si el rollo se acaba, el premio se descuenta igual. Mientras
    tanto, la red de seguridad es la del `README` §5 punto 8: cotejar
    `datos/boletos.csv` y devolver el premio con `python3 -m ruleta liberar`.

17. **Los acentos tienen dos causas de fallo distintas y se arreglan distinto.**
    Si salen **ideogramas chinos**, es el modo Kanji: el programa ya manda
    `FS .` (`cancelar_modo_chino: true`, `ruleta/escpos.py` línea 34), y si aun
    así pasa, queda el **DIP 4** de la impresora. Si salen **símbolos raros pero
    latinos**, es la **tabla**: `codepage_n` + `codepage`, que se cambian
    **siempre en pareja** (Paso 8). Aviso de la investigación: el número **16**
    no es CP1252 en todos los firmwares de esta familia; **19 = PC858** es la
    apuesta consistente.

18. **El corte `auto` no es «cortar»: es `GS V 66 0`** (`ruleta/escpos.py`,
    línea 43), que le dice a la impresora «avanza hasta tu cuchilla y corta».
    Por eso con `auto` el valor por defecto de `lineas_antes_corte` es **1**, y
    con `parcial` o `completo` es **5** (`lineas_antes_corte_por_defecto`, línea
    67): en esos modos el papel **no** avanza solo y el texto se queda dentro.
    En esta familia el corte siempre deja una pestaña sin cortar: **es normal**,
    no es un cortador defectuoso.

19. **Dos redes con el mismo nombre.** El punto de acceso del Paso 0 se llama
    igual que el Wi-Fi del asadero: eso es lo que lo hace funcionar. Pero si
    alguien lo deja encendido **dentro** del restaurante, la Pi puede engancharse
    a la PC en vez de al router. **Al volver al asadero, apagar el punto de
    acceso.**

20. **La PC es la red.** Si se suspende, se cierra la tapa o se apaga el Wi-Fi,
    **la Pi se queda sin red a media prueba** y el SSH se corta. No es una
    avería de la Pi: se vuelve a encender el punto de acceso y se reintenta.
    Además, **Windows exige contraseñas de 8 caracteres o más** para su punto de
    acceso: si la del asadero es más corta, ese camino no existe (Paso 0, rama
    C).

21. **`python3 -m ruleta` solo funciona desde `~/ruleta`**, y sin
    `PYTHONIOENCODING=utf-8` los acentos de la consola se rompen (Fase 1, §5
    trampas 3 y 6). Las dos cosas juntas explican el 90 % de los «no funciona»
    que en realidad sí funcionan.

22. **Ni `probar-impresora` ni `vista-previa` tocan el inventario.** No
    consumen folios, no descuentan premios y no escriben en `estado.json`
    (`cmd_probar_impresora` ni siquiera lo abre; `cmd_vista_previa` solo lo lee
    para enseñar el número que vendría). **No hace falta correr `reiniciar`
    después de probar**, y de hecho está prohibido (§8, prohibición 2).

23. **Cada `probar-impresora` gasta unos 30 cm de papel** (cuatro líneas de
    acentos, la regla, cuatro tamaños, el logo y el corte). Tres vueltas de
    ajuste son casi un metro. Tener rollo de sobra evita quedarse a medias con
    la impresora abierta.

---

## 6. Mapa de anclas que derivan

Textos del repositorio de los que depende este plan, con la línea donde estaban
**el 2026-09-11**. **Re-grep antes de cada edición**: si el texto ya no está
donde dice esta tabla, **detenerse y preguntar**, porque significa que alguien
cambió el repositorio y el plan quedó viejo.

> **Tabla refrescada el 2026-09-11 contra el commit
> `61adf9676b1072115c5fd64e6a28f6bef5454a54`** (el que está desplegado en la
> Pi). Las líneas de antes eran las de antes de la sub-fase 2b y **todas las de
> abajo se volvieron a medir con `grep -n`**: esto cierra el censo de la ficha
> **F-166** y las fichas **F-148**, **F-149** y **F-151**. Donde 2b hizo
> desaparecer un texto, la fila lo dice en vez de dejar un número que ya no
> existe.

| Ancla | Cómo encontrarla | Por qué deriva |
|---|---|---|
| Clase `ImpresoraArchivo` completa | `grep -n "class ImpresoraArchivo" ruleta/escpos.py` → **603** (era 546) | De su cuerpo salen §0-bis H5 y H6, la trampa 4 (los modos de apertura) y el cambio (b) de 2b, ya implementado |
| Construcción del transporte por USB | `grep -n 'tipo == "archivo"' -A 3 ruleta/app.py` → **56-59** | **Corregido tras 2b:** hoy dice `anexar=True` **y sí pasa** `consultar_estado=imp.consultar_estado` (ficha F-148) |
| Salida temprana del diagnóstico | `grep -n "no se prueba Bluetooth" ruleta/__main__.py` → **el `grep` ya no devuelve nada** | 2b la borró para el tipo `archivo`. Fue el origen de la decisión D7 y de lo que arregla (c); si volviera a aparecer, alguien deshizo 2b (ficha F-149) |
| Conteo de líneas `[ok]` | `grep -c "\[ok\]" ruleta/__main__.py` → **8** en el **código** (eran 6) | Ojo: son las del código, no las de la salida. En la **salida** del diagnóstico se midió **7 `[ok]` + un `[??]`** en la Pi (§7.5, cuatro casos). El golden de la **Fase 1** sigue diciendo 6 y hay que actualizarlo: ficha **F-140** |
| Comandos que comprueban el servicio | `grep -n "servicio_activo" ruleta/__main__.py` → 90 (definición), 214, 230, 269, 417, 464 | Deriva la trampa 2: son **cinco** usos —`reporte --imprimir`, `liberar`, `reiniciar` y **dos** dentro de `diagnostico` (rama `archivo` y rama Bluetooth)— y `probar-impresora` no está entre ellos |
| Bytes y bits del estado en tiempo real | `grep -n "CMD_ESTADO_PAPEL\|CMD_ESTADO_IMPRESORA\|_MASCARA_FIJA_ESTADO\|BITS_SIN_PAPEL" ruleta/escpos.py` → **58-60 y 64-66** (constantes), **104**, **118-125** y **661-662** (usos) | Son los valores exactos de los goldens de (b): `0x93`/`0x12`, `0x60`, `0x0C`, `0x08`. Desde 2b los tres últimos tienen nombre (`BITS_SIN_PAPEL`, `BITS_POCO_PAPEL`, `BIT_FUERA_DE_LINEA`) y los comparte `ruleta/__main__.py` (351-355) |
| Tabla de códecs | `grep -n "CODECS_TABLA" ruleta/escpos.py ruleta/ticket.py` → **54** en `escpos.py` (era 50) y **15/229** en `ticket.py` | De ahí sale la tabla de parejas `codepage_n` ↔ `codepage` del Paso 8. Si alguien añade una tabla, el boleto de prueba cambia |
| Bytes del corte y su defecto | `grep -n "CMD_CORTE_AVANCE" ruleta/escpos.py` → **47** (era 43) y `grep -n "def lineas_antes_corte_por_defecto" -A 3 ruleta/escpos.py` → **77** (era 67) | Explican por qué `auto` es 1 línea y los demás 5 (trampa 18) |
| Llaves válidas de `impresora` | `grep -n "class ConfigImpresora" -A 26 ruleta/config.py` (hoy 53) | `ruta` existe con defecto `salida_impresora.bin`; **una llave desconocida hace fallar el arranque entero** (`_construir` en `config.py`) |
| Validación de la configuración | `grep -n "^def validar" -A 45 ruleta/config.py` (hoy 266) | Qué valores se aceptan: `chars_por_linea >= 32`, `corte` de la lista, `codepage` que Python conozca. Si se pone algo fuera de rango, el programa lo rechaza con un mensaje claro |
| `config.json` de hoy | `grep -n '"tipo"\|"ruta"' config.json` → **16** (`"tipo": "archivo"`) y **19** (`"ruta": "/dev/ruleta-impresora"`) | **La `ruta` ya está puesta, a propósito, desde 2b** (antes había que añadirla, ficha F-077). Que aparezca **no** es motivo para detenerse; lo sería que volviera a decir `"bluetooth"` |
| Censo de premios de prueba | `grep -c '"id": "test' config.json` → **7** | De ahí salen los goldens del Paso 9 (7 boletos de premio, 9 `[CORTE]`) |
| Grupos suplementarios del servicio | `grep -n "SupplementaryGroups" ruleta.service` → **15** (era 13) | **Ya dice `gpio lp`** desde 2b, y `grep -n "RestartPreventExitStatus" ruleta.service` → **27**. Golden por igualdad de la unidad entera en `tests/test_instalacion.py` |
| Dónde va lo nuevo en el instalador | `grep -n "== 2/7" instalar.sh` → **37**; `grep -n "60-ruleta-rp1-gpiochip4" instalar.sh` → **51**; `grep -n "61-ruleta-impresora-usb" instalar.sh` → **65** | Los pasos se renumeraron a `n/7` en 2b: `grep -n "== 2/6"` **ya no devuelve nada**. El bloque de la impresora es el `5/7` |
| `emparejar.sh` reescribe la configuración | `grep -n 'impresora"\]\["tipo"\]' herramientas/emparejar.sh` (hoy 131) | Trampa 10: deja `tipo: bluetooth` y reformatea el archivo |
| `emparejar.sh` es interactivo | `grep -n "read -rp" herramientas/emparejar.sh` (hoy 55) | Ficha F-078: por SSH no interactivo hay que pasarle la MAC |
| Rechazo de la MAC de relleno | `grep -n 'strip("0")' ruleta/app.py` (hoy 46) | Explica por qué hoy el servicio muere con código 2 en bucle (§0-bis H8) |
| Mensajes del log del arranque | `grep -n "Lista. Esperando jugadas.\|Inventario impreso" ruleta/app.py` → **117** y **270** (eran 115 y 268) | Son literalmente los goldens del Paso 13, y los dos salieron en el journal del 2026-09-11 a las 22:32:48 |
| Menciones de `/dev/usb/lp0` en el README | `grep -n "/dev/usb/lp0" README.md` → **128, 304, 514 y 518** (eran 255 y 429) | Ya no son un error que corregir (ficha F-088, resuelta): ahora nombran el **nodo real** que hay detrás de `/dev/ruleta-impresora` |
| Afirmación del README §5 sobre el servicio | `grep -c "comandos lo detectan" README.md` → **0** | 2b la quitó: el §5 ya nombra los tres comandos que sí avisan y advierte de que `probar-impresora` no (ficha F-089, resuelta en la parte de documentación) |
| Zona horaria en el README | `grep -c "America/Mexico_City" README.md` → **0**; `grep -c "America/Hermosillo" README.md` → **2** (líneas 82 y 182) | Corregido en 2b (ficha F-053, resuelta) |
| Convenciones del repositorio | `grep -n "^## Convenciones de este repo" -A 12 CLAUDE.md` | Define `docs/planes/`, `docs/actas/<AAAA-MM-DD>-<fase>.md` y `docs/fichas.md`: las rutas que usa este plan |
| Deploy y estado de la Fase 1 | `grep -n "^## 9. Siguientes fases" -A 30 docs/planes/fase-1-preparar-pi.md` y su §0-bis | De ahí vienen el orden USB→Bluetooth y los pendientes que esta fase hereda. **El commit `601c4c2` que cita ya no manda:** la Pi venía de `2052e47` (nunca llegó a clonar el de cierre de la Fase 1) y desde el deploy de 2b está en `61adf96` (fichas F-098 y F-127) |

---

## 7. Criterios de aceptación de la fase y goldens

La fase está cerrada cuando **todos** estos comandos, corridos desde la PC en
Git Bash (con el `ssh` nativo de Windows), devuelven **exactamente** la salida
indicada —comparación **por igualdad**, no «parecido»— y cuando los **goldens
de papel** están cumplidos y fotografiados. Todos se pegan, con su salida real,
en el acta del Paso 14.

> **Estado de estos goldens el 2026-09-11, después del deploy de 2b.** El acta
> (`docs/actas/2026-09-11-fase-2.md`, §3) los recorre uno por uno con su salida
> real. Resumen: se midieron los de red y acceso, los del repositorio y las
> pruebas (7.1, 7.2, 7.12), el grupo `lp`, la regla `udev` y el enlace (7.3), la
> configuración (7.4), el diagnóstico entero (7.5) y el arranque del servicio
> (7.8). **Quedaron sin medir tres del 7.3** —`ls /etc/udev/rules.d/ | grep -c
> impresora`, el `stat` del nodo y el `ieee1284_id`, todos medidos a mano
> aquella noche pero no vueltos a comprobar tras el deploy— y **los grupos del
> proceso del Paso 13**. Ficha **F-187**.

### 7.1 Red y acceso

```bash
ssh ruleta 'hostname'
# ruleta

ssh ruleta 'ip -4 -o addr show scope global | grep -c "192\.168\.137\."'
# 1
# (si Windows repartió otro rango, se sustituye por el real y se anota; ver Paso 0)
```

### 7.2 Estado del programa y del repositorio

```bash
ssh ruleta 'cd ~/ruleta && git status --porcelain | wc -l'
# 0

ssh ruleta 'cd ~/ruleta && python3 -m unittest discover -s tests -t . 2>&1 | tail -n 1'
# OK

ssh ruleta 'cd ~/ruleta && sha256sum config.json'
sha256sum config.json
# el MISMO hash en las dos (después del Paso 11)
```

### 7.3 El dispositivo USB y sus permisos

```bash
ssh ruleta 'test -c /dev/usb/lp0 && echo NODO_OK'
# NODO_OK

ssh ruleta 'test -c /dev/ruleta-impresora && echo ENLACE_OK'
# ENLACE_OK
# (nombre corregido por la sub-fase 2b: es el que ya existe en la Pi y el que
#  escribe instalar.sh; ver la nota de 2b en la §0)

ssh ruleta 'stat -c "%a %U %G" /dev/usb/lp0'
# 660 root lp
# (666 root lp SOLO si se aplicó la salida de emergencia de la decisión D4;
#  en ese caso se anota en el acta como desviación aceptada, no como fallo)

ssh ruleta 'test -w /dev/usb/lp0 && echo ESCRIBIBLE'
# ESCRIBIBLE

ssh ruleta 'id -nG | tr " " "\n" | grep -cx lp'
# 1

ssh ruleta 'grep -c idVendor /etc/udev/rules.d/61-ruleta-impresora-usb.rules'
# 1
# (0 SOLO si se usó la regla de emergencia sin VID:PID; se anota)

ssh ruleta 'ls /etc/udev/rules.d/ | grep -c impresora'
# 1
# (dos archivos de impresora serían dos reglas compitiendo: si sale 2, sobra la
#  vieja 61-ruleta-impresora.rules de un intento anterior y hay que borrarla)

ssh ruleta 'cat /sys/class/usbmisc/lp0/device/ieee1284_id'
# Evidencia, no igualdad: se pega TAL CUAL salga.
# Medido el 2026-09-11: MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1
# (NO trae el MDL:ZJ-80250 del PPD del fabricante; ver §0-bis H9 y el Paso 3)
```

### 7.4 La configuración

```bash
ssh ruleta 'cd ~/ruleta && python3 -c "import json;i=json.load(open(\"config.json\"))[\"impresora\"];print(i[\"tipo\"],i[\"ruta\"],i[\"beep\"])"'
# archivo /dev/ruleta-impresora True
# (corregido por la sub-fase 2b: es lo que trae el config.json del repositorio,
#  que es el que quedará en la Pi tras el git pull)
```

### 7.5 El diagnóstico

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico >/dev/null 2>&1; echo $?'
# 0

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "\[!!\]"'
# 0

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "\[ok\]"'
# 7      <-- MEDIDO en la Pi el 2026-09-11 después del deploy de 2b.
#
# El conteo depende del estado real de la impresora y del servicio; son cuatro
# casos y ninguno es un fallo. Antes de 2b siempre eran 6.
#   8  impresora conectada, con papel de sobra y contestando, servicio parado.
#   7  + [??] poco papel  <-- ESTE es el caso medido: la impresora contestó y
#      dijo que le queda poco rollo (7 [ok] y un [??], código 0).
#   7  + [??] no contestó al estado (firmware que no responde a DLE EOT).
#   7  + [--] el servicio 'ruleta' está corriendo: el diagnóstico no le pregunta
#      nada a la impresora para no interferir. Es el caso más probable DURANTE
#      el evento (fichas F-140, F-178 y F-186).

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "no se prueba Bluetooth"'
# 1      <-- 0 DESPUÉS del cambio (c) de la sub-fase 2b: esa salida temprana ya
#            no existe para tipo 'archivo'

# Solo DESPUÉS de la sub-fase 2b (antes esta línea no existe):
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "impresora conectada en /dev/ruleta-impresora"'
# 1
```

> **Recordatorio, porque este es el error más fácil de cometer:** ANTES de la
> sub-fase 2b estos goldens **no dicen nada sobre la impresora** (decisión D7):
> salen igual con el cable desconectado. DESPUÉS de 2b sí lo dicen —el
> diagnóstico abre la ruta y pregunta por el papel—, pero el criterio de la fase
> sigue siendo el mismo: **papel en la mano**.

### 7.6 La impresión

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta probar-impresora >/dev/null 2>&1; echo $?'
# 0
```

### 7.7 La vista previa (sin gastar papel)

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta vista-previa --todos | grep -c "=== Boleto de premio:"'
# 7      <-- derivado de la lista 'premios' de config.json; si cambia, cambia

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta vista-previa --todos | grep -c "\[CORTE\]"'
# 9      <-- 7 premios + 1 consuelo + 1 inventario
```

### 7.8 El servicio en vivo (Paso 13, con el servicio arriba)

```bash
ssh ruleta 'systemctl is-active ruleta'
# active

ssh ruleta 'journalctl -u ruleta -n 60 --no-pager | grep -c "impresora=archivo"'
# 1

ssh ruleta 'journalctl -u ruleta -n 60 --no-pager | grep -c "Inventario impreso (arranque)"'
# 1

ssh ruleta 'journalctl -u ruleta -n 60 --no-pager | grep -c "Lista. Esperando jugadas."'
# 1

ssh ruleta 'journalctl -u ruleta -n 60 --no-pager | grep -c "No se pudo imprimir el inventario"'
# 0
```

### 7.9 El estado en que se deja la Pi (al cerrar la fase)

> **SUPERADO POR DECISIÓN (2026-09-11, ~23:20).** Este golden pedía dejar la Pi
> como la dejó la Fase 1. **Ya no:** el kiosco **queda corriendo por USB**, así
> que lo que se espera hoy es `enabled` / **`active`** / **`running`**, que es
> justo lo que midió el verificador en vivo (con `NRestarts=0`). Se conserva el
> texto original de abajo por historia. Ficha **F-185**, cerrada.

```bash
ssh ruleta 'systemctl is-enabled ruleta'
# enabled

ssh ruleta 'systemctl is-active ruleta || true'
# inactive
# SUPERADO: hoy dice 'active', y es lo correcto (decision del 2026-09-11).

ssh ruleta 'systemctl show -p SubState --value ruleta'
# dead
# SUPERADO: hoy dice 'running'.
```

### 7.10 Goldens de papel (no hay comando que los sustituya)

| # | Qué | Cómo se comprueba |
|---|---|---|
| **P1** | **Boleto de prueba** completo, legible, con logo, con las líneas de acentos perfectas y **cortado** | está en la mano, y hay **foto** en el acta. **CUMPLIDO:** foto de las 19:25 con el código anterior a 2b, y **confirmación del usuario el 2026-09-11 ~23:20** con el código desplegado, ya con las cuatro tablas **en dos renglones, sin partirse** (el texto decía «**una** línea de acentos»: eran cuatro, y 2b las partió en dos renglones cada una) |
| **P2** | **Boleto de inventario del arranque** del servicio, con los siete premios de prueba | está en la mano, y hay **foto** en el acta. **CUMPLIDO:** foto de las 19:22 y confirmación del usuario del arranque posterior al deploy (~23:20) |
| **P3** | **Página de autoprueba** de la impresora, con los DIP y el ancho anotados | está guardada, y hay **foto** en el acta. **Única excepción:** si la autoprueba no sale con la combinación del Paso 2, manda su SI FALLA («no bloquea la fase»): P3 se da por cumplido escribiendo **«sin autoprueba»** en el acta y anotando el ancho y el DIP 5 deducidos del papel del Paso 7 |

**Los goldens de papel mandan sobre los de consola.** Si `codigo=0` y no hay
papel, la fase **no** está cerrada (decisión D7).

### 7.11 Si se acabó usando el respaldo Bluetooth (Paso 10)

Las secciones 7.3 y 7.4 no aplican, y en su lugar valen:

```bash
ssh ruleta 'bluetoothctl info AA:BB:CC:DD:EE:FF | grep -c "Paired: yes"'
# 1

ssh ruleta 'bluetoothctl info AA:BB:CC:DD:EE:FF | grep -c "Trusted: yes"'
# 1

ssh ruleta 'cd ~/ruleta && python3 -c "import json;i=json.load(open(\"config.json\"))[\"impresora\"];print(i[\"tipo\"],i[\"mac\"],i[\"canal\"])"'
# bluetooth AA:BB:CC:DD:EE:FF 1

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "la impresora acepta conexiones"'
# 1
```

y el golden 7.8 de `impresora=archivo` pasa a ser `impresora=bluetooth`.

### 7.12 Goldens de la sub-fase 2b (si se ejecuta)

```bash
# Estos dos corren en la PC (no llevan ssh). En esta PC el interprete se llama
# python: python3 es el atajo de la Microsoft Store y contesta
# "Python was not found" sin ejecutar nada.
python -m unittest discover -s tests -t . 2>&1 | tail -n 1
# OK

python -m unittest tests.test_instalacion -v 2>&1 | tail -n 1
# OK
# (el archivo se llama tests/test_instalacion.py, no test_instalador.py: lo fijó
#  así el brief de 2b, que además metió ahí los goldens del servicio y de los
#  códigos de salida)

python -m unittest discover -s tests -t . 2>&1 | tail -n 3
# Ran 194 tests
# OK
```

Además, **cada golden nuevo de 2b se prueba con al menos seis mutaciones por
copia, y todas deben quedar en rojo** (`CLAUDE.md` §5). Las mutaciones concretas
están listadas en el Paso 12, cambio por cambio. Un golden que sobrevive a su
mutación no es un golden: es decoración.

---

## 8. Prohibiciones

Valen para toda la fase. Se repiten aunque ya estén en el plan de la Fase 1
porque esta es la fase donde más tienta saltárselas.

1. **No se arranca el servicio `ruleta` hasta el Paso 13**, y solo cuando
   `probar-impresora` haya salido bien **y** `config.json` tenga la conexión
   final. Antes de eso, el servicio se queda **detenido y deshabilitado**
   (decisión D6).
2. **No se corre `python3 -m ruleta reiniciar` ni `liberar` durante la fase.**
   Poner el inventario en cero es de la **Fase 4**, y las pruebas de esta fase
   **no** consumen folios (§5, trampa 22). Única excepción, en el **paso de
   cierre**: si el arranque del Paso 13 dejó algún boleto en estado `incierto`
   (se cortó a media impresión), se puede correr `liberar FOLIO` **con el
   servicio detenido** y anotándolo en el acta.
3. **Nunca `sudo` delante de `python3 -m ruleta`.** Crea archivos de root en
   `datos/` que luego el servicio no puede escribir, y en el peor caso crea un
   archivo normal donde debería estar el dispositivo (§5, trampa 4).
4. **Ningún agente teclea contraseñas ni PIN.** Ni la del Wi-Fi (la escribe el
   usuario en su PC), ni la de `asadero`, ni el PIN de la impresora (lo maneja
   `bt-agent` leyéndolo de un archivo que crea el propio `emparejar.sh`). Si un
   paso las pide, se marca **«requiere al usuario»**.
5. **No se toca `/boot/firmware/config.txt`.** La batería RTC es el Paso 12 de
   la Fase 1 y necesita visto bueno explícito del usuario.
6. **No se edita `config.json` en la PC y en la Pi al mismo tiempo.** Hasta el
   Paso 11 la única copia viva es la de la Pi; a partir del Paso 11, la del
   repositorio (decisión D5).
7. **El ejecutor no commitea.** Eso es del agente de commit, con la lista de
   rutas acordada por adelantado.
8. **Nunca `git add .` ni `git add -A`.** Solo rutas explícitas.
9. **No se instalan paquetes nuevos** (`pyusb`, `python-escpos`, CUPS, el driver
   del fabricante) **sin visto bueno del usuario**. Esta fase no los necesita
   (decisión D10). Y **nada de `pip install`**: Raspberry Pi OS lo rechaza fuera
   de un entorno virtual, y este proyecto se instala solo con `apt`.
10. **Nunca `apt full-upgrade` ni `apt dist-upgrade`.** Puede cambiar el kernel y
    romper GPIO, Bluetooth o `usblp` a media semana de evento.
11. **Nunca se borra `~/.ssh/known_hosts` entero.** Si hace falta, `ssh-keygen -R
    <host>`.
12. **No se ejecuta el driver del fabricante en la Pi.** Sus binarios son x86 y
    la Pi es `aarch64` (§0-bis H4). Instalarlo solo puede romper cosas.
13. **No se cambia la regla `udev` a `MODE="0666"` «por si acaso».** Solo si la
    medición del Paso 13 lo exige, y anotándolo en el acta (decisión D4).
14. **No se apaga la impresora ni se desconecta el cable USB entre los Pasos 3 y
    8.** El nodo puede cambiar de número y las mediciones dejan de valer (§5,
    trampa 14).
15. **No se cambia el nombre del repositorio** ni se «corrige» su URL: se llama
    `Ruelta-Aleatoria-Pi5` y así se usa.
16. **No se toca el `README.md` sin visto bueno explícito del usuario**
    (decisión D12). Va entero en el punto (d) de 2b o no va.
17. **No se parchea a mano lo que un script deja a medias.** Se vuelve a correr
    el script completo, que para eso es repetible.
18. **No se deja el punto de acceso de Windows encendido dentro del asadero**
    (§5, trampa 19), ni se planifica el evento contando con él: en producción la
    Pi va **sin red**.

---

## 9. Siguientes fases

### Lo que esta fase entrega a la siguiente

- La impresora **funcionando por cable**, con sus valores medidos y
  commiteados, y el servicio demostrado en vivo.
- La Pi con el servicio **`enabled` y `active`**: **el kiosco queda corriendo
  por USB**, por decisión del orquestador del 2026-09-11 ~23:20. *(Esta línea
  decía «`enabled` e `inactive`, el mismo estado que dejó la Fase 1»; la
  decisión la superó, igual que al final del Paso 13 y al golden §7.9. Ficha
  **F-185**, cerrada.)* **Consecuencia que la Fase 3 tiene que respetar:** con
  el servicio arriba, cualquier pulsación de un botón —cuando se cableen—
  gastaría papel y folio, y un apagón lo vuelve a arrancar solo. Antes de apagar
  la Pi para cablear: `sudo systemctl stop ruleta` **y**
  `sudo systemctl disable ruleta`; al terminar, `sudo systemctl enable ruleta`.
- Un camino de red reproducible para trabajar **desde cualquier sitio** (Paso 0).

### Lo que esta fase deja pendiente, y no hay que olvidar

| Pendiente | Dónde está escrito | Cuándo se resuelve |
|---|---|---|
| **Batería RTC ML-2020** (la Pi irá **sin red**, así que sin ella los boletos salen con fecha equivocada tras un apagón) | Fase 1, Paso 12 y §0-bis D9 | **Antes del evento**; es el principal riesgo abierto del proyecto |
| **Sub-fase 2b** | §4, Paso 12 de este plan | **Hecha, commiteada (`61adf96`), desplegada y verificada en vivo** el 2026-09-11 |
| **Aviso de «sin papel» por USB** | §0-bis H5 y cambio (b) | **Implementado y funcionando en hardware real:** el 2026-09-11 la impresora contestó `DLE EOT` por USB y el servicio avisó de **poco papel** antes de imprimir. Falta el caso extremo, con el rollo fuera (ficha F-091) |
| **README corregido** | cambio (d) y fichas F-001, F-002, F-003, F-052, F-053, F-088, F-089 | **Hecho el 2026-09-11** con el visto bueno del usuario; F-089 queda abierta a medias (falta la parte de código) y quedan tres fichas nuevas de README: F-153, F-167 y F-177 |
| **Golden `[ok]` = 6 de la Fase 1** | §6, mapa de anclas, y fichas F-140, F-178 y F-186 | Con 2b la **salida** del diagnóstico da **7 `[ok]` + un `[??]`** (medido en la Pi), y hasta 8 con papel de sobra. **Resuelto el 2026-09-11 ~23:20:** el plan de la **Fase 1** (§7 y §6) y su acta llevan ya una **nota fechada** que dice que desde `61adf96` son **8** con la impresora conectada y respondiendo (**7** si no responde), **sin borrar el `6` histórico** (fichas F-140 y F-186, cerradas) |
| **Devolver el servicio a `enabled` + `inactive`** | Paso 13, final, §7.9 y ficha F-185 | **SUPERADO POR DECISIÓN el 2026-09-11 ~23:20:** el kiosco **se queda corriendo** (`active` y `enabled`). Ficha F-185, cerrada. Lo que queda para la Fase 3 es el `stop` + `disable` **antes de apagar la Pi para cablear** |
| **Volver a correr `probar-impresora` después de 2b** | Paso 7 y ficha F-188 | **HECHO el 2026-09-11 ~23:20**, confirmado en papel por el usuario: acentos en dos renglones sin partirse y un pitido por boleto. Ficha F-188, cerrada |
| **Cambiar el rollo de papel** | ficha F-190 | Antes del evento: la impresora lleva avisando de poco papel desde el 2026-09-11 |

### Fase 3 · Botones y LED

Se cablea el botón **JUGAR** a GPIO 17, el botón **HABILITAR** del mesero a
GPIO 27 y el LED opcional a GPIO 22, todos contra GND (`README` §2). Primero se
prueba la lógica **sin hardware**, con
`python3 -m ruleta --simular --impresora vista` (teclas `h`, `j`, `i`), y solo
después con los botones reales. Aquí se ajustan `rebote_ms`, `modo_habilitar` y
`pulsacion_larga_seg`.

**Tres avisos que salen de esta fase y que la Fase 3 debe respetar:**

1. **Antes de apagar la Pi para cablear**, `sudo systemctl stop ruleta` y
   `sudo systemctl disable ruleta`; al volver a encenderla,
   `sudo systemctl enable ruleta`. Si no, systemd la arranca sola a media faena
   (§0-bis H8). **Hoy hace falta hacer las dos cosas**: la Fase 2 dejó el
   servicio `enabled` **y `active`**, y eso ya no es un descuido sino una
   decisión —el kiosco se queda corriendo por USB— (ficha F-185, cerrada).
2. **Ahora la impresora sí imprime**: cada pulsación de prueba con el servicio
   arriba **gasta papel y consume un folio**. Para probar los botones sin gastar
   nada, `--impresora vista` (los boletos salen por la consola).
3. Los folios que se consuman probando se limpian en la **Fase 4** con
   `reiniciar --si`, no antes.

### Fase 4 · Prueba general y entrega

Se cambian los `test1`…`test7` por los **premios reales** con sus pesos, stocks
y topes diarios; se pone el **logo definitivo**; se instala la **batería RTC** y
se fija la hora; se corre `python3 -m ruleta reiniciar --si` para dejar folio e
inventario en cero; se arranca el servicio (`sudo systemctl start ruleta`, que a
partir de ahí arranca solo al encender) y se hace una prueba completa de punta a
punta. Se **aísla la Pi de la red** (se apaga el punto de acceso y se deja sin
Wi-Fi para el evento). Se cierra con la **capacitación del personal**: encender,
leer el inventario impreso, qué hacer si no sale un boleto, cómo liberar un
folio y **qué avisa y qué no avisa el programa cuando se acaba el papel**: con
2b sí pregunta por USB antes de cada boleto y, si la impresora contesta que no
hay papel, **no descuenta el premio**; pero si el firmware no contestara, el
folio se gasta igual y hay que cotejarlo a mano (README §5, punto 8).

---

## 10. Regla final

**Si el código real, el `README.md` o la propia Raspberry Pi contradicen este
plan, el ejecutor se detiene y pregunta; no improvisa.**
