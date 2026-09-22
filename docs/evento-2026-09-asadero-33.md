# Evento de la ruleta · Asadero 33 · septiembre de 2026

**Fechas:** del **lunes 21 al viernes 25 de septiembre de 2026** (5 días seguidos).
**Horario:** de **12:00 a 23:00**, hora de Hermosillo (`America/Hermosillo`; Sonora
no cambia de horario, así que es la misma hora todo el evento).
**Días con nombre:** 21 lunes · 22 martes · 23 miércoles · **24 jueves** · **25 viernes**.

**Última edición:** 2026-09-16 · Claude (ejecutor), Fase 4d: **cambió el modelo
entero.** Tu dictado de hoy —«**es imposible saber cuántas jugadas habrá**»— tiró
el número **N** en el que se apoyaba todo el §2 viejo. Ahora **los premios se
reparten por HORAS**: el cupo de cada día se va abriendo solo a lo largo de las
once horas del evento. Con eso quedaron **construidas las cuatro piezas** que
faltaban (**A**, **B**, **C** y **D**), se cargaron las **franjas** y el
**horario** en `config.json`, se confirmaron los **siete nombres y detalles**
(quitados los asteriscos) y se respondieron las **preguntas 1 a 6** del §4. Lo
viejo **no se borró**: está como nota histórica en el §2. Lo único que **no** se
cargó son las **fechas `desde`/`hasta`** (ficha **F-259**), porque hoy 16 estás
probando.

*(2026-09-16, más tarde · Claude (escriba), cierre documental de las Fases 4b, 4c
y 4d: **lo único que se añadió fue la última línea de la bitácora del §7**. No se
tocó ninguna tabla, ningún cupo, ninguna probabilidad ni ninguna pregunta del §4.
Acta: `docs/actas/2026-09-16-fase-4bcd.md`.)*

*(2026-09-16, al cerrar el día · Claude (ejecutor), **Fase 4e**: **ya no falta
nada por cargar.** Las **fechas `desde`/`hasta`** que el párrafo de arriba daba
por pendientes **están en `config.json`** —hielera **24 y 25**, los otros seis
**del 21 al 25**— y con ellas **hasta el lunes 21 toda jugada sale de consuelo**,
que es lo correcto (ficha **F-259**, cerrada). También subió a **5 minutos** la
espera de la hora al encender y esa espera **ya se ve en el journal**. Tampoco
aquí se tocó ninguna tabla, ningún cupo, ninguna probabilidad ni ninguna pregunta
del §4. Plan: `docs/planes/fase-4e-final.md`.)*

*(**2026-09-22**, martes por la mañana · Claude (ejecutor), **día 2, paso 1**:
**esta vez SÍ cambiaron tablas, y con tu permiso** («así va»). El lunes 21 se
jugó **55 veces** y **los premios grandes se quedaron en la bodega**: **0 de 2
sillas** y **1 de 2 sets BBQ**. Este paso **no toca el programa**, solo
`config.json`: **la separación entre premios baja de 3 minutos a 1**, el **peso**
de la silla, el set BBQ y la hielera **sube a 100** —para que salgan casi seguro
en cuanto el reloj los abre—, las **franjas se mueven a horas sueltas** repartidas
por la tarde y la noche, y **se repone lo que no salió el lunes** con dos
entradas nuevas de apaño, `silla_extra` y `bbq_extra`. Las tablas del §1, del §2
y del §3 quedan al día. Plan: `docs/planes/dia2-paso1-config.md`.)*

*(**2026-09-22**, martes por la tarde · Claude (ejecutor), **día 2, paso 2**:
**esto sí toca el programa, y cierra lo que el paso 1 no podía hacer.** Dos
cosas, las dos dictadas por ti esta tarde: (1) **cada día tiene SUS horas** —el
programa aprendió `dias` dentro de cada franja, así que ya no hacen falta las
horas del martes para los cuatro días—; y (2) los tres premios grandes salen
**FORZADOS**: «después de tal hora, el próximo juego se la saca», es decir que
**la siguiente jugada se lleva la pieza abierta, sin sorteo y sin esperar el
minuto de separación**. Las tablas del §1 y del §3 quedan con las horas de cada
día; el §5.2 estrena la pieza **E**. Lo que **no** cambió: nombres, detalles,
stocks, cupos, pesos, horario, fechas y el peso del consuelo. Plan:
`docs/planes/dia2-paso2-forzado.md`.)*

---

## Cómo usar este documento

Este es **el documento del evento**: aquí viven los premios, los cupos y las
horas. Está escrito para que **tú lo edites a mano**.

- Las **tablas** del §1 y del §3 son **tu dictado**: los premios, los stocks y
  los cupos los confirmaste el **2026-09-16**; la **reposición** y las **horas
  sueltas**, el **2026-09-22** por la mañana; y las **horas por día** más el
  **premio forzado**, esa misma tarde. *(Los minutos exactos de cada franja los
  puse yo, repartiendo tu «horas sueltas, no redondas»; el reparto por días y la
  regla de «el próximo juego se la saca» son tuyos.)* Las explicaciones, los
  cálculos y los formatos de `config.json` (los §2, §3, §5 y §6) los escribí yo a
  partir de ese dictado y del código.
- Lo que lleve un asterisco **\*** sería una propuesta mía a confirmar. **Hoy ya
  no queda ninguno en las tablas de premios.**
- **No edites `config.json`.** Edita este archivo, avísame, y yo lo convierto en
  `config.json` con la cadena de revisión (§6).

### Las piezas del programa que hubo que construir

Este documento describía cuatro piezas —**A**, **B**, **C** y **D**— que había
que construir para que el evento saliera tal cual, y el día 2 añadió una quinta,
la **E**. **Las cinco están hechas**:

| # | Pieza | Cuándo se construyó |
|---|---|---|
| ~~**A**~~ | ~~**Probabilidad propia del boleto de consuelo**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4c). El consuelo tiene `peso` propio y compite en cada jugada. |
| ~~**B**~~ | ~~**Franjas horarias por premio, con cupo por franja**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4d). Las franjas que rigen hoy están en el §3: el 2026-09-22 por la mañana se movieron a **horas sueltas** y esa tarde pasaron a tener **una hora distinta por día** (pieza **E**). |
| ~~**C**~~ | ~~**Horario del evento (12:00–23:00)**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4d). Fuera de ese horario la ruleta imprime **boleto de consuelo**. |
| ~~**D**~~ | ~~**Esperar a que la hora esté sincronizada al encender**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4d). Al arrancar, la Pi espera hasta **5 minutos** a tener la hora buena; si no la consigue, **lo escribe en el boleto**. (El tope subió de 2 a 5 minutos el 2026-09-16, Fase 4e, tras probarlo con la Pi desenchufada; §5.1.) |
| ~~**E**~~ | ~~**Horas por día y premio forzado**~~ | **CONSTRUIDA** el **2026-09-22 por la tarde** (día 2, paso 2). No estaba prevista: nació de tu dictado de esa tarde, después de ver el lunes. Cada franja lleva los **días** en que existe, y la silla, el set BBQ y la hielera salen **forzados** —la siguiente jugada se lleva la pieza abierta, sin sorteo—. §3 y §5.2 E. |

**Lo que se puede cargar en la Pi es este documento entero**, y desde el
**2026-09-16** (Fase 4e) **ya lo está, fechas incluidas**: las `desde`/`hasta` del
§5.1 se cargaron en `config.json` (ficha **F-259**, cerrada).

---

## 1. Los premios

**Los siete nombres y detalles los confirmaste el 2026-09-16** (era la pregunta 6
del §4), con dos correcciones tuyas: la cerveza y el agua ahora dicen de qué son.
Ya **no hay asteriscos**: los premios, los stocks y los cupos de esta tabla son tuyos.
**Las horas de la última columna se rehicieron el 2026-09-22** con tu dictado de
esa mañana —«horas sueltas, no redondas» y el reparto de sillas y sets por día—;
los minutos exactos los repartí yo. Ver la nota fechada de más abajo.

| id | NOMBRE EN EL BOLETO | Detalle (texto chico) | Tipo | Stock | Cupo/día | Días en que sale | Franja horaria |
|---|---|---|---|---|---|---|---|
| `hielera` | **HIELERA IGLOO** | Premio mayor | mayor | **2** | **1** | **jue 24 y vie 25** | **19:36** el jueves y **20:04** el viernes, **hasta el cierre** |
| `silla` | **SILLA DE PLAYA** | Premio grande | grande | **10** | **2** | **mar 22 a vie 25** | **dos horas distintas cada día** (tabla de abajo), 2 h cada una |
| `silla_extra` | **SILLA DE PLAYA** | Premio grande | grande | **2** | **1** | **mar 22 y mié 23** | 16:08 el martes y 16:21 el miércoles, 2 h |
| `bbq` | **SET BBQ** | Premio grande | grande | **10** | **2** | **mar 22 a vie 25** | **dos horas distintas cada día** (tabla de abajo), 2 h cada una |
| `bbq_extra` | **SET BBQ** | Premio grande | grande | **1** | **1** | **mar 22** | 17:34, 2 h |
| `tacos3` | **3 TACOS DE PASTOR** | Plato de 3 tacos de pastor | chico | **20** | **4** | **los 5 días** | **todo el día**, repartidos parejo |
| `tacos2` | **2 TACOS DE PASTOR** | Plato de 2 tacos de pastor | chico | **20** | **4** | **los 5 días** | **todo el día**, repartidos parejo |
| `cerveza` | **CERVEZA** | Tecate Light, Tecate Roja o Indio | chico | **50** | **10** | **los 5 días** | **todo el día**, repartidas parejo |
| `agua` | **AGUA FRESCA** | Horchata, Jamaica o Cebada | chico | **55** | **11** | **los 5 días** | **todo el día**, repartidas parejo |
| **Totales** | | | | **170** (ver la nota) | **35** el martes 22 · **34** el miércoles, el jueves y el viernes (el **lunes 21** fueron **33**) | | |

**`silla_extra` y `bbq_extra` NO son premios nuevos.** Son **la misma silla y el
mismo set BBQ** —mismo nombre en el boleto, mismo detalle— metidos una segunda
vez en la lista para poder darles **una hora distinta y unos días distintos**.
Hacen falta porque `config.json` **solo admite un juego de franjas y un cupo
diario por premio**, iguales para los cinco días. Por eso el **170** de la fila
de totales **no son 170 piezas en la bodega**: las piezas siguen siendo **167**,
de las que quedan **10 sillas** y **9 sets BBQ** (el lunes salió uno).

*(**Actualizado el 2026-09-22 por la tarde**, en el paso 2: el programa **ya sabe
de horas por día** —cada franja lleva sus `dias`—, así que estas dos entradas
**ya no hacen falta para eso**. Aun así **se quedan hasta que acabe el evento**:
`datos/estado.json` lleva la cuenta **por id**, y quitarlas ahora, con premios ya
entregados, descontaría mal y el kiosco creería que le quedan más sillas de las
que hay. Se retiran al cerrar el viernes. Fichas **F-281** y **F-284**.)*

### Nota fechada · 2026-09-22 · la reposición del día 2

**Lo que pasó el lunes 21, medido:** **55 jugadas**, y de ellas **agua 11 de 11**,
**cerveza 8 de 10**, **3 tacos 4 de 4**, **2 tacos 3 de 4**, **set BBQ 1 de 2** y
**silla 0 de 2**. Los grandes se quedaron porque **casi nadie jugó en sus
franjas** (9 jugadas entre 13:00 y 16:00; **ninguna** entre 19:00 y 20:00) y
porque con **peso 2** competían contra el agua (11), la cerveza (10), los tacos
(4 + 4) y el consuelo (10): **≈ 5 % por jugada**. Ficha **F-280**.

**Lo que decidiste hoy:** que **salgan casi seguro en cuanto se abren** —de ahí
el **peso 100**—, que las horas sean **sueltas y no redondas**, y **reponer lo
que no salió**, de modo que entre martes y viernes puedan salir **10 sillas** y
**9 sets BBQ**:

| Día | Sillas | Sets BBQ |
|---|---|---|
| **martes 22** | **3** | **3** |
| **miércoles 23** | **3** | **2** |
| **jueves 24** | **2** | **2** |
| **viernes 25** | **2** | **2** |
| **Total** | **10** | **9** |

**Aviso importante sobre las horas, y es el límite de este paso:** las horas
sueltas que quedan cargadas son **las del martes**, y **rigen igual los cuatro
días**, porque hoy `config.json` no sabe de horas por día. Lo mismo con la
hielera: queda a las **19:36** el jueves **y el viernes**, cuando lo suyo sería
una hora **distinta cada día**. *(Las dos horas concretas —19:36 el jueves y
20:04 el viernes— las propuse yo, como el resto de los minutos sueltos.)* **Eso llega en el paso 2**, que es
programa y no configuración.

*(**Resuelto esa misma tarde**, en el **paso 2**: el programa aprendió `dias`
dentro de cada franja y **cada día tiene ya sus propias horas**, las de la tabla
de aquí abajo. El aviso se conserva porque explica por qué las horas del martes
llegaron a regir los cuatro días.)*

### Nota fechada · 2026-09-22, por la tarde · las horas de cada día

**Esto lo dictaste tú**, y es lo que rige desde el paso 2. Cada pieza **abre a su
hora** y su ventana **dura dos horas**, menos las que llegan al cierre. *(Los
minutos exactos los repartí yo, como los del paso 1; el reparto por días es
tuyo.)*

| Día | Sillas abren a las | Sets BBQ abren a las | Hielera |
|---|---|---|---|
| **martes 22** | **13:17** · **16:08** · **19:23** | **14:41** · **17:34** · **20:47** | — |
| **miércoles 23** | **13:09** · **16:21** · **19:38** | **14:52** · **20:19** | — |
| **jueves 24** | **13:26** · **19:11** | **14:37** · **20:52** | **19:36**, hasta el cierre |
| **viernes 25** | **13:04** · **19:31** | **14:58** · **21:06**, hasta el cierre | **20:04**, hasta el cierre |
| **Total** | **10** | **9** | **2** |

**Y salen FORZADAS**: en cuanto el reloj abre una silla, un set BBQ o la hielera,
**la siguiente jugada se la lleva**, sin sorteo. No hay que esperar a que alguien
tenga suerte. Está explicado en llano en el §3.

**Ojo con el lunes 21:** la silla y el set BBQ (`silla` y `bbq`) siguen teniendo
`desde` en el **21**, pero **ninguna de sus franjas cae ese día**, así que el lunes ya no
podrían salir. Da igual —el lunes ya pasó—, y se deja así para no tocar fechas
que ya no afectan a nada.

### La cuenta de la bodega, rehecha después del lunes

Rehecha el **2026-09-22** con lo que quedó después del lunes. La cuenta de los
grandes ya **no** es «cupo × 5 días»: el lunes se fue un set BBQ y las dos sillas
y el set que no salieron **se reponen** en los cuatro días que quedan.

| Premio | Lo que queda | Cupo × días que quedan | ¿Cabe? |
|---|---|---|---|
| `hielera` | 2 | 1 × 2 días (jue y vie) = **2** | sí, exacto |
| `silla` + `silla_extra` | 10 | 2 × 4 días + 1 × 2 días = **10** | sí, exacto |
| `bbq` + `bbq_extra` | 9 (salió 1 el lunes) | 2 × 4 días + 1 × 1 día = **9** | sí, exacto |
| `tacos3` | 16 (salieron 4) | 4 × 4 días = **16** | sí, exacto |
| `tacos2` | 17 (salieron 3) | 4 × 4 días = **16** | sobra **1** |
| `cerveza` | 42 (salieron 8) | 10 × 4 días = **40** | sobran **2** |
| `agua` | 44 (salieron 11) | 11 × 4 días = **44** | sí, exacto |

Por día: **6 premios grandes el martes** (3 sillas + 3 sets), **5 el miércoles**
(3 + 2) y **4** el jueves y el viernes (2 + 2), más **29 chicos** (4 + 4 + 10 +
11) todos los días y **1 hielera** el jueves y el viernes.

**Lo que sobró el lunes de cerveza (2) y de 2 tacos (1) NO se repone**: se queda
en la bodega. Es decisión del orquestador, y la puedes cambiar (ficha **F-282**).

Como casi no sobra margen, si un día sale menos de lo previsto **esas piezas se
quedan en la bodega**: el cupo **no** se arrastra al día siguiente.

### Los nombres caben en el papel

Medido el 2026-09-13 con la función real que arma el boleto, a 48 columnas:
**los siete nombres se imprimen en el tamaño más grande que existe (×4)**, en
una o dos líneas:

`HIELERA / IGLOO` · `SILLA DE / PLAYA` · `SET BBQ` · `3 TACOS DE / PASTOR` ·
`2 TACOS DE / PASTOR` · `CERVEZA` · `AGUA FRESCA`

**Regla para cambiar un nombre:** que **ninguna palabra pase de 12 letras** y que
el nombre completo no ocupe más de 3 renglones de 12 letras. Si te pasas, el
programa no falla: solo imprime el nombre más chico. Los acentos y la `ñ` salen
bien (tabla `cp858`, confirmada en papel el 2026-09-11).

---

## 2. Cómo se decide quién gana (explicado sin programación)

**Esto cambió entero el 2026-09-16, con tu dictado.** Antes, el reparto colgaba
de **N**, las jugadas que esperabas en un día. Tú dijiste que **es imposible
saberlo**, y tienes razón: si N se estima mal, o se regalan los premios en la
primera hora o no sale casi nada. Así que **ya no hay N**: ahora manda **el
reloj**.

### La idea en una frase

> **El cupo del día no está disponible entero desde las 12:00: se va abriendo
> poco a poco, una pieza cada tanto, hasta las 23:00.**

Cada premio tiene su cupo del día (11 aguas, 10 cervezas, 4 y 4 tacos…). El
programa reparte esas piezas a lo largo de las **once horas** del evento, y
**solo lo que el reloj ya abrió puede salir**. Si a las 12:30 se abrió la primera
agua, hasta las 13:30 no se abre la segunda: por muchas jugadas que haya en esa
hora, **no salen dos aguas**.

### A qué hora se abre cada pieza

Tabla **calculada por el programa** el **2026-09-22** con el `config.json` real y
el horario de 12:00 a 23:00. Los premios **sin franja** se abren en el **punto
medio** de su tramo, para que ni la primera salga al abrir ni la última al
cerrar; los que **sí** tienen franja se abren **al empezar la franja**:

| Premio | Piezas al día | Se abren a las |
|---|---|---|
| **AGUA FRESCA** | 11 | 12:30 · 13:30 · 14:30 · 15:30 · 16:30 · 17:30 · 18:30 · 19:30 · 20:30 · 21:30 · 22:30 |
| **CERVEZA** | 10 | 12:33 · 13:39 · 14:45 · 15:51 · 16:57 · 18:03 · 19:09 · 20:15 · 21:21 · 22:27 |
| **3 TACOS DE PASTOR** | 4 | 13:22 · 16:07 · 18:52 · 21:37 |
| **2 TACOS DE PASTOR** | 4 | 13:22 · 16:07 · 18:52 · 21:37 |
| **SILLA DE PLAYA** (`silla`) | 2 | **distintas cada día** → tabla del §3 |
| **SILLA DE PLAYA** (`silla_extra`) | 1 (mar y mié) | **16:08** el martes · **16:21** el miércoles |
| **SET BBQ** (`bbq`) | 2 | **distintas cada día** → tabla del §3 |
| **SET BBQ** (`bbq_extra`) | 1 (solo el mar) | **17:34** |
| **HIELERA IGLOO** | 1 (jue y vie) | **19:36** el jueves · **20:04** el viernes |

Los cuatro premios chicos se abren **a la misma hora todos los días**, porque se
reparten parejo sobre el horario del evento. Las piezas con **franja** se abren
**al empezar su franja**, no a la mitad: la silla del martes se puede ganar **a
las 13:17 en punto**.

*(Horas **sueltas y no redondas** desde el **2026-09-22**, porque tú lo pediste
así, y **distintas cada día** desde esa misma tarde, que es lo que trajo el paso
2. Hasta el 22 eran 13:00 y 19:00 para la silla y el set, y 19:00 para la
hielera; con los grandes concentrados en las horas en punto y con **peso 2**,
el lunes 21 **no salió ninguna silla**. Ficha **F-280**.)*

### Cuatro reglas que van con esto, y que tú dictaste

1. **Una pieza CHICA abierta no la gana forzosamente la primera jugada.** El
   boleto de consuelo sigue compitiendo, con **peso 10**. Si a las 12:30 se abrió
   un agua y alguien juega, gana el agua **52 de cada 100 veces**; las otras 48
   se llevan su «gracias por participar». *(Hasta el 2026-09-22 por la tarde esta
   regla valía para **todos** los premios. Desde el paso 2, **la silla, el set
   BBQ y la hielera salen FORZADOS**: su pieza abierta **se la lleva la siguiente
   jugada, sin sorteo**. Está explicado en el §3.)*
2. **Lo que se abre y no se gana, no se pierde.** Esa agua sigue esperando a
   quien la gane, hasta las 23:00. Pero **tampoco adelanta la siguiente**: la
   número 2 no se abre hasta las 13:30, pase lo que pase.
3. **Las piezas no se acumulan por adelantado.** Al abrir el día no hay nada
   abierto: a las 12:00 en punto, **la primera jugada del día no puede ganar**
   (la primera pieza se abre a las 12:30).
4. **Los premios no salen seguidos… salvo los tres grandes.** Entre dos boletos
   con premio tienen que pasar al menos **1 minuto**, y dentro de ese minuto toda
   jugada sale de consuelo aunque haya piezas abiertas. **La silla, el set BBQ y
   la hielera se saltan esa espera** desde el 2026-09-22 por la tarde, porque
   salen forzados (§3, y ficha **F-283**). *(Eran **3 minutos** hasta el
   2026-09-22: el lunes 21, **6 de las 55 jugadas** salieron de consuelo por esa
   regla teniendo premio abierto, así que la bajaste a 1. Ficha **F-280**.)*

### Lo bueno: la ruleta se ajusta sola al gentío

Esta es la ventaja de no depender de N. Simulado por el programa el 2026-09-16
—un día completo del jueves 24, 30 corridas por renglón, con los premios, las
franjas y la separación reales—:

| Si se juega… | Jugadas en el día | Premios que salen | Gana |
|---|---|---|---|
| una cada 20 segundos (muy lleno) | 1 980 | **34 de 34** | 1.7 % (1 de cada 58) |
| una cada minuto | 660 | **34 de 34** | 5.2 % (1 de cada 19) |
| una cada 3 minutos | 220 | **34 de 34** | 15.5 % (1 de cada 6) |
| una cada 10 minutos (flojo) | 66 | 31.7 de 34 | 48 % (1 de cada 2) |

Léelo así: **salga la gente que salga, se entrega el cupo del día casi completo**,
y lo que cambia es cada cuántas jugadas toca. Con el modelo viejo, **acertando**
N, la regla simple entregaba el **84 %** del cupo, y el «factor de holgura» del §4
lo subía hasta el 96–98 % a costa de que los premios chicos se agotaran a media
tarde; con este, de unas **220 jugadas al día para arriba** se entrega el cupo
**entero**, y por debajo se queda alguna pieza (medido por el programa el
2026-09-16: **33.6 de 34** con 99 jugadas y **31.7 de 34** con 66).

*(Nota fechada, **2026-09-22**: esta tabla se simuló el **2026-09-16** con la
configuración de entonces —silla y set con **peso 2**, hielera **1**, franjas en
horas redondas y **3 minutos** de separación—, así que **sus números son de
aquel reparto, no del de hoy**. No se ha vuelto a simular: **el reloj sigue
abriendo las mismas piezas al día**, que es lo que manda la columna «Premios que
salen», y lo que el peso 100 cambia es **quién se lleva la pieza abierta**, no
cuántas se abren. Lo que sí está medido de verdad es el día real: el lunes 21,
con **55 jugadas**, salieron **27 premios de 33 posibles**, y los que faltaron
fueron los grandes. Ficha **F-280**.)*

### Qué tan seguido se gana, momento a momento

Depende de **qué haya abierto en ese instante**, no de una tabla fija. Dos
ejemplos, **calculados por el programa** con el `config.json` real:

| Qué está abierto en ese momento | Papelitos | Gana |
|---|---|---|
| Una pieza de AGUA FRESCA (peso 11) | 11 + 10 = 21 | **52.4 %** |
| Solo la HIELERA IGLOO (peso 100) | 100 + 10 = 110 | **90.9 %** |

El **10** de las dos filas es el **peso del boleto de consuelo**, y es el único
número de todo el modelo que se puede subir o bajar si quieres que gane más o
menos gente. **Los tres premios grandes van a peso 100 desde el 2026-09-22**
(antes: silla 2, set 2, hielera 1), que es lo que convierte «una hielera
abierta» en **9 de cada 10 jugadas** en vez de 1 de cada 11: con todo lo demás
abierto a la vez, cada grande se lleva **100 de 239 papelitos ≈ 42 %**, y a
solas contra el consuelo, **100 de 110 ≈ 91 %**. El porcentaje exacto de cada momento lo ves sin imprimir con
`python3 -m ruleta reporte`.

**Si nadie juega en un buen rato, se juntan varias piezas abiertas** y las
primeras jugadas que lleguen ganarán más seguido, hasta ponerse al corriente. Es
a propósito: es lo que hace que el cupo del día se entregue igual en un día
flojo.

### Nota histórica: cómo se repartía antes del 2026-09-16

*(Se conserva corta porque hay fichas viejas que razonan desde aquí, y porque el
aviso vuelve a valer si algún día se pone el horario en `null`.)*

Hasta hoy, el reparto era **«el peso es el cupo»**: cada premio metía en la
tómbola tantos papelitos como su cupo diario (agua 11, cerveza 10, tacos 4 y 4,
silla 2, set 2) y el consuelo metía **N − 33**, donde **N** eran las jugadas
esperadas en un día. La tabla de equivalencias era
**150 → 117 · 200 → 167 · 250 → 217 · 300 → 267 · 400 → 367**, y con N = 250
ganaba el 13.55 % de las jugadas. Dos pegas, y por eso se cambió: **N no se
puede saber**, y aun acertando se entregaba solo el **84 %** del cupo, porque el
cupo cortaba los días buenos y nadie reponía los malos.

---

## 3. Franjas horarias · **DECIDIDAS**

Una **franja** es una ventana de horas en la que un premio puede salir, con su
**propio cupo**. Fuera de su franja el premio **no está en la tómbola**. Lo
decidiste el 2026-09-16 (eran las preguntas 2 y 3 del §4):

**Rehechas el 2026-09-22** (día 2, paso 1), con horas **sueltas** y **repartidas**
en vez de las horas redondas de antes, y **otra vez esa misma tarde** (paso 2),
para darle a **cada día las suyas**. Esta es la tabla que rige:

| Premio (id) | Día | Franja | Cupo en esa franja |
|---|---|---|---|
| SILLA DE PLAYA (`silla`) | **mar 22** | **13:17 – 15:17** · **19:23 – 21:23** | 1 en cada una |
| SILLA DE PLAYA (`silla`) | **mié 23** | **13:09 – 15:09** · **19:38 – 21:38** | 1 en cada una |
| SILLA DE PLAYA (`silla`) | **jue 24** | **13:26 – 15:26** · **19:11 – 21:11** | 1 en cada una |
| SILLA DE PLAYA (`silla`) | **vie 25** | **13:04 – 15:04** · **19:31 – 21:31** | 1 en cada una |
| SILLA DE PLAYA (`silla_extra`) | **mar 22** · **mié 23** | **16:08 – 18:08** · **16:21 – 18:21** | 1 |
| SET BBQ (`bbq`) | **mar 22** | **14:41 – 16:41** · **20:47 – 22:47** | 1 en cada una |
| SET BBQ (`bbq`) | **mié 23** | **14:52 – 16:52** · **20:19 – 22:19** | 1 en cada una |
| SET BBQ (`bbq`) | **jue 24** | **14:37 – 16:37** · **20:52 – 22:52** | 1 en cada una |
| SET BBQ (`bbq`) | **vie 25** | **14:58 – 16:58** · **21:06 – 23:00** | 1 en cada una |
| SET BBQ (`bbq_extra`) | **mar 22** | **17:34 – 19:34** | 1 |
| HIELERA IGLOO (`hielera`) | **jue 24** | **19:36 – 23:00** | 1 |
| HIELERA IGLOO (`hielera`) | **vie 25** | **20:04 – 23:00** | 1 |

La idea sigue siendo **la tarde y la noche**, pero ya no todos a la misma hora:
cada pieza **abre en su minuto** y **dura dos horas** —menos las que llegan al
cierre—, así que a lo largo de la tarde y de la noche hay casi siempre **algún
premio grande vivo**, y a ratos **dos a la vez**: medido con el programa, el
martes y el miércoles pasa aproximadamente una cuarta parte del tiempo, y las
noches del **jueves** (de 19:36 a 22:52) y del **viernes** (de 20:04 al cierre)
hay **siempre dos o tres abiertos**, porque la hielera llega hasta las 23:00.

### Los grandes salen FORZADOS · **decisión tuya del 2026-09-22 por la tarde**

Lo dijiste así: **«después de tal hora, el próximo juego se la saca»**. Eso es
ahora una regla del programa, y solo la llevan **la silla, el set BBQ y la
hielera**:

> **En cuanto el reloj abre una pieza de esos tres, la SIGUIENTE jugada se la
> lleva. No hay sorteo: el boleto sale con ese premio.**

Tres cosas que van con eso, y conviene tenerlas claras:

1. **No hay que esperar a la suerte.** Hasta esta tarde una silla abierta ganaba
   el **72 %** de las jugadas cuando era el único grande abierto —que era lo
   normal— y solo el **42 %** cuando había otro grande abierto a la vez (peso
   100). Medido con el motor del paso 1 sobre los **240 minutos** del martes en
   que la silla estaba abierta: **71.9 %** durante 151 de ellos, **41.8 %**
   durante 83 y **76.3 %** durante los 6 primeros, antes de que abrieran los
   tacos. Podía tardar dos o tres jugadas en salir, o no salir. Ahora sale **en
   la primera**.
2. **Se salta el minuto de separación.** La regla de que «los premios no salen
   seguidos» (§2, regla 4) **no aplica a estos tres**, porque lo que pediste es
   que se la lleve *la siguiente jugada*, no la siguiente que pase el minuto.
   **Consecuencia:** si hay **dos piezas grandes abiertas a la vez** y nadie ha
   jugado, **salen dos premios grandes en dos boletos seguidos**. Pasa **los
   cuatro días**, y estas son todas las ventanas, barridas minuto a minuto con
   el programa el 2026-09-22 por la tarde: el **martes** de 14:41 a 15:17, de
   16:08 a 16:41, de 17:34 a 18:08, de 19:23 a 19:34 y de 20:47 a 21:23; el
   **miércoles** de 14:52 a 15:09, de 16:21 a 16:52 y de 20:19 a 21:38; el
   **jueves** de 14:37 a 15:26 y de 19:36 a 22:52; y el **viernes** de 14:58 a
   15:04 y de 20:04 hasta el cierre. Y si además se arrastra lo que no se ganó
   antes, la racha llega a **4 boletos seguidos** el martes y el miércoles y a
   **5** el jueves y el viernes. Ficha **F-283**.
3. **Si hay dos abiertas, primero la del premio cuya ventana se abrió antes.** Ojo:
   no es lo mismo que «la que lleva más rato esperando» —el jueves a las 20:52 el
   set BBQ lleva abierto desde las 14:37 y aun así sale **después** de la hielera,
   que abrió a las 19:36—. Y si nadie
   jugó en toda la tarde, la pieza del mediodía **sigue esperando** (§3, más
   abajo), así que pueden salir **tres seguidas**: medido con el programa el
   jueves a las 19:40 —silla, silla y hielera—.

Los cuatro premios chicos **no** son forzados: siguen sorteándose con sus pesos
contra el boleto de consuelo, exactamente como hasta ahora.

**Dónde se ve:** el boleto de inventario marca esos premios con **`*forzado`**
junto al nombre y trae abajo la línea «`* forzado: abierto, lo gana la siguiente
jugada`». En el registro del kiosco cada uno deja una línea propia
(«`Boleto 00062: pieza forzada de SILLA DE PLAYA`»); en el **papel del cliente**
no se nota nada: el boleto sale idéntico a cualquier otro premio.

*(Hasta el 2026-09-22 eran **13:00–16:00 y 19:00–22:00** para la silla y el set,
y **19:00–23:00** para la hielera. Se movieron porque el lunes 21 casi nadie jugó
en esas ventanas —**9 jugadas** entre 13:00 y 16:00, **ninguna** entre 19:00 y
20:00— y no salió **ninguna silla**. Ficha **F-280**.)*

**Lo que sí puede pasar, y conviene saberlo:** si en la comida no se gana la
silla ni el set BBQ, esas dos piezas **no se pierden**, se suman a las de la
cena, y de noche pueden salir **varias seguidas**. Medido con el programa el
2026-09-22, y **vuelto a medir esa tarde con las horas por día y el forzado
puesto**: sin haber ganado nada antes de las 19:00 salen **5 grandes** el
martes (el set de reposición, 2 sillas y 2 sets), **4** el miércoles y **5** el
jueves y el viernes (2 sillas, 2 sets y la hielera). Lo que corta el día siguen
siendo los `tope_diario`, pero con las entradas de reposición el tope del día ya
no es cuatro: son **6** grandes el martes, **5** el miércoles y **5** el jueves y
el viernes contando la hielera. Ficha **F-269**.

**Y ahora salen en boletos SEGUIDOS**, porque el forzado se salta el minuto de
separación: medido el jueves a las **19:40**, con nadie habiendo jugado desde el
mediodía, las tres primeras jugadas se llevan **silla, silla y hielera**, una
detrás de otra. Ficha **F-283**.

**Los pesos de los grandes ya NO son su cupo diario.** Hasta el 2026-09-16 la
silla, el set y la hielera llevaban de peso su cupo (2, 2 y 1) y aquí se decía
que con el reparto por horas eso bastaba, porque cada grande sería «la única
pieza grande abierta» en su franja. **El lunes 21 demostró que no bastaba:** con
el agua (11), la cerveza (10), los tacos (4 + 4) y el consuelo (10) abiertos a la
vez, una silla abierta salía en **≈ 5 %** de las jugadas, y en 55 jugadas **no
salió ninguna**. Desde el **2026-09-22** los tres van a **peso 100**: en cuanto el
reloj abre uno, se lleva **≈ 42 %** de las jugadas con todo lo demás abierto y
**≈ 91 %** si está solo. Sigue sin haber `peso` por franja —el campo no existe—:
lo que cambió es el `peso` del premio. Ficha **F-280**.

*(Nota fechada, **2026-09-22 por la tarde**, paso 2: **ese peso 100 ya no decide
nada mientras la pieza esté abierta**, porque los tres salen **forzados** y no
pasan por la tómbola. Se conserva en `config.json` —es lo que valdría si algún
día se les quitara el forzado— y **sigue saliendo en la columna PROB del boleto
de inventario**, que describe la tómbola y no el resultado: cuando la fila lleva
`*forzado` y la pieza está abierta, **lo que manda es el forzado**, no ese
porcentaje. Ficha **F-285**.)*

### Los premios chicos NO llevan franja

Se reparten solos, parejo de 12:00 a 23:00, con las horas de la tabla del §2. Es
lo más simple de operar y de explicarle al personal, y con el reparto por horas
ya no hay riesgo de que se acaben a media tarde: **no pueden**, porque el reloj
no los ha abierto.

### Nota del final de la noche

Las franjas no terminan a la misma hora, y desde el paso 2 **cada noche acaba
distinto**. Calculado por el programa el **2026-09-22 por la tarde**, con la
configuración que rige:

| Noche | La última ventana grande en cerrar | Qué queda hasta las 23:00 |
|---|---|---|
| **martes 22** | el set BBQ, a las **22:47** | nada grande entre las 22:47 y el cierre |
| **miércoles 23** | el set BBQ, a las **22:19** | nada grande desde las 22:19 |
| **jueves 24** | la hielera, **hasta el cierre** | de **22:52** (cierra el set BBQ) a las 23:00, **solo la hielera** |
| **viernes 25** | la hielera **y** el set BBQ, los dos **hasta el cierre** | los dos vivos hasta las 23:00 |

Como los tres grandes salen **forzados**, lo que importa de esta tabla ya no son
porcentajes: **si a esas horas hay una pieza abierta, se la lleva la siguiente
jugada**. La noche que más se aprovecha es la del **viernes**, con dos ventanas
llegando al cierre.

---

## 4. Preguntas abiertas

- [x] **1. ¿Cuántas jugadas esperas por día (N)?**
  **YA NO HACE FALTA** (2026-09-16). Tu respuesta fue que **es imposible
  saberlo**, y de ahí salió el reparto por horas del §2, que **no usa N**.

- [x] **2. Franjas de la SILLA DE PLAYA y el SET BBQ.**
  **SÍ**, las dos: **13:00–16:00 y 19:00–22:00, una pieza en cada franja**
  (2026-09-16). La de los grandes cierra a las 22:00, no a las 23:00.
  *(**Respuesta superada el 2026-09-22**: esas ventanas quedaron vacías el lunes
  21 y las cambiaste por **horas sueltas de dos horas** —silla 13:17 y 19:23, set
  BBQ 14:41 y 20:47, más las de reposición—, que son las del **martes**; esa
  misma tarde le diste **sus horas a cada día**. Las de hoy están en el §3.)*

- [x] **3. Confirmar la HIELERA: 19:00–23:00 los días 24 y 25, una por día.**
  **SÍ** (2026-09-16). *(**Los días siguen siendo el 24 y el 25**; la hora se
  movió a las **19:36** el 2026-09-22 por la mañana y, esa misma tarde, a
  **19:36 el jueves y 20:04 el viernes**, las dos hasta el cierre. Desde esa
  tarde sale además **forzada**: la siguiente jugada se la lleva.)*

- [x] **4. ¿Los premios chicos van por franjas?**
  **NO**: van **repartidos parejo** de 12:00 a 23:00 (2026-09-16). Es la opción
  (a) de siempre, ahora con el reparto por horas encima.

- [x] **5. Fuera del horario del evento** (antes de las 12:00 o después de las
  23:00), si alguien aprieta JUGAR con el mesero habilitando:
  **CONSUELO** (2026-09-16): se imprime el boleto de «gracias por participar»,
  para que el cliente se lleve algo. Gasta papel y folio, no premios.

- [x] **6. Nombres y detalles exactos** (los siete del §1).
  **CONFIRMADOS** (2026-09-16), con dos cambios tuyos: **CERVEZA** → «Tecate
  Light, Tecate Roja o Indio» y **AGUA FRESCA** → «Horchata, Jamaica o Cebada».
  Los otros cinco quedan como estaban.

- [ ] **7. (extra) Factor de holgura** del §2 viejo.
  **Ya casi no aplica.** Servía para pelear contra el 84 % de entrega del modelo
  viejo; con el reparto por horas se entrega **el 100 % del cupo** salvo en días
  muy flojos (tabla del §2). Si algún día quieres que en un día flojo salga todo,
  lo que se toca es el **peso del consuelo** (bajarlo de 10), no un factor.

---

## 5. Cómo se traduce a `config.json`

### 5.1 Lo que YA se puede cargar hoy

Estos campos existen en el programa y funcionan. **Comprobado el 2026-09-16: los
dos bloques cargan sin un solo error** en el validador del programa
(`ruleta/config.py`). **Desde el 2026-09-16 (Fase 4e) los dos bloques están
cargados ENTEROS en `config.json`, fechas incluidas** (ficha **F-259**, cerrada):
la hielera solo puede salir el **jueves 24** y el **viernes 25**, y los otros seis
del **lunes 21** al **viernes 25**.

**Consecuencia de tener las fechas puestas, y es la correcta:** **hasta el lunes
21 ninguna jugada puede dar premio**. Antes de esa fecha todos los premios están
*fuera de fechas*, así que **todo sale boleto de consuelo**. No es una avería.

*(**Actualizado el 2026-09-22**, día 2 paso 1: en este bloque cambiaron **los
pesos** de los tres grandes —silla, set BBQ y hielera, de 2, 2 y 1 a **100**—,
**las franjas** —a horas sueltas— y **la separación entre premios**, de 3 minutos
a **1**. Y aparecen **dos entradas nuevas**, `silla_extra` y `bbq_extra`, que
**no son premios nuevos**: son la misma silla y el mismo set con otra hora y
otros días, porque `config.json` solo admite un juego de franjas por premio (§1 y
ficha **F-281**). Lo demás —tacos, cerveza, agua, consuelo, horario,
`espera_hora_seg`, fechas— **no se tocó**.)*

*(**Actualizado otra vez el 2026-09-22 por la tarde**, día 2 paso 2: en este
bloque aparecen **dos llaves nuevas**, y solo en los cinco premios grandes.
**`forzado": true`** hace que la pieza abierta se la lleve la siguiente jugada
sin sorteo, y **`"dias"` dentro de cada franja** dice en qué días existe esa
ventana, que es lo que permite darle **a cada día sus horas**. Por eso la silla y
el set BBQ pasan de dos franjas a **ocho** —dos por cada uno de los cuatro
días— y la hielera, de una a **dos**. Los pesos, los stocks, los cupos, las
fechas `desde`/`hasta` y el bloque `juego` **no se tocaron**. La pieza está
explicada en el §5.2 **E**.)*

**Los premios**, con sus descripciones confirmadas y sus franjas:

```json
"premios": [
  { "id": "hielera",     "nombre": "HIELERA IGLOO",     "detalle": "Premio mayor",                      "stock": 2,  "tope_diario": 1,  "peso": 100, "desde": "2026-09-24", "hasta": "2026-09-25", "forzado": true,
    "franjas": [ { "desde_hora": "19:36", "hasta_hora": "23:00", "tope": 1, "dias": ["2026-09-24"] },
                 { "desde_hora": "20:04", "hasta_hora": "23:00", "tope": 1, "dias": ["2026-09-25"] } ] },
  { "id": "silla",       "nombre": "SILLA DE PLAYA",    "detalle": "Premio grande",                     "stock": 10, "tope_diario": 2,  "peso": 100, "desde": "2026-09-21", "hasta": "2026-09-25", "forzado": true,
    "franjas": [ { "desde_hora": "13:17", "hasta_hora": "15:17", "tope": 1, "dias": ["2026-09-22"] },
                 { "desde_hora": "19:23", "hasta_hora": "21:23", "tope": 1, "dias": ["2026-09-22"] },
                 { "desde_hora": "13:09", "hasta_hora": "15:09", "tope": 1, "dias": ["2026-09-23"] },
                 { "desde_hora": "19:38", "hasta_hora": "21:38", "tope": 1, "dias": ["2026-09-23"] },
                 { "desde_hora": "13:26", "hasta_hora": "15:26", "tope": 1, "dias": ["2026-09-24"] },
                 { "desde_hora": "19:11", "hasta_hora": "21:11", "tope": 1, "dias": ["2026-09-24"] },
                 { "desde_hora": "13:04", "hasta_hora": "15:04", "tope": 1, "dias": ["2026-09-25"] },
                 { "desde_hora": "19:31", "hasta_hora": "21:31", "tope": 1, "dias": ["2026-09-25"] } ] },
  { "id": "silla_extra", "nombre": "SILLA DE PLAYA",    "detalle": "Premio grande",                     "stock": 2,  "tope_diario": 1,  "peso": 100, "desde": "2026-09-22", "hasta": "2026-09-23", "forzado": true,
    "franjas": [ { "desde_hora": "16:08", "hasta_hora": "18:08", "tope": 1, "dias": ["2026-09-22"] },
                 { "desde_hora": "16:21", "hasta_hora": "18:21", "tope": 1, "dias": ["2026-09-23"] } ] },
  { "id": "bbq",         "nombre": "SET BBQ",           "detalle": "Premio grande",                     "stock": 10, "tope_diario": 2,  "peso": 100, "desde": "2026-09-21", "hasta": "2026-09-25", "forzado": true,
    "franjas": [ { "desde_hora": "14:41", "hasta_hora": "16:41", "tope": 1, "dias": ["2026-09-22"] },
                 { "desde_hora": "20:47", "hasta_hora": "22:47", "tope": 1, "dias": ["2026-09-22"] },
                 { "desde_hora": "14:52", "hasta_hora": "16:52", "tope": 1, "dias": ["2026-09-23"] },
                 { "desde_hora": "20:19", "hasta_hora": "22:19", "tope": 1, "dias": ["2026-09-23"] },
                 { "desde_hora": "14:37", "hasta_hora": "16:37", "tope": 1, "dias": ["2026-09-24"] },
                 { "desde_hora": "20:52", "hasta_hora": "22:52", "tope": 1, "dias": ["2026-09-24"] },
                 { "desde_hora": "14:58", "hasta_hora": "16:58", "tope": 1, "dias": ["2026-09-25"] },
                 { "desde_hora": "21:06", "hasta_hora": "23:00", "tope": 1, "dias": ["2026-09-25"] } ] },
  { "id": "bbq_extra",   "nombre": "SET BBQ",           "detalle": "Premio grande",                     "stock": 1,  "tope_diario": 1,  "peso": 100, "desde": "2026-09-22", "hasta": "2026-09-22", "forzado": true,
    "franjas": [ { "desde_hora": "17:34", "hasta_hora": "19:34", "tope": 1, "dias": ["2026-09-22"] } ] },
  { "id": "tacos3",      "nombre": "3 TACOS DE PASTOR", "detalle": "Plato de 3 tacos de pastor",        "stock": 20, "tope_diario": 4,  "peso": 4,   "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "tacos2",      "nombre": "2 TACOS DE PASTOR", "detalle": "Plato de 2 tacos de pastor",        "stock": 20, "tope_diario": 4,  "peso": 4,   "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "cerveza",     "nombre": "CERVEZA",           "detalle": "Tecate Light, Tecate Roja o Indio", "stock": 50, "tope_diario": 10, "peso": 10,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "agua",        "nombre": "AGUA FRESCA",       "detalle": "Horchata, Jamaica o Cebada",        "stock": 55, "tope_diario": 11, "peso": 11,  "desde": "2026-09-21", "hasta": "2026-09-25" }
]
```

**El juego**, con el horario del evento, la separación entre premios, la espera
de la hora al encender y el peso del consuelo:

```json
"juego": {
  "horario": { "abre": "12:00", "cierra": "23:00", "fuera_de_horario": "consuelo" },
  "separacion_min_entre_premios": 1,
  "espera_hora_seg": 300,
  "consuelo": { "titulo": "SIGUE PARTICIPANDO", "texto": "¡Gracias por jugar!", "peso": 10 }
}
```

Qué significa cada campo:

| Campo | Qué hace |
|---|---|
| `id` | nombre corto interno; sale en el reporte de inventario y en la bitácora `boletos.csv`. Nunca lo ve el cliente |
| `nombre` | **lo que se imprime grande y en mayúsculas** en el boleto |
| `detalle` | el texto chico debajo del nombre |
| `stock` | piezas para **todo el evento** |
| `tope_diario` | máximo por **día operativo**, y **el cupo que se reparte por horas** (§2) |
| `peso` | los papelitos en la tómbola cuando la pieza ya está abierta (§2) |
| `desde` / `hasta` | primer y último día en que puede salir, **los dos incluidos** |
| `franjas` | ventanas de horas en que ese premio existe, con su `tope` propio (§3) |
| `franjas[].dias` | días en que existe **esa** ventana; sin la llave, vale todos (§5.2 E) |
| `forzado` | `true` = la pieza abierta se la lleva la **siguiente jugada**, sin sorteo (§3 y §5.2 E) |
| `horario` | apertura y cierre del evento; `fuera_de_horario` dice qué pasa afuera |
| `separacion_min_entre_premios` | minutos mínimos entre dos boletos **con premio** |
| `espera_hora_seg` | segundos que el kiosco espera al encender a tener la hora buena |
| `consuelo.peso` | los papelitos del boleto de «gracias por participar» |

**Sobre el «día operativo»:** el programa cambia de día a las **6 de la mañana**
(`juego.hora_inicio_dia`). Como el evento corre de 12:00 a 23:00, **el día
operativo siempre coincide con el día del calendario**; nada se pasa a la
madrugada siguiente. Comprobado.

**Sobre el reloj:** todo el reparto del §2 depende de la hora de la Pi. **Decisión
tuya del 2026-09-15:** en el evento la Pi tendrá **el internet del asadero**, que
es lo que le pone la hora al arrancar por NTP, y **no habrá batería RTC**. De ahí
salió la **pieza D**, ya construida: al encender, el kiosco **espera hasta 5
minutos** a que la hora esté sincronizada antes de imprimir nada, y si no lo
consigue **escribe en el boleto de inventario** la línea
`HORA SIN CONFIRMAR: revisar fecha`. Si ves esa línea: **no reinicies**, espera un
par de minutos y pide otro inventario con el gesto del botón HABILITAR.
*(Hasta el 2026-09-16 este párrafo decía que la Pi iba **sin red** y que **por eso
la batería RTC era necesaria**; lo derogó tu decisión del 2026-09-15. Ficha
**F-266**, cerrada.)*

*(Nota fechada, **2026-09-16**, Fase 4e: **probado en hardware, con la Pi
desenchufada unos minutos**. Sin batería, el reloj arrancó en **1970** y encima le
cayó la **hora vieja** que el sistema tenía guardada —**4 min 54 s atrasada**—; la
restaura **systemd** desde la marca `/var/lib/systemd/timesync/clock`, y
`fake-hwclock` **no está instalado** en esta Pi. El kiosco **esperó 28.3 s**, la
hora llegó por NTP y **el inventario salió 0.6 s después, con la fecha correcta**:
el orden Pi → internet → hora → inventario → listo se cumple. El tope subió de
**2 a 5 minutos** por margen, no por coste —si la hora llega en 3 s, el kiosco
arranca en 3 s—: esos 28 s se midieron en la red de casa, contra un servidor por
IPv6, y la del asadero puede tardar distinto. Evidencia:
`docs/actas/2026-09-16-hechos-medidos-fase-4e.md`. Ficha **F-241**, cerrada
también en hardware.)*

### 5.2 Lo que hubo que CONSTRUIR

**Las cuatro piezas están construidas.** Se deja escrito cómo quedó cada una,
porque de estos bloques **derivan** las pruebas automáticas.

**PENDIENTE A · Peso propio del boleto de consuelo** (dentro de `"juego"`)
— **CONSTRUIDA el 2026-09-16, Fase 4c**; plan:
`docs/planes/fase-4c-consuelo-peso.md`. **Recalibrada el 2026-09-16, Fase 4d**
(plan `docs/planes/fase-4d-horas.md`): con el reparto por horas el consuelo ya no
compite contra los 34 papelitos del día entero, sino contra **la pieza o dos que
estén abiertas**, así que su peso bajó de **217** a **10**:

```json
"consuelo": { "titulo": "SIGUE PARTICIPANDO", "texto": "¡Gracias por jugar!", "peso": 10 }
```

`titulo` y `texto` son decisión tuya del 2026-09-13 y **no se han tocado**. Qué
hace el programa:

- El consuelo **compite en cada jugada** como uno más de la tómbola, con sus
  `peso` papelitos. Una sola tirada decide entre premios y consuelo.
- El consuelo **no descuenta stock ni cupo** (no es un premio), pero **sí gasta
  folio**, como siempre.
- El **inventario impreso** (`python3 -m ruleta reporte`) trae una línea con el
  peso del consuelo y su probabilidad de ese momento.
- Con `"peso": 0` —o si se borra la llave— el consuelo **solo** sale cuando ya no
  queda ningún premio abierto.

**PENDIENTE B · Franjas por premio, con cupo por franja** (dentro de cada premio)
— **CONSTRUIDA el 2026-09-16, Fase 4d**. Esta es la forma exacta del campo, y son
**las franjas de la hielera tal cual están cargadas** (con `dias`, desde el día 2
paso 2 del 2026-09-22):

```json
"franjas": [ { "desde_hora": "19:36", "hasta_hora": "23:00", "tope": 1, "dias": ["2026-09-24"] },
             { "desde_hora": "20:04", "hasta_hora": "23:00", "tope": 1, "dias": ["2026-09-25"] } ]
```

Reglas de ese campo, tal como quedaron:

- Un premio **con** `franjas` **no está disponible fuera de ellas**.
- `tope` son las piezas que esa franja **abre** ese día; además siguen mandando
  el `tope_diario` del premio y su `stock`. **Ojo, porque el programa NO lleva la
  cuenta franja por franja:** cuenta «piezas abiertas hoy menos entregadas hoy»,
  así que **lo que una franja abre y nadie gana se arrastra a la siguiente franja
  del mismo día**. Si la silla de la tarde no sale, a las **19:23** hay **dos**
  disponibles y **las dos pueden salir esa noche**; lo que corta el día sigue
  siendo el `tope_diario` (2). Ficha **F-269**.
- La pieza de una franja de **una** pieza se abre **al empezar la franja**; si la
  franja tuviera varias, se repartirían parejo dentro de ella (§2).
- Un premio **sin** `franjas` se reparte sobre todo el horario del evento. (Así
  los cuatro premios chicos no necesitan nada.)
- **No hay `peso` por franja**, y ya no hace falta: lo explica el §3.

**PENDIENTE C · Horario del evento** (dentro de `"juego"`) — **CONSTRUIDA el
2026-09-16, Fase 4d**:

```json
"horario": { "abre": "12:00", "cierra": "23:00", "fuera_de_horario": "consuelo" }
```

- `fuera_de_horario` es `"consuelo"` (tu respuesta a la pregunta 5) o
  `"no_jugar"` (no imprime nada y solo avisa el LED). **Este evento usa
  `"consuelo"`**; la otra ruta existe, está probada y **no se usa**.
- El cierre es **exclusivo**: a las **23:00 en punto ya no se juega**.
- **Sin el bloque `horario`** se juega a cualquier hora, como antes de esta fase.

**PENDIENTE D · Esperar a que la hora esté sincronizada** (dentro de `"juego"`)
— **CONSTRUIDA el 2026-09-16, Fase 4d**:

```json
"espera_hora_seg": 300
```

- Al **arrancar**, el kiosco pregunta cada 2 segundos si el sistema ya puso la
  hora (el archivo que deja `systemd-timesyncd` o, si no, `timedatectl`), hasta
  ese tope de segundos.
- Si la consigue, sigue como siempre. Si **se agota el tiempo**, arranca igual
  —nunca se queda colgado— pero **imprime en el boleto de inventario de arranque**
  la línea `HORA SIN CONFIRMAR: revisar fecha` y lo anota como **aviso** en el
  registro.
- **Ninguna jugada espera nada**: esto pasa una sola vez, al encender.
- Con `0` no se espera nada, que es como se comportaba antes.
- **Mientras espera lo dice en el registro** (desde el 2026-09-16, Fase 4e): una
  línea al empezar, otra cada **10 segundos** y una última con **cuántos segundos
  costó** («Hora sincronizada tras 28 s»). Sirve para saber, leyendo el journal,
  si la hora llegó al instante o costó minutos. Ficha **F-273**, cerrada.
- El tope pasó de **120** a **300 segundos** el 2026-09-16 (Fase 4e): ver la nota
  fechada del §5.1.

**PIEZA E · Horas por día (`dias`) y premio forzado (`forzado`)** — **CONSTRUIDA
el 2026-09-22 por la tarde**, día 2 paso 2; plan:
`docs/planes/dia2-paso2-forzado.md`. Es la única pieza que **no** estaba prevista
en la versión original de este documento: nació del dictado de esa tarde, después
de ver el lunes y el martes por la mañana.

**`dias`, dentro de cada franja.** Dice en qué **días operativos** existe esa
ventana. Así se le da a cada día su hora sin duplicar el premio: son las dos
franjas de la silla del jueves y del viernes, tal cual están cargadas (el
ejemplo completo del campo, con su forma exacta, es el del **PENDIENTE B**).

```
{ "desde_hora": "13:26", "hasta_hora": "15:26", "tope": 1, "dias": ["2026-09-24"] },
{ "desde_hora": "13:04", "hasta_hora": "15:04", "tope": 1, "dias": ["2026-09-25"] }
```

- **Sin la llave `dias`, o con la lista vacía, la franja vale TODOS los días**,
  que es como se comportaba el programa hasta el 2026-09-22. Un `config.json`
  viejo sigue funcionando igual.
- Un premio que **tiene franjas pero ninguna de hoy** no existe hoy: no se cae al
  reparto del `tope_diario`, no abre ninguna pieza y el inventario impreso dice
  «franjas de hoy cerradas».
- El día es el **día operativo** (cambia a las 06:00), igual que `desde`/`hasta`.
- Si la fecha está mal escrita, el kiosco **no arranca** y el mensaje dice en qué
  premio y en qué franja está el error. Formato `"AAAA-MM-DD"`, entre comillas.

**`forzado`, dentro del premio.** Es el dictado de esa tarde: «después de tal
hora, el próximo juego se la saca».

```
"forzado": true
```

- Con `true`, **en cuanto el reloj abre una pieza de ese premio, la SIGUIENTE
  jugada se la lleva**: no hay tómbola, no compite con el consuelo y **no espera
  el minuto de separación** entre premios.
- Si hay **varias piezas forzadas abiertas a la vez**, sale primero la del premio
  **cuya ventana empezó antes**; la siguiente jugada se lleva la otra. Por eso
  pueden salir **varios premios grandes en boletos seguidos**: medidos con el
  motor real **4** el martes y el miércoles y **5** el jueves y el viernes, si no
  se ha ganado ninguno antes (ficha **F-283**).
- **El horario del evento sigue mandando**: fuera de 12:00–23:00 no hay ninguna
  pieza abierta, así que tampoco hay forzados.
- El `peso` del premio **se conserva** y deja de decidir mientras esté forzado.
  Sigue apareciendo en la columna **PROB** del boleto de inventario, que describe
  la tómbola y no el resultado (ficha **F-285**).
- Con `false` —o sin la llave— el premio se sortea como siempre. **Los cuatro
  premios chicos no lo llevan.**
- Se ve en el **boleto de inventario** (`*forzado` junto al nombre, con su
  leyenda abajo) y en el **registro** del kiosco, con una línea por boleto:
  `Boleto 00062: pieza forzada de SILLA DE PLAYA`. En el papel del cliente **no
  se nota**.

---

## 6. Cómo se modifica este documento y qué pasa después

1. **Edita este archivo** (`docs/evento-2026-09-asadero-33.md`): cambia lo que
   quieras de las tablas del §1 y del §3, y anota tu cambio en la bitácora del §7.
   **No toques `config.json`**: si los dos archivos dicen cosas distintas, gana
   este documento y el otro se rehace.
2. **Avísame** («ya edité el documento del evento»).
3. **Yo lo convierto** en `config.json` con la cadena de trabajo de siempre:
   ejecutor, dos revisores en paralelo, escéptico, pruebas automáticas y commit
   con compuertas.
4. **Se despliega a la Pi** (`git pull` y reinicio del servicio) y se verifica en
   vivo contra lo desplegado.
5. **Antes del lunes 21, sin falta**, había que hacer dos cosas. **Nota fechada
   (2026-09-16, Fase 4e):**

   **(a) cargar las fechas `desde`/`hasta`** del bloque del §5.1 en `config.json`
   (ficha **F-259**): **HECHO el 2026-09-16.** Ya están puestas, así que la
   hielera no puede salir antes del jueves 24 y **hasta el lunes 21 toda jugada
   sale de consuelo**.

   **(b) poner el marcador en cero**, o los boletos de las pruebas contarán como
   premios ya entregados. Se hace en el **deploy de la Fase 4e**; si por lo que
   fuera no se hubiera hecho, o si quieres abrir el lunes con el folio en
   **00000**, se repite entonces (ficha **F-262**):

   ```bash
   sudo systemctl stop ruleta
   python3 -m ruleta reiniciar --si     # folio y contadores a cero; respalda lo anterior
   sudo systemctl start ruleta
   ```

6. **Comprobaciones finales**, ya con la configuración real cargada:

   ```bash
   python3 -m ruleta reporte                 # stock, cupo, horas de liberación y probabilidad
   python3 -m ruleta vista-previa --todos    # cómo se ve el boleto de cada premio
   ```

   El reporte debe decir **exactamente** los mismos stocks y cupos que la tabla
   del §1. Si no coinciden, algo salió mal y **no se abre el evento**.

---

## 7. Bitácora de cambios de este documento

| Fecha | Quién | Qué cambió |
|---|---|---|
| 2026-09-13 | Claude (ejecutor), del dictado de sdurazo | **Primera versión.** Fechas 21–25 de septiembre, horario 12:00–23:00 de Hermosillo, los 7 premios reales con stock y cupo (167 piezas, 33 al día), nombres y detalles propuestos, modelo de probabilidad «peso = cupo» con escenarios de N = 150 / 250 / 400, franjas propuestas para los grandes y la hielera, 7 preguntas abiertas y el mapa a `config.json` con las tres piezas pendientes de construir (A: peso del consuelo · B: franjas · C: horario del evento). |
| 2026-09-15 | Claude (ejecutor), cierre de la Fase 3 | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo ni ninguna probabilidad.** (1) **Los botones quedaron cableados y probados** en hardware: tres jugadas reales imprimieron boleto (acta: `docs/actas/2026-09-15-fase-3.md`). (2) El usuario decidió que **no habrá batería RTC** y que **la Pi irá con el internet del asadero**, que es lo que le pondrá la hora al encender. (3) De ahí sale una **pieza D pendiente de construir**, además de la A, la B y la C: que el programa **espere a que la hora esté sincronizada** antes de imprimir el inventario y de aceptar jugadas, y lo **avise en el boleto** si no lo consigue. Importa para este documento porque durante los primeros minutos tras encender la Pi cree que es otro día —el 2026-09-15 se midieron unos tres, de las 11:44:42 a las 11:47—, y del día dependen los **topes diarios** y las fechas **`desde`/`hasta`** (ficha **F-241**). (4) Recordatorio con fecha límite, ya escrito en el §6 paso 5: **reiniciar el inventario antes del lunes 21**, porque las pruebas del día dejaron el folio en 10 (ficha **F-243**). (5) **Aviso que afecta a los premios de este documento:** una prueba deliberada con la impresora **sin papel** demostró que hoy, con el rollo agotado, el kiosco **emite el boleto, descuenta el premio y lo da por impreso aunque no salga papel**. Hasta que la Fase 4 lo arregle, la defensa es de procedimiento: **rollo de repuesto junto a la Pi** y cuadrar `boletos.csv` contra la caja al cerrar el día (fichas **F-091**, **F-190** y **F-250**). |
| 2026-09-15 | Claude (escriba), cierre de la Fase 4a | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo ni ninguna probabilidad.** (1) **El papel agotado quedó RESUELTO y probado en hardware.** El aviso del 2026-09-15 que encabeza la línea de arriba —«con el rollo agotado el kiosco emite el boleto, descuenta el premio y lo da por impreso aunque no salga papel»— **ya no es cierto**: desde el commit `2a0aba3` el programa lee el estado real de la impresora y **se niega a jugar sin papel**, devolviendo el premio al inventario. Medido esa misma noche a las **21:32**, con el usuario sacando y reponiendo el rollo: dos jugadas rechazadas con el premio devuelto, **nada retenido en la impresora** y las dos siguientes impresas normales (ficha **F-250**, **resuelta**; **F-091** y **F-190**, cerradas **solo en su parte del papel**: de la **F-190** sigue abierta la **compra del rollo de repuesto** y de la **F-091**, las llaves de ritmo que por cable no tienen efecto; acta `docs/actas/2026-09-15-fase-4a.md`). **La defensa de procedimiento sigue siendo buena idea** —rollo de repuesto junto a la Pi—, pero ya no es lo único que hay. (2) **Lo que FALTA y afecta a la operación de estos cinco días:** **no hay ninguna señal perceptible** de que una jugada fue rechazada. Sin LED conectado, cuando se acabe el rollo el kiosco dejará de dar boletos **en silencio**, y el mesero pensará que falla el botón. Hay tres opciones sobre la mesa (LED real, zumbador propio o un pitido de la impresora) y **la decisión es del usuario**: ficha **F-256**. (3) **Los premios reales, los nombres, los cupos y las franjas de este documento siguen pendientes de tus respuestas** (§4, preguntas abiertas), igual que las piezas **A**, **B**, **C** y **D**. (4) Siguen en pie los dos recordatorios de la línea anterior, con el número al día: **reiniciar el inventario antes del lunes 21** —las pruebas del papel lo dejaron en el **folio 16**, no en 10— (**F-243**), y la **pieza D** de la hora (**F-241**). |
| 2026-09-15 | Claude (ejecutor), Fase 4b | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo ni ninguna probabilidad.** (1) **`config.json` ya lleva los siete premios de este documento.** Se cargó el bloque `"premios"` del §5.1 tal cual —`id`, `nombre`, `detalle`, `stock`, `tope_diario` y `peso` **idénticos**—, **menos `desde` y `hasta`, omitidos a propósito** (ficha **F-259**): con las fechas puestas (del 21 al 25) **ningún** premio estaría disponible el **miércoles 16**, y lo que pediste fue justamente probar ese día los nombres y los detalles en papel para corregirlos. **Hay que cargar las fechas antes del lunes 21.** (2) **El bloque del §5.1 y `config.json` ya no se pueden desincronizar en silencio:** una prueba automática **deriva** los premios del bloque del §5.1 **de este documento** y los compara campo por campo con `config.json`; si dejan de coincidir, la suite se pone en rojo (`tests/test_config.py`, `TestPremiosOficialesDelEvento`). **Ojo: esa prueba NO vigila la tabla del §1** —medido el 2026-09-15: cambiando solo el §1, la suite sigue en verde—, así que cuando corrijas ahí un nombre (pregunta 6 del §4) hay que copiarlo también al bloque del §5.1 y de ahí a `config.json` (ficha **F-260**). Sigue mandando este documento, como dice el §6 paso 1. (3) **Lo que sigue pendiente de ti:** las siete preguntas del §4, empezando por los **nombres y detalles marcados con \*** (pregunta 6, ficha **F-260**) y por **N** (pregunta 1); y las piezas **A**, **B**, **C** y **D**. (4) **Recordatorio con fecha, ya escrito en el §6:** sin la **pieza A**, y mientras `config.json` vaya sin fechas, **las primeras 34 jugadas de cada día ganan premio, una tras otra** —34 y no 33 porque sin `desde` la hielera también entra; en cuanto se entreguen sus dos piezas son 33— (ficha **F-261**), y **hay que volver a reiniciar el inventario el lunes 21 antes de abrir** si el 16 se juega (ficha **F-262**). Plan: `docs/planes/fase-4b-config-oficial.md`. El despliegue a la Pi y el reinicio del inventario a **folio 00000** van en esta misma fase, **después** de esta edición. |
| 2026-09-16 | Claude (ejecutor), Fase 4c | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo, ninguna probabilidad de las tablas ni ninguna pregunta del §4.** (1) **La pieza A quedó CONSTRUIDA**, que es lo que este documento llamaba «lo más importante»: el boleto de consuelo tiene **`peso` propio** y **compite en cada jugada**, con la forma exacta que proponía el §5.2 —`"peso"` dentro de `juego.consuelo`—, cargada en `config.json` con **217** (= N − 33 con **N = 250**, la propuesta por omisión de la **pregunta 1 del §4**). El §5.2 y la tabla del encabezado quedaron marcados, **sin borrar la propuesta**. (2) **Por qué ahora:** el **2026-09-16**, probando en vivo, el usuario reportó que «no ha salido ningún boleto de gracias por participar, solo premios». Era exactamente lo que este documento tenía escrito y lo que la ficha **F-261** anotaba: sin la pieza A ganaban las primeras **34** jugadas del día, una tras otra. **F-261 queda cerrada.** (3) **Cómo quedó, calculado por el programa** con el `config.json` real (todavía **sin `desde`/`hasta`**, así que la hielera entra todos los días): 34 papelitos de premio + 217 del consuelo = **251**; **gana el 13.55 % de las jugadas**, 1 de cada 7 u 8. (4) **Dos redes nuevas que muerden:** una prueba automática **deriva** el bloque `consuelo` **de este documento** (§5.2) y lo compara con `config.json`, y otra comprueba que el `peso` del §5.2 obedezca la regla **N − 33** del §2 y sea una de las N que ese §2 tabula. Si cambias N en un solo sitio, la suite se pone en rojo. (5) **Lo que sigue pendiente de ti:** las siete preguntas del §4, empezando por **N** (pregunta 1; el 217 es mi propuesta, no tu decisión: ficha **F-263**) y por los **nombres y detalles** (pregunta 6, **F-260**); y las piezas **B** (franjas), **C** (horario) y **D** (la hora, **F-241**). (6) **Recordatorios con fecha, sin cambios:** cargar `desde`/`hasta` antes del lunes 21 (**F-259**) y **reiniciar el inventario** antes de abrir (**F-243**, **F-262**) — esta fase **no** lo reinició, porque el usuario estaba probando. Plan: `docs/planes/fase-4c-consuelo-peso.md`. |
| 2026-09-16 | Claude (ejecutor), Fase 4d | **Esta vez SÍ cambiaron tablas, y con tu permiso: «así va, apúntalo y lanza la cadena».** (1) **Se cayó el modelo de N.** Dijiste que **es imposible saber cuántas jugadas habrá**, y todo el §2 viejo colgaba de ese número. El §2 se reescribió entero: **los premios se reparten por HORAS**, el cupo del día se abre poco a poco de 12:00 a 23:00, y **N ya no existe**. La explicación vieja (peso = cupo, N − 33, el 84 % de entrega) se conserva como **nota histórica corta** al final del §2. La **pregunta 1 del §4** queda respondida: *ya no hace falta*. (2) **Se construyeron las tres piezas que faltaban: B (franjas), C (horario del evento) y D (esperar la hora al encender).** Con la A ya hecha, **las cuatro están construidas** y el encabezado lo dice. (3) **Se cargaron en `config.json`**: el `horario` 12:00–23:00 con `fuera_de_horario: "consuelo"` (tu respuesta a la **pregunta 5**), las **franjas** de la hielera, la silla y el set BBQ (**preguntas 2 y 3**), **3 minutos** de separación mínima entre premios («los premios no deben salir seguidos») y **120 s** de espera de la hora al arrancar. (4) **El peso del consuelo bajó de 217 a 10**, que es lo que tiene sentido cuando compite contra una o dos piezas abiertas y no contra los 34 papelitos del día: con un agua abierta se gana el **52.4 %** de las jugadas; con solo la hielera, el **9.1 %**. (5) **Se confirmaron los siete nombres y detalles** (**pregunta 6**) y se quitaron **todos los asteriscos** de la tabla del §1; los dos cambios tuyos son **CERVEZA → «Tecate Light, Tecate Roja o Indio»** y **AGUA FRESCA → «Horchata, Jamaica o Cebada»**. Ficha **F-260**, cerrada. (6) **Lo importante que esto arregla, medido por el programa:** simulando un día entero, **salga la gente que salga se entrega el cupo completo** (34 de 34 con 1 980, 660 o 220 jugadas; 31.7 con solo 66). Con el modelo viejo, acertando N, se entregaba el **84 %**. (7) **Lo que sigue pendiente de ti:** solo la **pregunta 7** (factor de holgura), que con este modelo casi no aplica. (8) **Recordatorios con fecha, sin cambios:** **cargar `desde`/`hasta` antes del lunes 21** (**F-259**) y **reiniciar el inventario** antes de abrir (**F-243**, **F-262**). Se cerró la **F-266** reescribiendo el párrafo «Sobre el reloj» del §5.1, que todavía decía que la Pi iba sin red. Plan: `docs/planes/fase-4d-horas.md`. |
| 2026-09-16 | Claude (escriba), cierre de las Fases 4b, 4c y 4d | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo, ninguna probabilidad ni ninguna pregunta del §4.** (1) **Lo probaste tú y funciona.** Después de que un agente reiniciara el inventario a **folio 00000** a las **12:46** del 2026-09-16, con el reparto por horas ya desplegado, jugaste y dijiste: **«ya probé, salieron consuelos y una cerveza, funciona bien»**. Cuadra con lo que este documento promete: a esa hora estaban abiertas **el agua (12:30)** y **la cerveza (12:33)** —y, si ya habían dado las **13:00**, también **una silla** y **un set BBQ**; la hora exacta de esas jugadas no se midió—, con los **3 minutos** de separación entre premios. (2) **Las tres fases quedan CERRADAS** —`f810bc4` (premios reales), `d01a0ca` (pieza A) y `613f875` (piezas B, C y D más el reparto por horas)—, las tres desplegadas y verificadas en la Pi, con la suite en **268 pruebas en verde** allá y aquí. (3) **Lo único que falta antes del lunes 21, y no es programación:** **cargar las fechas `desde`/`hasta`** del §5.1 (ficha **F-259**) y **reiniciar el inventario antes de abrir** (fichas **F-262** y **F-243**) — después del reinicio de las 12:46 volviste a jugar, así que **no está en cero**. Además, el **perfil Wi-Fi del asadero** todavía no está en la Pi y **la contraseña la tecleas tú**. (4) **Dos avisos honestos sobre lo que aún no se ha visto en hardware:** la línea `HORA SIN CONFIRMAR: revisar fecha` **no se ha impreso nunca en papel** —las dos veces que el servicio arrancó ese día ya con esta pieza dentro, la Pi ya tenía la hora— y **la separación de 3 minutos tampoco se ha visto morder en el journal**; las dos están probadas con goldens, no con la Pi. (5) **De ti sigue sin respuesta solo la pregunta 7** del §4 (factor de holgura), que con el reparto por horas casi no aplica. Acta con todo lo medido: `docs/actas/2026-09-16-fase-4bcd.md`; hechos en crudo: `docs/actas/2026-09-16-hechos-medidos-fase-4bcd.md`. |
| 2026-09-16 | Claude (ejecutor), Fase 4e | **No cambió ninguna tabla, ningún cupo, ninguna probabilidad ni ninguna pregunta del §4: esta pasada CARGA lo que ya decía este documento.** (1) **Las fechas `desde`/`hasta` del §5.1 ya están en `config.json`**: la hielera **24 y 25**, los otros seis **del 21 al 25**. Era el último pendiente con fecha límite (ficha **F-259**, cerrada). **Consecuencia escrita en el §5.1 y en el README: hasta el lunes 21 toda jugada sale de consuelo**, porque ningún premio está dentro de fechas. (2) **La espera de la hora al encender subió de 120 a 300 segundos** (§5.1 y §5.2 D). Motivo medido: en el arranque en frío del 2026-09-16 la hora tardó **34 s** en llegar por NTP **en la red de casa y por IPv6**; la del asadero puede tardar distinto, y el tope es margen, no coste. (3) **La pieza D quedó probada en hardware**, que era lo único que le faltaba: con la Pi desenchufada, el reloj arrancó **4 min 54 s atrasado** (lo restaura **systemd**, no `fake-hwclock`, que no está instalado), el kiosco **esperó 28.3 s** y **el inventario salió 0.6 s después con la fecha correcta**. Ficha **F-241**, cerrada en hardware. (4) **Ahora la espera se ve en el journal**: una línea al empezar, otra cada 10 s y una última con lo que costó (ficha **F-273**, cerrada). (5) **Lo que NO cambió:** premios, stocks, cupos, pesos, franjas, horario, separación y textos del boleto, todos idénticos. Plan: `docs/planes/fase-4e-final.md`; hechos medidos: `docs/actas/2026-09-16-hechos-medidos-fase-4e.md`. |
| 2026-09-16 | Claude (escriba), cierre documental de la Fase 4e | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo, ninguna probabilidad ni ninguna pregunta del §4.** (1) **El kiosco quedó LISTO PARA EL EVENTO.** El commit `70bcaa6` se desplegó en la Pi a las **14:44** del 2026-09-16, con la suite en **273 pruebas en verde** allá y aquí, el servicio `active` y `NRestarts=0`. (2) **El inventario está en cero.** En ese mismo despliegue, y **después de que dijeras «listo, ya terminé las pruebas, reinicia el inventario para que quede listo»**, se reinició por última vez: de **folio 00010 con 2 premios entregados** —una cerveza y un agua— a **folio 00000**, con respaldos fechados. **El lunes 21 ya no hay que reiniciar nada**; hacerlo es decisión tuya (fichas **F-243**, cerrada, y **F-262**). (3) **Lo que pediste sobre la hora quedó probado en hardware, no en teoría.** Con la Pi **desenchufada**, el reloj arrancó **4 min 54 s atrasado**, el kiosco **esperó 28.3 s** sin imprimir nada y **el inventario salió 0.6 s después con la fecha correcta**: el orden **Pi → internet → hora → inventario → listo** se cumple (ficha **F-241**, cerrada en hardware). (4) **Dos avisos honestos:** el tope de **300 s nunca se ha agotado** en la Pi y la línea `HORA SIN CONFIRMAR: revisar fecha` **sigue sin imprimirse nunca en papel**; las dos cosas están probadas con goldens, no con hardware. (5) **Lo que falta antes de abrir, y no es programación:** dar de alta el **Wi-Fi del asadero en la Pi** —**en sitio y tecleando tú la contraseña**—, hacer allá una **prueba de corriente** y **mirarle la fecha al boleto de inventario**, **asegurar el pulsador HABILITAR** y decidir la **señal cuando una jugada se rechaza**, que hoy no se percibe porque no hay LED (fichas **F-278**, **F-275**, **F-239**, **F-256**). (6) **De ti sigue sin respuesta solo la pregunta 7** del §4 (factor de holgura), que con el reparto por horas casi no aplica. Acta con todo lo medido: `docs/actas/2026-09-16-fase-4e.md`; hechos en crudo: `docs/actas/2026-09-16-hechos-medidos-fase-4e.md`. |
| 2026-09-21 | Claude (escriba), apertura del evento | **Solo esta línea de bitácora: no se tocó ninguna tabla, ningún cupo, ninguna probabilidad ni ninguna pregunta del §4.** (1) **La red del restaurante ya está en la Pi.** A las ~08:20 del lunes 21, en el asadero, levantaste el punto de acceso de tu laptop, entraste por SSH y **tecleaste tú la contraseña**: quedó el perfil `asadero` apuntando al Wi-Fi **`INFINITUM04F0_2.4`** con **prioridad 30**, por encima de `casa` (20) y `miltimex` (10). Un agente de solo lectura lo comprobó a las **08:26**: internet OK y `timedatectl` → **`synchronized yes`**. Fichas **F-275** y **F-278**, cerradas. (2) **La prueba de corriente, hecha allá y con el peor caso posible.** La Pi encendió creyendo que era el **16 de septiembre a las 15:46** —unos 4 días y 17 horas atrasada—, **no imprimió nada durante 28 segundos**, agarró la hora por el internet del asadero y sacó el boleto de inventario a las **08:22:21**, con **folio `00000`** y **sin** la línea `HORA SIN CONFIRMAR`. (3) **Y lo confirmaste en papel:** «**sí, el boleto dice 21/09/2026 08:22**». Es la primera vez que esa fecha se lee en papel después de un arranque en frío en el sitio real. (4) **La duda que dejaba este documento queda respondida.** El §5.1 decía que esos 28 s se habían medido en la red de casa y que **la del asadero podía tardar distinto**: tardó **lo mismo, 28 s**, así que los **300 segundos** de espera siguen siendo margen de sobra. (5) **Dos avisos honestos, los de siempre:** el tope de **300 s nunca se ha agotado** en la Pi y la línea `HORA SIN CONFIRMAR: revisar fecha` **sigue sin imprimirse nunca en papel**. Lo que sí dejó de ser teoría son **los avisos de los 10 segundos** del registro, vistos **por primera vez en hardware** esa mañana. (6) **Lo que queda es decisión tuya, y no impide abrir:** **asegurar o soldar el pulsador HABILITAR** (**F-239**) y **la señal cuando una jugada se rechaza**, que hoy no se percibe porque no hay LED (**F-256**). (7) **Aviso nuevo para el evento:** tras un arranque en frío el registro queda con **dos fechas distintas** y `systemctl status` dice que el servicio arrancó el día viejo; **no es avería** (ficha **F-279**). (8) **De ti sigue sin respuesta solo la pregunta 7** del §4 (factor de holgura), que con el reparto por horas casi no aplica. **Este documento no cubre la apertura misma:** lo medido llega hasta las **08:35**. Acta: `docs/actas/2026-09-21-apertura.md`; hechos en crudo: `docs/actas/2026-09-16-hechos-medidos-fase-4e.md`, sección «En el asadero · 2026-09-21». |
| 2026-09-22 | Claude (ejecutor), día 2 · paso 1 | **Esta vez SÍ cambiaron tablas, y con tu permiso: «así va».** (1) **Lo que pasó el lunes 21, medido:** **55 jugadas** y **27 premios**; **agua 11 de 11**, **cerveza 8 de 10**, **3 tacos 4 de 4**, **2 tacos 3 de 4**, **set BBQ 1 de 2** y **silla 0 de 2**. Los grandes se quedaron en la bodega por dos razones medidas: **casi nadie jugó en sus franjas** (9 jugadas entre 13:00 y 16:00; **ninguna** entre 19:00 y 20:00) y **con peso 2 salían en ≈ 5 % de las jugadas**, porque competían contra el agua (11), la cerveza (10), los tacos (4 + 4) y el consuelo (10); además **6 jugadas** salieron de consuelo solo por la separación de 3 minutos. Ficha **F-280**. (2) **La separación entre premios baja de 3 minutos a 1** (§2, regla 4). (3) **La silla, el set BBQ y la hielera pasan a peso 100** (§2 y §3): en cuanto el reloj abre uno, se lleva **≈ 42 %** de las jugadas con todo lo demás abierto y **≈ 91 %** si está solo. (4) **Las franjas se mueven a horas sueltas y repartidas** (§1 y §3): silla **13:17** y **19:23**, set BBQ **14:41** y **20:47**, hielera **19:36**; cada pieza dura **dos horas**, menos la de la hielera, que llega **hasta el cierre** (**19:36–23:00**). (5) **Se repone lo que no salió el lunes**: entre martes y viernes pueden salir **10 sillas** y **9 sets BBQ** —martes 3 y 3, miércoles 3 y 2, jueves y viernes 2 y 2—. Para conseguirlo, y porque `config.json` **solo admite un juego de franjas y un cupo diario por premio**, se añaden **dos entradas de apaño** con el **mismo nombre en el boleto**: `silla_extra` (mar y mié, 16:08) y `bbq_extra` (solo el mar, 17:34). Ficha **F-281**. (6) **Lo que este paso NO puede hacer, y llega en el paso 2** (que sí toca el programa): **horas distintas por día**. Hoy rigen **las del martes los cuatro días**, y la hielera queda a las **19:36 el jueves y el viernes**, cuando lo suyo sería una hora distinta cada día: **19:36** y **20:04**, dos horas que **propuse yo**, no tú. (7) **Lo que sobró el lunes de cerveza (2) y de 2 tacos (1) NO se repone**: decisión del orquestador, la puedes cambiar (ficha **F-282**). (8) **Lo que NO cambió:** nombres, detalles, textos del boleto, stocks de los chicos, cupos de los chicos, horario 12:00–23:00, `espera_hora_seg` y las fechas `desde`/`hasta` de los siete premios de siempre. Plan: `docs/planes/dia2-paso1-config.md`. |
| 2026-09-22 (tarde) | Claude (ejecutor), día 2 · paso 2 | **Cambiaron las tablas de horas del §1 y del §3, con tu dictado de esta tarde, y esta vez SÍ se tocó el programa.** (1) **Cada día tiene sus horas.** El programa aprendió la llave **`dias` dentro de cada franja**, así que se acabó lo de que las horas del martes rigieran los cuatro días (era el límite escrito del paso 1). Quedan cargadas las que dictaste: sillas **13:17 · 16:08 · 19:23** el martes, **13:09 · 16:21 · 19:38** el miércoles, **13:26 · 19:11** el jueves y **13:04 · 19:31** el viernes; sets BBQ **14:41 · 17:34 · 20:47**, **14:52 · 20:19**, **14:37 · 20:52** y **14:58 · 21:06**; y la **hielera** a las **19:36** el jueves y a las **20:04** el viernes, las dos hasta el cierre. Siguen siendo **10 sillas y 9 sets** entre martes y viernes. Los minutos exactos los repartí yo; el reparto por días es tuyo. (2) **La silla, el set BBQ y la hielera salen FORZADOS**, que es tu «después de tal hora, el próximo juego se la saca»: **la siguiente jugada se lleva la pieza abierta, sin sorteo**. Se explica en llano en el §3 y en el §5.2 **E**, que es una **pieza nueva** del programa, la quinta. (3) **El forzado se salta el minuto de separación** (§2, regla 4), porque lo que pediste es la *siguiente* jugada. **Consecuencia medida:** si hay dos o tres piezas grandes abiertas y nadie ha jugado, **salen en boletos seguidos** —el jueves a las 19:40: silla, silla y hielera—. Ficha **F-283**. (4) **Dónde se ve:** el boleto de inventario marca esos premios con **`*forzado`** y una leyenda al pie, y el registro deja una línea por boleto; en el **papel del cliente no se nota nada**. (5) **La columna PROB del inventario sigue siendo la de la tómbola**, así que para un premio forzado y abierto **no dice la verdad del resultado**: manda el forzado. Ficha **F-285**. (6) **Las entradas `silla_extra` y `bbq_extra` SE QUEDAN** aunque ya no hagan falta para las horas por día: `estado.json` cuenta **por id** y quitarlas con premios ya entregados descontaría mal. Se retiran al cerrar el viernes (fichas **F-281** y **F-284**). (7) **Lo que NO cambió:** nombres, detalles, stocks, cupos, pesos, horario 12:00–23:00, `espera_hora_seg`, peso del consuelo y las fechas `desde`/`hasta`. Plan: `docs/planes/dia2-paso2-forzado.md`. |
|  |  |  |
