<!-- Copia INTEGRA y LITERAL del archivo de hechos medidos del orquestador de la
     sesion del 2026-09-15 (scratchpad efimero: hechos-fase-3.md, 6943 bytes,
     sha256 013b3950607926f979e367ee5e78471a6d106209d59af214b65a024678e6916b).
     No se corrigio ni se anadio nada a su contenido: el acta
     docs/actas/2026-09-15-fase-3.md se escribe DESDE aqui, nunca de memoria.
     El orquestador siguio anadiendo hechos mientras se escribia el cierre: esta
     copia es la del archivo tal como estaba al terminarlo, con la seccion de la
     prueba SIN PAPEL de las 13:29 ya incluida. -->

# Hechos medidos · Fase 3 (botones) · 2026-09-15

Archivo de hechos del orquestador. Las actas se escriben desde aquí, nunca de memoria.
Horas = reloj de la Pi (America/Hermosillo), salvo que se indique.

## Contexto
- Sin plan prescriptivo previo de Fase 3: el usuario pidió cablear en vivo ("Vamos a conectar cables").
  Desviación consciente del §2 del protocolo; el acta debe decirlo. El plan de Fase 3 se
  escribe retroactivamente desde este archivo.
- Diagrama de cableado entregado al usuario: scratchpad `cableado-botones.svg` (generador
  `gen_cableado.py`), verificado por agente Sonnet contra pinout oficial J8, `config.json`
  (gpio 17/27/22, pull_up true) y README §2; una corrección (etiquetas de pin 11 y 13 encimadas).
  Pendiente: incorporarlo al repo (`docs/`).
- Hardware del usuario: JUGAR = botón arcade amarillo con microswitch de cuchillas (dos cables:
  verde/teal y negro, terminales de crimpar). HABILITAR = botón chico metálico de tapa roja,
  2 patitas delgadas, cables azul y negro con terminales de crimpar tipo cuchilla (contacto
  precario: las terminales son para cuchillas anchas). SIN LED conectado (config sigue con
  `"led": 22`; gpiozero no falla sin LED físico).

## Cronología medida
- 11:44:42 Pi arrancó (uptime -s); reloj saltó (journal mostró "Sep 13 17:09" hasta que NTP
  corrigió a las 11:47). Evidencia de que sin red la hora se pierde → batería RTC.
- 11:47:03 servicio ruleta recibió SIGTERM (usuario/agente lo detuvo); is-enabled = enabled.
- 11:56:24 y 12:02:20 monitor `/tmp/monitor-botones.py` (Button 17/27 pull_up, LED 22 blink):
  reposo jugar=False habilitar=False (3 lecturas directas también False/False).
- 12:04:16–12:04:36 y 12:05:42–12:06:02: pulsaciones registradas SOLO en GPIO 17 (pin 11).
  Ninguna en GPIO 27. El usuario dijo haber pulsado HABILITAR 3 veces a ~12:06:00; primera
  hipótesis (HABILITAR en pin 11) resultó FALSA: a las 12:07–12:09 volvió a pulsar y no entró nada.
- 12:11:08 escáner `/tmp/scan-pines.py` (17 GPIO libres como entrada pull-up, ningún pin como
  salida): reposo todos False. 12:14:37 JUGAR → GPIO 17. Tres pulsaciones de HABILITAR: nada.
- Prueba "juntar los dos cables de HABILITAR" (12:20): nada en 17 pines.
- 12:20:55 escáner ampliado a GPIO 2–27 (26 pines). Pruebas cruzadas con el microswitch de JUGAR:
  12:24:56 "GPIO 11 (pin físico 23) presionado", y GPIO 11 quedó en bajo continuo
  (`pinctrl get 11` = lo). Diagnóstico: el cable NEGRO de HABILITAR estaba en el pin 23
  (GPIO 11) en vez del pin 25 (GND), una fila arriba. Coincide con la foto del header.
- 12:28:47 el usuario movió el negro al pin 25. 12:28:55–12:29:17: pulsaciones en GPIO 27
  (pin 13) ✓ y gesto combinado HABILITAR sostenido + JUGAR (GPIO 17) a las 12:29:09, :13, :15.
- 12:29:57 `sudo systemctl start --no-block ruleta` → active, NRestarts=0, "GPIO listo:
  jugar=17 habilitar=27 led=22", inventario de arranque impreso (folio 00000), "Lista".
- 12:30:25 Boleto 00001 TEST 4 impreso; 12:30:32 Boleto 00002 TEST 7; 12:30:38 Boleto 00003
  TEST 6 (tres jugadas reales con botones). Entre ellas "Pulsación ignorada: faltan 2.0 s de
  espera" (cooldown de 5 s funciona). 12:30:42–12:30:47: 9 × "Pulsación ignorada: el botón
  HABILITAR no está presionado" (la compuerta del mesero funciona).
- estado.json: folio 3, entregados test4/test7/test6 = 1, boletos_por_dia 2026-09-15 = 3.
  boletos.csv: 6 líneas (emitido+impreso × 3). → `python3 -m ruleta reiniciar --si` antes del 21.
- Aviso falso "poco papel" sigue apareciendo en cada arranque (diagnóstico cerrado el 13;
  arreglo pendiente de autorización).

## Estado final de la sesión de hardware (12:31)
- Servicio ruleta ACTIVE y enabled, kiosco operable con botones reales.
- Cableado final: JUGAR NO→pin 11 (GPIO 17), COM→pin 9 (GND); HABILITAR señal→pin 13
  (GPIO 27), negro→pin 25 (GND). Sin LED.
- En /tmp de la Pi: monitor-botones.py/.log/.out, scan-pines.py/.log/.out (tmpfs, se borran al reiniciar).
- Red: Pi en "Miltimex 5G", 192.168.50.168; alias `ruleta` resolvió bien todo el día.

## Trampas aprendidas (para el plan retroactivo y fichas)
- `pkill -f "<patrón>"` dentro de un `ssh 'bash -c ...'` cuyo comando contiene el patrón
  literal mata al propio bash y no ejecuta nada más (pasó 3 veces). Usar `[p]ython3` y no
  repetir la ruta literal en el mismo comando (variable `M=...`).
- Un proceso lanzado por ssh en segundo plano deja la sesión colgada hasta el timeout aunque
  se use setsid+nohup+redirecciones; el proceso sobrevive: verificar desde una conexión nueva.
- El monitor inicial ponía GPIO 22 como salida (LED). Con un botón mal cableado en el pin 15
  sería un corto: los escáneres de diagnóstico deben usar SOLO entradas.
- Contacto de las terminales de crimpar sobre patitas delgadas: no fiable; soldar o enrollar.
- El registro del monitor no distingue "qué botón cree el usuario que pulsa": las pruebas
  cruzadas (tocar un cable contra la tierra/señal buena del otro botón) sí.

## Prueba SIN PAPEL (F-091), 2026-09-15 13:29, servicio active, folio previo 8
- El usuario dejó la impresora sin papel y jugó una vez (13:29:17). La impresora encendió el foco
  rojo de error y pita cada segundo sin parar (papel agotado, trabajo retenido en su búfer).
- Journal: "Boleto 00009 emitido: TEST 7" → WARNING "reporta poco papel" (byte rezagado) →
  "Boleto 00009 impreso: TEST 7". NO se detectó "sin papel" ni "fuera de línea": la predicción
  del escéptico del 2026-09-13 se cumplió tal cual (los dos guardias derrotados por el desfase
  de un comando). boletos.csv registra 00009 emitido+impreso; estado.json folio 9; premio TEST 7
  descontado aunque no salió nada. Proceso sano (wchan hrtimer_nanosleep, NRestarts=0): la
  escritura a usblp no bloqueó; la impresora aceptó los bytes en su búfer.
- Consecuencia para producción: sin arreglo, con papel agotado el kiosco "regala" folios y premios
  sin boleto. Arreglo de fondo necesario en Fase 4 (leer la respuesta FRESCA: tras DLE EOT leer
  hasta ~64 bytes / 150 ms y quedarse con el último byte válido, o drenar con tope antes de
  preguntar), además de la máscara estricta ya propuesta.
- Recuperación (13:31–13:33): al reponer el papel la impresora imprimió sola el boleto 00009
  retenido en su búfer (salió cortado; el usuario lo vio con folio 00009). Límites: si se apaga
  la impresora o la Pi antes de reponer papel, el trabajo retenido se pierde aunque el programa
  ya lo dio por impreso; si el papel se acaba a media impresión sale un boleto incompleto.
- 13:33:23 jugada con papel: Boleto 00010 TEST 6 emitido e impreso normal (aviso falso de poco
  papel de nuevo). Servicio active, NRestarts=0. estado.json: folio 10, entregados
  test4=1, test7=4, test6=3, test5=2 (el usuario jugó varias veces por su cuenta entre 12:31 y
  13:18: folios 4–8, todos impresos según boletos.csv/journal).
