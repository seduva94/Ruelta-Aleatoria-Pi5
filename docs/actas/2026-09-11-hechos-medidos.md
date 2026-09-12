# Hechos medidos - Fase 1 (preparar la Raspberry Pi 5)

Generado automaticamente el 2026-09-11T16:25 a partir de los informes JSON de los agentes (archivos tasks/*.output de la sesion) y de mediciones del orquestador con herramientas. Nada de este archivo viene de memoria.

## Mediciones del orquestador (PC Windows del usuario)

- Raspberry Pi Imager instalado (registro de Windows, ahora): Raspberry Pi Imager v2.0.11.1
- microSD del usuario (medido con Get-Volume/Get-Disk el 2026-09-11 antes de grabar): unidad D: FAT32 0.5 GB etiqueta 'bootfs' sobre Disk 1 'Generic Mass-Storage' USB de 28.9 GB (traia un Raspberry Pi OS previo). Imager la borro por completo.
- Cliente SSH nativo: C:/Windows/System32/OpenSSH/ssh.exe OpenSSH_for_Windows_9.5p2. Git Bash trae OpenSSH 10.3 pero monta C: con noacl (chmod no tiene efecto): los agentes usan el nativo.
- ping ruleta.local ahora: Pinging ruleta.local [fe80::2ecf:67ff:fe17:10d%20] with 32 bytes of data: Reply from fe80::2ecf:67ff:fe17:10d%20: time=1ms
- Decisiones del usuario en chat (2026-09-11): SSH con llave SOLO para instalar/probar; en produccion la Pi va SIN red (por tanto bateria RTC necesaria); autorizo sudo sin contrasena creando el mismo /etc/sudoers.d/010_asadero-nopasswd; Raspberry Pi Connect desactivado; prefiere conectar la impresora por USB (se probara manana; no trajo el cable de corriente de la impresora).

## Llave SSH (workflow ruleta-llave-ssh)

- Publica: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK2FW7iyyiVzR66kZuO+aZyJclDr9ZiDq7mWcUPgn3Zz ruleta-asadero
- Huella: 256 SHA256:sOmEM5P6LNzx7c5SOyy33NnxWOj+Qt4/RpPjwCcDSQw ruleta-asadero (ED25519)
- Rutas: C:/Users/seduv/.ssh/id_ruleta / C:/Users/seduv/.ssh/id_ruleta.pub; alias en ~/.ssh/config: True
- Verificador: correcto=True
  - nota ejecutor: No existia ~/.ssh: se creo desde cero. No se sobreescribio nada; no habia id_ruleta previo ni ~/.ssh/config previo.
  - nota ejecutor: Llave ed25519 generada sin frase de paso, comentario 'ruleta-asadero'. Verificado que la privada abre sin passphrase y que su derivada publica coincide exactamente con id_ruleta.pub (par integro).
  - nota ejecutor: La llave privada nunca fue mostrada, copiada ni transmitida. Solo se verifico su cabecera y la coincidencia del par.
  - nota ejecutor: ~/.ssh/config creado nuevo con el bloque exacto solicitado. Hay exactamente 1 linea 'Host ruleta' (sin duplicados). Validado con 'ssh -G ruleta' (resuelve config en local, NO contacta ninguna maquina): devuelve hostname=ruleta.local, user=asadero, identityfile=~/.ssh/id_ruleta, identitiesonly=yes, connecttimeout=10, serveraliveinterval=30.
  - nota ejecutor: No se ejecuto ssh contra ninguna maquina. No se toco el repositorio del proyecto ni git.
  - nota ejecutor: ATENCION (unico riesgo abierto): los chmod se ejecutaron con exito pero NO tuvieron efecto real. Git Bash monta C: con la opcion 'noacl' (ver /etc/fstab), asi que la capa POSIX reporta 644/755 de forma fija y chmod es un no-op. 'stat' muestra .ssh=755, id_ruleta=644, id_ruleta.pub=644, config=644.
  - nota ejecutor: Lo bueno: a nivel Windows, que es lo que de verdad se aplica, los permisos SI son correctos. 'icacls' sobre id_ruleta muestra solo SYSTEM, BUILTIN\Administrators y DUVA_LAP\seduv con control total. No hay acceso para 'Users' ni 'Everyone'. La llave privada NO esta expuesta a otros usuarios de la PC.
  - nota ejecutor: Consecuencia practica a verificar en la primera conexion real: hay DOS ssh en el PATH. El de Git Bash (/usr/bin/ssh, OpenSSH_10.3p1) usa los modos POSIX emulados y su binario SI contiene el chequeo estricto ('UNPROTECTED PRIVATE KEY FILE' / 'are too open'), por lo que podria rechazar la llave al verla como 0644. El nativo de Windows (C:/Windows/System32/OpenSSH/ssh.exe, OpenSSH_for_Windows_9.5p2) usa las ACL de NTFS, que ya verificamos correctas.
  - nota ejecutor: Recomendacion: que los agentes usen el ssh NATIVO de Windows (C:/Windows/System32/OpenSSH/ssh.exe) para la conexion no interactiva, que es el camino que ya tiene permisos validos. Si se prefiere el ssh de Git Bash y este llegara a rechazar la llave por permisos, la solucion es agregar la opcion 'acl' al montaje de C: en /etc/fstab de Git for Windows. NO hice ese cambio porque es configuracion persistente y global del entorno, fuera del alcance de esta tarea: requiere tu visto bueno explicito.
  - nota ejecutor: 'HostName ruleta.local' depende de resolucion mDNS. Windows 11 la soporta, pero si la Raspberry no responde por .local habra que sustituirlo por su IP fija en el bloque Host ruleta.
  - nota ejecutor: Reversion completa si hace falta: borrar C:/Users/seduv/.ssh/id_ruleta, C:/Users/seduv/.ssh/id_ruleta.pub y C:/Users/seduv/.ssh/config (este ultimo fue creado por mi y no contenia nada previo).
  - nota ejecutor: Siguiente paso pendiente (no ejecutado, requiere la Raspberry encendida): instalar la llave publica de arriba en /home/asadero/.ssh/authorized_keys de la Pi.

## Primer acceso a la Pi (workflow ruleta-fase1-primer-acceso)

- comando_ssh_que_funciono: /c/Windows/System32/OpenSSH/ssh.exe -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 ruleta <comando>   -- Funciono al PRIMER intento (paso 1, sin variantes). No hizo falta -4, ni -i con la llave explicita, ni la IPv6 literal. Resolvio ruleta.local a la IPv4 192.168.50.178. La primera conexion agrego la huella ED25519 a known_hosts. Nunca pidio contrasena (la llave id_ruleta y el Host "ruleta" del ~/.ssh/config funcionan bien).
- hostname: ruleta
- ip: 192.168.50.178 (wlan0, DHCP dinamico, /24, brd 192.168.50.255; tambien accesible como ruleta.local por mDNS)
- modelo: Raspberry Pi 5 Model B Rev 1.0
- arquitectura: aarch64
- codename: trixie (VERSION_ID=13, Debian 13 / Raspberry Pi OS Lite 64-bit; kernel 6.18.34+rpt-rpi-2712)
- python: Python 3.13.5
- grupos: asadero adm dialout cdrom sudo audio video plugdev games users netdev gpio i2c spi render input lpadmin
- sudo_sin_contrasena: False
- bluetooth: OK, no esta bloqueado. Adaptador hci0 presente: Soft blocked: no, Hard blocked: no. bluetoothctl show -> Name: ruleta, Powered: yes. Servicio bluetooth: active y enabled. MATIZ IMPORTANTE: el binario rfkill vive en /usr/sbin y /usr/sbin NO esta en el PATH de una sesion ssh no interactiva (PATH=/usr/local/bin:/usr/bin:/bin:/usr/games), por eso 'rfkill list bluetooth' dio "command not found" en el primer script; con la ruta absoluta /usr/sbin/rfkill funciono perfecto. El paquete rfkill SI esta instalado.
- internet: True
- hora: Local time: Fri 2026-09-11 16:03:34 MST | Time zone: America/Hermosillo (MST, -0700) | System clock synchronized: yes
- throttled: 0x0
- paquetes_presentes: ['bluez', 'python3-gpiozero', 'python3-lgpio', 'rfkill']
- paquetes_faltantes: ['git', 'python3-pil', 'bluez-tools']
  - problema/observacion: BLOQUEANTE: sudo pide contrasena. 'sudo -n true' devolvio SUDO_PIDE_CONTRASENA y 'sudo -n -l' respondio 'sudo: a password is required'. El usuario asadero SI esta en el grupo sudo, pero NO existe el archivo NOPASSWD tipico de Raspberry Pi OS: /etc/sudoers.d/ solo contiene 010_at-export, 010_dpkg-threads, 010_global-tty, 010_proxy y README (falta 010_pi-nopasswd o equivalente). Consecuencia: ningun paso automatizado por SSH que requiera root (apt install, systemctl enable, escribir en /etc, reglas udev) podra correr solo; el usuario tendra que teclear la contrasena, o autorizar explicitamente crear una regla NOPASSWD.
  - problema/observacion: git NO esta instalado en la Pi. dpkg-query reporta 'git unknown ok not-installed' y 'command -v git' no encuentra nada. Hara falta instalarlo (apt install git) para clonar o desplegar el proyecto en la Pi; requiere sudo, que como se indica arriba pide contrasena.
  - problema/observacion: python3-pil (Pillow) FALTA. Es esperado en Raspberry Pi OS Lite, pero es necesario para generar las imagenes/tickets que se mandan a la impresora Bluetooth AOMU My-A1, asi que habra que instalarlo (paquete python3-pil o pip dentro de un venv).
  - problema/observacion: bluez-tools FALTA. Esperado en Lite. Conviene instalarlo si se quiere emparejar y administrar la impresora Bluetooth por linea de comandos con bt-device/bt-adapter; bluetoothctl por si solo podria bastar.
  - problema/observacion: TRAMPA A DOCUMENTAR: el PATH de SSH no interactivo no incluye /usr/sbin ni /sbin (PATH=/usr/local/bin:/usr/bin:/bin:/usr/games). Cualquier script lanzado por SSH que llame a rfkill, shutdown, iw, etc., debe usar ruta absoluta o exportar el PATH; si no, falla con 'command not found' aunque el paquete este instalado. No es una falla de la Pi.
  - problema/observacion: La IP 192.168.50.178 es DHCP dinamica sobre wlan0 (WiFi). Para un evento de una semana conviene fijarla (reserva DHCP en el router o IP estatica) para que el acceso SSH y el kiosco no se rompan si el router reasigna direcciones. ruleta.local por mDNS funciono, pero mDNS no siempre es confiable desde todos los dispositivos.
  - problema/observacion: SIN PROBLEMA, solo para constancia de lo verificado: codename trixie (correcto), arquitectura aarch64 (correcta), Python 3.13.5 (correcto), internet OK (DNS resolvio github.com a 140.82.112.3 y curl devolvio HTTP/2 200), throttled=0x0 (alimentacion correcta, sin bajo voltaje ni limitacion termica), temperatura 44.6 C (44650 milideg, fria), disco / con 23G libres de 28G (15% usado), RAM 4049 MB totales con 3653 MB libres, reloj sincronizado en America/Hermosillo. El usuario asadero ya pertenece a los grupos gpio, i2c, spi, dialout, video e input, asi que el boton arcade por GPIO no necesitara permisos extra.
- Verificador: acceso_correcto=True
  - Todas las comprobaciones coinciden con lo afirmado por el ejecutor: hostname=ruleta, VERSION_CODENAME=trixie, uname -m=aarch64, python3=Python 3.13.5, whoami=asadero.
  - sudo -n true devolvió código de salida 1 con mensaje 'sudo: a password is required' -> confirma que sudo SIN contraseña = false, tal como afirmó el ejecutor.
  - getent hosts deb.debian.org devolvió registros IPv6 válidos y se imprimió DNS_OK -> confirma que hay internet, tal como afirmó el ejecutor.
  - No se detectó ninguna discrepancia entre lo afirmado y lo medido.
  - El acceso SSH con el alias 'ruleta' (BatchMode=yes, StrictHostKeyChecking=accept-new, ConnectTimeout=15) funcionó sin pedir contraseña en las 7 conexiones separadas, confirmando que la llave y el Host 'ruleta' en ~/.ssh/config están correctamente configurados.

### Salida cruda del script remoto
```
########## COMANDO DE CONEXION INICIAL (paso 1, exitoso al primer intento) ##########
$ /c/Windows/System32/OpenSSH/ssh.exe -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15 ruleta hostname
Warning: Permanently added 'ruleta.local' (ED25519) to the list of known hosts.
ruleta
EXIT_CODE=0

########## SCRIPT 1 (medicion principal, solo lectura) ##########
=== HOSTNAME ===
ruleta
=== HOSTNAME_I ===
192.168.50.178 
=== MODEL ===
Raspberry Pi 5 Model B Rev 1.0 
=== ARCH ===
aarch64
=== KERNEL ===
6.18.34+rpt-rpi-2712
=== OS_RELEASE ===
VERSION_ID="13"
VERSION_CODENAME=trixie
=== PYTHON ===
Python 3.13.5
=== GRUPOS ===
asadero adm dialout cdrom sudo audio video plugdev games users netdev gpio i2c spi render input lpadmin
=== SUDO ===
SUDO_PIDE_CONTRASENA
=== RFKILL_BT ===
bash: line 10: rfkill: command not found
=== BLUETOOTHCTL ===
	Name: ruleta
	Powered: yes
=== TIMEDATECTL ===
               Local time: Fri 2026-09-11 16:03:34 MST
                Time zone: America/Hermosillo (MST, -0700)
System clock synchronized: yes
=== DISCO ===
/dev/mmcblk0p2   28G  3.9G   23G  15% /
=== RAM ===
Mem:            4049         220        3653          12         243        3828
=== THROTTLED ===
throttled=0x0
=== TEMP ===
44650
=== IP4 ===
    inet 127.0.0.1/8 scope host lo
    inet 192.168.50.178/24 brd 192.168.50.255 scope global dynamic noprefixroute wlan0
=== DNS ===
140.82.112.3    github.com
DNS_OK
=== CURL ===
HTTP/2 200 
=== PAQUETES ===
dpkg-query: no packages found matching python3-pil
dpkg-query: no packages found matching bluez-tools
bluez install ok installed
git unknown ok not-installed
python3-gpiozero install ok installed
python3-lgpio install ok installed
rfkill install ok installed
=== FIN ===
EXIT_CODE=0

########## SCRIPT 2 (seguimiento solo lectura: rfkill con ruta absoluta, git, sudo, servicio BT) ##########
=== RFKILL_FULLPATH ===
0: hci0: Bluetooth
	Soft blocked: no
	Hard blocked: no
=== RFKILL_ALL ===
0: hci0: Bluetooth
	Soft blocked: no
	Hard blocked: no
1: phy0: Wireless LAN
	Soft blocked: no
	Hard blocked: no
=== WHICH_GIT ===
GIT_NO_ENCONTRADO
=== SUDOERS_D ===
total 28
drwxr-xr-x  2 root root 4096 Jun 17 17:21 .
drwxr-xr-x 93 root root 4096 Sep 11 15:57 ..
-r--r-----  1 root root   36 Apr 29  2019 010_at-export
-r--r-----  1 root root   44 Jun 19  2024 010_dpkg-threads
-r--r-----  1 root root   31 Jul 25  2023 010_global-tty
-r--r-----  1 root root  211 Mar 18  2022 010_proxy
-r--r-----  1 root root 1068 Apr 11 05:21 README
=== SUDO_N_DETALLE ===
sudo: a password is required
=== BT_SERVICE ===
active
enabled
=== PATH_NOINTERACTIVO ===
/usr/local/bin:/usr/bin:/bin:/usr/games
=== FIN2 ===
EXIT_CODE=0
```

## Instalacion en la Pi (workflow ruleta-fase1-instalacion)

- sudo sin contrasena verificado: True (regla /etc/sudoers.d/010_asadero-nopasswd)
  - 1. sudo -n true; echo EXIT=$? -> EXIT=0 (coincide)
  - 2. sudo -n cat /etc/sudoers.d/010_asadero-nopasswd -> "asadero ALL=(ALL) NOPASSWD: ALL" (coincide exactamente)
  - 3. sudo -n visudo -c -> incluye la linea "/etc/sudoers.d/010_asadero-nopasswd: parsed OK" (coincide); tambien se listan otros archivos de sudoers.d ya existentes, todos parsed OK, sin errores
  - 4. sudo -n stat -c "%a %U" /etc/sudoers.d/010_asadero-nopasswd -> "440 root" (coincide exactamente)
  - Los 4 chequeos coinciden con lo esperado por el usuario: sudo sin contrasena funciona correctamente para el usuario asadero via la regla 010_asadero-nopasswd
- ok: True
- paquetes_instalados: ['git 1:2.47.3-0+deb13u1', 'python3-pil 11.1.0-5+deb13u4', 'bluez-tools 2.0~20170911.0.7cb788c-4+b2', '(el instalador ademas actualizo 14 paquetes de sistema ya presentes: bsdextrautils, bsdutils, eject, fdisk, libblkid1, libfdisk1, liblastlog2-2, libmount1, libsmartcols1, libuuid1, login, mount, rfkill, util-linux -> 2.41.5-0+deb13u1)']
- hash_clonado: 2052e4700c53f274a2b2f28ff0d7df62d519ffa8
- instalador_exit: 0
- servicio: enabled / inactive (habilitado para arrancar solo al encender la Pi, y NO iniciado, tal como se pidio). Unidad: User=asadero, WorkingDirectory=/home/asadero/ruleta, ExecStart=/usr/bin/python3 -m ruleta, Environment=GPIOZERO_PIN_FACTORY=lgpio / PYTHONUNBUFFERED=1 / PYTHONIOENCODING=utf-8
- pasos:
  - 1. apt-get update -> EXIT=0. Cola del log: 'Fetched 27.0 MB in 3s (7,842 kB/s)' / 'Reading package lists...'. Log en la Pi: /home/asadero/apt-update.log
  - 2. apt-get install -y git python3-pil bluez-tools -> EXIT=0 (ultima linea: 'Processing triggers for libc-bin (2.41-12+rpt1+deb13u3)'). dpkg-query confirma: 'bluez-tools 2.0~20170911.0.7cb788c-4+b2 install ok installed', 'git 1:2.47.3-0+deb13u1 install ok installed', 'python3-pil 11.1.0-5+deb13u4 install ok installed'. Log: /home/asadero/apt-install.log
  - 3. test -e ~/ruleta -> LIBRE (la carpeta no existia, se podia clonar)
  - 4. git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git ~/ruleta -> EXIT=0 ('Cloning into /home/asadero/ruleta...'). HEAD = 2052e4700c53f274a2b2f28ff0d7df62d519ffa8, rama = main. Log: /home/asadero/clone.log
  - 5. chmod +x -> /home/asadero/ruleta/instalar.sh queda -rwxrwxr-x y /home/asadero/ruleta/herramientas/emparejar.sh queda -rwxrwxr-x (es el unico .sh en herramientas/)
  - 6. sudo ./instalar.sh -> instalador_exit=0. El log recorre '== 1/6 Paquetes del sistema' (apt actualizo 14 paquetes de util-linux/rfkill, 0 nuevos, 0 eliminados), '== 2/6 Grupos del usuario', '== 3/6 Bluetooth encendido y habilitado al arranque', '== 4/6 Regla udev para el chip GPIO de la Pi 5', '== 5/6 Carpeta de datos y permisos', '== 6/6 Servicio systemd' con 'Created symlink /etc/systemd/system/multi-user.target.wants/ruleta.service -> /etc/systemd/system/ruleta.service' y el mensaje literal "Servicio 'ruleta' habilitado (arranca solo al encender). Aun NO se inicio.". Termina con el diagnostico y el unico [!!] esperado (MAC de impresora). Log completo: /home/asadero/instalar.log
  - 7a. systemctl is-enabled/is-active ruleta -> 'enabled' e 'inactive'. El servicio NO fue iniciado, como se pidio. (El comando ssh devuelve codigo 3 porque asi responde 'systemctl is-active' ante un servicio inactivo; es el resultado esperado, no un fallo)
  - 7b. Unidad /etc/systemd/system/ruleta.service -> User=asadero, WorkingDirectory=/home/asadero/ruleta, ExecStart=/usr/bin/python3 -m ruleta, mas Environment=GPIOZERO_PIN_FACTORY=lgpio, Environment=PYTHONUNBUFFERED=1, Environment=PYTHONIOENCODING=utf-8. Todo correcto
  - 7c. La regla /etc/udev/rules.d/60-ruleta-rp1-gpiochip4.rules existe con el contenido: SUBSYSTEM=="gpio", KERNEL=="gpiochip*", DRIVERS=="pinctrl-rp1", SYMLINK+="gpiochip4". En /dev estan gpiochip0, 10, 11, 12, 13 (crw-rw---- root gpio) y gpiochip4 existe como enlace simbolico -> gpiochip0. Correcto
  - 7d. id -nG asadero -> asadero adm dialout cdrom sudo audio video plugdev games users input render netdev bluetooth spi i2c gpio lpadmin. Incluye gpio
  - 7e. python3 -m unittest discover -s tests -t . -> 'Ran 141 tests in 0.238s' y 'OK' (sin fallos ni skips)
  - 7f. python3 -m ruleta diagnostico -> EXIT=1, con [ok] en carpeta de datos escribible, PIL 11.1.0, gpiozero, lgpio, logo /home/asadero/ruleta/logo.png e inventario folio 00000; el unico [!!] es la MAC Bluetooth faltante, que es lo esperado para la Fase 2
  - 7g. Versiones de librerias: el comando textual del paso fallo con 'AttributeError: module gpiozero has no attribute __version__' porque este build de gpiozero no expone __version__; los tres import (PIL, gpiozero, lgpio) SI funcionaron. Re-consultado con importlib.metadata: PIL 11.1.0, gpiozero 2.0.1, lgpio 0.2.2.0. Es el mismo motivo por el que el diagnostico imprime '[ok] gpiozero' y '[ok] lgpio' con la version en blanco: detalle cosmetico, no un fallo de instalacion
  - 7h. ~/ruleta/datos existe (drwxr-xr-x asadero asadero) con estado.json (134 bytes) y ruleta.log (0 bytes), ambos asadero:asadero. stat -> 'asadero /home/asadero/ruleta' y 'asadero /home/asadero/ruleta/config.json'. Dueno correcto
- requiere_al_usuario: Nada bloquea la Fase 1: quedo todo instalado y verificado. Para la Fase 2, en la Pi como usuario asadero dentro de /home/asadero/ruleta: 1) encender la impresora AOMU My-A1 y correr ./herramientas/emparejar.sh para emparejarla y guardar su MAC en impresora.mac de config.json; 2) python3 -m ruleta probar-impresora para el boleto de prueba y elegir la tabla de acentos; 3) python3 -m ruleta vista-previa --todos para revisar los boletos sin gastar papel; 4) poner los premios reales en config.json y dejar el inventario en cero con python3 -m ruleta reiniciar --si; 5) arrancar con sudo systemctl start ruleta. Yo no inicie el servicio, no toque config.json y no corri reiniciar ni liberar, como se me indico. Nota: el usuario asadero ya pertenecia al grupo gpio, asi que no hace falta cerrar y volver a abrir sesion.
- pruebas en la Pi:
```
----------------------------------------------------------------------
Ran 141 tests in 0.238s

OK
```
- diagnostico en la Pi:
```
Ruleta v1.0.0 | Python 3.13.5 | linux
Configuracion: /home/asadero/ruleta/config.json
Carpeta de datos: /home/asadero/ruleta/datos
  [ok] la carpeta de datos se puede escribir
  [ok] PIL 11.1.0
  [ok] gpiozero 
  [ok] lgpio 
  [ok] logo: /home/asadero/ruleta/logo.png
  [ok] inventario: folio 00000
  [!!] Falta la direccion Bluetooth de la impresora: pon la MAC real en impresora.mac de config.json (la obtienes con herramientas/emparejar.sh)
EXIT=1

(El unico [!!] es el esperado por la MAC pendiente de la Fase 2. Las versiones en blanco de gpiozero y lgpio son cosmeticas: esos modulos no exponen __version__; las versiones reales son gpiozero 2.0.1 y lgpio 0.2.2.0)
```
- Verificador: instalacion_correcta=True
  - Discrepancia menor en comprobación 2: 'git status --porcelain | wc -l' da 2, no 0 como esperaba el guion (no es un 'clon limpio' al 100%). El diff son solo cambios de permisos (chmod 644->755) en instalar.sh y herramientas/emparejar.sh, aplicados después del clon para dejarlos ejecutables (esto es justamente lo que exige la comprobación 8, que sí pasa como X_OK). No hay cambios de contenido, solo de modo de archivo. El resto del afirmado (hash local 2052e4700c53f274a2b2f28ff0d7df62d519ffa8 y coincidencia con origin/main) sí se confirmó exactamente igual.
  - Todo lo demás coincide exactamente con lo esperado: paquetes dpkg (git, python3-pil, bluez-tools, python3-gpiozero, python3-lgpio, bluez) 'install ok installed'; servicio 'enabled'/'inactive'; unidad systemd con User=asadero (1), WorkingDirectory=/home/asadero/ruleta (1), y contenido completo coincide con lo declarado (lgpio, PYTHONUNBUFFERED, PYTHONIOENCODING, ExecStart); regla udev 60-ruleta-rp1-gpiochip4.rules presente y /dev/gpiochip4 existe (symlink a gpiochip0); 141 tests pasan con 'OK'; diagnóstico muestra exactamente los 6 [ok] esperados (carpeta de datos, PIL, gpiozero, lgpio, logo, inventario) y exactamente un [!!] sobre la MAC de la impresora Bluetooth; instalar.sh y herramientas/emparejar.sh son ejecutables (X_OK).

## Git y GitHub (workflows de commit y verificacion)

- commit inicial: {"ok": true, "hash": "9e8b9e87e5cb9ee98db0ca81f722263b1717a942", "rama": "main"}
- push inicial: {"ok": true, "hash_remoto": "9e8b9e87e5cb9ee98db0ca81f722263b1717a942"}
- verificacion push inicial: {"hash_remoto": "9e8b9e87e5cb9ee98db0ca81f722263b1717a942", "push_correcto": false}
- commit docs CLAUDE.md: commit 2052e4700c53f274a2b2f28ff0d7df62d519ffa8 push=True; verificador push_correcto=True
- plan fase 1: ejecutor ok=True archivos=['C:/Users/seduv/Desktop/Ruleta Asadero/docs/planes/fase-1-preparar-pi.md', 'C:/Users/seduv/Desktop/Ruleta Asadero/docs/fichas.md']; rondas de lentes=2; esceptico correcciones=3 residuales=12; commit 0464f5aad3e94be158f8eeee9b4c8a232267da14 push=True archivos=['docs/planes/fase-1-preparar-pi.md', 'docs/fichas.md']; verificador push_correcto=False (unico hallazgo: el grep de 'bitacora' sin acento del verificador no encontro 'Bitácora'; falso negativo del guion, no del documento)
  - duda del ejecutor: Contradiccion real: README.md seccion 4 paso 1 manda copiar con scp -r "Ruleta Asadero" usuario@ruleta.local:~/ruleta, mientras la decision cerrada 6 instala con git clone. No toque el README (fuera de mi alcance) y lo deje como ficha F-001 con la correccion propuesta. Hace falta visto bueno del usuario para reescribir ese paso.
  - duda del ejecutor: README.md seccion 3 dice "activa SSH" y ssh usuario@ruleta.local, sin mencionar el usuario asadero ni la opcion "Allow public-key authentication only" de Imager (ficha F-002). README seccion 4 paso 7 propone sudo timedatectl set-ntp false, que solo aplica sin internet, mientras la Fase 1 deja NTP encendido (ficha F-003). Ambas pendientes de visto bueno.
  - duda del ejecutor: La Fase 1 instala por git clone, asi que depende de que los 2 commits locales esten publicados en https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git. No puedo ejecutar git para comprobarlo. El plan mitiga esto verificando el contenido del clon en el Paso 8 y ordenando detenerse si faltan archivos, pero conviene que un verificador de solo lectura confirme el HEAD remoto antes de arrancar la fase (ficha F-005).
  - duda del ejecutor: Raspberry Pi Imager solo configura zona horaria y teclado, no el idioma completo del sistema: es_MX.UTF-8 no se puede fijar desde Imager. Lo resolvi con un Paso 13 opcional en la Pi (raspi-config nonint do_change_locale, con camino manual de respaldo) y advertencia de que traduce la salida de varios comandos. Confirmar si el usuario lo quiere o si prefiere dejar el sistema en ingles, que no afecta al programa.
  - duda del ejecutor: No pude confirmar si Raspberry Pi OS Lite Trixie trae git preinstalado. El Paso 8 lo comprueba con command -v git y, si falta, lo instala con apt; si sudo pidiera contrasena ese subpaso queda marcado "requiere al usuario". Si resulta que no viene, conviene que el usuario lo sepa de antemano.

## Driver Linux del fabricante (medido el 2026-09-11 por el orquestador, sin ejecutar nada)

Fuente: C:/Users/seduv/Downloads/Linux Driver/Linux Driver/ (descargado por el usuario de la pagina del fabricante). Contiene 4 instaladores: linux32bit/install58, linux32bit/install80, linux64bit/install58, linux64bit/install80 (2015-04-26, 24-34 KB). Son scripts POSIX sh con un tar.gz incrustado (offset gzip 3838 en install80 de 64 bits). Se desempaco en el scratchpad (driver80/extraido) SIN ejecutar el instalador.

Hechos:
- Cabecera del script: "Shenzhen ZiJiang Electronics Co..Ltd", "Models included: POS80 / POS58"; instala un filtro CUPS (bin/rastertozj, ELF x86-64; y rastertozj58) y PPDs en usr/share/cups/model/zjiang. Los binarios son x86 (32/64 bits): NO sirven en la Raspberry (aarch64). El driver del fabricante no se puede usar en la Pi; el programa habla ESC/POS directo, que es lo previsto.
- PPD del modelo de 80 mm (ppd/POS80.ppd): Manufacturer "Zijiang", Product "(zj-80250)", ModelName "ZJ-80250", NickName "POS-80250", 1284DeviceID "MFG:Zijiang;CMD:Zijiang;MDL:ZJ-80250;CLS:PRINTER;". Es decir, la AOMU My-A1 es una Zjiang ZJ-80250 (familia POS-80, 250 mm/s), como suponia la investigacion. La clase USB es PRINTER (CLS:PRINTER): en Linux el driver usblp deberia reclamarla y crear /dev/usb/lp0; el ieee1284_id de sysfs deberia mostrar ese texto.
- Resolucion 203 dpi (HWResolution[203 203]); anchos de pagina 80 mm; area imprimible definida en puntos PostScript.
- Opciones del dispositivo en el PPD (confirman hardware): Cutting (No cutting / Cut at the end of page / Cut at the end of document; por defecto corta al final de pagina) -> tiene cortador; Beeper (No beeping / after every page / before every page / after document / before document; por defecto "Beep before every page") -> tiene zumbador, asi que ESC B deberia sonar (config "beep": true es viable); NV Logo 1-8 (logos guardados en memoria de la impresora, no lo usamos); Cash Drawer #1/#2 (pulso ESC p; no aplica); FeedDist 3-45 mm (por defecto 30 mm) -> la distancia cabezal-cuchilla la maneja el driver con avance configurable; BlankSpace.
- El filtro rastertozj construye los comandos en codigo (funciones cutPaper, ejectCashDrawer, beeperSetting, feedDistSetting, cuttingSetting, NVLogo); solo aparecen como bytes contiguos ESC @ (1B 40), ESC d (1B 64) y DLE EOT 1 (10 04 01) -> el driver del fabricante usa DLE EOT 1 (estado en tiempo real), lo que respalda que la impresora responde a DLE EOT (nuestra consulta de papel).
- No hay VID:PID USB en el paquete (CUPS lo descubre por su backend usb). Se medira en la Pi con lsusb / udevadm.
- Los PPD del modelo de 58 mm (POS58 / ZJ-58, filtro rastertozj58) no aplican.

## Noche del 2026-09-11 (misma fecha; el usuario volvio desde otra ubicacion) - ejecucion adelantada de la Fase 2

Medido por agentes (workflows ruleta-fase2-deteccion-usb, ruleta-fase2-permisos-y-prueba, ruleta-fase2-boleto-prueba) y por el orquestador; fotos del papel enviadas por el usuario.

- Red: la Pi solo conocia el Wi-Fi del asadero. Solucion adoptada y funcionando: Punto de acceso movil de Windows en la laptop con el MISMO SSID y contrasena (2.4 GHz). La Pi se conecto sola: 192.168.137.95/24 (PC 192.168.137.1), ruleta.local resuelve, internet via la PC (DNS_OK, HTTP/2 200), sudo -n OK. nmcli muestra la conexion "netplan-wlan0-SDV 5G". La laptop no tiene Ethernet ni WSL; no es posible editar el Wi-Fi en la SD desde Windows.
- Impresora por USB (puerto USB 3.0 azul): lsusb "Bus 001 Device 002: ID 0418:5011 AST Research USB Printer Port"; cadenas USB iManufacturer "USB Print", iProduct "USB Printer Port", iSerial 1A6766D50000; clase 7 Printer, subclase 1, protocolo 2 (bidireccional), EP 0x81 IN y 0x01 OUT de 64 bytes; full-speed 12 Mbps; driver usblp; nodo /dev/usb/lp0 crw-rw---- root:lp 180,0; ieee1284_id "MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1" (NO el ID Zijiang del PPD del driver). udevadm no expone ID_VENDOR para usbmisc (la regla usa ATTRS). El grupo lp existia vacio; asadero NO estaba en lp -> NO_ESCRIBIBLE.
- Permisos aplicados A MANO en la Pi (pendiente incorporar a instalar.sh por la cadena): /etc/udev/rules.d/61-ruleta-impresora-usb.rules con la linea exacta: SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*", ATTRS{idVendor}=="0418", ATTRS{idProduct}=="5011", MODE="0660", GROUP="lp", SYMLINK+="ruleta-impresora"  (md5 2c2c308ba8f3b9683663e1dc93cd9983). usermod -aG lp asadero (getent group lp -> lp:x:7:asadero). udevadm reload + trigger: /dev/ruleta-impresora -> usb/lp0 creado a la primera; test -w /dev/usb/lp0 -> ESCRIBIBLE. Verificado por agente independiente.
- config.json EN LA PI (no en el repo): impresora.tipo = "archivo", impresora.ruta = "/dev/ruleta-impresora"; respaldo ~/ruleta/config.json.bak-2026-09-12 (nombre con fecha equivocada: era 09-11). diagnostico -> EXIT=0 sin [!!] ("[--] impresora tipo 'archivo': no se prueba Bluetooth"). En el clon de la Pi, git status muestra M config.json, ?? config.json.bak-2026-09-12 y M instalar.sh / M herramientas/emparejar.sh (solo modo, por el chmod; el repo ya trae 100755 desde 601c4c2 y se resolvera con git checkout -- de esos dos y git pull).
- HALLAZGO: al encender la Pi en la nueva ubicacion el servicio ruleta arranco solo (enabled) y quedo en bucle de reinicios (restart counter 118, RestartSec=3, StartLimitIntervalSec=0) porque la config era Bluetooth con MAC 00:00:00:00:00:00 (crear_impresora lanza ErrorConfig y el proceso sale con 2). Ayer los agentes lo vieron "inactive" por caer entre reinicios. Al cambiar la config a USB arranco estable (active desde 19:22:22 MST) e IMPRIMIO el inventario de arranque por USB. Boton GPIO sin cablear: pull-up interno, sin pulsaciones.
- Boleto de INVENTARIO impreso (foto del usuario, 19:22): acentos correctos (Dia operativo, Ultimo folio), tabla y columnas alineadas, guiones llenan 48 columnas, corte automatico limpio.
- Servicio detenido por el ejecutor (sudo systemctl stop ruleta) para imprimir la prueba; queda inactive.
- Boleto de PRUEBA impreso (foto del usuario, 19:25): ESC t 2 (cp850) y ESC t 19 (cp858) correctos con mayusculas acentuadas; ESC t 0 (cp437) sin mayusculas acentuadas (transliteradas); ESC t 16 imprime basura (la tabla 16 de esta impresora NO es CP1252). Configurado codepage_n=19 (cp858): CORRECTO, no se cambia. Regla de ancho: 48 digitos llenan la linea exacta. Tamanos 1x-4x y negrita correctos. Logo provisional nitido y centrado. Corte automatico (GS V 66 0) funciona. Cosmetico: las lineas de acentos del boleto de prueba superan 48 caracteres y se parten (ficha).
- Pendiente de esta noche: prueba del zumbador (ESC B) por USB; sincronizar config.json final (tipo archivo, ruta /dev/ruleta-impresora) al repo por la cadena; sub-fase 2b (udev en instalar.sh, diagnostico para tipo archivo y versiones, README USB, consulta de papel por USB o documentar su ausencia, cosmetico del boleto de prueba); Fase 3 botones.
- Zumbador (probado por USB con el servicio detenido, ~19:30): ESC B 3 3 -> el usuario oyo un pitido; ESC @ + ESC B 5 8, pausa 6 s, ESC B 2 8 -> el usuario oyo exactamente DOS pitidos cortos en total. Conclusion: la impresora tiene zumbador y responde a ESC B, pero emite UN pitido corto por comando e ignora los parametros n (cantidad) y t (duracion). Para dos pitidos hay que enviar dos comandos. Decision pendiente del usuario: activar "beep": true (un pitido corto por boleto).
