# Protocolo de trabajo (obligatorio en este repo)

Este protocolo manda sobre cualquier comportamiento por defecto. Aplica a todo
trabajo multi-fase: planes, código, docs, commits y deploys. Se lee al inicio de
cada sesión; un `/clear` no lo borra.

## 1. Roles fijos, por modelo

- **Orquestador (Fable).** No escribe código. Mide hechos antes de cada fase,
  escribe el brief, arma la cadena de agentes, decide los gates y verifica de
  forma independiente al final. Solo toca docs de memoria y archivos efímeros de
  sesión. **Fable no ejecuta git, ni siquiera comandos de solo lectura:** la
  comprobación de que un commit o un push quedó bien la hace un agente
  verificador de solo lectura que le informa con hechos medidos; Fable lee ese
  informe, no la terminal.
- **Ejecutor (Opus, esfuerzo máximo).** Implementa una fase completa: análisis,
  código, goldens y documentación en el mismo cambio. Nunca commitea.
- **Revisores (Opus, solo lectura).** Dos lentes en paralelo con enfoques
  distintos (conducta/seguridad y fidelidad plan↔docs), luego un escéptico
  independiente que no vio a los lentes e intenta refutar. Devuelven
  correcciones exactas «texto actual → texto nuevo»; jamás editan.
- **Exploradores y extractores (Sonnet, solo lectura, esfuerzo bajo/medio).**
  Búsquedas y el inventario crudo del diff.
- **Escriba (Opus, esfuerzo máximo, solo lectura).** Testigo independiente que
  lee el diff real, no lo que dice el ejecutor, y enruta cada cambio a su doc con
  veredicto y huecos.
- **Agente de commit (Opus, esfuerzo alto).** La única mano que toca git y push,
  con gates duros.
- **Verificador de push (Sonnet, solo lectura, esfuerzo medio).** Después de
  cada commit o push, un agente distinto del que lo hizo comprueba contra el
  remoto (hash, rama, conjunto de archivos, árbol limpio) e informa al
  orquestador. Nada se da por publicado hasta ese informe.

## 2. El plan manda

Todo trabajo multi-fase nace como un plan prescriptivo en el repo: bitácora con
casillas, decisiones cerradas, trampas del repo que un ejecutor sin contexto no
puede adivinar, mapa de anclas que «derivan» (re-grep antes de cada edición),
criterios de aceptación por fase y prohibiciones.

Regla clave: **si el código real contradice el plan, el ejecutor se detiene y
pregunta; no improvisa.**

## 3. La cadena por fase, siempre la misma

Brief con hechos medidos → ejecutor → lentes en paralelo → correctivo (bucle
acotado, 2 o 3 rondas) → escéptico → commit compuertado → deploy observado hasta
verde → verificador en vivo contra lo desplegado → extractor + escriba →
confrontación de docs → lente de la confrontación → segundo commit solo de docs.

Cada eslabón que produce commit espera un «listo» explícito de los revisores.

## 4. Gates del commit

- Conjunto de archivos permitido por adelantado.
- Nada pendiente de push antes de commitear.
- `git add` solo por rutas explícitas.
- Compuerta por conjunto de hashes (exactamente uno, igual a HEAD) antes del push.
- Nunca pushear con un deploy en vuelo.
- Nunca saltarse hooks.
- El run se observa hasta verde y un fallo se reporta, no se parchea en caliente.

## 5. Redes que muerden

- Los goldens ejecutan funciones puras con vectores reales y comparan conjuntos
  por igualdad, no por presencia; anclan cuerpos enteros, no líneas; derivan
  censos en vez de enumerar.
- Cada golden nuevo se prueba con mutaciones por copia (mínimo media docena,
  todas en rojo).
- Parada escrita en el prompt de cada revisor: **solo pide corregir por defecto
  de conducta, assert que no muerde, golden en rojo o afirmación de doc falsa; lo
  residual va a ficha.** Sin esa parada, las rondas no convergen.

## 6. Reglas de higiene

- Las actas se escriben desde un archivo de hechos medidos, nunca de memoria.
- Los agentes nunca teclean credenciales; lo que exige login se reporta
  «requiere al usuario». Secretos solo como prefijo.
- Ante un fallo o corte: diagnóstico primero y nunca rehacer; se relanza el mismo
  script con el estado previo descrito.
- Pausa segura = detener tareas, dejar el árbol sin commitear pero descrito, y
  anotar en memoria cómo retomar.
- Memoria actualizada en cada hito.

## 7. Detalles del Workflow tool

- Un script determinista por fase, con `phase()` por eslabón.
- `schema` para que cada agente devuelva JSON validado.
- Modelo y esfuerzo explícitos por agente.
- `parallel` solo para los lentes.
- Sin backticks dentro de los prompts.
- Al fallar a medias, se reanuda con `resumeFromRunId` o se relanza con el
  prompt del ejecutor amendado.

## Convenciones de este repo (por defecto; se cambian si el usuario lo pide)

- Planes prescriptivos: `docs/planes/<nombre>.md`.
- Hechos medidos y actas: `docs/actas/<AAAA-MM-DD>-<fase>.md`, generados desde
  el archivo de hechos de la sesión (scratchpad), nunca de memoria.
- Fichas de lo residual (hallazgos que no cumplen la parada del §5):
  `docs/fichas.md`, una entrada por hallazgo con fecha y origen.
- Goldens: en `tests/`, como el resto de la suite (`python3 -m unittest discover -s tests -t .`).
- Idioma: todo en español (docs, mensajes, comandos, boletos); el usuario opera
  el sistema con personal no técnico.

## Contexto del producto

Ruleta de premios para el restaurante Asadero 33: Raspberry Pi 5, botón arcade
JUGAR más botón HABILITAR del mesero, impresora térmica de 80 mm y sin pantalla.

**EL EVENTO ABRE EL LUNES 2026-09-21 A LAS 12:00, Y ESA MAÑANA EL KIOSCO QUEDÓ
VERIFICADO EN EL SITIO.** Entre las 08:20 y las 08:35, en el asadero, se dio de
alta la Wi-Fi del restaurante en la Pi, se comprobó que la hora estaba
sincronizada y **el usuario leyó en papel la fecha del boleto de inventario**:
«sí, el boleto dice 21/09/2026 08:22». Lo medido llega **hasta las 08:35**: de la
apertura misma, y de cualquier jugada del evento, **no hay nada medido en este
repositorio**. Acta: `docs/actas/2026-09-21-apertura.md`.

*(Actualizado el 2026-09-21 por la mañana con lo medido **en el asadero** el día
de la apertura —la red del restaurante dada de alta por el usuario, el arranque
en frío visto por primera vez en el sitio y con la red real, y la fecha del
boleto confirmada en papel—. Antes, el 2026-09-16 por la tarde, con lo medido en
la **Fase 4e**, la pasada final antes del evento —las fechas de vigencia
cargadas, la espera de la
hora en 300 s con rastro en el journal, la pieza D probada en un arranque en frío
real y el inventario reiniciado a folio `00000`—; **con eso el kiosco quedó listo
para el evento**. Antes, el mismo día, con las Fases 4b, 4c y 4d —los premios
reales, el consuelo con peso propio y el reparto por horas, con sus franjas, su
horario y la espera de la hora al arrancar—. Antes, el 2026-09-15, con las Fases
3 y 4a (botones, papel, red y hora); y el 2026-09-11 se había corregido lo de
«impresora Bluetooth» y «valores sin confirmar». Evidencia:
`docs/actas/2026-09-11-fase-2.md`, `docs/actas/2026-09-15-fase-3.md`,
`docs/actas/2026-09-15-fase-4a.md`, `docs/actas/2026-09-16-fase-4bcd.md`,
`docs/actas/2026-09-16-fase-4e.md` y `docs/actas/2026-09-21-apertura.md`.)*

- **La impresora es una AOMU My-A1, que es un clon POS-80** (ESC/POS). Medido en
  la Pi: USB `0418:5011` e `ieee1284_id` =
  `MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1`, es decir **emulación EPSON**.
  El PPD del driver del fabricante la llama **Zjiang ZJ-80250**; eso sale del
  PPD, no del aparato.
- **Va conectada por cable USB:** `impresora.tipo = "archivo"` y
  `impresora.ruta = "/dev/ruleta-impresora"` (nombre fijo que crea una regla
  `udev` por VID:PID, con grupo `lp`). **El Bluetooth queda solo como respaldo**,
  escrito pero nunca ejercido en hardware.
- **Valores confirmados en hardware** (papel en la mano, 2026-09-11): tabla de
  acentos **19 (`cp858`)**, **48 columnas**, **corte automático** y zumbador que
  da **un pitido corto por comando `ESC B`** —ignora cantidad y duración—, con
  `"beep": true` = un pitido al final de cada boleto.
- **Botones, cableados y probados en hardware el 2026-09-15** (Fase 3):
  **JUGAR** en **GPIO 17 (pin 11)** y **HABILITAR** en **GPIO 27 (pin 13)**, los
  dos contra tierra, con las **tierras en los pines 9 y 25**. Los tres boletos de
  prueba salieron con jugadas reales, y el cooldown y la compuerta del mesero se
  vieron morder en el journal. **No hay ningún LED conectado**, aunque
  `config.json` sigue diciendo `"led": 22` —`gpiozero` no falla por eso— y **esa
  es hoy la única señal de error que el programa tiene prevista**, así que una
  jugada rechazada **no se percibe** (fichas **F-240** y **F-256**). Diagrama:
  `docs/cableado-botones.svg`.
- **Papel: la impresora habla sin parar, y solo una pregunta se entera.** La
  AOMU repite por el endpoint de lectura **el último byte de estado** que fijó su
  firmware (~21 kB/s), así que leer un byte tras un `DLE EOT` devuelve la
  respuesta a la **pregunta anterior**. Medido el 2026-09-15: con el rollo fuera,
  **`DLE EOT 4` y `DLE EOT 1` son ciegos en este clon** —siguen contestando
  `0x12` y `0x16`— y **solo `DLE EOT 2`, bit 5 (`0x32`), reporta el fin de
  papel**. Desde **`2a0aba3`** el programa **drena lo viejo, pregunta y se queda
  con el último byte válido**, y con eso **se niega a jugar sin papel**: no
  imprime, devuelve el premio al inventario y no deja nada retenido en la
  impresora (probado en vivo el 2026-09-15 a las 21:32; evidencia:
  `docs/actas/2026-09-15-fase-4a.md`). El viejo aviso de «poco papel» era un
  artefacto de esa lectura y **ya no aparece**.
- **Red y hora. Decisión del usuario del 2026-09-15:** en el evento **la Pi
  tendrá el internet del asadero**, que es lo que le pone la hora al arrancar
  (NTP), y **NO habrá batería RTC**. El riesgo que eso acepta tiene nombre: en
  los **primeros minutos tras encender** —unos tres, medidos el 2026-09-15— la Pi
  **cree que es otro día**, y de la fecha dependen los topes diarios, las fechas
  `desde`/`hasta` y el boleto de inventario de arranque. La mitigación es la
  **pieza D**, que **ya existe desde `613f875`** (2026-09-16, Fase 4d): al
  arrancar, el kiosco espera hasta `juego.espera_hora_seg` segundos —**desde
  `70bcaa6` (2026-09-16, Fase 4e) son 300**, cinco minutos, preguntando cada
  2 s— a que el sistema sincronice la hora, y si no lo consigue **arranca igual**
  pero deja un WARNING en el journal e imprime la línea **`HORA SIN CONFIRMAR:
  revisar fecha`** en el boleto de inventario.
  **F-241 queda resuelta en lo esencial.** Dos avisos: **esto solo pasa al
  arrancar** —ninguna jugada vuelve a esperar— y **la línea del boleto no se ha
  impreso nunca en papel**. *(Nota fechada, 2026-09-16, Fase 4e: hasta ese día
  aquí decía además que **la pieza D nunca se había visto morder en la Pi**. **Ya
  se vio.** El usuario **desenchufó la Pi** unos minutos y la volvió a enchufar:
  sin batería el reloj arrancó en **1970** y encima le cayó la última hora
  guardada, **4 min 54 s atrasada** —la restaura **systemd** desde
  `/var/lib/systemd/timesync/clock`; `fake-hwclock` **no está instalado**—. Con
  esa fecha falsa el kiosco **no imprimió nada**: **esperó 28.3 s**, la hora
  llegó por NTP y **el inventario salió 0.6 s después, con la fecha correcta**,
  sin `HORA SIN CONFIRMAR`, `NRestarts=0` y `estado.json` intacto. El orden que
  pidió el usuario —Pi → internet → hora → inventario → listo— **se cumple**.
  Desde `70bcaa6` la espera además **deja rastro en el journal**: una línea al
  empezar, otra cada 10 s y una última con lo que costó; la primera vez que esa
  última línea se vio en la Pi, el 16 a las 14:44, decía «Hora sincronizada
  tras 0 s». Evidencia:
  `docs/actas/2026-09-16-fase-4e.md` §4 y §8.)* *(Nota fechada, **2026-09-21**,
  la mañana de la apertura: **el arranque en frío se vio también EN EL ASADERO,
  con la red real**, que era la única incógnita que quedaba. La Pi encendió allá
  creyendo que era el **16 de septiembre a las 15:46** —unos **4 días y 17 horas
  atrasada**—, **esperó 28 s** sin imprimir nada, la hora llegó por la Wi-Fi del
  restaurante y el inventario salió a las **08:22:21 con folio `00000`** y sin
  `HORA SIN CONFIRMAR`. **La red del asadero tardó lo mismo que la de casa.**
  Dos estrenos: **los avisos de los 10 s se vieron por primera vez en hardware**
  —a los 10 s y a los 20 s— y **el usuario leyó la fecha EN PAPEL** por primera
  vez tras un arranque en frío en el sitio: «sí, el boleto dice 21/09/2026
  08:22». Hasta ese día aquí decía que esos avisos **no se habían visto en la
  Pi**; ya se vieron. **Lo que sigue sin verse en hardware es solo esto:** el
  tope de 300 s **nunca se ha agotado** y la línea `HORA SIN CONFIRMAR: revisar
  fecha` **nunca se ha impreso en papel**. Y un aviso para leer el journal
  durante el evento: tras un arranque en frío el mismo proceso deja líneas con
  **dos fechas distintas** y `systemctl status` dice que el servicio arrancó el
  día viejo —no es avería, ficha **F-279**—. Evidencia:
  `docs/actas/2026-09-21-apertura.md` §3 y §4.)* **La regla práctica sigue en pie, y es la que manda:** encender la Pi
  unos minutos antes de abrir y **mirar la fecha del boleto de inventario**; si
  está mal, **no reiniciar**, esperar y pedir otro inventario. *(Nota fechada:
  hasta el 2026-09-15 este párrafo decía que **en producción la Pi va sin red**
  y que **por eso la batería RTC es necesaria**. La
  decisión del usuario lo derogó; se conserva aquí porque hay fichas viejas que
  todavía razonan desde esa premisa. Ficha **F-242**.)*
  **La red del evento ya está dada de alta, y tiene nombre:** el **2026-09-21**,
  en el asadero, **el usuario** levantó el punto de acceso de su laptop para
  entrar por SSH y **tecleó él mismo la contraseña** del Wi-Fi del restaurante.
  La Pi conoce hoy **tres** perfiles: **`asadero`** = SSID
  **`INFINITUM04F0_2.4`**, con **prioridad 30**, que es la del local y la que
  gana; `casa` = `SL-Durazo` (**20**), la de las pruebas; y `miltimex` (**10**),
  el **punto de acceso móvil de Windows** de la laptop del usuario, que **sigue
  siendo la red de laboratorio**. **Ojo: no existe ninguna red llamada
  «asadero»** —es el nombre del perfil dentro de la Pi—. Verificado el
  2026-09-21 a las 08:26: la Pi en `INFINITUM04F0_2.4` (2.4 GHz), IP
  `192.168.1.94/24`, internet OK y `timedatectl` → `synchronized yes`. Fichas
  **F-275** y **F-278**, cerradas. *(Nota fechada, 2026-09-21: hasta ese día aquí
  se decía que el punto de acceso de la laptop llevaba **el mismo nombre y
  contraseña** que el Wi-Fi del asadero y que por eso la Pi entraba sola. **No es
  así**: el punto de acceso se llama «Miltimex 5G» y el del restaurante
  `INFINITUM04F0_2.4`, y en la Pi son **dos perfiles distintos**.)*
- **El inventario YA ESTÁ EN CERO y el kiosco queda listo.** El 2026-09-16 se
  reinició **tres veces**, siempre con el servicio parado y con respaldo fechado
  en `datos/`: a las **00:10** al desplegar los premios reales (de folio 16 a
  00000; `estado_20260916_001053.json` y `boletos_20260916_001053.csv`), a las
  **12:46** para probar limpio el reparto por horas (de folio 6 a 00000;
  `estado_20260916_124629.json` y `boletos_20260916_124629.csv`) y **por última
  vez a las 14:44**, en el deploy de la Fase 4e y **después
  de que el usuario dijera que ya había terminado de probar**: de **folio 00010
  con 2 premios entregados** —una cerveza y un agua— a **`Folio en 00000`**, con
  respaldos `datos/estado_20260916_144415.json` y
  `datos/boletos_20260916_144415.csv`. El servicio arrancó a las **14:44:37** y
  el verificador leyó en vivo «Inventario impreso (arranque). Folio actual
  **00000**». **El reinicio del lunes 21 ya no hace falta** —con las fechas
  cargadas ningún premio puede salir antes del 21, así que lo único que avanzaría
  es el folio—: hacerlo es **decisión del usuario** (fichas **F-243**, cerrada, y
  **F-262**). **Ojo:** `reiniciar` respalda `estado.json` y `boletos.csv`, **no
  `ruleta.log`**, y `boletos.csv` se **mueve** al respaldo y se vuelve a crear
  con el primer boleto, así que entre el reinicio y la primera jugada **ese
  archivo no existe** y **eso no es una avería** (ficha **F-277**).
- **Cómo se reparten los premios (Fases 4b, 4c y 4d, 2026-09-16).** Es el modelo
  con el que abre el evento, y está probado en vivo: después del reinicio de las
  12:46 el usuario jugó y dijo «ya probé, salieron consuelos y una cerveza,
  funciona bien».
  - **Siete premios reales**, 167 piezas y **34 de cupo diario sumado** (33 sin
    la hielera): `hielera` HIELERA IGLOO «Premio mayor» (2/1/1), `silla` SILLA DE
    PLAYA «Premio grande» (10/2/2), `bbq` SET BBQ «Premio grande» (10/2/2),
    `tacos3` 3 TACOS DE PASTOR «Plato de 3 tacos de pastor» (20/4/4), `tacos2`
    2 TACOS DE PASTOR «Plato de 2 tacos de pastor» (20/4/4), `cerveza` CERVEZA
    **«Tecate Light, Tecate Roja o Indio»** (50/10/10) y `agua` AGUA FRESCA
    **«Horchata, Jamaica o Cebada»** (55/11/11), en `stock`/`tope_diario`/`peso`.
    Los siete nombres y detalles los **confirmó el usuario el 2026-09-16**
    (ficha **F-260**).
  - **Horario del evento 12:00–23:00**, con el **cierre exclusivo** (a las 23:00
    en punto ya no se juega). **Fuera de él no hay ningún premio disponible y la
    jugada sale de consuelo**, que es lo que el usuario eligió; la otra opción,
    `"fuera_de_horario": "no_jugar"`, existe y **no se usa**.
  - **Franjas:** la **hielera** solo de **19:00 a 23:00**; la **silla** y el
    **set BBQ**, una pieza de **13:00 a 16:00** y otra de **19:00 a 22:00**. Un
    premio con franjas **no existe fuera de ellas**.
  - **Tacos, cerveza y agua se reparten por los PUNTOS MEDIOS del cupo diario:**
    la pieza *k* se abre en `abre + (k − 0.5) × (cierra − abre) / tope_diario`.
    Con el `config.json` de hoy: agua a las 12:30, 13:30 … 22:30; cerveza a las
    12:33, 13:39 … 22:27; los dos platos de tacos a las 13:22:30, 16:07:30,
    18:52:30 y 21:37:30. **Lo que se abre y no se gana no se pierde, pero
    tampoco adelanta la siguiente pieza.**
  - **El consuelo compite con peso 10** contra lo que esté abierto en ese
    momento (no contra el cupo del día entero: por eso bajó de 217 a 10).
  - **Separación mínima de 3 minutos** entre dos boletos **con premio**. El
    instante del último se guarda en `datos/estado.json`, así que **sobrevive a
    un reinicio**; un reloj que se va hacia atrás **no** bloquea el juego.
  - **Al arrancar, el kiosco espera hasta 300 s** —cinco minutos, desde
    `70bcaa6`; antes eran 120— a que la hora esté sincronizada, y si no lo
    consigue imprime **`HORA SIN CONFIRMAR: revisar fecha`** en el boleto de
    inventario.
  - **Las fechas `desde`/`hasta` YA ESTÁN CARGADAS** desde `70bcaa6`
    (2026-09-16, Fase 4e; ficha **F-259**, cerrada): la **hielera** solo el
    **jueves 24 y el viernes 25**, y los otros seis del **lunes 21 al viernes
    25**. **Consecuencia, y es la correcta: hasta el lunes 21 ninguna jugada
    puede dar premio**, todas salen de **consuelo**; eso **no es una avería**.
    *(Nota fechada: hasta el 2026-09-16 este punto decía que las fechas
    **todavía no** estaban cargadas y que por eso los siete premios entraban
    **todos los días**. Se conserva porque hay fichas viejas que razonan desde
    esa premisa.)*
  - Evidencia de todo lo anterior: `docs/actas/2026-09-16-fase-4bcd.md` y
    `docs/actas/2026-09-16-fase-4e.md`, y el documento que manda sobre
    `config.json`, `docs/evento-2026-09-asadero-33.md`.

Ver `README.md` para operación e instalación, y `docs/actas/` para la evidencia
medida de cada uno de estos valores.
