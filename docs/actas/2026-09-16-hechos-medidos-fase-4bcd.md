<!-- Copia INTEGRA y LITERAL del archivo de hechos medidos del orquestador de la
     sesion del 2026-09-15 (noche) y 2026-09-16 para las Fases 4b, 4c y 4d
     (scratchpad efimero: hechos-fase-4bcd.md, 11379 bytes, 128 lineas, sha256
     54a6aa5dfc4633948c4bcd66e90d8aa3edd474a2e601be6fcfaee4ec5148bbb5).
     Copiado el 2026-09-16 al cerrar las tres fases, con el archivo ya completo:
     su ultima seccion es la PRUEBA DEL USUARIO de las ~13:00 y la lista de
     pendientes para el lunes 21.
     No se corrigio ni se anadio nada a su contenido. Los tres planes
     (docs/planes/fase-4b-config-oficial.md, fase-4c-consuelo-peso.md,
     fase-4d-horas.md) y el acta docs/actas/2026-09-16-fase-4bcd.md se escriben
     DESDE aqui y desde el diff real de los commits f810bc4, d01a0ca y 613f875,
     nunca de memoria.
     El arnes de mutaciones que citan las secciones de la Fase 4d
     (scratchpad/mutar.py) y las copias que genero en %TEMP%\mut4d\ viven solo en
     el scratchpad de esa sesion y NO estan en el repositorio: lo que se conserva
     aqui son los conteos y los veredictos que el orquestador anoto. -->

# Hechos medidos · Fases 4b, 4c y 4d · 2026-09-15 noche y 2026-09-16

Archivo de hechos del orquestador, compilado de los informes de los agentes (ejecutor, commit,
verificador de push, deploy y verificador en vivo) de cada cadena y de lo que el usuario dijo.
Las actas se escriben desde aquí. Horas = reloj de la Pi (America/Hermosillo).

## Contexto común
- Repo: main; base de la Fase 4b = 9afdd9c (cierre docs de la Fase 4a). Pi: /home/asadero/ruleta,
  servicio systemd ruleta, impresora USB, botones cableados, sin LED, sin RTC, con internet
  (Wi-Fi SL-Durazo de la casa del usuario durante estos días; 192.168.1.212; NTP yes).
- Decisión del usuario 2026-09-15 noche: «cambiar la Pi al programa oficial que usaremos; haré
  pruebas mañana para hacer algunos cambios y que quede todo listo para el lunes».
- Las tres fases se hicieron con el usuario probando en vivo; cada una escribió su plan antes del
  código y commiteó plan + código en un solo commit (desviación anotada en cada plan).

## Fase 4b · premios reales en config.json (workflow ruleta-fase4b-config-oficial, run wf_2221d496-a34)
- Commit f810bc4d039b97127670b46f9aa6b8371a8db22a (base 9afdd9c; 16 commits). Archivos:
  config.json, tests/test_config.py, docs/planes/fase-4b-config-oficial.md, docs/fichas.md,
  README.md, docs/evento-2026-09-asadero-33.md. Push verificado (HEAD = origin/main, árbol limpio).
- config.json: 7 premios del bloque JSON §5.1 del documento del evento, SIN desde/hasta (D1):
  hielera 2/1/1, silla 10/2/2, bbq 10/2/2, tacos3 20/4/4, tacos2 20/4/4, cerveza 50/10/10,
  agua 55/11/11 (stock/tope_diario/peso); suma stock 167, suma tope 34.
- Golden nuevo TestPremiosOficialesDelEvento: parsea el único bloque ```json con "premios" del
  documento y compara por igualdad contra config.cargar('config.json'). Suite 214 → 216 OK.
  Mutaciones: 7/7 en rojo (M6 y M7 mutan el DOCUMENTO: demuestran que el golden deriva).
- Lentes: ronda 1 = 9 correcciones, ronda 2 = 2; escéptico 2 correcciones (sobreafirmaciones en
  el doc del evento y README sobre «no se pueden desincronizar»).
- Fichas F-259 (fechas desde/hasta pendientes antes del lunes), F-260 (nombres a confirmar),
  F-261 (pieza A bloquea el evento), F-262 (reiniciar inventario el lunes si el 16 se juega).
- Deploy en la Pi (2026-09-16 00:10–00:11): pull 2a0aba3 → f810bc4 (17 archivos), 216 OK en la Pi,
  stop, `python3 -m ruleta reiniciar --si` → «Folio actual: 00016. Premios entregados registrados: 0.
  Respaldo: datos/estado_20260916_001053.json / datos/boletos_20260916_001053.csv. Inventario
  reiniciado. Folio en 00000.» (OJO: reiniciar respalda estado.json y boletos.csv, NO ruleta.log;
  boletos.csv se mueve y se recrea con el primer boleto). start 00:11:02 → active, NRestarts=0,
  journal «Ruleta arrancando. Premios: hielera, silla, bbq, tacos3, tacos2, cerveza, agua»,
  «Inventario impreso (arranque). Folio actual 00000», 0 avisos de poco papel. Verificado en vivo.

## Fase 4c · consuelo con peso propio, pieza A (workflow ruleta-fase4c-consuelo-peso, run wf_9e938066-987)
- Motivo: 2026-09-16 por la mañana el usuario, probando, reportó «no ha salido ningún boleto de
  gracias por participar, solo han salido premios» (comportamiento previo: consuelo solo sin premio
  disponible; las primeras 34 jugadas del día ganaban seguidas).
- Commit d01a0ca61a531f90b70a20fb6042db8e295a6d38 (base f810bc4; 17 commits). Archivos: README,
  config.json, doc del evento, fichas, docs/planes/fase-4c-consuelo-peso.md, ruleta/__main__.py,
  ruleta/app.py, ruleta/config.py, ruleta/inventario.py, ruleta/ticket.py, tests/test_app.py,
  test_config.py, test_instalacion.py, test_inventario.py, test_ticket.py. Push verificado.
- Diseño: juego.consuelo.peso (int ≥ 0, default 0 = como antes); config.json 217 (= N − 33 con
  N = 250, respuesta por omisión de la pregunta 1 del doc). sortear(): UNA elección ponderada
  premios disponibles + [None] con peso_consuelo; sin premios → None sin sortear. El consuelo no
  descuenta stock ni tope, sí folio. resumen: probabilidad_consuelo; boleto de inventario y reporte
  con la línea «SIGUE PARTICIPANDO (consuelo)  peso 217 -> 86.5%» (48 columnas justas).
  Cableado en abrir_inventario() de __main__.py (único constructor de Inventario en producción;
  app.py no construye Inventario; ficha F-265). app.py: el warning «Sin premios disponibles» se
  partió en info (cayó en consuelo) / warning (de verdad no queda premio).
- Goldens: RngEspia captura choices (población y pesos por igualdad), config (tipos, rango,
  ausente = 0), derivado del bloque §5.2 A del doc y de la fila «Boleto de consuelo» de la tabla
  del §2 (obliga al doc a ser consistente consigo mismo), ticket (48 y 32 columnas), app.
  Suite 216 → 232 OK. Mutaciones 12/12 en rojo. Simulación: con peso 217, 250 jugadas → 32 premios
  repartidos (antes 34 seguidos).
- Lentes: 6 + 5 correcciones, 3 sin converger aplicadas por orden del orquestador; escéptico 1.
- Deploy 2026-09-16 10:47:25: pull → d01a0ca, 232 OK en la Pi, restart, active NRestarts=0,
  «Inventario impreso (arranque). Folio actual 00005» (el usuario había jugado 5 veces esa mañana
  tras el reinicio de las 00:11: agua 3, bbq 1, cerveza 1). 0 ERROR/WARNING. Verificado en vivo.
  El agente de deploy señaló que CLAUDE.md y F-243 decían «folio 16»: desactualizados.

## Fase 4d · reparto por horas, franjas, horario, espera de hora, descripciones (workflow ruleta-fase4d-horas, run wf_5b3b93b5-7a9)
- Decisiones del usuario 2026-09-16 (confirmadas «así va, apúntalo y lanza la cadena»): N es
  imposible de saber → reparto por horas; evento 12:00–23:00; tabla de 7 premios confirmada con
  descripciones nuevas: CERVEZA «Tecate Light, Tecate Roja o Indio», AGUA FRESCA «Horchata, Jamaica
  o Cebada»; tacos son dos premios; hielera 19:00–23:00 jue 24 y vie 25; silla y BBQ una pieza
  13:00–16:00 y otra 19:00–22:00; tacos, cerveza y agua parejo en las 11 horas; una pieza liberada
  no la gana forzosamente la primera jugada; no se acumulan por adelantado; fuera de horario →
  consuelo; «todos los demás deben ser de gracias por participar».
- Commit 613f87552afefe5daaf5c1aa20bf5bbf1e811af3 (base d01a0ca; 18 commits). Archivos: README,
  config.json, doc del evento, fichas, docs/planes/fase-4d-horas.md, ruleta/__main__.py, app.py,
  config.py, inventario.py, ticket.py, tests/test_app.py, test_config.py, test_instalacion.py,
  test_inventario.py, test_ticket.py. hardware.py permitido pero no tocado (F-272). Push verificado.
- Diseño desplegado (config.json medido en la Pi): juego.horario {abre 12:00, cierra 23:00 (cierre
  exclusivo), fuera_de_horario consuelo}; separacion_min_entre_premios 3; espera_hora_seg 120;
  consuelo.peso 10; franjas: hielera [19:00–23:00 tope 1], silla y bbq [13:00–16:00 tope 1,
  19:00–22:00 tope 1]; sin desde/hasta todavía (F-259). Reparto: instantes_de_liberacion(inicio,
  fin, cupo) por puntos medios (k − 0.5); franja de tope 1 se abre al inicio; disponible =
  liberadas − entregadas_hoy > 0 además de stock/tope/fechas/horario/franja; lo liberado y no
  ganado no se pierde ni adelanta. Separación: sortear devuelve None sin sortear si el último
  boleto CON premio impreso fue hace < 3 min; instante persistido en estado.json «ultimo_premio»
  (ausente = sin restricción; reloj hacia atrás no bloquea). Espera de hora: comprobador inyectable
  (/run/systemd/timesync/synchronized o timedatectl), cada 2 s hasta 120 s; si falla, WARNING y
  línea «HORA SIN CONFIRMAR: revisar fecha» en el boleto de arranque; nada bloquea jugadas después.
  Inventario impreso/reporte: por premio «hoy X - liberadas Y - sig HH:MM» (o «sin mas hoy»).
- Tabla de liberaciones calculada por el programa (12:00–23:00): hielera 19:00; silla y bbq 13:00 y
  19:00; tacos3 y tacos2 13:22, 16:07, 18:52, 21:37 (13:22:30 …); cerveza 12:33, 13:39, 14:45,
  15:51, 16:57, 18:03, 19:09, 20:15, 21:21, 22:27; agua 12:30, 13:30, …, 22:30.
  Simulación de un jueves completo (30 corridas): una jugada cada 20 s → 34/34 premios; cada 60 s →
  34/34; cada 180 s → 34/34; cada 600 s → 31.7 de 34.
- Doc del evento: §1 sin asteriscos y descripciones nuevas; §2 reescrito (reparto por horas, nota
  histórica del modelo N); §3 franjas decididas; §4 preguntas 1–6 respondidas (7 queda); §5.1 bloques
  premios (con franjas) y juego; §5.2 A/B/C/D construidas; bitácora §7.
- Goldens: instantes por igualdad de listas HH:MM; liberadas/disponibles a horas concretas;
  franjas (dentro/fuera con motivos); fuera de horario (consuelo y no_jugar); separación; persistencia
  de ultimo_premio y carga de estados viejos; config (10 mensajes de horario, 9 de franjas);
  derivados del doc (premios con franjas, bloque juego, coherencia §5.1/§5.2, probabilidades del §2
  calculadas por el programa); espera de hora (no/no/sí; tope; comprobador que falla); inventario
  impreso del config real. Suite 232 → 268 OK. Mutaciones 14/14 en rojo.
- Lentes: 7 + 3 correcciones, 2 sin converger aplicadas por orden del orquestador; escéptico 2
  (comentario y mensaje de error de config.py que decían que «tope» es «el máximo de esa franja ese
  día», falso con la lectura elegida).
- Decisiones del ejecutor ACEPTADAS por el orquestador: (F-267) sin juego.horario el reparto se hace
  sobre el día operativo completo (cambia la conducta de tope_diario en instalaciones sin horario);
  (F-269) el tope de franja NO se persiste por franja: una pieza de franja no ganada sigue disponible
  (a las 19:00 puede haber 2 sillas); (D4) la separación la marca solo un boleto impreso con premio.
- Deploy 2026-09-16 12:42:46: date «Wed 16 Sep 12:42:39 MST 2026», NTPSynchronized=yes; pull →
  613f875; 268 OK en la Pi; restart --no-block; active, NRestarts=0, PID 3560; journal: «Premios:
  hielera, silla, bbq, tacos3, tacos2, cerveza, agua», «Inventario impreso (arranque). Folio actual
  00005», «Lista. Esperando jugadas.»; 0 ERROR. Sin línea de hora en el journal cuando todo va bien
  (solo se registra el fallo). Verificado en vivo (hora_pi 12:45:11, NTP yes).
- Reinicio del inventario para probar limpio (agente, 12:46): antes folio 6, entregados agua 3,
  bbq 1, cerveza 1 (+1 consuelo 00006 a las 12:46:12 con el proceso viejo); stop; reiniciar --si →
  respaldos datos/estado_20260916_124629.json y datos/boletos_20260916_124629.csv, «Folio en
  00000»; start 12:46:48 → active NRestarts=0, «Inventario impreso (arranque). Folio actual 00000»,
  0 ERROR/WARNING en el proceso nuevo.
- PRUEBA DEL USUARIO (~13:00, después del reinicio): «ya probé, salieron consuelos y una cerveza,
  funciona bien». (Con el reparto: agua liberada 12:30, cerveza 12:33; separación 3 min.)

## Pendientes que dejan estas fases (para el lunes 21)
1. Cargar desde/hasta (hielera 2026-09-24..25; resto 2026-09-21..25) y ajustar el golden que ancla
   «todavía no traen fechas» (F-259). 2. Reiniciar el inventario antes de abrir el lunes (F-262).
3. Perfil Wi-Fi del asadero en la Pi (el usuario teclea la contraseña; el perfil viejo desapareció).
4. Soldar/asegurar el pulsador HABILITAR (F-239). 5. Señal perceptible sin LED (F-256, decisión).
6. CLAUDE.md «Contexto del producto»: inventario ya no en folio 16; modelo de reparto por horas.
