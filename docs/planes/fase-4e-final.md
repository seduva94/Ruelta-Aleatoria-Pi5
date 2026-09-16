# Fase 4e · Pasada final antes del lunes 21 (fechas, espera de hora y registro)

Plan prescriptivo. Redactado el **2026-09-16**, **antes** de tocar una sola línea
de código. Es la **última pasada de programación antes del evento**: carga las
fechas de vigencia que faltaban, sube la espera de la hora al arrancar y hace que
esa espera **se vea en el journal**. No inventa funciones nuevas.

**Desviación anotada del protocolo (§3 de `CLAUDE.md`), igual que en la Fase 4d:**
esta fase se hace en **una sola pasada** del ejecutor —plan, `config.json`,
documento del evento, código, goldens, mutaciones y docs en el mismo cambio— y el
plan se commitea **junto con** el código. Motivo: el usuario **ya terminó de
probar** y pidió «dejar todo listo para el lunes». Los eslabones de revisión
(lentes, escéptico, commit compuertado, deploy y verificación en vivo) **no se
saltan**: van después, como siempre.

**ESTADO GLOBAL (2026-09-16, tras el paso del ejecutor).** **PLAN, `config.json`,
DOCUMENTO DEL EVENTO, CÓDIGO, GOLDENS, MUTACIONES, FICHAS Y DOCS HECHOS; SIN
COMMITEAR Y SIN DESPLEGAR.** Las casillas **0 a 6** de la §0 están marcadas con su
evidencia; las **7 a 11** son de otros eslabones de la cadena. La suite pasó de
**268** a **273** pruebas en verde y **las diez mutaciones del §5 quedaron en
rojo**, tres de ellas mutando **`config.json`** o **el documento del evento** y no
el código, que es lo que demuestra que los goldens **derivan** de verdad. **Lo que
esta fase promete sigue sin medirse contra la Pi:** hasta el Paso 9 (deploy), lo
único demostrado es que en la PC las fechas sacan a los siete premios antes del
lunes 21 y que la espera de la hora deja las líneas que dice el §2.

**ESTADO GLOBAL (2026-09-16, al escribir el plan; se conserva).** **FASE 4e ABIERTA.** Árbol
limpio en `main` sobre **`da1385e`** (cierre documental de las Fases 4b, 4c y
4d), `HEAD` = `origin/main`, **19** commits. Suite: **268 pruebas OK** en la PC.
En la Pi corre `613f875` (código) con los docs por detrás. El inventario de la Pi
**se reinicia en el deploy de esta fase**.

## Por qué existe esta fase

1. **Las fechas `desde`/`hasta` nunca se cargaron** (ficha **F-259**). Sin ellas
   **la hielera puede salir el lunes 21**, cuando el dictado del usuario dice que
   es del **jueves 24 y el viernes 25**. Fecha límite: **antes del lunes 21**.
2. **La espera de la hora se midió en hardware el 2026-09-16** —arranque en frío,
   sin batería RTC— y funcionó: el reloj arrancó **4 min 54 s atrasado**, el
   programa esperó **28.3 s** y el inventario salió **0.6 s después** de la
   sincronización, con la fecha correcta. Pero esos 28 s se midieron **en casa**,
   contra un servidor NTP por **IPv6**. **La red del asadero puede tardar más**, y
   el tope de 120 s no tiene margen medido.
3. **Esos 28 s fueron 28 s de silencio en el journal** (ficha **F-273**): hoy no
   hay forma de distinguir «la hora se confirmó a la primera» de «costó 90
   segundos» más que por la ausencia de líneas.

## Fuente de verdad

`docs/evento-2026-09-asadero-33.md`. Manda sobre `config.json` y sobre este plan
(su §6, paso 1). Los hechos medidos de esta fase están en
`docs/actas/2026-09-16-hechos-medidos-fase-4e.md` (copia literal del archivo de
hechos de la sesión, con su tamaño y su `sha256`).

## Convención de comandos (idéntica a las Fases 1 a 4d; se repite porque muerde)

- En **esta PC** el intérprete se llama **`python`**. En la **Pi** se llama
  **`python3`**. Un `python3` tecleado en Windows abre la Tienda de Microsoft.
- Suite: `python -m unittest discover -s tests -t .` (en la Pi, `python3`).
- **El ejecutor no corre ningún `git` que modifique.**

---

## 0. Bitácora

`[x]` = hecho **y** con su criterio de aceptación cumplido. `[~]` = hecho pero
sin verificar. `[ ]` = pendiente. **Las casillas se marcan desde salidas de
comando pegadas, nunca de memoria.**

| # | Paso | Quién | Estado |
|---|---|---|---|
| 0 | Este plan, escrito **antes** del código | ejecutor | `[x]` 2026-09-16 |
| 1 | **D1 D2** `config.json`: las siete fechas y `espera_hora_seg` 300 | ejecutor | `[x]` 2026-09-16 (el validador real carga las **siete** parejas —hielera 24-25, los otros seis 21-25— y `espera_hora_seg` **300.0**, sin un solo error) |
| 2 | **D1 D2** Documento del evento: §5.1 y §5.2 al día (fechas cargadas, 300 s, reloj medido) | ejecutor | `[x]` 2026-09-16 (§5.1: las fechas **cargadas** y la consecuencia escrita —«hasta el lunes 21 toda jugada sale de consuelo»—, bloque juego a **300** y nota fechada del arranque en frío; §5.2 **D** a 300 y el registro nuevo; §6 paso 5 al día; fila nueva en la bitácora del §7) |
| 3 | **D3** `ruleta/app.py`: registro de la espera de la hora | ejecutor | `[x]` 2026-09-16 (constante `PERIODO_AVISO_HORA = 10.0` y tres `log.info`; con `espera_hora_seg` = 0 **no registra nada**; ni el tope, ni la consulta cada 2 s, ni el aviso del boleto cambiaron) |
| 4 | **D1 D3** Goldens nuevos por igualdad (fechas derivadas del documento y mensajes del journal) | ejecutor | `[x]` 2026-09-16 (**268 → 273** pruebas OK; `desde`/`hasta` dentro de `CLAVES_DEL_DOCUMENTO`, censo de fechas por igualdad, calendario con el motor de producción y cuatro goldens de journal con `assertLogs`) |
| 5 | **D3** Mutaciones **sobre copia**, mínimo 6, **todas en rojo** | ejecutor | `[x]` 2026-09-16 (**diez**, las diez en rojo y cada una con el test que dice la tabla; copia limpia en verde con 273) |
| 6 | **D4 D5** `README.md`, plan de la 4d, fichas y acta de hechos medidos | ejecutor | `[x]` 2026-09-16 (`README.md` §2, §5 —párrafo para el personal—, §7 y §9; nota fechada en la **D6** del plan de la 4d; **F-259** y **F-273** cerradas, **F-241** y **F-262** con nota fechada, **F-275** y **F-276** nuevas; acta `docs/actas/2026-09-16-hechos-medidos-fase-4e.md` con tamaño y `sha256`) |
| 7 | Revisores en paralelo, correctivo y escéptico | revisores | `[ ]` |
| 8 | Commit compuertado (conjunto de archivos del §6 de este plan) | agente de commit | `[ ]` |
| 9 | Deploy en la Pi **con reinicio del inventario** (§8) | agente de deploy | `[ ]` |
| 10 | Verificación en vivo contra lo desplegado | verificador | `[ ]` |
| 11 | Acta, fichas de cierre y memoria | escriba / orquestador | `[ ]` |

---

## 1. Objetivo

Que el lunes 21 el kiosco se encienda y **no haya nada que tocar**:

1. Cada premio **sabe qué días existe** (`desde`/`hasta`), y la hielera no puede
   salir antes del jueves 24.
2. Al encender, el kiosco espera **hasta 5 minutos** a tener la hora buena, y
   **lo dice en el journal**: cuándo empieza a esperar, cada ~10 s que sigue
   esperando, y cuánto costó.
3. Los documentos que lee el personal (`README.md` §5 y §7, documento del evento)
   dicen **lo que el programa hace de verdad**, incluido que **hasta el lunes 21
   toda jugada da consuelo**.

---

## 2. Decisiones cerradas (no se discuten aquí; se implementan)

### D1 · Fechas de vigencia en `config.json` (cierra **F-259**)

Se copian **del §5.1 del documento**, que ya las trae:

| Premio | `desde` | `hasta` |
|---|---|---|
| `hielera` | `2026-09-24` | `2026-09-25` |
| `silla`, `bbq`, `tacos3`, `tacos2`, `cerveza`, `agua` | `2026-09-21` | `2026-09-25` |

Formato `AAAA-MM-DD`, que es el que ya valida `ruleta/config.py`.
**Consecuencia aceptada y documentada:** desde que esto se despliega y hasta el
**lunes 21**, **toda jugada da boleto de consuelo**, porque ningún premio está
dentro de fechas. No es una avería: se escribe en `README.md` §5 y en el §5.1 del
documento del evento.

### D2 · `juego.espera_hora_seg`: 120 → 300

Medido el 2026-09-16 en casa: la sincronización NTP tardó **34 s** contra un
servidor **IPv6**. En la red del asadero puede tardar distinto y **no está
medido**. 300 s es margen, no coste: si la hora llega en 3 s, el kiosco arranca
en 3 s. Se cambia en `config.json` **y en los dos bloques del documento**
(§5.1 `"juego"` y §5.2 PENDIENTE D), porque los goldens derivan de ahí.

### D3 · Registro de la espera de la hora (cierra **F-273**)

En `ruleta/app.py`, `esperar_hora_sincronizada()`:

- **Al empezar la espera**, un `log.info`:
  `Esperando a que la hora se sincronice (hasta N s)…`
- **Cada ~10 s** mientras espera, un `log.info` con los segundos transcurridos.
- **Al terminar**, un `log.info` con lo que costó:
  `Hora sincronizada tras X s` —o el `log.warning` **HORA SIN CONFIRMAR** que ya
  existe, si se agotó el tope.
- **Con `espera_hora_seg` = 0 no se registra absolutamente nada**, porque no se
  espera nada. Un `log.info` ahí sería ruido en cada arranque de cualquier
  instalación que no use la pieza D.

**No cambia la política:** el tope, el periodo de consulta (2 s), el aviso del
boleto y el hecho de que **ninguna jugada espera nada** siguen igual. El
comprobador sigue siendo **inyectable** (`hora_sincronizada=`), que es lo que
permite anclar los mensajes con un reloj falso.

### D4 · Docs que hay que poner al día

- **`fake-hwclock` no está instalado en esta Pi.** Quien restaura la hora vieja
  al arrancar es **systemd**, desde la marca `/var/lib/systemd/timesync/clock`
  («System time advanced to timestamp on /var/lib/systemd/timesync/clock»).
  **Re-grep obligatorio** (`grep -rni "hwclock" .`) antes de editar: cualquier
  texto del repositorio que se lo atribuya a `fake-hwclock` es **falso** y se
  corrige con **nota fechada**. **No se tocan `CLAUDE.md` ni las actas**: son
  evidencia; lo que digan se anota en fichas y se le reporta al orquestador.
- **`README.md` §5**, un párrafo corto para el personal: al encender, la Pi
  **espera hasta 5 minutos** a tener la hora por internet antes de imprimir el
  inventario; si el boleto dice **HORA SIN CONFIRMAR**, revisar el internet y
  pedir **otro inventario** (HABILITAR 6 s) **antes de abrir**; y los premios
  **solo salen del 21 al 25 de septiembre, de 12:00 a 23:00**.
- **`README.md` §7** y el documento del evento: donde diga «120» o «2 minutos»
  hablando de la espera, **300** y «5 minutos», con la medición que lo justifica.

### D5 · Plan, acta de hechos y fichas

- Este plan, **antes** del código.
- Copia **literal** del archivo de hechos de la sesión a
  `docs/actas/2026-09-16-hechos-medidos-fase-4e.md`, con cabecera de **tamaño** y
  **sha256** del original.
- Fichas (`docs/fichas.md`, numeración consecutiva; **re-grep**
  `grep -n "^## F-" docs/fichas.md | tail -3` antes de escribir):
  - **F-259** se **cierra**: las fechas están cargadas.
  - **F-273** se **cierra**: el registro existe y tiene goldens.
  - **F-241** recibe **nota fechada**: su riesgo quedó **cerrado en hardware**
    con el arranque en frío del 2026-09-16.
  - **F-262** se **actualiza**: el inventario se reinicia en el deploy de esta
    fase y, **con las fechas cargadas ya no puede salir un premio antes del
    lunes**, así que **no hace falta** otro reinicio el 21 salvo que el usuario
    quiera el folio en cero.
  - **Fichas nuevas** para lo residual que aparezca (perfil Wi-Fi del asadero,
    afirmaciones de `CLAUDE.md` que esta fase deja desfasadas).

### D6 · Goldens y mutaciones

- Goldens **por igualdad**, nunca por presencia, y **derivados** del documento
  del evento donde ya hay costumbre de hacerlo.
- El golden que anclaba que los premios **todavía no** traen fechas
  (`tests/test_config.py`) **pasa a anclar las fechas reales**: censo por
  igualdad (hielera 24-25, los otros seis 21-25) **y** las llaves `desde`/`hasta`
  añadidas a `CLAVES_DEL_DOCUMENTO`, con lo que la comparación campo por campo
  contra el §5.1 las cubre. **No se relaja la comparación.**
- Los mensajes del journal se anclan **por igualdad de lista** con `assertLogs` y
  el reloj falso (0 s, 10 s, 20 s), más el caso del **tope agotado** y el caso de
  **`espera_hora_seg` = 0** (que no registra nada).
- **Mutaciones sobre copia, mínimo 6, todas en rojo** (§5).

---

## 3. Trampas de este repositorio (un ejecutor sin contexto no las adivina)

1. **Hay goldens que DERIVAN del documento del evento.**
   `tests/test_config.py::TestPremiosOficialesDelEvento` parsea los bloques de
   código `json` del documento y los compara campo por campo con lo que
   `ruleta/config.py` carga de `config.json`. Cambiar uno sin el otro **pone la
   suite en rojo, y está hecho a propósito**. Los bloques se localizan **por su
   contenido** (por la llave con la que empiezan), no por el número de sección.
2. **Las fechas no viajan igual por los dos lados.** El documento las trae como
   **texto** (`"2026-09-21"`) y el validador las carga como `datetime.date`. Al
   añadirlas a la comparación hay que **normalizar** (como ya hace `como_dict`
   con las franjas), **no** aflojar el assert.
3. **`tests/__init__.py` apaga el registro** (`logging.disable(CRITICAL)`), así
   que `assertLogs` y `assertNoLogs` **no ven nada** si no se vuelve a encender
   (ficha **F-253**). `tests/test_escpos.py` ya tiene el patrón: el
   contextmanager `registro_activo()`. Se **reutiliza o se replica**; lo que no
   se hace es anclar mensajes con el registro apagado.
4. **El reloj de las pruebas es falso y hay que hacerlo avanzar.**
   `tests/test_app.py::TestRuleta.reloj_que_avanza()` devuelve un `dormir` que
   además mueve el reloj: sin él, la espera de la hora no avanza nunca.
5. **`liberadas` y `proxima_liberacion` NO miran `desde`/`hasta`.** Las fechas
   solo entran por `motivo_no_disponible`. Por eso cargar las fechas **no cambia**
   los goldens del reparto por horas de `tests/test_ticket.py`, que están fechados
   el **2026-09-15**; lo que sí cambia es que **ningún premio está disponible** ese
   día, y con eso la probabilidad del consuelo pasa a **100 %**. Si algún golden
   se cae por eso, se **recalcula con la misma regla**, no se afloja.
6. **`python` en la PC, `python3` en la Pi.**
7. **LF siempre.** `.gitattributes` normaliza `*.py`, `*.md` y `*.json`; el árbol
   de trabajo en Windows puede quedar con CRLF. Lo que se commitea es **LF**.
8. **Anclas que DERIVAN: re-grep antes de cada edición.** Los números de línea se
   mueven. Buscar por texto: `grep -rn "espera_hora_seg" .`,
   `grep -rni "hwclock" .`, `grep -n "^## F-" docs/fichas.md | tail -3`,
   `grep -n "esperar_hora_sincronizada" ruleta/app.py`.

---

## 4. Pasos, cada uno con su criterio de aceptación

**Paso 1 · `config.json` (D1, D2).** Añadir `desde`/`hasta` a los siete premios y
poner `"espera_hora_seg": 300`.
*Criterio:* cargar `config.json` con el validador real imprime las siete parejas
de fechas y **300.0**, sin un solo error.

**Paso 2 · Documento del evento (D1, D2).** §5.1: el bloque `"juego"` con
`"espera_hora_seg": 300`, el texto que decía que las fechas **faltan** reescrito a
que **están cargadas**, y el párrafo «Sobre el reloj» con los **5 minutos** y lo
medido en el arranque en frío. §5.2 PENDIENTE D: `"espera_hora_seg": 300` y el
mismo cambio de minutos. Encabezado de «Las cuatro piezas»: 5 minutos.
*Criterio:* en `docs/evento-2026-09-asadero-33.md` no queda ninguna línea que diga
«120» o «2 minutos» hablando de la espera de la hora, y la suite sigue verde.

**Paso 3 · `ruleta/app.py` (D3).** Las tres líneas de registro dentro de
`esperar_hora_sincronizada()`, con una constante nueva para el periodo del aviso.
*Criterio:* la función sigue devolviendo `True`/`False` igual que antes; con
`espera_hora_seg` = 0 **no registra nada**; ningún otro método cambia.

**Paso 4 · Goldens (D6).** En `tests/test_config.py`, las fechas; en
`tests/test_app.py`, los mensajes.
*Criterio:* suite **en verde** y con **más pruebas que antes** (268 al empezar).

**Paso 5 · Mutaciones (D6).** Las del §5, **sobre copia**, ejecutadas de verdad.
*Criterio:* copia limpia en verde y **todas las mutaciones en rojo**, cada una con
el test que dice la tabla.

**Paso 6 · Docs (D4, D5).** `README.md` §5 y §7, nota fechada en el plan de la
Fase 4d, fichas y acta de hechos medidos.
*Criterio:* `grep -rni "hwclock" .` no devuelve ninguna afirmación falsa;
`README.md` §5 trae el párrafo del personal; `docs/fichas.md` cierra **F-259** y
**F-273**.

---

## 5. Mutaciones que hay que poner en rojo (sobre copia, mínimo 6)

Se hacen **sobre una copia del repositorio**, nunca sobre el árbol de trabajo, y
se ejecutan de verdad. Cada una debe caer con **el test que dice la tabla**.

**Ejecutadas el 2026-09-16** con el arnés `scratchpad/mutar.py` (el mismo de la
Fase 4d, reapuntado), que copia el repositorio a
`C:/Users/seduv/AppData/Local/Temp/mut4e/<Mn>` y corre la suite entera en cada
copia. **Copia limpia: 273 pruebas en verde. Las diez mutaciones: ROJO, y en las
diez cayó el test esperado.** (La **M6** se escribió dos veces: la primera dejaba
el `log.info` **fuera** del `if` y rompía la sintaxis, así que ponía la suite en
rojo **por el motivo equivocado**; corregida, cae en el test que toca y con las
273 pruebas corriendo.)

| # | Qué se muta | Dónde | Test que debe caer | Resultado |
|---|---|---|---|---|
| M1 | se borra el `log.info` **inicial** de la espera | `ruleta/app.py` | `test_la_espera_de_la_hora_se_ve_en_el_journal` | **ROJO** (y otros 2) |
| M2 | se borra el aviso **periódico** de «sigo esperando» | `ruleta/app.py` | `test_la_espera_de_la_hora_se_ve_en_el_journal` | **ROJO** |
| M3 | el periodo del aviso pasa de **10 s a 5 s** | `ruleta/app.py` | `test_la_espera_de_la_hora_se_ve_en_el_journal` | **ROJO** |
| M4 | se cambia el **texto** del mensaje final | `ruleta/app.py` | `test_la_espera_de_la_hora_se_ve_en_el_journal` | **ROJO** (y 1 más) |
| M5 | el mensaje final **no dice cuántos segundos** costó | `ruleta/app.py` | `test_la_espera_de_la_hora_se_ve_en_el_journal` | **ROJO** (y 1 más) |
| M6 | se registra **aunque `espera_hora_seg` sea 0** | `ruleta/app.py` | `test_sin_espera_configurada_no_se_registra_nada` | **ROJO** |
| M7 | agotado el tope, **no** queda el WARNING | `ruleta/app.py` | `test_el_tope_agotado_se_ve_en_el_journal` | **ROJO** |
| M8 | la hielera pasa a `"desde": "2026-09-21"` **en `config.json`** | `config.json` | `test_los_premios_del_config_traen_las_fechas_del_evento` | **ROJO** (y otros 2) |
| M9 | la hielera pasa a `"desde": "2026-09-21"` **en el documento** | `docs/evento-2026-09-asadero-33.md` | `test_config_json_lleva_exactamente_los_premios_del_documento` | **ROJO** |
| M10 | `"espera_hora_seg": 300` → `120` **en `config.json`** | `config.json` | `test_config_json_lleva_el_bloque_de_juego_del_documento` | **ROJO** |

**M8, M9 y M10 son las que demuestran que los goldens DERIVAN**: mutando **solo
el documento** (M9), o **solo `config.json`** (M8, M10), la suite se pone en rojo.

---

## 6. Conjunto de archivos permitido (compuerta del commit)

Exactamente estos, ni uno más:

```
ruleta/app.py
ruleta/config.py
config.json
tests/test_app.py
tests/test_config.py
tests/test_instalacion.py
docs/planes/fase-4e-final.md
docs/actas/2026-09-16-hechos-medidos-fase-4e.md
docs/fichas.md
README.md
docs/evento-2026-09-asadero-33.md
docs/planes/fase-4d-horas.md
```

**Nota fechada (2026-09-16, al terminar el ejecutor):** de esos doce, se tocaron
**once**. **`ruleta/config.py` estaba permitido y NO hizo falta tocarlo**: las
fechas `desde`/`hasta` ya las validaba desde antes (`_fecha`, formato
`AAAA-MM-DD`) y `espera_hora_seg` es un número que el validador ya acotaba a
«no negativo». Es el mismo caso que `ruleta/hardware.py` en la Fase 4d (ficha
**F-272**): que un archivo esté permitido no obliga a cambiarlo, y el agente de
commit **solo añade rutas que existan en el diff**.

---

## 7. Prohibiciones

- **No se toca `CLAUDE.md`** ni ninguna acta ya escrita: son evidencia. Lo que
  esté desfasado se anota en **fichas** y se le reporta al orquestador.
- **No se tocan `ruleta/inventario.py`, `ruleta/ticket.py` ni
  `ruleta/escpos.py`.** El reparto por horas y el papel están cerrados y
  verificados en hardware.
- **No se cambian las franjas, los pesos, los `stock`, los `tope_diario` ni el
  horario del evento.** Son el dictado del usuario.
- **No se cambia la política de la pieza D**: ni la consulta cada 2 s, ni el aviso
  del boleto, ni el hecho de que ninguna jugada espere.
- **No se inventan valores.** Lo que no esté en el §2 de este plan, no entra.
- **El ejecutor no commitea**, y no corre ningún `git` que modifique.

---

## 8. Deploy, para el agente que lo ejecute

1. `git pull --ff-only` en `/home/asadero/ruleta`. **Lo único que puede aparecer
   sin seguimiento es `?? config.json.bak-2026-09-12`.** Si `config.json` aparece
   **modificado**, **NO se fuerza nada**: se **reporta** y se detiene.
2. Suite en la Pi: `python3 -m unittest discover -s tests -t .` desde `~/ruleta`.
3. `sudo -n systemctl stop ruleta`.
4. `python3 -m ruleta reiniciar --si`, **copiando la salida entera** (dice con qué
   nombre respaldó `estado.json` y `boletos.csv`).
5. `sudo -n systemctl start --no-block ruleta`.
6. Verificar **desde una conexión nueva**: `active`, `NRestarts=0`, y en el
   journal las líneas nuevas de la espera de la hora —o, si la hora ya estaba
   sincronizada, **`Hora sincronizada tras 0 s`**—, `Ruleta arrancando. Premios:
   hielera, …`, `Inventario impreso (arranque). Folio actual 00000` y
   `Lista. Esperando jugadas.`.
7. **NO jugar.** Con las fechas cargadas, cualquier jugada anterior al lunes 21
   sale de **consuelo**, y además gastaría folio.

---

## 9. Qué queda abierto al terminar esta fase

- **Sin señal perceptible** cuando una jugada se rechaza: no hay LED conectado
  (**F-240**, **F-256**).
- **El perfil Wi-Fi del asadero** hay que darlo de alta **en sitio**: el perfil
  viejo ya no existe en la Pi.
- **Reinicio del inventario el lunes 21**: ya **no es obligatorio** (las fechas
  impiden que salga un premio antes), pero sigue siendo **decisión del usuario**
  si quiere abrir con el folio en **00000** (**F-262**, **F-243**).
- **`CLAUDE.md`** sigue diciendo **120 s**: no se toca aquí; lo decide el
  orquestador.
