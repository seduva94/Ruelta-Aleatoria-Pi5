# Fase 1 · Preparar la Raspberry Pi

Plan prescriptivo. Redactado el 2026-09-11. Estado global: **COMPLETADA Y
VERIFICADA el 2026-09-11** en los pasos 1 a 11 y 14. **Faltan el Paso 12 y el
Paso 13:** el 13 (idioma del sistema) sí es opcional, pero el **Paso 12, la
batería RTC, dejó de ser opcional** el 2026-09-11, cuando el usuario decidió que
en producción la Pi va **sin red** (§0-bis D9): es el **principal riesgo
abierto** de esta fase.

Acta de la ejecución, con la evidencia cruda:
`docs/actas/2026-09-11-fase-1.md`. Lo que se hizo distinto de lo escrito aquí
está en la **§0-bis**, y ahí se explica por qué. **Quien lea este plan para
ejecutar la Fase 2 lee primero la §0-bis**: varias afirmaciones del texto
original resultaron falsas al medirlas y ya están corregidas en su sitio.

Este documento se escribió para **dos lectores**:

- **El dueño del restaurante** (todo lo físico: comprar, descargar, meter la
  microSD, teclear contraseñas, encender). Sus pasos dicen **QUIÉN: usuario**.
- **Un ejecutor Opus sin contexto** (todo lo que se hace desde la PC por
  terminal o por SSH). Sus pasos dicen **QUIÉN: agente** y traen comandos
  exactos, copiables tal cual.

Cada paso tiene siempre las mismas cuatro partes: **QUIÉN**, **QUÉ hacer**,
**CRITERIO DE ACEPTACIÓN** (cómo se comprueba, sin opinar) y **SI FALLA**
(diagnóstico y salida). Nada se da por hecho hasta que su criterio se cumple.

Convención de comandos: los que empiezan con `ssh ruleta ...` se corren **desde
la PC Windows, en Git Bash**, y usan el alias que se crea en el Paso 3. **Un
agente no invoca el `ssh` de Git Bash: escribe siempre la ruta completa del
cliente nativo de Windows, `/c/Windows/System32/OpenSSH/ssh.exe`, en lugar de
`ssh`** (medido el 2026-09-11: Git Bash monta `C:` con `noacl`, su `ssh` ve la
llave privada como `644` y puede rechazarla con `UNPROTECTED PRIVATE KEY FILE`;
ver §0-bis D8 y §5 trampa 17). En todos los ejemplos de este plan `ssh` se
escribe corto por legibilidad; el agente lo sustituye por esa ruta completa. Un
agente añade siempre `-o BatchMode=yes -o ConnectTimeout=10` para que, si algo
pidiera una contraseña, el comando **falle en vez de quedarse colgado**:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 ruleta 'hostname'
```

En los ejemplos se omiten esas dos opciones para que se lean mejor; el agente
las agrega siempre. El usuario, cuando corra algo él mismo, **no** las usa.

**Tiempo límite de los comandos largos.** Un comando de este plan pasa de dos
minutos: `sudo ./instalar.sh` (Paso 9, de 3 a 10 minutos). La herramienta de
terminal del ejecutor corta a los **2 minutos** por defecto, así que ese comando
**se lanza con un límite explícito de 10 minutos** (`timeout: 600000` en la
herramienta Bash). Sin eso, el corte no es un aviso: deja `apt` a medias (ver
§5, trampa 9).

*(Corregido con lo medido el 2026-09-11: la redacción original decía que
`python3 -m ruleta diagnostico` también tardaba «hasta un par de minutos
probando canales RFCOMM contra una MAC que no existe». **Es falso.** Con la MAC
de relleno `00:00:00:00:00:00` el programa ni siquiera intenta conectarse: la
rechaza antes, en `crear_impresora` (`ruleta/app.py`), y el diagnóstico termina
en segundos. Ver §5, trampa 12, y §0-bis D13. Dejar el límite de 10 minutos en
`instalar.sh` sigue siendo correcto: ese sí tardó.)*

---

## 0. Bitácora

Se marcan `[x]` solo cuando el criterio de aceptación del paso se cumplió, con
la fecha y la evidencia real (salida de comando, nunca de memoria). **Marcadas
el 2026-09-11 desde el archivo de hechos medidos de la sesión**; la salida
cruda completa está en el anexo del acta `docs/actas/2026-09-11-fase-1.md`.

La columna «Quién» dice quién lo hizo **de verdad**, no quién lo iba a hacer.
Cuando dice «verificador», un segundo agente de solo lectura, distinto del que
ejecutó, volvió a medir lo mismo y coincidió.

| Nº | Paso | Quién | Estado | Fecha | Evidencia |
|---|---|---|---|---|---|
| 1 | Instalar Raspberry Pi Imager en la PC | usuario | [x] | 2026-09-11 | Registro de Windows (medido por el orquestador): `Raspberry Pi Imager v2.0.11.1`. No se usó el `ls` del criterio ni hay foto; la prueba de que quedó bien instalado es que el Paso 4 grabó la tarjeta |
| 2 | Generar el par de llaves SSH en la PC | agente ejecutor + verificador | [x] | 2026-09-11 | `ssh-keygen -l -f ~/.ssh/id_ruleta.pub` → `256 SHA256:sOmEM5P6LNzx7c5SOyy33NnxWOj+Qt4/RpPjwCcDSQw ruleta-asadero (ED25519)`. `~/.ssh` **no existía**: se creó desde cero, no se sobrescribió nada |
| 3 | Crear el alias `ruleta` en `~/.ssh/config` | agente ejecutor + verificador | [x] | 2026-09-11 | `ssh -G ruleta` → `hostname ruleta.local`, `user asadero`, `identityfile ~/.ssh/id_ruleta`, `identitiesonly yes`, `connecttimeout 10`, `serveraliveinterval 30`. Exactamente **1** línea `Host ruleta`, **sin** `StrictHostKeyChecking` (ver §0-bis D5) |
| 4 | Grabar la microSD con Imager (hostname, usuario, Wi-Fi, llave pública) | usuario | [x] | 2026-09-11 | Sin foto de "Write Successful" en el archivo de hechos; la evidencia es el resultado: la Pi arrancó como `ruleta`, con el usuario `asadero`, en el Wi-Fi y aceptando la llave. Zona horaria elegida por el usuario: **America/Hermosillo** (no `America/Mexico_City`, ver §0-bis D4). La microSD (unidad `D:`, `bootfs`, Disk 1 `Generic Mass-Storage` USB de 28.9 GB) **traía un Raspberry Pi OS previo**; Imager la borró por completo |
| 5 | Primer arranque de la Pi | usuario | [x] | 2026-09-11 | `ping ruleta.local` → `Reply from fe80::2ecf:67ff:fe17:10d%20: time=1ms`. Sin foto en el archivo de hechos |
| 6 | Entrar por SSH desde la PC | agente ejecutor + verificador | [x] | 2026-09-11 | `/c/Windows/System32/OpenSSH/ssh.exe -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 ruleta hostname` → `Warning: Permanently added 'ruleta.local' (ED25519) to the list of known hosts.` + `ruleta`, `EXIT_CODE=0`. **Al primer intento**, sin variantes, sin contraseña. IP resuelta: `192.168.50.178`. El verificador repitió 7 conexiones separadas, todas sin contraseña |
| 7 | Comprobaciones del sistema en la Pi | agente ejecutor + verificador | [x] | 2026-09-11 | `uname -m`→`aarch64`; `VERSION_CODENAME`→`trixie`; `python3 --version`→`Python 3.13.5`; `whoami`→`asadero`; `id -nG` incluye `sudo gpio i2c spi dialout video input`; `sudo -n true`→**`SUDO_PIDE_CONTRASENA`** (bloqueante, ver fila 7-bis); `rfkill list bluetooth`→`command not found` y `/usr/sbin/rfkill list bluetooth`→`Soft blocked: no` / `Hard blocked: no` (ver §5, trampa 16); `bluetoothctl show`→`Powered: yes`; `df -h /`→`23G` libres de 28G; `throttled=0x0`; temperatura 44.6 °C |
| 7-bis | **Autorizar `sudo` sin contraseña** (paso NO previsto en este plan) | usuario | [x] | 2026-09-11 | `sudo -n true; echo EXIT=$?`→`EXIT=0`; `sudo -n cat /etc/sudoers.d/010_asadero-nopasswd`→`asadero ALL=(ALL) NOPASSWD: ALL`; `sudo -n visudo -c`→`/etc/sudoers.d/010_asadero-nopasswd: parsed OK`; `stat -c "%a %U"`→`440 root`. Lo creó **el usuario**, no un agente (ver §0-bis D2) |
| 8 | Clonar el repositorio en `~/ruleta` y dar permiso de ejecución | agente ejecutor + verificador | [x] | 2026-09-11 | `command -v git`→`GIT_NO_ENCONTRADO`: **git no venía en la imagen** (§0-bis D3), se instaló con `apt-get install -y git python3-pil bluez-tools`→`EXIT=0`; `git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git ~/ruleta`→`EXIT=0`, HEAD `2052e4700c53f274a2b2f28ff0d7df62d519ffa8`, rama `main`; tras el `chmod +x`, `instalar.sh` y `herramientas/emparejar.sh` quedan `-rwxrwxr-x` y el verificador confirma `test -x` en los dos |
| 9 | Correr `sudo ./instalar.sh` | agente ejecutor (ya con `sudo` sin contraseña) | [x] | 2026-09-11 | `instalador_exit=0`; log completo en la Pi: `/home/asadero/instalar.log`, con `== 1/6` … `== 6/6`, `Created symlink /etc/systemd/system/multi-user.target.wants/ruleta.service -> /etc/systemd/system/ruleta.service` y el mensaje literal `Servicio 'ruleta' habilitado (arranca solo al encender). Aun NO se inicio.`; `systemctl is-enabled ruleta`→`enabled`; `systemctl is-active ruleta`→`inactive` |
| 10 | Verificar el programa (diagnóstico, pruebas, servicio) | agente ejecutor + verificador | [x] | 2026-09-11 | `python3 -m unittest discover -s tests -t .`→`Ran 141 tests in 0.238s` + `OK`; `python3 -m ruleta diagnostico`→**6** `[ok]` y **un solo** `[!!]` (el de la MAC de la impresora), `EXIT=1`; unidad con `User=asadero` y `WorkingDirectory=/home/asadero/ruleta`; `/etc/udev/rules.d/60-ruleta-rp1-gpiochip4.rules` presente y `/dev/gpiochip4 -> gpiochip0`; `~/ruleta/datos` con `estado.json` y `ruleta.log`, dueño `asadero:asadero`. **La vista previa NO se corrió** (§0-bis D14) |
| 11 | Hora, zona horaria y NTP | agente ejecutor | [x] | 2026-09-11 | `timedatectl`→`Local time: Fri 2026-09-11 16:03:34 MST`, `Time zone: America/Hermosillo (MST, -0700)`, `System clock synchronized: yes`. **No** se corrieron `timedatectl show -p NTP --value` ni `-p LocalRTC --value`: quedan sin medir (§0-bis D12) |
| 12 | Batería RTC — **ya no es opcional** (requiere visto bueno para tocar `config.txt`) | usuario + agente | [ ] | | **NO REALIZADO.** No hay batería instalada ni línea `rtc_bbat_vchg` en `config.txt`. Deja de ser opcional porque en producción la Pi va **sin red** (§0-bis D9). **Riesgo abierto de la Fase 1** |
| 13 | Idioma del sistema `es_MX.UTF-8` (opcional) | agente | [ ] | | **NO REALIZADO.** La locale no se tocó; el sistema quedó como lo dejó la imagen. No afecta al programa: el servicio ya fuerza `PYTHONIOENCODING=utf-8` y los textos están en español dentro del código (§0-bis D6) |
| 14 | Cierre de fase: acta, fichas y memoria | agente ejecutor + agente de commit | [x] | 2026-09-11 | Acta `docs/actas/2026-09-11-fase-1.md` escrita desde el archivo de hechos medidos; fichas nuevas F-051 a F-054 en `docs/fichas.md`; esta bitácora marcada. El commit y el push los hace el agente de commit, no el ejecutor (§8, prohibición 12) |

---

## 0-bis. Desviaciones y hechos descubiertos en la ejecución

Escrito el **2026-09-11**, al cerrar la fase, desde el archivo de hechos medidos
de la sesión. Cada punto dice **qué decía el plan**, **qué pasó de verdad** y
**qué consecuencia tiene para las fases siguientes**. Nada de aquí viene de
memoria: lo que no se midió, se dice que no se midió.

**D1 · La fase se ejecutó antes de que el plan estuviera commiteado.**
El plan se escribió y se ejecutó **el mismo día, en paralelo**, porque el
usuario estaba frente al hardware en vivo. El orden que manda `CLAUDE.md`
(plan → revisión → commit → ejecución) se rompió a propósito. **Es una
desviación consciente del orquestador, no un descuido**, y la asumió él. Efecto
práctico: cuando el Paso 8 clonó el repositorio, lo que bajó a la Pi fue el
commit `2052e4700c53f274a2b2f28ff0d7df62d519ffa8`, **anterior** al commit
`0464f5aad3e94be158f8eeee9b4c8a232267da14`, que es el que publicó
`docs/planes/fase-1-preparar-pi.md` y `docs/fichas.md`. O sea: la Pi tiene el
programa completo, pero **no** tiene este plan ni las fichas. No es un problema
(el programa no los necesita), pero explica por qué el clon de la Pi se ve "sin
docs" y por qué la lista esperada de `ls ~/ruleta` del Paso 8 no los menciona.
Para la Fase 2: **primero se commitea, después se ejecuta**.

**D2 · La imagen NO traía `sudo` sin contraseña. La regla la creó el usuario.**
El Paso 7 midió `sudo -n true` → `SUDO_PIDE_CONTRASENA`, y `/etc/sudoers.d/`
solo tenía `010_at-export`, `010_dpkg-threads`, `010_global-tty`, `010_proxy` y
`README`: **falta el `010_pi-nopasswd` típico de Raspberry Pi OS**. Eso bloqueaba
todo el Paso 9 (apt, systemctl, `/etc`, udev). **El usuario decidió y tecleó él
mismo** la creación de `/etc/sudoers.d/010_asadero-nopasswd` con
`asadero ALL=(ALL) NOPASSWD: ALL`, modo `440 root`. Ningún agente tecleó su
contraseña; la §8 prohibición 1 se respetó. Verificado con cuatro comprobaciones
(`sudo -n true` → `EXIT=0`, contenido exacto, `visudo -c` → `parsed OK`,
`stat` → `440 root`). **Consecuencia para las fases siguientes:** los agentes ya
pueden correr `sudo` por SSH sin pedir nada; la rama «requiere al usuario» de
los Pasos 9, 11, 12 y 13 **ya no aplica** mientras ese archivo exista. Si algún
día se reinstala la Pi, vuelve a aplicar.

**D3 · `git` NO viene preinstalado en Raspberry Pi OS Lite Trixie.**
Era una duda declarada al escribir el plan. Ya está resuelta y medida:
`command -v git` → `GIT_NO_ENCONTRADO`, `dpkg-query` → `git unknown ok
not-installed`. Se instaló junto con lo que faltaba:
`sudo apt-get install -y git python3-pil bluez-tools` → `EXIT=0`
(`git 1:2.47.3-0+deb13u1`, `python3-pil 11.1.0-5+deb13u4`,
`bluez-tools 2.0~20170911.0.7cb788c-4+b2`; además actualizó 14 paquetes de
`util-linux`). **Sí venían** `bluez`, `python3-gpiozero`, `python3-lgpio` y
`rfkill`. **Consecuencia:** en una reinstalación, el `apt-get install` del Paso 8
**no es opcional**, y como necesita `sudo`, depende de D2.

**D4 · La zona horaria real es `America/Hermosillo`, no `America/Mexico_City`.**
La decisión cerrada 5 y los goldens decían `America/Mexico_City`. **El usuario
eligió `America/Hermosillo` en Imager**, que es la correcta para Sonora, y así
quedó: `Time zone: America/Hermosillo (MST, -0700)`. Sonora **no** cambia de
horario. **Este plan ya está corregido** en la decisión 5, en el Paso 4, en el
Paso 11 y en el golden de la §7. **Consecuencia:** la hora impresa en los
boletos y el corte del "día" de las 6:00 usan `MST (-0700)`; cualquier ejemplo
con `America/Mexico_City` (incluido el `README.md` §4 paso 7) está mal para este
restaurante — queda como ficha **F-053**, pendiente de visto bueno para tocar el
README.

**D5 · `~/.ssh` no existía, y la colisión de `known_hosts` que el Paso 3
anunciaba nunca ocurrió.**
El Paso 2 no "verificó" una llave previa: **la creó desde cero** (no había
`~/.ssh`, ni `id_ruleta`, ni `config`). El bloque `Host ruleta` se escribió
nuevo, con `IdentitiesOnly yes` y `ConnectTimeout 10`, y **sin**
`StrictHostKeyChecking`: por eso `ssh -G ruleta` contesta
`stricthostkeychecking ask`, tal como el plan predijo. La rama manual del Paso 3
**no se usó**: en su lugar, cada conexión llevó la opción en la línea de
comandos (`-o StrictHostKeyChecking=accept-new`), que consigue lo mismo sin
editar el archivo. Y la alarma del Paso 3 sobre "tres huellas ya grabadas para
`ruleta.local`" **no se materializó**: la primera conexión imprimió
`Warning: Permanently added 'ruleta.local' (ED25519) to the list of known
hosts.`, es decir la trató como **nueva**, y funcionó al primer intento. El
archivo de hechos **no registra** que se haya corrido `ssh-keygen -R
ruleta.local`, así que **por qué no chocó queda sin explicar**: ver la duda en el
acta. La advertencia se deja escrita porque volverá a valer si alguna vez se
regraba la microSD (§5, trampa 15).

**D6 · La locale NO se cambió (Paso 13 no hecho).**
El sistema quedó con la locale que trae la imagen. No se corrió
`raspi-config nonint do_change_locale es_MX.UTF-8` ni el camino manual, y
`localectl status` **no se consultó**. No afecta al programa: el servicio ya
fuerza `PYTHONIOENCODING=utf-8` y todos los textos de los boletos están en
español dentro del código. **Consecuencia buena:** como el sistema sigue en
inglés, la trampa 11 de la §5 (comandos traducidos) **no muerde hoy**. Si
alguien hace el Paso 13 después, vuelve a valer.

**D7 · El PATH de una sesión SSH no interactiva NO incluye `/usr/sbin`.**
Medido: `PATH=/usr/local/bin:/usr/bin:/bin:/usr/games`. Por eso
`ssh ruleta 'rfkill list bluetooth'` contestó `rfkill: command not found`
**aunque el paquete `rfkill` sí está instalado**; con
`/usr/sbin/rfkill list bluetooth` funcionó perfecto. **Consecuencia:** cualquier
comando por SSH que llame a `rfkill`, `shutdown`, `reboot`, `iw`, `visudo`,
`usermod`… necesita **ruta absoluta** o exportar el PATH. Ya está recogido como
trampa 16 de la §5, y el golden de `rfkill` de la §7 quedó corregido. `sudo` no
tiene ese problema porque resetea el PATH él mismo.

**D8 · Los agentes usan el `ssh` NATIVO de Windows, no el de Git Bash.**
En esta PC hay dos clientes: `C:/Windows/System32/OpenSSH/ssh.exe`
(OpenSSH_for_Windows 9.5p2) y el de Git Bash (OpenSSH 10.3p1). **Git Bash monta
`C:` con la opción `noacl`**, así que `chmod` es un no-op y la capa POSIX
reporta `id_ruleta` como `644`: el `ssh` de Git Bash **puede rechazar la llave**
con `UNPROTECTED PRIVATE KEY FILE`. A nivel Windows los permisos sí son
correctos (`icacls` muestra solo SYSTEM, Administradores y `DUVA_LAP\seduv`, sin
`Users` ni `Everyone`), y el cliente nativo lee esas ACL. **Regla para todas las
fases:** los comandos SSH de los agentes se lanzan con
`/c/Windows/System32/OpenSSH/ssh.exe`. No se tocó `/etc/fstab` de Git for
Windows: eso es configuración global del entorno y necesita visto bueno del
usuario. Recogido como trampa 17 de la §5.

**D9 · En producción la Pi va SIN red. La batería RTC deja de ser opcional.**
Decisión del usuario, tomada hoy: el SSH con llave y el Wi-Fi son **solo para
instalar y probar**; durante el evento la Pi trabaja aislada. Dos consecuencias
duras:

1. **La batería RTC ML-2020 (Paso 12) pasa de "opcional, recomendado" a
   NECESARIA.** Sin red no hay NTP: tras un corte de luz la Pi arranca con una
   hora inventada y **los boletos salen con fecha equivocada**. El Paso 12 está
   **sin hacer**: es el principal riesgo abierto de esta fase.
2. **Cualquier actualización futura exige volver a conectar la Pi al Wi-Fi.**
   El `git pull` de la decisión 7, un `apt install` o un cambio de premios por
   SSH no funcionan con la Pi aislada. El camino es: reconectar al Wi-Fi →
   actualizar → verificar → volver a aislar. Planearlo **antes** del evento, no
   a media semana.

**D10 · La Pi tomó IP DHCP `192.168.50.178` y `ruleta.local` SÍ resuelve.**
`wlan0`, `/24`, `brd 192.168.50.255`, `dynamic`. mDNS funcionó desde Windows 11
sin ayuda. **Pero la IP es dinámica**: si el router la reasigna, el alias
`ruleta` sigue sirviendo mientras mDNS funcione, y si mDNS falla hay que editar
el `HostName` del bloque `Host ruleta`. Para una semana de evento conviene
**reservar la IP en el router**. Riesgo abierto, menor mientras la Pi esté
aislada (sin red no hay SSH que romper).

**D11 · La microSD ya traía un Raspberry Pi OS previo.**
Medido antes de grabar: unidad `D:`, FAT32, 0.5 GB, etiqueta `bootfs`, sobre
Disk 1 `Generic Mass-Storage` USB de 28.9 GB. Imager la borró por completo, que
es lo que se quería. Se anota porque **no era una tarjeta virgen**: si alguien
esperaba encontrar datos ahí, ya no están.

**D12 · El Paso 11 se midió con `timedatectl` a secas, no con los cuatro
`show -p ... --value`.**
Lo que hay medido es el bloque completo: `Local time: Fri 2026-09-11 16:03:34
MST`, `Time zone: America/Hermosillo (MST, -0700)`, `System clock synchronized:
yes`. **No se midieron** `NTP` ni `LocalRTC`. El criterio del paso se da por
cumplido en lo esencial (zona horaria correcta y reloj sincronizado), y los dos
valores que faltan se anotan como **no verificados**, no como cumplidos. Si la
Fase 2 necesita certeza sobre ellos, se vuelven a correr.

**D13 · El diagnóstico da UN solo `[!!]` y termina en segundos.**
El plan afirmaba que la MAC de relleno `00:00:00:00:00:00` "tiene formato válido,
así que el programa la acepta y de verdad intenta conectarse", con "dos o tres
líneas `[!!]`" y "hasta un par de minutos probando canales RFCOMM". **Medido:
es falso.** `crear_impresora` (`ruleta/app.py`) rechaza la MAC toda a ceros
**antes** de abrir ningún socket y lanza `ErrorConfig`, así que la salida real es
exactamente seis `[ok]`, **un** `[!!]`
(`Falta la direccion Bluetooth de la impresora: pon la MAC real en
impresora.mac de config.json`) y `EXIT=1`, en segundos. **Ya está corregido** en
el encabezado, en el Paso 9, en el Paso 10, en la trampa 12 de la §5 y en el
golden de la §7, que contaba una frase (`no está emparejada`) que **no aparece**.
Ficha **F-054**.

**D14 · La vista previa del Paso 10 no se corrió.**
`python3 -m ruleta vista-previa --premio test1` **no** aparece en el archivo de
hechos: no se ejecutó y no hay salida que pegar. El resto del Paso 10 (pruebas,
diagnóstico, servicio, udev, `datos/`) sí se midió. La vista previa es la
comprobación de acentos y de formato de boleto, así que **se corre al principio
de la Fase 2**, que es donde de verdad hace falta antes de gastar papel. Se
marca aquí para que nadie la dé por hecha.

**D15 · En la Pi, `git status` muestra 2 cambios de modo.**
El verificador midió `git status --porcelain | wc -l` → `2`, no `0`. **No son
cambios de contenido**: son los `chmod 644 → 755` que el Paso 8 aplica a
`instalar.sh` y `herramientas/emparejar.sh` para poder ejecutarlos, contra un
índice que los tiene como `100644` (§5, trampa 1). El hash local
`2052e4700c53f274a2b2f28ff0d7df62d519ffa8` coincide con `origin/main`.
**Cómo se resuelve:** commiteando el bit de ejecución en el repositorio (modo
`100755`), cosa que hace el **agente de commit en este mismo cierre**. Cuando
eso esté publicado, un `git pull` en la Pi dejará el árbol limpio y el
`chmod +x` del Paso 8 pasará a ser una red de seguridad en vez de un requisito.
**Hasta entonces, el `chmod +x` sigue siendo obligatorio.**

**D16 · El usuario prefiere conectar la impresora por USB. La Fase 2 se
replantea.**
Decisión del usuario tomada hoy: probará primero el **cable USB** de la impresora
AOMU My-A1, no el Bluetooth. Hoy no se pudo probar porque **no trajo el cable de
corriente de la impresora**; queda para mañana. La §9 de este plan ya está
reescrita con ese orden (USB primero, Bluetooth de respaldo) y el plan detallado
se escribirá en `docs/planes/fase-2-impresora.md`, archivo que **todavía no
existe** en el repositorio. Dos cosas medidas que la Fase 2 va a necesitar: el
usuario `asadero` **no** pertenece al grupo `lp` (sí a `lpadmin`), y el
`README.md` §9 dice que para `/dev/usb/lp0` hay que estar en `lp` — ficha
**F-052**.

**D17 · El acta se llama `2026-09-11-fase-1.md`, no
`2026-09-11-fase-1-preparar-pi.md`.**
El Paso 14 y la fila 14 de la bitácora pedían
`docs/actas/<AAAA-MM-DD>-fase-1-preparar-pi.md`; la convención de `CLAUDE.md` es
`docs/actas/<AAAA-MM-DD>-<fase>.md`. Se siguió la convención de `CLAUDE.md`.
Este plan ya está corregido para que apunte al archivo que de verdad existe.

### Correcciones aplicadas al texto de este plan

Un ejecutor que hubiera guardado una copia vieja debe saber qué cambió. Estas
son **todas** las correcciones de contenido (lo demás son notas añadidas):

| Dónde | Antes (falso) | Ahora (medido) | Por qué |
|---|---|---|---|
| Encabezado, tiempos | `diagnostico` tarda "un par de minutos" | solo `instalar.sh` necesita el límite de 10 min | D13 |
| §2, decisión 5 | Zona horaria `America/Mexico_City` | `America/Hermosillo` | D4 |
| §3, material | Batería RTC "(Opcional, recomendado)" | **necesaria**, pendiente de comprar | D9 |
| Paso 4, punto 7 | Time zone `America/Mexico_City` | `America/Hermosillo` | D4 |
| Paso 7, comando y tabla | `rfkill list bluetooth` | `LC_ALL=C /usr/sbin/rfkill list bluetooth` | D7 |
| Paso 9, "cosas normales" | "dirá que la impresora no está emparejada… par de minutos" | un solo `[!!]` de MAC faltante, en segundos | D13 |
| Paso 10, criterio 1 | `[!!] la impresora 00:00:00:00:00:00 no está emparejada…` | `[!!] Falta la direccion Bluetooth de la impresora…` | D13 |
| Paso 11 | `set-timezone America/Mexico_City`, `date` con `CST` | `America/Hermosillo`, `date` con `MST` | D4 |
| Paso 12 | "(opcional)" | necesaria: la Pi va sin red | D9 |
| Paso 14 | acta `…-fase-1-preparar-pi.md` | acta `2026-09-11-fase-1.md` | D17 |
| §5, trampa 12 | la MAC de relleno "se acepta y se intenta conectar" | se rechaza antes, en `crear_impresora` | D13 |
| §7, golden `rfkill` | `rfkill list bluetooth` | `/usr/sbin/rfkill list bluetooth` | D7 |
| §7, golden diagnóstico | `grep -c "no está emparejada"` → 1 | `grep -c "\[!!\]"` → 1 y `grep -c "impresora.mac"` → 1 | D13 |
| §7, golden `Timezone` | `America/Mexico_City` | `America/Hermosillo` | D4 |
| §9, Fase 2 | Bluetooth primero | USB primero, Bluetooth de respaldo | D16 |

**No se tocó nada más**, pero ojo: **no todos los demás goldens de la §7 se
midieron.** `systemctl show -p SubState --value ruleta` **no se corrió** y queda
anotado como **no verificado**, no como cumplido (§7 y acta §3); y el de la
versión de Python se comprobó con `python3 --version` (`Python 3.13.5`), no con
el `python3 -c` que está escrito. Los goldens restantes sí se midieron y
salieron exactamente como estaban escritos: se dejan tal cual.

---

## 1. Objetivo y alcance

**Objetivo.** Dejar una Raspberry Pi 5 encendida, en la red Wi-Fi del negocio,
accesible por SSH con llave desde la PC sin teclear nada, con el programa de la
ruleta clonado en `/home/asadero/ruleta`, todas sus dependencias instaladas, sus
pruebas automáticas en verde y el servicio `ruleta` **registrado y habilitado
para arrancar solo al encender, pero detenido**.

**Qué queda dentro de esta fase**

- Grabar el sistema en la microSD y el primer arranque.
- Acceso remoto por SSH con llave (sin contraseña para los agentes).
- Clonar el repositorio y correr el instalador.
- Comprobar sistema, dependencias, Bluetooth encendido (el adaptador de la Pi,
  no la impresora), hora y pruebas automáticas.

**Qué queda explícitamente FUERA de esta fase**

- **La impresora.** No se empareja, no se prueba, no se toca `emparejar.sh` ni
  `probar-impresora`. Eso es la Fase 2.
- **Los botones y el LED.** No se cablea nada al header de 40 pines. Eso es la
  Fase 3.
- **Arrancar el servicio.** `sudo systemctl start ruleta` **no** se corre en
  esta fase: sin impresora emparejada el servicio solo acumularía errores de
  conexión en el log. Queda `enabled` (arrancará solo cuando se reinicie la Pi
  después de la Fase 2) pero `inactive` hoy.
- Premios reales, logo definitivo y reinicio de inventario. Eso es la Fase 4.

---

## 2. Decisiones cerradas

Estas decisiones ya están tomadas. **Solo el usuario puede cambiarlas.** Un
ejecutor que crea que alguna está mal se detiene y pregunta; no improvisa.

1. **Sistema: Raspberry Pi OS Lite (64-bit), versión Trixie (Debian 13), grabado
   con Raspberry Pi Imager desde la PC Windows. Sin escritorio.**
   *Por qué:* es el sistema oficial, trae Python 3.13 y ya incluye `gpiozero`,
   `lgpio` y `bluez`; sin escritorio arranca más rápido, usa menos memoria y no
   necesita monitor, que es justo lo que pide una caja sin pantalla.

2. **Nombre de equipo: `ruleta`. Usuario: `asadero`.**
   *Por qué:* el nombre hace que la Pi se llame `ruleta.local` en la red y todos
   los comandos del proyecto se escriben una sola vez; el usuario `asadero` es
   el que queda escrito dentro del servicio systemd y en la ruta
   `/home/asadero/ruleta`, así que cambiarlo después obliga a reinstalar.

3. **Contraseña: la elige y la teclea el usuario dentro de Imager.**
   Sirve para entrar por consola local (teclado y monitor) y como respaldo.
   **Ningún agente la conoce, la pide ni la escribe en ningún lado.**
   *Por qué:* una credencial que ningún agente ve no se puede filtrar en un
   chat, en un log ni en el repositorio.

4. **Acceso remoto: SSH con llave.** Par ed25519 generado en la PC en
   `~/.ssh/id_ruleta`, **sin frase de paso**. La llave privada nunca sale de la
   PC, nunca se pega en un chat y nunca entra al repositorio. La llave pública
   `id_ruleta.pub` se pega en Imager en **"Allow public-key authentication
   only"**. Alias `ruleta` en `~/.ssh/config` de la PC, con respaldo por IP si
   mDNS falla.
   *Por qué:* sin frase de paso los agentes pueden entrar y verificar sin que
   nadie teclee nada; con "solo llave pública" nadie puede entrar adivinando la
   contraseña, y el alias hace que todos los comandos de todas las fases se
   escriban igual aunque cambie la IP.

5. **Wi-Fi: SSID y contraseña los teclea el usuario en Imager. País MX. Zona
   horaria `America/Hermosillo`. Teclado `latam` (o `es`). Locale
   `es_MX.UTF-8`.**
   *Por qué:* el país es obligatorio, si no el Wi-Fi queda bloqueado por
   regulación; la zona horaria decide la fecha que sale impresa en los boletos y
   el corte del "día" de las 6:00.
   *(Corregido con lo medido el 2026-09-11: esta decisión decía
   `America/Mexico_City`. **El usuario eligió `America/Hermosillo` en Imager** y
   esa es la correcta: Sonora va en `MST (-0700)` y no cambia de horario. Ver
   §0-bis D4. La locale `es_MX.UTF-8` **no se aplicó**: el Paso 13 quedó sin
   hacer y no afecta al programa, §0-bis D6.)*

6. **Instalación del programa: `git clone` del repositorio público en
   `~/ruleta`** (no `scp`), luego `chmod +x` de los `.sh` y `sudo ./instalar.sh`
   dentro de `~/ruleta`.
   *Por qué:* clonar trae exactamente lo que está publicado, con finales de
   línea LF, sin arrastrar la carpeta `datos/` de pruebas de la PC, y deja
   `git pull` listo para las actualizaciones de todas las fases siguientes.

7. **Deploy para todas las fases siguientes**, desde la PC, por SSH:

   ```bash
   ssh ruleta 'cd ~/ruleta && git pull --ff-only && chmod +x instalar.sh herramientas/*.sh && sudo systemctl restart ruleta'
   ```

   Verde = `ssh ruleta 'journalctl -u ruleta -n 50'` muestra
   `Lista. Esperando jugadas.` e `Inventario impreso (arranque)`.
   *Por qué:* un solo comando reproducible, que nunca pisa cambios locales
   (`--ff-only` falla en vez de mezclar a ciegas) y que deja el servicio con el
   código nuevo. **En la Fase 1 este deploy no aplica: el servicio no se
   arranca.**

8. **División del trabajo.** Lo físico (comprar, descargar Imager, meter la
   microSD, pegar la llave pública, teclear contraseñas en Imager, encender) lo
   hace el **usuario**. Todo lo que se pueda hacer desde la PC por terminal o
   por SSH lo hace un **agente**, y lo verifica **otro**. Los agentes **nunca
   teclean credenciales**: si un paso exige contraseña (por ejemplo `sudo` sin
   NOPASSWD), el paso se marca **"requiere al usuario"** y lo corre él.
   *Por qué:* separa lo que una máquina puede repetir sin error de lo que exige
   manos y ojos, y mantiene las credenciales fuera del alcance de los agentes.
   *(Así ocurrió el 2026-09-11: `sudo` pedía contraseña, el paso se marcó
   "requiere al usuario" y **el usuario tecleó y creó él mismo**
   `/etc/sudoers.d/010_asadero-nopasswd`. Desde entonces los agentes ya corren
   `sudo` por SSH sin pedir nada. Ver §0-bis D2.)*

---

## 3. Material necesario

- [ ] **Raspberry Pi 5** (cualquier cantidad de RAM sirve; 4 GB sobra).
- [ ] **Fuente oficial de 27 W USB-C** (la Pi 5 con una fuente de celular
      arranca, pero avisa "low voltage" y se porta raro bajo carga).
- [ ] **microSD de 16 GB o más, clase A2** (A2 o A1; las genéricas lentas hacen
      que todo tarde el triple).
- [ ] **Lector de microSD para la PC** (adaptador USB o la ranura de la laptop).
- [ ] **Red Wi-Fi 2.4 o 5 GHz con internet**, con su SSID y contraseña a la
      mano. El internet solo hace falta para instalar; después la ruleta
      funciona sin él.
- [ ] *(Opcional)* **Cable Ethernet**: si el Wi-Fi da problemas, conectar la Pi
      al módem por cable resuelve la Fase 1 sin tocar nada más.
- [ ] **Batería RTC ML-2020** ("RTC Battery for Raspberry Pi 5", conector J5
      junto al USB-C): mantiene la hora tras un corte de luz cuando no hay
      internet. **Ya NO es opcional**: el 2026-09-11 el usuario decidió que en
      producción la Pi va **sin red**, así que sin esta batería los boletos
      saldrían con la fecha equivocada después de cualquier apagón. **Pendiente
      de comprar e instalar** (§0-bis D9, Paso 12).

**No hace falta monitor ni teclado.** Todo se hace desde la PC.

---

## 4. Pasos

### Paso 1 · Instalar Raspberry Pi Imager en la PC

**QUIÉN:** usuario.
*(Medido el 2026-09-11 antes de empezar: Imager NO estaba instalado en esta PC.
**Hecho el mismo día:** el usuario lo instaló y el registro de Windows reporta
`Raspberry Pi Imager v2.0.11.1`. Ese fue el criterio que se usó; el `ls` de
abajo no se corrió.)*

**QUÉ HACER**

1. Abrir en el navegador: `https://www.raspberrypi.com/software/`
2. Descargar **"Download for Windows"** (archivo `imager_x.y.z.exe`).
3. Doble clic → **Install** → **Finish**. Instalación normal, sin opciones.

**CRITERIO DE ACEPTACIÓN**

- En el menú Inicio aparece **Raspberry Pi Imager** y al abrirlo muestra tres
  botones grandes: dispositivo, sistema operativo y almacenamiento.
- Comprobación desde Git Bash (la puede correr un agente):

  ```bash
  ls -l /c/Program\ Files*/Raspberry*Pi*Imager*/rpi-imager.exe
  ```

  Debe imprimir **al menos una** ruta. Según la versión, el instalador de Imager
  deja el programa en `C:\Program Files\Raspberry Pi Imager\` o en
  `C:\Program Files (x86)\Raspberry Pi Imager\`; el patrón de arriba cubre las
  dos. Si no imprime ninguna, antes de dar el paso por fallido comprobar el
  menú Inicio y, si hace falta, buscarlo con:

  ```bash
  ls -l "/c/Program Files/Raspberry Pi Imager/rpi-imager.exe" \
        "/c/Program Files (x86)/Raspberry Pi Imager/rpi-imager.exe" 2>/dev/null
  ```

**SI FALLA**

- Windows muestra *"Windows protegió tu PC"* (SmartScreen): **Más información →
  Ejecutar de todas formas**. Hacerlo **solo** si el archivo se descargó de
  `raspberrypi.com`.
- *"Se requieren privilegios de administrador"*: clic derecho en el `.exe` →
  **Ejecutar como administrador**.
- Si la descarga se corta a la mitad, borrar el `.exe` y bajarlo de nuevo; un
  instalador incompleto da errores raros al grabar.

---

### Paso 2 · Generar el par de llaves SSH en la PC

**QUIÉN:** agente (desde Git Bash).
*(Corregido con lo medido el 2026-09-11: aquí decía que `~/.ssh` «ya existe» con el par `id_ruleta` y que por eso este paso era «de verificación, no de generación». **Es falso.** El archivo de hechos medidos de la sesión dice lo contrario: **no existía `~/.ssh`, ni `id_ruleta`, ni `~/.ssh/config`**, y el agente del Paso 2 **generó la llave desde cero**, sin sobrescribir nada (ver §0-bis D5 y la fila 2 de la §0). Lo que sí sigue valiendo: el `test -f ... ||` impide regenerarla, y **no se regenera** — la pública que se pegó en Imager es la de huella `256 SHA256:sOmEM5P6LNzx7c5SOyy33NnxWOj+Qt4/RpPjwCcDSQw ruleta-asadero`.)*

**QUÉ HACER**

```bash
mkdir -p ~/.ssh
test -f ~/.ssh/id_ruleta || ssh-keygen -t ed25519 -f ~/.ssh/id_ruleta -N "" -C ruleta-asadero
```

El `test -f ... ||` está a propósito: si la llave ya existe, `ssh-keygen`
preguntaría *"Overwrite (y/n)?"* y dejaría al agente colgado, o peor,
sobrescribiría una llave que la Pi ya conoce.

Después, entregar al usuario **solo el contenido de la llave pública**:

```bash
cat ~/.ssh/id_ruleta.pub
cat ~/.ssh/id_ruleta.pub | clip     # opcional: la deja en el portapapeles de Windows
```

**CRITERIO DE ACEPTACIÓN**

```bash
ls -l ~/.ssh/id_ruleta ~/.ssh/id_ruleta.pub
ssh-keygen -l -f ~/.ssh/id_ruleta.pub
```

- Existen los dos archivos.
- La huella se imprime así (el `SHA256:` cambia en cada PC, lo demás no):

  ```
  256 SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx ruleta-asadero (ED25519)
  ```

- `cat ~/.ssh/id_ruleta.pub` imprime **una sola línea**, que empieza con
  `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5` y termina en ` ruleta-asadero`.

**SI FALLA**

- `ssh-keygen: command not found`: usar el cliente de Windows,
  `/c/Windows/System32/OpenSSH/ssh-keygen.exe`, con los mismos argumentos.
- `Saving key "/c/Users/.../.ssh/id_ruleta" failed: No such file or directory`:
  faltó el `mkdir -p ~/.ssh`.

**PROHIBIDO EN ESTE PASO:** mostrar, copiar, pegar o enviar el archivo
`~/.ssh/id_ruleta` (el que **no** termina en `.pub`). Ese es el secreto y se
queda en la PC. Al usuario se le entrega únicamente el contenido de `.pub`.

---

### Paso 3 · Alias `ruleta` en `~/.ssh/config` de la PC

**QUIÉN:** agente.

**QUÉ HACER**

```bash
touch ~/.ssh/config
grep -q "^Host ruleta$" ~/.ssh/config || cat >> ~/.ssh/config <<'FIN'

Host ruleta
    HostName ruleta.local
    User asadero
    IdentityFile ~/.ssh/id_ruleta
    IdentitiesOnly yes
    StrictHostKeyChecking accept-new
    ServerAliveInterval 30
FIN
```

Qué hace cada línea, para que nadie la "mejore" a ciegas:

- `IdentitiesOnly yes`: obliga a usar **esta** llave y no todas las que haya en
  el agente SSH (si no, tras 5 llaves rechazadas la Pi corta la conexión).
- `StrictHostKeyChecking accept-new`: acepta la huella la **primera** vez sin
  preguntar (un agente con `BatchMode` no puede contestar "yes") y después la
  deja fijada: si algún día cambia, la conexión se rechaza y hay que
  investigarlo. No es lo mismo que desactivar la comprobación.
- `ServerAliveInterval 30`: evita que el Wi-Fi tire una sesión larga (el
  instalador tarda minutos).

Git Bash y el `ssh.exe` de Windows leen **el mismo archivo**
(`C:\Users\seduv\.ssh\config`), así que el alias sirve en los dos.

**CRITERIO DE ACEPTACIÓN**

```bash
ssh -G ruleta | grep -E "^(hostname|user|identityfile|stricthostkeychecking) "
```

Debe imprimir, en este orden:

```
user asadero
hostname ruleta.local
identityfile ~/.ssh/id_ruleta
stricthostkeychecking accept-new
```

(el orden de las cuatro líneas puede variar según la versión; lo que importa es
que los cuatro valores sean esos).

**Si `stricthostkeychecking` sale `ask`**, el bloque `Host ruleta` ya existía
**sin** esa línea, así que el `grep -q` de arriba no agregó nada: hay que abrir
`~/.ssh/config`, agregar `StrictHostKeyChecking accept-new` dentro del bloque y
volver a correr la comprobación **antes** de seguir. Si no, el Paso 6 falla con
`Host key verification failed`: con `BatchMode=yes` ningún agente puede
contestar "yes" a la pregunta de la huella.
*(Medido el 2026-09-11: en esta PC `~/.ssh/config` ya trae un bloque
`Host ruleta` **sin** `StrictHostKeyChecking`; este es exactamente el caso.)*

**Además, `~/.ssh/known_hosts` de esta PC YA TIENE tres huellas grabadas para
`ruleta.local` (medido el 2026-09-11; también existe `known_hosts.old`), y la Pi
todavía no existe.** Consecuencia doble:

1. `StrictHostKeyChecking accept-new` **no** sirve aquí: la huella no será
   «nueva» sino **distinta**, así que el Paso 6 fallará en su primer intento con
   `REMOTE HOST IDENTIFICATION HAS CHANGED!` y `BatchMode=yes` no podrá
   contestar nada.
2. Una huella grabada para un nombre que aún no debería resolver significa que
   **algo más contestó como `ruleta.local`**. Antes de borrarla hay que
   **avisar al usuario** de la anomalía; borrarla en silencio equivale a aceptar
   a ciegas cualquier equipo que responda a ese nombre.

Por eso, **antes del Paso 6 y solo después de avisar**, se corre una vez:

```bash
ssh-keygen -R ruleta.local
```

(nunca borrar `known_hosts` entero: §8 prohibición 11). Se anota en el acta que
la huella previa existía y que se eliminó.

> **QUÉ PASÓ DE VERDAD el 2026-09-11 (no borrar este aviso, volverá a valer).**
> Nada de esas dos consecuencias ocurrió. El Paso 6 funcionó **al primer
> intento** y la primera conexión imprimió
> `Warning: Permanently added 'ruleta.local' (ED25519) to the list of known
> hosts.`, es decir, trató la huella como **nueva**, no como cambiada. **El
> archivo de hechos no registra que se haya corrido `ssh-keygen -R
> ruleta.local`**, así que por qué no hubo choque **queda sin explicar** (ver la
> duda en `docs/actas/2026-09-11-fase-1.md`). Tampoco hizo falta la rama manual
> de `stricthostkeychecking ask`: cada conexión llevó
> `-o StrictHostKeyChecking=accept-new` en la línea de comandos. El aviso se
> queda escrito porque **sí** valdrá el día que se regrabe la microSD (§5,
> trampa 15). Ver §0-bis D5.

**SI FALLA**

- `Bad configuration option`: una línea mal escrita; revisar que la indentación
  sean espacios y que no haya caracteres raros por copiar de un PDF.
- `Warning: Unprotected private key file` (lo tira el `ssh.exe` de Windows, no
  el de Git Bash): corregir permisos solo si aparece, con
  `icacls "%USERPROFILE%\.ssh\id_ruleta" /inheritance:r /grant:r "%USERNAME%":R`
  desde CMD. Si se usa siempre Git Bash, no suele aparecer.

---

### Paso 4 · Grabar la microSD con Raspberry Pi Imager

**QUIÉN:** usuario. **Este es el paso más delicado de la fase: Imager BORRA
POR COMPLETO el disco que se le indique.**

**ANTES DE EMPEZAR**, tener a la mano:

- El SSID (nombre) y la contraseña del Wi-Fi.
- La contraseña que va a usar para el usuario `asadero` (anotada en papel, no
  en un chat).
- El contenido de `~/.ssh/id_ruleta.pub` del Paso 2 (una línea larga).

*(Ayuda opcional del agente, solo lectura, para identificar la microSD: en
PowerShell `Get-Disk | Select-Object Number, FriendlyName, Size, BusType`. La
microSD es la de tamaño chico y `BusType` `USB` o `SD`. Un agente NUNCA graba
discos.)*

**QUÉ HACER**

1. Meter la microSD en el lector y el lector en la PC.
2. Abrir **Raspberry Pi Imager**.
3. **"Raspberry Pi Device"** (*Dispositivo Raspberry Pi*) → elegir
   **Raspberry Pi 5**.
4. **"Operating System"** (*Sistema operativo*) → **"Raspberry Pi OS (other)"**
   → **"Raspberry Pi OS Lite (64-bit)"**. En su descripción debe decir *"no
   desktop environment"*. **No** elegir la primera opción de la lista (esa trae
   escritorio).
5. **"Storage"** (*Almacenamiento*) → elegir la microSD.
   **TRAMPA:** aquí se elige un disco que se va a borrar entero. Comprobar que
   el tamaño coincide con la microSD (por ejemplo `32 GB`) y que **no** es el
   disco del sistema ni un disco externo con fotos. Si aparecen dos discos con
   el mismo tamaño, desconectar el que no es y volver a abrir la lista.
6. **"Next"** (*Siguiente*) → pregunta *"Would you like to apply OS
   customisation settings?"* → **"Edit Settings"** (*Editar ajustes*).
   *(En versiones viejas de Imager esto está en el engrane ⚙ de la esquina.)*
7. Pestaña **GENERAL**:
   - ✔ **"Set hostname"** → escribir `ruleta`
   - ✔ **"Set username and password"** → Username: `asadero` · Password: la que
     el usuario elija (**la teclea él; ningún agente la ve**)
   - ✔ **"Configure wireless LAN"** → SSID y Password del Wi-Fi ·
     **"Wireless LAN country"** → **MX**
   - ✔ **"Set locale settings"** → **"Time zone"**: `America/Hermosillo` ·
     **"Keyboard layout"**: `latam` (si no aparece, `es`)
     *(Corregido con lo medido el 2026-09-11: aquí decía `America/Mexico_City`.
     El usuario eligió `America/Hermosillo`, que es la correcta para Sonora.
     Ver §0-bis D4.)*
8. Pestaña **SERVICES** (*Servicios*):
   - ✔ **"Enable SSH"**
   - Elegir **"Allow public-key authentication only"** (*Permitir solo
     autenticación con llave pública*)
   - En el cuadro de texto, **pegar la línea completa** de
     `~/.ssh/id_ruleta.pub`. Debe quedar **una sola línea**, empezando por
     `ssh-ed25519` y sin cortes.
9. Pestaña **OPTIONS** (*Opciones*): ✔ "Eject media when finished" si se quiere
   que expulse sola la tarjeta. Si aparece "Enable telemetry", se puede
   desmarcar.
10. **"Save"** (*Guardar*) → vuelve a la pregunta anterior → **"Yes"** (*Sí*)
    para aplicar los ajustes.
11. Aviso final: *"All existing data on '...' will be erased"* → **confirmar
    solo si el disco nombrado es la microSD**.
12. Esperar: escribe y luego **verifica**. Entre 5 y 15 minutos según la
    tarjeta. No desconectar nada.

**CRITERIO DE ACEPTACIÓN**

- Imager muestra **"Write Successful"** / *"Escritura correcta"*.
- Foto de esa pantalla, guardada como evidencia.

**SI FALLA**

- *"Verify failed"* / *"Error de verificación"*: repetir el grabado. Si vuelve a
  fallar, la microSD o el lector están mal: probar otra tarjeta.
- Al terminar, Windows abre ventanas del tipo **"Tienes que formatear el disco
  de la unidad E: antes de usarlo"**: **CANCELAR siempre**. Es la partición
  Linux, que Windows no sabe leer. Formatearla arruina el grabado.
- Si Imager se queda pegado en 0 %, sacar y volver a meter el lector y reiniciar
  Imager.
- Si el Wi-Fi es de **red oculta** o pide aceptar un portal web, Imager no lo
  puede configurar: usar el **cable Ethernet** para esta fase.

---

### Paso 5 · Primer arranque de la Pi

**QUIÉN:** usuario.

**QUÉ HACER**

1. Sacar la microSD de la PC (expulsar antes desde Windows si no la expulsó
   Imager).
2. Meterla en la ranura de abajo de la Raspberry Pi 5, con los contactos hacia
   la placa. Entra suave; no forzar.
3. *(Opcional)* Conectar el cable Ethernet al módem.
4. Conectar la fuente de 27 W. La Pi enciende sola.
5. **Esperar de 2 a 3 minutos.** Es normal que:
   - el LED verde parpadee de forma irregular (está leyendo la microSD),
   - la Pi **se reinicie sola una vez** (expande el sistema de archivos y aplica
     la configuración de Imager).
6. No desconectar la corriente durante esos minutos.

**CRITERIO DE ACEPTACIÓN**

Desde la PC, en Git Bash:

```bash
ping -n 1 ruleta.local
```

Debe contestar con una línea `Respuesta desde 192.168.x.x` (o
`Reply from ...`). Guardar también una foto de la Pi encendida.

**SI FALLA**

- **Nada responde a los 5 minutos:** desconectar la corriente, revisar que la
  microSD esté bien metida, volver a encender y esperar otros 3 minutos.
- **Sigue sin responder:** lo más probable es un error de dedo en el SSID o la
  contraseña del Wi-Fi dentro de Imager. Eso **no** se puede corregir por red:
  hay que **volver al Paso 4** y regrabar la tarjeta. Antes de regrabar, probar
  con el cable Ethernet: si por cable sí aparece, el problema es el Wi-Fi.
- **El LED verde no prende nada:** fuente insuficiente o microSD mal grabada.
  Probar la fuente oficial de 27 W y regrabar.
- Si el nombre `ruleta.local` no resuelve pero la Pi sí está encendida, no es
  un fallo de arranque: seguir con el Paso 6, que trae el respaldo por IP.

---

### Paso 6 · Entrar por SSH desde la PC

**QUIÉN:** agente.

**QUÉ HACER**

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 ruleta 'hostname'
```

**CRITERIO DE ACEPTACIÓN**

La salida es exactamente:

```
ruleta
```

Sin preguntas, sin pedir contraseña, sin frase de paso.

**SI FALLA**

- **`ssh: Could not resolve hostname ruleta.local`** (mDNS no resolvió en esta
  red). Buscar la IP de la Pi:

  ```bash
  ping -n 1 ruleta.local
  arp -a | grep -i -E "d8-3a-dd|dc-a6-32|e4-5f-01|b8-27-eb|2c-cf-67"
  ```

  (esos son prefijos MAC de Raspberry Pi). Si no aparece, este sub-paso
  **requiere al usuario**: entrar a la administración del módem exige teclear la
  contraseña del router, y **ningún agente teclea credenciales** (§2 decisión 8,
  §8 prohibición 1). El usuario abre la página del módem, busca el dispositivo
  llamado `ruleta` en la lista de clientes DHCP y le pasa la IP al agente.

  Con la IP en la mano, **editar el bloque `Host ruleta`** de `~/.ssh/config` y
  cambiar `HostName ruleta.local` por `HostName 192.168.x.x`. Así **ningún otro
  comando de este plan ni de las fases siguientes cambia**. Anotar la IP en el
  acta y, si el módem lo permite, reservarla por DHCP para que no se mueva.

- **`Permission denied (publickey)`**: la llave pública pegada en Imager no
  corresponde a `~/.ssh/id_ruleta`, o se pegó cortada. Como Imager quedó en
  *"solo llave pública"*, no hay forma de entrar con contraseña por red: se
  **regraba la microSD** (Paso 4) pegando bien el contenido de
  `~/.ssh/id_ruleta.pub`. No inventar llaves nuevas: se reusa la misma.

- **`REMOTE HOST IDENTIFICATION HAS CHANGED!` / `Host key verification failed`**
  (típico después de regrabar la tarjeta, porque la Pi genera otra identidad):

  ```bash
  ssh-keygen -R ruleta.local
  ssh-keygen -R 192.168.x.x
  ```

  y volver a intentar.

- **`Connection timed out`**: la Pi no terminó de arrancar o no está en la red.
  Volver al Paso 5.

- **Pide contraseña o frase de paso**: con `BatchMode=yes` el comando falla en
  vez de colgarse, que es lo que se quiere. Revisar que `IdentityFile` apunte a
  `~/.ssh/id_ruleta` y que esa llave se creó con `-N ""`.

---

### Paso 7 · Comprobaciones del sistema en la Pi

**QUIÉN:** agente.

**QUÉ HACER**

```bash
ssh ruleta 'uname -m'
ssh ruleta '. /etc/os-release; echo $VERSION_CODENAME'
ssh ruleta 'python3 --version'
ssh ruleta 'whoami; id -nG'
ssh ruleta 'sudo -n true && echo SUDO_SIN_CONTRASENA || echo SUDO_PIDE_CONTRASENA'
ssh ruleta 'LC_ALL=C /usr/sbin/rfkill list bluetooth'
ssh ruleta 'bluetoothctl show | head -n 6'
ssh ruleta 'df -h /; free -h'
```

*(Corregido con lo medido el 2026-09-11: aquí decía `rfkill list bluetooth` a
secas y contestó `rfkill: command not found`, **aunque el paquete sí está
instalado**. El PATH de una sesión SSH no interactiva no incluye `/usr/sbin`
(§5, trampa 16; §0-bis D7). Con la ruta absoluta funciona.)*

**CRITERIO DE ACEPTACIÓN**

| Comando | Salida esperada |
|---|---|
| `uname -m` | `aarch64` |
| `VERSION_CODENAME` | `trixie` |
| `python3 --version` | `Python 3.13.x` |
| `whoami` | `asadero` |
| `id -nG` | incluye `gpio` y `sudo` |
| `sudo -n true` | imprime `SUDO_SIN_CONTRASENA` |
| `LC_ALL=C /usr/sbin/rfkill list bluetooth` | `Soft blocked: no` y `Hard blocked: no` |
| `bluetoothctl show` | contiene `Powered: yes` |
| `df -h /` | espacio libre de sobra (más de 10 GB) |

**Anotar los tres resultados que cambian el resto de la fase:**

1. Si `sudo -n true` imprime **`SUDO_PIDE_CONTRASENA`**, el Paso 9 se marca
   **"requiere al usuario"** y lo corre él. Ningún agente teclea contraseñas.
   *(Eso pasó el 2026-09-11: la imagen **no** traía el `010_pi-nopasswd` típico
   de Raspberry Pi OS. El usuario resolvió creando él mismo
   `/etc/sudoers.d/010_asadero-nopasswd`; a partir de ahí el Paso 9 lo pudo
   correr un agente. Ver §0-bis D2.)*
2. Si `id -nG` **no** incluye `gpio`, no es un problema: el Paso 9 lo agrega. Lo
   que sí hay que recordar es que el cambio **solo se ve al abrir una sesión SSH
   nueva** (ver §5, trampa 5).
3. Si `rfkill` dice `Soft blocked: yes`, tampoco es un problema aquí: el
   instalador del Paso 9 corre `rfkill unblock bluetooth`. Se vuelve a
   comprobar en el Paso 10.

**SI FALLA**

- `uname -m` dice `armv7l`: se grabó la imagen de **32 bits**. Regrabar
  (Paso 4) eligiendo **Lite (64-bit)**.
- `VERSION_CODENAME` dice `bookworm`: es una imagen anterior. El instalador la
  soporta, pero **anotarlo en el acta y avisar al usuario**: los hechos de este
  plan (Python 3.13, paquetes preinstalados) se midieron sobre Trixie.
- `bluetoothctl: command not found`: falta `bluez`; lo instala el Paso 9.
  Continuar.
- `bluetoothctl show` dice `No default controller available`: se resuelve en el
  Paso 9 (`rfkill unblock bluetooth` + `systemctl enable --now bluetooth`). Si
  después del Paso 9 sigue igual, **detenerse y reportar**: puede ser un
  problema de la imagen y no del plan.

---

### Paso 8 · Clonar el repositorio y dar permiso de ejecución

**QUIÉN:** agente.

**QUÉ HACER**

```bash
ssh ruleta 'command -v git >/dev/null && echo GIT_OK || echo FALTA_GIT'
```

Si dijo `FALTA_GIT` (y `sudo` no pide contraseña):

```bash
ssh ruleta 'sudo apt-get update && sudo apt-get install -y git'
```

*(Medido el 2026-09-11, y ya no es una duda: **Raspberry Pi OS Lite Trixie NO
trae `git`**. El comando contestó `GIT_NO_ENCONTRADO` y `dpkg-query` dijo
`git unknown ok not-installed`. En la misma pasada faltaban también
`python3-pil` y `bluez-tools`, así que se instalaron los tres de una vez con
`sudo apt-get install -y git python3-pil bluez-tools` → `EXIT=0`. Sí venían
`bluez`, `python3-gpiozero`, `python3-lgpio` y `rfkill`. Ver §0-bis D3.)*

Clonar. **La URL va tal cual, con "Ruelta": así se llama el repositorio, no es
un error de dedo de este documento.**

```bash
ssh ruleta 'git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git ~/ruleta'
ssh ruleta 'cd ~/ruleta && chmod +x instalar.sh herramientas/*.sh'
```

**CRITERIO DE ACEPTACIÓN**

```bash
ssh ruleta 'ls ~/ruleta'
```

Debe listar al menos: `CLAUDE.md  README.md  config.json  herramientas
instalar.sh  logo.png  ruleta  ruleta.service  tests`

```bash
ssh ruleta 'test -x ~/ruleta/instalar.sh && test -x ~/ruleta/herramientas/emparejar.sh && echo PERMISOS_OK'
```

Debe imprimir `PERMISOS_OK`.

**SI FALLA**

- `fatal: destination path '/home/asadero/ruleta' already exists`: ya estaba
  clonado. No borrar nada: usar
  `ssh ruleta 'cd ~/ruleta && git pull --ff-only'`.
- `Could not resolve host: github.com`: la Pi no tiene internet o DNS.
  Comprobar con `ssh ruleta 'ping -c 1 1.1.1.1'` (si responde, es DNS; si no,
  es la red). Revisar el Wi-Fi o conectar el cable Ethernet.
- `Repository not found` / pide usuario y contraseña de GitHub: el repositorio
  no está público o la URL cambió. **DETENERSE Y PREGUNTAR AL USUARIO.** No
  intentar credenciales ni buscar URLs alternativas.
- **El clon trae menos archivos de los esperados** (por ejemplo falta `tests/`
  o `instalar.sh`): quiere decir que lo que hay publicado en GitHub no es lo que
  hay en la PC. **DETENERSE Y AVISAR**: alguien tiene que subir los commits
  antes de seguir. Esta fase depende de que el repositorio publicado tenga el
  código completo.

---

### Paso 9 · Instalar

**QUIÉN:** agente **si** el Paso 7 dijo `SUDO_SIN_CONTRASENA`. Si dijo
`SUDO_PIDE_CONTRASENA`, este paso **requiere al usuario**: él abre su propia
terminal, corre `ssh ruleta`, y dentro escribe los dos comandos tecleando su
contraseña cuando se la pida. **Ningún agente teclea contraseñas.**

**QUÉ HACER**

```bash
ssh ruleta 'cd ~/ruleta && sudo ./instalar.sh'
```

Qué hace el instalador, en orden (para poder leer su salida sin sorpresas):

1. Paquetes del sistema con `apt`: `python3 python3-gpiozero python3-lgpio
   python3-pil bluez bluez-tools rfkill`. En Lite ya vienen `gpiozero`, `lgpio`
   y `bluez`; los que realmente se descargan son `python3-pil` y `bluez-tools`.
2. Agrega al usuario a los grupos `gpio` y `bluetooth`.
3. `rfkill unblock bluetooth` + `systemctl enable --now bluetooth`.
4. Regla udev para el chip GPIO de la Pi 5 (`gpiochip4`).
5. Crea `datos/`, ajusta dueño y permisos.
6. Genera `/etc/systemd/system/ruleta.service` con el usuario y la carpeta
   reales, hace `daemon-reload` y **`systemctl enable`** (no `start`).
7. Corre `python3 -m ruleta diagnostico` y luego imprime "Instalación terminada"
   con los siguientes pasos.

**Cosas normales que NO son errores:**

- Tarda de **3 a 10 minutos** la primera vez (`apt update` + paquetes).
- Al final, el diagnóstico dirá, en **una sola línea**:
  `[!!] Falta la direccion Bluetooth de la impresora: pon la MAC real en
  impresora.mac de config.json (la obtienes con herramientas/emparejar.sh)`.
  **Es exactamente lo esperado en la Fase 1**: la impresora es la Fase 2.
- Esa parte **no tarda**: termina en segundos.

*(Corregido con lo medido el 2026-09-11: aquí decía que el diagnóstico avisaría
de que la impresora "no está emparejada" y que podía tardar "un par de minutos
probando canales RFCOMM". **Las dos cosas son falsas.** Con la MAC toda a ceros,
`crear_impresora` (`ruleta/app.py`) la rechaza antes de abrir ningún socket. Ver
§0-bis D13 y §5, trampa 12. Medido: `instalador_exit=0`, y el diagnóstico final
del instalador terminó con ese único `[!!]`.)*

**CRITERIO DE ACEPTACIÓN**

```bash
ssh ruleta 'systemctl is-enabled ruleta'
ssh ruleta 'systemctl is-active ruleta || true'
ssh ruleta 'grep -E "^(User|WorkingDirectory)=" /etc/systemd/system/ruleta.service'
```

Salidas esperadas:

```
enabled
inactive
User=asadero
WorkingDirectory=/home/asadero/ruleta
```

**SI FALLA**

- `E: Unable to locate package ...`: `apt-get update` no pudo bajar los índices
  (sin internet, o con la hora muy desfasada). Revisar red y el Paso 11, y
  volver a correr el instalador.
- `Ejecuta este instalador con sudo: sudo ./instalar.sh`: faltó el `sudo`.
- `bash: ./instalar.sh: Permission denied`: faltó el `chmod +x` del Paso 8.
- `/usr/bin/env: 'bash\r': No such file or directory`: el archivo llegó con
  finales de línea de Windows. Con `git clone` no debería pasar (el repo fuerza
  LF); si pasa, **detenerse y reportar**: alguien copió los archivos por otra
  vía.
- **Se cortó a la mitad** (se cayó el Wi-Fi, se cerró la sesión, o el comando
  llegó a su tiempo límite): **volver a correrlo tal cual**. El instalador está
  hecho para repetirse las veces que haga falta. **Nunca** parchear a mano lo
  que dejó a medias. Única excepción: si al repetirlo `apt` contesta
  `Could not get lock /var/lib/dpkg/lock-frontend` o
  `dpkg was interrupted, you must manually run 'dpkg --configure -a'`, el corte
  dejó a `dpkg` a medio configurar y **ningún** reintento del instalador va a
  pasar de ahí. Correr **una sola vez**:

  ```bash
  ssh ruleta 'sudo dpkg --configure -a'
  ```

  y después sí `ssh ruleta 'cd ~/ruleta && sudo ./instalar.sh'` entero. Si el
  mensaje del candado dice que hay **otro** proceso `apt` corriendo, no matarlo:
  esperar a que termine y reintentar.

---

### Paso 10 · Verificar el programa

**QUIÉN:** agente.

**QUÉ HACER**

```bash
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico; echo "codigo=$?"'
ssh ruleta 'cd ~/ruleta && python3 -m unittest discover -s tests -t . 2>&1 | tail -n 3'
ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta vista-previa --premio test1'
```

**CRITERIO DE ACEPTACIÓN**

1. **Diagnóstico.** Deben salir **seis** líneas `[ok]`, en este orden:

   ```
     [ok] la carpeta de datos se puede escribir
     [ok] PIL 11.1.0
     [ok] gpiozero
     [ok] lgpio
     [ok] logo: /home/asadero/ruleta/logo.png
     [ok] inventario: folio 00000
   ```

   Y **un solo** `[!!]`, el de la impresora:

   ```
     [!!] Falta la direccion Bluetooth de la impresora: pon la MAC real en impresora.mac de config.json (la obtienes con herramientas/emparejar.sh)
   ```

   **`codigo=1` es la salida esperada en esta fase**, porque el diagnóstico
   marca error mientras la impresora no tenga MAC. No es un fallo: es la Fase 2
   pendiente. Cualquier `[!!]` que **no** hable de la impresora sí es un fallo.

   *(Corregido y completado con lo medido el 2026-09-11, salida real pegada en
   `docs/actas/2026-09-11-fase-1.md`. Dos correcciones: (a) el `[!!]` que sale
   **no** es el de "no está emparejada" ni hay fallo RFCOMM — la MAC toda a
   ceros se rechaza antes (§0-bis D13); (b) **`gpiozero` y `lgpio` salen sin
   número de versión**, y eso es normal: el código imprime
   `getattr(m, '__version__', '')` y esos dos módulos no exponen `__version__`.
   Las versiones reales, consultadas con `importlib.metadata`, son
   `gpiozero 2.0.1` y `lgpio 0.2.2.0`. Es cosmético, no un fallo de instalación:
   ficha **F-051**.)*

2. **Pruebas automáticas.** Las últimas líneas deben ser:

   ```
   Ran <N> tests in <t>s

   OK
   ```

3. **Vista previa.** *(NO se corrió el 2026-09-11: no hay salida que pegar. Se
   corre al principio de la Fase 2, antes de gastar papel. Ver §0-bis D14.)*
   Salen **tres** bloques, siempre en este orden:
   `=== Boleto de premio: test1 ===`, `=== Boleto de consuelo (sin premios
   disponibles) ===` y `=== Reporte de inventario ===`. `vista-previa --premio
   ID` imprime los tres aunque se pida un solo premio (verificado contra
   `cmd_vista_previa` en `ruleta/__main__.py`: tras el premio siempre imprime el
   consuelo y el inventario). Las líneas
   grandes se dibujan con los caracteres **repetidos**, porque la consola imita
   el doble y cuádruple ancho de la impresora: el encabezado sale como
   `AAssaaddeerroo  3333`, el título como `¡¡GGAANNAASSTTEE!!` y el premio como
   `TTTTEEEESSSSTTTT    1111`. **Eso es lo correcto, no es basura.** Lo que se
   revisa es que los acentos y signos (`¡`, `á`, `ó`) se vean bien y que la
   última línea sea la de `[CORTE]`. Si en su lugar salen caracteres raros
   (`Ã¡`, `?`), falta `PYTHONIOENCODING=utf-8` (ver §5, trampa 6).

**SI FALLA**

- `[!!] falta PIL: sudo apt install python3-pil`: el Paso 9 no terminó. Volver
  a correr el instalador.
- `/usr/bin/python3: No module named ruleta`: faltó el `cd ~/ruleta`. El
  programa se ejecuta desde su carpeta.
- `FAILED (failures=... errors=...)` en las pruebas: **detenerse, pegar la
  salida completa en el acta y reportar**. No parchear código en esta fase: el
  plan es de preparación, no de desarrollo.
- `[!!] no se puede escribir en la carpeta de datos`: permisos; volver a correr
  el instalador, que hace `chown` de toda la carpeta.

---

### Paso 11 · Hora, zona horaria y NTP

**QUIÉN:** agente.

**QUÉ HACER**

```bash
ssh ruleta 'timedatectl show -p Timezone --value'
ssh ruleta 'timedatectl show -p NTP --value'
ssh ruleta 'timedatectl show -p NTPSynchronized --value'
ssh ruleta 'timedatectl show -p LocalRTC --value'
ssh ruleta 'date'
```

Se usa `timedatectl show ... --value` y no `timedatectl` a secas **a propósito**:
esa forma imprime valores que no se traducen aunque el sistema quede en español
(ver §5, trampa 11).

Si la zona horaria no es la correcta:

```bash
ssh ruleta 'sudo timedatectl set-timezone America/Hermosillo'
```

*(Corregido con lo medido el 2026-09-11: aquí decía `America/Mexico_City`. La
zona correcta para este restaurante es **`America/Hermosillo`** (Sonora, `MST`
`-0700`, sin cambio de horario), y es la que el usuario eligió en Imager, así
que **este comando no hizo falta correrlo**. Ver §0-bis D4.)*

Si `NTPSynchronized` es `no`:

```bash
ssh ruleta 'sudo timedatectl set-ntp true'
```

y volver a consultar después de un minuto.

**CRITERIO DE ACEPTACIÓN**

Cada comando imprime **un solo valor**, así el criterio no depende del orden en
que `timedatectl` liste las propiedades:

- `Timezone` → `America/Hermosillo`
- `NTP` → `yes` (el servicio de hora está activo)
- `NTPSynchronized` → `yes` (ya sincronizó)
- `LocalRTC` → `no` (el reloj de hardware va en UTC, que es lo correcto)

Además, `date` muestra la hora real del restaurante, con `MST`.

*(Medido el 2026-09-11, con el `timedatectl` completo y no con los cuatro
`show -p ... --value`: `Local time: Fri 2026-09-11 16:03:34 MST`,
`Time zone: America/Hermosillo (MST, -0700)`, `System clock synchronized: yes`.
`Timezone` y `NTPSynchronized` quedan **verificados**; `NTP` y `LocalRTC`
quedan **sin medir** y así se anotaron en el acta, no como cumplidos. Ver
§0-bis D12 y D4.)*

**SI FALLA**

- `NTPSynchronized=no` después de varios minutos: la Pi no tiene salida a
  internet, o la red bloquea NTP. No es bloqueante para la Fase 1; se anota en
  el acta y se resuelve con la batería RTC (Paso 12) o fijando la hora a mano en
  la Fase 4 (`README` §4, paso 7).
- La hora sale con 6 o 7 horas de diferencia: la zona horaria quedó en UTC;
  correr el `set-timezone` de arriba.

---

### Paso 12 · Batería RTC — **NECESARIA** (antes decía "opcional")

**QUIÉN:** usuario (la parte física) + agente (la línea de configuración,
**solo con visto bueno explícito del usuario**, porque toca
`/boot/firmware/config.txt`).

**ESTADO: NO REALIZADO el 2026-09-11. Es el principal riesgo abierto de la
Fase 1.**

> **Por qué dejó de ser opcional.** El 2026-09-11 el usuario decidió que
> **durante el evento la Pi trabajará SIN red** (el Wi-Fi y el SSH son solo para
> instalar y probar). Sin red no hay NTP, y sin NTP **la única forma de que la
> Pi sepa la hora después de un corte de luz es esta batería**. Sin ella, los
> boletos salen con fecha y hora equivocadas y el corte del "día" de las 6:00 se
> descuadra. Ya no es un "estaría bien": **hay que comprarla e instalarla antes
> del evento**, o aceptar por escrito el riesgo. Ver §0-bis D9.

Sin batería y sin internet, después de un corte de luz los boletos saldrían con
fecha equivocada.

**QUÉ HACER**

1. **Usuario:** apagar la Pi (`ssh ruleta 'sudo poweroff'` desde la PC), esperar
   a que el LED se apague, **desconectar la corriente**, conectar la batería
   ML-2020 al conector **J5** (el chiquito junto al USB-C), volver a conectar la
   corriente.
2. **Agente, solo si el usuario dio el visto bueno por escrito:**

   ```bash
   ssh ruleta 'grep -n rtc_bbat_vchg /boot/firmware/config.txt || echo NO_ESTA'
   ssh ruleta 'test -f /boot/firmware/config.txt.bak || sudo cp /boot/firmware/config.txt /boot/firmware/config.txt.bak'
   ssh ruleta 'grep -q rtc_bbat_vchg /boot/firmware/config.txt || echo dtparam=rtc_bbat_vchg=3000000 | sudo tee -a /boot/firmware/config.txt'
   # El Paso 9 dejó el servicio 'enabled': si se reinicia la Pi tal cual,
   # systemd ARRANCA 'ruleta' sin impresora, contra lo decidido en la §1 y
   # contra los goldens de la §7 (is-active = inactive, SubState = dead).
   # Por eso se deshabilita antes de reiniciar y se vuelve a habilitar después.
   ssh ruleta 'sudo systemctl disable ruleta'
   ssh ruleta 'sudo reboot'
   # El 'reboot' corta la sesión: ese ssh devuelve 255 y ES NORMAL, no es fallo.
   # NO correr el 'enable' hasta que la Pi conteste de nuevo; si se corre antes,
   # falla en silencio y el servicio se queda 'disabled', que es justo lo que
   # este bloque intenta evitar (golden de la §7: is-enabled = enabled).
   # Este comando BLOQUEA hasta que la Pi vuelve (lanzarlo con timeout 600000):
   until ssh -o BatchMode=yes -o ConnectTimeout=5 ruleta 'true' 2>/dev/null; do sleep 10; done
   ssh ruleta 'sudo systemctl enable ruleta'
   ssh ruleta 'systemctl is-enabled ruleta; systemctl is-active ruleta || true'
   ```

   Esa línea activa la **recarga** de la batería; sin ella la batería se
   descarga y no se repone.

**CRITERIO DE ACEPTACIÓN**

```bash
ssh ruleta 'grep rtc_bbat_vchg /boot/firmware/config.txt'
ssh ruleta 'cat /sys/class/rtc/rtc0/name'
```

- La primera imprime `dtparam=rtc_bbat_vchg=3000000`.
- La segunda imprime el nombre del reloj de hardware que ve el kernel: basta con
  que **imprima algo y no dé error** (en la Pi 5 suele ser `rpi_rtc`). Si
  contesta `No such file or directory`, el kernel no expone el RTC: el paso se
  anota como no verificado en el acta y no se da por cumplido.
- La prueba de verdad la hace el usuario: desconectar la corriente 5 minutos,
  volver a encender **sin internet** y comprobar que `ssh ruleta 'date'` marca la
  hora correcta.

**SI FALLA**

- **La Pi no vuelve a arrancar después de editar `config.txt`:** apagar, sacar
  la microSD, meterla en la PC, abrir la unidad que Windows sí lee (se llama
  `bootfs`), abrir `config.txt` con el Bloc de notas, **borrar la línea
  agregada**, guardar, expulsar y volver a arrancar. Por eso se hizo el `.bak`.
- La batería no entra o el conector se ve distinto: **no forzar**; es un
  conector frágil. Dejar el paso sin hacer y anotarlo.

---

### Paso 13 · Idioma del sistema `es_MX.UTF-8` (opcional)

**QUIÉN:** agente.

**ESTADO: NO REALIZADO el 2026-09-11**, y no pasa nada: el sistema quedó como lo
dejó la imagen. No se corrió ningún comando de este paso y `localectl status`
**no** se consultó. Efecto secundario bueno: como el sistema sigue en inglés, la
trampa 11 de la §5 (comandos traducidos) no muerde hoy. Ver §0-bis D6.

Imager configura zona horaria y teclado, pero **no** el idioma completo del
sistema. Este paso lo ajusta. **No es indispensable** para que la ruleta
funcione: el servicio ya fuerza `PYTHONIOENCODING=utf-8` y todos los textos del
programa están en español dentro del propio código.

**QUÉ HACER**

```bash
ssh ruleta 'sudo raspi-config nonint do_change_locale es_MX.UTF-8'
```

Si ese comando no existe o falla, el camino manual:

```bash
ssh ruleta 'sudo sed -i "s/^# *es_MX.UTF-8 UTF-8/es_MX.UTF-8 UTF-8/" /etc/locale.gen'
ssh ruleta 'sudo locale-gen es_MX.UTF-8'
ssh ruleta 'sudo localectl set-locale LANG=es_MX.UTF-8'
```

**CRITERIO DE ACEPTACIÓN**

```bash
ssh ruleta 'localectl status'
```

Muestra `System Locale: LANG=es_MX.UTF-8`.

**SI FALLA**

- `cannot set LC_ALL` o avisos de locale en cada comando posterior: la locale no
  se generó. Correr el camino manual completo (los tres comandos, en orden).
- **ADVERTENCIA:** a partir de aquí varios comandos del sistema contestan en
  español. Los goldens de la §7 están escritos para que **eso no los rompa**; si
  algún comando nuevo se agrega al plan, anteponerle `LC_ALL=C`.

---

### Paso 14 · Cierre de fase

**QUIÉN:** agente.

**QUÉ HACER**

1. **Escribir el acta** en `docs/actas/<AAAA-MM-DD>-<fase>.md` —para esta fase,
   **`docs/actas/2026-09-11-fase-1.md`**, que es el archivo que de verdad se
   escribió—, **desde el archivo de hechos medidos de la sesión (el del
   scratchpad), nunca de memoria**. *(Este paso decía
   `<AAAA-MM-DD>-fase-1-preparar-pi.md`; se siguió la convención de `CLAUDE.md`,
   que es `<AAAA-MM-DD>-<fase>.md`. Ver §0-bis D17. La carpeta `docs/actas/` no
   existía: hay que crearla.)* Debe contener, como mínimo:
   - la salida real, pegada, de cada golden de la §7;
   - la IP que tomó la Pi y si `ruleta.local` resolvió o hubo que usar IP;
   - si `sudo` pide contraseña o no;
   - la versión real de Python y el codename real del sistema;
   - qué pasos opcionales (12 y 13) se hicieron y cuáles no;
   - cualquier desviación respecto a este plan.
2. **Marcar las casillas de la §0** con fecha y evidencia.
3. **Anotar en `docs/fichas.md`** todo hallazgo residual que no justifique
   detener la fase.
4. **Actualizar la memoria del proyecto**: Fase 1 cerrada, alias SSH, usuario y
   hostname, si mDNS funcionó, si `sudo` pide contraseña, IP reservada.

**CRITERIO DE ACEPTACIÓN**

- El acta existe y cada golden de la §7 aparece con su salida real, o con la
  marca de **no medido** si no se corrió (nunca inventado).
- Todas las casillas obligatorias de la §0 (pasos 1 a 11 y 14) están marcadas.

*(Cumplido el 2026-09-11: acta en `docs/actas/2026-09-11-fase-1.md`, fichas
nuevas F-051 a F-054, bitácora de la §0 marcada y §0-bis escrita. Los pasos 12 y
13, opcionales, quedaron sin hacer y así están anotados.)*

**SI FALLA**

- Si falta la salida de algún golden, **no se inventa**: se vuelve a correr el
  comando contra la Pi y se pega lo que salga.

**PROHIBIDO:** el ejecutor **no commitea**. El commit lo hace el agente de
commit, con la lista de archivos acordada por adelantado y por rutas explícitas.

---

## 5. Trampas del entorno y del repositorio

Cosas que un ejecutor sin contexto **no puede adivinar** y que han roto este
tipo de instalaciones antes:

1. **Windows no conserva el bit de ejecución, y este repositorio tampoco lo
   tiene guardado.** Por eso la decisión es clonar con `git`, no copiar con
   `scp`. Pero además, en el índice de git `instalar.sh` y
   `herramientas/emparejar.sh` están con modo `100644`, es decir **sin** bit de
   ejecución (se comprueba en la PC con `git ls-files -s instalar.sh
   herramientas/emparejar.sh`). Consecuencia: el clon los trae SIN permiso de
   ejecución y el `chmod +x instalar.sh herramientas/*.sh` del Paso 8 es
   **obligatorio**, no una precaución barata. Si se salta, `sudo ./instalar.sh`
   falla con `Permission denied`.
   *(Medido el 2026-09-11: confirmado, y con una consecuencia que no estaba
   escrita. Después del `chmod +x`, en la Pi `git status --porcelain | wc -l`
   da **2**: son esos dos cambios de modo `644 → 755`, sin un solo cambio de
   contenido. Un ejecutor que espere un clon "limpio" al 100 % se asusta sin
   motivo. **Se resuelve commiteando el bit de ejecución en el repositorio**
   (modo `100755`), cosa que hace el agente de commit en el cierre de esta
   fase; después de eso, un `git pull` deja el árbol limpio. **Mientras no esté
   publicado, el `chmod +x` sigue siendo obligatorio.** Ver §0-bis D15.)*

2. **`instalar.sh` decide la carpeta del servicio a partir de dónde está él
   mismo.** El archivo `/etc/systemd/system/ruleta.service` queda apuntando a esa
   ruta con `WorkingDirectory`. Por eso el programa **debe** vivir en
   `/home/asadero/ruleta` y el instalador se corre con
   `cd ~/ruleta && sudo ./instalar.sh`. Instalarlo desde otra carpeta deja un
   servicio apuntando al lugar equivocado, y el error solo aparece días después.

3. **`python3 -m ruleta` solo funciona desde `~/ruleta`.** El paquete se
   encuentra por la carpeta actual. Fuera de ahí: `No module named ruleta`. El
   archivo `config.json`, en cambio, sí se localiza solo (el programa lo busca
   junto al paquete), así que no hace falta pasar `--config`.

4. **`ruleta.local` puede no resolver.** En Windows 11 la resolución mDNS es
   nativa y suele funcionar, pero hay redes (algunas con aislamiento de
   clientes o con Wi-Fi de invitados) donde no. El plan siempre trae el respaldo
   por IP: se cambia el `HostName` del bloque `Host ruleta` y **ningún otro
   comando cambia**.

5. **El grupo `gpio` requiere volver a iniciar sesión.** `usermod -aG` no afecta
   a las sesiones SSH ya abiertas. Para uso **manual** del GPIO hay que cerrar y
   abrir la sesión SSH. **El servicio no lo necesita**: `ruleta.service` trae
   `SupplementaryGroups=gpio`, así que systemd le da el grupo directamente.

6. **`PYTHONIOENCODING=utf-8` para los acentos en consola.** Al correr comandos
   por SSH sin terminal interactiva, Python puede elegir una codificación que
   destroza `ñ`, `¡` y `¿`. El servicio ya lo trae en `ruleta.service`; los
   comandos a mano se escriben
   `PYTHONIOENCODING=utf-8 python3 -m ruleta ...`.

7. **Bluetooth "soft-blocked" en imágenes Lite de Trixie.** Hay reportes de que
   el adaptador arranca bloqueado. `instalar.sh` ya corre
   `rfkill unblock bluetooth` y `systemctl enable --now bluetooth`; por eso el
   Paso 7 solo **anota** el estado y no lo arregla, y el Paso 10 lo verifica.

8. **Nunca `dtoverlay=disable-wifi` en la Pi 5.** En la Pi 5 el Wi-Fi y el
   Bluetooth comparten el mismo chip: ese overlay **también apaga el
   Bluetooth**, y la ruleta se queda sin impresora. Prohibido, aunque alguien
   quiera "ahorrar energía".

9. **`apt update` necesita internet, y el instalador tarda.** De 3 a 10 minutos
   la primera vez. Un agente que corta a los 2 minutos creyendo que se colgó
   deja el sistema a medias. Si se corta, se **vuelve a correr entero**.

10. **`systemctl is-active ruleta` devuelve `inactive` y código de salida 3.**
    Eso es lo correcto en esta fase. Un agente que trate cualquier código
    distinto de 0 como fallo va a reportar un error inexistente: por eso los
    comandos del plan llevan `|| true`.

11. **Cambiar la locale traduce la salida de varios comandos.** Si se hace el
    Paso 13, `timedatectl` sin argumentos contesta en español y rompería
    cualquier comparación por texto. Por eso los goldens usan
    `timedatectl show -p ... --value` y `systemctl show -p ... --value`, que no
    se traducen.

12. **`config.json` viene con `"mac": "00:00:00:00:00:00"`.** *(Reescrita el
    2026-09-11 con lo medido; lo que decía antes era falso.)* El programa
    **rechaza** esa MAC toda a ceros **antes de abrir ningún socket**:
    `crear_impresora`, en `ruleta/app.py`, comprueba
    `imp.mac.replace(":", "").strip("0") == ""` y lanza `ErrorConfig`.
    Consecuencia real: en la Fase 1 `diagnostico` termina con código 1 y con
    **una sola** línea `[!!]`
    (`Falta la direccion Bluetooth de la impresora: pon la MAC real en
    impresora.mac de config.json`), **en segundos**. **No** dice "no está
    emparejada", **no** intenta conectarse y **no** busca canales RFCOMM: ese
    camino del código solo se recorre con una MAC de verdad. Es lo esperado. Se
    arregla solo cuando la Fase 2 escriba la MAC real. Ver §0-bis D13 y ficha
    F-054.

13. **La contraseña del Wi-Fi, la contraseña de `asadero` y la llave privada
    `~/.ssh/id_ruleta` NUNCA van al repositorio, ni a un chat, ni a un acta.**
    En el acta se escribe "el usuario configuró el Wi-Fi", no el SSID con su
    clave. La llave pública `.pub` sí se puede mostrar: para eso es pública.

14. **`datos/` está en `.gitignore`.** El clon no la trae; la crea el instalador
    vacía. Nunca se copia una `datos/` de pruebas hechas en la PC: contaminaría
    folios e inventario.

15. **Regrabar la microSD cambia la identidad SSH de la Pi.** El siguiente
    intento de conexión falla con `REMOTE HOST IDENTIFICATION HAS CHANGED`. Se
    resuelve con `ssh-keygen -R ruleta.local` (y con la IP), nunca borrando el
    `known_hosts` entero.

16. **El PATH de una sesión SSH no interactiva NO incluye `/usr/sbin` ni
    `/sbin`.** *(Trampa nueva, medida el 2026-09-11.)* Una sesión
    `ssh ruleta '<comando>'` trae
    `PATH=/usr/local/bin:/usr/bin:/bin:/usr/games`. Por eso
    `ssh ruleta 'rfkill list bluetooth'` contestó `rfkill: command not found`
    **aunque el paquete `rfkill` está instalado**. **No es una falla de la Pi ni
    hay nada que arreglar**: se llama al binario por **ruta absoluta**
    (`/usr/sbin/rfkill`, `/usr/sbin/shutdown`, `/usr/sbin/reboot`,
    `/usr/sbin/iw`…) o se exporta el PATH al principio del comando. `sudo` no
    sufre esto porque arma su propio PATH. Un ejecutor que lea "command not
    found" como "falta el paquete" va a instalar cosas que ya están y a dar por
    rota una fase que está bien. Ver §0-bis D7.

17. **En esta PC hay DOS clientes `ssh`, y solo uno sirve para los agentes.**
    *(Trampa nueva, medida el 2026-09-11.)* Git Bash monta `C:` con la opción
    `noacl` (ver su `/etc/fstab`), así que `chmod` es un **no-op** y la capa
    POSIX siempre reporta `~/.ssh/id_ruleta` como `644`. El `ssh` de Git Bash
    (OpenSSH 10.3p1) hace la comprobación estricta de permisos y **puede
    rechazar la llave** con `UNPROTECTED PRIVATE KEY FILE ... are too open`. El
    cliente **nativo de Windows**, `C:/Windows/System32/OpenSSH/ssh.exe`
    (OpenSSH_for_Windows 9.5p2), usa las ACL de NTFS, que sí están bien
    (`icacls` muestra solo SYSTEM, Administradores y el usuario de la PC; ni
    `Users` ni `Everyone`). **Regla:** todos los comandos SSH de los agentes se
    lanzan con `/c/Windows/System32/OpenSSH/ssh.exe`. **Prohibido** "arreglarlo"
    agregando `acl` al `/etc/fstab` de Git for Windows: es configuración global
    del entorno y necesita visto bueno explícito del usuario. Ver §0-bis D8.

---

## 6. Mapa de anclas que derivan

Textos del repositorio de los que depende este plan. **Re-grep antes de cada
edición**: si el texto ya no está donde dice esta tabla, **detenerse y
preguntar**, porque significa que alguien cambió el repositorio y el plan quedó
viejo.

| Ancla | Cómo encontrarla | Por qué deriva |
|---|---|---|
| `README.md` §4, pasos 1 a 8 | `grep -n "^## 4. Instalación paso a paso" -A 90 README.md` | El paso 1 propone copiar con `scp -r`; esta fase decidió `git clone`. **Hoy no se toca el README**: la corrección necesita visto bueno del usuario (ver `docs/fichas.md`). |
| `README.md` §4, paso 1 en concreto | `grep -n "scp -r" README.md` | Es la línea exacta que contradice la decisión 6. |
| `README.md` §3 "Sistema operativo (propuesta)" | `grep -n "^## 3. Sistema operativo" -A 12 README.md` | Dice "activa SSH" y `ssh usuario@ruleta.local`; no menciona la autenticación solo por llave ni el usuario `asadero`. |
| `README.md` §4, paso 7 (hora) | `grep -n "set-ntp false" README.md` | Propone **apagar** NTP; eso solo aplica si la Pi no tendrá internet. En la Fase 1, con Wi-Fi, NTP queda **encendido**. |
| Bloque final de `instalar.sh` | `grep -n "Instalación terminada" -B 3 -A 28 instalar.sh` | Enumera los "siguientes pasos" 1 a 5 (emparejar, probar impresora, vista previa, premios, arrancar). Las Fases 2 a 4 se apoyan en ese texto. |
| Diagnóstico dentro de `instalar.sh` | `grep -n "== Diagnóstico" -A 3 instalar.sh` | Es lo que hace que el instalador termine mostrando errores de impresora en la Fase 1. |
| Convenciones de `CLAUDE.md` | `grep -n "^## Convenciones de este repo" -A 12 CLAUDE.md` | Define `docs/planes/`, `docs/actas/<AAAA-MM-DD>-<fase>.md` y `docs/fichas.md`: las rutas que usa este plan. |
| Plantilla del servicio | `grep -n "@USUARIO@\|@DIR@\|SupplementaryGroups" ruleta.service` | De ahí salen los goldens `User=asadero` y `WorkingDirectory=/home/asadero/ruleta`, y la razón por la que el servicio no necesita re-login para el grupo `gpio`. |
| Líneas `[ok]` del diagnóstico | `grep -n "\[ok\]" ruleta/__main__.py` | El golden "6 líneas `[ok]`" se deriva de ahí. Si alguien agrega o quita una comprobación, ese número cambia. |
| Rechazo de la MAC toda a ceros | `grep -n 'strip("0")' ruleta/app.py` | *(Ancla nueva, 2026-09-11.)* De esa línea de `crear_impresora` sale el golden de **un solo** `[!!]` y el hecho de que el diagnóstico termine en segundos (§5 trampa 12, §0-bis D13). Si alguien la quita, el diagnóstico volvería a intentar la conexión RFCOMM y el golden cambiaría. |
| `README.md` §9, impresora por USB | `grep -n "/dev/usb/lp0" README.md` | *(Ancla nueva, 2026-09-11.)* Dice `"tipo": "archivo", "ruta": "/dev/usb/lp0"` y "agrega tu usuario al grupo `lp`". De ahí arranca la Fase 2 por USB (§9). **Medido: `asadero` NO está en `lp`** (sí en `lpadmin`): ficha F-052. |
| Versiones de `gpiozero` y `lgpio` en el diagnóstico | `grep -n "__version__" ruleta/__main__.py` | *(Ancla nueva, 2026-09-11.)* `getattr(m, '__version__', '')` es la razón de que esas dos líneas `[ok]` salgan sin número. Ficha F-051. |

---

## 7. Criterios de aceptación de la fase y goldens

La fase está cerrada cuando **todos** estos comandos, corridos desde la PC en
Git Bash, devuelven **exactamente** la salida indicada (comparación por
igualdad, no "parecido"). Se pegan todos, con su salida real, en el acta.

> **Estado el 2026-09-11: cumplidos.** Tres de estos goldens estaban **mal
> escritos** y se corrigieron con lo medido (`rfkill` sin ruta absoluta, la
> frase del diagnóstico y la zona horaria); van marcados abajo. Uno,
> `SubState`, **no se midió** y así está anotado en el acta: no se da por
> cumplido. La tabla golden por golden, con la evidencia de cada uno, está en
> `docs/actas/2026-09-11-fase-1.md`.

```bash
ssh ruleta 'hostname'
# ruleta

ssh ruleta 'whoami'
# asadero

ssh ruleta 'uname -m'
# aarch64

ssh ruleta '. /etc/os-release; echo $VERSION_CODENAME'
# trixie

ssh ruleta 'python3 -c "import sys; print(sys.version_info[0], sys.version_info[1])"'
# 3 13

ssh ruleta 'id -nG | tr " " "\n" | grep -cx gpio'
# 1

ssh ruleta 'test -d ~/ruleta/.git && echo CLON_OK'
# CLON_OK

ssh ruleta 'test -x ~/ruleta/instalar.sh && test -x ~/ruleta/herramientas/emparejar.sh && echo PERMISOS_OK'
# PERMISOS_OK

ssh ruleta 'python3 -c "import PIL, gpiozero, lgpio" && echo DEPS_OK'
# DEPS_OK

ssh ruleta 'systemctl is-active bluetooth'
# active

ssh ruleta 'bluetoothctl show | grep -c "Powered: yes"'
# 1

ssh ruleta 'LC_ALL=C /usr/sbin/rfkill list bluetooth | grep -c "blocked: no"'
# 2
# (CORREGIDO 2026-09-11: sin la ruta absoluta da 'rfkill: command not found'
#  y este golden salía 0. El PATH de ssh no interactivo no trae /usr/sbin:
#  ver §5 trampa 16 y §0-bis D7.)

ssh ruleta 'systemctl is-enabled ruleta'
# enabled

ssh ruleta 'systemctl is-active ruleta || true'
# inactive

ssh ruleta 'systemctl show -p SubState --value ruleta'
# dead

ssh ruleta 'grep -c "^User=asadero$" /etc/systemd/system/ruleta.service'
# 1

ssh ruleta 'grep -c "^WorkingDirectory=/home/asadero/ruleta$" /etc/systemd/system/ruleta.service'
# 1

ssh ruleta 'cd ~/ruleta && python3 -m unittest discover -s tests -t . 2>&1 | tail -n 1'
# OK

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "\[ok\]"'
# 6

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "\[!!\]"'
# 1

ssh ruleta 'cd ~/ruleta && PYTHONIOENCODING=utf-8 python3 -m ruleta diagnostico 2>&1 | grep -c "impresora.mac"'
# 1
# (CORREGIDO 2026-09-11: estos dos reemplazan a
#  grep -c "no está emparejada" -> 1, que era FALSO: esa frase NO aparece.
#  Con la MAC toda a ceros el programa la rechaza antes de conectarse y saca
#  un solo [!!]: 'Falta la direccion Bluetooth de la impresora: pon la MAC
#  real en impresora.mac de config.json'. Se cuenta por '[!!]' y por
#  'impresora.mac' a propósito: las dos cadenas son SIN acentos, así que el
#  golden no se rompe si la salida llega transliterada. Ver §0-bis D13.)

ssh ruleta 'timedatectl show -p Timezone --value'
# America/Hermosillo
# (CORREGIDO 2026-09-11: decía America/Mexico_City. La real es
#  America/Hermosillo, elegida por el usuario en Imager. Ver §0-bis D4.)

ssh ruleta 'timedatectl show -p NTPSynchronized --value'
# yes
```

**Notas sobre estos goldens, para no leerlos mal:**

- El de `diagnostico` **NO tarda**: termina en segundos. *(Aquí decía que podía
  tardar "un par de minutos probando la conexión Bluetooth contra una MAC que no
  existe". Es falso: con la MAC toda a ceros no llega a intentar conectarse.
  Ver §0-bis D13.)*
- `python3 -m ruleta diagnostico` termina con **código de salida 1** en esta
  fase. Eso **no** invalida el golden: lo que se compara es el conteo de líneas
  `[ok]`, que debe ser 6.
- Las líneas `[ok] gpiozero` y `[ok] lgpio` salen **sin número de versión**, y
  está bien: esos módulos no exponen `__version__`. El golden es un conteo, así
  que no se ve afectado. Ficha F-051.
- El golden de `timedatectl show -p NTPSynchronized --value` es el único que
  puede quedar en `no` legítimamente: si la red del restaurante bloquea NTP, se
  anota en el acta como desviación aceptada y se resuelve con la batería RTC.
  Cualquier otro golden que no dé exactamente su valor **bloquea la fase**.
- **Ojo con la red en producción:** a partir de la decisión del usuario del
  2026-09-11 (la Pi trabaja **sin red**, §0-bis D9), estos goldens solo se
  pueden volver a correr **reconectando la Pi al Wi-Fi**. No son verificables
  con la Pi aislada.
- Si alguien agrega o quita una comprobación en `cmd_diagnostico`
  (`ruleta/__main__.py`), el `6` deja de valer: ver la §6, última fila.

---

## 8. Prohibiciones

Valen para todas las fases; se repiten aquí porque esta es la fase donde más
tienta saltárselas.

1. **Los agentes nunca teclean contraseñas ni frases de paso.** Ni de Wi-Fi, ni
   de `sudo`, ni de GitHub. Si un paso las pide, se marca "requiere al usuario".
2. **Los agentes nunca graban discos.** Imager lo maneja el usuario, siempre.
3. **No se arranca el servicio `ruleta` en esta fase.** Nada de
   `sudo systemctl start ruleta` hasta que la Fase 2 tenga impresora.
4. **No se edita `/boot/firmware/config.txt` sin visto bueno explícito del
   usuario**, y siempre con copia `.bak` antes (Paso 12).
5. **Nunca `git add .` ni `git add -A`.** Solo rutas explícitas, acordadas antes
   del commit.
6. **Nunca `apt full-upgrade` ni `apt dist-upgrade` sin visto bueno.** Puede
   cambiar el kernel y romper GPIO o Bluetooth a media semana de evento.
7. **Nunca desactivar el Wi-Fi por overlay** (`dtoverlay=disable-wifi`): en la
   Pi 5 apaga también el Bluetooth.
8. **Nunca cambiar el nombre del repositorio** ni "corregir" la URL: se llama
   `Ruelta-Aleatoria-Pi5` y así se usa.
9. **Nunca subir secretos al repositorio**: llave privada, contraseñas, SSID con
   su clave, ni la carpeta `datos/`.
10. **Nunca parchear a mano lo que un script deja a medias.** Se vuelve a correr
    el script completo, que para eso es repetible.
11. **Nunca borrar `~/.ssh/known_hosts` entero** para "arreglar" un aviso de
    huella: se usa `ssh-keygen -R <host>`.
12. **El ejecutor no commitea.** Eso es del agente de commit.

---

## 9. Siguientes fases

**Fase 2 · Impresora: USB primero, Bluetooth como respaldo.** Su plan detallado
**está por escribirse** en `docs/planes/fase-2-impresora.md`; ese archivo **aún
no existe** en el repositorio (comprobar con `ls docs/planes/`), así que por
ahora lo que sigue es todo lo que hay: el resumen de hacia dónde va.

*(Reescrito el 2026-09-11: este párrafo decía que la Fase 2 empezaba por el
emparejamiento Bluetooth. **El usuario decidió probar primero el cable USB.**
Ver §0-bis D16.)*

- **Camino principal, USB.** Se conecta la AOMU My-A1 a la Pi con su cable USB y
  se configura `"tipo": "archivo"` con `"ruta": "/dev/usb/lp0"` en
  `config.json`. Es más simple y más estable que el Bluetooth: sin
  emparejamiento, sin PIN, sin canal RFCOMM, sin que un celular le robe la
  conexión. **Lo que hay que verificar antes de darlo por bueno:** que aparezca
  `/dev/usb/lp0` al conectar la impresora, y **los permisos**: el `README.md` §9
  dice que hay que estar en el grupo `lp`, y el 2026-09-11 se midió que el
  usuario `asadero` **no** está en `lp` (sí en `lpadmin`, que no es lo mismo).
  Ficha **F-052**.
- **Camino de respaldo, Bluetooth.** Si el USB no funciona, se enciende la
  impresora y se corre `./herramientas/emparejar.sh` (que la busca, prueba los
  PIN `0000` y `1234`, la marca como confiable y escribe su MAC en
  `config.json`), y se vuelve a `"tipo": "bluetooth"`. Todo lo que la Fase 1
  dejó listo para esto sigue en pie: `bluez`, `bluez-tools`, el adaptador `hci0`
  sin bloqueos y el servicio `bluetooth` activo y habilitado.
- **En los dos casos**, después: `python3 -m ruleta probar-impresora` y, sobre el
  papel impreso, se decide la tabla de acentos (`codepage_n`, entre 0, 2, 16 y
  19), si el ancho es de 48 o 42 columnas y si el corte automático funciona o hay
  que pasar a `parcial`. También se corre ahí la **vista previa** que la Fase 1
  dejó pendiente (§0-bis D14).
- **Cierre de la Fase 2:** `python3 -m ruleta diagnostico` debe salir **sin
  ningún `[!!]`** y con código 0. Con `"tipo": "archivo"` el diagnóstico ni
  siquiera prueba Bluetooth: imprime `[--] impresora tipo 'archivo': no se
  prueba Bluetooth` y devuelve 0 si lo demás está bien.
- **Pendiente físico:** el 2026-09-11 no se pudo probar nada porque el usuario
  **no trajo el cable de corriente de la impresora**. Queda para el día
  siguiente.

**Fase 3 · Botones y LED.** Se cablea el botón JUGAR a GPIO 17, el botón
HABILITAR del mesero a GPIO 27 y el LED opcional a GPIO 22, todos contra GND.
Primero se prueba la lógica sin hardware con
`python3 -m ruleta --simular --impresora vista` (teclas `h`, `j`, `i`), y solo
después se prueba con los botones reales. Aquí se ajustan `rebote_ms`,
`modo_habilitar` y `pulsacion_larga_seg`.

**Fase 4 · Prueba general y entrega.** Se cambian los `test1`…`test7` por los
premios reales con sus pesos, stocks y topes diarios, se pone el logo definitivo,
se revisa la hora, se corre `python3 -m ruleta reiniciar --si` para dejar folio e
inventario en cero, se arranca el servicio (`sudo systemctl start ruleta`, que a
partir de ahí arranca solo al encender) y se hace una prueba completa de punta a
punta. Se cierra con la capacitación del personal: encender, leer el inventario
impreso, qué hacer si no sale el boleto y cómo liberar un folio.

---

## 10. Regla final

**Si el código real, el `README.md` o la propia Raspberry Pi contradicen este
plan, el ejecutor se detiene y pregunta; no improvisa.**
