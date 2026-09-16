# Ruleta de premios · Asadero 33

Un botón arcade conectado a una Raspberry Pi 5. El cliente lo presiona, el
programa sortea un premio según las probabilidades e inventario configurados,
y una impresora térmica conectada por cable USB imprime el boleto con el logo,
el premio en letras grandes y el número de boleto. No hay pantalla: la
retroalimentación es el boleto, un LED opcional y el log.

```
  mesero mantiene HABILITAR ──┐
                              ├──> sorteo ──> boleto impreso y cortado ──> espera 5 s ──> listo
  cliente presiona JUGAR ─────┘
```

Todo el texto (config, boletos, mensajes, comandos) está en español.

---

## 1. Qué necesitas

| Pieza | Detalle |
|---|---|
| Raspberry Pi 5 | con fuente oficial de 27 W y microSD de 16 GB o más |
| Batería RTC (**no se va a poner**) | "RTC Battery for Raspberry Pi 5" (Panasonic ML-2020, conector J5 junto al USB-C). Sin ella, tras un corte de luz y sin internet la hora de los boletos saldrá mal. *(Esta fila decía «recomendada». **El 2026-09-15 el usuario decidió no comprarla**: la Pi irá con el internet del asadero, que es lo que le pone la hora al encender. **No hace falta que compres nada aquí**; lo que sí hay que hacer está en la §2: encender la Pi unos minutos antes de abrir y mirar la fecha del boleto de inventario. Ficha **F-241**.)* |
| Impresora | AOMU My-A1 (familia POS-80), 80 mm, con cortador automático y zumbador. Va por **cable USB**; el Bluetooth queda de respaldo. Rollos térmicos de 80 mm |
| Botón JUGAR | botón arcade (cualquier botón normalmente abierto sirve) |
| Botón HABILITAR | pulsador para el mesero; se mantiene presionado mientras el cliente juega |
| LED (opcional) | LED normal + resistencia de 330 Ω, o el LED del propio botón arcade (ver nota) |
| Cables | el cable USB A-B de la impresora, dupont hembra para el header de la Pi y terminales para los botones |

---

## 2. Conexión eléctrica

Los botones van **entre el pin GPIO y tierra (GND)**. No hace falta resistencia:
el programa activa las resistencias pull-up internas de la Pi. Presionado = 0 V.

**Hay un dibujo de todo esto:** `docs/cableado-botones.svg`. Ábrelo con doble
clic —se ve en cualquier navegador y se puede imprimir—. Enseña la Pi vista
desde arriba, qué cable va a qué pin y qué no hay que conectar nunca.

| Función | GPIO (BCM) | Pin físico | El otro cable a |
|---|---|---|---|
| Botón JUGAR | GPIO 17 | pin 11 | GND (pin 9) |
| Botón HABILITAR | GPIO 27 | pin 13 | GND (**pin 25** en la Pi del asadero; sirve cualquier GND) |
| LED (opcional) | GPIO 22 | pin 15 | resistencia 330 Ω → LED → GND |

```
        header de 40 pines (vista desde arriba, USB hacia abajo)
   3V3  (1) (2)  5V
 GPIO2  (3) (4)  5V
 GPIO3  (5) (6)  GND
 GPIO4  (7) (8)  GPIO14
   GND  (9) (10) GPIO15      <-- GND para los botones
GPIO17 (11) (12) GPIO18      <-- JUGAR
GPIO27 (13) (14) GND         <-- HABILITAR
GPIO22 (15) (16) GPIO23      <-- LED
```

Los pines se cambian en `config.json` → sección `gpio`. Evita GPIO 0-3, 7-11,
14, 15 y 18-21 (tienen funciones especiales). Alternativas limpias: 23, 24, 25, 5, 6, 16, 26.

**Así quedó cableado de verdad** (2026-09-15, medido con los botones puestos):
JUGAR con el contacto **NO al pin 11** y el **COM al pin 9 (GND)**; HABILITAR con
la **señal al pin 13** y el otro cable al **pin 25 (GND)**. Los ocho pines de
tierra (6, 9, 14, 20, 25, 30, 34 y 39) son intercambiables: si un cable no llega
al 9, se usa el 25 y no pasa nada —pero **mueve cualquier cable con la Pi
apagada y con el cable de corriente desconectado**, como dice el aviso 1 del
dibujo—. Lo que **no** se cambia son los GPIO 17 y 27.

**Pulsadores con patitas delgadas.** Los pulsadores chicos de metal traen dos
patitas planas y **delgadas**. Las terminales de crimpar tipo cuchilla son para
cuchillas anchas y **no las sujetan**: el botón puede funcionar hoy y dejar de
funcionar con el primer tirón del cable. **Suelda el cable a la patita, o
enrolla bien el cobre**, antes de meterlo todo en la caja.

**La hora, si la Pi NO lleva batería RTC.** Sin batería, la Pi olvida la hora al
apagarse y la recupera **por internet** al encender (así se decidió el
2026-09-15 para este evento). En la práctica: **enciende la Pi unos minutos
antes de abrir** y **mira la fecha del boleto de inventario** que imprime
al arrancar. Si sale una fecha vieja, **no la apagues para volver a
encenderla**: lo medido el 2026-09-15 es que la Pi tardó **unos tres minutos
desde que arrancó** (11:44:42) en que internet le corrigiera la hora (11:47), así
que reiniciarla vuelve a imprimir un boleto con la fecha mal. **Espera unos
minutos** con la Pi encendida y el internet funcionando y **pide otro boleto de
inventario**: el mesero mantiene **HABILITAR 6 segundos sin que nadie toque
JUGAR** (§5, punto 4). No abras hasta que ese boleto traiga la fecha de hoy.

**LED del botón arcade.** Muchos botones arcade traen un módulo LED de 5 V o
12 V. Un pin GPIO da 3.3 V y muy poca corriente: conéctalo a través de un
transistor NPN (2N2222 o similar) con 1 kΩ en la base, alimentando el LED desde
5 V (pin 2) o desde tu fuente de 12 V. Si no quieres LED, pon `"led": null`.

**Significado del LED**: apagado = HABILITAR suelto · fijo = listo para jugar ·
parpadeo lento = imprimiendo · parpadeo rápido = error (unos segundos).

---

## 3. Sistema operativo (propuesta)

**Raspberry Pi OS Lite, 64 bits** (versión actual "Trixie", Debian 13). Es el
oficial, sin escritorio (no hace falta pantalla) y trae Python 3.13, gpiozero y
Bluetooth listos. Todo lo que el programa necesita se instala con `apt`; no se
usa `pip`.

En **Raspberry Pi Imager** elige "Raspberry Pi OS Lite (64-bit)" y, en las
opciones avanzadas:

- **Nombre de equipo:** `ruleta` (así responde como `ruleta.local`).
- **Usuario:** `asadero`, con su contraseña.
- **Wi-Fi:** el del negocio, con su nombre y su contraseña exactos.
- **Zona horaria:** `America/Hermosillo`.
- **SSH activado con "Allow public-key authentication only"**: se pega ahí la
  llave pública de tu PC (`~/.ssh/id_ruleta.pub`). No se entra con contraseña.

Desde tu PC entras con `ssh asadero@ruleta.local` (o `ssh ruleta` si guardaste
el alias en `~/.ssh/config`).

**El SSH y el Wi-Fi son solo para instalar y probar.** *(Corregido el
2026-09-15. Aquí decía que «en el evento la Pi va **sin red**, así que la
**batería RTC es necesaria**». El usuario decidió ese día lo contrario: **no
habrá batería RTC** y **la Pi llevará el internet del asadero** durante el
evento, que es lo que le pone la hora al encender. Lo que sigue siendo verdad es
que, sin batería y sin red, los boletos salen con la fecha equivocada tras un
apagón: por eso hay que encenderla unos minutos antes de abrir y mirar la fecha
del boleto de inventario, §2.)*

**Si te llevas la Pi fuera del negocio** no encontrará su Wi-Fi y no responderá.
La salida, sin regrabar nada: en tu PC, **Configuración → Red e Internet → Punto
de acceso móvil**, con **el mismo nombre y la misma contraseña** del Wi-Fi del
asadero y banda 2.4 GHz. La Pi se conecta sola (queda en `192.168.137.x`) y
`ruleta.local` vuelve a responder. **Apágalo al volver al restaurante**: si no,
habría dos redes con el mismo nombre y la Pi podría engancharse a la PC.

---

## 4. Instalación paso a paso

**Paso 1 · Traer el programa a la Pi** (en la Pi, por SSH):
```bash
git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git ~/ruleta
```
Para actualizarlo después: `cd ~/ruleta && git pull`. Si editaste `config.json`
en la Pi, guárdalo antes fuera del repositorio (`cp ~/ruleta/config.json ~/`) o
`git pull` se quejará.

**Paso 2 · Instalar** (en la Pi, por SSH):
```bash
cd ~/ruleta
chmod +x instalar.sh herramientas/*.sh
sudo ./instalar.sh
```
Instala dependencias, deja los permisos de la impresora USB (regla `udev` y
grupo `lp`), habilita el Bluetooth de respaldo y registra el servicio que
arranca solo al encender. Se puede volver a correr cuando quieras.

**Paso 3 · Conectar la impresora por USB.** Enchufa su cable USB a la Pi,
enciéndela con papel dentro y comprueba que el sistema la ve:
```bash
python3 -m ruleta diagnostico
```
Tiene que decir `[ok] impresora conectada en /dev/ruleta-impresora`. Ese nombre
lo crea la regla `udev` del instalador; el nodo real es `/dev/usb/lp0` y su
número puede cambiar, el nombre fijo no. En `config.json` ya viene puesto:
```json
"impresora": { "tipo": "archivo", "ruta": "/dev/ruleta-impresora", ... }
```
Si dice **sin permiso**, tu usuario aún no está en el grupo `lp`: sal y vuelve a
entrar por SSH (el instalador ya lo agregó). Si dice **no existe la ruta**,
revisa el cable y que la impresora esté encendida. El camino por Bluetooth
está más abajo, en "Respaldo".

**Paso 4 · Boleto de diagnóstico:**
```bash
python3 -m ruleta probar-impresora
```
Revisa en el papel:
- **Acentos**: sale una etiqueta por tabla (`ESC t 0 / 2 / 16 / 19`) con su
  muestra debajo. Aquella cuya muestra se lea bien —`ñ Ñ á é í ó ú Á É Í Ó Ú ü
  ¿ ¡`— es la tabla correcta. En esta impresora está medido: la **19**
  (`cp858`), que es la que ya trae `config.json`; la 16 imprime basura. Si en la
  tuya fuera otra, pon ese número en `impresora.codepage_n` y su códec en
  `codepage` (`0`→`cp437`, `2`→`cp850`, `16`→`cp1252`, `19`→`cp858`).
- **Pitido**: al terminar cada boleto la impresora da un pitido corto
  (`"beep": true`). Si molesta, ponlo en `false`.
- **Regla de ancho** `0123456789...`: debe llenar exactamente la línea. Si se
  corta, la impresora está en 42 columnas (interruptor DIP 5): pon
  `chars_por_linea: 42` o cambia el DIP.
- **Corte**: si no cortó solo, prueba `"corte": "parcial"` (y revisa el DIP 1
  del cortador). Que quede una pestaña sin cortar es normal en esta familia.

**Paso 5 · Tu logo.** Prepara un PNG o JPG de 8 bits, entre 384 y 576 píxeles de
ancho, fondo blanco o transparente (el programa lo reduce si es más ancho, pero
nunca lo agranda). Desde la PC:
```bash
scp logo.png asadero@ruleta.local:~/ruleta/
```
El logo se lee en cada boleto, así que no hay que reiniciar nada. Vuelve a
correr `python3 -m ruleta probar-impresora` y comprueba que sale nítido y
centrado. Si es una foto, pon `"logo_tramado": true`. Si el archivo falta o
está dañado, el boleto sale sin logo (lo avisa `python3 -m ruleta diagnostico`).

**Paso 6 · Premios y textos.** Edita `config.json` en la Pi (`nano config.json`)
o en la PC y cópialo con `scp config.json asadero@ruleta.local:~/ruleta/`.
Cambia los `test1`…`test7` por tus premios reales (ver §7). Comprueba cómo se
verán los boletos sin gastar papel:
```bash
python3 -m ruleta vista-previa --todos
```
**Cada vez que cambies `config.json` con el servicio corriendo:**
`sudo systemctl restart ruleta`.

**Paso 7 · Hora e inventario en cero.** *(Corregido el 2026-09-15. Este paso
decía «en el evento la Pi va sin internet, así que **instala la batería RTC** y
deja la hora fija». Ya no: **no hay batería RTC** y **la Pi va con el internet
del asadero**, así que lo correcto es dejar que la hora la ponga la red.)*
Comprueba la zona horaria y **deja encendida la sincronización**:
```bash
sudo timedatectl set-timezone America/Hermosillo
sudo timedatectl set-ntp true
timedatectl                          # que la fecha y la hora sean las de hoy
```
Los dos comandos que ponían la hora a mano (`set-ntp false` y
`set-time "…"`) solo hacen falta si de verdad no va a haber red: con red,
apagar la sincronización deja el reloj a la deriva.
Deja el inventario en cero para el evento:
```bash
python3 -m ruleta reiniciar --si
```

**Paso 8 · Arrancar** (a partir de aquí arranca sola al encender la Pi):
```bash
sudo systemctl start ruleta
journalctl -u ruleta -f      # log en vivo; Ctrl+C para salir
```

### Respaldo: la impresora por Bluetooth

Solo si el USB no fuera posible (cable roto, puerto muerto). Enciende la
impresora y empareja:
```bash
./herramientas/emparejar.sh                        # o pásale la MAC: ...sh AA:BB:CC:DD:EE:FF
```
El script empareja, prueba los PIN `0000` y `1234`, guarda la MAC y deja
`"tipo": "bluetooth"` en `config.json` (reescribe el archivo entero, así que
revísalo después). Para volver al cable, pon otra vez `"tipo": "archivo"`.

Si la impresora no aparece en la búsqueda, imprímele su **página de
autoprueba**: apágala, mantén presionado el botón FEED, enciéndela y suelta a
los 3-5 segundos. Ahí vienen su nombre Bluetooth, la MAC, el PIN y los puntos
por línea.

---

## 5. Operación diaria

1. **Encender la Pi y la impresora.** A los pocos segundos se imprime solo el
   **inventario** (restantes de cada premio, entregados hoy, probabilidades y,
   si los hay, boletos pendientes de revisar). Si la impresora aún no responde
   lo reintenta unas veces; luego queda lista y sigue reintentando en cada jugada.
2. El mesero **mantiene presionado HABILITAR** y el cliente **presiona JUGAR**.
   Se imprime el boleto y se corta. Durante 5 segundos se ignoran más pulsaciones.
   Da igual si el cliente lo toca o lo sostiene: su botón solo sirve para jugar.
3. Pulsar JUGAR sin HABILITAR no hace nada (queda anotado en el log). El mesero
   debe presionar HABILITAR **antes** que el cliente.
4. **Inventario a media jornada**: el mesero mantiene **HABILITAR 6 segundos sin
   que nadie toque JUGAR**. Se imprime el inventario. Si alguien juega en esos
   segundos, el gesto se cancela (suelta y vuelve a intentar). Se ajusta o
   desactiva con `gpio.pulsacion_larga_seg`.
5. Si **no queda ningún premio disponible** se imprime un boleto de
   "SIGUE PARTICIPANDO" (texto configurable). El folio también avanza.
6. **No salió boleto y el LED parpadea rápido.** Antes de imprimir, el programa
   le pregunta a la impresora si tiene papel y está en línea (por USB y por
   Bluetooth); si contesta que no, o si no logra abrirla, **el premio regresa al
   inventario** y el folio se anota como `error_conexion`. Revisa impresora y
   papel y vuelve a jugar.
7. **Se cortó a medio boleto** (se perdió la conexión mientras imprimía): el folio
   queda como `incierto` y el premio **sigue contado como entregado** para no
   regalarlo dos veces. Aparece en el inventario bajo "REVISAR". Si compruebas
   que el boleto no salió, devuelve el premio (con el servicio detenido):
   ```bash
   sudo systemctl stop ruleta
   python3 -m ruleta liberar          # lista los folios pendientes
   python3 -m ruleta liberar 42       # devuelve el premio del boleto 00042
   sudo systemctl start ruleta
   ```
8. **Se acabó el papel.** **El kiosco no juega hasta que pongas el rollo.** Con
   `consultar_estado: true` el programa le pregunta a la impresora antes de cada
   boleto y, si le contesta que no tiene papel, **no imprime, no descuenta el
   premio y el LED parpadea rápido** (así avisa de error): el premio vuelve al
   inventario y el
   journal dice `NO impreso (premio devuelto al inventario)`. Pon el rollo,
   cierra bien la tapa y vuelve a jugar. **No apagues la impresora**: si tenía
   algo en su memoria, sale solo al reponer el papel. No todos los firmwares
   contestan; si el tuyo no contesta, el programa imprime igual (es lo correcto:
   callarse no es lo mismo que fallar), así que **coteja** los últimos folios de
   `datos/boletos.csv` (o del inventario impreso) con los boletos físicos y
   libera con el punto 7 los que no hayan salido.

> **Aviso del 2026-09-15 (Fase 4a): en este kiosco NO hay ningún LED
> conectado.** Los puntos 6 y 8 de arriba dicen «el LED parpadea rápido» porque
> el LED es la señal de error que el programa tiene prevista, y **funciona si
> alguien lo conecta** (§2). Hoy no hay ninguno, y eso está medido: en la prueba
> en vivo de las 21:32 del 2026-09-15, con el rollo fuera, el kiosco **rechazó
> dos jugadas correctamente** —no imprimió, devolvió los dos premios y no dejó
> nada retenido— y el usuario, que estaba delante, dijo **«no vi ninguna
> diferencia realmente»**. Mientras no haya LED (o zumbador), **la única forma de
> enterarse es que no salga boleto y mirar el journal o el rollo**. Ficha
> **F-256**; evidencia: `docs/actas/2026-09-15-fase-4a.md`.
>
> En el mismo aviso, un matiz del punto 8: **desde el 2026-09-15 la impresora ya
> no se queda con el boleto**. El programa se entera de que no hay papel **antes
> de mandar un solo byte**, así que al reponer el rollo **no sale ningún boleto
> solo** (antes sí salía). Lo de «no apagues la impresora» sigue valiendo por si
> el fallo la pilla a media impresión, que es otro caso.

**Archivos que genera** (carpeta `datos/`):

| Archivo | Contenido |
|---|---|
| `estado.json` | folio actual, entregados por premio (total y por día). Se escribe de forma atómica: un apagón no lo corrompe |
| `boletos.csv` | bitácora: folio, fecha, día operativo, premio, evento (`emitido`, `impreso`, `error_conexion`, `incierto`, `liberado`). Ábrelo en Excel |
| `ruleta.log` | log técnico (rotativo, 1 MB × 3) |

```bash
python3 -m ruleta reporte              # inventario en pantalla (funciona con el servicio corriendo)
python3 -m ruleta reporte --imprimir   # y en la impresora (con el servicio detenido)
python3 -m ruleta reiniciar            # evento nuevo: folio y contadores a cero (respalda los archivos)
```

**Detén el servicio** (`sudo systemctl stop ruleta`) antes de `reiniciar`,
`liberar`, `reporte --imprimir` o `probar-impresora`: el servicio guarda el
inventario en memoria y no conviene que dos programas escriban a la vez en la
impresora. `reiniciar`, `liberar` y `reporte --imprimir` lo detectan y te lo
recuerdan; **`probar-impresora` no avisa**, ahí tienes que acordarte tú. Al
terminar: `sudo systemctl start ruleta`.

**El "día"** empieza a las 6:00 (`juego.hora_inicio_dia`): una jugada a la 1:00
de la madrugada cuenta para el día anterior, como en la operación real del negocio.

---

## 6. Configuración (`config.json`)

Cualquier llave que omitas toma el valor por defecto. Al arrancar se valida
todo (incluidos los tipos: un número entre comillas se rechaza con un mensaje
claro) y, si algo está mal, el programa dice exactamente qué corregir. Los
cambios se aplican al reiniciar el servicio: `sudo systemctl restart ruleta`.

### `negocio`
| Llave | Defecto | Qué es |
|---|---|---|
| `nombre` | `"Asadero 33"` | encabezado del boleto (2× de tamaño) |
| `logo` | `"logo.png"` | ruta del logo, relativa a config.json. `null` = sin logo |
| `logo_ancho` | `384` | ancho en píxeles al imprimir (8 a 576 en 80 mm) |
| `logo_tramado` | `false` | `true` para fotos (tramado); `false` para logos de trazo (umbral) |
| `titulo_premio` | `"¡GANASTE!"` | línea sobre el premio |
| `pie` | 3 líneas | texto al pie del boleto (lista de líneas) |

### `impresora`
| Llave | Defecto | Qué es |
|---|---|---|
| `tipo` | `"bluetooth"` | `archivo` = por cable USB (**lo que trae este `config.json`**), `bluetooth` = respaldo, `vista` = consola |
| `mac` | — | dirección Bluetooth; la escribe `emparejar.sh` |
| `canal` | `1` | canal RFCOMM; `diagnostico` lo detecta si no es 1 |
| `ruta` | `"salida_impresora.bin"` | con `tipo: archivo`, el dispositivo de la impresora: `/dev/ruleta-impresora` (el nodo real es `/dev/usb/lp0`) |
| `ancho_puntos` | `576` | puntos por línea (80 mm = 576; 58 mm = 384) |
| `chars_por_linea` | `48` | columnas en fuente normal (42 si el DIP 5 está activo; mínimo 32) |
| `codepage` / `codepage_n` | `cp858` / `19` | tabla de caracteres para acentos (ver paso 4) |
| `juego_internacional` | `0` | `ESC R n`; 0 evita que `# $ @ \` salgan cambiados |
| `cancelar_modo_chino` | `true` | manda `FS .` tras inicializar; sin esto los acentos salen como ideogramas |
| `corte` | `"auto"` | `auto` (avanza hasta la cuchilla y corta), `parcial`, `completo`, `ninguno` |
| `lineas_antes_corte` | `null` | líneas en blanco antes de cortar; `null` = 1 con `auto`, 5 con los demás |
| `beep` | `false` | pitido al terminar el boleto (este `config.json` lo trae en `true`: un pitido corto por boleto) |
| `consultar_estado` | `true` | antes de cada boleto pregunta si hay papel y está en línea, por USB y por Bluetooth; si no responde, imprime igual |
| `reintentos` / `espera_reintento_seg` | `3` / `2.0` | intentos de conexión por boleto |
| `timeout_seg` | `10.0` | tiempo máximo para conectar (mayor que 0). Si subes esto o `reintentos`, sube `TimeoutStopSec` en `ruleta.service` |
| `tamano_bloque` / `pausa_bloque_seg` | `512` / `0.03` | ritmo de envío; si el logo sale con basura usa `256` / `0.04` |
| `pausa_inicial_seg` | `0.4` | espera tras conectar (los módulos Bluetooth baratos pierden los primeros bytes) |
| `pausa_final_seg` / `bytes_por_segundo` | `1.5` / `16000` | espera antes de cerrar para que la impresora reciba todo |
| `banda_imagen` | `64` | filas de imagen por comando; baja a 32 si el logo sale desplazado |

**Solo valen con `tipo: bluetooth`:** `mac`, `canal`, `reintentos`,
`timeout_seg`, `tamano_bloque`, `pausa_bloque_seg`, `pausa_inicial_seg`,
`pausa_final_seg` y `bytes_por_segundo`. Por cable no hacen nada: no hay enlace
que se caiga ni ritmo que controlar. `espera_reintento_seg` **sí** cuenta con
cualquier tipo, USB incluido: es la espera (por dos) entre los intentos del
inventario de arranque (`juego.intentos_inventario_arranque`).

### `gpio`
| Llave | Defecto | Qué es |
|---|---|---|
| `boton_jugar` | `17` | GPIO (numeración BCM) del botón del cliente |
| `boton_habilitar` | `27` | GPIO del botón del mesero (`null` si no hay) |
| `led` | `22` | GPIO del LED (`null` si no hay) |
| `modo_habilitar` | `"mantener"` | `mantener` = hay que tener HABILITAR presionado; `siempre` = sin botón de mesero |
| `pull_up` | `true` | botones a GND (lo normal). `false` si los cableas a 3.3 V |
| `rebote_ms` | `30` | filtro antirrebote |
| `pulsacion_larga_seg` | `6.0` | segundos de HABILITAR presionado, sin tocar JUGAR, para imprimir inventario; `null` = desactivado |

### `juego`
| Llave | Defecto | Qué es |
|---|---|---|
| `espera_entre_jugadas_seg` | `5.0` | segundos en que se ignoran pulsaciones tras un boleto |
| `hora_inicio_dia` | `6` | hora a la que cambia el "día" para los topes diarios |
| `imprimir_inventario_al_arrancar` | `true` | inventario automático al encender |
| `intentos_inventario_arranque` | `3` | reintentos de ese inventario si la impresora tarda en estar lista |
| `consuelo.titulo` / `consuelo.texto` | `"SIGUE PARTICIPANDO"` / … | boleto cuando no hay premios disponibles |

### `premios` (lista)
| Llave | Obligatoria | Qué es |
|---|---|---|
| `id` | sí | identificador corto sin espacios (`test1`). Con él se llevan los contadores: **no lo cambies a media semana** |
| `nombre` | sí | lo que sale en grande en el boleto (se imprime en MAYÚSCULAS) |
| `peso` | sí | número > 0; la probabilidad es proporcional (ver abajo) |
| `stock` | no | unidades para todo el evento; `null` = ilimitado |
| `tope_diario` | no | máximo por día operativo; `null` = sin tope |
| `desde` / `hasta` | no | fechas `"AAAA-MM-DD"` (día operativo) en que el premio puede salir |
| `detalle` | no | texto chico bajo el premio ("Orden de tacos", "Canjeable en barra") |

---

## 7. Premios y probabilidades

En cada jugada solo participan los premios **disponibles** (con stock, sin
llegar a su tope del día y dentro de sus fechas). Entre ellos:

```
probabilidad del premio = peso del premio / suma de pesos de los disponibles
```

Cuando un premio se agota o llega a su tope, su peso se reparte entre los
demás. Por eso la probabilidad "real" cambia durante el día; el inventario
impreso muestra la probabilidad vigente en ese momento.

Con la configuración de prueba incluida (pesos 4, 4, 1, 25, 25, 25, 25 → suma 109):

| Premio | Stock | Tope/día | Peso | Probabilidad inicial |
|---|---|---|---|---|
| TEST 1 (grande) | 10 | 2 | 4 | 3.7 % |
| TEST 2 (grande) | 10 | 2 | 4 | 3.7 % |
| TEST 3 (mayor) | 1 | 1 | 1 | 0.9 % |
| TEST 4 · 5 · 6 · 7 (chicos) | 50 c/u | 10 c/u | 25 c/u | 22.9 % c/u |

Consejos:
- **Para que el premio mayor no salga el primer día**, ponle `"desde": "2026-09-20"`
  (el último día del evento) o dale un peso muy bajo y confía en la suerte.
- **Para repartir los grandes en la semana**, usa `tope_diario`: con stock 10 y
  tope 2, salen máximo 2 al día durante 5 días.
- Si quieres que **siempre haya premio**, deja al menos un premio chico con
  `"stock": null`. Si prefieres que se acaben, el boleto de consuelo se encarga.
- Los porcentajes exactos los ves sin imprimir con `python3 -m ruleta reporte`.

Los ids `test1`…`test7` son de prueba. Antes del evento: detén el servicio,
cámbialos por los premios reales, corre `python3 -m ruleta reiniciar --si` y
vuelve a arrancar el servicio.

---

## 8. Comandos

```bash
python3 -m ruleta                        # arranca la ruleta (lo que hace el servicio)
python3 -m ruleta --simular --impresora vista    # prueba en cualquier PC: teclas h/j/i, boletos en consola
python3 -m ruleta probar-impresora [--tablas 0,2,16,19]   # boleto de diagnóstico
python3 -m ruleta vista-previa [--todos | --premio ID]    # cómo se verán los boletos, sin hardware
python3 -m ruleta reporte [--imprimir]   # inventario actual
python3 -m ruleta liberar [FOLIO] [--si] # lista pendientes / devuelve el premio de un boleto que no salió
python3 -m ruleta reiniciar [--si]       # folio y contadores a cero (respalda estado.json y boletos.csv)
python3 -m ruleta diagnostico            # dependencias, carpeta de datos, emparejamiento, conexión y canal
python3 -m ruleta --config otro.json ... # otro archivo de configuración
python3 -m ruleta -v ...                 # log detallado
python3 -m unittest discover -s tests -t .   # pruebas automáticas (sin hardware)
```

Servicio:
```bash
sudo systemctl start|stop|restart|status ruleta
journalctl -u ruleta -f
```

---

## 9. Solución de problemas

**No imprime nada y el LED parpadea rápido.** Corre
`python3 -m ruleta diagnostico`; con la impresora por USB te dice cuál de las
tres cosas pasa:

- `[!!] no existe la ruta de la impresora`: está apagada o el cable está suelto.
  Enchúfalo, enciéndela y vuelve a correr el diagnóstico.
- `[!!] sin permiso para escribir`: falta la regla `udev` o el grupo `lp`. Se
  arregla volviendo a correr `sudo ./instalar.sh` y saliendo y entrando por SSH.
- `[!!] la impresora reporta SIN PAPEL` o `fuera de línea`: pon papel y cierra
  bien la tapa. **Esta tercera revisión solo se hace con el servicio detenido.**
  Con el servicio corriendo el diagnóstico no le pregunta nada a la impresora,
  para no interferir, y lo avisa con `[--] el servicio 'ruleta' está corriendo`.
  Si necesitas esta revisión: `sudo systemctl stop ruleta`, repite el
  diagnóstico y vuelve a arrancarlo con `sudo systemctl start ruleta`.

Por Bluetooth el diagnóstico dice además si está emparejada y en qué canal
responde; si dice "rechazó la conexión", desconecta otros dispositivos (un
celular le roba la impresora) o vuelve a emparejar:
```bash
bluetoothctl remove AA:BB:CC:DD:EE:FF
./herramientas/emparejar.sh
```

**Se acabó el papel: el kiosco deja de dar boletos, y eso está bien.** Cuando la
impresora dice que no tiene papel, el programa **no imprime, devuelve el premio
al inventario** y el LED parpadea rápido (así avisa de error); en el journal sale
`NO impreso (premio devuelto al inventario): la impresora /dev/ruleta-impresora
no tiene papel`. **No se pierde ningún premio.** Pon el rollo, cierra bien la
tapa y vuelve a jugar: el siguiente boleto sale normal.

*(Probado en hardware el 2026-09-15 a las 21:32, con el rollo fuera y el usuario
delante: los boletos 00013 y 00014 se revirtieron sin mandar un byte, **no quedó
nada retenido en la impresora** y los dos siguientes, con el rollo puesto,
salieron normales. **Pero sin LED conectado nadie ve el rechazo**: si el kiosco
deja de dar boletos de golpe, lo primero que hay que mirar es el rollo. Fichas
**F-250** y **F-256**; acta `docs/actas/2026-09-15-fase-4a.md`.)*

**Sale `[??] la impresora reporta poco papel`.** **No corras a comprar rollo.**
Este aviso solo puede venir de una impresora **con sensor de papel de verdad**, y
la que tiene el kiosco **no lo tiene** (medido el 2026-09-15: contesta «papel
bien» hasta con el rollo fuera). Si algún día aparece, **abre la tapa y mira el
rollo**, que es lo único que no miente. Los avisos que salieron entre el
2026-09-11 y el 2026-09-15 eran **falsos** —el último fue el de la jugada sin
papel de las 13:29 del 2026-09-15— y ya están arreglados.

**Los acentos salen como símbolos raros o letras chinas.** Revisa que
`cancelar_modo_chino` sea `true` y elige la tabla correcta con
`probar-impresora` (paso 4). Algunas unidades tienen un interruptor DIP 4
"sin caracteres chinos": activarlo también ayuda.

**El texto se corta a la derecha o las líneas de guiones no llenan el ancho.**
La impresora está en 42 columnas (DIP 5). Pon `chars_por_linea: 42`.

**No corta el papel.** Revisa el DIP 1 del cortador. Cambia `corte` a
`"parcial"`. Si corta a mitad del texto, sube `lineas_antes_corte`.

**El logo sale con basura, bandas movidas o incompleto.** Prueba
`banda_imagen: 32` y reduce el logo (`logo_ancho: 320`). Si sale como bloque
negro o en blanco, guárdalo de nuevo como PNG de 8 bits con fondo blanco. Por
Bluetooth, además, baja el ritmo: `tamano_bloque: 256`, `pausa_bloque_seg: 0.04`
(por cable esas dos no hacen nada).

**El botón no responde.** Verifica que el cable vaya a GND y al GPIO correcto
(numeración BCM, no el número de pin físico; `pinout` en la terminal muestra el
header). Mira el log: `journalctl -u ruleta -f`. Si dice que HABILITAR no está
presionado, el mesero debe mantenerlo **antes** de que el cliente presione;
para probar sin él pon `"modo_habilitar": "siempre"`.

**Se imprimió el inventario sin pedirlo.** El mesero mantuvo HABILITAR 6
segundos sin que el cliente jugara. Sube `pulsacion_larga_seg` o ponlo en
`null` (entonces el inventario solo sale al encender o con `reporte --imprimir`).

**El servicio no arranca y `systemctl status ruleta` dice "failed".** Casi
siempre es un error en `config.json`: el programa sale con código 2 y systemd
**no lo reintenta** a propósito (un error de configuración no se arregla solo).
Mira el motivo, corrígelo y vuelve a arrancarlo:
```bash
systemctl status ruleta
journalctl -u ruleta -n 20 --no-pager    # dice qué llave está mal
nano config.json
sudo systemctl restart ruleta
```
Si en cambio se reinicia una y otra vez (`activating`), el fallo sí es
transitorio: permisos del GPIO o carpeta de datos que no se puede escribir. Un
fallo de la impresora **no** reinicia el servicio (el boleto no sale, el LED
parpadea rápido y el programa sigue esperando). `python3 -m ruleta
diagnostico` lo señala.

**Hora o fecha incorrectas en los boletos.** *(2026-09-15: para este evento **no
hay batería RTC**; la hora se la pone el internet del asadero al encender. Si la
fecha sale mal es que la Pi todavía no ha sincronizado la hora: **no la apagues
para volver a encenderla**. Al reiniciar vuelve a arrancar con la fecha vieja y a
imprimir otro boleto de inventario equivocado —lo medido el 2026-09-15 es que
tardó **unos tres minutos**, de las 11:44:42 a las 11:47—. Déjala encendida con
el internet funcionando, espera unos minutos y **pide otro boleto de inventario**
(el mesero mantiene HABILITAR 6 segundos sin que nadie toque JUGAR, §5 punto 4)
hasta que traiga la fecha de hoy.)* Si algún día sí se instala la batería RTC: fija la hora con
`timedatectl` (paso 7) y activa su recarga agregando
`dtparam=rtc_bbat_vchg=3000000` a `/boot/firmware/config.txt`.

**El Bluetooth de la Pi no aparece** (`No default controller available`):
```bash
sudo rfkill unblock bluetooth
sudo systemctl enable --now bluetooth
bluetoothctl show      # Powered: yes
```

**Quiero probar sin la Pi ni la impresora.** En cualquier computadora con
Python 3.11+ y Pillow:
```bash
python3 -m ruleta --simular --impresora vista
```
Teclas: `h` alterna HABILITAR, `j` pulsa JUGAR, `i` simula el gesto de
inventario, `q` sale.

**El nombre `/dev/ruleta-impresora` no aparece.** Lo crea la regla
`/etc/udev/rules.d/61-ruleta-impresora-usb.rules` que escribe `instalar.sh`, y
solo cuando el sistema reconoce la impresora. Comprueba en este orden:
```bash
lsusb                                  # debe aparecer la impresora (0418:5011)
ls -l /dev/usb/lp0 /dev/ruleta-impresora
id -nG | grep -w lp                    # tu usuario debe estar en el grupo lp
sudo ./instalar.sh                     # vuelve a poner la regla y el grupo
```
Mientras tanto puedes apuntar `"ruta": "/dev/usb/lp0"`, que es el nodo real.
Y si el USB no fuera viable, queda el respaldo por Bluetooth (§4).

---

## 10. Estructura

```
ruleta/               código
  __main__.py         comandos (python3 -m ruleta ...)
  app.py              ciclo principal: botones -> sorteo -> impresión
  config.py           carga y validación de config.json
  inventario.py       premios, sorteo ponderado, estado.json, boletos.csv, liberar
  ticket.py           diseño de los boletos
  escpos.py           comandos ESC/POS, estado del papel y transportes (USB y Bluetooth)
  hardware.py         botones/LED con gpiozero y simulación por teclado
tests/                pruebas automáticas (unittest)
herramientas/         emparejar.sh (respaldo Bluetooth)
docs/                 planes, actas y fichas de cada fase del proyecto
config.json           configuración
logo.png              logo provisional (reemplázalo por el real)
instalar.sh           instalador para Raspberry Pi OS
ruleta.service        plantilla del servicio systemd
datos/                se crea al correr: estado.json, boletos.csv, ruleta.log, ruleta.lock
```
