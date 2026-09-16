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

*(Actualizado el 2026-09-15 con lo medido y decidido en las Fases 3 y 4a
—botones, papel, red y hora—. Antes, el 2026-09-11, ya se había corregido lo de
«impresora Bluetooth» y «valores sin confirmar». Evidencia:
`docs/actas/2026-09-11-fase-2.md`, `docs/actas/2026-09-15-fase-3.md` y
`docs/actas/2026-09-15-fase-4a.md`.)*

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
  **pieza D**, que **todavía no existe**: esperar a que la hora esté sincronizada
  antes de imprimir y de aceptar jugadas (ficha **F-241**). Regla práctica
  mientras tanto: encender la Pi unos minutos antes de abrir y **mirar la fecha
  del boleto de inventario**; si está mal, **no reiniciar**, esperar y pedir otro
  inventario. *(Nota fechada: hasta el 2026-09-15 este párrafo decía que **en
  producción la Pi va sin red** y que **por eso la batería RTC es necesaria**. La
  decisión del usuario lo derogó; se conserva aquí porque hay fichas viejas que
  todavía razonan desde esa premisa. Ficha **F-242**.)* La red de **laboratorio**
  sigue siendo el **punto de acceso móvil de Windows** de la laptop del usuario,
  con el mismo nombre y contraseña que el Wi-Fi del asadero; la Pi entra sola.
- **El inventario real NO está en cero:** las pruebas de hardware del 2026-09-15
  lo dejaron en el **folio 16**, con premios de prueba ya contados como
  entregados. **Hay que correr `python3 -m ruleta reiniciar --si` antes del lunes
  21 de septiembre** o esos boletos contarán como premios entregados (ficha
  **F-243**).

Ver `README.md` para operación e instalación, y `docs/actas/` para la evidencia
medida de cada uno de estos valores.
