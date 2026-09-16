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

---

## Cómo usar este documento

Este es **el documento del evento**: aquí viven los premios, los cupos y las
horas. Está escrito para que **tú lo edites a mano**.

- Las **tablas** del §1 y del §3 son **tu dictado**, ya **confirmado por ti el
  2026-09-16**. Las explicaciones, los cálculos y los formatos de `config.json`
  (los §2, §3, §5 y §6) los escribí yo a partir de ese dictado y del código.
- Lo que lleve un asterisco **\*** sería una propuesta mía a confirmar. **Hoy ya
  no queda ninguno en las tablas de premios.**
- **No edites `config.json`.** Edita este archivo, avísame, y yo lo convierto en
  `config.json` con la cadena de revisión (§6).

### Las cuatro piezas que faltaban ya están construidas

Este documento describía cuatro piezas del programa que había que construir para
que el evento saliera tal cual. **Las cuatro están hechas**:

| # | Pieza | Cuándo se construyó |
|---|---|---|
| ~~**A**~~ | ~~**Probabilidad propia del boleto de consuelo**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4c). El consuelo tiene `peso` propio y compite en cada jugada. |
| ~~**B**~~ | ~~**Franjas horarias por premio, con cupo por franja**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4d). La hielera solo de 19:00 a 23:00; la silla y el set BBQ, una pieza en la comida y otra en la cena. |
| ~~**C**~~ | ~~**Horario del evento (12:00–23:00)**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4d). Fuera de ese horario la ruleta imprime **boleto de consuelo**. |
| ~~**D**~~ | ~~**Esperar a que la hora esté sincronizada al encender**~~ | **CONSTRUIDA** el 2026-09-16 (Fase 4d). Al arrancar, la Pi espera hasta **5 minutos** a tener la hora buena; si no la consigue, **lo escribe en el boleto**. (El tope subió de 2 a 5 minutos el 2026-09-16, Fase 4e, tras probarlo con la Pi desenchufada; §5.1.) |

**Lo que se puede cargar en la Pi es este documento entero**, y desde el
**2026-09-16** (Fase 4e) **ya lo está, fechas incluidas**: las `desde`/`hasta` del
§5.1 se cargaron en `config.json` (ficha **F-259**, cerrada).

---

## 1. Los premios

**Los siete nombres y detalles los confirmaste el 2026-09-16** (era la pregunta 6
del §4), con dos correcciones tuyas: la cerveza y el agua ahora dicen de qué son.
Ya **no hay asteriscos**: todo lo de esta tabla es tuyo.

| id | NOMBRE EN EL BOLETO | Detalle (texto chico) | Tipo | Stock | Cupo/día | Días en que sale | Franja horaria |
|---|---|---|---|---|---|---|---|
| `hielera` | **HIELERA IGLOO** | Premio mayor | mayor | **2** | **1** | **jue 24 y vie 25** | **19:00–23:00** |
| `silla` | **SILLA DE PLAYA** | Premio grande | grande | **10** | **2** | **los 5 días** | 13:00–16:00 y 19:00–22:00, **1 en cada una** |
| `bbq` | **SET BBQ** | Premio grande | grande | **10** | **2** | **los 5 días** | 13:00–16:00 y 19:00–22:00, **1 en cada una** |
| `tacos3` | **3 TACOS DE PASTOR** | Plato de 3 tacos de pastor | chico | **20** | **4** | **los 5 días** | **todo el día**, repartidos parejo |
| `tacos2` | **2 TACOS DE PASTOR** | Plato de 2 tacos de pastor | chico | **20** | **4** | **los 5 días** | **todo el día**, repartidos parejo |
| `cerveza` | **CERVEZA** | Tecate Light, Tecate Roja o Indio | chico | **50** | **10** | **los 5 días** | **todo el día**, repartidas parejo |
| `agua` | **AGUA FRESCA** | Horchata, Jamaica o Cebada | chico | **55** | **11** | **los 5 días** | **todo el día**, repartidas parejo |
| **Totales** | | | | **167** | **33** al día (**34** el jueves 24 y el viernes 25) | | |

### La cuenta cuadra exactamente

Comprobado con calculadora el 2026-09-13 y sin cambios desde entonces: **cupo
diario × días = stock, para los siete premios**, sin sobrar ni faltar una pieza.

| Premio | Cupo × días | Stock | ¿Cabe? |
|---|---|---|---|
| `hielera` | 1 × 2 días = **2** | 2 | sí, exacto |
| `silla` | 2 × 5 días = **10** | 10 | sí, exacto |
| `bbq` | 2 × 5 días = **10** | 10 | sí, exacto |
| `tacos3` | 4 × 5 días = **20** | 20 | sí, exacto |
| `tacos2` | 4 × 5 días = **20** | 20 | sí, exacto |
| `cerveza` | 10 × 5 días = **50** | 50 | sí, exacto |
| `agua` | 11 × 5 días = **55** | 55 | sí, exacto |
| **Total** | 33 × 5 + 1 × 2 = **167** | **167** | **cuadra** |

Por día: **4 premios grandes** (2 sillas + 2 sets) y **29 chicos** (4 + 4 + 10 +
11) = **33**; el jueves y el viernes se suma **1 hielera** = **34**.

Como no sobra margen, si un día sale menos de lo previsto **esas piezas se quedan
en la bodega**: el cupo **no** se arrastra al día siguiente.

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

Tabla **calculada por el programa** el 2026-09-16 con el `config.json` real y el
horario de 12:00 a 23:00. Cada pieza se abre en el **punto medio** de su tramo,
para que ni la primera salga al abrir ni la última al cerrar:

| Premio | Piezas al día | Se abren a las |
|---|---|---|
| **AGUA FRESCA** | 11 | 12:30 · 13:30 · 14:30 · 15:30 · 16:30 · 17:30 · 18:30 · 19:30 · 20:30 · 21:30 · 22:30 |
| **CERVEZA** | 10 | 12:33 · 13:39 · 14:45 · 15:51 · 16:57 · 18:03 · 19:09 · 20:15 · 21:21 · 22:27 |
| **3 TACOS DE PASTOR** | 4 | 13:22 · 16:07 · 18:52 · 21:37 |
| **2 TACOS DE PASTOR** | 4 | 13:22 · 16:07 · 18:52 · 21:37 |
| **SILLA DE PLAYA** | 2 | 13:00 (franja de la comida) · 19:00 (franja de la cena) |
| **SET BBQ** | 2 | 13:00 (franja de la comida) · 19:00 (franja de la cena) |
| **HIELERA IGLOO** | 1 (jue y vie) | 19:00 (franja de la noche) |

Las piezas con **franja** se abren **al empezar su franja**, no a la mitad: la
silla se puede ganar **a las 13:00 en punto**.

### Cuatro reglas que van con esto, y que tú dictaste

1. **Una pieza abierta no la gana forzosamente la primera jugada.** El boleto de
   consuelo sigue compitiendo, con **peso 10**. Si a las 12:30 se abrió un agua y
   alguien juega, gana el agua **52 de cada 100 veces**; las otras 48 se llevan
   su «gracias por participar».
2. **Lo que se abre y no se gana, no se pierde.** Esa agua sigue esperando a
   quien la gane, hasta las 23:00. Pero **tampoco adelanta la siguiente**: la
   número 2 no se abre hasta las 13:30, pase lo que pase.
3. **Las piezas no se acumulan por adelantado.** Al abrir el día no hay nada
   abierto: a las 12:00 en punto, **la primera jugada del día no puede ganar**
   (la primera pieza se abre a las 12:30).
4. **Los premios no salen seguidos.** Entre dos boletos con premio tienen que
   pasar al menos **3 minutos**. Dentro de esos 3 minutos toda jugada sale de
   consuelo, aunque haya piezas abiertas.

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

### Qué tan seguido se gana, momento a momento

Depende de **qué haya abierto en ese instante**, no de una tabla fija. Dos
ejemplos, **calculados por el programa** con el `config.json` real:

| Qué está abierto en ese momento | Papelitos | Gana |
|---|---|---|
| Una pieza de AGUA FRESCA (peso 11) | 11 + 10 = 21 | **52.4 %** |
| Solo la HIELERA IGLOO (peso 1) | 1 + 10 = 11 | **9.1 %** |

El **10** de las dos filas es el **peso del boleto de consuelo**, y es el único
número de todo el modelo que se puede subir o bajar si quieres que gane más o
menos gente. El porcentaje exacto de cada momento lo ves sin imprimir con
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

| Premio | Franja | Cupo en esa franja | Días | Se abre a las |
|---|---|---|---|---|
| HIELERA IGLOO | **19:00 – 23:00** | 1 | **jue 24** y **vie 25** | 19:00 |
| SILLA DE PLAYA | **13:00 – 16:00** | 1 | los 5 días | 13:00 |
| SILLA DE PLAYA | **19:00 – 22:00** | 1 | los 5 días | 19:00 |
| SET BBQ | **13:00 – 16:00** | 1 | los 5 días | 13:00 |
| SET BBQ | **19:00 – 22:00** | 1 | los 5 días | 19:00 |

La idea: **una comida y una cena**. De 13:00 a 16:00 cae la comida fuerte, y de
19:00 a 22:00 la cena, que es cuando más lleno está. Así el que llega temprano
también tiene con qué ganar.

**Lo que sí puede pasar, y conviene saberlo:** si en la comida no se gana la
silla ni el set BBQ, esas dos piezas **no se pierden**, se suman a las de la
cena, y entre 19:00 y 22:00 pueden salir **los cuatro premios grandes del día**.
El `tope_diario` (2 sillas y 2 sets) sigue cortando el día, así que nunca salen
más de cuatro. Ficha **F-269**.

**Ya no hacen falta «pesos de franja».** Con el modelo viejo había que inflar el
peso de la silla a 12 para compensar que compitiera en pocas jugadas. Con el
reparto por horas eso sobra: la silla **es la única pieza grande abierta** en su
franja y compite solo contra el consuelo y los chicos que estén abiertos. Los
pesos se quedan en su cupo diario (silla 2, set 2, hielera 1).

### Los premios chicos NO llevan franja

Se reparten solos, parejo de 12:00 a 23:00, con las horas de la tabla del §2. Es
lo más simple de operar y de explicarle al personal, y con el reparto por horas
ya no hay riesgo de que se acaben a media tarde: **no pueden**, porque el reloj
no los ha abierto.

### Nota de las 22:00 a las 23:00

Las franjas no terminan a la misma hora: la de los grandes cierra a las **22:00**
y la de la hielera a las **23:00**. Entre 22:00 y 23:00 del jueves y el viernes,
en la tómbola quedan los chicos, el consuelo y la hielera. Calculado por el
programa a las 22:30 del jueves, con todo abierto sin ganar: la hielera va al
**2.5 %** por jugada.

---

## 4. Preguntas abiertas

- [x] **1. ¿Cuántas jugadas esperas por día (N)?**
  **YA NO HACE FALTA** (2026-09-16). Tu respuesta fue que **es imposible
  saberlo**, y de ahí salió el reparto por horas del §2, que **no usa N**.

- [x] **2. Franjas de la SILLA DE PLAYA y el SET BBQ.**
  **SÍ**, las dos: **13:00–16:00 y 19:00–22:00, una pieza en cada franja**
  (2026-09-16). La de los grandes cierra a las 22:00, no a las 23:00.

- [x] **3. Confirmar la HIELERA: 19:00–23:00 los días 24 y 25, una por día.**
  **SÍ** (2026-09-16).

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

**Los premios**, con sus descripciones confirmadas y sus franjas:

```json
"premios": [
  { "id": "hielera", "nombre": "HIELERA IGLOO",     "detalle": "Premio mayor",                      "stock": 2,  "tope_diario": 1,  "peso": 1,  "desde": "2026-09-24", "hasta": "2026-09-25",
    "franjas": [ { "desde_hora": "19:00", "hasta_hora": "23:00", "tope": 1 } ] },
  { "id": "silla",   "nombre": "SILLA DE PLAYA",    "detalle": "Premio grande",                     "stock": 10, "tope_diario": 2,  "peso": 2,  "desde": "2026-09-21", "hasta": "2026-09-25",
    "franjas": [ { "desde_hora": "13:00", "hasta_hora": "16:00", "tope": 1 },
                 { "desde_hora": "19:00", "hasta_hora": "22:00", "tope": 1 } ] },
  { "id": "bbq",     "nombre": "SET BBQ",           "detalle": "Premio grande",                     "stock": 10, "tope_diario": 2,  "peso": 2,  "desde": "2026-09-21", "hasta": "2026-09-25",
    "franjas": [ { "desde_hora": "13:00", "hasta_hora": "16:00", "tope": 1 },
                 { "desde_hora": "19:00", "hasta_hora": "22:00", "tope": 1 } ] },
  { "id": "tacos3",  "nombre": "3 TACOS DE PASTOR", "detalle": "Plato de 3 tacos de pastor",        "stock": 20, "tope_diario": 4,  "peso": 4,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "tacos2",  "nombre": "2 TACOS DE PASTOR", "detalle": "Plato de 2 tacos de pastor",        "stock": 20, "tope_diario": 4,  "peso": 4,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "cerveza", "nombre": "CERVEZA",           "detalle": "Tecate Light, Tecate Roja o Indio", "stock": 50, "tope_diario": 10, "peso": 10, "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "agua",    "nombre": "AGUA FRESCA",       "detalle": "Horchata, Jamaica o Cebada",        "stock": 55, "tope_diario": 11, "peso": 11, "desde": "2026-09-21", "hasta": "2026-09-25" }
]
```

**El juego**, con el horario del evento, la separación entre premios, la espera
de la hora al encender y el peso del consuelo:

```json
"juego": {
  "horario": { "abre": "12:00", "cierra": "23:00", "fuera_de_horario": "consuelo" },
  "separacion_min_entre_premios": 3,
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
— **CONSTRUIDA el 2026-09-16, Fase 4d**. Esta es la forma exacta del campo, y es
**la franja de la hielera tal cual está cargada**:

```json
"franjas": [ { "desde_hora": "19:00", "hasta_hora": "23:00", "tope": 1 } ]
```

Reglas de ese campo, tal como quedaron:

- Un premio **con** `franjas` **no está disponible fuera de ellas**.
- `tope` son las piezas que esa franja **abre** ese día; además siguen mandando
  el `tope_diario` del premio y su `stock`. **Ojo, porque el programa NO lleva la
  cuenta franja por franja:** cuenta «piezas abiertas hoy menos entregadas hoy»,
  así que **lo que una franja abre y nadie gana se arrastra a la siguiente franja
  del mismo día**. Si la silla de la comida no sale, a las 19:00 hay **dos**
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
|  |  |  |
