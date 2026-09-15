# Evento de la ruleta · Asadero 33 · septiembre de 2026

**Fechas:** del **lunes 21 al viernes 25 de septiembre de 2026** (5 días seguidos).
**Horario:** de **12:00 a 23:00**, hora de Hermosillo (`America/Hermosillo`; Sonora
no cambia de horario, así que es la misma hora todo el evento).
**Días con nombre:** 21 lunes · 22 martes · 23 miércoles · **24 jueves** · **25 viernes**.

**Última edición:** 2026-09-15 · Claude (ejecutor), y **solo la bitácora del §7**
(cierre de la Fase 3). Los premios, los cupos, las franjas y las probabilidades
siguen siendo los del dictado de sdurazo del **2026-09-13**: no se tocó ninguna
tabla.

---

## Cómo usar este documento

Este es **el documento del evento**: aquí viven los premios, los cupos y las
horas. Está escrito para que **tú lo edites a mano**.

- En las **tablas** del §1 y del §3, lo que está **sin marca** viene de tu dictado
  del 2026-09-13: **no lo cambié.** El resto del documento (las explicaciones, los
  cálculos, el modelo de probabilidad y los formatos de `config.json` de los §2,
  §3, §5 y §6) lo escribí yo a partir de tu dictado y del código: también es **a
  confirmar**.
- Lo que lleva un asterisco **\*** es **una propuesta mía** y está **a
  confirmar**: cámbialo con toda confianza.
- **No edites `config.json`.** Edita este archivo, avísame, y yo lo convierto en
  `config.json` con la cadena de revisión (§6).

### Tres cosas que el programa TODAVÍA NO SABE HACER

Este documento describe el evento que quieres. Hay tres piezas del programa que
**hay que construir** para que el evento salga tal cual. Están marcadas
**PENDIENTE DE CONSTRUIR** en todo el documento:

| # | Falta | Qué pasa hoy sin eso |
|---|---|---|
| **A** | **Probabilidad propia del boleto de consuelo** | Hoy el consuelo **solo** sale cuando ya no queda **ningún** premio disponible. Es decir: **las primeras 33 jugadas del día ganan premio, una tras otra**, y de la 34 en adelante todo es consuelo. (El 24 y el 25 son 34, y de la 35 en adelante.) *Medido el 2026-09-13 corriendo el sorteo real del programa con estos premios.* |
| **B** | **Franjas horarias por premio, con cupo por franja** | Hoy un premio solo se puede limitar por **día** (`tope_diario`) y por **fecha** (`desde`/`hasta`). **No hay forma de decir "de 7 a 11 de la noche".** La hielera saldría a cualquier hora del 24 y del 25. |
| **C** | **Horario del evento (12:00–23:00)** | Hoy la ruleta juega a **cualquier hora** en que alguien apriete JUGAR con el mesero habilitando. No conoce la hora de apertura ni la de cierre. |

Hasta que existan A, B y C, lo único que se puede cargar en la Pi es la parte
del §5.1, «lo que YA se puede cargar hoy».

---

## 1. Los premios

| id | NOMBRE EN EL BOLETO | Detalle (texto chico) | Tipo | Stock | Cupo/día | Días en que sale | Franja horaria (PENDIENTE DE CONSTRUIR · pieza B) |
|---|---|---|---|---|---|---|---|
| `hielera` | **HIELERA IGLOO** \* | Premio mayor \* | mayor | **2** | **1** | **jue 24 y vie 25** | **19:00–23:00** (tu dictado: «a partir de las 7pm»); el cierre a las 23:00 lo propongo yo \* |
| `silla` | **SILLA DE PLAYA** \* | Premio grande \* | grande | **10** | **2** | **los 5 días** | 13:00–16:00 y 19:00–22:00, **1 en cada una** \* |
| `bbq` | **SET BBQ** \* | Premio grande \* | grande | **10** | **2** | **los 5 días** | 13:00–16:00 y 19:00–22:00, **1 en cada una** \* |
| `tacos3` | **3 TACOS DE PASTOR** \* | Plato de 3 tacos de pastor \* | chico | **20** | **4** | **los 5 días** | **todo el día** |
| `tacos2` | **2 TACOS DE PASTOR** \* | Plato de 2 tacos de pastor \* | chico | **20** | **4** | **los 5 días** | **todo el día** |
| `cerveza` | **CERVEZA** \* | Una cerveza \* | chico | **50** | **10** | **los 5 días** | **todo el día** |
| `agua` | **AGUA FRESCA** \* | Vaso de 1/2 litro \* | chico | **55** | **11** | **los 5 días** | **todo el día** |
| **Totales** | | | | **167** | **33** al día (**34** el jueves 24 y el viernes 25) | | |

**\*** = propuesta mía, **a confirmar**. Todo lo demás es tu dictado, literal.

### La cuenta cuadra exactamente

Comprobado con calculadora el 2026-09-13: **cupo diario × días = stock, para los
siete premios**, sin sobrar ni faltar una pieza.

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

Como no sobra margen, si un día sale menos de lo previsto **esas piezas se
quedan en la bodega**: el cupo **no** se arrastra al día siguiente. Eso es
importante y lo explico con números en el §2, «Aviso 1».

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

Cada vez que alguien aprieta **JUGAR**, la ruleta hace un sorteo. En ese sorteo
**no participan todos los premios**: participan solo los que en ese momento
están **disponibles**, más el **boleto de consuelo**.

Un premio está disponible cuando cumple **las cuatro condiciones**:

1. **Le queda stock** del evento.
2. **No ha llegado a su cupo del día.**
3. **Estamos dentro de sus días** (la hielera, solo el 24 y el 25).
4. **Estamos dentro de su franja** (PENDIENTE DE CONSTRUIR: hoy esta condición
   no existe).

Imagínate una tómbola. Cada participante mete adentro un puñado de papelitos: a
ese puñado el programa le llama **peso**. Entonces:

> **probabilidad = papelitos de ese premio ÷ papelitos de todos los que están en
> la tómbola en ese momento**

### La regla que propongo: «el peso es el cupo»

Llamemos **N** al número de **jugadas que esperas en un día**. Propongo:

- **Peso de cada premio = su cupo diario** (agua 11, cerveza 10, tacos 4 y 4,
  silla 2, set 2).
- **Peso del consuelo = N − 33** (las jugadas del día menos los 33 premios).

Con esa regla la tómbola tiene **exactamente N papelitos**, y la cuenta se lee
sola: **de cada N jugadas del día salen, en promedio, los cupos de cada premio y
todo lo demás es consuelo.** Si el agua tiene 11 papelitos de 250, salen 11
aguas en 250 jugadas. Así de directo.

**Lo bueno de esta regla:** si mañana decides que N era otro número, **solo
cambia un valor**, el peso del consuelo. Los pesos de los premios no se tocan
nunca, porque son los cupos que tú fijaste.

### Escenarios: qué pasa con N = 150, 250 y 400 jugadas al día

Probabilidad **por jugada**, con la regla de arriba y **sin franjas** (el §3
muestra qué cambia si les ponemos franjas a los grandes):

| Participante | Papelitos (peso) | **N = 150** | **N = 250** | **N = 400** |
|---|---|---|---|---|
| AGUA FRESCA | 11 | 7.33 % | 4.40 % | 2.75 % |
| CERVEZA | 10 | 6.67 % | 4.00 % | 2.50 % |
| 3 TACOS DE PASTOR | 4 | 2.67 % | 1.60 % | 1.00 % |
| 2 TACOS DE PASTOR | 4 | 2.67 % | 1.60 % | 1.00 % |
| SILLA DE PLAYA | 2 | 1.33 % | 0.80 % | 0.50 % |
| SET BBQ | 2 | 1.33 % | 0.80 % | 0.50 % |
| **Boleto de consuelo** | **N − 33** = 117 / 217 / 367 | **78.00 %** | **86.80 %** | **91.75 %** |
| **Total** | N | 100 % | 100 % | 100 % |

| Cuántas jugadas ganan algo | **N = 150** | **N = 250** | **N = 400** |
|---|---|---|---|
| Lunes, martes y miércoles (33 premios) | **22.00 %** | **13.20 %** | **8.25 %** |
| Jueves 24 y viernes 25 (33 + la hielera) | **22.67 %** | **13.60 %** | **8.50 %** |

Léelo así: **con 250 jugadas al día gana más o menos 1 de cada 8 personas.** Con
150 gana 1 de cada 4 y medio; con 400, 1 de cada 12.

La hielera va aparte porque vive dentro de su franja de la noche: sus números
están en el §3.

### Las probabilidades suben solas durante el día

Cuando un premio **se agota o llega a su cupo**, sus papelitos **salen de la
tómbola** y los demás pasan a valer más. Ejemplo con N = 250: mientras están
todos, el agua va al 4.40 %; si ya salieron las 11 aguas del día, esos 11
papelitos desaparecen y **la cerveza sube de 4.00 % a 10 ÷ 239 = 4.18 %**. Por
eso el inventario impreso (`python3 -m ruleta reporte`) muestra la probabilidad
**de ese momento**, no la de la mañana.

### Aviso 1 — el cupo es un **techo**, no una promesa

Esto conviene entenderlo antes de decidir nada. Con la regla «peso = cupo» el
promedio sale clavado… pero **el azar no reparte parejo**: unos días salen más y
otros menos, y **el cupo corta los días buenos, mientras que los días malos no se
recuperan**. Resultado: en promedio se entrega **menos** que el cupo.

Calculado el 2026-09-13 (esta tabla **casi no cambia** con N: da lo mismo para
150, 250 o 400):

| Premio | Cupo del día | Se entregan, en promedio | Porcentaje |
|---|---|---|---|
| AGUA FRESCA | 11 | 9.7 | 88 % |
| CERVEZA | 10 | 8.8 | 88 % |
| 3 TACOS DE PASTOR | 4 | 3.2 | 81 % |
| 2 TACOS DE PASTOR | 4 | 3.2 | 81 % |
| SILLA DE PLAYA | 2 | 1.5 | 73 % |
| SET BBQ | 2 | 1.5 | 73 % |
| **Total del día** | **33** | **27.9** | **84 %** |

En los 5 días: **unas 139 piezas de las 165** (sin contar la hielera).
**Sobrarían unas 26.**

**Si quieres que se entregue casi todo**, hay un remedio de una sola línea:
multiplicar **todos** los pesos por un **factor de holgura**. Calculado para
N = 250:

| Factor | Se entrega del cupo | Costo |
|---|---|---|
| **1.0** (la regla simple) | 84 % | ninguno; es lo más parejo a lo largo del día |
| 1.25 | 92 % | los premios se acaban un poco antes de cerrar |
| 1.5 | 96 % | varios días los chicos se agotan a media tarde |
| 2.0 | 98 % | casi todos los días los chicos se agotan temprano |

**Mi propuesta por omisión: factor 1.0** (la regla simple). Que sobren unas
cuantas piezas sale más barato que quedarte sin nada que dar en la última hora.
Es tu decisión: pregunta 7 del §4.

### Aviso 2 — cuánto vale N y qué pasa si le atino mal

**N es la decisión pendiente más importante de este documento.** Es tu número, no
el mío: **¿cuántas veces se va a apretar el botón en un día del evento?**

Para estimarlo: cuenta los clientes de un viernes normal y calcula cuántos
jugarían. Ya arrancado el evento, el reporte impreso te lo dice medido
(renglón `Boletos emitidos hoy`, con `python3 -m ruleta reporte`).

**La buena noticia: equivocarse no rompe nada.**

- Si vienen **más** jugadas que N, los premios llegan a su cupo **más temprano** y
  el resto de la noche es puro consuelo. No se regala de más: **el cupo manda.**
- Si vienen **menos** jugadas que N, salen **menos** premios de los previstos y
  quedan piezas en la bodega.

**Cómo cambiar N:** en el §5.2, en el bloque de PENDIENTE A, pon como `"peso"` del
consuelo el resultado de **N − 33**. Nada más. (150 → 117 · 200 → 167 · 250 → 217
· 300 → 267 · 400 → 367.)

**Mi propuesta por omisión: N = 250.**

---

## 3. Franjas horarias (PENDIENTE DE CONSTRUIR · pieza B)

Una **franja** es una ventana de horas en la que un premio puede salir, con su
**propio cupo**. Fuera de su franja el premio simplemente **no está en la
tómbola**.

| Premio | Franja | Cupo en esa franja | Días | Peso dentro de la franja | Origen |
|---|---|---|---|---|---|
| HIELERA IGLOO | **19:00 – 23:00** | 1 | **jue 24** y **vie 25** | **9** \* | la hora es tu dictado; el cierre y el peso los propongo yo |
| SILLA DE PLAYA | 13:00 – 16:00 \* | 1 | los 5 días | **12** \* | propuesta mía |
| SILLA DE PLAYA | 19:00 – 22:00 \* | 1 | los 5 días | **12** \* | propuesta mía |
| SET BBQ | 13:00 – 16:00 \* | 1 | los 5 días | **12** \* | propuesta mía |
| SET BBQ | 19:00 – 22:00 \* | 1 | los 5 días | **12** \* | propuesta mía |

La idea: **una comida y una cena**. De 13:00 a 16:00 cae la comida fuerte, y de
19:00 a 22:00 la cena, que es cuando más lleno está. Así los cuatro premios
grandes del día no se amontonan en la misma hora, y el que llega temprano
también tiene con qué ganar.

### Por qué el peso de un premio con franja es 12 y no 2

Porque **compite en muchas menos jugadas**. Con N = 250 en un día de 11 horas
salen unas **23 jugadas por hora**; una franja de 3 horas se lleva solo unas
**68 jugadas** de las 250, no las 250.

**Un supuesto que conviene decir en voz alta:** esa cuenta reparte las jugadas
**parejo** entre las 11 horas del día. Si en el asadero la gente juega sobre
todo de noche, las franjas de la noche se llevarán **más** jugadas de las que
supongo y sus premios saldrán más fácil; las de la comida, al revés. Con un solo
día real ya se puede corregir: la bitácora `datos/boletos.csv` guarda la **hora
exacta** de cada boleto, así que basta contar cuántos cayeron en cada franja y
ajustar el peso.

Medido el 2026-09-13, dentro de una franja de 3 horas y con N = 250:

| Peso de la silla en su franja | Sillas que salen, en promedio | Días de cada 100 en que **sí** aparece |
|---|---|---|
| 2 (el cupo, sin ajustar) | 0.5 | 42 |
| 3.7 (ajustado «a la buena»: 11 h ÷ 3 h) | 1.0 | **63** |
| **12** (mi propuesta) | 3.0 | **95** |

La segunda fila es la trampa: aunque el promedio dé **exactamente 1**, el premio
**solo aparecería 63 de cada 100 días**, porque el cupo de 1 corta los días en
que salían dos y nadie repone los días en que no salió ninguno. Con **peso 12**
la silla aparece **95 de cada 100 días**: unas **9.5 sillas de las 10** a lo
largo del evento, en vez de 6.3.

Y el 12 **casi no depende de N**: comprobado, con 150 / 250 / 400 jugadas al día
da 95 % / 95 % / 96 %.

### La hielera

Mismo razonamiento, con una franja de 4 horas y sin competencia de otro premio
mayor: **peso 9**.

| | N = 150 | N = 250 | N = 400 |
|---|---|---|---|
| Jugadas dentro de 19:00–23:00 | ~55 | ~91 | ~145 |
| Probabilidad de la hielera por jugada, en esa franja | 5.03 % | **3.23 %** | 2.10 % |
| Que salga la hielera **ese** día | 94 % | **95 %** | 95 % |
| **Que salgan las dos** (jueves y viernes) | 88 % | **90 %** | 91 % |

Si quieres estar **seguro** de entregar las dos hieleras, la salida no es
matemática sino de operación: si el viernes a las 22:30 no ha salido, que el
gerente juegue él mismo, o que se entregue a mano. Con puro azar, 90 % es lo que
hay. (Subirle más el peso hace que salga casi siempre en los primeros minutos de
las 7, que es peor: nadie la ve salir.)

### Nota de las 22:00 a las 23:00

Las franjas propuestas no terminan a la misma hora: la de los grandes cierra a
las **22:00** y la de la hielera a las **23:00**. Entre 22:00 y 23:00 del jueves
y el viernes, en la tómbola quedan los chicos, el consuelo y la hielera. No es un
problema; solo que en esa última hora la hielera tiene un poco más de
probabilidad (3.53 % en vez de 3.23 %). Si prefieres que todo cierre a la misma
hora, dilo en la pregunta 2.

### ¿Y los premios chicos, también por franjas?

**Mi propuesta por omisión: NO.** Los chicos se reparten solos, porque el cupo se
va gastando: cuando salieron las 11 aguas ya no hay más aguas ese día, sin
necesidad de horarios. Es lo más simple de operar y de explicarle al personal.

La alternativa, si te preocupa que a las 8 de la noche ya no quede nada chico que
dar:

| Opción | Cómo queda | Pega |
|---|---|---|
| **(a) Cupo diario sin franjas** *(propuesta)* | agua 11, cerveza 10, tacos 4 y 4, a cualquier hora | en un día muy movido los chicos pueden acabarse antes de la cena |
| **(b) Cupo partido en dos mitades** | 12:00–17:30 y 17:30–23:00, la mitad del cupo en cada una (agua 6 y 5; cerveza 5 y 5; tacos 2 y 2) | los cupos impares no parten parejo, y lo que no salió en la primera mitad **se pierde**: se entregaría todavía menos que el 84 % del Aviso 1 |

---

## 4. Preguntas abiertas

Marca la casilla `[x]` de lo que decidas, o escribe tu respuesta al lado. **Si no
respondes una, se aplica la propuesta por omisión**, que está en negritas.

- [ ] **1. ¿Cuántas jugadas esperas por día (N)?**
  Escribe el número: **N = ..........**
  *Por omisión: **250**.* Es lo único que falta para fijar la probabilidad del
  consuelo (§2, «Aviso 2»).

- [ ] **2. Franjas de la SILLA DE PLAYA y el SET BBQ.**
  *Por omisión: **13:00–16:00 y 19:00–22:00, una pieza en cada franja**.*
  Si prefieres otras horas, escríbelas aquí: ..............................
  ¿Cierro también la de los grandes a las 23:00, para que todo termine junto?
  `sí` / `no`

- [ ] **3. Confirmar la HIELERA: 19:00–23:00 los días 24 y 25, una por día.**
  Tu dictado dice «a partir de las 7pm»; **entendí que corre hasta el cierre
  (23:00)**. ¿Es así? `sí` / `no, hasta las .....`

- [ ] **4. ¿Los premios chicos van por franjas?**
  *Por omisión: **no**; cupo diario y a cualquier hora (opción (a) del §3).*

- [ ] **5. Fuera del horario del evento** (antes de las 12:00 o después de las
  23:00), si alguien aprieta JUGAR con el mesero habilitando:
  *Por omisión: **no se imprime nada** y el LED avisa (no se gasta papel ni
  folio).* Alternativa: **imprimir boleto de consuelo**, para que el cliente se
  lleve algo. `no imprimir` / `consuelo`

- [ ] **6. Nombres y detalles exactos** (los siete de la tabla del §1, todos
  marcados **\***).
  *Por omisión: los que están escritos ahí.* Corrige directamente sobre la tabla
  del §1 el que no te guste.

- [ ] **7. (extra) Factor de holgura** del §2, «Aviso 1».
  *Por omisión: **1.0**, la regla simple (se entrega ~84 % del cupo y sobran unas
  26 piezas).* Si quieres que se entregue casi todo: `1.25` / `1.5` / `2.0`

---

## 5. Cómo se traduce a `config.json`

### 5.1 Lo que YA se puede cargar hoy

Estos campos existen en el programa y funcionan. Es el bloque `"premios"`
completo, con la propuesta para **N = 250** (peso = cupo diario). **Comprobado el
2026-09-13: este bloque carga sin un solo error** en el validador del programa
(`ruleta/config.py`).

```json
"premios": [
  { "id": "hielera", "nombre": "HIELERA IGLOO",     "detalle": "Premio mayor",               "stock": 2,  "tope_diario": 1,  "peso": 1,  "desde": "2026-09-24", "hasta": "2026-09-25" },
  { "id": "silla",   "nombre": "SILLA DE PLAYA",    "detalle": "Premio grande",              "stock": 10, "tope_diario": 2,  "peso": 2,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "bbq",     "nombre": "SET BBQ",           "detalle": "Premio grande",              "stock": 10, "tope_diario": 2,  "peso": 2,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "tacos3",  "nombre": "3 TACOS DE PASTOR", "detalle": "Plato de 3 tacos de pastor", "stock": 20, "tope_diario": 4,  "peso": 4,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "tacos2",  "nombre": "2 TACOS DE PASTOR", "detalle": "Plato de 2 tacos de pastor", "stock": 20, "tope_diario": 4,  "peso": 4,  "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "cerveza", "nombre": "CERVEZA",           "detalle": "Una cerveza",                "stock": 50, "tope_diario": 10, "peso": 10, "desde": "2026-09-21", "hasta": "2026-09-25" },
  { "id": "agua",    "nombre": "AGUA FRESCA",       "detalle": "Vaso de 1/2 litro",          "stock": 55, "tope_diario": 11, "peso": 11, "desde": "2026-09-21", "hasta": "2026-09-25" }
]
```

Qué significa cada campo:

| Campo | Qué hace |
|---|---|
| `id` | nombre corto interno; sale en el reporte de inventario y en la bitácora `boletos.csv`. Nunca lo ve el cliente |
| `nombre` | **lo que se imprime grande y en mayúsculas** en el boleto |
| `detalle` | el texto chico debajo del nombre |
| `stock` | piezas para **todo el evento** |
| `tope_diario` | máximo por **día operativo** |
| `peso` | los papelitos en la tómbola (§2) |
| `desde` / `hasta` | primer y último día en que puede salir, **los dos incluidos** |

**Sobre el «día operativo»:** el programa cambia de día a las **6 de la mañana**
(`juego.hora_inicio_dia`). Como el evento corre de 12:00 a 23:00, **el día
operativo siempre coincide con el día del calendario**; nada se pasa a la
madrugada siguiente. Comprobado.

**Sobre el reloj:** las franjas dependen de la hora de la Pi, y en producción la
Pi **va sin red**. Por eso **la batería del reloj (RTC) tiene que estar puesta y
la hora correcta antes del lunes 21**. Si el reloj se atrasa, la hielera puede
salir a la hora equivocada.

### 5.2 Lo que hay que CONSTRUIR

Los tres bloques de abajo **no existen todavía**. Esta es la forma que propongo;
la decide la fase que los programe.

**PENDIENTE A · Peso propio del boleto de consuelo** (dentro de `"juego"`):

```json
"consuelo": { "titulo": "SIGUE PARTICIPANDO", "texto": "¡Gracias por jugar!", "peso": 217 }
```

`217` es **N − 33** con N = 250. `titulo` y `texto` ya existen y ya están así en
`config.json` (decisión tuya del 2026-09-13); **lo nuevo es `peso`**.

> **Lo más importante de este documento.** Mientras el `peso` del consuelo **no
> exista**, el programa reparte **premio en cada jugada** mientras haya stock:
> **las primeras 33 jugadas del día ganan seguidas** (34 el jueves y el viernes)
> y solo después empieza el consuelo. Medido el 2026-09-13. Por eso **no se debe
> abrir el evento sin la pieza A**.

**PENDIENTE B · Franjas por premio, con cupo por franja** (dentro de cada premio):

```json
{ "id": "hielera", "stock": 2, "tope_diario": 1, "peso": 1,
  "franjas": [ { "desde_hora": "19:00", "hasta_hora": "23:00", "tope": 1, "peso": 9 } ] },

{ "id": "silla", "stock": 10, "tope_diario": 2, "peso": 2,
  "franjas": [ { "desde_hora": "13:00", "hasta_hora": "16:00", "tope": 1, "peso": 12 },
               { "desde_hora": "19:00", "hasta_hora": "22:00", "tope": 1, "peso": 12 } ] }
```

Reglas que propongo para ese campo:

- Un premio **con** `franjas` **no está disponible fuera de ellas**.
- Dentro de una franja manda el `peso` de la franja; si la franja no trae `peso`,
  se usa el del premio.
- `tope` es el máximo **de esa franja, ese día**; además siguen mandando el
  `tope_diario` del premio y su `stock`.
- Un premio **sin** `franjas` se comporta como hoy: todo el día. (Así los cuatro
  premios chicos no cambian en nada.)

**PENDIENTE C · Horario del evento** (dentro de `"juego"`):

```json
"horario": { "abre": "12:00", "cierra": "23:00", "fuera_de_horario": "no_jugar" }
```

`fuera_de_horario` sería `"no_jugar"` (no imprime, el LED avisa) o `"consuelo"`
(imprime boleto de consuelo). Es la pregunta 5 del §4.

---

## 6. Cómo se modifica este documento y qué pasa después

1. **Edita este archivo** (`docs/evento-2026-09-asadero-33.md`): cambia lo que
   quieras de la tabla del §1, marca las casillas del §4 y anota tu cambio en la
   bitácora del §7. **No toques `config.json`**: si los dos archivos dicen cosas
   distintas, gana este documento y el otro se rehace.
2. **Avísame** («ya edité el documento del evento»).
3. **Yo lo convierto** en `config.json` con la cadena de trabajo de siempre:
   ejecutor, dos revisores en paralelo, escéptico, pruebas automáticas y commit
   con compuertas. Lo que está PENDIENTE DE CONSTRUIR (A, B y C) sale como una
   fase de programación aparte, con su propio plan.
4. **Se despliega a la Pi** (`git pull` y reinicio del servicio) y se verifica en
   vivo contra lo desplegado.
5. **Antes del lunes 21, sin falta**, hay que poner el marcador en cero, o los
   boletos de las pruebas contarán como premios ya entregados:

   ```bash
   sudo systemctl stop ruleta
   python3 -m ruleta reiniciar --si     # folio y contadores a cero; respalda lo anterior
   sudo systemctl start ruleta
   ```

6. **Comprobaciones finales**, ya con la configuración real cargada:

   ```bash
   python3 -m ruleta reporte                 # stock, cupo y probabilidad de cada premio
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
|  |  |  |
