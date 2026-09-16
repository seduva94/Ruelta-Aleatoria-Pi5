<!-- COPIA LITERAL. No se edita: si hay que corregir algo, se corrige en el acta
     de la fase o en una ficha, nunca aqui. -->

# Hechos medidos de la Fase 4e (copia literal del archivo de hechos de la sesion)

Este archivo es la **copia literal** del archivo de hechos que el orquestador fue
escribiendo durante la sesion del **2026-09-16**. Se guarda en el repositorio
porque de el salen las actas y porque cuatro documentos lo citan como evidencia:
`README.md` (§7), el §5.1 del documento del evento, el plan
`docs/planes/fase-4e-final.md` y el acta `docs/actas/2026-09-16-fase-4e.md`.

**Vuelto a copiar en el cierre documental de la Fase 4e (2026-09-16).** La copia
anterior se hizo cuando el ejecutor termino su pasada, y el archivo **siguio
creciendo despues**: le entraron la cadena de la fase, el **deploy de las 14:44**
con el reinicio del inventario, la verificacion en vivo y el **estado final del
kiosco**. Por eso el tamano y el `sha256` de la tabla **no son los de la copia
anterior**, y por eso esta copia es mas larga: **no se perdio ni se reescribio
nada de lo que ya estaba**.

| Dato del original | Valor |
|---|---|
| Ruta en la sesion | `scratchpad/hechos-fase-4e.md` |
| Tamano | **7202 bytes** |
| `sha256` | `45a473936a39bea00cf9200eb221576c4eb94f4efcbd0187309e6788b71a63dd` |
| Copiado el | **2026-09-16** (cierre documental de la Fase 4e) |
| Copia anterior | **3140 bytes**, `sha256` `6a0254b53b029a5f2d47157c8860f1fedb30a78e87f1d8e2d094fd347e5f7f15` (commit `70bcaa6`, paso 6 del plan) |

---

# Hechos medidos · Fase 4e (pasada final antes del evento) · desde 2026-09-16

Archivo de hechos del orquestador. Las actas se escriben desde aquí. Horas = reloj de la Pi.

## Requisito del usuario (2026-09-16 ~12:50)
«Asegurar que la hora de la Pi se actualice cada vez que encienda; el orden sería: Pi enciende >
conexión a internet > actualizar hora y fecha actual > imprimir inventario > listo para jugar».

## Medición 1 · reinicio caliente (`systemctl reboot`, 12:53:27, commit 613f875)
- Servicio arrancado a los 5.94 s (ANTES de la red); wlan0 conectada a SL-Durazo a los 8.90 s;
  IP 192.168.1.212 a los 11.09 s; NTP «Initial clock synchronization» a los 34.18 s (servidor
  IPv6 de 2.debian.pool.ntp.org); «Inventario impreso (arranque). Folio actual 00005» a los 34.54 s
  (0.37 s después de la sincronización); «Lista. Esperando jugadas.» a los 34.55 s. Espera interna
  de la pieza D: 28.3 s de 120. Sin WARNING «HORA SIN CONFIRMAR». NRestarts=0. Folio 5 antes y
  después. Caveat: en un reboot caliente el RTC interno de la Pi 5 conserva la hora (el kernel
  restauró 2026-09-16T19:53:37 UTC), así que NO ejercita el caso «la Pi cree que es otro día».

## Medición 2 · ARRANQUE EN FRÍO (el usuario desenchufó unos minutos y enchufó, ~13:03)
- `rpi-rtc … setting system clock to 1970-01-01T00:00:09 UTC` (3.06 s): sin batería, el RTC arranca
  en cero. fake-hwclock NO está instalado; quien restaura la hora vieja es systemd:
  «System time advanced to timestamp on /var/lib/systemd/timesync/clock: Wed 2026-09-16 12:58:58 MST»
  (3.08 s). El journal de este arranque empieza a las 12:59:00 con hora VIEJA (real ≈ 13:03:53).
- Línea de tiempo monotónica: 6.25 s Started ruleta.service; 6.61 s «Ruleta arrancando…»
  (fechada 12:59:03, hora vieja); 9.15 s wlan0 conectada; 9.32 s IP; 9.36 s activated;
  34.28 s «Contacted time server [2605:e440:5::367]:123» + «Initial clock synchronization to
  Wed 2026-09-16 13:04:24.450935 MST» (salto hacia adelante ≈ 4 min 54 s); 34.88 s «Inventario
  impreso (arranque). Folio actual 00005» fechado 2026-09-16 13:04:25 (hora ya correcta);
  34.88 s «Lista. Esperando jugadas.». Espera real del programa 28.3 s (de 120). Sin
  «HORA SIN CONFIRMAR», 0 WARNING/ERROR de ruleta, NRestarts=0, timedatectl synchronized yes.
- estado.json intacto (actualizado 12:49:03): el inventario de arranque no consume folio.
- VEREDICTO: el orden Pi → internet → hora → inventario → listo se cumple en arranque en frío
  real sin RTC. Riesgo de F-241 cerrado en hardware.
- Observaciones: (1) el programa no registra nada mientras espera (28 s de silencio que en el
  journal aparentan 5 min por el salto de reloj) → candidato: log.info cada ~10 s «Esperando la
  hora…»; (2) ActiveEnterTimestamp de systemd queda fosilizado con la hora vieja (12:59:03 vs
  uptime -s 13:03:50); (3) NTP por IPv6: en la red del asadero puede tardar distinto → subir
  espera_hora_seg a 300 en la pasada final; (4) la marca de /var/lib/systemd/timesync/clock se
  actualiza cada ~1 min con sync; en apagón duro puede quedar hasta un minuto atrás.

## Cadena de la Fase 4e (2026-09-16 ~14:00–14:50, workflow ruleta-fase4e-final, run wf_c854f163-eb9)
- Decisión del usuario (~14:00): «listo, ya terminé las pruebas, reinicia el inventario para que
  quede listo». El día anterior/mismo día: «tal vez mañana lleve el proyecto al asadero para
  conectarlo al wifi donde estará».
- Commit 70bcaa60e06f97edd48677783c1d64f988d674aa (base da1385e; 20 commits). Archivos:
  ruleta/app.py, config.json, tests/test_app.py, tests/test_config.py, tests/test_instalacion.py,
  docs/planes/fase-4e-final.md, docs/actas/2026-09-16-hechos-medidos-fase-4e.md (copia de la
  versión previa de este archivo, sha256 6a0254b5…, 3140 bytes), docs/fichas.md, README.md,
  docs/evento-2026-09-asadero-33.md, docs/planes/fase-4d-horas.md. Push verificado (HEAD =
  origin/main, árbol limpio). ruleta/config.py permitido pero no tocado (ya validaba fechas).
- Cambios: config.json con desde/hasta (hielera 2026-09-24..25; silla, bbq, tacos3, tacos2,
  cerveza, agua 2026-09-21..25) y espera_hora_seg 120 → 300; app.py: PERIODO_AVISO_HORA = 10.0 y
  tres log.info en esperar_hora_sincronizada («Esperando a que la hora se sincronice (hasta N s)…»,
  «Sigo esperando la hora: llevo N s de N s» cada 10 s, «Hora sincronizada tras X s»); con
  espera_hora_seg = 0 no registra nada. Goldens: 4 de journal por igualdad de listas (test_app),
  fechas por censo e igualdad derivadas del bloque §5.1 del documento (desde/hasta entraron en
  CLAVES_DEL_DOCUMENTO), calendario del evento con el motor real (test_instalacion). Suite 268 →
  273 OK. Mutaciones 10/10 en rojo (M9 muta el DOCUMENTO). `python -m ruleta reporte` el 16:
  los siete «no disponible: desde 21/09» (hielera «desde 24/09»), consuelo 100 %.
- D4: `grep -rni hwclock` en el repo = 0 coincidencias (la premisa fake-hwclock solo vivía en
  mensajes de sesión); se documentó el mecanismo real (systemd, /var/lib/systemd/timesync/clock)
  en README §7, doc §5.1 y plan 4d con nota fechada. README §5: párrafo para el personal (espera
  de 5 min, HORA SIN CONFIRMAR, premios solo del 21 al 25 de 12:00 a 23:00).
- Fichas: F-259 y F-273 cerradas; F-241 con nota «cerrada en hardware» (queda la idea de bloquear
  también las jugadas mientras la hora no esté confirmada); F-262 actualizada (con fechas no hace
  falta reiniciar el lunes salvo para folio en cero); F-275 y F-276 nuevas (Wi-Fi del asadero
  pendiente en sitio; y la que anotó el ejecutor). Lentes 1 corrección; escéptico 1.
- CLAUDE.md quedó desfasado en tres frases (120 s; «las fechas todavía no están cargadas»; «la
  pieza D nunca se ha visto morder»): lo corrige el cierre documental de esta fase.
- Deploy en la Pi (14:44): pull 613f875 → 70bcaa6, git status limpio salvo config.json.bak-2026-09-12,
  273 OK en la Pi; config leído en la Pi: espera 300, fechas como arriba, consuelo.peso 10, horario
  12:00–23:00 consuelo. stop → `reiniciar --si`: «Folio actual: 00010. Premios entregados
  registrados: 2. Respaldo: datos/estado_20260916_144415.json / datos/boletos_20260916_144415.csv.
  Inventario reiniciado. Folio en 00000.» (los 2 entregados borrados eran cerveza 1 y agua 1 de
  las pruebas del usuario; boletos.csv se mueve al respaldo y reaparece con el primer boleto).
  start 14:44:37 → active, NRestarts=0, PID 1527, enabled; journal: «Esperando a que la hora se
  sincronice (hasta 300 s)…», «Hora sincronizada tras 0 s» (Pi encendida 1 h 39 min, ya
  sincronizada), «Inventario impreso (arranque). Folio actual 00000», «Lista. Esperando
  jugadas.»; ERROR/WARNING/HORA SIN CONFIRMAR = 0. Verificado en vivo (HEAD, active, config, folio 0).
- Estado final del kiosco: LISTO PARA EL EVENTO salvo (1) perfil Wi-Fi del asadero (el usuario en
  sitio, tecleando la contraseña; la Pi conoce casa=20 y miltimex=10, que es el hotspot de la
  laptop), (2) prueba de corriente en el asadero (fecha del inventario), (3) soldar/asegurar el
  pulsador HABILITAR (F-239), (4) señal perceptible sin LED (F-256, decisión del usuario).
