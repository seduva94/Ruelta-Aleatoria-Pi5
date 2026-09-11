# Ruleta de premios · Asadero 33

Un botón arcade conectado a una Raspberry Pi 5. El cliente lo presiona, el
programa sortea un premio según las probabilidades e inventario configurados,
y una impresora térmica Bluetooth imprime el boleto con el logo, el premio en
letras grandes y el número de boleto. No hay pantalla: la retroalimentación es
el boleto, un LED opcional y el log.

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
| Batería RTC (recomendada) | "RTC Battery for Raspberry Pi 5" (Panasonic ML-2020, conector J5 junto al USB-C). Sin ella, tras un corte de luz y sin internet la hora de los boletos saldrá mal |
| Impresora | AOMU My-A1, 80 mm, Bluetooth, cortador automático. Rollos térmicos de 80 mm |
| Botón JUGAR | botón arcade (cualquier botón normalmente abierto sirve) |
| Botón HABILITAR | pulsador para el mesero; se mantiene presionado mientras el cliente juega |
| LED (opcional) | LED normal + resistencia de 330 Ω, o el LED del propio botón arcade (ver nota) |
| Cables | dupont hembra para el header de la Pi y terminales para los botones |

---

## 2. Conexión eléctrica

Los botones van **entre el pin GPIO y tierra (GND)**. No hace falta resistencia:
el programa activa las resistencias pull-up internas de la Pi. Presionado = 0 V.

| Función | GPIO (BCM) | Pin físico | El otro cable a |
|---|---|---|---|
| Botón JUGAR | GPIO 17 | pin 11 | GND (pin 9) |
| Botón HABILITAR | GPIO 27 | pin 13 | GND (pin 9 o 14) |
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

En **Raspberry Pi Imager**: elige "Raspberry Pi OS Lite (64-bit)", y en las
opciones avanzadas pon nombre de equipo (`ruleta`), usuario y contraseña, tu red
Wi-Fi y **activa SSH**. Así entras desde tu computadora con `ssh usuario@ruleta.local`.

---

## 4. Instalación paso a paso

**Paso 1 · Copiar el programa a la Pi** (desde tu PC, en la carpeta que contiene
"Ruleta Asadero"). La primera vez:
```bash
scp -r "Ruleta Asadero" usuario@ruleta.local:~/ruleta
```
Para **actualizar** archivos después (si ya existe `~/ruleta`, la línea anterior
crearía una carpeta anidada), copia el *contenido*:
```bash
scp -r "Ruleta Asadero/." usuario@ruleta.local:~/ruleta/
```
No copies una carpeta `datos/` de pruebas hechas en la PC: el paso 7 deja el
inventario en cero de todos modos.

**Paso 2 · Instalar** (en la Pi, por SSH):
```bash
cd ~/ruleta
chmod +x instalar.sh herramientas/*.sh
sudo ./instalar.sh
```
Instala dependencias, habilita el Bluetooth y registra el servicio que arranca
solo al encender. Se puede volver a correr cuando quieras.

**Paso 3 · Emparejar la impresora** (enciéndela primero):
```bash
./herramientas/emparejar.sh
```
Si la impresora no aparece, imprímele su **página de autoprueba**: apágala,
mantén presionado el botón FEED, enciéndela y suelta a los 3-5 segundos. Ahí vienen
su nombre Bluetooth, la MAC, el PIN (normalmente `0000` o `1234`) y los puntos por
línea. El script prueba ambos PIN solo y guarda la MAC en `config.json`.

**Paso 4 · Boleto de diagnóstico:**
```bash
python3 -m ruleta probar-impresora
```
Revisa en el papel:
- **Acentos**: hay cuatro líneas `ESC t 0 / 2 / 16 / 19`. La que muestre bien
  `ñ Ñ á é í ó ú Á É Í Ó Ú ü ¿ ¡` es la tabla correcta. Si no es la 19, pon en
  `config.json` → `impresora.codepage_n` ese número y en `codepage` su códec
  (`0`→`cp437`, `2`→`cp850`, `16`→`cp1252`, `19`→`cp858`).
- **Regla de ancho** `0123456789...`: debe llenar exactamente la línea. Si se
  corta, la impresora está en 42 columnas (interruptor DIP 5): pon
  `chars_por_linea: 42` o cambia el DIP.
- **Corte**: si no cortó solo, prueba `"corte": "parcial"` (y revisa el DIP 1 del cortador).

**Paso 5 · Tu logo.** Prepara un PNG o JPG de 8 bits, entre 384 y 576 píxeles de
ancho, fondo blanco o transparente (el programa lo reduce si es más ancho, pero
nunca lo agranda). Desde la PC:
```bash
scp logo.png usuario@ruleta.local:~/ruleta/
```
El logo se lee en cada boleto, así que no hay que reiniciar nada. Vuelve a
correr `python3 -m ruleta probar-impresora` y comprueba que sale nítido y
centrado. Si es una foto, pon `"logo_tramado": true`. Si el archivo falta o
está dañado, el boleto sale sin logo (lo avisa `python3 -m ruleta diagnostico`).

**Paso 6 · Premios y textos.** Edita `config.json` en la Pi (`nano config.json`)
o en la PC y cópialo con `scp config.json usuario@ruleta.local:~/ruleta/`.
Cambia los `test1`…`test7` por tus premios reales (ver §7). Comprueba cómo se
verán los boletos sin gastar papel:
```bash
python3 -m ruleta vista-previa --todos
```
**Cada vez que cambies `config.json` con el servicio corriendo:**
`sudo systemctl restart ruleta`.

**Paso 7 · Hora e inventario en cero.** Si la Pi no tendrá internet, pon la hora
(e instala la batería RTC):
```bash
sudo timedatectl set-timezone America/Mexico_City
sudo timedatectl set-ntp false
sudo timedatectl set-time "2026-09-15 18:30:00"
```
Deja el inventario en cero para el evento:
```bash
python3 -m ruleta reiniciar --si
```

**Paso 8 · Arrancar** (a partir de aquí arranca sola al encender la Pi):
```bash
sudo systemctl start ruleta
journalctl -u ruleta -f      # log en vivo; Ctrl+C para salir
```

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
   pregunta a la impresora si tiene papel y está en línea; si reporta que no, o
   si no logra conectarse, **el premio regresa al inventario** y el folio se
   anota como `error_conexion`. Revisa impresora y papel y vuelve a jugar.
7. **Se cortó a medio boleto** (Bluetooth se cayó mientras imprimía): el folio
   queda como `incierto` y el premio **sigue contado como entregado** para no
   regalarlo dos veces. Aparece en el inventario bajo "REVISAR". Si compruebas
   que el boleto no salió, devuelve el premio (con el servicio detenido):
   ```bash
   sudo systemctl stop ruleta
   python3 -m ruleta liberar          # lista los folios pendientes
   python3 -m ruleta liberar 42       # devuelve el premio del boleto 00042
   sudo systemctl start ruleta
   ```
8. **Se acabó el papel.** No apagues la impresora: pon el rollo nuevo y lo que
   estuviera en su memoria sale solo. Luego coteja los últimos folios de
   `datos/boletos.csv` (o del inventario impreso) con los boletos físicos; si
   alguno no salió, libéralo como en el punto 7. Con la consulta de estado
   activa (`consultar_estado: true`) la impresora avisa que no hay papel y el
   programa no descuenta el premio.

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
inventario en memoria y la impresora acepta una sola conexión Bluetooth. Los
comandos lo detectan y te lo recuerdan. Al terminar: `sudo systemctl start ruleta`.

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
| `tipo` | `"bluetooth"` | `bluetooth`, `archivo` (escribe a `ruta`) o `vista` (consola) |
| `mac` | — | dirección Bluetooth; la escribe `emparejar.sh` |
| `canal` | `1` | canal RFCOMM; `diagnostico` lo detecta si no es 1 |
| `ruta` | `"salida_impresora.bin"` | solo con `tipo: archivo`; p. ej. `/dev/usb/lp0` si algún día va por USB |
| `ancho_puntos` | `576` | puntos por línea (80 mm = 576; 58 mm = 384) |
| `chars_por_linea` | `48` | columnas en fuente normal (42 si el DIP 5 está activo; mínimo 32) |
| `codepage` / `codepage_n` | `cp858` / `19` | tabla de caracteres para acentos (ver paso 4) |
| `juego_internacional` | `0` | `ESC R n`; 0 evita que `# $ @ \` salgan cambiados |
| `cancelar_modo_chino` | `true` | manda `FS .` tras inicializar; sin esto los acentos salen como ideogramas |
| `corte` | `"auto"` | `auto` (avanza hasta la cuchilla y corta), `parcial`, `completo`, `ninguno` |
| `lineas_antes_corte` | `null` | líneas en blanco antes de cortar; `null` = 1 con `auto`, 5 con los demás |
| `beep` | `false` | pitido al terminar el boleto (solo si la impresora tiene zumbador y su DIP 2 activo) |
| `consultar_estado` | `true` | antes de cada boleto pregunta si hay papel y está en línea; si no responde, imprime igual |
| `reintentos` / `espera_reintento_seg` | `3` / `2.0` | intentos de conexión por boleto |
| `timeout_seg` | `10.0` | tiempo máximo para conectar (mayor que 0). Si subes esto o `reintentos`, sube `TimeoutStopSec` en `ruleta.service` |
| `tamano_bloque` / `pausa_bloque_seg` | `512` / `0.03` | ritmo de envío; si el logo sale con basura usa `256` / `0.04` |
| `pausa_inicial_seg` | `0.4` | espera tras conectar (los módulos Bluetooth baratos pierden los primeros bytes) |
| `pausa_final_seg` / `bytes_por_segundo` | `1.5` / `16000` | espera antes de cerrar para que la impresora reciba todo |
| `banda_imagen` | `64` | filas de imagen por comando; baja a 32 si el logo sale desplazado |

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

**No imprime nada y el LED parpadea rápido.** La impresora está apagada, sin
papel, fuera de alcance o con un celular conectado. Corre
`python3 -m ruleta diagnostico`: te dice si está emparejada, si responde y en
qué canal. Si dice "rechazó la conexión", prueba desconectar otros
dispositivos, o vuelve a emparejar:
```bash
bluetoothctl remove AA:BB:CC:DD:EE:FF
./herramientas/emparejar.sh
```

**Los acentos salen como símbolos raros o letras chinas.** Revisa que
`cancelar_modo_chino` sea `true` y elige la tabla correcta con
`probar-impresora` (paso 4). Algunas unidades tienen un interruptor DIP 4
"sin caracteres chinos": activarlo también ayuda.

**El texto se corta a la derecha o las líneas de guiones no llenan el ancho.**
La impresora está en 42 columnas (DIP 5). Pon `chars_por_linea: 42`.

**No corta el papel.** Revisa el DIP 1 del cortador. Cambia `corte` a
`"parcial"`. Si corta a mitad del texto, sube `lineas_antes_corte`.

**El logo sale con basura, bandas movidas o incompleto.** Baja el ritmo:
`tamano_bloque: 256`, `pausa_bloque_seg: 0.04`, `banda_imagen: 32`. Reduce el
logo (`logo_ancho: 320`). Si sale como bloque negro o en blanco, guárdalo de
nuevo como PNG de 8 bits con fondo blanco.

**El botón no responde.** Verifica que el cable vaya a GND y al GPIO correcto
(numeración BCM, no el número de pin físico; `pinout` en la terminal muestra el
header). Mira el log: `journalctl -u ruleta -f`. Si dice que HABILITAR no está
presionado, el mesero debe mantenerlo **antes** de que el cliente presione;
para probar sin él pon `"modo_habilitar": "siempre"`.

**Se imprimió el inventario sin pedirlo.** El mesero mantuvo HABILITAR 6
segundos sin que el cliente jugara. Sube `pulsacion_larga_seg` o ponlo en
`null` (entonces el inventario solo sale al encender o con `reporte --imprimir`).

**El servicio se reinicia en bucle** (`systemctl status ruleta` dice
"activating"): casi siempre es un error en `config.json`. Corre
`python3 -m ruleta diagnostico`; el mensaje dice qué llave corregir.

**Hora o fecha incorrectas en los boletos.** Instala la batería RTC, fija la
hora con `timedatectl` (paso 7) y activa su recarga agregando
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

**La impresora resulta ser solo BLE** (el diagnóstico no ve "Serial Port" y
nunca conecta): usa el cable USB de la impresora y pon
`"tipo": "archivo", "ruta": "/dev/usb/lp0"` (agrega tu usuario al grupo `lp`).

---

## 10. Estructura

```
ruleta/               código
  __main__.py         comandos (python3 -m ruleta ...)
  app.py              ciclo principal: botones -> sorteo -> impresión
  config.py           carga y validación de config.json
  inventario.py       premios, sorteo ponderado, estado.json, boletos.csv, liberar
  ticket.py           diseño de los boletos
  escpos.py           comandos ESC/POS, estado de papel y transporte Bluetooth
  hardware.py         botones/LED con gpiozero y simulación por teclado
tests/                pruebas automáticas (unittest)
herramientas/         emparejar.sh
config.json           configuración
logo.png              logo provisional (reemplázalo por el real)
instalar.sh           instalador para Raspberry Pi OS
ruleta.service        plantilla del servicio systemd
datos/                se crea al correr: estado.json, boletos.csv, ruleta.log, ruleta.lock
```
