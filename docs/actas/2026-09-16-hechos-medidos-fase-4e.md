<!-- COPIA LITERAL. No se edita: si hay que corregir algo, se corrige en el acta
     de la fase o en una ficha, nunca aqui. -->

# Hechos medidos de la Fase 4e (copia literal del archivo de hechos de la sesion)

Este archivo es la **copia literal** del archivo de hechos que el orquestador fue
escribiendo durante la sesion del **2026-09-16**, tal cual estaba al empezar la
Fase 4e. Se guarda en el repositorio porque de el salen las actas y porque tres
documentos lo citan como evidencia: `README.md` (§7), el §5.1 del documento del
evento y el plan `docs/planes/fase-4e-final.md`.

| Dato del original | Valor |
|---|---|
| Ruta en la sesion | `scratchpad/hechos-fase-4e.md` |
| Tamano | **3140 bytes** |
| `sha256` | `6a0254b53b029a5f2d47157c8860f1fedb30a78e87f1d8e2d094fd347e5f7f15` |
| Copiado el | **2026-09-16** (Fase 4e, paso 6 del plan) |

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
