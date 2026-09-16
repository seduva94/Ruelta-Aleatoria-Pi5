# Fichas de lo residual

Hallazgos que **no** justifican detener una fase (no son defecto de conducta,
assert que no muerde, golden en rojo ni afirmación de doc falsa), pero que no se
deben olvidar. Una entrada por hallazgo, con fecha y origen. Se cierran cuando
alguien las resuelve, anotando en qué fase y con qué cambio.

---

## F-001 · El README propone `scp -r` y la Fase 1 decidió `git clone`

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · redacción de `docs/planes/fase-1-preparar-pi.md`
- **Dónde:** `README.md` §4, paso 1 (`grep -n "scp -r" README.md`)
- **Qué pasa:** el README dice que el programa se copia a la Pi con
  `scp -r "Ruleta Asadero" usuario@ruleta.local:~/ruleta`, mientras que la
  decisión cerrada 6 de la Fase 1 instala con
  `git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git ~/ruleta`.
  Además el README usa el usuario genérico `usuario` y la Fase 1 fijó `asadero`.
- **Por qué es residual:** el README no está mal escrito ni miente sobre el
  código; describe una alternativa que sigue funcionando. Es una decisión que
  cambió después de escribirlo.
- **Riesgo si no se toca:** alguien sin contexto copia por `scp` desde Windows y
  arrastra finales de línea CRLF, pierde el bit de ejecución de los `.sh` y se
  lleva una carpeta `datos/` de pruebas con folios falsos.
- **Propuesta:** reescribir el paso 1 del §4 como `git clone` y dejar el `scp`
  solo como alternativa para actualizar sin internet. **Requiere visto bueno del
  usuario** (toca documentación que él lee).
- **Estado:** **resuelta** el 2026-09-11 (sub-fase 2b, cambio (g) del brief). El §4 paso 1 del `README.md` instala con `git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git ~/ruleta` y el usuario es `asadero`. Medido: `grep -c "scp -r" README.md` → **0**. El `scp` sobrevive solo para copiar el logo y el `config.json` sueltos, que es su uso legítimo.
---

## F-002 · El README §3 no menciona la autenticación solo por llave

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · redacción del plan
- **Dónde:** `README.md` §3 "Sistema operativo (propuesta)"
  (`grep -n "^## 3. Sistema operativo" -A 12 README.md`)
- **Qué pasa:** el README dice "activa SSH" y `ssh usuario@ruleta.local`. La
  Fase 1 fija: usuario `asadero`, opción **"Allow public-key authentication
  only"** en Imager y alias `ruleta` en `~/.ssh/config`.
- **Por qué es residual:** no contradice al código; es documentación anterior a
  la decisión.
- **Propuesta:** actualizar §3 con el usuario real y la llave, o remitir al plan
  de la Fase 1. **Requiere visto bueno del usuario.**
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (g)). El §3 del `README.md` fija el nombre de equipo `ruleta`, el usuario `asadero`, la opción **«Allow public-key authentication only»** con la llave de la PC, y dice que el SSH y el Wi-Fi son solo para instalar y probar. Medido: `grep -c "usuario@ruleta.local" README.md` → **0**.
---

## F-003 · El README §4 paso 7 apaga NTP; la Fase 1 lo deja encendido

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · redacción del plan
- **Dónde:** `README.md` §4, paso 7 (`grep -n "set-ntp false" README.md`)
- **Qué pasa:** el README propone `sudo timedatectl set-ntp false` y fijar la
  hora a mano. Ese consejo aplica **solo si la Pi no tendrá internet**, cosa que
  el propio README dice, pero en una lectura rápida parece el camino normal.
  La Fase 1, con Wi-Fi, deja NTP **encendido** y sincronizando.
- **Por qué es residual:** el README ya trae la condición; es ambigüedad, no
  error.
- **Propuesta:** resaltar la condición ("solo si no habrá internet") en el paso
  7. Se puede resolver junto con F-001.
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (g)). El §4 paso 7 del `README.md` ya no presenta la hora manual como una rama condicional: dice que en el evento la Pi va **sin red**, que por eso la **batería RTC es necesaria**, y deja anotado que mientras haya internet puede quedarse con `set-ntp true`.
---

## F-004 · `config.json` trae una MAC de impresora inventada

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · lectura de `config.json` y de `cmd_diagnostico`
- **Dónde:** `config.json` → `impresora.mac = "00:00:00:00:00:00"`;
  `ruleta/__main__.py` → `cmd_diagnostico`
- **Qué pasa:** esa MAC tiene formato válido, así que pasa la validación y el
  diagnóstico intenta conectarse de verdad. Consecuencia en la Fase 1 (y en el
  diagnóstico que corre `instalar.sh` al final): dos o tres líneas `[!!]`,
  código de salida 1 y hasta un par de minutos probando canales RFCOMM contra un
  dispositivo que no existe.
- **Por qué es residual:** es el comportamiento correcto del programa con una
  MAC sin configurar, y se resuelve solo en la Fase 2, cuando `emparejar.sh`
  escriba la MAC real.
- **Riesgo si no se toca:** un ejecutor sin contexto lee el código 1 como fallo
  de instalación y "arregla" algo que no está roto. Ya está advertido en el plan
  de la Fase 1, §5 trampa 12 y §7.
- **Propuesta (opcional, para después del evento):** que el diagnóstico detecte
  la MAC de relleno `00:00:00:00:00:00` y diga "impresora sin configurar" en vez
  de intentar conectarse. No tocarlo antes del evento.
- **Estado:** abierta, sin acción en las Fases 1 a 4.

---

## F-005 · La Fase 1 depende de que el repositorio publicado esté al día

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · redacción del plan
- **Dónde:** decisión cerrada 6 (instalación por `git clone`)
- **Qué pasa:** la Pi instala lo que esté **publicado** en
  `https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git`. Si algún commit local
  de la PC no se ha subido, la Pi instalaría una versión vieja o incompleta sin
  avisar de forma obvia.
- **Por qué es residual:** no es un defecto del código ni del plan; es una
  dependencia de proceso.
- **Mitigación ya puesta:** el Paso 8 del plan verifica con `ls ~/ruleta` que el
  clon trae `tests/`, `instalar.sh`, `config.json`, etc., y ordena **detenerse y
  avisar** si faltan archivos.
- **Propuesta:** antes de arrancar la Fase 1, un agente verificador de solo
  lectura confirma que el remoto tiene el mismo `HEAD` que la PC.
- **Estado:** abierta.

---

## F-006 · El material del README no incluye lector de microSD ni Imager

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · redacción del plan
- **Dónde:** `README.md` §1 "Qué necesitas"
- **Qué pasa:** la tabla lista Pi, fuente, microSD, impresora, botones y cables,
  pero no el **lector de microSD para la PC** ni **Raspberry Pi Imager**, que
  son imprescindibles para la Fase 1.
- **Por qué es residual:** el §3 sí menciona Imager; solo falta en la tabla de
  material.
- **Propuesta:** agregar las dos filas al §1. Se puede resolver junto con F-001.
- **Estado:** abierta.

---

## F-007 · `BatchMode=yes` no garantiza tanto como dice el encabezado del plan

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Convención del encabezado: 'Un agente añade siempre -o BatchMode=yes -o ConnectTimeout=10 para que, si algo pidiera una contraseña, el comando falle en vez de quedarse colgado'. BatchMode solo afecta a la autenticación del propio ssh, no a un `sudo` remoto: lo que salva ahí es que sin tty `sudo` falla con 'no tty present'. El efecto práctico es el mismo, pero la frase da una garantía más amplia de la que ofrece la opción.
- **Estado:** abierta.

---

## F-008 · La bitácora §0 no refleja que las llaves SSH ya existen

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Bitácora §0: la casilla del Paso 2 está vacía aunque el par de llaves ya existe en la PC desde el 2026-09-11 15:39. Al arrancar la fase conviene marcarla con esa evidencia en vez de volver a 'generar'. Lo mismo con la fila del Paso 3, cuya evidencia sigue enumerando solo tres valores de `ssh -G`.
- **Estado:** abierta.

---

## F-009 · La llave `id_ruleta` es el único punto de acceso remoto

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Único punto de acceso: si se pierde `~/.ssh/id_ruleta` (falla la PC, se reinstala Windows), con 'Allow public-key authentication only' el único camino de vuelta es consola local con monitor+teclado, o regrabar la microSD. El plan lo explica en la decisión 3 y en el Paso 6 SI FALLA, pero la §3 'Material necesario' dice 'No hace falta monitor ni teclado'. Vale una línea que recomiende tener HDMI+teclado a la mano durante el evento, o una copia de la llave en un lugar seguro.
- **Estado:** abierta.

---

## F-010 · "Un par de minutos" de diagnóstico es una cota superior, no un dato medido

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Estimación de tiempo del diagnóstico ('hasta un par de minutos probando canales RFCOMM'): `buscar_canal` (ruleta/escpos.py) solo sigue al siguiente canal si el error es ECONNREFUSED; con la MAC 00:00:00:00:00:00 el primer error no lo es y se propaga de inmediato, así que en la práctica suele terminar mucho antes. Es una cota superior, no un hecho medido.
- **Estado:** abierta.

---

## F-011 · El `sudo poweroff` del Paso 12 falla si `sudo` pide contraseña

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 12, punto 1: el usuario apaga con `ssh ruleta 'sudo poweroff'`. Si el Paso 7 dio SUDO_PIDE_CONTRASENA ese comando falla por falta de tty; conviene mencionar la alternativa (apagar desde consola local o, con la Pi ya detenida, desconectar la corriente).
- **Estado:** abierta.

---

## F-012 · El `rfkill` del Paso 7 no lleva `LC_ALL=C`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 7 usa `ssh ruleta 'rfkill list bluetooth'` sin `LC_ALL=C`. Ahí todavía no se cambió la locale, así que hoy no rompe nada, pero por consistencia con la regla de §5 trampa 11 podría llevarlo también.
- **Estado:** abierta.

---

## F-013 · La carpeta `docs/` todavía no está versionada en el repositorio

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** `docs/` está sin versionar en el repo (`git status` lo muestra como `?? docs/`), así que el plan, las fichas y las futuras actas aún no están publicados. Es coherente con la ficha F-005 (la Fase 1 depende de que el remoto esté al día) y con que el ejecutor no commitea; solo conviene que el agente de commit lo tenga presente.
- **Estado:** abierta.

---

## F-014 · El Paso 12 no dice qué hacer si `rtc_bbat_vchg` ya estaba puesto

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 12 no dice qué hacer si el `grep -n rtc_bbat_vchg` inicial encuentra la línea ya presente (por ejemplo tras una repetición): con las guardas propuestas el paso simplemente no cambia nada, pero el texto podría decirlo explícitamente.
- **Estado:** abierta.

---

## F-015 · El Paso 9 cita el comando de diagnóstico distinto al de `instalar.sh`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 9, punto 7 de «qué hace el instalador»: dice que corre `python3 -m ruleta diagnostico`, pero `instalar.sh` corre en realidad `sudo -u "${USUARIO}" env PYTHONIOENCODING=utf-8 python3 -m ruleta --config "${DIR}/config.json" diagnostico`. No cambia el resultado, pero el texto exacto no coincide con el script.
- **Estado:** abierta.

---

## F-016 · La estimación de minutos del diagnóstico también está en la ficha F-004

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Estimación de tiempo del diagnóstico: el plan (Paso 9 y notas de la §7) dice «hasta un par de minutos probando canales RFCOMM». En el código, `probar()` falla en como mucho `timeout_seg` (10 s) y `buscar_canal` aborta en el primer error que no sea ECONNREFUSED (`raise ErrorConexion`), así que con la MAC 00:00:00:00:00:00 lo normal son segundos, no minutos. Misma estimación optimista/pesimista en la ficha F-004.
- **Estado:** abierta.

---

## F-017 · La línea `[ok] lgpio` puede salir sin número de versión

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 10, bloque de seis `[ok]`: la línea `[ok] lgpio <versión>` puede salir sin versión, porque el código imprime `getattr(m, '__version__', '')` y el módulo `lgpio` no siempre expone `__version__`. El golden por conteo (`grep -c`) no se ve afectado.
- **Estado:** abierta.

---

## F-018 · El Paso 9 dice "los dos comandos" pero muestra una sola línea

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 9, variante «requiere al usuario»: dice «escribe los dos comandos», pero el bloque QUÉ HACER muestra un solo comando de una línea (`cd ~/ruleta && sudo ./instalar.sh`). Conviene enumerar explícitamente `cd ~/ruleta` y `sudo ./instalar.sh`.
- **Estado:** abierta.

---

## F-019 · El criterio del Paso 12 pide `rtc0/name` sin decir qué valor esperar

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 12, criterio: se pide `cat /sys/class/rtc/rtc0/name` pero no se dice qué valor esperar (en Pi 5 suele ser `rpi_rtc`). Como criterio queda sin golden.
- **Estado:** abierta.

---

## F-020 · La línea RTC se anexa a `config.txt` sin fijar la sección `[all]`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 12: la línea `dtparam=rtc_bbat_vchg=3000000` se anexa al final de `/boot/firmware/config.txt` sin comprobar bajo qué filtro de sección (`[all]`, `[pi5]`, `[cm5]`…) cae. En la imagen por defecto termina en `[all]` y funciona, pero convendría anexar explícitamente bajo `[all]`.
- **Estado:** abierta.

---

## F-021 · El criterio del Paso 3 fija un orden y dos líneas después se desdice

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 3, criterio: dice «Debe imprimir, en este orden: user / hostname / identityfile» y dos líneas después se desdice («el orden puede variar»). Basta con dejar solo la comprobación por valores.
- **Estado:** abierta.

---

## F-022 · La lista esperada de `ls ~/ruleta` del Paso 8 ya no incluye `docs`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 8, criterio: la lista esperada de `ls ~/ruleta` no menciona `docs` (que existe en el repo desde que se agregó este plan). El «al menos» lo cubre, pero la lista ya no es el contenido completo.
- **Estado:** abierta.

---

## F-023 · La §7 corre el diagnóstico dos veces pudiendo guardarlo una sola vez

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §7: `python3 -m ruleta diagnostico` se ejecuta dos veces más (un `grep -c` por golden). Se podría guardar la salida una vez en un archivo del scratchpad y contar sobre ella, ahorrando dos conexiones Bluetooth fallidas.
- **Estado:** abierta.

---

## F-024 · El Paso 14 no dice que hay que crear la carpeta `docs/actas/`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 14: manda escribir `docs/actas/<AAAA-MM-DD>-fase-1-preparar-pi.md`, pero la carpeta `docs/actas/` todavía no existe en el repo; convendría decir explícitamente que hay que crearla (`mkdir -p docs/actas`).
- **Estado:** abierta.

---

## F-025 · El criterio del Paso 12 no vuelve a comprobar `systemctl is-enabled ruleta`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 12 (batería RTC): el bloque deshabilita el servicio (`sudo systemctl disable ruleta`), reinicia y lo vuelve a habilitar, pero el CRITERIO DE ACEPTACIÓN del paso solo comprueba `grep rtc_bbat_vchg` y `cat /sys/class/rtc/rtc0/name`; no vuelve a verificar `systemctl is-enabled ruleta` = `enabled`. Hoy solo lo salva el golden de la §7 al cierre de fase. Convendría añadir esa comprobación al propio paso.
- **Estado:** abierta.

---

## F-026 · Los Pasos 11, 12 y 13 usan `sudo` sin la rama de contraseña escrita al lado

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Pasos 11, 12 y 13 corren `sudo` (timedatectl, cp/tee sobre `config.txt`, reboot, raspi-config/sed/locale-gen) pero solo el Paso 9 trae la rama explícita «requiere al usuario» si el Paso 7 dio `SUDO_PIDE_CONTRASENA`. Se apoyan en la regla general (§2 decisión 8 y §8 prohibición 1); no hay defecto de conducta, pero la rama no está escrita donde se usa.
- **Estado:** abierta.

---

## F-027 · La tabla del Paso 7 exige el grupo `gpio` que en realidad agrega el Paso 9

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 7: la tabla de CRITERIO DE ACEPTACIÓN exige que `id -nG` incluya `gpio` y `sudo`, cuando el grupo `gpio` lo agrega el Paso 9. La nota «Anotar los tres resultados…» lo aclara dos párrafos después, pero la tabla por sí sola se lee como un criterio que va a fallar en su primera pasada.
- **Estado:** abierta.

---

## F-028 · La evidencia de la fila 3 de la bitácora omite `stricthostkeychecking`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Bitácora §0, fila 3: la evidencia listada es `ssh -G ruleta | grep -E "^(hostname|user|identityfile) "`, sin `stricthostkeychecking`, que sí forma parte del criterio del Paso 3 y es lo que evita el fallo del Paso 6 con `BatchMode=yes`. La evidencia de la bitácora debería incluir el cuarto valor.
- **Estado:** abierta.

---

## F-029 · El respaldo por consola local pide hardware que la §3 declara innecesario

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Decisión 2.3 dice que la contraseña de `asadero` sirve «para entrar por consola local (teclado y monitor) y como respaldo», mientras que la §3 cierra con «No hace falta monitor ni teclado» y el material no incluye cable micro-HDMI ni teclado USB. El respaldo existe, pero ejercerlo requiere hardware que el plan declara innecesario; conviene decirlo en la decisión 3 junto con la ficha F-009.
- **Estado:** abierta.

---

## F-030 · El doble diagnóstico de la §7 (F-023) ahora pesa en el límite de 10 minutos

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §7, nota de los goldens: `python3 -m ruleta diagnostico` se corre dos veces (conteo de `[ok]` y conteo de «no está emparejada»), cada una con su espera de RFCOMM. Ya está anotado como F-023; sigue vigente y ahora pesa más al fijar el tiempo límite de 10 minutos.
- **Estado:** abierta.

---

## F-031 · El Paso 9 dice `enable` (no `start`) y `instalar.sh` también hace `restart`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** Paso 9, descripción del instalador, punto 6: dice «hace `daemon-reload` y `systemctl enable` (no `start`)», pero `instalar.sh` sí hace `systemctl restart` cuando el servicio ya estaba activo. En la Fase 1 nunca lo está, así que no cambia nada hoy; es una omisión que importaría si alguien reusa esa descripción en fases posteriores.
- **Estado:** abierta.

---

## F-032 · La fila 3 de la bitácora prueba tres valores y el Paso 3 exige cuatro

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §0 Bitácora, fila 3: la evidencia pide `ssh -G ruleta | grep -E "^(hostname|user|identityfile) "`, pero el CRITERIO del Paso 3 exige cuatro valores, incluido `stricthostkeychecking accept-new`. Convendría alinear la fila 3 con el grep de cuatro campos del Paso 3 para que la evidencia del acta pruebe lo mismo que el criterio.
- **Estado:** abierta.

---

## F-033 · El `head -n 6` del Paso 7 puede dejar fuera la línea `Powered:`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §4 Paso 7: `ssh ruleta 'bluetoothctl show | head -n 6'` recorta la salida a seis líneas. En BlueZ la línea `Powered:` suele ser la quinta, pero el orden de campos ha cambiado entre versiones y podría quedar fuera del recorte; el golden de la §7 (`bluetoothctl show | grep -c "Powered: yes"`) no tiene ese riesgo y es el que manda. Subir a `head -n 10` eliminaría el falso negativo.
- **Estado:** abierta.

---

## F-034 · La espera de 2 minutos del Paso 12 va como comentario y no resiste el pegado

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §4 Paso 12: el bloque de comandos del agente pone `ssh ruleta 'sudo reboot'` y, dos líneas después, `ssh ruleta 'sudo systemctl enable ruleta'`; la espera de 2 minutos va solo como comentario dentro del bloque. Copiado y pegado entero, el `enable` fallaría con `Connection refused`. Sacar la espera del comentario y ponerla como sub-paso numerado lo haría a prueba de pegado.
- **Estado:** abierta.

---

## F-035 · El Paso 9 cita el diagnóstico sin el `sudo -u` ni el `--config` de `instalar.sh`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §4 Paso 9, lista de lo que hace el instalador, punto 7: dice que corre `python3 -m ruleta diagnostico`; `instalar.sh` lo corre como `sudo -u "${USUARIO}" env PYTHONIOENCODING=utf-8 python3 -m ruleta --config "${DIR}/config.json" diagnostico`. El efecto es el mismo, pero el texto exacto difiere.
- **Estado:** abierta.

---

## F-036 · El Paso 9 no dice que el grupo `bluetooth` es condicional en `instalar.sh`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §4 Paso 9, punto 2: dice que el instalador agrega al usuario a los grupos `gpio` y `bluetooth`; en `instalar.sh` el de `bluetooth` es condicional (`getent group bluetooth >/dev/null && usermod -aG bluetooth ... || true`). No cambia ningún golden (ninguno comprueba el grupo `bluetooth`), pero el matiz no está dicho.
- **Estado:** abierta.

---

## F-037 · El Paso 9 enumera siete puntos y `instalar.sh` se autonumera `1/6` … `6/6`

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §4 Paso 9: la lista enumera siete puntos mientras que `instalar.sh` se autonumera `1/6` … `6/6` más el diagnóstico y el mensaje final. Es solo numeración, pero un ejecutor que cuente etiquetas en la salida verá seis, no siete.
- **Estado:** abierta.

---

## F-038 · El respaldo por IP del Paso 6 empieza con un `ping` al nombre que no resuelve

- **Fecha:** 2026-09-11
- **Origen:** lentes fase 1
- **Qué pasa:** §4 Paso 6, sub-paso de respaldo por IP: propone `ping -n 1 ruleta.local` como primer comando para averiguar la IP justo en el caso en que el error fue `Could not resolve hostname ruleta.local`; ahí ese `ping` también va a fallar. El `arp -a` de la línea siguiente es el que realmente sirve.
- **Estado:** abierta.

---

## F-039 · Los hechos medidos del orquestador sobre `~/.ssh` están desactualizados

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** Los hechos medidos que me dio el orquestador («no existe la carpeta ~/.ssh ni ninguna llave SSH») están desactualizados: verifiqué en disco que ~/.ssh existe con `config`, `id_ruleta`, `id_ruleta.pub` (ED25519, huella SHA256:sOmEM5P6LNzx7c5SOyy33NnxWOj+Qt4/RpPjwCcDSQw, comentario `ruleta-asadero`), `known_hosts` y `known_hosts.old`, todos de hoy 15:39-16:03. Las notas «(Medido...)» del Paso 2 y del Paso 3 del plan son las correctas; no hay nada que corregir ahí.
- **Estado:** abierta.

---

## F-040 · El bloque `Host ruleta` real trae `ConnectTimeout 10` e `IdentitiesOnly yes`

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** El bloque `Host ruleta` real de esta PC trae además `ConnectTimeout 10` (que el plan no menciona) y `IdentitiesOnly yes`. El criterio del Paso 3 no comprueba `identitiesonly`, aunque el propio plan explica por qué importa (corte tras 5 llaves rechazadas). Añadirlo al `grep -E` sería gratis.
- **Estado:** abierta.

---

## F-041 · La rama «`stricthostkeychecking` sale `ask`» del Paso 3 es la única acción manual del plan

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** El Paso 3, rama «si `stricthostkeychecking` sale `ask`», es el único punto del plan que pide una acción manual («abrir `~/.ssh/config`, agregar la línea») en un documento donde todo lo demás es copiable. Como ese caso está medido y es seguro que ocurrirá, convendría dar el comando exacto (por ejemplo `sed -i '/^Host ruleta$/a\    StrictHostKeyChecking accept-new' ~/.ssh/config` seguido del `ssh -G`).
- **Estado:** abierta.

---

## F-042 · La vista previa lleva prefijo de consola y el título de consuelo sale a 3x

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** En la vista previa cada línea lleva prefijo de la consola (`   |`, `*2x|`, `*4x|`) y el texto centrado conserva sus espacios (también duplicados). Los ejemplos del plan (`AAssaaddeerroo  3333`) omiten ese prefijo. Además el título del boleto de consuelo sale a 3x (`SSSIIIGGGUUUEEE` / `PPPAAARRRTTTIIICCCIIIPPPAAANNNDDDOOO`), no a 2x como el de premio.
- **Estado:** abierta.

---

## F-043 · El logo sale en la vista previa como líneas `[IMAGEN 384x64 px]` y no está descrito

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** El logo aparece en la vista previa como tres líneas `[IMAGEN 384x64 px]` / `[IMAGEN 384x22 px]` (por `banda_imagen: 64`). No está descrito y un ejecutor puede leerlo como un error del logo.
- **Estado:** abierta.

---

## F-044 · «Un par de minutos» de diagnóstico se repite en tres sitios sin haberse medido

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** El plan repite en tres sitios (preámbulo de tiempos, Paso 9 «Cosas normales», §5 trampa 12 y nota de la §7) que el diagnóstico «puede tardar un par de minutos probando canales RFCOMM». Leyendo `buscar_canal` (ruleta/escpos.py:442-458), solo continúa al siguiente canal con `ECONNREFUSED`; cualquier otro error aborta el barrido en el primer canal, así que contra `00:00:00:00:00:00` lo más probable es que tarde segundos. El límite de 10 minutos no estorba, pero conviene medir el tiempo real y anotarlo en el acta en vez de heredar la estimación.
- **Estado:** abierta.

---

## F-045 · El `sudo poweroff` del Paso 12 falla sin TTY si `sudo` pide contraseña

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** Paso 12, sub-paso 1: `ssh ruleta 'sudo poweroff'` sin TTY falla si `sudo` pide contraseña (`sudo: a terminal is required`). Como el Paso 7 ya determina ese dato, bastaría condicionarlo o usar `ssh -t`.
- **Estado:** abierta.

---

## F-046 · El Paso 14 escribe el acta en `docs/actas/`, que todavía no existe

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** Paso 14 escribe el acta en `docs/actas/<AAAA-MM-DD>-fase-1-preparar-pi.md`, pero ese directorio no existe todavía en el repo (solo hay `docs/fichas.md` y `docs/planes/`). Falta un `mkdir -p docs/actas` explícito.
- **Estado:** abierta.

---

## F-047 · La §7 no tiene golden para la escritura y propiedad de `~/ruleta/datos`

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** La §7 no tiene golden para la escritura/propiedad de `~/ruleta/datos`, aunque el criterio de las 6 líneas `[ok]` depende de ello. Un `ssh ruleta 'test -w ~/ruleta/datos && stat -c %U ~/ruleta/datos'` lo haría explícito.
- **Estado:** abierta.

---

## F-048 · Los comandos de verificación escriben en `datos/` y el plan no lo avisa

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** Los comandos de verificación (`vista-previa`, `diagnostico`, `reporte`) crean y tocan `datos/` (estado.json, lock). Es inocuo y `reiniciar --si` de la Fase 4 lo limpia, pero el plan no avisa de que sus propios pasos de verificación escriben en `datos/`.
- **Estado:** abierta.

---

## F-049 · El Paso 1 propone saltarse SmartScreen en vez de comprobar el SHA256 publicado

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** Paso 1 SI FALLA indica saltarse SmartScreen («Ejecutar de todas formas»). Está condicionado a que el archivo venga de raspberrypi.com, lo cual es razonable, pero comprobar el SHA256 publicado sería más sólido que confiar en el origen recordado.
- **Estado:** abierta.

---

## F-050 · Anclas y afirmaciones del repo ya verificadas (para no volver a auditarlas)

- **Fecha:** 2026-09-11
- **Origen:** esceptico fase 1
- **Qué pasa:** Anclas y afirmaciones del repo que verifiqué y SÍ son ciertas, para que nadie las vuelva a auditar: `git ls-files -s` da 100644 para `instalar.sh` y `herramientas/emparejar.sh` (trampa 1 correcta); `.gitattributes` fuerza `eol=lf`; `config.json` trae `"mac": "00:00:00:00:00:00"` y `"canal": 1`; `ruleta.service` trae `SupplementaryGroups=gpio`, `PYTHONIOENCODING=utf-8`, `User=@USUARIO@`, `WorkingDirectory=@DIR@`; `instalar.sh` instala exactamente la lista de paquetes que enumera el Paso 9, hace `enable` sin `start`, y contiene «== Diagnóstico» e «Instalación terminada» con 5 siguientes pasos; `CONFIG_DEFECTO = RAIZ / "config.json"` confirma la trampa 3; `datos/` está en `.gitignore`; el golden de 6 líneas `[ok]` se deriva correctamente de `cmd_diagnostico` (datos + PIL + gpiozero + lgpio + logo + inventario); la suite corre 141 pruebas y su última línea es exactamente `OK`; `ssh -G ruleta` imprime `identityfile ~/.ssh/id_ruleta` sin expandir (el criterio del Paso 3 es comparable tal como está) y hoy devuelve `stricthostkeychecking ask`, tal como el plan predijo.
- **Estado:** abierta.

---

## F-051 · El diagnóstico imprime `gpiozero` y `lgpio` sin número de versión

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · ejecución real en la Pi (`docs/actas/2026-09-11-fase-1.md`)
- **Dónde:** `ruleta/__main__.py`, dentro de `cmd_diagnostico`
  (`grep -n "__version__" ruleta/__main__.py`)
- **Qué pasa:** el diagnóstico imprime la versión de cada librería con
  `print(f"  [ok] {modulo} {getattr(m, '__version__', '')}")`. **Ni `gpiozero`
  ni `lgpio` exponen el atributo `__version__`**, así que las dos líneas salen
  con el nombre y **nada detrás**. Salida real medida en la Pi:
  `[ok] gpiozero ` y `[ok] lgpio ` (con el espacio y sin número), frente a
  `[ok] PIL 11.1.0`, que sí lo trae. **Las librerías están perfectamente
  instaladas**: consultadas con `importlib.metadata`, son `gpiozero 2.0.1` y
  `lgpio 0.2.2.0`. El mismo motivo hizo fallar un comando de verificación con
  `AttributeError: module gpiozero has no attribute __version__`.
- **Por qué es residual:** es **cosmético**. No afecta al funcionamiento, y el
  golden de la §7 del plan cuenta líneas `[ok]` (`grep -c`), así que tampoco se
  rompe.
- **Riesgo si no se toca:** alguien lee `[ok] gpiozero` sin número, cree que la
  instalación quedó a medias y "arregla" algo que no está roto. Ya está
  advertido en el plan de la Fase 1 (Paso 10 y notas de la §7).
- **Propuesta (para después del evento):** sustituir el `getattr` por
  `importlib.metadata.version(paquete)` dentro de un `try` / `except
  PackageNotFoundError`, que sí devuelve la versión real de cualquier paquete
  instalado por `apt` o por `pip`. Es un cambio de una línea y no toca ninguna
  prueba.
- **Relación con otras fichas:** **confirma y amplía la F-017**, que lo suponía
  solo para `lgpio` y a partir de la lectura del código. Ahora está medido en
  hardware real y se sabe que también le pasa a `gpiozero`. F-017 se puede
  cerrar contra esta.
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (e)). `version_modulo()` en `ruleta/__main__.py` pregunta primero a `importlib.metadata`, cae a `__version__` y, si no hay ninguno de los dos, dice `instalado`. Goldens en `tests/test_instalacion.py` (`TestVersionModulo`), incluido el vector real de PIL, que **no** tiene una distribución llamada «PIL» y por tanto solo pasa si el respaldo por `__version__` sigue en su sitio. **Confirmado en hardware el 2026-09-11**, tras el deploy: el diagnóstico de la Pi imprime `[ok] gpiozero 2.0.1` y `[ok] lgpio 0.2.2.0`, con número.
---

## F-052 · El `README.md` §9 pide el grupo `lp` y `asadero` no está en `lp`

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · ejecución real en la Pi + decisión del usuario de conectar
  la impresora por USB (`docs/actas/2026-09-11-fase-1.md`)
- **Dónde:** `README.md` §9 "Solución de problemas", último bloque
  (`grep -n "/dev/usb/lp0" README.md`): «usa el cable USB de la impresora y pon
  `"tipo": "archivo", "ruta": "/dev/usb/lp0"` (agrega tu usuario al grupo `lp`)»
- **Qué pasa:** el 2026-09-11 el usuario decidió que la impresora se conectará
  **por USB** (Bluetooth solo como respaldo), así que ese camino deja de ser una
  nota al pie y pasa a ser el principal de la Fase 2. **Pero los grupos medidos
  de `asadero` en la Pi son:** `asadero adm dialout cdrom sudo audio video
  plugdev games users input render netdev bluetooth spi i2c gpio lpadmin`.
  **Está `lpadmin`, que NO es lo mismo que `lp`.** `lpadmin` sirve para
  administrar CUPS; `lp` es el que suele dar acceso a los dispositivos de
  impresión. Además, ni `instalar.sh` agrega a `lp`, ni se ha comprobado que el
  nodo `/dev/usb/lp0` aparezca al conectar esta impresora, ni con qué grupo y
  permisos lo crea `udev` en Trixie.
- **Por qué es residual hoy:** en la Fase 1 no había impresora conectada, así
  que nada de esto se podía medir ni rompía nada.
- **Riesgo si no se toca:** la Fase 2 conecta el cable, escribe
  `"tipo": "archivo"` y el programa falla con `Permission denied` sobre
  `/dev/usb/lp0`, perdiendo tiempo en el sitio con el usuario esperando.
- **Qué verificar al empezar la Fase 2** (en este orden, con la impresora
  encendida y conectada):
  1. `ls -l /dev/usb/lp0` → ¿existe?, ¿de qué grupo es?, ¿qué permisos tiene?
  2. `id -nG asadero` → confirmar si hace falta `lp` o si el grupo real del nodo
     es otro.
  3. Si hace falta: `sudo usermod -aG <grupo> asadero`, **y recordar que el
     cambio solo se ve en una sesión SSH nueva** (§5, trampa 5 del plan de la
     Fase 1). Para el **servicio** no basta con eso: habría que agregar ese
     grupo a `SupplementaryGroups=` en `ruleta.service`, igual que ya se hace
     con `gpio`.
  4. Decidir si el arreglo definitivo es una **regla `udev`** (como la que ya
     existe para `gpiochip4`) en vez de tocar grupos a mano.
- **Propuesta:** resolverlo dentro de la Fase 2 y, con el resultado medido,
  corregir la frase del `README.md` §9 (que hoy da por hecho que el grupo es
  `lp`). **Tocar el README requiere visto bueno del usuario**, igual que F-001 a
  F-003.
- **Nota de la ronda 2 (lentes f1):** el pendiente 1 de la §7 del acta («resolver los permisos») queda como instrucción abierta: no dice qué se mide ni qué se considera éxito. **No es defecto del acta** —es lista de pendientes, no plan— porque los cuatro pasos concretos de verificación para el arranque de la Fase 2 están arriba, en esta misma ficha. Se anota aquí para no abrir una ficha repetida.
- **Estado:** **resuelta** el 2026-09-11 (medición en la Pi + sub-fase 2b). Medido esa noche: `/dev/usb/lp0` es `crw-rw---- root:lp` y `getent group lp` → `lp:x:7:asadero`, con `test -w` → ESCRIBIBLE. Y ya es reproducible: `instalar.sh` escribe la regla `/etc/udev/rules.d/61-ruleta-impresora-usb.rules` y hace `usermod -aG lp`; `ruleta.service` trae `SupplementaryGroups=gpio lp`; el `README.md` §4 paso 3 y §9 cuentan el camino real; y el diagnóstico, cuando no puede escribir, nombra la regla y el grupo en el mensaje.
---

## F-053 · El `README.md` usa `America/Mexico_City` y la zona real es `America/Hermosillo`

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · ejecución real (`docs/actas/2026-09-11-fase-1.md`,
  desviación D4)
- **Dónde:** `README.md` §4, paso 7 (`grep -n "America/Mexico_City" README.md`):
  `sudo timedatectl set-timezone America/Mexico_City`
- **Qué pasa:** la Pi quedó configurada en **`America/Hermosillo`** (`MST`,
  `-0700`), que es la zona de Sonora y la que el usuario eligió en Imager.
  Medido: `Time zone: America/Hermosillo (MST, -0700)`. El ejemplo del README
  propone `America/Mexico_City`, que es **una hora distinta** y, peor, **sí
  cambia de horario** mientras que Sonora no. El plan de la Fase 1 arrastraba el
  mismo error en su decisión cerrada 5, en el Paso 4, en el Paso 11 y en un
  golden de la §7: **eso ya está corregido** en
  `docs/planes/fase-1-preparar-pi.md`. **El README no se tocó.**
- **Por qué es residual:** es un ejemplo dentro de un paso condicional ("si la
  Pi no tendrá internet"), no una afirmación sobre el código. No rompe nada por
  sí solo.
- **Riesgo si no se toca:** alguien copia y pega ese comando tal cual para
  "arreglar la hora" y **deja los boletos con una hora de diferencia**, además
  de reintroducir el cambio de horario que Sonora no tiene. El daño se ve en el
  papel impreso y en el corte del "día" de las 6:00.
- **Propuesta:** cambiar el ejemplo del §4 paso 7 a
  `sudo timedatectl set-timezone America/Hermosillo`. **Requiere visto bueno del
  usuario** (toca documentación que él lee). Conviene resolverlo junto con
  F-001, F-002 y F-003, en una sola pasada al README.
- **Nota para quien lo haga:** el mismo paso 7 del README propone
  `sudo timedatectl set-ntp false` (ficha F-003). Con la decisión del 2026-09-11
  de que **la Pi irá sin red en producción**, ese consejo pasa de "solo si no
  habrá internet" a ser **el caso real** de este restaurante, siempre que la
  batería RTC esté instalada. Revisar las dos fichas a la vez.
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (g)). El `README.md` §4 paso 7 dice `sudo timedatectl set-timezone America/Hermosillo`. Medido: `grep -c "America/Mexico_City" README.md` → **0**.
---

## F-054 · El diagnóstico NO intenta conectarse con la MAC de relleno: un solo `[!!]` y termina en segundos

- **Fecha:** 2026-09-11
- **Origen:** Fase 1 · ejecución real en la Pi
  (`docs/actas/2026-09-11-fase-1.md`, anexo C)
- **Dónde:** `ruleta/app.py`, función `crear_impresora`
  (`grep -n 'strip("0")' ruleta/app.py`)
- **Qué pasa:** varias afirmaciones del plan y de la ficha F-004 decían que la
  MAC de relleno `00:00:00:00:00:00` "tiene formato válido, así que el programa
  la acepta y de verdad intenta conectarse", con "dos o tres líneas `[!!]`" y
  "hasta un par de minutos probando canales RFCOMM". **Medido en hardware real:
  es falso.** `crear_impresora` comprueba
  `imp.mac.replace(":", "").strip("0") == ""` y lanza `ErrorConfig` **antes de
  abrir ningún socket**. La salida real del diagnóstico es: seis `[ok]`, **una
  sola** línea `[!!] Falta la direccion Bluetooth de la impresora: pon la MAC
  real en impresora.mac de config.json (la obtienes con
  herramientas/emparejar.sh)` y `EXIT=1`, **en segundos**. El verificador
  independiente confirmó "exactamente un `[!!]`".
- **Por qué es residual:** el comportamiento del programa es **el correcto y el
  deseable**; lo que estaba mal era la documentación.
- **Qué ya se corrigió** en `docs/planes/fase-1-preparar-pi.md`: el encabezado
  de tiempos, el Paso 9 ("cosas normales que NO son errores"), el criterio 1 del
  Paso 10, la trampa 12 de la §5 y el golden de la §7, que contaba una frase
  (`no está emparejada`) **que no aparece**; se sustituyó por `grep -c "\[!!\]"`
  → `1` y `grep -c "impresora.mac"` → `1`, los dos sin acentos a propósito, para
  que no se rompan si la salida llega transliterada.
- **Qué queda pendiente:** las fichas **F-004**, **F-010** y **F-016** siguen
  repitiendo la estimación vieja. F-010 y F-016 ya sospechaban que era una cota
  superior y **acertaron**. La "propuesta" de F-004 —que el diagnóstico detecte
  la MAC de relleno y lo diga en vez de intentar conectarse— **ya está
  implementada en el código**: se puede cerrar contra esta ficha.
- **Ojo para la Fase 2:** el camino de conexión RFCOMM y la búsqueda de canal
  **nunca se han ejecutado**. Con una MAC de verdad sí se recorrerán, y ahí sí
  puede haber esperas y varios `[!!]`. Lo que se midió hoy **no** dice nada
  sobre cuánto tarda ese camino.
- **Estado:** abierta (solo para cerrar F-004, F-010 y F-016 cuando alguien las
  revise).

---

## F-055 · El acta se publica en un repositorio público con la IP local, el hostname y la regla de `sudoers`

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** El acta se va a publicar en un repositorio público (Ruelta-Aleatoria-Pi5) e incluye la IP local 192.168.50.178, la IPv6 de enlace local con su MAC, el hostname, el usuario asadero y el contenido de /etc/sudoers.d/010_asadero-nopasswd. Nada de eso es un secreto, pero conviene que el usuario sepa que queda publicado.
- **Nota de la ronda 2 (lentes f1):** reconfirmada. Los datos salen en el acta §3 fila 7-bis, §5 punto 2 y §6 punto 3 (nombre y contenido exacto de `/etc/sudoers.d/010_asadero-nopasswd`) y en la §4 (IP `192.168.50.178`, la IPv6 de enlace local —que lleva dentro la MAC de la Pi— y el hostname). No es un secreto y el acceso sigue siendo solo-por-llave, pero **conviene que el usuario lo sepa antes del push**.
- **Estado:** abierta.

---

## F-056 · `asadero ALL=(ALL) NOPASSWD: ALL` da root sin contraseña a quien tenga la llave `id_ruleta`

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** La regla 'asadero ALL=(ALL) NOPASSWD: ALL' da root sin contraseña a cualquiera que tenga la llave id_ruleta. Se creó a propósito y la decidió el usuario; valdría la pena acotarla o retirarla al terminar la instalación (el evento corre con la Pi aislada).
- **Nota de la ronda 2 (lentes f1):** reconfirmada. `asadero ALL=(ALL) NOPASSWD: ALL` convierte la llave `id_ruleta` en root sin contraseña; la ronda 2 insiste en **decidir si se acota o se retira al terminar la instalación**.
- **Estado:** abierta.

---

## F-057 · El acta cita como fuente `scratchpad/hechos-fase-1.md`, una ruta fuera del repositorio

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** El acta cita su fuente como 'scratchpad/hechos-fase-1.md', una ruta fuera del repositorio (directorio temporal de la sesión). Un lector futuro del repo no podrá abrirla; el Anexo A lo mitiga pegando la salida cruda.
- **Nota de la ronda 2 (lentes f1):** sin cerrar. La ronda 2 verificó que el **Anexo A es byte-idéntico** a la salida cruda del archivo de hechos, así que la mitigación funciona; lo que sigue apuntando fuera del repositorio es la cita de la fuente.
- **Estado:** abierta.

---

## F-058 · El encabezado de la §7 del plan dice «cumplidos» y dos líneas después admite que `SubState` no se midió

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Plan §7, encabezado: dice «Estado el 2026-09-11: cumplidos» y dos líneas después admite que el golden `SubState` no se midió, mientras el cuerpo de la §7 exige que **todos** los goldens den su valor exacto para cerrar la fase. La contradicción está a la vista del lector y el acta la registra como riesgo abierto, pero el encabezado convendría matizarlo a «cumplidos salvo `SubState`, no medido».
- **Anotado dos veces en la misma ronda:** la otra redacción, más corta, dice: «El aviso de la §7 del plan empieza con «Estado el 2026-09-11: cumplidos» y dos líneas después dice que SubState no se midió. Se entiende leyendo el párrafo entero, pero el titular va más lejos que la evidencia.» Es el mismo hallazgo, por eso va en una sola ficha.
- **Nota de la ronda f1:** esta ronda **no** tocó el encabezado de la §7 (no estaba en la lista de correcciones). Sí quedó corregido el cierre de la tabla de la §0-bis, que antes afirmaba que todos los demás goldens se habían medido. La ficha sigue abierta por el encabezado de la §7.
- **Nota de la ronda 2 (lentes f1):** sin tocar. El encabezado de la §7 del plan sigue diciendo «Estado el 2026-09-11: cumplidos» mientras el cuerpo exige que **todos** los goldens den su valor exacto y `SubState` no se midió. El acta sí lo marca «NO MEDIDO»; el titular del plan va más lejos que la evidencia. Emparentada con la nueva **F-071**: el mismo tipo de titular sin matiz, esta vez en el encabezado del acta.
- **Estado:** abierta.

---

## F-059 · El Paso 13 edita la locale del sistema con `sudo` sin exigir el visto bueno que sí pide el Paso 12

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** El Paso 13 hace que un agente edite /etc/locale.gen y la locale del sistema con sudo sed / localectl sin exigir el visto bueno explícito que sí pide el Paso 12 para config.txt. Hoy no muerde (paso no realizado), pero es asimétrico. Relacionado con F-026.
- **Estado:** abierta.

---

## F-060 · La advertencia del Paso 3 sobre «tres huellas ya grabadas» viene de la misma medición desactualizada

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** La advertencia del Paso 3 sobre «tres huellas ya grabadas para ruleta.local» viene de la misma medición desactualizada del orquestador que el Paso 2 (ficha F-039). El bloque de cita que sigue ya explica que no ocurrió, así que no bloquea.
- **Nota de la ronda f1:** la nota del Paso 2 ya quedó corregida en esta ronda (decía que `~/.ssh` «ya existía» y que el paso era «de verificación»; el archivo de hechos dice que no existía y que la llave se generó desde cero). La advertencia del Paso 3 **no** se tocó: no estaba en la lista de correcciones.
- **Estado:** abierta.

---

## F-061 · `git ls-files -s` sigue dando `100644`: tres textos prometen el modo `100755` «en este mismo cierre»

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Acta §5 punto 12 y §8 (fila del bit de ejecución) y Plan §0-bis D15 afirman que el agente de commit publica el modo `100755` «en este mismo cierre». Hoy `git ls-files -s` sigue dando `100644` para `instalar.sh` y `herramientas/emparejar.sh`. Es una promesa sobre un paso en curso, no una falsedad todavía; si el commit de cierre no incluye el cambio de modo, los tres textos quedan falsos y hay que corregirlos.
- **Anotado dos veces en la misma ronda:** la otra redacción dice: «Medido ahora en el repo: 'git ls-files -s' sigue dando 100644 para instalar.sh y herramientas/emparejar.sh. El acta (§5 punto 12 y §8) y la §0-bis D15 prometen que el agente de commit sube el modo 100755 «en este mismo cierre»: hay que verificarlo después del commit, o esas tres afirmaciones quedarán falsas.» Es el mismo hallazgo, por eso va en una sola ficha.
- **Qué hacer:** después del commit de cierre, correr `git ls-files -s instalar.sh herramientas/emparejar.sh`. Si sale `100755`, se cierran esta ficha y la parte correspondiente de F-050. Si sale `100644`, hay que corregir los tres textos.
- **Nota de la ronda 2 (lentes f1):** vuelta a medir hoy: `git ls-files -s instalar.sh herramientas/emparejar.sh` sigue devolviendo `100644` en los dos y `git log` no registra commit nuevo. La ronda 2 añade una **cuarta ubicación**: la §3 del acta (tabla de goldens) también promete el `100755` «en este mismo cierre». Sigue siendo una promesa sobre un paso en curso, no una falsedad todavía: re-medir después del commit de cierre y, si sigue en `100644`, corregir acta §3, acta §5 punto 12, acta §8 y plan §0-bis D15.
- **Estado:** abierta.

---

## F-062 · El acta §1 asigna modelo y esfuerzo por rol, y su propia nota admite que eso no se midió

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Acta §1, tabla de participantes: asigna modelo y esfuerzo («Opus, esfuerzo máximo») a cada agente, y la nota inmediatamente después aclara que el archivo de hechos no registra el modelo de cada corrida. La tabla afirma algo que la nota dice no haber medido; se sostiene solo por `CLAUDE.md` §1. Convendría marcar esa columna como «según CLAUDE.md §1 (no medido)».
- **Anotado dos veces en la misma ronda:** la otra redacción, más corta, dice: «El acta §1 asigna modelo y esfuerzo a cada rol; el archivo de hechos no registra el modelo de cada corrida. El propio acta lo advierte en su nota al pie, así que queda como constancia.» Es el mismo hallazgo, por eso va en una sola ficha.
- **Nota de la ronda 2 (lentes f1):** reconfirmada. La columna «Modelo / esfuerzo» afirma «Opus, esfuerzo máximo» por rol y la nota posterior admite que el archivo de hechos no registra el modelo de cada corrida; se sostiene solo por `CLAUDE.md` §1. La ronda 2 encontró además que ese puntero **falla para la fila «Fable»**: va aparte, en la nueva **F-076**.
- **Estado:** abierta.

---

## F-063 · El bloque del Paso 12 invoca `ssh` a secas, no el cliente nativo de Windows

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** El bloque del Paso 12 (sudo poweroff, sudo reboot, el bucle 'until ssh ... done') también invoca 'ssh' a secas: si se acepta la corrección del encabezado sobre el cliente nativo, conviene repasar ese bloque antes de ejecutarlo.
- **Nota de la ronda f1:** la corrección del encabezado **sí se aplicó**: la «Convención de comandos» ya manda escribir `/c/Windows/System32/OpenSSH/ssh.exe` en lugar de `ssh`, y avisa que en los ejemplos `ssh` va corto por legibilidad. El bloque del Paso 12 queda cubierto por esa regla general, pero **no** se reescribió comando por comando: antes de ejecutarlo hay que sustituir cada `ssh` por la ruta completa.
- **Nota de la ronda 2 (lentes f1):** sin cerrar, reconfirmada tal cual. El bloque del Paso 12 (`sudo poweroff`, `sudo reboot`, el bucle `until ssh ... done`) sigue invocando `ssh` a secas. Queda cubierto por la regla general de la «Convención de comandos», pero **antes de ejecutarlo hay que sustituir cada `ssh` por `/c/Windows/System32/OpenSSH/ssh.exe`**.
- **Estado:** abierta.

---

## F-064 · Los pendientes 1 a 4 de la §7 del acta coinciden con la §9 del plan; solo cambia el orden

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Los pendientes 1 a 4 de la §7 del acta sí son Fase 2 y coinciden con la §9 del plan; solo difiere el orden interno (el plan pone la vista previa junto a probar-impresora). Es estilo, no defecto.
- **Nota de la ronda f1:** los pendientes **5 y 6** de esa misma §7 sí eran un defecto (eran Fase 4, no Fase 2) y quedaron corregidos en esta ronda. Los 1 a 4 se dejan tal cual.
- **Estado:** abierta.

---

## F-065 · Plan §0, fila 11: marcada `[x]` aunque el criterio del Paso 11 se cumplió solo a medias

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Plan §0, fila 11 de la bitácora: está marcada `[x]` aunque el criterio de aceptación del Paso 11 pide cuatro valores y solo se midieron dos (`NTP` y `LocalRTC` quedaron sin medir). No engaña —la propia celda de evidencia lo dice y D12 lo explica— pero contradice la regla del encabezado de la §0 («se marcan `[x]` solo cuando el criterio de aceptación del paso se cumplió»). El acta ya usa «✅ parcial»; convendría que el plan use la misma marca.
- **Nota de la ronda 2 (lentes f1):** sin tocar. La fila 11 de la bitácora §0 del plan sigue `[x]` aunque el criterio del Paso 11 pide cuatro valores y solo se midieron dos (`NTP` y `LocalRTC` sin medir). El acta usa «✅ parcial»; el plan debería usar la misma marca para no romper la regla de su propio encabezado.
- **Estado:** abierta.

---

## F-066 · El golden `systemctl show -p SubState --value ruleta` sigue sin medir y cuesta un comando

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Golden `systemctl show -p SubState --value ruleta` → `dead`: es el único sin medir y cuesta un comando. Mientras la Pi siga en el Wi-Fi conviene correrlo y cerrar el hueco; con la Pi aislada (decisión D9) ya no se podrá.
- **Nota de la ronda 2 (lentes f1):** sin cerrar. Sigue siendo el **único golden sin medir** y cuesta un solo comando. Mientras la Pi siga en el Wi-Fi conviene correrlo; con la Pi aislada (decisión D9) ya no se podrá.
- **Estado:** abierta.

---

## F-067 · El mensaje de `instalar.sh` se cita sin acentos: `Aun NO se inicio.` frente a `Aún NO se inició.`

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Acta §3 fila 9 y Plan §0 fila 9 llaman «el mensaje literal» a `Servicio 'ruleta' habilitado (arranca solo al encender). Aun NO se inicio.`, pero el texto real de `instalar.sh` lleva acentos: `Aún NO se inició.`. La versión sin acentos es como llegó la salida al archivo de hechos. Nadie depende hoy de esa cadena, pero si alguien escribe un golden con `grep` literal, fallará.
- **Nota de la ronda 2 (lentes f1):** vigente y **confirmada hoy contra el archivo fuente**: `instalar.sh` línea 72 imprime `Servicio 'ruleta' habilitado (arranca solo al encender). Aún NO se inició.` **con** acentos. La cita sin acentos es fiel al archivo de hechos e infiel al fuente; un golden con `grep` literal fallaría. Precisión: una de las dos redacciones de la ronda 2 sitúa la cita en el acta §3 fila 9 **y en la §4**; medido hoy, en el acta solo aparece en la §3 fila 9 (línea 77) y en el plan en la §0 fila 9 (línea 85). No hay una tercera copia.
- **Estado:** abierta.

---

## F-068 · La ficha F-009 conserva la ambigüedad de «una copia segura de la llave»

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Acta §8, fila «La llave `id_ruleta` es el único acceso remoto»: propone «una copia segura de la llave» como mitigación, mientras la decisión cerrada 4 del plan dice que la llave privada nunca sale de la PC. No es contradicción dura (una copia offline no es «salir a un chat o al repositorio»), pero convendría redactarlo para que nadie lo lea como permiso para copiarla a la nube o a un chat. La ficha F-009 tiene la misma ambigüedad.
- **Nota de la ronda f1:** la fila del acta §8 **ya quedó corregida** en esta ronda: ahora dice expresamente que ningún agente copia, muestra ni transmite `~/.ssh/id_ruleta`, y que si el usuario quiere un respaldo lo hace él mismo, en un medio cifrado bajo su control. Lo que sigue abierto es el texto de **F-009**, que conserva la frase «o una copia de la llave en un lugar seguro» sin decir quién ni dónde.
- **Estado:** abierta.

---

## F-069 · El criterio escrito del Paso 1 (`ls` de `rpi-imager.exe`) nunca se corrió

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Acta §3, fila 1: el criterio del Paso 1 era el `ls` de `rpi-imager.exe` y se sustituyó por el registro de Windows. La evidencia es buena, pero el criterio escrito en el plan nunca se corrió; si alguien repite la fase, convendría alinear el criterio del Paso 1 con lo que de verdad se usó.
- **Estado:** abierta.

---

## F-070 · Sigue sin explicarse por qué no chocó `known_hosts` pese a las tres huellas previas

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 1
- **Qué pasa:** Acta §9 duda 1: sigue sin explicarse por qué no chocó `known_hosts` pese a las tres huellas previas que el plan daba por seguras. Queda como hueco de conocimiento; volverá a importar si se regraba la microSD (§5 trampa 15).
- **Nota de la ronda 2 (lentes f1):** sigue abierta, y la ronda 2 trae el dato que casi la cierra: el archivo de hechos **no registra ningún `ssh-keygen -R ruleta.local`**, pero sí dice «No existia ~/.ssh: se creo desde cero», de donde se sigue que tampoco existía `known_hosts` y por eso la primera conexión trató la huella como nueva. Lo que estaba mal era la medición del plan (Paso 3: «YA TIENE tres huellas grabadas»), la misma medición desactualizada de F-039 y F-060. Ver la nueva **F-075**.
- **Estado:** abierta.

---

## F-071 · El encabezado del acta dice «Fase 1 completada y verificada» sin el matiz que sí trae el plan

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md`, viñeta **Resultado** del encabezado (`grep -n "Resultado:" docs/actas/2026-09-11-fase-1.md`). Comparar con `docs/planes/fase-1-preparar-pi.md`, líneas 3 a 8.
- **Qué pasa:** Acta, encabezado: 'Resultado: Fase 1 completada y verificada' va sin matiz, mientras el plan es mas preciso ('COMPLETADA Y VERIFICADA en los pasos 1 a 11 y 14; faltan el 12 y el 13'). El propio acta lo aclara en la §2 y en la §3 (pasos 12 y 13 marcados NO REALIZADO, golden SubState NO MEDIDO), asi que no enganya; pero el titular va un poco mas lejos que la evidencia. Emparentado con F-058.
- **Comprobado en esta ronda:** medido hoy: el acta dice «**Fase 1 completada y verificada.**» (línea 7) y el plan «**COMPLETADA Y VERIFICADA el 2026-09-11** en los pasos 1 a 11 y 14. **Faltan el Paso 12 y el Paso 13**» (líneas 3 y 4). El acta sí marca «❌ NO REALIZADO» los pasos 12 y 13 (líneas 80 y 81) y «⚠️ NO MEDIDO» el golden `SubState` (línea 102): la aclaración existe, lo que va sin matiz es el titular.
- **Propuesta:** alinear el encabezado del acta con el del plan, por ejemplo «Fase 1 completada y verificada en los pasos 1 a 11 y 14; faltan el 12 (batería RTC) y el 13 (idioma)». Es un cambio de una frase y no toca ninguna evidencia.
- **Estado:** abierta.

---

## F-072 · El acta §9 duda 2 llama «verificados» a los dos commits siguientes, y el tercero también salió `push_correcto=false`

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §9, duda 2 (`grep -n "push_correcto" docs/actas/2026-09-11-fase-1.md`).
- **Qué pasa:** Acta §9 duda 2: dice que 'los dos commits siguientes si quedaron verificados', cuando el tercero (0464f5aa) tambien salio con push_correcto=false y se explica como falso negativo del guion. Se entiende leyendo la frase entera, pero convendria separar 'verificado' de 'falso negativo explicado'.
- **Comprobado en esta ronda:** el archivo de hechos registra tres commits: el inicial `9e8b9e87…` con `push_correcto: false` **y sin motivo**; `2052e470…` con `push_correcto=True`; y `0464f5aa…` con `push_correcto=False` **y motivo escrito** (el `grep` de «bitacora» sin acento del verificador no encontró «Bitácora»: falso negativo del guion, no del documento). O sea: uno verificado limpio, uno con falso negativo explicado y uno sin explicar.
- **Propuesta:** redactar la duda 2 con los tres casos separados, para que nadie cuente dos verificaciones limpias donde hay una. No cambia ningún hecho medido: solo el conteo que sugiere la frase.
- **Estado:** abierta.

---

## F-073 · El aviso del acta §7 sobre `docs/planes/fase-2-impresora.md` está verificado: ese archivo todavía no existe

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §7, párrafo de entrada; carpeta `docs/planes/`.
- **Qué pasa:** Acta §7: el aviso de que docs/planes/fase-2-impresora.md todavia no existe esta verificado (docs/planes/ solo contiene fase-1-preparar-pi.md). Se anota para que el cierre de esta fase no se lea como que el plan de la Fase 2 ya esta escrito.
- **Comprobado en esta ronda:** comprobado hoy: `docs/planes/` contiene **un solo archivo**, `fase-1-preparar-pi.md`. El aviso del acta es cierto.
- **Propuesta:** ninguna corrección: esta ficha existe **para que no se pierda el aviso**. Se cierra el día en que se escriba `docs/planes/fase-2-impresora.md`.
- **Estado:** abierta.

---

## F-074 · El acta §8 da por hecho que el usuario anotó la contraseña de `asadero` en papel, y eso no se midió

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §8, fila «La llave `id_ruleta` es el único acceso remoto»; `docs/planes/fase-1-preparar-pi.md`, Paso 4, bloque **ANTES DE EMPEZAR** (línea 675).
- **Qué pasa:** Acta §8, fila de la llave: «con la contraseña de `asadero` que el usuario anotó en papel». El archivo de hechos medidos NO registra eso; sale del bloque de requisitos del Paso 4 del plan (línea 675, prescriptivo). Choca con el encabezado del propio acta («lo que no se midió se dice que no se midió»). Sugerencia: «con la contraseña de `asadero` que solo el usuario conoce (el plan, Paso 4, pide anotarla en papel; no se midió que se hiciera)».
- **Comprobado en esta ronda:** el plan, en el bloque **ANTES DE EMPEZAR** del Paso 4, dice: «La contraseña que va a usar para el usuario `asadero` (anotada en papel, no en un chat)». Es una **instrucción**, no una medición, y el archivo de hechos no la confirma.
- **Propuesta:** aplicar la sustitución que propone el propio hallazgo. Es la redacción más corta que respeta la regla del encabezado del acta y no le quita fuerza a la mitigación.
- **Estado:** abierta.

---

## F-075 · La duda 1 del acta §9 está sobre-abierta: el archivo de hechos sí explica por qué no chocó `known_hosts`

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §9, duda 1; `docs/planes/fase-1-preparar-pi.md`, Paso 3, advertencia de las tres huellas (línea 621).
- **Qué pasa:** Acta §9, duda 1: el archivo de hechos sí contiene la explicación implícita de por qué no chocó `known_hosts` — «No existia ~/.ssh: se creo desde cero», luego tampoco existía `known_hosts`. Lo que estaba mal era la medición del plan (Paso 3, línea 621: «YA TIENE tres huellas grabadas»), la misma medición desactualizada de F-039/F-060. La duda está sobre-abierta; convendría cerrarla apuntando a esa contradicción. Complementa F-070.
- **Comprobado en esta ronda:** el archivo de hechos, en la nota del ejecutor de la llave SSH, dice: «No existia ~/.ssh: se creo desde cero. No se sobreescribio nada; no habia id_ruleta previo ni ~/.ssh/config previo.» Y más abajo: «La primera conexion agrego la huella ED25519 a known_hosts.» Si `~/.ssh` no existía, `known_hosts` tampoco: **no había nada con qué chocar**.
- **Propuesta:** cerrar la duda 1 del acta reescribiéndola como explicación (no como hueco de conocimiento) y apuntando a la medición desactualizada del plan. **F-070** queda apuntando aquí; las dos se cierran juntas.
- **Estado:** abierta.

---

## F-076 · El acta §1 remite a `CLAUDE.md` §1 para el modelo de Fable, y esa sección no fija modelo para el orquestador

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §1, fila «Fable», columna «Modelo / esfuerzo»; `CLAUDE.md` §1 «Roles fijos, por modelo».
- **Qué pasa:** Acta §1, fila «Fable»: la columna «Modelo / esfuerzo» dice «Según CLAUDE.md §1», pero CLAUDE.md §1 NO fija modelo ni esfuerzo para el orquestador (sí lo hace para ejecutor, revisores, exploradores, escriba, agente de commit y verificador de push). El puntero apunta a algo que no está escrito. Complementa F-062.
- **Comprobado en esta ronda:** leído hoy `CLAUDE.md` §1: la viñeta «**Orquestador (Fable).**» es **la única sin modelo ni esfuerzo entre paréntesis**. Las otras seis sí los traen: «Ejecutor (Opus, esfuerzo máximo)», «Revisores (Opus, solo lectura)», «Exploradores y extractores (Sonnet, solo lectura, esfuerzo bajo/medio)», «Escriba (Opus, esfuerzo máximo, solo lectura)», «Agente de commit (Opus, esfuerzo alto)» y «Verificador de push (Sonnet, solo lectura, esfuerzo medio)».
- **Propuesta:** o poner «—» en esa celda (como en la fila del usuario), o decidir el modelo del orquestador y **escribirlo en `CLAUDE.md` §1**. **Tocar `CLAUDE.md` requiere visto bueno del usuario.**
- **Estado:** abierta.

---

## F-077 · El pendiente 1 del acta §7 dice «poner» la llave `ruta` en `config.json`, y hoy esa llave hay que AÑADIRLA

- **Fecha:** 2026-09-11
- **Origen:** lentes f1 ronda 2
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §7, pendiente 1; `config.json`, objeto `impresora` (líneas 15 a 27); `ruleta/config.py` (valor por defecto).
- **Qué pasa:** Detalle menor del pendiente 1 de la §7 del acta: `config.json` hoy NO tiene la llave `ruta` dentro de `impresora` (usa el valor por defecto de `ruleta/config.py`, `salida_impresora.bin`). Poner `"tipo": "archivo", "ruta": "/dev/usb/lp0"` es válido (la llave existe en la dataclass), pero conviene decir que hay que AÑADIR la llave, no cambiarla.
- **Comprobado en esta ronda:** comprobado hoy: el objeto `impresora` de `config.json` trae `tipo`, `mac`, `canal`, `ancho_puntos`, `chars_por_linea`, `codepage`, `codepage_n`, `juego_internacional`, `cancelar_modo_chino`, `corte`, `lineas_antes_corte` y `beep`. **Ninguna llave `ruta`.**
- **Propuesta:** al escribir el plan de la Fase 2, redactarlo como «**añadir** la llave `ruta`» y no como «cambiarla», para que nadie la busque, no la encuentre y crea que el `config.json` está incompleto o corrupto.
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (c)). La llave se **añadió** al `config.json` del repositorio: `"ruta": "/dev/ruleta-impresora"`, junto con `"tipo": "archivo"` y `"beep": true`, y hay un golden que compara esa tupla completa por igualdad en `tests/test_config.py`.
---

## F-078 · `herramientas/emparejar.sh` sin argumento es interactivo y por SSH no interactivo muere con `MAC inválida: ''`

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §7, pendiente 2; `herramientas/emparejar.sh` (`grep -n "read -rp" herramientas/emparejar.sh`).
- **Qué pasa:** el pendiente 2 manda correr `./herramientas/emparejar.sh` **sin argumento**. Ese camino es **interactivo**: el script pregunta con `read -rp "Escribe la MAC de la impresora (AA:BB:CC:DD:EE:FF) o el número de la lista: "`. Lanzado desde una sesión SSH no interactiva —que es como los agentes hablan con la Pi— ese `read` lee EOF de inmediato, la MAC se queda vacía y el script muere con `MAC inválida: ''`. Nadie se queda colgado, pero el ejecutor ve un error que parece de la impresora y no lo es.
- **Comprobado en esta ronda:** `herramientas/emparejar.sh` línea 55 (`read -rp …`) y línea 64 (`echo "MAC inválida: '${MAC}'" >&2`).
- **Propuesta:** en el plan de la Fase 2, o bien decir que **este comando lo corre el usuario en la consola de la Pi** (teclado y pantalla, o `ssh -t`), o bien pasarle la MAC como argumento (`./herramientas/emparejar.sh AA:BB:CC:DD:EE:FF`) cuando ya se conozca.
- **Estado:** abierta.

---

## F-079 · El pendiente 5 de la §7 mete `reiniciar --si` en la lista de la Fase 2 aunque su propio texto avise que es Fase 4

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §7, pendiente 5; `ruleta/__main__.py`, `cmd_reiniciar`.
- **Qué pasa:** la lista se titula «Pendientes para la Fase 2» y su punto 5 trae `python3 -m ruleta reiniciar --si`, es decir **sin pedir confirmación**. El texto avisa entre paréntesis «Esto ya es Fase 4, no Fase 2», pero un ejecutor que recorra la lista numerada de arriba abajo deja folio e inventario en cero antes de tiempo.
- **Comprobado en esta ronda:** no hay pérdida definitiva: `cmd_reiniciar` respalda `estado.json` y `ruleta.log` con marca de tiempo (`shutil.copy2` a `<nombre>_AAAAMMDD_HHMMSS.<ext>`) antes de vaciar, e incluso se niega a correr si el servicio `ruleta` está activo. Lo que se pierde es el tiempo y la confianza en la lista.
- **Propuesta:** sacar el punto 5 de la lista numerada (a un apartado propio «Esto NO es la Fase 2») o marcarlo **NO EJECUTAR EN LA FASE 2** al principio de la línea, no entre paréntesis.
- **Estado:** abierta.

---

## F-080 · El golden `NTPSynchronized` se marcó ✅ con `timedatectl` a secas, no con el comando que pide el plan

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §3, tabla «Goldens de la §7 del plan», última fila; `docs/planes/fase-1-preparar-pi.md` §7 (`grep -n "NTPSynchronized" docs/planes/fase-1-preparar-pi.md`, línea 1650).
- **Qué pasa:** el golden escrito en el plan es `timedatectl show -p NTPSynchronized --value` → `yes`. Lo que se midió fue la línea `System clock synchronized: yes` de `timedatectl` **a secas**. En la práctica dicen lo mismo, pero no son el mismo comando. En la fila de Python el acta **sí** anotó esa distinción («se midió con `python3 --version`, no con el `python3 -c`»); aquí falta el mismo matiz.
- **Comprobado en esta ronda:** el archivo de hechos solo trae el bloque `=== TIMEDATECTL ===` con las tres líneas de `timedatectl` a secas; no contiene ninguna salida de `timedatectl show`.
- **Propuesta:** añadir a esa fila el mismo paréntesis que lleva la de Python, o correr el comando exacto cuando la Pi vuelva a estar en red (se puede juntar con el golden pendiente de **F-066**).
- **Estado:** abierta.

---

## F-081 · La fila 12 de la §3 afirma «no hay batería ni línea `rtc_bbat_vchg`» como hecho medido, y nadie leyó `config.txt`

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §3, fila 12 «Batería RTC», columna «Evidencia medida».
- **Qué pasa:** la celda dice «No hay batería ni línea `rtc_bbat_vchg`». Lo de la batería consta (el usuario todavía no la compra). Lo de la línea **no se midió**: el archivo de hechos no contiene ninguna lectura de `/boot/firmware/config.txt`. Es casi seguro cierto, porque nadie corrió el Paso 12, pero el propio acta se impone la regla «lo que no se midió se dice que no se midió» y aquí no la cumple.
- **Comprobado en esta ronda:** buscado hoy en el archivo de hechos: **cero** apariciones de `config.txt` y ninguna salida de `grep rtc_bbat_vchg`. Lo único que hay es la decisión del usuario («en producción la Pi va SIN red, por tanto batería RTC necesaria»).
- **Propuesta:** reescribir la celda como «Batería: **no instalada** (consta). Línea `rtc_bbat_vchg`: **no medida**; nadie leyó `/boot/firmware/config.txt`», y dejar la comprobación para el Paso 12.
- **Estado:** abierta.

---

## F-082 · La fila 14 de la §3 dice «fichas F-051 a F-054» y hoy `docs/fichas.md` llega mucho más lejos

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §3, fila 14 «Cierre de fase» (línea 82).
- **Qué pasa:** la evidencia de la fila 14 enumera «las fichas **F-051 a F-054**». Ese rango era cierto cuando se escribió la fila, pero las rondas de revisión de este mismo cierre añadieron de **F-055 en adelante**. Quien lea la fila creerá que el cierre de la Fase 1 produjo cuatro fichas.
- **Comprobado en esta ronda:** antes de esta ronda `docs/fichas.md` tenía **77** fichas y la última era **F-077**; esta ronda añade de **F-078** en adelante.
- **Propuesta:** cambiar el rango por «las fichas **F-051 en adelante** (ver `docs/fichas.md`)», que no caduca con cada ronda de revisión.
- **Estado:** abierta.

---

## F-083 · La §1 dice «3 correcciones aplicadas» del escéptico y el archivo de hechos solo registra 3 propuestas

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §1, fila «Escéptico»; archivo de hechos, línea «plan fase 1: … `esceptico correcciones=3 residuales=12`».
- **Qué pasa:** la celda dice «3 correcciones **aplicadas**, 12 hallazgos residuales a fichas». El archivo de hechos solo registra el número de correcciones que el escéptico **propuso**; que se aplicaran no está medido en ninguna parte.
- **Comprobado en esta ronda:** la única línea del archivo de hechos sobre el escéptico es `esceptico correcciones=3 residuales=12`. No hay informe de aplicación ni diff que lo respalde.
- **Propuesta:** escribir «3 correcciones **propuestas**» salvo que se recupere la evidencia de que se aplicaron. Es el mismo criterio que el resto del acta se impone.
- **Estado:** abierta.

---

## F-084 · El `[!!]` de la impresora se cita sin acentos (`Falta la direccion…`) frente al `Falta la dirección…` del código

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md`, **Anexo C** (línea 466); `ruleta/app.py` línea 48 (`crear_impresora`).
- **Qué pasa:** el mensaje real del código lleva acento: `Falta la dirección Bluetooth de la impresora: pon la MAC real en impresora.mac de config.json …`. El acta lo reproduce **sin acentos** porque así llegó al archivo de hechos (la salida por SSH los perdió). Nadie depende hoy de esa cadena, pero quien compare por igualdad literal contra la Pi verá una diferencia. Es el mismo caso que **F-067** (`Aun NO se inicio.` frente a `Aún NO se inició.`).
- **Comprobado en esta ronda (precisión sobre el hallazgo original):** el hallazgo lo situaba en la §3 y la §4 del acta. Medido hoy, la cita literal aparece **solo en el Anexo C**; la §3 (fila del golden `no está emparejada`) y la §4 hablan del `[!!]` sin reproducir el texto.
- **Propuesta:** una sola nota junto a los anexos que diga que **el archivo de hechos llegó sin acentos** y que los textos reales de `ruleta/app.py` e `instalar.sh` sí los llevan. Con eso se cubren esta ficha y **F-067** de una vez.
- **Estado:** abierta.

---

## F-085 · La tabla de riesgos §8 no tiene fila para «el servicio quedó `enabled` y arranca solo en cada reinicio»

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §8 «Riesgos abiertos»; §7, pendiente 6; `ruleta.service` (`WantedBy=multi-user.target`, `Restart=always`, `RestartSec=3`, `StartLimitIntervalSec=0`).
- **Qué pasa:** entre la Fase 1 y la Fase 4 hay al menos dos apagados previstos (poner la batería RTC y conectar el cable USB de la impresora), y en cada uno systemd arranca `ruleta` **solo**. La tabla de riesgos no lo menciona, y la tabla es justo lo que se lee de un vistazo.
- **Comprobado en esta ronda:** el pendiente 6 de la §7 **ya quedó corregido** en esta ronda y lo explica con detalle (bucle de reintentos cada 3 s con la MAC en ceros; ruleta jugando e imprimiendo con los premios `test1`…`test7` si la impresora ya funciona). La §8 sigue sin fila propia.
- **Propuesta:** añadir a la §8 una fila «El servicio quedó `enabled` y arranca solo en cada reinicio antes de la Fase 4» — gravedad **media**; «qué pasa»: con la MAC en ceros entra en bucle de reintentos sin límite, y con la impresora ya funcionando imprime el inventario con premios de prueba; «qué hacer»: `sudo systemctl disable ruleta` antes de apagar y `sudo systemctl enable ruleta` al volver, igual que el Paso 12 del plan.
- **Estado:** abierta.

---

## F-086 · El encabezado de la §7 dice «como usuario `asadero`» y tres de sus pendientes necesitan `sudo`

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §7, encabezado y pendientes 1, 2 y 6; `herramientas/emparejar.sh` línea 30; §3, fila 7-bis.
- **Qué pasa:** el encabezado dice «Todo esto se corre **en la Pi, como usuario `asadero`**, dentro de `/home/asadero/ruleta`». Tres pendientes van más allá: el **1** (arreglar los permisos de `/dev/usb/lp0`) necesita `sudo`, el **6** (`sudo systemctl start ruleta`) lo lleva escrito, y el **2** (`emparejar.sh`) hace `sudo rfkill unblock bluetooth` **por dentro**, sin avisar. Hoy no hay fricción por la regla NOPASSWD que creó el usuario (§3, fila 7-bis), pero conviene decirlo en vez de dejar que se descubra en el sitio.
- **Comprobado en esta ronda:** `herramientas/emparejar.sh` línea 30: `sudo rfkill unblock bluetooth 2>/dev/null || true`.
- **Propuesta:** añadir al encabezado «algunos pasos usan `sudo`; hoy funciona sin contraseña por `/etc/sudoers.d/010_asadero-nopasswd`». Relacionada con **F-056**: si esa regla se acota o se retira al terminar la instalación, estos pendientes empezarán a pedir contraseña.
- **Estado:** abierta.

---

## F-087 · La fila «Bit de ejecución (+x)» de la §8 no dice que `instalar.sh` ya hace `chmod +x` de `herramientas/*.sh`

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `docs/actas/2026-09-11-fase-1.md` §8, fila «Bit de ejecución (`+x`) fuera del repositorio»; `instalar.sh` línea 60.
- **Qué pasa:** la fila dice que cada clon nuevo necesita el `chmod +x` o `instalar.sh` falla con `Permission denied`. Falta el matiz: el paso **5/6** de `instalar.sh` ya corre `chmod +x "${DIR}/herramientas/"*.sh`. Es decir, el `chmod +x` manual del Paso 8 es imprescindible **solo para `instalar.sh`**; `emparejar.sh` recupera su bit en cuanto el instalador corre una vez.
- **Comprobado en esta ronda:** `instalar.sh` línea 60, dentro del bloque `== 5/6 Carpeta de datos y permisos`: `chmod +x "${DIR}/herramientas/"*.sh 2>/dev/null || true`.
- **Propuesta:** añadir ese matiz a la fila de la §8 (y, si se quiere, al Paso 8 del plan). No cambia la solución de fondo, que sigue siendo commitear el modo `100755` (**F-061**).
- **Estado:** abierta.

---

## F-088 · El `/dev/usb/lp0` del README aparece en dos sitios (§6 y §9); al corregirlo hay que tocar los dos

- **Fecha:** 2026-09-11
- **Origen:** escéptico f1
- **Dónde:** `README.md` línea 255 (§6, tabla de `config.json`, fila de la llave `ruta`) y línea 429 (§9, solución de problemas); `docs/actas/2026-09-11-fase-1.md` §9 duda 3 y §7 pendiente 1.
- **Qué pasa:** la duda 3 de la §9 y el pendiente 1 de la §7 del acta citan **solo** el `README.md` §9. La tabla del §6 también menciona `/dev/usb/lp0`: «`ruta` | `"salida_impresora.bin"` | solo con `tipo: archivo`; p. ej. `/dev/usb/lp0` si algún día va por USB». Cuando se corrija el README con visto bueno del usuario hay que tocar **los dos sitios**; si no, el README seguirá diciendo a la vez que el USB es el camino principal de la Fase 2 y que es un «algún día».
- **Comprobado en esta ronda:** `grep -n "/dev/usb/lp0" README.md` → líneas **255** y **429**.
- **Propuesta:** anotar las dos ubicaciones en **F-052** (que hoy apunta solo al §9) y corregirlas juntas, en el mismo cambio y con el mismo visto bueno. Emparentada con **F-077** (la llave `ruta` hay que **añadirla**, no cambiarla).
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (g)). Los dos sitios se corrigieron juntos: la fila `ruta` del §6 dice que el valor real es `/dev/ruleta-impresora` (con `/dev/usb/lp0` como el nodo que hay detrás) y el §9 dejó de hablar de «si algún día va por USB». Medido: `grep -c "/dev/ruleta-impresora" README.md` → **5** y `grep -c "/dev/usb/lp0" README.md` → **4**, todas como nodo real, no como alternativa.
---

## F-089 · El `README.md` §5 dice que los comandos avisan si el servicio está corriendo, y `probar-impresora` no lo hace

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · redacción de `docs/planes/fase-2-impresora.md` (lectura
  del código, no del papel)
- **Dónde:** `README.md` §5, líneas 222-225
  (`grep -n "Los comandos lo detectan" README.md`) y
  `ruleta/__main__.py` (`grep -n "servicio_activo" ruleta/__main__.py`).
- **Qué pasa:** el README dice, literalmente: «**Detén el servicio**
  (`sudo systemctl stop ruleta`) antes de `reiniciar`, `liberar`,
  `reporte --imprimir` o `probar-impresora` […] **Los comandos lo detectan y te
  lo recuerdan.**» Medido en el código: `servicio_activo()` se define en la
  línea 87 y se llama **cuatro** veces —`cmd_reporte` (211, solo bajo
  `--imprimir`), `cmd_liberar` (227), `cmd_reiniciar` (266) y `cmd_diagnostico`
  (375)—. **`cmd_probar_impresora` no la llama nunca.** Es decir: de los cuatro
  comandos que el README nombra, **tres avisan y uno no**, y justamente el que
  no avisa es el que se usa a cada rato mientras se ajusta la impresora.
- **Por qué es residual:** no rompe nada por sí solo y el propio README manda
  detener el servicio; lo que falla es la promesa de que el programa te va a
  proteger si se te olvida.
- **Riesgo si no se toca:** alguien corre `probar-impresora` con el servicio
  arriba confiando en el aviso. Por Bluetooth eso da un error de conexión
  confuso (la impresora acepta una sola conexión); por USB los dos procesos
  escriben al mismo dispositivo y **puede salir un boleto mezclado con otro**.
- **Dos propuestas, y conviene hacer las dos:**
  1. **Código:** llamar a `servicio_activo()` también en `cmd_probar_impresora`,
     con el mismo mensaje que ya usa `cmd_reporte`. Es de tres líneas y tiene
     golden fácil.
  2. **Documentación:** corregir la frase del README. **Requiere visto bueno del
     usuario**, igual que F-001 a F-003, F-052, F-053 y F-088; va en la misma
     pasada, dentro del punto (d) de la sub-fase 2b.
- **Mientras tanto:** el plan de la Fase 2 lo cubre a mano — su Paso 7 obliga a
  comprobar `systemctl is-active ruleta` antes de imprimir, y su §5 trampa 2 lo
  explica.
- **Estado:** **resuelta a medias.** La parte de documentación quedó hecha el 2026-09-11 (2b, cambio (g)): el `README.md` §5 dice ahora que `reiniciar`, `liberar` y `reporte --imprimir` sí lo detectan y que **`probar-impresora` no avisa**. Medido: `grep -c "comandos lo detectan" README.md` → **0**. La parte de código (llamar a `servicio_activo()` dentro de `cmd_probar_impresora`) **sigue pendiente**: no estaba en el alcance de 2b y toca un comando que el usuario corre a cada rato.
---

## F-090 · `ImpresoraArchivo` abre con `O_CREAT`: con `sudo` puede crear un archivo donde debería estar el dispositivo

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · redacción del plan (lectura del código)
- **Dónde:** `ruleta/escpos.py`, `ImpresoraArchivo.imprimir`
  (`grep -n "class ImpresoraArchivo" -A 25 ruleta/escpos.py`, hoy línea 546; la
  apertura está en la 560).
- **Qué pasa:** el transporte abre con
  `self._abrir(self.ruta, "ab" if self.anexar else "wb", buffering=0)`, y
  `crear_impresora` lo construye siempre con `anexar=True` (`ruleta/app.py`,
  línea 56). Los modos `"ab"` y `"wb"` incluyen `O_CREAT`: **si la ruta no
  existe, se crea**. Con el camino USB eso significa que, si `/dev/usb/lp0` no
  está (impresora apagada, cable suelto, `usblp` sin cargar) y alguien corre el
  programa **con `sudo`**, se crea un **archivo normal** llamado
  `/dev/usb/lp0` que **se traga los boletos sin dar ningún error** —código de
  salida 0, mensaje «Listo», y ni un centímetro de papel— y que además **impide
  que el nodo real aparezca** cuando la impresora vuelva.
- **Lo que hoy nos salva:** como usuario `asadero` no se puede escribir en
  `/dev` ni en `/dev/usb` (son de root), así que el intento falla con
  `Permission denied`, que es justo el error que se quiere ver. **El riesgo
  aparece solo si alguien usa `sudo`**, cosa que además rompe los permisos de
  `datos/`.
- **Por qué es residual:** el comportamiento actual es correcto para el uso
  previsto (escribir a un archivo de pruebas), y el camino peligroso exige un
  `sudo` que el plan prohíbe explícitamente.
- **Riesgo si no se toca:** una tarde de prisas, alguien escribe `sudo` por
  costumbre y deja el kiosco «funcionando» sin imprimir nada, con el diagnóstico
  en verde. Es de los fallos más difíciles de encontrar mirando la pantalla.
- **Propuesta:** en la sub-fase 2b, cuando se toque `ImpresoraArchivo` para la
  consulta de papel (cambio (b)), abrir con `os.open` sin `O_CREAT` cuando la
  ruta **empiece por `/dev/`**, o comprobar con `stat` que la ruta existe y es
  un dispositivo antes de abrirla, devolviendo `ErrorConexion` con un mensaje
  claro si no. Golden fácil: con una ruta inexistente bajo `/dev`, `imprimir`
  lanza `ErrorConexion` y **no crea el archivo**.
- **Mientras tanto:** el plan de la Fase 2 lo cubre en su §5 trampa 4, en su §8
  prohibición 3 y en el «SI FALLA» del Paso 7 (`test -c`).
- **Estado:** abierta, y **con el mismo riesgo que antes** del 2026-09-11 (2b, cambio (d)). Es cierto que `ImpresoraArchivo` abre con `r+b` —que **no crea** el archivo— cuando va a consultar el papel, pero ese camino solo se toma si la ruta **ya existe y es un dispositivo de caracteres** (`preguntar = self.consultar_estado and self._es_dispositivo(self.ruta)`, y `es_dispositivo_caracteres` devuelve `False` cuando la ruta no existe). Es decir: en el escenario peligroso de esta ficha —el nodo NO está y alguien corre con `sudo`— se sigue abriendo con `ab`/`wb` y se sigue creando un archivo normal donde debería estar el dispositivo. La propuesta de rechazar rutas inexistentes bajo `/dev/` no se implementó: no estaba en el alcance de 2b.
---

## F-091 · Por USB se ignoran `consultar_estado`, `reintentos` y todas las llaves de ritmo

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · redacción del plan (lectura del código)
- **Dónde:** `ruleta/app.py`, `crear_impresora` (`grep -n 'tipo == "archivo"' -A
  2 ruleta/app.py`, hoy línea 56) y `ruleta/escpos.py`, `ImpresoraArchivo`
  (546).
- **Qué pasa:** con `"tipo": "archivo"`, el transporte se construye con
  `escpos.ImpresoraArchivo(imp.ruta, anexar=True)` **y nada más**. Todas estas
  llaves de la sección `impresora` de `config.json` **no tienen ningún efecto**
  por USB: `consultar_estado`, `reintentos`, `espera_reintento_seg`,
  `timeout_seg`, `tamano_bloque`, `pausa_bloque_seg`, `pausa_inicial_seg`,
  `pausa_final_seg` y `bytes_por_segundo`. Solo las usa
  `ImpresoraBluetooth`. Dos consecuencias concretas: **(1)** por USB el programa
  **no pregunta si hay papel** —si el rollo se acaba, el premio se descuenta y
  el boleto no sale—, y **(2)** por USB **no hay reintentos**: un fallo puntual
  al abrir el dispositivo pierde ese boleto (el premio **sí** vuelve al
  inventario, porque `ErrorConexion` lo devuelve, así que no se regala nada; lo
  que se pierde es la impresión).
- **Por qué es residual:** por cable, la falta de reintentos y de control de
  ritmo es razonable: no hay un enlace de radio que se caiga a media frase. Lo
  que sí importa de verdad es la consulta de papel.
- **Riesgo si no se toca:** **(a)** el evento corre una semana sin aviso de
  «sin papel»; **(b)** alguien intenta arreglar un problema de impresión por
  cable subiendo `reintentos` o bajando `tamano_bloque`, y no pasa nada, porque
  esas llaves no se leen. Se pierde una tarde buscando donde no hay.
- **Propuesta:** el cambio (b) de la sub-fase 2b (consulta `DLE EOT` en
  `ImpresoraArchivo`, respetando `consultar_estado`), **solo si la interfaz USB
  resulta ser bidireccional** (`bInterfaceProtocol = 02`, se mide en el Paso 3
  del plan de la Fase 2). Y, en cualquier caso, decir en la tabla del `README`
  §6 qué llaves valen para cada `tipo`: hoy la tabla las presenta como si
  valieran siempre.
- **Nota:** el PPD del driver del fabricante confirma que la impresora entiende
  `DLE EOT 1`, así que la consulta tiene sentido técnico
  (`docs/actas/2026-09-11-hechos-medidos.md`, sección del driver).
- **Estado:** **resuelta a medias** el 2026-09-11 (2b, cambio (d)). `consultar_estado` ya vale por USB: `crear_impresora` se lo pasa a `ImpresoraArchivo` y este pregunta `DLE EOT` antes del boleto cuando la ruta es un dispositivo de caracteres, con la misma política que el Bluetooth (si no contesta, se imprime igual). **Siguen sin efecto por cable** `reintentos`, `timeout_seg`, `tamano_bloque`, `pausa_bloque_seg`, `pausa_inicial_seg`, `pausa_final_seg` y `bytes_por_segundo`, y así lo dice ahora la tabla del `README.md` §6, con una nota debajo. `espera_reintento_seg` **sí** cuenta con cualquier tipo: `Ruleta.arrancar` (`ruleta/app.py`) espera el doble de ese valor entre los intentos del inventario de arranque. **Medido en hardware real el 2026-09-11**, tras el deploy: la impresora contestó `DLE EOT` por el nodo USB y el servicio escribió `La impresora /dev/ruleta-impresora reporta poco papel: cambia el rollo pronto` **antes** de mandar el inventario. **Corrección del 2026-09-15 (Fase 4a): esa frase decía que «la consulta funciona de verdad por cable y lanzada desde systemd», y es falsa.** Lo único que quedó demostrado por cable es que **el nodo acepta la escritura del comando**: el byte que se leyó era el **rezagado de otra pregunta** (la impresora repite sin parar el último byte de estado), de modo que aquel aviso de «poco papel» era **falso** (**F-190**). Lo único que sigue sin probarse de esta parte es el caso extremo (sin papel o fuera de línea) con el rollo fuera. **MEDIDO POR FIN el 2026-09-15 a las 13:29:17 (Fase 3), y FALLÓ.** El usuario dejó la impresora **sin papel** a propósito y jugó una vez, con el servicio `active` y el folio previo en 8. La impresora encendió su foco rojo y se puso a pitar cada segundo, con el trabajo retenido en su búfer. El journal dice, en orden: `Boleto 00009 emitido: TEST 7` → `WARNING … reporta poco papel` (el aviso rezagado de siempre) → `Boleto 00009 impreso: TEST 7`. **No se detectó «sin papel» ni «fuera de línea»:** las dos guardias que añadió 2b quedaron derrotadas por el **mismo desfase de un comando** diagnosticado el 2026-09-13 —la impresora repite el último byte de estado y el programa lee la respuesta a la **pregunta anterior**—, tal y como lo había predicho el escéptico de ese día. Daño medido: `boletos.csv` con el 00009 `emitido` **e** `impreso`, `estado.json` en folio 9 y el premio **TEST 7 descontado sin que saliera papel**; el proceso, sano (`wchan` = `hrtimer_nanosleep`, `NRestarts=0`), porque la escritura a `usblp` no se bloqueó. Al reponer el papel (13:31–13:33) la impresora soltó sola el boleto retenido, cortado —lo que **no** salva el caso: si se apaga la impresora o la Pi antes de reponer, el trabajo se pierde y el programa ya lo dio por impreso—. Evidencia: `docs/actas/2026-09-15-fase-3.md` §6-bis. **El arreglo va en la ficha F-250.** **Cerrado el 2026-09-15 (Fase 4a):** el camino «sin papel» **ya está medido** —falló— y **queda arreglado en el cambio de código de esta fase**: `leer_estado_fresco` (`ruleta/escpos.py`) drena el atraso, escribe el comando y se queda con el **último** byte válido, y `verificar_estado` añade la pregunta `DLE EOT 2`, que es la única que en esta impresora se entera del rollo agotado (`0x32`, medido). Lo que **sigue abierto** de esta ficha es lo de siempre: `reintentos`, `timeout_seg` y las llaves de ritmo siguen **sin efecto por cable**.
- **Nota de cierre del 2026-09-15 (Fase 4a, tras la prueba en vivo de las 21:32).**
  **El camino «sin papel» ya está medido EN LOS DOS SENTIDOS, con el usuario
  delante y el mismo experimento las dos veces.** Con el código viejo, el
  2026-09-15 a las **13:29**, **falló**: el kiosco emitió el 00009, lo descontó y
  lo dio por impreso sin que saliera papel. Con el código de
  `2a0aba3e01dcd15878579f1d02a64457b1834046`, el mismo día a las **21:32**,
  **funcionó**: los boletos **00013** y **00014** se revirtieron sin mandar un
  solo byte (`la impresora /dev/ruleta-impresora no tiene papel` →
  `premio devuelto al inventario`), **no quedó nada retenido** en la impresora y
  con el rollo repuesto el **00015** y el **00016** salieron normales;
  `estado.json` conservó `test5` = 2, o sea que **los premios revertidos no se
  descontaron**. Evidencia: `docs/actas/2026-09-15-fase-4a.md` §8. **Lo que esta
  ficha sigue teniendo abierto es solo lo de la línea anterior:** `reintentos`,
  `timeout_seg` y las llaves de ritmo, que por cable siguen sin efecto.
---

## F-092 · El plan de la Fase 2 dice que incorpora mediciones del 2026-09-12 y todas son del 2026-09-11

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md` encabezado, §0-bis, §3 (material) y Paso 2.
- **Qué pasa (texto del lente, tal cual):** Fechas incoherentes: el encabezado dice «Redactado el 2026-09-11 … incorporando los hechos que el orquestador midió el 2026-09-12», y la §0-bis, la §3 (material) y el Paso 2 repiten «medido el 2026-09-12». Un documento escrito el 11 no puede incorporar mediciones del 12, y la fecha de hoy en esta sesión es 2026-09-11. Alinear las fechas al escribir el acta.
- **Estado tras la ronda correctiva 1:** los cuatro sitios que nombra el lente (encabezado, §0-bis, §3 y Paso 2) **ya quedaron en 2026-09-11**. Siguen escritas dos menciones al 2026-09-12 que **no** son error de fecha del plan: el nombre real del respaldo de la Pi (`config.json.bak-2026-09-12`) y el ejemplo de nombre de acta del Paso 14 (ver **F-111**).
- **Estado:** abierta (solo para revisarlo al escribir el acta).

---

## F-093 · El `sudo rm -f /dev/usb/lp0` del Paso 7 va sin guarda y se puede pegar por error sobre el dispositivo real

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 7, SI FALLA, punto 2.
- **Qué pasa (texto del lente, tal cual):** Paso 7, SI FALLA, punto 2: `ssh ruleta 'sudo rm -f /dev/usb/lp0'` va sin guarda. La rama está bien explicada (solo si la primera letra de `ls -l` es `-`), pero el comando se puede pegar por error sobre el dispositivo real. Sería a prueba de pegado: `ssh ruleta 'test -c /dev/usb/lp0 && echo ES_DISPOSITIVO_NO_BORRAR || sudo rm -f /dev/usb/lp0'`.
- **Relacionada con:** **F-090** (el `O_CREAT` de `ImpresoraArchivo`, que es lo que crea ese archivo falso).
- **Estado:** abierta.

---

## F-094 · El plan deshabilita CUPS y ModemManager de forma permanente sin decir cómo revertirlo

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 3 rama B2 y Paso 10 punto 2.
- **Qué pasa (texto del lente, tal cual):** Paso 3 rama B2 y Paso 10 punto 2 deshabilitan servicios del sistema de forma permanente (`sudo systemctl disable --now cups cups-browsed`, `sudo systemctl disable --now ModemManager`) sin decir cómo revertirlo ni pedir que quede anotado en el acta como cambio de sistema.
- **Estado:** abierta.

---

## F-095 · Anclas del plan con desfase de una línea (lista del primer lente)

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, decisión D7, §5 trampas 1, 4 y 17, §0-bis H5 y §6 (mapa de anclas).
- **Qué pasa (texto del lente, tal cual):** Anclas con desfase de una línea (no rompen nada, pero el mapa de anclas manda re-grep): el `[--] … no se prueba Bluetooth` está en `ruleta/__main__.py:344` (D7 y §5 trampa 1 dicen 343; el mapa de anclas sí dice 344); `ImpresoraArchivo` abre el archivo en `escpos.py:562` (trampa 4 dice 560); `crear_impresora` construye `ImpresoraArchivo` en `app.py:57` (H5 dice 56, que es el `if`); el valor por defecto `cancelar_modo_chino=True` está en `escpos.py:131` (trampa 17 cita la 34, que es `CMD_CANCELAR_KANJI`).
- **Relacionada con:** **F-108** y **F-109**, que traen la misma familia de desfases medidos por el otro lente y **no coinciden en un número** (aquí `escpos.py:562` para la apertura del archivo; en F-108, la 561 para el modo `"ab"`). Antes de tocar cualquiera de esas líneas hay que volver a medir, que es justo lo que ordena la §6 del plan.
- **Estado:** abierta.

---

## F-096 · D7 y la trampa 1 dicen que `cmd_diagnostico` «devuelve 0 sin abrir la ruta», y puede devolver 1 por otras causas

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, decisión D7 y §5 trampa 1; `ruleta/__main__.py`, `cmd_diagnostico`.
- **Qué pasa (texto del lente, tal cual):** D7 y §5 trampa 1 dicen que `cmd_diagnostico` «devuelve 0 sin abrir la ruta»; el código hace `return 0 if ok else 1`, así que puede devolver 1 por otras causas (datos, PIL, logo, inventario). El acta de la Fase 1 lo redacta mejor: «devuelve 0 en cuanto pasan los demás [ok]».
- **Estado:** abierta.

---

## F-097 · El Paso 1 corre las pruebas con `tail -n 3` y su tabla de criterios las cita con `tail -n 1`

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 1 punto 5 y tabla de CRITERIO DE ACEPTACIÓN del Paso 1.
- **Qué pasa (texto del lente, tal cual):** Paso 1 punto 5 corre las pruebas con `tail -n 3` y la tabla de criterios cita `unittest … | tail -n 1`. Conviene usar el mismo comando en los dos sitios.
- **Estado:** abierta.

---

## F-098 · La tabla del Paso 1 exige el commit `601c4c2` sin la rama «si no hubo internet se queda en 2052e47»

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 1, tabla de CRITERIO DE ACEPTACIÓN (fila `git rev-parse HEAD`) frente a su SI FALLA.
- **Qué pasa (texto del lente, tal cual):** Paso 1, tabla de criterios: `git rev-parse HEAD` → `601c4c2…` no lleva la rama «si no hubo internet se queda en 2052e47», que sí está en SI FALLA. La tabla sola se lee como un criterio que va a fallar. (Verificado: `origin/main` = `601c4c2b64fc93e2a76b539f2b79fee9e1f91843`, así que el `pull` sí puede llegar ahí.)
- **Estado:** **cerrada** el 2026-09-11 con la medición del deploy: la Pi estaba efectivamente en `2052e47` —la rama que esta ficha pedía escribir, no en `601c4c2`—; el `git pull --ff-only` la llevó a `61adf96` y la §6 del plan ya no presenta `601c4c2` como el commit esperado.

---

## F-099 · D3 y el Paso 0 exigen 2.4 GHz y la PC comparte la radio que ya está asociada en 5 GHz

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, decisión D3 y Paso 0.
- **Qué pasa (texto del lente, tal cual):** D3 y Paso 0 exigen banda 2.4 GHz en el punto de acceso, pero la PC comparte la misma radio (Intel AX211) que está asociada a `FDA806_5G` en 5 GHz; algunos controladores no dejan fijar una banda distinta a la de la conexión. Falta la rama «si Windows no deja elegir 2.4 GHz, dejar Cualquiera disponible» (la Pi 5 es de doble banda).
- **Estado:** abierta.

---

## F-100 · El `ipconfig | grep` del Paso 0 puede no casar por la página de códigos OEM de la consola

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 0, SI FALLA.
- **Qué pasa (texto del lente, tal cual):** Paso 0, SI FALLA: `ipconfig | grep -A 5 -i "punto de acceso\|Local Area Connection"` puede no casar por la página de códigos OEM de la consola en Git Bash (los acentos y la ñ). El `arp -a | grep 192.168.137` de la línea siguiente es el que realmente sirve.
- **Estado:** abierta.

---

## F-101 · El punto de acceso con el mismo nombre y contraseña atraerá a los celulares que conozcan el Wi-Fi del asadero

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 0 y §5 trampa 19.
- **Qué pasa (texto del lente, tal cual):** Paso 0 no avisa de un efecto lateral del punto de acceso con el mismo nombre y contraseña: cualquier equipo que conozca el Wi-Fi del asadero (el celular del usuario, el del personal) se conectará solo a la PC y saldrá a internet por ella. Vale una línea junto a la trampa 19.
- **Estado:** abierta.

---

## F-102 · El golden `stat` de la §7.3 no distingue si la regla `udev` del Paso 4 funcionó

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, §7.3 (goldens del dispositivo USB).
- **Qué pasa (texto del lente, tal cual):** §7.3: el golden `stat -c "%a %U %G" /dev/usb/lp0` → `660 root lp` no distingue si la regla del Paso 4 funcionó, porque ese es también el valor por defecto esperado. El que sí lo distingue es `test -c /dev/impresora-ruleta` → `ENLACE_OK`; conviene decirlo.
- **Estado:** abierta.

---

## F-103 · Los tres respaldos que el plan deja en el `$HOME` de la Pi no tienen destino al cerrar la fase

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Pasos 5, 8 y 10 (los `cp` de respaldo) y Paso 14 (cierre).
- **Qué pasa (texto del lente, tal cual):** El plan crea tres respaldos en el `$HOME` de la Pi (`~/config.json.antes-de-fase2`, `~/config.json.medido-fase2`, `~/config.json.antes-de-bluetooth`) y nunca dice qué hacer con ellos al cerrar la fase (dejarlos, listarlos en el acta o borrarlos tras verificar el hash).
- **Estado:** abierta.

---

## F-104 · F-013 sigue vigente y afecta al Paso 11: el plan no nombra las rutas de `docs/` que hay que commitear

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 11 («la lista de rutas acordada por adelantado»).
- **Qué pasa (texto del lente, tal cual):** Sigue vigente F-013 y afecta al Paso 11: hoy `docs/planes/fase-2-impresora.md`, `docs/actas/2026-09-11-hechos-medidos.md` y `docs/PAUSA-2026-09-11.md` salen como `??` en `git status`, y `docs/fichas.md` como ` M`. El Paso 11 habla de «la lista de rutas acordada por adelantado» pero no nombra estas rutas, y sin ellas el propio plan no llega a la Pi con el `git pull`.
- **Relacionada con:** **F-013** (la carpeta `docs/` todavía no está versionada) y **F-115**, que dice lo mismo desde el lado del archivo de hechos medidos.
- **Estado:** abierta.

---

## F-105 · F-055 y F-056 siguen aplicando: el plan y su acta se publican en un repositorio público

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md` (Paso 0, §0-bis) y el acta que cerrará esta fase.
- **Qué pasa (texto del lente, tal cual):** F-055/F-056 siguen aplicando a esta fase: el plan y su acta se publican en un repositorio público y ya contienen hostname, rango de red del punto de acceso y la existencia de `sudo` sin contraseña. El plan hace bien en excluir la contraseña del Wi-Fi; conviene que el acta repita esa exclusión explícitamente.
- **Relacionada con:** **F-055** y **F-056**.
- **Estado:** abierta.

---

## F-106 · El Paso 6 cita `Configuracion:` sin tilde y el código imprime `Configuración:`

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 6 (bloque de salida esperada del diagnóstico); `ruleta/__main__.py`.
- **Qué pasa (texto del lente, tal cual):** Paso 6, bloque de salida esperada del diagnóstico: dice `Configuracion: /home/asadero/ruleta/config.json` y el código imprime `Configuración:` con tilde (`ruleta/__main__.py`, `print(f"Configuración: {args.config}")`). El archivo de hechos también lo trae sin tilde porque está escrito entero sin acentos. No es golden (los de la §7.5 cuentan con `grep -c`), así que no bloquea.
- **Relacionada con:** **F-084** y **F-107** (misma familia: mensajes del programa citados sin acentos).
- **Estado:** abierta.

---

## F-107 · El Paso 1 cita el mensaje del log sin tilde (`Falta la direccion Bluetooth…`)

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 1 punto 1; `ruleta/app.py`.
- **Qué pasa (texto del lente, tal cual):** Paso 1, punto 1: cita el log como `ERROR de configuración: Falta la direccion Bluetooth de la impresora...`; el mensaje real de `ruleta/app.py` es `Falta la dirección Bluetooth de la impresora: pon la MAC real en impresora.mac de config.json (la obtienes con herramientas/emparejar.sh)`, con tilde en «dirección». Mismo tema que la ficha F-084.
- **Relacionada con:** **F-084** y **F-106**.
- **Estado:** abierta.

---

## F-108 · Anclas del plan con desfase de una línea (lista del segundo lente)

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, §0-bis H5, §5 trampas 1, 4 y 17, y §6 (mapa de anclas).
- **Qué pasa (texto del lente, tal cual):** Anclas con desfase de una línea (el `grep` de la §6 las encuentra igual): §0-bis H5 y §5 trampa 1 dicen `ruleta/app.py` línea 56, y la construcción `ImpresoraArchivo(imp.ruta, anexar=True)` está en la 57 (la 56 es el `if tipo == "archivo":`); §5 trampa 4 dice `escpos.py` línea 560 y el modo `"ab"` está en la 561; §5 trampa 17 dice `escpos.py` línea 34 y `CMD_CANCELAR_KANJI` está en la 33 (la llave `cancelar_modo_chino`, en la 131); el mapa de anclas dice `CMD_ESTADO_*` en 54-57 y son 54-57 contando `_VALOR_FIJO_ESTADO` (57), correcto.
- **Relacionada con:** **F-095** (misma familia; discrepan en un número: allí la apertura de `ImpresoraArchivo` se sitúa en la 562 y aquí el modo `"ab"` en la 561). **Re-grep antes de tocar nada.**
- **Estado:** abierta.

---

## F-109 · La §6 dice «hoy 344» y la trampa 1 y D7 dicen «línea 343» para la misma salida del diagnóstico

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, §6 fila «Salida temprana del diagnóstico», §5 trampa 1 y decisión D7.
- **Qué pasa (texto del lente, tal cual):** §6, fila «Salida temprana del diagnóstico»: dice «hoy 344» y la §5 trampa 1 y la decisión D7 dicen «línea 343»; la línea real del `print` es la 344 y el `if` que lo gobierna la 343. Es la misma incoherencia interna de una línea.
- **Relacionada con:** **F-095** y **F-108**.
- **Estado:** **cerrada** el 2026-09-11 (Paso 14): la incoherencia desapareció al refrescar la §6. Ni el mapa de anclas, ni la §5 trampa 1, ni la decisión D7 citan ya un número de línea para esa salida: la sub-fase 2b la borró y el `grep` no devuelve nada.

---

## F-110 · El Paso 1 dice «los tres goldens» y lista seis comandos

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 1 punto 3.
- **Qué pasa (texto del lente, tal cual):** Paso 1, punto 3: dice «los tres goldens que la Fase 1 dejó sin medir» y lista seis comandos (`SubState`, `Timezone`, `NTP`, `NTPSynchronized`, `LocalRTC`, `date`). El número no cuadra con la lista, aunque los goldens no medidos de la Fase 1 sí son tres.
- **Estado:** abierta.

---

## F-111 · Menciones sueltas al «2026-09-12» que no son criterio ni comando y no se corrigieron

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, §0-bis H9 y Paso 1 (nombre del respaldo) y Paso 14 (ejemplo de nombre de acta).
- **Qué pasa (texto del lente, tal cual):** Quedan otras menciones sueltas a «2026-09-12» que no corrijo aquí por no ser criterio ni comando: el respaldo real de la Pi se llama `config.json.bak-2026-09-12` (nombre con la fecha equivocada, así lo anota el archivo de hechos) y el Paso 14 ejemplifica el acta como `docs/actas/2026-09-12-fase-2.md`; si la fase se cierra el 2026-09-11 el acta se llamará `docs/actas/2026-09-11-fase-2.md` y chocará con `2026-09-11-fase-1.md` solo en la fecha, no en el nombre.
- **Relacionada con:** **F-092**.
- **Estado:** abierta.

---

## F-112 · El Paso 8 dice «si no suena es el DIP, no el programa» y el zumbador ya está medido

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 8, apartado «Zumbador»; §0-bis H9.
- **Qué pasa (texto del lente, tal cual):** Paso 8, apartado «Zumbador»: dice «si no suena es el DIP, no el programa». Ya está medido lo contrario (§0-bis H9): `ESC B` **sí** suena por USB, pero da **un pitido corto por comando** e ignora los parámetros `n` y `t`. Conviene incorporarlo cuando se toque ese apartado.
- **Estado:** abierta.

---

## F-113 · El Paso 8 no menciona que las líneas de acentos del boleto de prueba se parten en el papel

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 8; `ruleta/ticket.py`, `boleto_prueba`.
- **Qué pasa (texto del lente, tal cual):** Paso 8 no menciona el hallazgo cosmético ya medido: las cuatro líneas de acentos del boleto de prueba pasan de 48 columnas y se parten en el papel. Es candidato a ficha y a un arreglo de `ticket.boleto_prueba` en 2b.
- **Estado:** **resuelta** el 2026-09-11 (2b, cambio (f) + bitácora del plan). El boleto de prueba imprime la etiqueta (`  ESC t 19 (cp858):`) en una línea y la muestra de acentos en la siguiente, así que ninguna pasa de 48 columnas; hay golden en `tests/test_ticket.py` que compara el bloque entero por igualdad y comprueba a 32, 42 y 48 columnas. Y la bitácora del Paso 8 ya lo anota como cosmético medido esa noche. **Comprobado en papel el 2026-09-11 ~23:20:** el usuario corrió la reprueba post-2b y confirmó que las cuatro tablas de acentos salen **en dos renglones, sin partirse** (ficha **F-188**, cerrada). *(Hasta ese momento solo estaba el boleto de las 19:25, impreso con el código viejo.)*
---

## F-114 · El golden `"canal": 1` de la §7.11 fija un canal que decide el diagnóstico

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, §7.11 (goldens del respaldo Bluetooth) y Paso 10.
- **Qué pasa (texto del lente, tal cual):** §7.11 (respaldo Bluetooth) fija el golden `"canal": 1` con la MAC de ejemplo `AA:BB:CC:DD:EE:FF`; el canal real lo decide el diagnóstico y puede no ser 1. Como el Paso 10 solo se hace si el USB falla, y hoy el USB funciona, no bloquea.
- **Estado:** abierta.

---

## F-115 · El archivo de hechos medidos que cita el plan existe y está sin commitear

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 1
- **Dónde:** `docs/actas/2026-09-11-hechos-medidos.md`, `docs/planes/fase-2-impresora.md`, `docs/PAUSA-2026-09-11.md`.
- **Qué pasa (texto del lente, tal cual):** El plan cita `docs/actas/2026-09-11-hechos-medidos.md` como «hechos crudos» y ese archivo existe y está sin commitear (`?? docs/actas/2026-09-11-hechos-medidos.md`), igual que el propio plan y `docs/PAUSA-2026-09-11.md`. El agente de commit tendrá que incluirlos en la lista de rutas (ficha F-013 sigue vigente).
- **Relacionada con:** **F-013** y **F-104**.
- **Estado:** abierta.

---

## F-116 · El Paso 5, SI FALLA, citaba un `assert` que el script del punto 3 ya no tiene

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 5, SI FALLA (primera viñeta) y Paso 5 punto 3 (bloque `python3 - <<"PY"`).
- **Qué pasa (texto del lente, tal cual):** Paso 5, SI FALLA, primera viñeta: dice «El `assert` se dispara (`no hay exactamente una linea de tipo`)», pero el script del punto 3 ya no tiene ningún `assert` ni ese mensaje: termina con `raise SystemExit("config.json no esta en ninguno de los tres estados previstos: parar y preguntar")`. El remedio (detenerse y preguntar) es el mismo, así que no bloquea; conviene citar el mensaje real. (Parece resto de la reescritura de la ronda 1, que pasó el script a tres estados.)
- **Estado:** **cerrada** en esta misma ronda correctiva (f2 · ronda 2, corrección 5): la viñeta ya cita el mensaje real del script.

---

## F-117 · El encabezado §Tiempos manda subir el límite en un «bucle de espera del Paso 13» que no existe

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §Tiempos (`grep -n "600000" docs/planes/fase-2-impresora.md`) y Paso 13 (`sleep 8`); `docs/planes/fase-1-preparar-pi.md`, Paso 12.
- **Qué pasa (texto del lente, tal cual):** Encabezado §Tiempos: «solo hay que subirlo (a 600000) en el bucle de espera del Paso 13 si hubiera que reiniciar la Pi». El Paso 13 no reinicia la Pi ni tiene bucle de espera (solo `sleep 8`); el único reinicio del proyecto es el Paso 12 de la Fase 1. La referencia sobra o debería apuntar a ese otro paso.
- **Estado:** abierta.

---

## F-118 · La regla `udev` del Paso 4 se puede pegar con `@VID@` y `@PID@` sin sustituir y el golden no lo delata

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 4 punto 2.b (bloque que escribe `/etc/udev/rules.d/61-ruleta-impresora.rules`) y §7.3 (goldens del dispositivo USB).
- **Qué pasa (texto del lente, tal cual):** Paso 4, punto 2.b: la regla se escribe con los marcadores `@VID@` y `@PID@`. Si un ejecutor la pega sin sustituir, el archivo queda escrito y el golden `grep -c idVendor` sigue dando 1: lo único que lo delata es `test -c /dev/impresora-ruleta`. Refuerza la ficha F-102; se podría añadir un golden `grep -c '@VID@' /etc/udev/rules.d/61-ruleta-impresora.rules` → 0.
- **Relacionada con:** **F-102** (el golden `stat` tampoco distingue si la regla funcionó) y **F-130**.
- **Estado:** abierta.

---

## F-119 · El SSID `FDA806_5G` de §0-bis H1 y del Paso 0 es dato de sesión, no hecho medido

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §0-bis H1 y Paso 0 punto 2; `scratchpad/hechos-fase-1.md`.
- **Qué pasa (texto del lente, tal cual):** §0-bis H1 y Paso 0 punto 2 afirman que la PC está conectada a `FDA806_5G`. Ese SSID no aparece en el archivo de hechos medidos de la sesión (`hechos-fase-1.md`), que sí registra la red de la Pi («netplan-wlan0-SDV 5G»). Es dato de sesión, no de hechos: conviene medirlo y anotarlo, o marcarlo como no medido. Toca también la ficha F-099.
- **Relacionada con:** **F-099** y **F-126** (el otro lente levanta el mismo hallazgo cotejándolo contra los archivos del repositorio).
- **Estado:** abierta.

---

## F-120 · El criterio `git status --porcelain | wc -l` → `1` del Paso 1 da por hecho que el `git pull` funcionó

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 1, tabla de CRITERIO DE ACEPTACIÓN, frente a su SI FALLA.
- **Qué pasa (texto del lente, tal cual):** Paso 1, tabla de criterios: `git status --porcelain | wc -l` → `1` da por hecho que el `git pull` funcionó. Si no hubo internet (rama ya prevista en SI FALLA), HEAD se queda en `2052e47`, el `chmod +x` obligatorio vuelve a ensuciar `instalar.sh` y `herramientas/emparejar.sh`, y el conteo será `3`. Amplía la ficha F-098 al conteo, no solo al `rev-parse`.
- **Relacionada con:** **F-098** (misma rama «si no hubo internet», allí sobre `git rev-parse HEAD`).
- **Estado:** abierta.

---

## F-121 · Comprobado y correcto en la ronda 2: el intérprete de esta PC y las anclas del §6 (para no volver a auditarlas)

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 11, §7.12 y §6 (mapa de anclas).
- **Qué pasa (texto del lente, tal cual):** Comprobado y correcto (para que nadie lo vuelva a auditar en la Fase 2): `python` en esta PC es `/c/Python314/python` (Python 3.14.4) y `python3` es el atajo de la Microsoft Store que contesta «Python was not found» —la nota del Paso 11 y de la §7.12 es exacta—; y las anclas del §6 casan hoy: app.py 46/56/115/268, escpos.py 34/43/50/54-57/67/546, __main__.py 87/211/227/266/375 y el `if` de 343 con su `print` en 344, `grep -c "[ok]"` = 6, config.json con una sola línea `"tipo": "bluetooth"` (16), sin `ruta` y con 7 premios `test`, instalar.sh 36-38/50/67, ruleta.service 13, README 78/87/153/225/255/429. Las fichas F-095, F-108 y F-109 siguen siendo solo desfases de una línea.
- **Relacionada con:** **F-095**, **F-108** y **F-109** (los desfases de una línea que este cotejo confirma como tales).
- **Estado:** cerrada de entrada (nota de verificación: no hay nada que corregir).

---

## F-122 · Verificados los goldens de bits del cambio (b) del Paso 12 contra `ruleta/escpos.py`

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 12, cambio (b) y sus goldens; `ruleta/escpos.py` y el test `test_archivo_con_papel_escribe_todo`.
- **Qué pasa (texto del lente, tal cual):** Verificado que los goldens de bits del cambio (b) del Paso 12 son correctos contra `ruleta/escpos.py`: 0x72 y 0x16 y 0x1a pasan la máscara fija 0x93/0x12, 0x72 casa `& 0x60` (sin papel), 0x16 casa `& 0x0C` (poco papel) y 0x1a casa `& 0x08` (fuera de línea); el orden papel→impresora del test `test_archivo_con_papel_escribe_todo` coincide con el del código (líneas 415-422). No hay nada que corregir ahí.
- **Estado:** cerrada de entrada (nota de verificación: no hay nada que corregir).

---

## F-123 · Verificada la afirmación de seguridad del Paso 13: «es seguro arrancar sin botones»

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 13; `config.json`; `ruleta/config.py` (líneas 84-85 y 309-312).
- **Qué pasa (texto del lente, tal cual):** Verificada la afirmación de seguridad del Paso 13 («es seguro arrancar sin botones»): `config.json` trae `modo_habilitar: "mantener"` y `pull_up: true`, y `config.py` (líneas 84-85, 309-312) los valida; con los pines al aire el botón se lee como no presionado. Correcto.
- **Estado:** cerrada de entrada (nota de verificación: no hay nada que corregir).

---

## F-124 · Las fichas F-092 a F-115 de la ronda 1 siguen abiertas y sin cambio

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/fichas.md`, F-092 a F-115; acta de cierre de la Fase 2 (Paso 14).
- **Qué pasa (texto del lente, tal cual):** Siguen abiertas y sin cambio las fichas F-092 a F-115 de la ronda 1; ninguna alcanza la PARADA y todas quedan anotadas para el acta.
- **Estado:** abierta.

---

## F-125 · El Paso 3 lista `0416:5011` entre los «valores típicos» y el VID:PID medido es `0418:5011`

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 3 (`grep -n "0416" docs/planes/fase-2-impresora.md`) y §0-bis H2.
- **Qué pasa (texto del lente, tal cual):** Paso 3: la lista de «valores típicos de la familia» incluye `0416:5011`, que difiere en un dígito del VID:PID realmente medido (`0418:5011`, §0-bis H2). Riesgo de copiar el equivocado a la regla udev; convendría poner el medido primero y marcar los demás como pistas ajenas.
- **Relacionada con:** **F-118** (la regla del Paso 4 es justo donde ese número acabaría).
- **Estado:** abierta.

---

## F-126 · El SSID `FDA806_5G` es el único dato de §0-bis H1 sin respaldo en el archivo de hechos

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §0-bis H1; `docs/actas/2026-09-11-hechos-medidos.md`; `docs/PAUSA-2026-09-11.md`; `docs/fichas.md`, F-099.
- **Qué pasa (texto del lente, tal cual):** §0-bis H1 afirma como hecho medido que la PC está conectada a `FDA806_5G`; ese SSID no aparece en `docs/actas/2026-09-11-hechos-medidos.md` ni en `docs/PAUSA-2026-09-11.md` (solo se repite en la ficha F-099). Es el único dato de H1 sin respaldo en el archivo de hechos.
- **Relacionada con:** **F-119** (el mismo hallazgo por el otro lente, cotejado contra `hechos-fase-1.md`) y **F-099**.
- **Estado:** abierta.

---

## F-127 · Documentos vecinos quedaron viejos: la Fase 1 y su acta dicen que `docs/planes/fase-2-impresora.md` «aún no existe»

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-1-preparar-pi.md` §9; `docs/actas/2026-09-11-fase-1.md` §7; `docs/fichas.md`, F-073; `docs/planes/fase-2-impresora.md`, Paso 14 punto 3.
- **Qué pasa (texto del lente, tal cual):** Documentos vecinos quedaron viejos por la existencia de este plan: `docs/planes/fase-1-preparar-pi.md` §9 dice que `docs/planes/fase-2-impresora.md` «aún no existe» y el acta de la Fase 1 §7 lo repite; la ficha F-073 los daba por verificados. Se corrige al cerrar la Fase 2 (Paso 14, punto 3).
- **Relacionada con:** **F-073**, que queda superada por este hallazgo: lo que allí se verificó como cierto dejó de serlo al escribirse el plan de la Fase 2.
- **Estado:** abierta.

---

## F-128 · La §7.12 corre las pruebas en la PC sin que esté medido si esta PC tiene Pillow

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §7.12 (goldens de la sub-fase 2b) y Paso 12.
- **Qué pasa (texto del lente, tal cual):** §7.12 manda correr `python -m unittest discover -s tests -t .` en la PC, pero no está medido que esta PC tenga Pillow instalado; si falta, las pruebas podrían fallar por entorno y no por el cambio de 2b. (Sí está verificado que en esta PC `python` es C:/Python314/python 3.14.4 y que `python3` es el atajo de la Microsoft Store, tal como dice el plan.)
- **Relacionada con:** **F-121** (donde se verifica la parte del intérprete).
- **Estado:** abierta.

---

## F-129 · El bucle de diferencias del Paso 11 solo recorre las llaves de primer nivel

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 11 punto 3 (bloque `python - <<"PY"` que compara los dos `config.json`).
- **Qué pasa (texto del lente, tal cual):** Paso 11, punto 3: el bucle de diferencias solo recorre las llaves de primer nivel, así que una diferencia dentro de `impresora` se reporta como «difiere: impresora -> {...} | {...}» sin señalar la llave concreta. El veredicto `IGUALES`/`DISTINTOS` sí es exacto; el detalle es solo poco legible.
- **Estado:** abierta.

---

## F-130 · La «Regla de emergencia sin VID:PID» del Paso 4 deja el golden `grep -c idVendor` en `0`

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 4 («Regla de emergencia sin VID:PID») y §7.3.
- **Qué pasa (texto del lente, tal cual):** Paso 4, «Regla de emergencia sin VID:PID»: deja `grep -c idVendor … → 0`, excepción ya contemplada en la §7.3. Sin conflicto, pero conviene que el acta cruce ambos sitios si se usa.
- **Relacionada con:** **F-118** y **F-102**.
- **Estado:** abierta.

---

## F-131 · §5 trampa 4 y §6 siguen citando `escpos.py` línea 560 y hoy la apertura está en la 562

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §5 trampa 4 y §6 (mapa de anclas); `ruleta/escpos.py`.
- **Qué pasa (texto del lente, tal cual):** §5 trampa 4 y §6 siguen citando `escpos.py` línea 560 para el modo `"ab"`; medido hoy la apertura está en la 562. Es la familia de desfases ya recogida en F-095/F-108, que además discrepan entre sí en un número: re-grep obligatorio antes de tocar esas líneas.
- **Relacionada con:** **F-095** y **F-108** (misma familia, y discrepan entre sí en un número). **Re-grep obligatorio antes de tocar esas líneas.**
- **Estado:** **cerrada** el 2026-09-11 (Paso 14). Las dos referencias se refrescaron contra `61adf96`: la §5 trampa 4 cita ahora `ruleta/escpos.py` 671-673 y explica los dos modos de apertura (`r+b` cuando toca preguntar por el papel, `ab`/`wb` en los demás casos), y la §6 sitúa la clase en la 603.

---

## F-132 · Verificados los anclajes de `instalar.sh`, `ruleta.service`, `emparejar.sh`, `config.py`, `escpos.py`, README y los mensajes de log del Paso 13

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §6 (mapa de anclas), §7.5, §7.7 y Paso 9.
- **Qué pasa (texto del lente, tal cual):** Verificado y correcto (no requiere acción): los anclajes de `instalar.sh` (2/6 en 36, `usermod` 37-38, regla udev en 50, `systemctl enable` en 67), `ruleta.service` (`SupplementaryGroups=gpio` en 13), `emparejar.sh` (`read -rp` en 55, bloque JSON 124-136, `tipo` en 131), `config.py` (`ConfigImpresora` en 53, `ruta` en 57, `validar` en 266), `escpos.py` (43, 50, 54-57, 67, 546), README (78, 87/92, 153, 225, 255, 429) y los mensajes de log del Paso 13 (`__main__.py` 142, `hardware.py` 83, `app.py` 115 y 268). Los conteos 6/7/9 de las §7.5, §7.7 y del Paso 9 se derivan bien del código y de `config.json`.
- **Estado:** cerrada de entrada (nota de verificación: no hay nada que corregir).

---

## F-133 · Verificado: la bitácora §0 está enteramente sin marcar, coherente con su propio texto

- **Fecha:** 2026-09-11
- **Origen:** lentes f2 ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §0 (Bitácora).
- **Qué pasa (texto del lente, tal cual):** La bitácora §0 está enteramente sin marcar, coherente con el texto que dice que se marca el día en que se corra el plan: no hay casillas marcadas sin evidencia.
- **Estado:** cerrada de entrada (nota de verificación: no hay nada que corregir).

---

## F-134 · §0-bis H3 da por hecho el modelo «Zjiang ZJ-80250» y el `ieee1284_id` medido no lo confirma

- **Fecha:** 2026-09-11
- **Origen:** escéptico f2
- **Dónde:** `docs/planes/fase-2-impresora.md`, §0-bis H3 (`grep -n "ZJ-80250" docs/planes/fase-2-impresora.md`) y Paso 3; `docs/actas/2026-09-11-hechos-medidos.md`.
- **Qué pasa (texto del escéptico, tal cual):** §0-bis H3 afirma como hecho que la unidad «es una Zjiang ZJ-80250» a partir del PPD del driver que descargó el usuario; el `ieee1284_id` realmente medido es `MFG:Printer;CMD:EPSON;MDL:POS-80;CLS:PRINTER;1`, que no lo confirma. El Paso 3 sí lo matiza; convendría matizarlo ya en H3.
- **Por qué es residual:** ningún comando ni criterio del plan depende del nombre comercial; H3 se usa para deducir que hay cortador, zumbador y `DLE EOT 1`, y esas tres cosas ya están medidas por separado (§0-bis H9). Es una etiqueta de confianza de más, no un dato que mueva un paso.
- **Estado:** abierta.

---

## F-135 · El `sudo dmesg | tail -n 30` del Paso 3 puede no traer la enumeración de la impresora

- **Fecha:** 2026-09-11
- **Origen:** escéptico f2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 3, bloque «QUÉ HACER — medición común (siempre)» (`grep -n "dmesg" docs/planes/fase-2-impresora.md`).
- **Qué pasa (texto del escéptico, tal cual):** Paso 3: `sudo dmesg | tail -n 30` puede no contener la enumeración de la impresora si lleva conectada desde el arranque y hubo mensajes posteriores (que es justo el estado descrito en H2/H9). `sudo dmesg | grep -iE "usblp|usb 1-" | tail -n 20` es más fiable para lo que se busca.
- **Por qué es residual:** no bloquea porque la línea `usblp0: ...` que se busca en `dmesg` es informativa: quien decide la rama del Paso 3 es `ls -l /dev/usb/`. Si `dmesg` no la trae, el ejecutor se queda sin la confirmación bonita, no sin el dato.
- **Estado:** abierta.

---

## F-136 · El bloque de Python del Paso 11 abre `config.json` con ruta relativa y no dice desde dónde correrlo

- **Fecha:** 2026-09-11
- **Origen:** escéptico f2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 11 punto 3 (bloque `python - <<"PY"`).
- **Qué pasa (texto del escéptico, tal cual):** Paso 11, punto 3: el bloque de Python abre `config.json` con ruta relativa; no dice explícitamente que hay que correrlo desde la raíz del repositorio de la PC (a diferencia de los comandos de la Pi, que sí llevan `cd ~/ruleta`).
- **Por qué es residual:** si se corre desde otra carpeta el intento revienta con `FileNotFoundError`, que es ruidoso e inequívoco: no puede pasar por bueno un `IGUALES` falso.
- **Estado:** abierta.

---

## F-137 · Verificado y correcto en la ronda del escéptico: vectores de estado, conteos del Paso 9 y §7.7, el commit `601c4c2b64…` y los anclajes de README, `instalar.sh`, `emparejar.sh` y `ruleta.service`

- **Fecha:** 2026-09-11
- **Origen:** escéptico f2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 12 cambio (b), Paso 9, §7.7, Paso 1 y §6 (mapa de anclas); `ruleta/escpos.py`, `ruleta/ticket.py`, `ruleta/__main__.py`, `config.json`, `tests/`.
- **Qué pasa (texto del escéptico, tal cual):** Verificado y correcto, para que nadie lo vuelva a auditar: los vectores de los goldens de 2b(b) coinciden con `ruleta/escpos.py` (`_MASCARA_FIJA_ESTADO=0x93`, `_VALOR_FIJO_ESTADO=0x12`, papel `& 0x60` sin papel, papel `& 0x0C` poco papel, estado `& 0x08` fuera de línea, `timeout_estado=1.0`, orden PAPEL→IMPRESORA en `_verificar_lista`); los conteos del Paso 9 y de la §7.7 se derivan bien (7 premios `test*` en `config.json`; 9 documentos con `[CORTE]` = 7 premio + consuelo + inventario, `ticket.py:94` dentro del cierre común); `grep -c "[ok]" ruleta/__main__.py` da 6; `601c4c2b64fc93e2a76b539f2b79fee9e1f91843` existe, es el cierre de Fase 1, coincide con `origin/main`, su `config.json` trae `"tipo": "bluetooth"` sin `"ruta"`, y `git ls-files -s` da `100755` para `instalar.sh` y `herramientas/emparejar.sh`; el único test que lee `config.json` (`test_config_json_del_proyecto_es_valido`) solo comprueba 7 premios y un stock, así que `tipo archivo` + `ruta` no rompe la suite; los anclajes de README (78, 87, 153, 225, 255, 429), `instalar.sh` (36-38, 50, 67, 69), `emparejar.sh` (55, 131) y `ruleta.service` (13) están donde dice el plan.
- **Relacionada con:** **F-121**, **F-122** y **F-132** (mismas notas de verificación; ésta añade lo que aquéllas no cubren: el contenido del commit `601c4c2b64…`, los modos `100755` de `git ls-files -s` y el alcance real de `test_config_json_del_proyecto_es_valido`).
- **Estado:** cerrada de entrada (nota de verificación: no hay nada que corregir).
## F-138 · El servicio se reiniciaba en bucle para siempre por un error de configuración

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · medición en la Pi la noche del 2026-09-11
  (`docs/actas/2026-09-11-hechos-medidos.md`, sección «Noche del 2026-09-11»)
- **Dónde:** `ruleta.service` (`Restart=always`, `StartLimitIntervalSec=0`),
  `ruleta/app.py` (`crear_impresora`, rechazo de la MAC de relleno) y
  `ruleta/__main__.py` (`cargar_config` e `impresora_desde_args`, que salen con 2).
- **Qué pasa:** al encender la Pi en la ubicación nueva, el servicio arrancó solo
  (estaba `enabled`) con la configuración todavía en Bluetooth y la MAC
  `00:00:00:00:00:00`. El programa sale con código **2** (error de
  configuración), systemd lo reinicia a los 3 s y, como
  `StartLimitIntervalSec=0` quita el freno, el ciclo no termina nunca:
  **118 reinicios** contados antes de que alguien mirara. Un error de
  configuración **no es transitorio**: reintentarlo solo llena el journal y
  esconde el problema real.
- **Qué se hizo:** en la sub-fase 2b se añadió `RestartPreventExitStatus=2` a
  `ruleta.service`. Ahora un error de configuración deja el servicio en
  `failed`, visible con `systemctl status ruleta`, y el `README.md` §9 explica
  qué mirar y cómo volver a arrancarlo. Lo demás (impresora, permisos, GPIO,
  inventario ocupado) sale con otro código y **sigue reintentándose**, que es lo
  que se quiere. Hay goldens en `tests/test_instalacion.py` que atan las dos
  cosas: leen el número de `RestartPreventExitStatus` del propio `.service` y
  comprueban que el programa sale con ese código ante una configuración
  inválida, y con otro ante un fallo transitorio.
- **Estado:** **resuelta y verificada en la Pi** el 2026-09-11. Tras el deploy, un agente independiente midió: `grep -c RestartPreventExitStatus=2 /etc/systemd/system/ruleta.service` → **1** (la unidad nueva sí llegó al sistema, porque el deploy corrió `instalar.sh` y no solo `git pull`), servicio `active`/`running` con **`NRestarts=0`** y journal del arranque sin un solo `ERROR` ni `Traceback`. El bucle de 118 reinicios quedó como historia previa dentro del journal.

---

## F-139 · La regla `udev` y el enlace de la impresora se llaman distinto que en el plan de la Fase 2

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · sub-fase 2b (contradicción entre el plan y lo medido)
- **Dónde:** `docs/planes/fase-2-impresora.md` Paso 4 (punto 2), Paso 5 y
  goldens §7.3 y §7.4, frente a `instalar.sh` (paso `5/7`) y `config.json`.
- **Qué pasa:** el plan manda escribir
  `/etc/udev/rules.d/61-ruleta-impresora.rules` con
  `SYMLINK+="impresora-ruleta"` y poner `"ruta": "/dev/usb/lp0"`, después de
  **borrar** la regla que se había escrito a mano. La sub-fase 2b hizo lo
  contrario por instrucción del orquestador: conservar los nombres que ya
  funcionan en la Pi (`61-ruleta-impresora-usb.rules`, `/dev/ruleta-impresora`),
  porque el deploy es un `git pull` sobre esa misma Pi y renombrar obligaría a
  tocar a mano `udev`, el enlace y el `config.json` de allá.
- **Riesgo si no se toca:** ninguno funcional. El riesgo es de lectura: quien
  siga el Paso 4 al pie de la letra escribiría una **segunda** regla para el
  mismo dispositivo. Por eso la §7.3 lleva ahora el golden
  `ls /etc/udev/rules.d/ | grep -c impresora` → **1**.
- **Propuesta:** dejarlo como está y que el orquestador confirme. Si prefiriera
  los nombres del plan, son tres líneas —la regla, su `SYMLINK+=` y la `ruta`—
  y se cambian las tres a la vez, con su golden y su deploy.
- **Estado:** **cerrada** el 2026-09-11. El orquestador no pidió volver a los nombres del plan y el deploy salió con los de 2b, así que los buenos son `61-ruleta-impresora-usb.rules` y `/dev/ruleta-impresora`. Verificado en la Pi por un agente independiente: el contenido de la regla coincide **carácter por carácter** con el que escribe `instalar.sh`, `getent group lp` incluye a `asadero` y `/dev/ruleta-impresora` existe. El Paso 4 del plan lleva ahora un aviso de que sus puntos 2.a y 2.b están derogados. Lo que **no** se midió es el golden que evita la regla duplicada (`ls /etc/udev/rules.d/ | grep -c impresora` → 1): eso pasa a la ficha **F-187**.

---

## F-140 · El golden `[ok]` de la Fase 1 pasa a 8, no a 7, y los documentos de la Fase 1 no se tocaron

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · sub-fase 2b
- **Dónde:** `docs/planes/fase-1-preparar-pi.md` §7 y su acta, que fijan
  `diagnostico | grep -c "\[ok\]"` → **6**; `docs/planes/fase-2-impresora.md`
  §6 y §9, que anunciaban **7** después del cambio (c).
- **Qué pasa:** el cambio (c)/(e) no añadió una línea al diagnóstico, sino
  **dos**: la de la ruta del dispositivo y la de la consulta del papel. Con la
  impresora conectada y contestando, el conteo real es **8** (7 si no contesta
  al estado, porque esa línea sale como `[??]`). La §7.5 del plan de la Fase 2
  ya está corregida; el plan y el acta de la **Fase 1** siguen diciendo 6, y
  esos archivos no estaban en el alcance de 2b.
- **Riesgo si no se toca:** que alguien corra el golden viejo, lea 8 donde
  esperaba 6 y crea que hay una regresión.
- **Propuesta:** corregirlo en el cierre de la Fase 2 (Paso 14), junto con el
  acta, en la misma pasada en que se toquen los documentos de la Fase 1.
- **Estado:** **resuelta** el 2026-09-11 ~23:20, en el cierre de la Fase 2. Los documentos de la **Fase 1** llevan ya su **nota fechada**, y **el `6` histórico no se borró** porque era cierto cuando se midió: `docs/planes/fase-1-preparar-pi.md` §7 (dentro del bloque de goldens y en dos de sus notas), §6 (mapa de anclas) y §9, y `docs/actas/2026-09-11-fase-1.md` (tabla de goldens y bajo el Anexo C). Todas dicen lo mismo: desde el commit `61adf96` el diagnóstico imprime **8 `[ok]`** con la impresora USB conectada y respondiendo, y **7** si no responde —o si el servicio `ruleta` está corriendo—. Lo medido en la Pi tras el deploy fueron **7 `[ok]` y un `[??]` de poco papel**: es el cuarto caso, ver **F-186**.

---

## F-141 · Verificado: la suite queda en verde y los goldens nuevos sí muerden

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** toda la suite (`python -m unittest discover -s tests -t .`) y dos
  copias del repositorio mutadas en el scratchpad.
- **Qué pasa:** la suite da **194 pruebas, OK**, que es lo que fija el golden
  §7.12 del plan. Dos pasadas de mutación independientes —una de **22** cambios
  y otra de **26**— dejaron **todas** las mutaciones en rojo: `VID 0418→0419`,
  `PID 5011→5012`, `MODE 0660→0666`, `GROUP lp→plugdev`, borrar el `SYMLINK+=`,
  renombrar la regla a `62-…`, quitar el `usermod -aG lp`,
  `SupplementaryGroups=gpio lp` → `gpio`, borrar o cambiar
  `RestartPreventExitStatus`, `BITS_SIN_PAPEL 0x60→0x06`, dejar
  `es_estado_valido` siempre en `True`, preguntar por el papel **después** de
  escribir, ignorar `consultar_estado`, no pasarlo en `crear_impresora`, tratar
  «no contesta» como fallo, tratar «poco papel» como fatal, marcar «sin papel»
  como `True`, quitar el límite de tiempo (`select`) de la lectura, abrir
  siempre en modo `ab`/`wb`, ignorar los permisos en `revisar_ruta_impresora`,
  marcar el archivo normal como error, quitar el respaldo de `__version__`,
  fijar `escribible=True`, `beep true→false`, `tipo archivo→bluetooth`,
  `ruta→/dev/usb/lp0` y rejuntar etiqueta y muestra en el boleto de prueba.
  Ningún assert nuevo dejó de morder.
- **Por qué es residual:** no hay nada que arreglar. Se anota para que nadie
  repita la medición.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejar constancia; volver a mutar solo si cambia el código que
  cubren esos goldens.
- **Nota de la ronda 2 (lentes 2b ronda 2):** reconfirmado hoy. La suite vuelve
  a dar `Ran 194 tests … OK` con `python -m unittest discover -s tests -t .`,
  igual que el golden §7.12. Y la mutación se repitió **de verdad sobre copias
  del repositorio**, no de memoria: quitar `RestartPreventExitStatus=2` → rojo
  (`Ran 162 tests`, `FAILED (errors=1)`); `VID 0418→0419` en `instalar.sh` →
  rojo (1 failure); `crear_impresora` sin `consultar_estado` → rojo (1 failure);
  preguntar el estado **después** de escribir el boleto → rojo (7 failures). Los
  goldens nuevos muerden.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-142 · Verificado: `instalar.sh` (paso 5/7) no tiene defectos de conducta ni de seguridad, y ningún documento filtra secretos

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `instalar.sh` (paso `5/7`), `ruleta.service`, `README.md` y el
  diff de `docs/`.
- **Qué pasa:** el heredoc de la regla `udev` es `<<'EOF'` (comillas simples),
  así que **no** expande variables; la regla está acotada por
  `SUBSYSTEM=="usbmisc"` + `KERNEL=="lp[0-9]*"` + el VID:PID medido y no toca
  ningún otro nodo; el `usermod -aG lp` va protegido con `getent group lp` y
  `-aG` no saca al usuario de ningún grupo. No hay `cat >>`, ni `rm`, ni
  `chmod 777`: todo lo que escribe usa `cat >` (sobrescribe) o `-aG` (agrega
  sin quitar), o sea que es idempotente. Tampoco hay contraseñas ni la llave
  privada en `README.md`, `instalar.sh`, `ruleta.service` ni en el diff de
  `docs/`: solo se nombra la pública `~/.ssh/id_ruleta.pub`.
- **Por qué es residual:** es una nota de verificación, no un hallazgo.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejar constancia para no repetir la auditoría.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-143 · Verificado: `RestartPreventExitStatus=2` solo atrapa errores de configuración

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `ruleta.service` (`RestartPreventExitStatus=2`), `ruleta/__main__.py`
  y `ruleta/app.py` (todas las salidas con código 2 del demonio).
- **Qué pasa:** rastreadas una por una, las únicas salidas con código 2 son
  `cargar_config` → `ErrorConfig` e `impresora_desde_args` → `ErrorConfig`
  (que con `tipo: archivo` ni siquiera puede dispararse, porque `crear_impresora`
  no valida nada en esa rama). El inventario ocupado sale con **1**, y el GPIO,
  la impresora y la carpeta de datos salen con **1** o no salen: a esos systemd
  los sigue reintentando. La llave hace exactamente lo que promete —no reiniciar
  en bucle por un `config.json` mal escrito— y no deja el kiosco muerto por un
  fallo transitorio.
- **Por qué es residual:** nota de verificación sobre el arreglo de **F-138**.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejar constancia.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-144 · Verificado: la consulta de papel por USB ni bloquea ni fuga descriptores

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `ruleta/escpos.py` (`ImpresoraArchivo._leer_estado`, `imprimir`,
  `consultar_papel`, `verificar_estado`).
- **Qué pasa:** `_leer_estado` pasa **siempre** por
  `self._esperar(f, self.timeout_estado)` (un `select` de 1 s) antes de cada
  `f.read(1)`, así que no hay ninguna lectura sin límite de tiempo. `imprimir` y
  `consultar_papel` abren y usan `with f:`, de modo que el nodo se cierra
  también cuando `verificar_estado` lanza `ErrorConexion` —que no hereda de
  `OSError` y por tanto no se confunde con un fallo de escritura—. Los bytes de
  la consulta no se cuentan en `bytes_enviados`, y eso lo fija el golden
  `test_fallo_a_mitad_no_cuenta_la_consulta`.
- **Por qué es residual:** nota de verificación del cambio (d) de 2b.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejar constancia.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-145 · Hueco de cobertura: `_hay_algo_que_leer` y la rama `archivo` de `cmd_diagnostico` no las ejecuta ninguna prueba

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `ruleta/escpos.py` (`_hay_algo_que_leer`, la implementación real
  con `select`), `tests/test_escpos.py` (`TestImpresoraArchivoUSB`, que inyecta
  `esperar_lectura=disp.hay_datos`) y `ruleta/__main__.py` (`cmd_diagnostico`,
  rama `tipo == "archivo"`).
- **Qué pasa:** la función con `select` no la corre ningún golden, porque todas
  las pruebas de `TestImpresoraArchivoUSB` inyectan un doble. El golden
  `test_cada_lectura_tiene_limite_de_tiempo` comprueba que se **pase**
  `timeout_estado=1.0`, no que `select` limite de verdad. Igual pasa con la rama
  nueva de `cmd_diagnostico`: solo se prueban las tres funciones puras
  (`revisar_ruta_impresora`, `interpretar_estado_papel` y `version_modulo`), no
  el comando; un error de cableado entre ellas —el orden, el `ok = ok and bien`,
  el `return` temprano o el guardia de `servicio_activo()`— no lo vería ningún
  assert.
- **Por qué es residual:** no es un assert que no muerda; es código que ningún
  assert alcanza, y las dos ramas dependen de Linux (`select` sobre un
  dispositivo de caracteres, `systemctl`), que es justo lo que no hay en esta PC.
- **Riesgo si no se toca:** una regresión en el `select` o en el orden del
  diagnóstico se descubriría en la Pi, no en la suite.
- **Propuesta:** cerrarlas en la Pi con los goldens de la §7.5. En la Fase 3,
  valorar una prueba de `cmd_diagnostico` con `os.stat`, `os.access` y
  `subprocess` simulados.
- **Nota de la ronda 2 (lentes 2b ronda 2):** confirmada sin cambios. Sigue sin
  haber un solo assert que ejecute la implementación real de
  `_hay_algo_que_leer` —todas las pruebas inyectan
  `esperar_lectura=disp.hay_datos`— ni la rama `tipo == "archivo"` de
  `cmd_diagnostico`, de la que solo se prueban las tres funciones puras. El
  cableado entre ellas (el orden, el `ok = ok and bien`, el `return` temprano y
  el guardia de `servicio_activo()`) sigue sin verlo ninguna prueba. Se cierra
  en la Pi con los goldens de la §7.5.
- **Estado:** abierta.

---

## F-146 · `tests/test_instalacion.py` deriva `CODIGO_CONFIG` al importar: si falta la llave, 32 pruebas dejan de correr con un error opaco

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `tests/test_instalacion.py`, `UNIDAD = leer_unidad(SERVICIO)`
  (línea 106) y
  `CODIGO_CONFIG = int(dict(UNIDAD["Service"])["RestartPreventExitStatus"])`
  (línea 214), las dos a nivel de módulo.
- **Qué pasa:** si alguien borra `RestartPreventExitStatus` de `ruleta.service`,
  el módulo entero revienta con `KeyError` al importarse: la suite pasa de
  **194** a **162** pruebas y se lee `Ran 162 tests ... errors=1` en vez de una
  falla legible. Muerde —que es lo que importa—, pero el diagnóstico es peor de
  lo necesario. El archivo también importa `PIL` a nivel de módulo; hoy no
  estorba porque existe tanto en la PC como en la Pi.
- **Por qué es residual:** el golden sí queda en rojo; lo malo es la calidad del
  mensaje, no la cobertura.
- **Riesgo si no se toca:** quien rompa el `.service` verá un error de
  importación y creerá que el problema está en las pruebas, no en la unidad.
- **Propuesta:** mover el cálculo dentro del test (o de un `setUpClass`) con un
  `assertIn` previo que diga «falta `RestartPreventExitStatus` en
  `ruleta.service`». Es código de pruebas: cabe en cualquier fase.
- **Estado:** abierta.

---

## F-147 · `tests/test_instalacion.py` está sin añadir a git y un `git commit -a` lo dejaría fuera

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `tests/test_instalacion.py`. Comprobado sin correr `git`: el
  índice (`.git/index`) solo lista `tests/test_app.py`, `tests/test_config.py`,
  `tests/test_escpos.py`, `tests/test_inventario.py` y `tests/test_ticket.py`.
- **Qué pasa:** el archivo es nuevo y no rastreado. Si el agente de commit usa
  `git commit -a`, **no** entra: el repositorio quedaría sin los 32 goldens del
  instalador, del servicio, de los códigos de salida y de las funciones del
  diagnóstico, y la suite del repositorio bajaría a 162 pruebas sin que nadie lo
  note.
- **Por qué es residual:** no es un defecto del código; es un paso del commit
  que hay que hacer explícito.
- **Riesgo si no se toca:** se pierde entera la red de seguridad del cambio 2b.
- **Propuesta:** que el agente de commit haga `git add tests/test_instalacion.py`
  explícitamente antes de commitear (así, además, `.gitattributes` le aplica la
  normalización a LF).
- **Nota de la ronda 2 (lentes 2b ronda 2):** confirmada, y con un filo que no
  estaba dicho: **el golden 7.2 del plan no la cazaría**. Ese golden es
  `unittest … | tail -n 1` → `OK`, y en la Pi seguiría diciendo `OK` con 161
  pruebas en vez de 194, así que nadie notaría la pérdida. El único golden que
  la caza es el **7.12** (194 pruebas), y ese corre en la PC. O sea que el
  `git add tests/test_instalacion.py` explícito no es opcional. (Las pruebas del
  archivo son **33**, no 32: ver **F-162**.)
- **Estado:** **cerrada** el 2026-09-11: `tests/test_instalacion.py` entró completo en el commit `61adf9676b1072115c5fd64e6a28f6bef5454a54` (archivo nuevo, 418 líneas) y sus pruebas corren tanto en la PC como en la Pi dentro de las **194** de la suite.

---

## F-148 · La fila «Construcción del transporte por USB» de la §6 del plan sigue diciendo que `app.py` no pasa `consultar_estado`

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md` §6, fila «Construcción del
  transporte por USB» (`grep -n "Construcción del transporte"`), frente a
  `ruleta/app.py` (`crear_impresora`).
- **Qué pasa:** la fila dice «Dice `anexar=True` y **no** pasa
  `consultar_estado`», y el cambio (b) de 2b ya lo pasa. La §6 obliga a
  «re-grep antes de cada edición»; en esta ronda sí se actualizaron la fila del
  conteo de `[ok]` y la de los usos de `servicio_activo()`, pero esta no. Los
  números de línea de esa misma tabla y de la §5 (343, 87/211/227/266/375, 560,
  13, 36, 50) también se movieron: ese desfase es la familia que ya recogen
  **F-095**, **F-108**, **F-109**, **F-131** y **F-136**, y no se duplica aquí.
- **Por qué es residual:** la §6 se declara explícitamente como fotografía del
  2026-09-11 y manda re-grepear antes de tocar, así que no engaña a quien siga
  sus propias reglas.
- **Riesgo si no se toca:** un ejecutor apurado edita `app.py` para «añadir»
  algo que ya está.
- **Propuesta:** actualizar la fila en el cierre de la Fase 2, en la misma
  pasada en que se refresquen las demás anclas.
- **Estado:** **cerrada** el 2026-09-11 (Paso 14): la fila «Construcción del transporte por USB» de la §6 dice ahora que `ruleta/app.py` 56-59 **sí** pasa `consultar_estado=imp.consultar_estado`.

---

## F-149 · El Paso 6 del plan sigue mostrando la salida temprana que 2b eliminó

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md`, bloque de salida esperada del
  Paso 6 (~línea 1176:
  `[--] impresora tipo 'archivo': no se prueba Bluetooth` + `codigo=0`).
- **Qué pasa:** ese ejemplo de salida es de antes de 2b; tras el deploy la línea
  ya no aparece y en su lugar salen las dos nuevas (ruta del dispositivo y
  consulta del papel). La §7.5 sí está corregida y la bitácora del Paso 6 en la
  §0 es legítima porque registra lo que se midió ese día; lo que quedó viejo es
  el bloque de ejemplo y el aviso que lo acompaña.
- **Por qué es residual:** el aviso que sigue al bloque («este paso NO dice nada
  sobre la impresora») sigue siendo el consejo correcto por la decisión D7.
- **Riesgo si no se toca:** quien compare la salida real contra el ejemplo creerá
  que le falta una línea y que algo se rompió.
- **Propuesta:** reescribir el bloque en el cierre de la Fase 2 con la salida
  real medida en la Pi.
- **Estado:** **cerrada** el 2026-09-11 (Paso 14): el criterio de aceptación del Paso 6 se sustituyó por la salida **medida en la Pi** después del deploy, y su «SI FALLA» ya explica los tres `[!!]` de impresora que 2b hizo posibles.

---

## F-150 · La justificación de la decisión D7 describe el diagnóstico anterior a 2b

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md` §2, decisión **D7** (~línea 423),
  y su eco en el «QUÉ» del Paso 12 (~línea 1811).
- **Qué pasa:** el «por qué (medido en el código)» dice que `cmd_diagnostico`
  «devuelve 0 sin abrir siquiera la ruta» (línea 343). La **decisión** sigue
  siendo válida —el criterio es papel en la mano, y el diagnóstico sigue sin
  demostrar que el boleto salga legible—, pero su justificación ya no describe
  el código. El texto del Paso 12 es una descripción de lo que había que
  cambiar, así que ése se lee bien en pasado.
- **Por qué es residual:** la decisión no cambia; solo su fundamento quedó viejo.
- **Riesgo si no se toca:** quien lea solo D7 creerá que el diagnóstico no revisa
  nada del USB y se saltará una comprobación que ahora sí sirve.
- **Propuesta:** reescribir el «por qué» en el cierre de la Fase 2 sin tocar la
  decisión.
- **Estado:** **cerrada** el 2026-09-11 (Paso 14): la justificación de **D7** distingue ahora lo que hacía el diagnóstico antes de 2b y lo que hace después, y dice por qué la decisión —papel en la mano— sigue en pie igualmente.

---

## F-151 · §5 trampa 4 del plan sigue diciendo que `ImpresoraArchivo` abre siempre con `"ab"`

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md` §5, trampa 4.
- **Qué pasa:** tras 2b el modo es `r+b` cuando se va a consultar el papel, y
  `ab`/`wb` en los demás casos; la trampa lo cuenta como si fuera siempre `ab`.
  Es una fotografía de antes de 2b. Su consejo conservador —**jamás**
  `sudo python3 -m ruleta ...`— sigue valiendo entero, y de hecho vale **más** de
  lo que la trampa sugiere: ver **F-090** y **F-152**. La trampa 2, que citaba el
  `README.md` §5 con «los comandos lo detectan y te lo recuerdan», sí se corrigió
  en esta ronda (`grep -c "comandos lo detectan" README.md` → **0**).
- **Por qué es residual:** el consejo operativo es correcto aunque el detalle
  técnico esté viejo.
- **Riesgo si no se toca:** bajo; a lo sumo confunde a quien lea el código
  después de la trampa.
- **Propuesta:** actualizar el modo de apertura en el cierre de la Fase 2, junto
  con **F-131**, que ya recoge el desfase de línea de esa misma trampa.
- **Estado:** **cerrada** el 2026-09-11 (Paso 14): la §5 trampa 4 dice ahora que el modo es `r+b` —que no crea nada— cuando toca preguntar por el papel, y `ab`/`wb` en los demás casos, entre ellos la impresora con `consultar_estado: false`.

---

## F-152 · F-090 es ahora más fácil de alcanzar: `config.json` apunta a un enlace que desaparece con la impresora apagada

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `config.json` (`"ruta": "/dev/ruleta-impresora"`) y
  `ruleta/escpos.py` (`ImpresoraArchivo.imprimir`, `es_dispositivo_caracteres`).
  Ficha madre: **F-090**.
- **Qué pasa:** la ruta del repositorio ya no es un archivo suelto sino el enlace
  que crea `udev`. Cuando la impresora está apagada o desenchufada el enlace
  **desaparece**, `es_dispositivo_caracteres` devuelve `False` y `imprimir`
  vuelve al modo `ab` (con `O_CREAT`) sobre esa misma ruta. Como `asadero` no
  puede escribir en `/dev`, el intento falla con `Permission denied` y el premio
  se revierte —que es lo deseado—, pero un `sudo python3 -m ruleta ...` sí
  crearía un archivo normal en `/dev/ruleta-impresora` que se traga los boletos
  sin dar error y que además impide que el nodo real aparezca. El agujero no
  cambió de tamaño; cambió de facilidad para llegar a él.
- **Por qué es residual:** no es un defecto nuevo, es la misma F-090 con un
  camino de acceso más común. Contenido solo por no correr nunca con `sudo`
  (§8, prohibición 3).
- **Riesgo si no se toca:** un `sudo` bienintencionado en la semana del evento
  tira boletos a un archivo y el enlace real ya no puede aparecer.
- **Propuesta:** en la Fase 3, rechazar rutas inexistentes bajo `/dev/`, que es
  la propuesta que ya trae F-090. Mientras tanto vale la comprobación
  `test -c /dev/ruleta-impresora`.
- **Nota de la ronda 2 (lentes 2b ronda 2):** confirmada, releído el código. Con
  `config.json` apuntando a `/dev/ruleta-impresora`: impresora apagada → el
  enlace desaparece → `es_dispositivo_caracteres` devuelve `False` → `imprimir`
  vuelve al modo `ab` (con `O_CREAT`) sobre esa misma ruta. Sin `sudo` falla con
  `Permission denied` y el premio se revierte, que es lo deseado; con `sudo` se
  crearía un archivo normal en `/dev` que se traga los boletos e impide que
  aparezca el nodo real. Sigue siendo **F-090** con un camino de acceso más
  común, contenida solo por la prohibición 3 (nunca `sudo`), y se cierra en la
  Fase 3 rechazando rutas inexistentes bajo `/dev/`.
- **Estado:** abierta (Fase 3). El «Estado» de F-090 quedó corregido en esta
  misma ronda: el riesgo **no** bajó con el cambio (d).

---

## F-153 · El README §9 manda re-correr `sudo ./instalar.sh` y en producción la Pi va sin red

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `README.md` §9 (`grep -n "sudo ./instalar.sh" README.md`, hoy en
  las líneas ~429 y ~508) e `instalar.sh` paso `1/7` (`apt-get update`, con
  `set -euo pipefail`).
- **Qué pasa:** el README aconseja «volver a correr `sudo ./instalar.sh`» para
  arreglar los permisos del dispositivo o reponer la regla `udev`. En producción
  la Pi va **sin red**: según con qué código termine `apt-get update` sin red, el
  script puede abortar en el paso 1/7 y no llegar nunca al 5/7, o sea no arreglar
  nada.
- **Por qué es residual:** no está medido. No se pudo comprobar desde aquí el
  código de salida de `apt-get update` sin red en esa Pi.
- **Riesgo si no se toca:** el operador sigue el README, el script aborta con un
  error de apt y él concluye que el problema es la impresora.
- **Propuesta:** medirlo en el deploy. Si aborta, añadir al README el arreglo
  corto:
  `sudo udevadm control --reload && sudo udevadm trigger --subsystem-match=usbmisc`.
- **Nota de la ronda 2 (lentes 2b ronda 2):** sigue sin medir y ahora tiene un
  **filo más**, peor que el de `apt`. Re-correr `sudo ./instalar.sh` ejecuta
  también el paso `7/7`, que hace `systemctl enable ruleta.service`: el consejo
  del README **vuelve a dejar el servicio `enabled`**, en contra de la decisión
  **D6** y de la **prohibición 1** mientras el Paso 13 no esté hecho. Al medirlo
  en el deploy hay que mirar las dos cosas. El arreglo corto sigue siendo
  documentar `sudo udevadm control --reload && sudo udevadm trigger
  --subsystem-match=usbmisc` en vez de mandar el instalador entero.
- **Estado:** abierta (medir en el deploy). **Medido en el deploy (2026-09-11):** `sudo ./instalar.sh` salió con **código 0** en la Pi, pero **con red** (la del punto de acceso de la laptop). El caso que preocupa a esta ficha —re-correrlo durante el evento, sin internet y con `apt-get update` fallando— sigue sin medir. **Nota del 2026-09-15 (Fase 3):** el usuario decidió que **no habrá batería RTC** y que **la Pi irá con el internet del asadero** durante el evento (acta `docs/actas/2026-09-15-fase-3.md` §7, ficha **F-241**). Con esa decisión, el escenario que preocupaba a esta ficha —re-correr el instalador **sin internet**— deja de ser el caso de producción, aunque sigue valiendo para un corte de red. Y el **segundo filo** de la nota de ronda 2 —que el paso `7/7` vuelve a dejar el servicio `enabled`— **ya no es un problema**: desde el cierre de la Fase 2 el kiosco se queda `enabled` **a propósito** (ficha **F-185**, cerrada). Sigue sin medirse el código de salida de `apt-get update` sin red.

---

## F-154 · Cosmético: faltan líneas en blanco antes de varios `---` y F-138 quedó pegada a F-137

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/fichas.md`: F-001, F-002, F-003, F-051, F-052, F-053, F-077,
  F-088, F-089, F-090, F-091 y F-113, más el corte entre F-137 y F-138.
- **Qué pasa:** al reescribir los `- **Estado:**` en la ronda anterior se perdió
  la línea en blanco que separaba el último bullet del `---`. En el peor caso,
  el encabezado `## F-138 …` arranca pegado al `- **Estado:**` de F-137, sin
  `---` ni línea en blanco de por medio. No rompe nada de lo que se ha probado,
  pero desalinea el formato del archivo respecto al resto de las fichas.
- **Por qué es residual:** es cosmético de Markdown, sin efecto sobre el
  contenido ni sobre ningún golden.
- **Riesgo si no se toca:** ninguno funcional; solo cuesta leer el diff.
- **Propuesta:** normalizarlo de una pasada cuando se vuelva a tocar el archivo
  por otro motivo, para no ensuciar el diff de esta ronda.
- **Estado:** abierta (cosmético).

---

## F-155 · `instalar.sh` usa `udevadm control --reload` en el paso 4/7 y `--reload-rules` en el 5/7

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `instalar.sh` líneas 54 y 69.
- **Qué pasa:** son sinónimos exactos, así que el efecto es idéntico; solo es una
  incoherencia de escritura entre dos pasos del mismo script. El golden
  `test_udevadm_recarga_las_dos_reglas` fija esa lista tal cual, o sea que
  unificarlo obliga a tocar también el golden.
- **Por qué es residual:** no hay diferencia de comportamiento.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejarlo como está. Si alguna vez se unifica, cambiar el script y
  el golden en el mismo commit.
- **Estado:** abierta (cosmético; decisión tomada de no tocarlo).

---

## F-156 · Verificado: todo cuadra contra el acta del 2026-09-11 y contra la Pi

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/actas/2026-09-11-hechos-medidos.md`, `instalar.sh` (paso 5/7),
  `config.json` y `README.md`.
- **Qué pasa:** comprobados uno por uno y todos cuadran: VID:PID `0418:5011`,
  clase 7 subclase 1 protocolo 2, `/dev/usb/lp0 crw-rw---- root:lp`, la línea
  exacta de la regla `udev`, `lp:x:7:asadero`, los 118 reinicios con
  `RestartSec=3` y `StartLimitIntervalSec=0`, `ESC t 19` correcto y `ESC t 16`
  basura, 48 columnas, corte `auto`, `ESC B` = un pitido corto por comando
  ignorando `n` y `t`, `192.168.137.95/24` y `America/Hermosillo`. Además: la
  regla `udev` que escribe `instalar.sh` es idéntica **byte a byte** a la
  aplicada a mano en la Pi (comprobado con `od -c`), y el `config.json` del
  repositorio coincide con el de la Pi más `"beep": true`, que es lo que necesita
  el deploy por `git pull` después del `git checkout --`. Los conteos golden del
  README también dan lo que dice el plan: `scp -r` → **0**,
  `America/Mexico_City` → **0**, `usuario@ruleta.local` → **0**,
  `comandos lo detectan` → **0**, `/dev/usb/lp0` → **4**,
  `/dev/ruleta-impresora` → **5**.
- **Por qué es residual:** nota de verificación; no hay nada que corregir.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejar constancia para no repetir el cotejo.
- **Nota de la ronda 2 (lentes 2b ronda 2):** re-cotejado, todo sigue cuadrando,
  con tres medidas nuevas. (1) La regla `udev` que escribe `instalar.sh` (línea
  66) es idéntica **carácter por carácter** a la aplicada a mano en la Pi: el
  md5 de la línea da `2c2c308ba8f3b9683663e1dc93cd9983`, el mismo que registra
  `docs/actas/2026-09-11-hechos-medidos.md`. (2) El `config.json` del
  repositorio son los valores finales de la Pi (`tipo: archivo`,
  `ruta: /dev/ruleta-impresora`) más `beep: true`, y `tests/test_config.py` los
  fija con un golden de tupla completa: es justo lo que necesita el deploy por
  `git checkout --` + `git pull`. (3) Las anclas ya actualizadas vuelven a dar lo
  esperado: `servicio_activo` en las líneas **90** (definición), **214**, **230**,
  **269**, **417** y **464** —cinco usos, y `probar-impresora` no está entre
  ellos— y los conteos golden del README: `scp -r` → **0**,
  `America/Mexico_City` → **0**, `usuario@ruleta.local` → **0**,
  `comandos lo detectan` → **0**, `/dev/usb/lp0` → **4**,
  `/dev/ruleta-impresora` → **5**. Lo que **no** cuadra son las anclas que la §6
  todavía no ha refrescado: van en **F-166**.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-157 · Verificado: sin BOM y con finales LF; `.gitattributes` cubre las extensiones que se tocan

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** todos los archivos tocados en 2b (`ruleta/*.py`, `tests/*.py`,
  `README.md`, `CLAUDE.md`, `config.json`, `instalar.sh`, `ruleta.service`,
  `docs/fichas.md`, `docs/planes/fase-2-impresora.md`) y `.gitattributes`.
- **Qué pasa:** medido con Python sobre los bytes: **ningún** archivo lleva BOM y
  **ninguno** tiene CRLF en el árbol de trabajo, tampoco el nuevo
  `tests/test_instalacion.py`. O sea que lo medido **no** reproduce la
  observación de la ronda de lentes de que el árbol estuviera en CRLF; muy
  probablemente esa lectura venía de una herramienta que normaliza al leer.
  Aparte, `.gitattributes` fuerza `text eol=lf` para `*.sh`, `*.service`, `*.py`,
  `*.json` y `*.md`, con lo que el índice queda en LF pase lo que pase.
- **Por qué es residual:** nota de verificación, con una corrección al hallazgo
  original.
- **Riesgo si no se toca:** ninguno, con una condición: que
  `tests/test_instalacion.py` entre al índice con `git add` para que la
  normalización se le aplique (ver **F-147**).
- **Propuesta:** dejar constancia.
- **Nota de la ronda 2 (lentes 2b ronda 2):** re-medido sobre los bytes, ya
  aplicadas las correcciones de esta ronda: **ningún** archivo tocado lleva BOM
  ni CRLF, incluidos el nuevo `tests/test_instalacion.py`, el `README.md` y
  `docs/planes/fase-2-impresora.md`.
- **Nota de la ronda 3 (lente docs fase 2, 2026-09-11):** el lente de
  documentación volvió a reportar que los tres `.md` de la Fase 2 estarían
  guardados en **CRLF** en el árbol de trabajo (424, 2720 y 3019 líneas con
  CR). **Re-medido hoy sobre los bytes, antes y después de aplicar las
  correcciones de esa ronda: cero bytes `\r`** en
  `docs/actas/2026-09-11-fase-2.md`, `docs/planes/fase-2-impresora.md` y
  `docs/fichas.md`, con dos métodos independientes (conteo en Python sobre
  los bytes y `tr -dc '\r' | wc -c`). Ninguno lleva BOM y los tres terminan
  en salto de línea. Es la **tercera** vez que aparece la observación y la
  tercera que no se reproduce: casi seguro viene de una herramienta que
  normaliza al leer. **No se abrió ficha nueva, por no duplicar ésta.**
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-158 · `interpretar_estado_papel(None, 0x12)` dice «hay papel» aunque el byte de papel nunca llegó

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `ruleta/__main__.py`, `interpretar_estado_papel`
  (`grep -n "def interpretar_estado_papel" ruleta/__main__.py`).
- **Qué pasa:** la función solo saca `[??]` cuando **ninguno** de los dos bytes
  contesta. Si llega el de estado pero no el del papel —el vector
  `interpretar_estado_papel(None, 0x12)`—, ninguna de las guardas intermedias se
  cumple y cae en el `return` final:
  `[ok] la impresora contesta: hay papel y está en línea`, afirmando algo que no
  se midió.
- **Por qué es residual:** el diagnóstico no bloquea nada (siempre se imprime
  igual) y el criterio de la fase es papel en la mano, no esta línea. Tampoco
  está claro que un firmware conteste a una consulta y no a la otra.
- **Riesgo si no se toca:** alguien se fía del `[ok]`, no revisa el rollo y se
  queda sin papel a media noche del evento.
- **Propuesta:** en la Fase 3, distinguir «papel: no contestó» de «papel: hay» y
  sacar `[??]` cuando falte cualquiera de los dos bytes.
- **Estado:** abierta.

---

## F-159 · `Documento.beep(veces, duracion)` conserva parámetros que esta impresora ignora

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `ruleta/escpos.py` (`def beep(self, veces: int = 2, duracion: int = 2)`)
  y `ruleta/ticket.py` (`doc.beep(2, 2)`).
- **Qué pasa:** medido en la Pi el 2026-09-11: esta impresora hace **un** pitido
  corto por cada `ESC B` e ignora `n` y `t`. La firma sigue prometiendo `n`
  pitidos de `t` unidades, y el boleto llama `doc.beep(2, 2)`, que produce **un**
  pitido. El nombre y los parámetros invitan a creer que produce dos.
- **Por qué es residual:** el comando es ESC/POS correcto y funcionaría en otra
  impresora de la familia; el defecto es de expectativa, no de conducta.
- **Riesgo si no se toca:** alguien sube `veces` buscando más pitidos, no pasa
  nada y cree que el zumbador está fallando.
- **Propuesta:** anotar en el docstring que **esta** unidad ignora `n` y `t`, o
  llamar `beep()` tantas veces como pitidos se quieran. Fase 3.
- **Estado:** abierta.

---

## F-160 · La decisión D8 fijaba `beep: false` y el repositorio lo deja en `true`

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `docs/planes/fase-2-impresora.md` §2, decisión **D8** (que lista
  `beep: false` entre los valores de arranque) y §5 trampa correspondiente,
  frente a `config.json` (`"beep": true`).
- **Qué pasa:** el repositorio lleva `true` por decisión explícita del usuario,
  medida esa misma noche (un pitido corto por boleto). Está justificado, anotado
  en la bitácora del Paso 8 de la §0 y reflejado en la tabla del `README.md` §6,
  pero la nota de 2b no lo cruza con D8: quien lea D8 sola creerá que el
  repositorio la desobedece.
- **Por qué es residual:** la decisión está tomada y documentada; falta el
  puente entre los dos textos.
- **Riesgo si no se toca:** un ejecutor futuro «corrige» el `config.json` a
  `false` creyendo que arregla una desviación, y el local se queda sin el aviso
  sonoro.
- **Propuesta:** anotar en D8 que quedó revisada el 2026-09-11 y por qué, en el
  cierre de la Fase 2.
- **Estado:** abierta, como vigilancia. El plan ya no se contradice a sí mismo: la decisión **D8** dice ahora que el papel confirmó `codepage_n`, `chars_por_linea` y `corte`, y que **`beep` es el único valor que cambió**, a `true`, por decisión del usuario después de oír el zumbador el 2026-09-11 (**F-188** y `docs/actas/2026-09-11-fase-2.md` §6 punto 2 y §10). La ficha sigue abierta por si el usuario prefiere volver a `false` cuando lo oiga una noche entera de evento; cerrarla es decisión suya, no de un agente, y la pasada del texto de consuelo no la traía en su alcance (ver **F-223**).

---

## F-161 · `test_sigue_registrando_y_habilitando_el_servicio` usa `assertIn` donde el Paso 12 pide igualdad

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 1
- **Dónde:** `tests/test_instalacion.py`,
  `test_sigue_registrando_y_habilitando_el_servicio` (líneas 156-161).
- **Qué pasa:** comprueba con `assertIn` que las tres órdenes
  (`systemctl enable --now bluetooth`, `systemctl daemon-reload`,
  `systemctl enable ruleta.service`) sigan estando en el instalador, mientras que
  el resto del archivo compara por igualdad, que es lo que piden las reglas de
  goldens del Paso 12.
- **Por qué es residual:** no es un assert que no muerda —si alguien borra una
  orden, la prueba falla—, pero rompe la convención del propio plan y no detecta
  que se le añadan opciones a esa misma línea.
- **Riesgo si no se toca:** bajo; una orden modificada (no borrada) pasaría
  inadvertida.
- **Propuesta:** convertirlo a comparación de líneas exactas cuando se toque el
  archivo por **F-146**.
- **Nota de la ronda 2 (lentes 2b ronda 2):** confirmada, con el matiz de cuánto
  muerde. El `assertIn` comprueba **presencia**: muerde si alguien borra
  `systemctl enable ruleta.service`, pero no si alguien **añade** un comando
  destructivo nuevo al instalador. Los demás goldens del archivo —pasos
  numerados, reglas `udev`, grupos, `udevadm`— sí derivan censos completos y
  comparan por igualdad, así que la cobertura por igualdad ya existe; es solo
  esta prueba la que es más débil que sus vecinas.
- **Estado:** abierta.

---

## F-162 · Las fichas F-146 y F-147 dicen «32 pruebas» y `tests/test_instalacion.py` tiene 33

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `docs/fichas.md`, **F-146** y **F-147**; `tests/test_instalacion.py`.
- **Qué pasa:** el conteo real del archivo son **33** pruebas: medido archivo por
  archivo, 194 = 29 (`test_app`) + 16 (`test_config`) + 70 (`test_escpos`) + 24
  (`test_inventario`) + 22 (`test_ticket`) + **33** (`test_instalacion`). Las dos
  fichas dicen 32 porque ese es el **delta observable**: cuando el import falla,
  `unittest` inyecta un `_FailedTest` que también cuenta como prueba, así que la
  suite cae a 162 y no a 161 (161 + 1 = 162). Medido por mutación en copia:
  quitar `RestartPreventExitStatus` deja exactamente
  `Ran 162 tests … FAILED (errors=1)`, o sea que la **salida** que predice F-146
  es correcta; lo único ambiguo es el número 32.
- **Por qué es residual:** cosmético. Ninguna decisión, golden ni paso del plan
  depende de esa cifra.
- **Riesgo si no se toca:** ninguno práctico; a lo sumo alguien resta mal al
  cuadrar el conteo de la suite.
- **Propuesta:** al tocar F-146 por su arreglo, escribir «33 pruebas (la suite
  cae a 162, no a 161, porque el `_FailedTest` cuenta como prueba)».
- **Estado:** abierta (cosmética).

---

## F-163 · `instalar.sh` añade el grupo `gpio` sin el guardia `getent` que sí tienen `bluetooth` y `lp`

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `instalar.sh` línea **38** (`usermod -aG gpio "${USUARIO}"`), frente
  a la línea 39 (`getent group bluetooth >/dev/null && usermod -aG bluetooth … || true`)
  y a la 68 (lo mismo para `lp`).
- **Qué pasa:** las tres altas de grupo hacen lo mismo y solo dos van protegidas.
  Con `set -euo pipefail` en la cabecera, en una imagen que no traiga el grupo
  `gpio` el `usermod` devuelve error y **aborta el instalador entero en el paso
  2/7**, antes de las reglas `udev`, del servicio y del diagnóstico.
- **Por qué es residual:** es **preexistente** —la sub-fase 2b no tocó esa
  línea— y no se dispara en Raspberry Pi OS, que sí crea el grupo `gpio`.
- **Riesgo si no se toca:** en otra imagen (Ubuntu, Debian puro) la instalación
  muere en el segundo paso con un mensaje de `usermod`, no de la ruleta, y el
  operador no sabrá qué mirar.
- **Propuesta:** dejarlo igual que sus dos vecinos:
  `getent group gpio >/dev/null && usermod -aG gpio "${USUARIO}" || true`.
  Comprobado: el golden `test_grupos_que_agrega_el_instalador` seguiría en verde,
  porque compara el **conjunto** `{gpio, bluetooth, lp}` y ya reconoce la forma
  con guardia (así están hoy `bluetooth` y `lp`). Fase 3.
- **Estado:** abierta.

---

## F-164 · El diagnóstico interno del instalador corre sin `udevadm settle` y puede dar un `[!!]` espurio

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `instalar.sh` línea **93** (diagnóstico interno) y línea **70**
  (`udevadm trigger --subsystem-match=usbmisc`).
- **Qué pasa:** entre el `trigger` y el diagnóstico no hay `udevadm settle`.
  `udev` es asíncrono, así que el enlace `/dev/ruleta-impresora` puede no existir
  todavía cuando el diagnóstico lo busca, y entonces el propio instalador imprime
  un `[!!] no existe la ruta de la impresora` que es falso.
- **Por qué es residual:** no aborta nada (el diagnóstico va con `|| true`) y
  basta con volver a correrlo; es ruido, no fallo.
- **Riesgo si no se toca:** el operador termina la instalación creyendo que la
  impresora está mal y se pone a desenchufar cables.
- **Propuesta:** `udevadm settle --timeout=10 2>/dev/null || true` justo después
  del `trigger` de la línea 70. Fase 3, junto con **F-155**.
- **Estado:** abierta.

---

## F-165 · Efecto secundario nuevo: el instalador ahora manda `DLE EOT` a la impresora durante la instalación

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `instalar.sh` línea 93 (diagnóstico interno), `config.json`
  (`"tipo": "archivo"` y `"consultar_estado": true`) y `ruleta/__main__.py`
  (`cmd_diagnostico`, rama `archivo`).
- **Qué pasa:** antes de 2b el diagnóstico salía temprano en cuanto veía
  `tipo: archivo` y nunca le hablaba a la impresora. Ahora, con la `ruta` puesta
  y `consultar_estado` en `true`, el diagnóstico que corre **dentro** de
  `sudo ./instalar.sh` le manda `DLE EOT` a la impresora durante la instalación.
- **Por qué es residual:** es inofensivo —`DLE EOT` no imprime ni gasta papel— y
  es justo el efecto que 2b buscaba. Se anota solo porque es conducta nueva del
  instalador que nadie pidió explícitamente y que conviene saber **antes** del
  deploy.
- **Riesgo si no se toca:** ninguno conocido; queda la duda de si el firmware de
  esta unidad reacciona raro a una consulta durante la instalación.
- **Propuesta:** mirar la salida del bloque «Diagnóstico» del instalador la
  primera vez que se corra en la Pi. Si molestara, `consultar_estado: false` lo
  apaga sin tocar código.
- **Estado:** abierta (informativa, mirar en el deploy). **Medido en el deploy (2026-09-11):** el instalador corrió con la impresora conectada y encendida y salió con **código 0**; el arranque posterior del servicio imprimió el inventario sin basura. No se guardó la salida del diagnóstico interno del instalador, así que de ese `DLE EOT` solo se sabe que no rompió nada.

---

## F-166 · Censo: diez anclas más de la §6 del plan quedaron viejas tras 2b y pueden parar el deploy en falso

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `docs/planes/fase-2-impresora.md` §6 «Mapa de anclas que derivan».
  Familia: **F-148**, **F-149**, **F-150**, **F-151**, más las anteriores
  **F-095**, **F-108**, **F-109**, **F-131** y **F-136**.
- **Qué pasa:** la §6 manda **detenerse y preguntar** si un ancla no está donde
  dice la tabla. Medido hoy, además de lo que ya recoge **F-148** (formato:
  ancla — lo que dice la §6 — lo que hay de verdad):

  - `class ImpresoraArchivo` en `ruleta/escpos.py` — 546 — **603**.
  - `no se prueba Bluetooth` en `ruleta/__main__.py` — 344 — **el `grep` ya no
    devuelve nada**.
  - `== 2/6` en `instalar.sh` — 36 — **el `grep` ya no devuelve nada**: hoy es
    `== 2/7`, en la línea 37.
  - `"tipo"` y `"ruta"` en `config.json` — una línea (16) y **cero** de `ruta` —
    **16 y 19**, con la `ruta` ya puesta.
  - `SupplementaryGroups` en `ruleta.service` — 13, «hoy dice `gpio`» — **15**, y
    dice `gpio lp`.
  - Bytes y bits del estado en `ruleta/escpos.py` — 54-57, 398, 415 y 421 —
    **58-60, 104, 118, 124 y 661-662**.
  - `/dev/usb/lp0` en el `README.md` — 255 y 429 — **128, 304, 514 y 518**.
  - `comandos lo detectan` en el `README.md` — 225 — **0: ya no está**.
  - `America/Mexico_City` en el `README.md` — 153 — **0: ya no está**.
  - `Lista. Esperando jugadas.` en `ruleta/app.py` — 115 — **117** (y
    `Inventario impreso`, 268 → **270**).

  La peor es la fila de `config.json`: su columna «por qué deriva» dice «si
  aparece ya puesta, alguien tocó el archivo», con lo que hoy dispararía un alto
  en falso nada más empezar, cuando la `ruta` está puesta **a propósito** por 2b.
  Las líneas del `README.md` se midieron después de las correcciones de esta
  ronda, que empujaron seis líneas hacia abajo todo lo que va tras el §9.
- **Por qué es residual:** las anclas hicieron su trabajo (avisar de que el
  repositorio se movió); lo que falta es refrescarlas ahora que el movimiento es
  el buscado.
- **Riesgo si no se toca:** medio deploy se detiene a preguntar por diferencias
  que son el resultado deseado de 2b, y el ejecutor sin contexto no puede saber
  cuáles son legítimas.
- **Propuesta:** refrescar la §6 entera **de una sola pasada** en el Paso 14,
  cerrando a la vez F-148, F-149, F-150, F-151, F-095, F-108, F-109, F-131 y
  F-136.
- **Estado:** **cerrada** el 2026-09-11 (Paso 14): la §6 entera se volvió a medir con `grep -n` contra `61adf96` y cada fila dice hoy la línea real, o que el texto ya no existe. Con ella se cierran **F-131**, **F-148**, **F-149**, **F-151** y **F-109**. Siguen abiertas **F-095**, **F-108** y **F-136**, que hablan de otras secciones.

---

## F-167 · El `README.md` §8 resume el diagnóstico sin las dos revisiones que añadió 2b

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `README.md` §8, línea del comando
  (`grep -n "ruleta diagnostico  #" README.md`).
- **Qué pasa:** el comentario dice «dependencias, carpeta de datos,
  emparejamiento, conexión y canal» y no menciona lo que trajo 2b: la revisión de
  la **ruta del dispositivo USB** y la **consulta de papel**. El §9 sí las cuenta
  bien, así que no es falso: es incompleto y describe el diagnóstico anterior al
  cambio.
- **Anotado dos veces en la misma ronda:** el lente lo señaló por separado como
  «no menciona la revisión de la ruta USB ni la consulta de papel» y como «no es
  falso, es incompleto». Es el mismo hallazgo, por eso va en una sola ficha.
- **Por qué es residual:** cosmético; esa lista es un resumen de una línea, no un
  contrato.
- **Riesgo si no se toca:** quien lea solo el §8 no sabrá que el diagnóstico
  ahora también revisa el cable y el papel, y no lo usará para eso.
- **Propuesta:** «dependencias, carpeta de datos, ruta USB, papel, emparejamiento
  y canal», en el cierre de la Fase 2 (toca documentación que lee el usuario).
- **Estado:** abierta.

---

## F-168 · `verificar_estado` e `interpretar_estado_papel` evalúan los mismos bits en distinto orden

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `ruleta/escpos.py`, `verificar_estado` (líneas 118-126) y
  `ruleta/__main__.py`, `interpretar_estado_papel` (líneas 351-357).
- **Qué pasa:** `verificar_estado` evalúa **sin papel → poco papel → fuera de
  línea**; `interpretar_estado_papel` evalúa **sin papel → fuera de línea → poco
  papel**. Es decir, «poco papel» va antes de «fuera de línea» en uno y después
  en el otro. Con los cinco vectores probados el resultado observable coincide,
  así que hoy no hay diferencia visible; son dos órdenes de prioridad que hay que
  mantener sincronizados a mano.
- **Por qué es residual:** no hay defecto de conducta con los bits de hoy; es la
  misma regla de negocio escrita dos veces.
- **Riesgo si no se toca:** el día que se añada un bit (tapa abierta, error del
  cabezal), los dos caminos pueden dar mensajes distintos para el mismo byte y
  nadie lo notará, porque las pruebas de cada uno van por separado.
- **Propuesta:** que `interpretar_estado_papel` reutilice la clasificación de
  `escpos.py`, o dejar en ambos el mismo orden con un comentario que se citen
  mutuamente. Fase 3.
- **Estado:** abierta.

---

## F-169 · `CLAUDE.md` §«Contexto del producto» quedó viejo tras 2b: impresora «Bluetooth» y valores «sin confirmar»

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `CLAUDE.md` §«Contexto del producto» (líneas 106-113).
- **Qué pasa:** sigue describiendo el hardware como «impresora térmica Bluetooth
  AOMU My-A1 de 80 mm» y afirmando que «los valores de impresora (canal, tabla de
  acentos, corte) están sin confirmar en hardware real hasta que el usuario corra
  `python3 -m ruleta probar-impresora` y `diagnostico` en la Pi». Las dos cosas
  son falsas contra el acta del 2026-09-11 (USB como primario y Bluetooth como
  respaldo; `cp858` / tabla 19, 48 columnas, corte `auto` y zumbador **medidos en
  papel**) y contra el `README.md` reescrito en 2b.
- **Por qué es residual y no corrección de esta ronda:** **tocar `CLAUDE.md`
  exige visto bueno explícito del usuario** (convención del repositorio, ver
  **F-076**), así que esta ronda lo deja igual a propósito.
- **Riesgo si no se toca:** un agente nuevo lee `CLAUDE.md` antes que nada, cree
  que la impresora va por Bluetooth y que no hay nada medido, y repite mediciones
  o decide al revés.
- **Propuesta:** que el orquestador lo lleve al usuario en el cierre de la Fase 2
  con el texto de reemplazo ya redactado, para que él solo tenga que decir sí o
  no.
- **Estado:** **resuelta** el 2026-09-11 ~23:20, **con el visto bueno del usuario**, en el cierre de la Fase 2. `CLAUDE.md` §«Contexto del producto» dice ahora: AOMU My-A1 = **clon POS-80** (USB `0418:5011`, `ieee1284_id` con **emulación EPSON**; el PPD del fabricante la llama **Zjiang ZJ-80250**), **conectada por cable USB** (`impresora.tipo = "archivo"`, `ruta = "/dev/ruleta-impresora"`), **Bluetooth solo de respaldo y nunca ejercido**; **valores confirmados en hardware** (tabla **19 / `cp858`**, **48 columnas**, **corte automático**, **un pitido por comando `ESC B`**); red de laboratorio = **punto de acceso de Windows** y **producción sin red**, con la batería RTC como consecuencia. El resto de `CLAUDE.md` —§1 a §7 y las convenciones del repositorio— quedó **intacto**.

---

## F-170 · `docs/PAUSA-2026-09-11.md` sigue diciendo que faltan los lentes de la Fase 2 y que la impresora está «sin probar»

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `docs/PAUSA-2026-09-11.md`, aviso «Lo que sigue pendiente de esta
  pausa» (líneas 17-21) y §1 «Estado al pausar», fila de la impresora (línea 34).
- **Qué pasa:** el aviso enumera como pendientes «los eslabones 8 a 12 (lentes de
  la Fase 2, correctivo, escéptico, commit y verificador de push)» y la fila de
  la impresora dice «sin probar; el usuario no trajo el cable de corriente».
  Después de la noche del 2026-09-11 y de la sub-fase 2b, ninguna de las dos
  sigue siendo cierta.
- **Por qué es residual:** el propio archivo se declara **histórico** («describe
  cómo se llegó hasta aquí»), así que no engaña a quien lo lea en su contexto.
- **Riesgo si no se toca:** quien lo abra suelto —por ejemplo buscando «qué
  falta»— se lleva el estado equivocado del proyecto.
- **Propuesta:** dos líneas al principio: «Superado el 2026-09-11 por la sub-fase
  2b; el estado vigente está en `docs/planes/fase-2-impresora.md` §0». Cierre de
  la Fase 2.
- **Estado:** abierta.

---

## F-171 · Dos pruebas de `tests/test_instalacion.py` repiten lo que `test_unidad_completa` ya fija por igualdad

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `tests/test_instalacion.py`:
  `test_los_errores_de_configuracion_no_se_reintentan` (líneas 201-204) y
  `test_el_servicio_puede_escribir_en_la_impresora_usb` (líneas 206-207), frente
  a `test_unidad_completa` (línea 175).
- **Qué pasa:** `test_unidad_completa` compara la unidad `ruleta.service`
  **entera por igualdad**, así que ya fija `RestartPreventExitStatus = 2` y
  `SupplementaryGroups = gpio lp`. Las otras dos vuelven a comprobar cada cosa
  por separado.
- **Por qué es residual:** las tres muerden (verificado por mutación); el defecto
  es de mantenimiento, no de cobertura.
- **Riesgo si no se toca:** el día que cambie la unidad hay que tocar **tres**
  pruebas en vez de una, y es fácil dejar dos coherentes y una no.
- **Propuesta:** conservarlas —documentan la intención, que es útil— pero anotar
  en cada una que la red de seguridad real es `test_unidad_completa`; o fundirlas
  cuando se toque el archivo por **F-146**.
- **Estado:** abierta (cosmética).

---

## F-172 · Índice: fichas de la ronda 1 confirmadas sin cambio en la ronda 2

- **Fecha:** 2026-09-11
- **Origen:** lentes 2b ronda 2
- **Dónde:** `docs/fichas.md`. Equivalente para 2b de lo que **F-124** fue para
  la ronda anterior.
- **Qué pasa:** vueltas a mirar hoy, siguen abiertas y **sin resolver por este
  cambio**: **F-145** (ni `_hay_algo_que_leer` con `select` real ni la rama
  `archivo` de `cmd_diagnostico` las ejecuta ningún assert), **F-146**
  (`CODIGO_CONFIG` se deriva al importar y la suite cae a 162 con un error
  opaco), **F-147** (`tests/test_instalacion.py` sigue sin rastrear en git: el
  agente de commit debe hacer `git add` explícito por ruta), **F-158**
  (`interpretar_estado_papel(None, 0x12)` sigue diciendo `[ok] hay papel` sin
  haberlo medido), **F-161** (`assertIn` donde el Paso 12 pide igualdad),
  **F-090** y **F-152** (con la impresora apagada el enlace desaparece e
  `imprimir` vuelve a `ab` con `O_CREAT`), **F-139** (la regla `udev` y el enlace
  se llaman distinto que en el plan: falta el visto bueno del orquestador antes
  del deploy) y **F-140** (el golden `[ok]` de la Fase 1 pasa de 6 a 8 y los
  documentos de la Fase 1 no se tocaron). Cada una lleva su propia «Nota de la
  ronda 2» donde hubo algo que añadir.
- **Por qué es residual:** es un índice para el cierre, no un hallazgo nuevo.
- **Riesgo si no se toca:** ninguno; existe para que el Paso 14 no se deje
  ninguna fuera.
- **Propuesta:** repasarlas en bloque en el Paso 14 y cerrar las que el deploy
  resuelva.
- **Estado:** abierta (índice).

---

## F-173 · Hueco de cobertura que **F-145** no cubre: la línea `[ok] {módulo} {version_modulo(...)}` del diagnóstico no la ejecuta ningún assert

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `ruleta/__main__.py`, `cmd_diagnostico`, línea **381**:
  `print(f"  [ok] {modulo} {version_modulo(modulo, m)}")`.
- **Qué pasa:** medido por mutación en copia: devolver esa línea a
  `getattr(m, "__version__", "")` deja la suite **entera en verde**. O sea que
  el arreglo visible de **F-051** (`gpiozero` y `lgpio` salían con la versión en
  blanco) se puede revertir sin que nada muerda. `version_modulo()` sí tiene
  goldens propios (`TestVersionModulo`, en `tests/test_instalacion.py`), pero
  **nadie comprueba que `cmd_diagnostico` la llame**.
- **Por qué es residual:** es cobertura que falta, no un defecto de conducta: la
  línea hoy está bien escrita.
- **Por qué NO lo cubre F-145:** **F-145** declara huecos en `cmd_diagnostico`,
  pero su justificación es que «las dos ramas dependen de Linux» (`select` sobre
  un dispositivo de caracteres, `systemctl`). Esa razón **no aplica a esta
  línea**: el bucle de módulos corre igual en Windows, así que este caso sí se
  puede cerrar en esta PC.
- **Riesgo si no se toca:** una regresión de una sola línea devuelve las
  versiones en blanco en la Pi, con la suite en verde.
- **Propuesta:** **ampliar F-145** con este caso y, cuando se toque el archivo,
  una prueba de `cmd_diagnostico` con los módulos simulados que fije la línea
  completa.
- **Estado:** abierta.

---

## F-174 · **F-145** confirmada con números: tres mutaciones más de la rama `archivo` de `cmd_diagnostico` sobreviven en verde

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `ruleta/__main__.py`, `cmd_diagnostico`, rama `tipo == "archivo"`
  (líneas 406-431).
- **Qué pasa:** no se repite lo que **F-145** ya dice; se le ponen números.
  Medido por mutación en copia, sobreviven **en verde**: (a) anular la rama
  entera, (b) quitar el `ok = ok and bien` de la revisión de la ruta y (c) no
  consultar nunca el papel. Ningún assert toca ese cableado.
- **Por qué es residual:** es la confirmación cuantificada de una ficha ya
  abierta, no un hallazgo nuevo.
- **Riesgo si no se toca:** el mismo de **F-145**, ahora medido: tres maneras de
  romper el diagnóstico sin que la suite se entere.
- **Propuesta:** anexar estos tres números a **F-145** y cerrarlos en la Pi con
  los goldens de la §7.5.
- **Estado:** abierta (confirma **F-145**).

---

## F-175 · Los valores por defecto de `ImpresoraArchivo.__init__` no los ancla ninguna prueba

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `ruleta/escpos.py`, `ImpresoraArchivo.__init__` (línea **620**):
  `consultar_estado: bool = False` y `timeout_estado: float = 1.0`.
- **Qué pasa:** medido por mutación: `consultar_estado=False → True` y
  `timeout_estado=1.0 → 0.0` **sobreviven en verde**.
- **Por qué es residual:** hoy no muerde de verdad. `ruleta/app.py` (línea 59)
  siempre pasa `consultar_estado=imp.consultar_estado` explícito, y el doble de
  las pruebas USB pasa `timeout_estado=1.0` a mano (`tests/test_escpos.py`,
  línea 472), así que ningún camino vivo depende del defecto.
- **Riesgo si no se toca:** un tercer llamador nuevo —otro comando, la Fase 3—
  heredaría el defecto sin red: se quedaría sin consulta de papel, o con un
  `select` de cero segundos que nunca espera respuesta.
- **Propuesta:** un assert de una línea que compare por igualdad los dos
  valores por defecto del constructor. Fase 3, junto con **F-171**.
- **Estado:** abierta.

---

## F-176 · DEPLOY: un `git pull` NO actualiza `/etc/systemd/system/ruleta.service`

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `ruleta.service` (plantilla del repositorio), `instalar.sh` (la
  copia con `sed` y el `systemctl enable` del paso 7/7), el «OJO» del Paso 12
  (a) del plan de la Fase 2 (línea 1714) y `README.md` §9.
- **Qué pasa:** es lo más importante de esta tanda y el plan ya lo cubre en ese
  «OJO»; se repite aquí porque es justo lo que se puede perder en el deploy. La
  unidad **viva** en la Pi es la copia que `instalar.sh` escribe con `sed` en
  `/etc/systemd/system/ruleta.service`, no el archivo del repositorio. Mientras
  no se vuelva a correr `sudo ./instalar.sh` —o no se regenere la unidad a mano
  y se haga `daemon-reload`—, `RestartPreventExitStatus=2` y
  `SupplementaryGroups=gpio lp` **no están aplicados en la Pi** y el bucle de
  **118 reinicios** de **F-138** sigue vivo, aunque el `README.md` §9 ya afirme
  que systemd «no lo reintenta».
- **Y el efecto secundario:** al volver a correr el instalador, su paso 7/7 hace
  `systemctl enable ruleta.service`. Si el Paso 13 todavía no se ha hecho, hay
  que devolverlo a `disabled` (`sudo systemctl disable ruleta`;
  `systemctl is-enabled ruleta` → `disabled`), que es lo que mandan la decisión
  **D6** y la **prohibición 1**.
- **Por qué es residual:** no es un defecto del código; es un paso del deploy
  que, si se salta, deja el arreglo sin aplicar y la documentación mintiendo.
- **Riesgo si no se toca:** el evento arranca con la unidad vieja —reinicios en
  bucle ante un error de configuración y sin el grupo `lp` para escribir en la
  impresora—, o con el servicio `enabled` antes de tiempo, que con un corte de
  luz arranca solo y gasta papel.
- **Propuesta:** en el deploy, después del `git pull`, correr
  `sudo ./instalar.sh` y comprobar la unidad viva con
  `systemctl cat ruleta | grep -E "RestartPreventExitStatus|SupplementaryGroups"`;
  enseguida, `systemctl is-enabled ruleta` → `disabled` si el Paso 13 aún no se
  ha hecho.
- **Estado:** **cerrada** el 2026-09-11: el deploy no se limitó al `git pull`, también corrió `sudo ./instalar.sh` (código 0), que es quien copia la unidad a `/etc/systemd/system/`. Verificado en la Pi por un agente independiente: `grep -c RestartPreventExitStatus=2 /etc/systemd/system/ruleta.service` → **1**, y el journal del arranque de las 22:32:48 ya trae la `Description` nueva («impresora USB o Bluetooth»).

---

## F-177 · El README §4 paso 5 manda `scp logo.png` y `logo.png` está rastreado por git

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `README.md` §4 paso 5 (línea **161**,
  `scp logo.png asadero@ruleta.local:~/ruleta/`) frente al §4 paso 1
  (líneas 108-110, el aviso de actualización con `git pull`).
- **Qué pasa:** `logo.png` **sí lo rastrea git**. Después de copiarlo con `scp`,
  el camino de actualización que el propio README documenta en el paso 1
  (`cd ~/ruleta && git pull`) se queja, y el procedimiento de deploy con
  `git checkout --` **borraría el logo real del restaurante**. El aviso del
  paso 1 solo nombra `config.json`.
- **Por qué es residual:** hoy no hay pérdida posible: la Pi todavía no tiene un
  `logo.png` modificado.
- **Riesgo si no se toca:** el día que el usuario ponga el logo del asadero, el
  siguiente deploy se lo lleva sin avisar y los boletos salen con el logo
  provisional.
- **Propuesta:** arreglo mínimo, una frase: nombrar también `logo.png` en el
  aviso del §4 paso 1 («si editaste `config.json` **o `logo.png`**, guárdalos
  fuera del repositorio antes del `git pull`»).
- **Estado:** abierta.

---

## F-178 · El golden de la §7.5 no cubre el tercer caso: con el servicio corriendo también son 7 `[ok]`

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `docs/planes/fase-2-impresora.md` §7.5 (comentario del golden
  `grep -c "\[ok\]"`) y `ruleta/__main__.py` líneas 417-419.
- **Qué pasa:** el golden dice **8** líneas `[ok]`, y **7** si la impresora no
  contesta al estado. Falta el tercer caso, que es el **más probable durante el
  evento**: con el servicio corriendo, el diagnóstico no le pregunta nada a la
  impresora para no interferir e imprime
  `[--] el servicio 'ruleta' está corriendo`; el conteo también es **7**. El
  `README.md` §9 sí lo explica; el golden del plan no.
- **Por qué es residual:** el golden no está mal calculado, está incompleto; y
  durante la Fase 2 el servicio va detenido (decisión **D6**), así que el caso
  no se da hasta el Paso 13.
- **Riesgo si no se toca:** quien corra el diagnóstico con el servicio ya
  arrancado lee 7 donde el plan promete 8 y cree que hay una regresión.
- **Propuesta:** añadir la tercera línea al comentario del golden, junto con la
  corrección de **F-140**. Paso 14.
- **Estado:** abierta. **Medido el 2026-09-11:** el caso real fue un **cuarto** que tampoco estaba escrito —la impresora contesta y avisa de **poco papel**: 7 `[ok]` y un `[??]`—. La §7.5 del plan ya lista los cuatro. Ver **F-186**.

---

## F-179 · **F-157** lista `CLAUDE.md` entre «todos los archivos tocados en 2b» y `CLAUDE.md` no está modificado

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `docs/fichas.md`, **F-157**, campo «Dónde».
- **Qué pasa:** esa lista enumera `CLAUDE.md`, y `git status` lo muestra **sin
  modificar** (coherente con **F-169**, que lo deja igual a propósito porque
  tocarlo exige visto bueno del usuario). El resto de la lista está escrita con
  globs sueltos (`ruleta/*.py` y `tests/*.py` incluyen archivos intactos), así
  que se lee como enumeración aproximada de dónde se midió, no como el conjunto
  de archivos cambiados.
- **Por qué es residual:** **F-157** es una nota de verificación cerrada de
  entrada, y lo que afirma —ni BOM ni CRLF— sigue siendo cierto de todos esos
  archivos, tocados o no.
- **Riesgo si no se toca:** que el agente de commit tome esa lista como el
  conjunto de rutas permitido y arrastre al commit archivos intactos, o que dé
  por hecho que `CLAUDE.md` cambió en 2b.
- **Propuesta:** dejarlo anotado aquí —**el agente de commit añade por ruta, no
  por esa lista**— y, si se toca **F-157**, aclarar que enumera dónde se midió.
- **Estado:** abierta (aviso para el paso de commit).

---

## F-180 · **F-169** reconfirmada por el escéptico 2b: `CLAUDE.md` §«Contexto del producto» sigue viejo

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `CLAUDE.md` §«Contexto del producto»; ficha **F-169**.
- **Qué pasa:** no se duplica el contenido de **F-169**, que ya lo describe
  entero. Solo se deja constancia de que, vuelto a mirar hoy tras las mediciones
  del 2026-09-11, sigue igual: dice «impresora térmica Bluetooth AOMU My-A1» y
  que «los valores de impresora (canal, tabla de acentos, corte) están sin
  confirmar en hardware real», cuando ya están confirmados (tabla 19 / `cp858`,
  48 columnas, corte automático y zumbador) y el transporte principal es **USB**.
- **Por qué es residual:** está fuera del alcance de 2b y **tocar `CLAUDE.md`
  exige visto bueno del usuario**.
- **Riesgo si no se toca:** es el archivo que se lee al inicio de cada sesión,
  así que cada agente nuevo arranca con el hardware equivocado.
- **Propuesta:** la de **F-169**: que el orquestador lo lleve al usuario en el
  cierre de la Fase 2 con el texto de reemplazo ya redactado.
- **Estado:** **resuelta** el 2026-09-11 ~23:20, junto con **F-169** y con el
  visto bueno del usuario: `CLAUDE.md` §«Contexto del producto» ya describe la
  impresora por **USB** (clon POS-80, emulación EPSON) con el **Bluetooth de
  respaldo**, y lista los valores **confirmados en papel**. Ver el estado de
  **F-169** para el detalle de lo que quedó escrito.

---

## F-181 · Duplicación hermana de **F-168**: la prueba `S_ISCHR` vive en dos sitios

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `ruleta/escpos.py`, `es_dispositivo_caracteres` (línea **131**), y
  `ruleta/__main__.py`, `revisar_ruta_impresora` (línea **332**).
- **Qué pasa:** las dos deciden por su cuenta si la ruta es un dispositivo de
  caracteres, cada una con su propio `stat.S_ISCHR`. Hoy coinciden.
- **Por qué es residual:** no hay defecto de conducta; es la misma regla escrita
  dos veces, igual que la de **F-168** con los bits del estado.
- **Riesgo si no se toca:** el día que una acepte también enlaces simbólicos o
  dispositivos de bloque, el **diagnóstico** y el **transporte** dirán cosas
  distintas de la misma ruta: el diagnóstico en verde y el boleto sin consulta
  de papel, o al revés.
- **Propuesta:** que `revisar_ruta_impresora` use
  `escpos.es_dispositivo_caracteres` (que `cmd_diagnostico` ya llama dos líneas
  después), o dejar en las dos un comentario que se citen mutuamente. Fase 3,
  junto con **F-168**.
- **Estado:** abierta.

---

## F-182 · Conducta nueva medida: con la impresora ausente, el diagnóstico interno de `instalar.sh` sale con código 1

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `instalar.sh` línea **93** (bloque «Diagnóstico», con `|| true`) y
  `ruleta/__main__.py` (`revisar_ruta_impresora` más `return 0 if ok else 1`).
- **Qué pasa:** complementa **F-164** y **F-165**. Sin impresora conectada, el
  diagnóstico que corre **dentro** del instalador termina con **código 1** y un
  `[!!] no existe la ruta de la impresora`; antes de 2b salía **0** con un
  `[--]`. Lo tapa el `|| true` de la línea 93, así que la instalación sigue
  adelante.
- **Por qué es residual:** el instalador no aborta, y el `[!!]` es información
  correcta (la impresora de verdad no está), no un fallo del instalador.
- **Riesgo si no se toca:** ninguno mientras el `|| true` siga ahí; **quitarlo
  convertiría una impresora desconectada en una instalación abortada**. Y, con
  **F-164** encima, ese `[!!]` puede ser espurio por la carrera de `udev`.
- **Propuesta:** saberlo antes del deploy, **no quitar el `|| true`** y mirar
  ese bloque la primera vez que se corra en la Pi.
- **Estado:** abierta (informativa, mirar en el deploy). **Medido en el deploy (2026-09-11):** con la impresora presente y encendida, `sudo ./instalar.sh` salió con **código 0**. El caso de esta ficha —instalar sin la impresora conectada— sigue sin medir.

---

## F-183 · Estilo, sin acción: la prueba nueva de `es_dispositivo_caracteres` usa un `lambda`

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** `tests/test_escpos.py`,
  `test_solo_un_dispositivo_de_caracteres_es_dispositivo`:
  `stat_fn = lambda ruta: SimpleNamespace(st_mode=modos[ruta])`.
- **Qué pasa:** si el repositorio prefiere un `def` anidado, es equivalente.
- **Por qué es residual:** cosmético puro; no cambia ningún conteo —la suite
  sigue en 194 pruebas, 70 de ellas en `tests/test_escpos.py`— ni ningún golden.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejarlo como está, o cambiarlo cuando se vuelva a tocar el
  archivo.
- **Estado:** cerrada de entrada (sin acción).

---

## F-184 · Verificado por el escéptico 2b: 56 mutaciones, goldens del README, códigos de salida, instalador idempotente y LF/BOM

- **Fecha:** 2026-09-11
- **Origen:** escéptico 2b
- **Dónde:** todo el alcance de la sub-fase 2b.
- **Qué pasa (para que nadie lo repita):**
  1. Las **8 mutaciones obligatorias** del Paso 12 (a) y las **8** del (b)
     quedan todas en **rojo**, más **40 mutaciones adicionales** sobre
     `instalar.sh`, `ruleta.service`, `config.json`, `ruleta/ticket.py`,
     `ruleta/app.py` y las tres funciones puras del diagnóstico: **56 en
     total**, todas medidas por copia en el scratchpad.
  2. Los conteos golden del `README.md` dan **0/0/0/0/4/5**, tal como dice el
     plan.
  3. Los **únicos códigos 2** del programa son errores de configuración
     (`cargar_config` e `impresora_desde_args`), así que
     `RestartPreventExitStatus=2` no deja el kiosco muerto por un fallo
     transitorio: el inventario ocupado sale con **1** y el GPIO también.
  4. `instalar.sh` leído como si se corriera **dos veces**: no hay `cat >>`, ni
     `rm`, ni `usermod -G`; todo es `cat >` o `-aG`. El único efecto de la
     segunda pasada es el `systemctl enable` del paso 7/7 (ver **F-176**).
  5. **LF y sin BOM** en los 15 archivos tocados, y `.gitattributes`
     (`text eol=lf`) cubre `.sh`, `.service`, `.py`, `.json` y `.md` pese a
     `core.autocrlf=true`.
  6. El boleto de prueba renderizado a **48 columnas**: ninguna línea del bloque
     de acentos se pasa, y el `[BEEP]` sale con `beep=true`.
  7. El `README.md` §5 dice la verdad: `servicio_activo()` se llama en
     `reporte --imprimir`, `liberar`, `reiniciar` y **dos veces** en
     `diagnostico`, y **no** en `probar-impresora`.
- **Por qué es residual:** nota de verificación; no pide ningún cambio.
- **Riesgo si no se toca:** ninguno.
- **Propuesta:** dejar constancia para no volver a auditar lo mismo.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-185 · La Fase 2 dejó el servicio `active`, y el Paso 13 pide devolverlo a `enabled` + `inactive`

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · escriba, confrontando el informe del deploy con el plan
- **Dónde:** `docs/planes/fase-2-impresora.md` Paso 13 (bloque «Al terminar,
  devolver el servicio al estado en que lo dejó la Fase 1») y §9 («Lo que esta
  fase entrega a la siguiente»), frente a lo medido en la Pi.
- **Qué pasa:** el Paso 13 termina con `sudo systemctl stop ruleta` y espera
  `enabled` + `inactive`, que es el estado en que la Fase 1 dejó la Pi. El
  deploy arrancó el servicio, lo verificó y **lo dejó corriendo**: medido dos
  veces esa noche, por el agente de deploy al cerrar y por el verificador en
  vivo, `systemctl is-active ruleta` → `active`, `is-enabled` → `enabled`,
  `SubState` → `running`, `NRestarts=0`.
- **Por qué es residual:** no es un fallo del software ni del deploy —el
  servicio corriendo es justo lo que se quería demostrar—, es el paso de cierre
  que faltó. Y el estado actual es el **seguro** en un sentido: sin botones
  cableados y con `modo_habilitar: "mantener"`, la Pi no sortea nada sola.
- **Riesgo si no se toca:** el kiosco está vivo. En cuanto la Fase 3 cablee los
  botones, cualquier pulsación de prueba **gasta papel y consume un folio**; y
  si alguien apaga la Pi para cablear, systemd lo vuelve a arrancar solo al
  encenderla.
- **Propuesta:** antes de empezar la Fase 3, `sudo systemctl stop ruleta` (y
  `sudo systemctl disable ruleta` antes de apagar la Pi para cablear, como
  manda el aviso 1 de la Fase 3). Ya está anotado en el plan: §0 bitácora Paso
  13, nota del deploy, §9 y aviso 1 de la Fase 3.
- **Estado:** **cerrada** el 2026-09-11 ~23:20, **no por ejecución sino por decisión del orquestador**: **el kiosco queda corriendo por USB**, con el servicio `active` y `enabled`. Por tanto el final del Paso 13 («devolver el servicio al estado en que lo dejó la Fase 1») y el golden **§7.9** quedan **SUPERADOS**, y así consta en `docs/planes/fase-2-impresora.md` (estado global, bitácora filas 13 y 13-bis, nota «Reprueba post-2b y cierre en papel», Paso 13, §7.9 y §9) y en `docs/actas/2026-09-11-fase-2.md` (§3, §7, §8 y §10). **Lo que la decisión NO cambia, y sigue siendo obligatorio en la Fase 3:** antes de apagar la Pi para cablear los botones, `sudo systemctl stop ruleta` **y** `sudo systemctl disable ruleta`, y `sudo systemctl enable ruleta` al volver; con el servicio arriba y los botones cableados, **cada pulsación de prueba gasta papel y consume un folio** (para probar sin gastar, `--impresora vista`). **Nota del 2026-09-15 (Fase 3, ejecutada):** se cablearon los botones y la receta se cumplió **a medias**: el servicio se **detuvo** (`SIGTERM` a las 11:47:03) pero **nunca se deshabilitó** —`is-enabled` seguía en `enabled`—. No llegó a morder porque **la Pi no se apagó**: el archivo de hechos registra un solo arranque, el de las 11:44:42. Lo otro que anunciaba esta ficha **sí pasó, y era el precio previsto**: las tres jugadas de prueba gastaron papel y **tres folios** (ficha **F-243**: hay que correr `reiniciar --si` antes del lunes 21). Evidencia: `docs/actas/2026-09-15-fase-3.md` §3, §5 y §8.

---

## F-186 · El diagnóstico da 7 `[ok]` y un `[??]` de poco papel: un cuarto caso que ningún documento contemplaba

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · escriba, confrontando la salida real del deploy con el plan
- **Dónde:** `docs/planes/fase-2-impresora.md` §7.5 y §6 (fila «Conteo de líneas
  `[ok]`»), y las fichas **F-140** y **F-178**.
- **Qué pasa:** el plan anunciaba **8** `[ok]` tras la sub-fase 2b, con dos
  excepciones escritas: 7 si la impresora no contesta (F-140) y 7 con el
  servicio corriendo (F-178). Lo que salió de verdad en la Pi fue un tercer
  camino que nadie había escrito: **la impresora contesta y avisa de poco
  papel**, así que la octava línea sale como
  `[??] la impresora reporta poco papel: ten listo el rollo de repuesto` y el
  conteo es **7 `[ok]`**, con `EXIT=0` y cero `[!!]`.
- **Por qué es residual:** el programa hace exactamente lo que debe —`[??]` es
  aviso, no fallo, y por eso el código de salida es 0—; lo que estaba
  incompleto era el golden.
- **Riesgo si no se toca:** quien compare por igualdad contra el `8` del plan
  lee 7 y declara una regresión que no existe.
- **Propuesta:** hecho en esta misma pasada: la §7.5 y la §6 del plan de la
  Fase 2 listan ahora los **cuatro** casos con su conteo. Falta el mismo
  arreglo en los documentos de la **Fase 1** (F-140), que están fuera de
  alcance.
- **Estado:** **resuelta** el 2026-09-11 ~23:20. La parte de la Fase 2 ya
  estaba corregida esa misma noche; la parte de la **Fase 1** se cerró en el
  cierre de fase, con notas fechadas en el plan (§7, §6 y §9) y en el acta de
  la Fase 1, sin borrar el `6` histórico (ver **F-140**). Los cuatro casos del
  conteo —8 con papel de sobra; 7 + `[??]` de poco papel (el medido); 7 + `[??]`
  si el firmware no contesta; 7 + `[--]` con el servicio corriendo— quedan
  escritos donde alguien los va a buscar.
- **Nota del 2026-09-15 (Fase 4a).** El segundo caso de ese conteo —«7 + `[??]`
  de poco papel»— era el **medido**, pero el aviso era **falso** (**F-190**). Con
  la lectura fresca y la máscara estricta, en esta impresora ese camino **ya no
  se dispara**: haría falta una con sensor de papel de verdad. El censo del
  **código** sigue siendo **8** (`grep -c "\[ok\]" ruleta/__main__.py`; las dos
  ramas que añade la Fase 4a —tapa abierta y error de impresora— son de fallo,
  `[!!]`, que pasan de 18 a 20). El censo de la **salida** con la impresora sana
  debería volver a ser **8 aciertos**, pero **eso hay que medirlo en la Pi**
  (Paso 10 del plan de la Fase 4a) y escribir aquí el número que salga: **al
  cerrar este cambio todavía no se había medido**.

---

## F-187 · El deploy no midió tres goldens de la §7 ni los grupos del proceso del Paso 13

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · escriba, cotejando la §7 del plan con los informes del
  deploy y del verificador en vivo
- **Dónde:** `docs/planes/fase-2-impresora.md` §7.3 y Paso 13.
- **Qué pasa:** de los goldens de la fase quedaron cuatro sin medir después del
  deploy:
  1. `ls /etc/udev/rules.d/ | grep -c impresora` → **1** (el que detectaría una
     regla duplicada; el verificador leyó el contenido de la regla buena, pero
     no contó cuántos archivos de impresora hay).
  2. `stat -c "%a %U %G" /dev/usb/lp0` → `660 root lp` (se midió a mano la
     noche del 2026-09-11, no después del deploy).
  3. `cat /sys/class/usbmisc/lp0/device/ieee1284_id` (igual: medido esa noche,
     no vuelto a comprobar).
  4. Los grupos que systemd le dio al proceso:
     `grep -E "^(Uid|Gid|Groups):" /proc/$(systemctl show -p MainPID --value ruleta)/status`
     frente a `getent group lp`. Es la pregunta que el Paso 4 dejó abierta y
     que el Paso 13 existía para cerrar.
- **Por qué es residual:** los cuatro están **implícitamente** respaldados por
  algo más fuerte: el servicio, corriendo como `asadero` bajo systemd, abrió
  `/dev/ruleta-impresora` en `r+b`, le preguntó por el papel y le imprimió el
  inventario. Si el grupo `lp` no hubiera llegado al proceso, eso habría fallado
  con `Permission denied`.
- **Riesgo si no se toca:** una regla `udev` duplicada de un intento anterior
  pasaría inadvertida, y el acta cierra la fase sin la medición directa que el
  propio plan pedía.
- **Propuesta:** son cuatro `ssh` de solo lectura; correrlos en la misma sesión
  en que se apague el servicio (F-185) y pegarlos en el acta.
- **Estado:** abierta (cuatro mediciones de solo lectura).

---

## F-188 · Nadie ha vuelto a correr `probar-impresora` después de 2b: el papel de 48 columnas y el pitido siguen sin verse

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · escriba, confrontando el diff con lo medido en papel
- **Dónde:** `ruleta/ticket.py` (`boleto_prueba`), `config.json`
  (`"beep": true`), Paso 7 del plan y fichas **F-113** y **F-159**.
- **Qué pasa:** el commit `61adf96` cambia dos cosas que **solo se ven en el
  papel**: las líneas de acentos del boleto de prueba ahora van partidas en dos
  para caber en 48 columnas, y el pitido queda activado. Las dos fotos que
  existen son **anteriores** al cambio (inventario 19:22 y prueba 19:25). Del
  deploy quedó pendiente lo que el propio informe llama «requiere al usuario»:
  **confirmar que salió el boleto de inventario de las 22:32 y que se oyó un
  pitido**.
- **Por qué es residual:** hay goldens que comparan el bloque de acentos por
  igualdad a 32, 42 y 48 columnas, y el `[BEEP]` sale en la vista previa; lo
  que falta es el hardware diciendo lo mismo.
- **Riesgo si no se toca:** se llega al evento sin haber visto nunca impresa la
  versión que está desplegada, y sin saber si el pitido por boleto molesta en la
  sala.
- **Propuesta:** con el servicio detenido (que además hay que detenerlo,
  F-185): `cd ~/ruleta && python3 -m ruleta probar-impresora`, mirar el papel y
  decidir sobre `beep` (F-160). Y preguntarle al usuario por el boleto de las
  22:32.
- **Estado:** **resuelta** el 2026-09-11 ~23:20 con la reprueba post-2b, **confirmada en papel por el usuario**: «todas las pruebas salieron y se escucharon los beeps». Cubre las tres cosas que faltaban: el **boleto de prueba con las cuatro tablas de acentos en dos renglones, sin líneas partidas** (cambio (f) de 2b, visto por fin impreso); el **boleto de inventario de arranque**; y **un pitido al final de cada boleto** (`"beep": true` operativo por USB). Queda escrito en `docs/actas/2026-09-11-fase-2.md` §10 y en la bitácora del plan (fila 13-bis). **Lo que esta ficha NO cierra:** el cambio de rollo (**F-190**, abierta) y la decisión de dejar `beep` en `true` durante toda la semana del evento (**F-160**, abierta: el usuario ya los oyó y los aprobó el 2026-09-11, pero la vigilancia para la semana del evento sigue en pie).

---

## F-189 · Dos respaldos de `config.json` viven en la Pi sin destino, y uno tiene la fecha equivocada

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · escriba, cotejando el `git status` de la Pi con el informe del deploy
- **Dónde:** en la Pi: `~/ruleta/config.json.bak-2026-09-12` y
  `~/config.json.pi-antes-deploy`. Fichas relacionadas: **F-103** (respaldos sin
  destino) y **F-111** (fechas «2026-09-12» que en realidad son del 11).
- **Qué pasa:** el primero lo dejó la sesión de aquella noche **dentro del
  repositorio** y con el nombre equivocado —se creó el 2026-09-11, no el 12— y
  sigue ahí: el verificador en vivo midió `git status --porcelain` en la Pi y
  lo único que sale es `?? config.json.bak-2026-09-12`. El segundo lo creó el
  agente de deploy antes de tocar nada (`cp ~/ruleta/config.json
  ~/config.json.pi-antes-deploy`, 2537 bytes) y está fuera del repositorio, que
  es lo correcto.
- **Por qué es residual:** ninguno estorba: el `.bak` no está rastreado y no
  entra en ningún `git pull`.
- **Riesgo si no se toca:** el `git status` de la Pi nunca sale limpio, así que
  el golden `git status --porcelain | wc -l` obliga a explicar la línea cada
  vez; y dentro de medio año nadie sabrá cuál de los dos archivos es el bueno ni
  de qué día es.
- **Propuesta:** en el cierre, mover el `.bak` fuera del repositorio con su
  fecha real (`mv ~/ruleta/config.json.bak-2026-09-12
  ~/config.json.bak-2026-09-11`) y decidir si el otro se conserva. Es
  `mv`, no `rm`: no se borra nada sin que el usuario lo diga.
- **Estado:** abierta.

---

## F-190 · El aviso de «poco papel» del 2026-09-11 era FALSO: el programa leía la respuesta de otra pregunta (y el rollo, ese sí, hay que tenerlo de repuesto)

- **Fecha:** 2026-09-11
- **Origen:** Fase 2 · escriba, leyendo el diagnóstico y el journal del deploy
- **Dónde:** salida del diagnóstico en la Pi
  (`[??] la impresora reporta poco papel: ten listo el rollo de repuesto`) y
  journal del arranque de las 22:32:48
  (`WARNING ruleta.escpos: La impresora /dev/ruleta-impresora reporta poco
  papel: cambia el rollo pronto`).
- **Qué pasa. CORRECCIÓN del 2026-09-15 (Fase 4a): NO fue el sensor.** La AOMU
  My-A1 repite sin parar por el endpoint de lectura el último byte de estado que
  fijó su firmware (~21 kB/s), así que leer un byte después de un `DLE EOT`
  devuelve la respuesta a la **pregunta anterior**. El `0x16` que se leía en la
  ranura del papel es la respuesta **sana** de `DLE EOT 1` (bit 2 = pin 3 del
  cajón; bit 3 = 0, **en línea**), y la comparación suelta `papel & 0x0C` se
  conformaba con **uno** de los dos bits de la pareja. Y lo medido el
  **2026-09-15**: `DLE EOT 4` contesta **`0x12` incluso con el rollo fuera**, o
  sea que en este clon **no hay sensor de papel útil en esa pregunta** y
  `BITS_SIN_PAPEL` no se enciende nunca; la única que se entera es `DLE EOT 2`
  (`0x32`). Evidencia: `docs/actas/2026-09-15-hechos-medidos-fase-4a.md`.
  **Redacción original del 2026-09-11, que se conserva:** «el sensor *near-end*
  de la impresora dice que al rollo le queda poco, y esto se midió **dos veces**
  la misma noche: en el diagnóstico y en el arranque del servicio. Entre las
  pruebas de aquella noche y el inventario del deploy ya se gastó papel.»
- **Por qué es residual:** no bloquea nada. El programa avisa y sigue
  imprimiendo, que es lo correcto: `[??]` no cambia el código de salida.
- **Riesgo si no se toca:** el evento dura una semana. Si el rollo se acaba a
  media noche y el firmware **no** contesta en ese momento, el folio se gasta y
  el premio se descuenta sin boleto (README §5, punto 8).
- **Propuesta:** poner rollo nuevo antes del evento y tener al menos uno de
  repuesto junto a la Pi. De paso, cambiar el rollo es la única forma de probar
  de verdad el camino «sin papel» que sigue sin medirse (**F-091**).
- **Estado:** abierta (compra / acción del usuario). **Nota del 2026-09-15 (Fase 3):** el rollo **se acabó de verdad**. Fue en una prueba deliberada de las 13:29 —el usuario dejó la impresora sin papel a propósito— y **lo repuso él mismo entre las 13:31 y las 13:33**, con lo que la impresora soltó el boleto que tenía retenido. Así que el **rollo de hoy es nuevo**; lo que **sigue abierto es el repuesto**: tiene que haber al menos un rollo más junto a la Pi durante la semana del evento. Y el **riesgo que esta ficha anunciaba ya no es una hipótesis**: se midió que, con el papel agotado, el folio se gasta y el premio se descuenta **sin boleto** —y no porque el firmware no conteste, sino porque contesta tarde— (**F-091** actualizada, **F-250** nueva). **Nota del 2026-09-15 (Fase 4a):** el **diagnóstico queda cerrado** —el aviso era un artefacto de lectura, no un sensor— y el defecto de código está **arreglado en el cambio de esta fase** (lectura fresca y `DLE EOT 2`; **F-250**). Con la máscara estricta, en esta impresora el aviso de «poco papel» **ya no puede salir**: haría falta una con sensor de verdad. Lo único que sigue vivo de esta ficha es **tener un rollo de repuesto junto a la Pi** durante la semana del evento.
- **Nota de cierre del 2026-09-15 (Fase 4a, tras el deploy de las 21:26:42).**
  **El aviso falso desapareció, y está contado.** Con
  `2a0aba3e01dcd15878579f1d02a64457b1834046` desplegado en la Pi y el servicio
  reiniciado a las **21:26:42**, las apariciones de «poco papel» en el journal
  desde ese restart son **0** —incluidas las dos jugadas sin papel de las 21:32,
  que dijeron «no tiene papel» y ninguna otra cosa—. Antes salía en **cada
  arranque** desde el 2026-09-11 y había aparecido **15 veces** en el log del
  kiosco. Con la máscara estricta (`(papel & BITS_POCO_PAPEL) == BITS_POCO_PAPEL`)
  y la lectura fresca, en esta impresora ese aviso **ya no puede salir**: haría
  falta una con sensor de verdad. Evidencia: `docs/actas/2026-09-15-fase-4a.md`
  §7.2 y §8. **Parte de diagnóstico y de código: cerrada.** **Sigue abierta solo
  la compra**: un rollo de repuesto junto a la Pi durante la semana del evento.

---

## F-191 · Referencias de línea viejas FUERA de la §6: el Paso 8 y la trampa 18 siguen con los números de antes de 2b

- **Fecha:** 2026-09-11
- **Origen:** lente docs fase 2
- **Dónde:** `docs/planes/fase-2-impresora.md`, Paso 8 (tabla de acentos) y §5
  trampa 18. Familia: **F-095** y **F-108**, las dos **abiertas**.
- **Qué pasa:** el refresco del Paso 14 volvió a medir la §6 entera, y su
  encabezado lo dice: «**todas las de abajo se volvieron a medir con
  `grep -n`**». Ese barrido **no salió de la §6**, y fuera de ella quedaron
  números de antes de 2b. Medido hoy contra `61adf96`:

  - Paso 8: «Las parejas válidas salen de `CODECS_TABLA` (`ruleta/escpos.py`,
    línea **50**)» — real **54**.
  - §5 trampa 18: «`lineas_antes_corte_por_defecto`, línea **67**» — real **77**.
  - §5 trampa 18, en la misma frase y **no** señalada por el lente: «`GS V 66 0`
    (`ruleta/escpos.py`, línea **43**)» — real **47**.

  Como la §6 sí acaba de corregir esas tres anclas, hoy el plan se contradice
  consigo mismo: la §6 dice **54 / 47 / 77** y el Paso 8 y la trampa 18 dicen
  **50 / 43 / 67**.
- **Por qué es residual:** caen dentro del alcance de **F-095** y **F-108**, que
  siguen abiertas y hablan justamente de los desfases de línea fuera del mapa de
  anclas. No se pidieron corregir en esta ronda.
- **Riesgo si no se toca:** menor que en la §6 —estos números son ilustrativos y
  no disparan el «detenerse y preguntar» del mapa de anclas—, pero quien vaya a
  tocar el corte o la tabla de códecs leerá dos líneas distintas para la misma
  constante y no sabrá cuál creer.
- **Propuesta:** barrerlas de una sola pasada cuando se cierren **F-095** y
  **F-108**, con el mismo criterio del Paso 14: re-grep y número real, o decir
  que el texto ya no existe.
- **Estado:** abierta.

---

## F-192 · La contabilidad de fichas que cierra el censo de F-166 no cuadra entre el plan y `docs/fichas.md`

- **Fecha:** 2026-09-11
- **Origen:** lente docs fase 2
- **Dónde:** `docs/planes/fase-2-impresora.md` §6, bloque citado que encabeza la
  tabla de anclas; y el **Estado** de **F-166** en `docs/fichas.md`.
- **Qué pasa:** el mismo cierre se cuenta de dos maneras distintas:

  - el plan dice que el refresco de la §6 «cierra el censo de la ficha
    **F-166** y las fichas **F-148**, **F-149** y **F-151**»;
  - el Estado de **F-166** dice «Con ella se cierran **F-131**, **F-148**,
    **F-149**, **F-151** y **F-109**».

  El plan se queda corto en dos (**F-131** y **F-109**) y **ninguna de las dos
  listas menciona F-150**, que también quedó **cerrada** ese día en el Paso 14,
  por la reescritura de la justificación de la decisión **D7**.
- **Por qué es residual:** ninguna ficha quedó mal cerrada; lo que falla es el
  recuento, que vive en dos sitios y no se puso de acuerdo.
- **Riesgo si no se toca:** quien audite el cierre de la Fase 2 contando fichas
  desde el plan se encontrará tres cerradas que el plan no reclama, y no sabrá
  si se cerraron de más o si al plan le falta texto.
- **Propuesta:** dejar **una sola lista canónica** —la del Estado de **F-166** en
  `docs/fichas.md`, que es la más completa—, añadirle **F-150**, y que el plan
  remita a ella en vez de repetirla con otro contenido.
- **Estado:** abierta.

---

## F-193 · El golden «7.1 Red y acceso» del acta mezcla una medición de la Fase 1 con las del deploy

- **Fecha:** 2026-09-11
- **Origen:** lente docs fase 2
- **Dónde:** `docs/actas/2026-09-11-fase-2.md` §3, fila «7.1 Red y acceso» de la
  tabla «Los goldens de la §7 del plan, uno por uno».
- **Qué pasa:** la fila dice «**Medido.** `hostname` → `ruleta`; la Pi entró sola
  en el `192.168.137.x` del punto de acceso», dentro de una tabla que repasa los
  goldens **después del deploy**. El dato del `hostname` no sale de ahí: viene de
  la sesión de la tarde (Fase 1) y de la §0-bis. El verificador en vivo **no
  corrió `hostname`** durante el deploy.
- **Por qué es residual:** no es falso —el nombre de equipo es `ruleta` y está
  medido—, pero junta bajo una sola casilla dos mediciones de momentos distintos,
  en una tabla que promete ser el estado tras el deploy.
- **Riesgo si no se toca:** es el mismo patrón que **F-187** ya señala en las
  filas 7.3, donde sí se distingue («Medido a mano el 2026-09-11, no vuelto a
  comprobar tras el deploy»). Aquí no se distingue, así que la fila seguirá
  diciendo «Medido» aunque el nombre de equipo cambie.
- **Propuesta:** partir la casilla, o marcar la parte del `hostname` como
  «medido en la Fase 1, no vuelto a comprobar tras el deploy», con la misma
  redacción que ya se usa en las filas 7.3.
- **Estado:** abierta.

---

## F-194 · El zumbador propio en un GPIO era la única anotación del acta sin ficha: ésta es su ficha

- **Fecha:** 2026-09-11
- **Origen:** lente docs fase 2
- **Dónde:** `docs/actas/2026-09-11-fase-2.md` §7, viñeta «Idea sin medir y sin
  decidir (queda anotada para no perderla)».
- **Qué pasa:** el acta anota la idea de poner un **zumbador propio en un GPIO**
  de la Pi en vez de depender del `ESC B` de la impresora. El argumento, tal como
  lo deja el acta: hoy el aviso sonoro solo existe **cuando hay boleto**, y un
  zumbador en la Pi podría avisar también **cuando algo falla** (sin papel,
  impresora apagada), que es justo cuando el mesero no está mirando el LED. El
  acta es explícita en que no hay hardware comprado, ni pines elegidos, ni
  código. Era la **única** anotación del acta sin número de ficha, o sea la única
  que no sobrevive a que alguien cierre la sesión.
- **Por qué es residual:** es una idea, no un defecto: no bloquea la Fase 2 ni
  contradice al código.
- **Riesgo si no se toca:** se pierde. Las actas se leen una vez; las fichas son
  lo que se repasa al empezar cada fase.
- **Propuesta:** decidirla al planear la **Fase 3** (botones y LED), que es cuando
  ya habrá GPIO cableado y añadir un pin más sale barato. Si se descarta, cerrar
  esta ficha anotando el motivo. Nota: la viñeta del acta todavía **no** cita
  este número; conviene añadírselo cuando el acta se vuelva a tocar.
- **Estado:** abierta (idea; decisión del usuario en la Fase 3). **Actualizada el 2026-09-15:** la Fase 3 **se ejecutó** —en vivo, sin plan previo, solo cableado de los dos botones— y **esta idea no se habló ni se decidió**. Sigue abierta y **cambia de dueño**: ya no es «decisión del usuario en la Fase 3» sino **decisión del usuario antes del evento**. Dato nuevo que la hace más pertinente: la instalación quedó **sin LED** (ficha **F-240**), así que hoy el mesero **no tiene ningún aviso** —ni visual ni sonoro— cuando algo falla; el único pitido que existe es el de la impresora al terminar un boleto. Evidencia: `docs/actas/2026-09-15-fase-3.md` §6.

---

## F-195 · El camino Bluetooth nunca se ha ejercido en hardware y la §8 del acta no lo lista como respaldo sin probar

- **Fecha:** 2026-09-11
- **Origen:** lente docs fase 2
- **Dónde:** `docs/actas/2026-09-11-fase-2.md` §5, desviación 9 (donde sí se
  dice) y §8, tabla de riesgos abiertos (donde falta con ese encuadre). En la Pi:
  `config.json` con `impresora.tipo = "archivo"` y
  `impresora.mac = "00:00:00:00:00:00"`.
- **Qué pasa:** dato informativo, ya señalado por el verificador en vivo y
  consistente con la memoria del proyecto: el `config.json` de la Pi sigue con
  `tipo=archivo` y la MAC de relleno, `herramientas/emparejar.sh` nunca se corrió
  y **el camino Bluetooth no se ha ejercido nunca en hardware real**. La §5,
  desviación 9, lo cuenta bien («El respaldo por Bluetooth se saltó con razón:
  el USB funcionó a la primera»). La §8 sí trae una fila sobre la MAC de relleno,
  pero encuadrada al revés —«quien vuelva a poner `"tipo": "bluetooth"` sin
  emparejar deja el servicio en `failed`», gravedad **Baja**, remitiendo a
  **F-004**—, que describe la conducta **correcta** desde 2b. Lo que no aparece
  en ninguna fila de riesgos es el fondo del asunto: **el plan B no está
  probado**.
- **Por qué es residual:** saltarse el Paso 10 fue lo correcto y está bien
  justificado, y el USB funciona. Es un hueco de encuadre en la tabla de riesgos,
  no un error de hecho.
- **Riesgo si no se toca:** si el USB falla durante la semana del evento, el
  respaldo que todos suponen disponible es un camino que nunca ha impreso una
  sola línea en este hardware; habría que emparejar y depurar con el evento
  encima.
- **Propuesta:** añadir a la §8 una fila «**camino de respaldo sin probar**»
  (gravedad Media) y decidir si conviene ejercerlo **una vez antes** del evento,
  con calma: correr `herramientas/emparejar.sh`, anotar la MAC y el canal reales,
  imprimir un boleto por Bluetooth y volver a dejar `tipo=archivo`.
- **Estado:** abierta.

---

## F-196 · Ortografía del fabricante: los documentos escriben «Zjiang» y el PPD medido dice «Zijiang»

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `CLAUDE.md` §«Contexto del producto» (`grep -n "Zjiang" CLAUDE.md`)
  y `docs/actas/2026-09-11-fase-2.md` §9, duda 4. El dato medido está en
  `docs/actas/2026-09-11-hechos-medidos.md` (PPD `ppd/POS80.ppd`) y en
  `docs/planes/fase-2-impresora.md` §0-bis H3.
- **Qué pasa (texto del lente, tal cual):** Ortografía del fabricante:
  `CLAUDE.md` (y la duda 4 de la §9 del acta) escriben «Zjiang ZJ-80250», pero
  el PPD medido dice Manufacturer «Zijiang» (`ModelName` sí es «ZJ-80250»). Es
  un uso ya extendido en todo el repositorio; no cambia ningún hecho técnico.
- **Por qué es residual:** es una letra en un nombre comercial que, además, ya
  está declarado como **deducción y no como medición** (ficha **F-134**). No
  afecta al código, ni a los goldens, ni a nada que salga impreso en papel.
- **Riesgo si no se toca:** casi ninguno; a lo sumo, quien busque el modelo por
  internet para comprar repuestos escribe mal el nombre.
- **Propuesta:** si algún día se toca esa parte de `CLAUDE.md`, escribir
  «Zijiang ZJ-80250» tal como lo dice el PPD, y dejar «zjiang» solo donde se cite
  el nombre del directorio del driver (`usr/share/cups/model/zjiang`). No vale la
  pena una pasada solo para esto.
- **Estado:** abierta (cosmética).

---

## F-197 · La fila 14 de la bitácora enumera «F-185 a F-190» y la misma pasada creó hasta la F-195

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-2-impresora.md` §0, bitácora, fila 14 («Cierre:
  acta desde hechos medidos, fichas y memoria»).
- **Qué pasa (texto del lente, tal cual):** Bitácora del plan de la Fase 2, fila
  14: dice «Fichas al día (nuevas **F-185** a **F-190**…)», pero F-191 a F-195
  también se crearon en la misma pasada (todas entraron en el commit `6ab9680`).
  La enumeración se quedó corta; es redacción heredada, no un hecho nuevo falso.
- **Por qué es residual:** las fichas existen y están completas en
  `docs/fichas.md`; lo que falla es el rango citado en una celda de bitácora.
  No se pierde información: se pierde el rastro de cinco números.
- **Riesgo si no se toca:** quien audite el cierre por la bitácora creerá que la
  Fase 2 produjo seis fichas nuevas y no once, y podría dar por huérfanas las
  F-191 a F-195. Es el mismo defecto que ya se anotó para la Fase 1 en **F-082**.
- **Propuesta:** cambiar el rango a «**F-185** a **F-195**» la próxima vez que se
  toque el plan.
- **Estado:** abierta.

---

## F-198 · La fila 14 de la bitácora está `[x]` aunque su propia celda dice que falta la memoria del proyecto

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-2-impresora.md` §0, bitácora, fila 14, última
  frase: «La **memoria del proyecto** la actualiza el orquestador».
- **Qué pasa (texto del lente, tal cual):** Bitácora del plan de la Fase 2, fila
  14 marcada `[x]` cuando la propia celda dice que «la **memoria del proyecto**
  la actualiza el orquestador», es decir, una parte del paso todavía no está
  hecha. Queda explícito en el texto, pero la casilla no lo refleja.
- **Por qué es residual:** no engaña a nadie que lea la celda entera —la
  salvedad está escrita ahí mismo— y cumple el encabezado de la §0, que obliga a
  que cada casilla marcada diga qué evidencia la sostiene.
- **Riesgo si no se toca:** contradice la regla del propio encabezado de la §0
  («se marcan `[x]` solo cuando el criterio de aceptación del paso se cumplió»).
  Es el mismo patrón ya anotado para la Fase 1 en **F-065**.
- **Propuesta:** usar `[~]` (o «✅ parcial», como hace el acta) hasta que el
  orquestador anote el hito en la memoria del proyecto, y entonces sí `[x]`.
- **Estado:** abierta.

---

## F-199 · La fila 13 de la bitácora está `[x]` aunque su propia celda dice que los grupos del proceso no se midieron

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-2-impresora.md` §0, bitácora, fila 13 («Arranque
  del servicio y verificación en vivo»), última frase: «**Lo único que no se
  midió:** los grupos del proceso (`/proc/<pid>/status`, ficha **F-187**,
  abierta)».
- **Qué pasa (texto del lente, tal cual):** Bitácora del plan de la Fase 2, fila
  13 marcada `[x]` mientras la celda reconoce que los grupos del proceso
  (`/proc/<pid>/status`, F-187) no se midieron. Igual que arriba: está
  declarado, pero la casilla dice cumplido.
- **Por qué es residual:** el hueco está declarado en la misma celda y tiene
  ficha propia (**F-187**), y lo que esa medición probaría —que el proceso tiene
  el grupo `lp`— ya está demostrado por la vía de los hechos: el servicio abrió
  `/dev/ruleta-impresora` y escribió en él.
- **Riesgo si no se toca:** el mismo que **F-198**: la casilla contradice la
  regla del encabezado de la §0.
- **Propuesta:** dejarla en `[~]` mientras **F-187** siga abierta, o cerrar
  F-187 con la medición y entonces sí marcar `[x]`.
- **Estado:** abierta.

---

## F-200 · El resumen del acta se lee como lista completa de lo que queda, y no lo es

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/actas/2026-09-11-fase-2.md`, viñeta **«Resultado»** del
  preámbulo (`grep -n "Lo que queda" docs/actas/2026-09-11-fase-2.md`), que es el
  resumen que precede a la §2 «Resumen del resultado».
- **Qué pasa (texto del lente, tal cual):** Resumen de la §2 del acta: «Lo que
  queda son anotaciones residuales, no bloqueos: el **cambio de rollo**
  (**F-190**) y cuatro mediciones de solo lectura (**F-187**)». La §10 del mismo
  acta enumera además F-189, F-055/F-056/F-105, F-194 y F-195, y la §8 mantiene
  F-091 y F-089 como riesgos abiertos. El resumen se lee como lista completa y no
  lo es.
- **Por qué es residual:** el acta **sí** enumera todo lo que queda, en la §8 y
  en la §10; el resumen no oculta nada, solo se queda corto donde el lector
  espera un inventario. Y las dos cosas que nombra son, efectivamente, las
  únicas con efecto directo en el evento.
- **Riesgo si no se toca:** quien lea solo el encabezado —que es lo que hace
  cualquiera que retome el proyecto tras un `/clear`— cerrará la Fase 2 creyendo
  que quedan dos pendientes y no nueve.
- **Propuesta:** añadir al final de esa frase «…; la §10 los enumera todos», o
  cambiar «Lo que queda son» por «Lo más urgente que queda son».
- **Estado:** abierta.

---

## F-201 · La decisión de dejar el kiosco corriendo no está en el archivo de hechos medidos

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/actas/2026-09-11-hechos-medidos.md` (sección «Noche del
  2026-09-11»), frente a `docs/actas/2026-09-11-fase-2.md` §10 («La decisión del
  orquestador sobre el servicio»), `docs/planes/fase-2-impresora.md` (Paso 13 y
  §7.9) y la ficha **F-185**. La regla que lo pide: `CLAUDE.md` §6, primera
  viñeta.
- **Qué pasa (texto del lente, tal cual):** La «DECISIÓN DEL ORQUESTADOR» de
  dejar el kiosco corriendo no aparece en
  `docs/actas/2026-09-11-hechos-medidos.md`, que solo registra el estado
  (`active`/`enabled`). Los documentos la etiquetan con honestidad como decisión
  y no como medición, pero la §6 de `CLAUDE.md` pide que las actas se escriban
  desde el archivo de hechos: convendría anotar también la decisión ahí.
- **Por qué es residual:** no hay ninguna afirmación falsa. El estado sí está
  medido y sí está en el archivo de hechos; lo que falta es la **decisión**, que
  además está rotulada como tal en los cuatro documentos donde aparece.
- **Riesgo si no se toca:** el archivo de hechos deja de ser la fuente única del
  cierre. Quien reconstruya la Fase 2 solo desde él verá un servicio `active` sin
  saber que quedó así **a propósito**, y podría «arreglarlo» apagándolo.
- **Propuesta:** añadir una línea a la última entrada del archivo de hechos, del
  estilo: «Decisión del orquestador (2026-09-11 ~23:20): el kiosco se queda
  corriendo, `active` y `enabled`; el final del Paso 13 queda superado».
  Marcarla como decisión, no como medición.
- **Estado:** abierta.

---

## F-202 · Encabezados de fichas ya cerradas que siguen redactados en presente

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/fichas.md`, títulos de **F-185** («…y el Paso 13 pide
  devolverlo a `enabled` + `inactive`») y **F-188** («Nadie ha vuelto a correr
  `probar-impresora`…»).
- **Qué pasa (texto del lente, tal cual):** Encabezados de fichas ya cerradas que
  siguen redactados en presente: F-185 («…y el Paso 13 pide devolverlo a
  `enabled` + `inactive`») y F-188 («Nadie ha vuelto a correr
  `probar-impresora`…»). Sólo se actualizó su campo **Estado**. Es la convención
  del archivo (F-113 hace lo mismo), así que se deja.
- **Por qué es residual:** es **la convención del archivo**, no un descuido: el
  título describe el hallazgo tal como se encontró y el campo **Estado** dice qué
  pasó con él. **F-113** está redactada igual.
- **Riesgo si no se toca:** quien hojee solo el índice de títulos puede creer
  abierto algo que está cerrado. Lo mitiga que el estado esté siempre en la
  última viñeta de cada ficha.
- **Propuesta:** ninguna. Se anota para que no se vuelva a abrir como hallazgo en
  la próxima ronda de lentes. Si algún día se decide cambiar la convención, hay
  que cambiarla en **todo** el archivo de una vez, no ficha por ficha.
- **Estado:** cerrada por convención (no se actúa).

---

## F-203 · La fila 1 de la bitácora cita F-185, que trata del estado final y no del trabajo

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-2-impresora.md` §0, bitácora, fila 1 («Poner la Pi
  en estado de trabajo…»), frente al título y al «Dónde» de la ficha **F-185** en
  `docs/fichas.md`.
- **Qué pasa (texto del lente, tal cual):** Bitácora del plan de la Fase 2, fila
  1: cita F-185 para el hecho de que el servicio nunca se deshabilitó **durante**
  el trabajo, cuando F-185 trata del **estado final**. Atribución imprecisa,
  heredada de antes de esta pasada.
- **Por qué es residual:** los dos hechos son ciertos y están medidos
  (`systemctl is-enabled ruleta` → `enabled` durante todo el deploy), y son las
  dos caras de la misma omisión; lo único torcido es a qué ficha se le cuelga
  cada una.
- **Riesgo si no se toca:** ahora que **F-185** está **cerrada** por la decisión
  del orquestador, un lector puede concluir que también quedó saldado el
  incumplimiento del Paso 1 —que el servicio debía trabajar **detenido y
  deshabilitado**—, y eso no lo cerró nadie: simplemente no se hizo, y por eso la
  fila 1 sigue en `[~]`.
- **Propuesta:** dejar en la fila 1 el hecho medido sin colgarlo de F-185, o
  abrir una ficha propia para el incumplimiento del Paso 1 si se quiere seguirle
  el rastro. La fila 1 debe seguir en `[~]`.
- **Estado:** abierta.

---

## F-204 · El conteo de `[ok]` tiene un quinto camino a 7 que el plan y F-186 no enumeran

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-2-impresora.md` §7.5 (bloque «son cuatro casos y
  ninguno es un fallo») y la ficha **F-186**; el código, en `ruleta/__main__.py`
  líneas 414-415 (`grep -n "consultar_estado" ruleta/__main__.py`).
- **Qué pasa (texto del lente, tal cual):** §7.5 del plan de la Fase 2 y la ficha
  F-186 enumeran «cuatro casos» del conteo de `[ok]`, pero el código tiene un
  quinto camino a 7: `consultar_estado: false` (`ruleta/__main__.py`, rama `[--]
  consultar_estado está en false`). Hoy vale `true` en `config.json`, así que no
  se da en la práctica.
- **Por qué es residual:** el quinto caso **no puede ocurrir** con el
  `config.json` que está desplegado (`"consultar_estado": true`, con golden en
  `tests/test_config.py`), y si ocurriera daría 7 `[ok]` y código 0, igual que
  los otros dos casos de 7: ningún golden se rompe.
- **Riesgo si no se toca:** si alguien pone `consultar_estado: false` para
  silenciar el aviso de poco papel, el diagnóstico dará 7 `[ok]` y un `[--]` que
  no está en la lista de casos, y el ejecutor de turno se detendrá creyendo que
  encontró una regresión.
- **Propuesta:** añadir el quinto caso a la lista de la §7.5 y a **F-186**:
  «7 + `[--] consultar_estado está en false`: nadie le preguntó a la impresora
  porque la configuración lo pidió así».
- **Estado:** abierta.

---

## F-205 · La nota de los «8 `[ok]`» en los documentos de la Fase 1 no dice que supone `tipo = "archivo"`

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-1-preparar-pi.md` §7 y su tabla de anclas
  (`grep -n "USB conectada" docs/planes/fase-1-preparar-pi.md`) y
  `docs/actas/2026-09-11-fase-1.md` (fila del golden `grep -c "\[ok\]"` y la nota
  del anexo).
- **Qué pasa (texto del lente, tal cual):** La nota nueva de la §7 del plan de la
  Fase 1 y de su acta habla de «8 `[ok]` con la impresora USB conectada» sin
  decir que ese conteo supone `impresora.tipo = "archivo"`. En la Fase 1 la
  configuración era `bluetooth`, así que el lector podría comparar peras con
  manzanas; el calificativo «USB conectada» lo insinúa pero no lo cierra.
- **Por qué es residual:** la nota está fechada, remite a las fichas **F-140** y
  **F-186**, y **no borra el `6` histórico**, que es lo que de verdad importaba
  para no falsear el acta de la Fase 1.
- **Riesgo si no se toca:** alguien reproduce el diagnóstico de la Fase 1 tal
  cual (con `tipo: "bluetooth"`), cuenta 6 `[ok]` y cree que la nota miente o que
  la Pi se rompió. El conteo de 8 solo sale con `tipo = "archivo"`, la ruta
  existente y la impresora contestando.
- **Propuesta:** añadir cinco palabras a la nota: «…con `impresora.tipo =
  "archivo"` y la impresora USB conectada y respondiendo».
- **Estado:** abierta.

---

## F-206 · El texto del golden de papel P1 se reescribió, no solo su estado

- **Fecha:** 2026-09-11
- **Origen:** lente cierre F2
- **Dónde:** `docs/planes/fase-2-impresora.md` §7.10, fila **P1** de la tabla de
  goldens de papel.
- **Qué pasa (texto del lente, tal cual):** §7.10 del plan de la Fase 2: el texto
  del golden P1 se reescribió («una línea de acentos perfecta» → «las líneas de
  acentos perfectas»). El cambio está anotado y justificado en la misma celda,
  pero es una modificación de la definición del golden, no sólo de su estado.
- **Por qué es residual:** la celda dice **por qué** se cambió, y con literalidad
  poco común: «el texto decía "**una** línea de acentos": eran cuatro, y 2b las
  partió en dos renglones cada una». El golden nuevo es **más exigente** que el
  viejo, no menos, y lo que se confirmó en papel cubre las cuatro tablas.
- **Riesgo si no se toca:** ninguno hoy. Importa como precedente: el formato
  antidrift trata los goldens como contrato, y reescribir uno en la misma pasada
  en que se declara cumplido es justo el movimiento que ese formato quiere hacer
  visible. Aquí quedó visible; conviene que siga siendo la excepción documentada
  y no la costumbre.
- **Propuesta:** ninguna sobre el texto —el nuevo es el correcto—. Se anota para
  dejar rastro de que el golden P1 **cambió de definición** el 2026-09-11, por si
  alguien compara el plan con una copia anterior.
- **Estado:** cerrada como anotación (no se actúa).

---

## F-207 · Procedencia del `logo.png` real y qué se le hizo antes de imprimirlo

- **Fecha:** 2026-09-12
- **Origen:** fase 4 logo
- **Dónde:** `logo.png` (raíz del repositorio) y las llaves `negocio.logo`,
  `negocio.logo_ancho` y `negocio.logo_tramado` de `config.json`.
- **Qué pasa:** el `logo.png` de 384 × 150 px que se había generado con Pillow
  para no dejar el repositorio sin logo **ya no está**: lo reemplaza el logo
  real del negocio (la corona sobre los «33»).
  - **Origen del archivo:** `G:/Other computers/Miltimex/Negocios/Asadero 33/Logo
    Corto.png`, en el Google Drive del usuario (archivo del 26/03/2024,
    204 357 bytes). Medido: PNG **RGBA de 4160 × 3475 px a 300 dpi**, fondo
    transparente (las cuatro esquinas con alfa 0), **dos colores** en RGB
    (negro y blanco) y solo **0.25 %** de los píxeles con alfa intermedio, que
    es el antialias del contorno. El original **no se tocó**: se abrió en modo
    solo lectura y sigue igual en su carpeta.
  - **Tratamiento** (script desechable con Pillow, fuera del repositorio):
    aplanado sobre blanco → conversión a gris (`L`) → recorte a la caja del
    contenido, que resultó ser **el lienzo completo** (`(0, 0, 4160, 3475)`: el
    original ya venía al ras por los cuatro lados, no había margen que quitar) →
    margen blanco del **2 % del ancho = 83 px por lado** (lienzo 4326 × 3641) →
    reducción a **576 × 485 px con LANCZOS** → guardado como **PNG gris de 8
    bits** (tipo de color 0, sin alfa, sin `tRNS`, sin entrelazado) con
    `optimize=True`: **21 057 bytes**, esquinas en 255, 10.25 % de píxeles bajo
    128 y apenas 0.91 % de tonos medios (el antialias).
  - **Cómo sale en papel:** con el `logo_ancho: 384` que trae `config.json`,
    `ruleta.escpos.preparar_imagen` lo deja en **384 × 323 px**, es decir
    **40.4 mm de alto** en papel de 203 dpi (mm = px / 8). En
    `python -m ruleta vista-previa` aparece como cinco bandas de 64 filas más
    una de 3, porque `banda_imagen` vale 64.
  - **Grosor del trazo:** medido sobre la imagen binaria que devuelve
    `preparar_imagen(Image.open("logo.png"), 384, False)`, la línea más delgada
    (las diagonales de la corona) queda en **≈2.8 px** (percentil 1 de la cuerda
    negra mínima en las 4 direcciones; mediana 8.5 px). Solo 19 píxeles de
    12 668 bajan de 2 px y son las puntas de las líneas. Por eso **no** se le
    aplicó el engrosado `MinFilter(3)` que se había previsto por si el trazo
    quedaba bajo 2 px: la versión engrosada sube el mínimo a ≈4 px, pero engorda
    las bolitas de la corona y cierra el hueco interior de los «33».
- **Por qué es residual:** no hay nada roto ni ninguna decisión pendiente. La
  suite sigue en verde (`python -m unittest discover -s tests -t .` → **194
  tests, OK**, con `test_prueba_del_config_real_cabe_entero`, que abre el
  `config.json` y el `logo.png` de verdad) y el logo nunca se validó en las
  pruebas por tamaño ni por contenido, así que cambiarlo no mueve ningún golden.
  Se anota porque, si mañana alguien quiere regenerarlo o retocarlo, esto es lo
  único que dice de dónde salió y con qué receta.
- **Riesgo si no se toca:** ninguno en el programa. El riesgo es de memoria: sin
  esta ficha, dentro de un mes nadie sabrá que el archivo bueno vive en el Drive
  del usuario, que el repositorio guarda una versión **ya reducida a 576 px** y
  que volver a reducirla desde el repositorio (en vez de desde el original de
  4160 px) degrada el trazo cada vez.
- **Propuesta (para cuando se vea en papel):** si el logo sale delgado o
  entrecortado, subir `negocio.logo_ancho` de **384 a 576**, que es el máximo del
  rollo de 80 mm y justo el ancho nativo del archivo (no hay que regenerar nada;
  a 576 el logo mide 485 px = **60.6 mm** de alto). Al revés, si 40 mm de logo
  por boleto se comen demasiado papel: `320` → 269 px ≈ 33.6 mm y `256` → 216 px
  = 27 mm. Y si alguna vez se cambia el logo por uno con fotografía o degradados,
  entonces sí hay que poner `"logo_tramado": true`.
- **Estado:** anotación de procedencia (no se actúa).

---

## F-208 · El README todavía llama «provisional» al `logo.png`

- **Fecha:** 2026-09-12
- **Origen:** fase 4 logo
- **Dónde:** `README.md`, árbol de archivos del final
  (`grep -n "logo provisional" README.md`), y el «Paso 5 · Tu logo» del §4
  (`grep -n "Paso 5 . Tu logo" README.md`).
- **Qué pasa:** el árbol de archivos del README dice
  `logo.png              logo provisional (reemplázalo por el real)`, y desde el
  2026-09-12 eso ya no es cierto: el archivo del repositorio **es** el logo real
  del negocio, a 576 × 485 px (ver **F-207**). El «Paso 5» sigue siendo correcto
  como instrucción para cambiarlo (pide un PNG o JPG de 8 bits entre 384 y 576
  px de ancho, que es exactamente lo que hay), pero al leerlo junto al árbol da a
  entender que el paso está pendiente.
- **Por qué es residual:** es una línea de documentación que se quedó vieja, no
  un error del programa ni una afirmación sobre el código que engañe al ejecutar
  nada. El boleto sale igual la lea alguien o no.
- **Riesgo si no se toca:** que el usuario (o quien instale la Pi) crea que
  todavía falta subir el logo y copie encima otro archivo —por ejemplo el
  original de 4160 px del Drive, que pesa 200 KB y hace que cada boleto tarde
  más en enviarse por Bluetooth—, o al revés, que dé por hecho que el logo se ve
  mal porque «es el de prueba».
- **Propuesta:** dos retoques de una línea en el `README.md`: en el árbol,
  `logo.png              logo del negocio (576 px; ver docs/fichas.md F-207)`; y
  en el «Paso 5», abrir con «El repositorio ya trae el logo del Asadero 33; este
  paso es solo para cambiarlo». **Requiere visto bueno del usuario**, porque toca
  documentación que él lee. No se hizo aquí: esta pasada solo tenía permiso para
  `logo.png` y `docs/fichas.md`.
- **Estado:** abierta. **Reconfirmada el 2026-09-12** por los lentes del
  logo (ronda 1), que la volvieron a levantar **dos veces** en la misma
  ronda (`README.md:538`) y coincidieron en dejarla fuera de alcance: el
  `README.md` no estaba entre los archivos que esa pasada podía tocar.
  **F-211** le agrega el motivo técnico para atenderla: hoy ninguna prueba
  impide que alguien copie otro archivo encima de `logo.png`.

---

## F-209 · El «0.91 % de tonos medios» de F-207 es una banda del histograma, no todo el antialias

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `docs/fichas.md`, ficha **F-207**, viñeta «Tratamiento»: la frase
  «apenas **0.91 %** de tonos medios (el antialias)». El número sale de
  `histograma_tonos()`, del script desechable `scratchpad/logo_medidas.py`, que
  define «medios» como la banda **64-191** del histograma.
- **Qué pasa:** el 0.91 % es exacto, pero es esa banda, no «el antialias».
  Vuelto a medir hoy sobre `logo.png` (576 × 485 = **279 360** píxeles):
  - negro puro (valor 0): **20 208 px**
  - blanco puro (valor 255): **242 511 px**
  - todo lo demás, que es el antialias real: **16 641 px = 5.96 %**
  - de esos, la banda 64-191: **2 555 px = 0.91 %** (lo que dice F-207)
  - el resto vive pegado a los extremos: 7 155 px en 1-63 y 6 931 px en 192-254.

  Aviso sobre el hallazgo mismo: los lentes reportaron «34 322 de 279 360» para
  el antialias, y ese conteo **no cuadra** (279 360 − 20 208 − 242 511 =
  **16 641**). El porcentaje que dieron, 5.96 %, sí es el correcto, así que fue
  error al transcribir el conteo, no error del hallazgo.
- **Por qué es residual:** F-207 no afirma nada falso; con la banda declarada,
  0.91 % es el número correcto. Lo único flojo es la etiqueta «(el antialias)» a
  secas, que hace parecer que el suavizado es seis veces menor de lo que es.
- **Riesgo si no se toca:** que alguien lea «casi no hay grises» y dé por hecho
  que la imagen ya está prácticamente binarizada. No lo está: 1 de cada 17
  píxeles es gris. Para imprimir da igual (`preparar_imagen` corta en 128 y
  `logo_tramado` está en `false`), pero importaría si algún día se compara este
  archivo contra otro para medir degradación.
- **Propuesta:** dejar en F-207 «apenas 0.91 % de tonos medios (banda 64-191);
  el antialias completo —todo lo que no es 0 ni 255— es 5.96 %». Es gusto de
  redacción, no corrección de un dato falso, así que **no se aplicó**: esta
  ficha ya deja el número fino anotado y F-207 no se reescribe por una precisión
  de estilo.
- **Estado:** anotación (no se actúa).

---

## F-210 · Las fichas del logo publican la ruta del Drive del usuario, con el nombre de otro negocio

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `docs/fichas.md`, ficha **F-207**, viñeta «Origen del archivo»:
  `G:/Other computers/Miltimex/Negocios/Asadero 33/Logo Corto.png`.
- **Qué pasa:** esa línea publica tres cosas que no hacen falta para entender de
  dónde salió el logo: que el usuario sincroniza un Google Drive con la carpeta
  «Other computers», el nombre de **otra** empresa suya, «Miltimex», que no
  tiene nada que ver con la ruleta, y la letra de unidad de su PC. Y el
  repositorio no es privado: el `README.md:106` manda
  `git clone https://github.com/seduva94/Ruelta-Aleatoria-Pi5.git` **sin
  credenciales**, y así se clonó en la Pi el 2026-09-11
  (`docs/planes/fase-1-preparar-pi.md:84`, `EXIT=0`).
- **Por qué es residual (y no corrección):** ya es la convención del
  repositorio, no un desliz de esta ficha. Antes de F-207 ya había rutas locales
  del usuario en `docs/actas/2026-09-11-fase-1.md:175`,
  `docs/actas/2026-09-11-hechos-medidos.md:17` y `:232`,
  `docs/planes/fase-1-preparar-pi.md:592` (ahí con contrabarras,
  `C:\Users\seduv\.ssh\config`), `docs/PAUSA-2026-09-11.md:31` y `:115`; y el
  nombre de equipo `DUVA_LAP\seduv` en `fase-1-preparar-pi.md:194`. Borrarla
  solo de F-207 daría una falsa sensación de limpieza.
- **Riesgo si no se toca:** bajo, pero permanente: lo que entra al historial de
  git ya no sale con un simple editar. Conviene decir qué **no** hay: no hay
  contraseñas, ni tokens, ni la llave SSH privada (esa se cita siempre por ruta,
  `C:/Users/seduv/.ssh/id_ruleta`, nunca por contenido; `grep "BEGIN OPENSSH"`
  sobre el repositorio → **0**). La llave **pública** sí está transcrita
  (`docs/actas/2026-09-11-fase-1.md:172`), y una llave pública es pública por
  diseño. Lo expuesto es contexto: nombre de usuario de Windows, nombre de
  equipo y el nombre comercial «Miltimex».
- **Propuesta:** es decisión del usuario, y de hacerse hay que hacerla en una
  pasada aparte que toque **todos** esos documentos a la vez. Dos caminos:
  dejarlo como está (es su repositorio y no hay secretos), o cambiar las rutas
  por algo genérico del tipo `<Drive del usuario>/Asadero 33/Logo Corto.png` y
  `~/.ssh/id_ruleta`. **Requiere visto bueno del usuario.**
- **Estado:** abierta (decisión del usuario).

---

## F-211 · Ninguna prueba fija el tamaño, los bytes ni el contenido de `logo.png`

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `tests/test_ticket.py:227`
  (`test_prueba_del_config_real_cabe_entero`) y el ayudante `lineas_vista` del
  mismo archivo (`tests/test_ticket.py:28`); también `tests/test_config.py:140`
  y `:145`.
- **Qué pasa:** el único test que abre el `logo.png` de verdad es
  `test_prueba_del_config_real_cabe_entero`. Carga el `config.json` del
  repositorio (que trae `"logo": "logo.png"`) y arma el boleto de prueba, así
  que el raster **sí** se genera: el boleto real pesa **16 381 bytes** y salen
  seis bandas de imagen (cinco `[IMAGEN 384x64 px]` y una `[IMAGEN 384x3 px]`).
  Pero lo único que comprueba es que ninguna **línea de texto** pase de las 48
  columnas. Las bandas de imagen ni siquiera llegan a esa comprobación:
  `lineas_vista` las descarta a propósito, con un `continue` para las marcas
  `[CORTE]`, `[IMAGEN` y `[BEEP]`. Matiz sobre el hallazgo: los lentes
  explicaron que esas líneas pasan «porque miden 19 caracteres»; medidas, miden
  **18** (`[IMAGEN 384x64 px]`) y **17** la última, y da igual, porque el filtro
  las salta antes de medirlas. La conclusión no cambia; queda más fuerte: aunque
  una banda midiera 500 caracteres, el test seguiría en verde.
  Del lado de la configuración pasa lo mismo:
  `test_config_json_del_proyecto_apunta_a_la_impresora_usb` ancla por igualdad
  los once campos del bloque `impresora`, pero nadie ancla `negocio.logo`,
  `negocio.logo_ancho` ni `negocio.logo_tramado`.
- **Por qué es residual:** es hueco de cobertura, no defecto. Hoy el archivo del
  repositorio es el correcto y el programa lo imprime bien; la suite completa
  sigue en **194 tests, OK**.
- **Riesgo si no se toca:** si alguien copia encima el original de 4 160 px del
  Drive —o cualquier otro PNG—, la suite sigue dando 194 OK y el problema
  aparece solo en papel: cada boleto tarda más en enviarse a la impresora y el
  logo puede salir con otro encuadre. Es exactamente el accidente que teme
  **F-208**, sin red que lo detenga.
- **Propuesta:** un golden de una línea que ancle las propiedades estables del
  archivo, no sus bytes: `Image.open("logo.png")` → `mode == "L"`,
  `size == (576, 485)` y `info.get("transparency") is None`. Los bytes exactos
  no sirven como golden porque cambian con la versión de Pillow y con
  `optimize`. Es **mejora, no defecto**, y toca `tests/`, que quedó fuera del
  alcance de esta pasada.
- **Estado:** abierta (mejora de pruebas).

---

## F-212 · `logo_ancho` sigue en 384 y la decisión se toma con el boleto impreso en la mano

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `config.json` → `negocio.logo_ancho: 384`; las equivalencias
  medidas están en la «Propuesta» de **F-207**.
- **Qué pasa:** con 384, el logo sale a 384 × 323 px, o sea **40.4 mm de alto en
  cada boleto**. El archivo ya soporta 576 sin regenerar nada, porque 576 es su
  ancho nativo y el máximo del rollo de 80 mm. Nadie ha visto todavía un boleto
  salido de la impresora **con este logo**: la última prueba confirmada en papel
  es la del 2026-09-11 ~23:20 (**F-188**, resuelta), y el logo cambió el
  2026-09-12.
- **Por qué es residual:** no hay nada roto ni ninguna afirmación falsa. Es
  gusto y consumo de papel. Los lentes lo levantaron **dos veces en la misma
  ronda**, lo que dice que es lo más visible que queda por decidir del logo, no
  que sea un defecto. Se anota aparte de F-207 porque F-207 está cerrada como
  anotación de procedencia y esta decisión sigue **abierta**.
- **Riesgo si no se toca:** solo papel y tiempo de impresión. A 384 el logo
  ocupa 40.4 mm de cada boleto; a 576 ocuparía 60.7 mm.
- **Propuesta:** imprimir un boleto y decidir viéndolo. Medidas ya verificadas:
  `576` → 485 px, `384` → 323 px, `320` → 269 px, `256` → 216 px. Cambiar el
  número en `config.json` es todo lo que hace falta; la imagen no se regenera.
  **Requiere visto bueno del usuario.**
- **Estado:** abierta (decisión con el boleto en la mano).

---

## F-213 · La regla «mm = px / 8» de F-207 redondea por lo bajo frente a los 203 dpi

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `docs/fichas.md`, ficha **F-207**, viñetas «Cómo sale en papel» y
  «Propuesta», donde convierte píxeles a milímetros con `mm = px / 8`.
- **Qué pasa:** 8 px/mm equivale a **203.2 dpi**, y la impresora es de 203, así
  que la regla se queda medio décimo corta. Medido: 485 px son **60.69 mm** (la
  ficha dice 60.6), 269 px son **33.66 mm** (dice 33.6), 216 px son **27.03 mm**
  (dice 27) y 323 px son **40.42 mm** (dice 40.4). La diferencia va de 0.03 a
  0.06 mm.
- **Por qué es residual:** no es una afirmación falsa. F-207 escribe la fórmula
  `(mm = px / 8)` al lado del número, así que cualquiera puede rehacer la
  cuenta. Y el error —seis centésimas de milímetro sobre sesenta— es la mitad de
  un punto de la impresora (un punto a 203 dpi mide 0.125 mm): no se podría
  imprimir esa diferencia aunque se quisiera.
- **Riesgo si no se toca:** ninguno práctico. Solo importaría si alguien suma
  alturas de muchos boletos para calcular cuánto rollo gasta el evento y
  arrastra el redondeo.
- **Propuesta:** ninguna. Se anota para que quien compare las cifras con una
  regla no crea que encontró un error.
- **Estado:** anotación (no se actúa).

---

## F-214 · La variante engrosada del logo se descartó por gusto, y sigue siendo la salida si el trazo sale entrecortado

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `scratchpad/construir_logo.py`, función `construir(engrosar=...)`,
  que genera dos candidatos (`logo576-lisa.png` y `logo576-eng.png`) y sus
  comparativas `cmp-lisa-384.png` y `cmp-eng-384.png`; la decisión está contada
  en **F-207**, viñeta «Grosor del trazo».
- **Qué pasa:** se eligió el candidato **liso** mirando las comparativas: el
  engrosado con `ImageFilter.MinFilter(3)` infla las bolitas de la corona y
  cierra el hueco interior de los «33». Es criterio estético, y los lentes lo
  revisaron y coincidieron. Medido hoy sobre los dos candidatos, pasados los dos
  por `preparar_imagen(..., 384, False)`:
  - píxeles negros: **12 668** (liso) contra **15 676** (engrosado), +23.7 % de
    tinta
  - grosor mínimo: **1.0 px** contra **1.41 px**
  - percentil 1: **2.83 px** contra **4.0 px**
  - mediana: **8.49 px** contra **10.0 px**
  - píxeles bajo 2 px: **19** contra **17**

  O sea: engrosar sube bien el percentil 1, pero casi no mueve el mínimo
  absoluto ni el número de puntas finas (ver **F-216**).
- **Por qué es residual:** es una preferencia sobre algo que nadie ha visto
  impreso. No hay defecto que arreglar mientras el papel no diga lo contrario.
- **Riesgo si no se toca:** si en papel térmico el trazo sale entrecortado hay
  que rehacer el logo, y la receta vive **fuera** del repositorio.
- **Propuesta:** si el papel decepciona, volver a correr `construir_logo.py` con
  `engrosar=True` y copiar el resultado sobre `logo.png`. Dos avisos: el script
  está en el scratchpad, que es efímero (ver **F-215**), y lee el original desde
  el Drive, así que hace falta la unidad `G:` montada. Si el script se perdiera,
  la receta completa está escrita en prosa en **F-207** y se puede reescribir.
- **Estado:** anotación (no se actúa; es la salida de emergencia si el papel
  decepciona).

---

## F-215 · El respaldo del logo provisional anterior solo vive en el scratchpad, que es efímero

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `scratchpad/logo-provisional-anterior.png` y
  `scratchpad/prev-head-logo.png`.
- **Qué pasa:** el `logo.png` que había antes —el de relleno generado con
  Pillow, **384 × 150 px, modo L, 4 717 bytes**— se guardó como copia en el
  scratchpad, en dos archivos **byte a byte idénticos** (mismo SHA-256,
  `4ac7902c…94817f`). El scratchpad es temporal: se borra sin avisar.
- **Por qué es residual:** no es pérdida. Los lentes verificaron que
  `git show HEAD:logo.png` devuelve ese mismo archivo, así que el historial del
  repositorio lo conserva. Yo **no** lo recomprobé: esta pasada tenía prohibido
  correr `git`. Lo que sí medí es que las dos copias del scratchpad son
  idénticas entre sí y coinciden con los 4 717 bytes y los 384 × 150 px que
  describe F-207.
- **Riesgo si no se toca:** ninguno, y además nadie lo quiere de vuelta: era un
  relleno para que el repositorio no quedara sin logo.
- **Propuesta:** ninguna. Se anota para que nadie pierda tiempo buscando ese
  archivo en el scratchpad dentro de un mes: se busca en el historial de git.
- **Estado:** cerrada como anotación (no se actúa).

---

## F-216 · El grosor mínimo real del trazo a 384 px es 1.0 px, no 2.83

- **Fecha:** 2026-09-12
- **Origen:** lentes logo ronda 1
- **Dónde:** `docs/fichas.md`, ficha **F-207**, viñeta «Grosor del trazo».
- **Qué pasa:** F-207 dice que «la línea más delgada … queda en **≈2.8 px**
  (percentil 1 de la cuerda negra mínima en las 4 direcciones; mediana 8.5 px).
  Solo 19 píxeles de 12 668 bajan de 2 px y son las puntas de las líneas». Los
  dos números son correctos y la ficha aclara que 2.8 es el **percentil 1**,
  pero leído de corrido se entiende que nada baja de ahí. El **mínimo absoluto
  es 1.0 px** (cinco píxeles exactos) y el percentil 0.1 es 1.41 px. Verifiqué
  dónde caen los 19 píxeles finos, y todos son extremos de trazo, no tramos
  largos: `y = 10` (la punta de la bolita de arriba de la corona), `y = 145` en
  `x = 7` y `x = 376` (los dos cabos de la línea de base, la que cruza el logo
  de lado a lado) y `y = 132-133, 146, 163, 170, 202, 235-238` (remates y
  esquinas de los «33» y de las diagonales).
- **Por qué es residual:** la ficha no engaña —declara el percentil— y el
  diagnóstico de fondo se sostiene: 19 píxeles de 12 668 es **0.15 %**, ruido.
  Por eso mismo la decisión de no engrosar sigue siendo la correcta.
- **Riesgo si no se toca:** si en la impresora real se ven **cabos
  desvanecidos** —la punta de la corona o los extremos de la línea de base—,
  este es el motivo y no hay que buscar otro. Dato medido para esa conversación:
  engrosar con `MinFilter(3)` tampoco los arregla del todo, porque el mínimo
  solo sube de 1.0 a 1.41 px y siguen quedando 17 píxeles bajo 2 px
  (ver **F-214**).
- **Propuesta:** ninguna hasta ver papel. Si hay que actuar, la salida está en
  F-214.
- **Estado:** anotación (no se actúa).

---

## F-217 · El logo se manda centrado con `ESC a 1`, y varias térmicas baratas ignoran esa alineación en los rasters

- **Fecha:** 2026-09-12
- **Origen:** esceptico logo
- **Dónde:** `ruleta/ticket.py:78` (`_encabezado`, que hace
  `doc.inicializar().alinear("centro")` y enseguida `doc.imagen(...)`) y
  `ruleta/escpos.py:372` (`raster_gs_v0`); `config.json` →
  `negocio.logo_ancho: 384` contra `impresora.ancho_puntos: 576`.
- **Qué pasa:** el raster del logo sale de **384 px de ancho** y el cabezal
  tiene **576**. El documento manda lo correcto: medido sobre los bytes del
  boleto de premio, el `ESC a \x01` (centrar) está en el **offset 10** y el
  primer `GS v 0` en el **13**, o sea pegado, sin ningún otro comando en medio.
  En la especificación de Epson la alineación vigente afecta también a la imagen
  raster; lo que **no** se puede verificar sin papel es si el firmware de esta
  impresora la respeta. Muchas térmicas chinas baratas la aplican solo al texto
  y sacan el raster pegado al margen izquierdo. Si ésta es una de ésas, el logo
  saldrá corrido a la izquierda con **192 px de papel en blanco a la derecha**
  (576 − 384 = 192 px, que a 203 dpi son **24.03 mm**).
- **Por qué es residual:** no hay defecto que arreglar. El programa emite la
  secuencia correcta y nadie ha visto todavía un boleto con este logo (la última
  prueba en papel confirmada es del 2026-09-11, **F-188**, y el logo cambió el
  2026-09-12). Es una duda que solo el papel contesta.
- **Riesgo si no se toca:** cosmético y acotado: el logo del evento sale
  descentrado en todos los boletos.
- **Propuesta:** se resuelve **mirando el primer boleto impreso**, la misma
  mirada que ya pide **F-212**. Si sale descentrado, subir
  `negocio.logo_ancho` de 384 a 576 lo arregla de paso, porque a 576 el raster
  ocupa el cabezal completo y no queda margen donde descentrarlo (ojo: eso
  también multiplica por 2.25 el peso del boleto, ver **F-218**). Si se quieren
  conservar los 40 mm de logo, la otra salida es rellenar la imagen con blanco
  hasta 576 px antes de mandarla, y eso sí obliga a regenerar el archivo.
  Detalle para quien toque el ancho: `preparar_imagen` no añade relleno hoy
  porque 384 ya es múltiplo de 8, pero si se pusiera un ancho que no lo fuera,
  el relleno blanco iría **a la derecha** (`ImageOps.pad(..., centering=(0, 0))`),
  empujando el logo aún más a la izquierda.
- **Estado:** abierta (se cierra con el primer boleto impreso; misma decisión
  que **F-212**).

---

## F-218 · El logo es el 97.6 % del peso del boleto de premio

- **Fecha:** 2026-09-12
- **Origen:** esceptico logo
- **Dónde:** los bytes que devuelve `ruleta.ticket.boleto_premio` con el
  `config.json` del repositorio; `impresora.tipo: "archivo"`,
  `bytes_por_segundo: 16000`, `tamano_bloque: 512`, `pausa_bloque_seg: 0.03`,
  `pausa_inicial_seg: 0.4`, `pausa_final_seg: 1.5`; y
  `juego.espera_entre_jugadas_seg: 5.0`. El envío está en
  `ruleta/escpos.py`, `ImpresoraBluetooth.imprimir` y `_espera_drenado`.
- **Qué pasa:** medido hoy, el raster del logo son **15 552 bytes** de los
  ~15 930 del boleto de premio: el **97.6 %**. Todo el texto del boleto —
  encabezado, premio, folio, fecha, pie, corte y pitido— cabe en **381 bytes**.
  - Matiz sobre el hallazgo: el escéptico citó «15 933 bytes» de total, y ése es
    el tamaño exacto del boleto de **TEST 3**. El total cambia con el nombre y
    el detalle del premio: entre **15 927** (TEST 6) y **15 935** (TEST 4) en
    los siete premios del `config.json`, y **no** depende del folio. El raster
    en cambio es siempre el mismo, 15 552 B = 6 bandas =
    5 × (8 + 64 × 48) + (8 + 3 × 48).
  - Con `impresora.tipo: "archivo"` (el USB de hoy) el peso da igual: se escribe
    al nodo de una vez y ninguna de esas llaves de temporización tiene efecto
    por cable (ver **F-091**).
  - Por el respaldo **Bluetooth** sí cuesta tiempo de reloj, y no es solo el
    envío: `pausa_inicial` 0.4 s + 0.03 s por bloque de 512 B (**32 bloques** =
    0.96 s) + `pausa_final` 1.5 s + el drenado estimado `bytes / 16000` =
    **0.996 s**. Total de pausas **≈3.86 s por boleto**, contra **1.95 s** si el
    boleto no llevara logo.
- **Por qué es residual:** no es defecto ni afirmación falsa de ningún
  documento. Es el precio previsto de imprimir un logo, y por USB ni se nota.
- **Riesgo si no se toca:** ninguno hoy. Importa el día que se caiga al
  Bluetooth: los ≈3.86 s de pausas todavía caben en los
  `espera_entre_jugadas_seg: 5.0`, pero con poco margen. Y si además se sube
  `logo_ancho` a 576 (la decisión abierta de **F-212**, y la salida que propone
  **F-217**), el raster pasa a **34 984 B**, el boleto a ~35 366 B y las pausas
  del Bluetooth a **≈6.21 s**, que ya **no** caben en los 5 s entre jugadas.
- **Propuesta:** ninguna. Es dato para dimensionar la espera entre jugadas si
  alguna vez se imprime por Bluetooth, y una consecuencia más que pesar el día
  que se decida el `logo_ancho`.
- **Estado:** anotación (no se actúa).

---

## F-219 · `logo.png` no está declarado en `.gitattributes`, y aun así git lo trata como binario

- **Fecha:** 2026-09-12
- **Origen:** esceptico logo
- **Dónde:** `.gitattributes` (cinco reglas: `*.sh`, `*.service`, `*.py`,
  `*.json`, `*.md`, todas `text eol=lf`) y `logo.png`.
- **Qué pasa:** no hay regla para `*.png`, ni un `* -text` de respaldo. No es
  problema: git autodetecta binario buscando un byte NUL en los primeros 8 000,
  y `logo.png` trae el **primer NUL en el offset 8** (**104** NUL en los
  primeros 8 000 bytes, **244** en el archivo entero), así que nunca entra a la
  normalización de finales de línea. Sobre el viaje de ida y vuelta: los lentes
  ya comprobaron que `git show HEAD:logo.png` devuelve un PNG válido de 4 717
  bytes —el logo de relleno anterior, ver **F-215**—; yo **no** lo recomprobé,
  esta pasada tenía prohibido correr `git`. Lo que sí medí son los bytes del
  archivo actual: **101 LF sueltos y un CRLF**, y ese CRLF está en el **offset
  4**, dentro de la propia firma PNG (`89 50 4E 47 0D 0A 1A 0A`), que existe
  justamente para delatar una transferencia hecha en modo texto.
- **Por qué es residual:** la ausencia no rompe nada. La autodetección de git ya
  cubre el caso y el archivo lleva así desde que entró.
- **Riesgo si no se toca:** solo se materializa si alguien añade a
  `.gitattributes` una regla `*.png text` o un `* text=auto` mal puesto: git
  convertiría entonces esos 101 LF a CRLF al sacar el archivo en Windows y el
  PNG quedaría corrupto. La falla sería silenciosa en el papel: `_cargar_logo`
  (`ruleta/ticket.py:56`) atrapa cualquier excepción de Pillow y devuelve
  `None`, así que el boleto saldría **sin logo** y sin avisar.
- **Propuesta:** opcional, una línea: añadir `*.png binary` a `.gitattributes`
  para dejarlo explícito en vez de depender de la autodetección. **No se hizo:**
  `.gitattributes` no está en el alcance de escritura de esta pasada, que solo
  podía tocar `logo.png` y `docs/fichas.md`.
- **Estado:** anotación (no se actúa; la mejora necesita una pasada que pueda
  tocar `.gitattributes`).

---

## F-220 · El boleto de consuelo ya no anuncia que los premios se agotaron, pero el valor por omisión del código sí

- **Fecha:** 2026-09-13
- **Origen:** usuario en demo
- **Dónde:** `config.json` (`juego.consuelo.texto`), `tests/test_config.py`
  (`test_config_json_del_proyecto_es_valido`), `ruleta/config.py`
  (`ConfigConsuelo.texto`, `grep -n "Por hoy se agotaron" ruleta/config.py`) y
  `tests/test_ticket.py` (`test_consuelo`).
- **Qué pasa:** viendo la demo, el usuario decidió que el boleto de
  «SIGUE PARTICIPANDO» **no** debe decirle al cliente que los premios se
  acabaron. El `config.json` del repositorio pasó de
  `"Por hoy se agotaron los premios. ¡Gracias por jugar!"` a
  **`"¡Gracias por jugar!"`**, y un golden nuevo ancla por igualdad ese texto y
  el título. Lo residual es que **el valor por omisión del código no cambió**:
  `ruleta/config.py` sigue trayendo el texto viejo y `test_consuelo` lo
  comprueba con `assertIn("Por hoy se agotaron los premios. ¡Gracias por", …)`,
  porque arma una config sintética sin bloque `juego.consuelo`.
- **Por qué es residual:** la impresora obedece al `config.json`, que es el
  archivo que viaja a la Pi con `git pull`; el defecto del código solo asomaría
  si alguien borrara el bloque `juego.consuelo`. Y el golden nuevo se pone en
  rojo justo en ese caso: medido como mutación M9 de esta pasada
  (`'Por hoy se agotaron los premios. ¡Gracias por jugar!' != '¡Gracias por jugar!'`).
- **Riesgo si no se toca:** dos textos oficiales conviviendo. Quien lea
  `ruleta/config.py` o `tests/test_ticket.py` creerá que el boleto todavía
  anuncia el agotamiento.
- **Propuesta:** en una pasada que pueda escribir `ruleta/` y
  `tests/test_ticket.py`, poner el mismo texto como valor por omisión y volver
  ese `assertIn` una igualdad. **No se hizo:** esta pasada solo podía escribir
  `config.json`, `tests/test_config.py` y `docs/fichas.md`.
- **Estado:** abierta en cuanto al defecto del código. La decisión del usuario
  ya está aplicada y anclada: `config.json` dice `"¡Gracias por jugar!"` y la
  suite completa quedó en verde (194 pruebas) el 2026-09-13.
- **Nota del 2026-09-16 (Fase 4c):** el bloque `juego.consuelo` ganó una tercera
  llave, **`peso`**, y **repite el mismo patrón a propósito**: por omisión vale
  **0** en `ruleta/config.py` y **217** en `config.json`. La diferencia con lo
  que esta ficha describe es que aquí **la asimetría es la decisión**, no un
  descuido: un repositorio que no cargue la llave tiene que comportarse
  **exactamente** como antes de la Fase 4c (consuelo solo al agotarse los
  premios), y por eso el defecto del código **no puede** ser 217. Lo ancla por
  igualdad `tests/test_config.py::TestReglas::test_consuelo_sin_peso_vale_cero`
  (mutación **M4** de esa fase: poniendo 217 como defecto, tres pruebas en rojo).
  Sigue valiendo lo que esta ficha pide para `texto`.

---

## F-221 · `juego.consuelo.texto` admite la cadena vacía sin queja

- **Fecha:** 2026-09-13
- **Origen:** ejecutor de la decisión del consuelo · mutación M4
- **Dónde:** `ruleta/config.py`, validación de `juego.consuelo`
  (`grep -n "consuelo" ruleta/config.py`).
- **Qué pasa:** al mutar el `config.json` de la copia con
  `"texto": ""` el cargador **no** protesta: la única razón por la que la
  mutación se puso en rojo fue el golden nuevo, que compara el texto exacto. Con
  otro texto vacío en producción el boleto de consuelo saldría con el título
  grande y **una línea en blanco** debajo. Compárese con `negocio.nombre`, que
  sí rechaza `"  "` (`tests/test_config.py`, "negocio.nombre").
- **Por qué es residual:** nadie vacía ese texto por accidente y hoy el golden
  lo cubre para el `config.json` del repositorio; no cubre un `config.json`
  editado a mano en la Pi.
- **Riesgo si no se toca:** un boleto de consuelo mudo, sin aviso en el log.
- **Propuesta:** exigir texto no vacío en `juego.consuelo.titulo` y
  `juego.consuelo.texto`, como ya se hace con `negocio.nombre`. **No se hizo:**
  `ruleta/config.py` no estaba en el alcance de escritura de esta pasada.
- **Estado:** abierta.

---

## F-222 · Verificado por los lentes del consuelo: alcance, 8 mutaciones en rojo, 194 pruebas y el papel a 48 columnas

- **Fecha:** 2026-09-13
- **Origen:** lentes consuelo
- **Dónde:** `config.json` (`juego.consuelo`), `tests/test_config.py`
  (`test_config_json_del_proyecto_es_valido`), las fichas **F-220** y **F-221**,
  y la vista previa (`python -m ruleta vista-previa`).
- **Qué pasa:** queda por escrito lo que midieron los dos lentes y el escéptico
  sobre la pasada del texto de consuelo, para no volver a auditar lo mismo:
  1. **Alcance:** el cambio toca exactamente los tres archivos permitidos
     (`config.json`, `tests/test_config.py`, `docs/fichas.md`), sin archivos sin
     rastrear, sin secretos, los tres en **UTF-8 sin BOM y con LF**, y el
     `config.json` sigue siendo **JSON válido**.
  2. **El golden muerde:** 8 mutaciones por copia en el scratchpad (nunca en el
     repositorio), **las 8 en rojo**: el texto viejo («Por hoy se agotaron los
     premios…»), texto vacío, texto con espacio final, texto sin la «¡» inicial,
     texto en minúsculas, título con espacio final, título
     `"SEGUI PARTICIPANDO"` y **borrar el bloque `juego.consuelo`** (que cae al
     valor por omisión del código). Al restaurar el archivo, verde.
  3. **Suite completa: 194 pruebas OK**, vuelta a correr en esta ronda
     correctiva (`python -m unittest discover -s tests -t .`).
  4. **Render real** con el `config.json` del repositorio: el boleto de consuelo
     saca el título en 3x partido en dos renglones (`SIGUE` / `PARTICIPANDO`),
     `¡Gracias por jugar!` centrado en **una sola línea**, sin renglón en blanco
     de más, y con `[BEEP]` y `[CORTE]` intactos.
  5. **Ancho de papel:** lo único que pasa de 48 columnas en la vista previa son
     las tres líneas de corte (56 caracteres), y el exceso son los 8 caracteres
     del marcador ` [CORTE]`, que lo pone el visor y no el papel. El **ancho
     real máximo, con el bloque de consuelo incluido, es 48** (23 líneas lo
     tocan exacto).
  6. **F-220 comprobada afirmación por afirmación:** `ruleta/config.py:95` sigue
     con el texto viejo, `tests/test_ticket.py:149` lo ancla con `assertIn`, el
     `config_base()` de `tests/test_ticket.py` no trae bloque `juego` (por eso
     cae al valor por omisión), y `config.json` está rastreado en git y es el
     que `instalar.sh:93` usa en la Pi.
  7. **F-221 comprobada:** `cargar()` acepta `juego.consuelo.texto = ""` y
     `"  "` sin queja (medido otra vez en esta ronda), mientras
     `negocio.nombre` sí rechaza `"  "` con «negocio.nombre no puede estar
     vacío» (`ruleta/config.py:335-336`, prueba en `tests/test_config.py:99`).
  8. **Ningún otro documento queda falso** con el cambio: `README.md:346` elide
     el valor con «…» y `README.md:231` solo menciona el título
     «SIGUE PARTICIPANDO» como texto configurable; los planes no citan el texto.
- **Por qué es residual:** nota de verificación; no pide ningún cambio.
- **Riesgo si no se toca:** ninguno. El riesgo sería perder los hechos y volver
  a medirlos, o escribir el acta de memoria, que es lo que el §6 del protocolo
  prohíbe.
- **Propuesta:** dejar constancia y copiar estos hechos al acta del 2026-09-13
  (ficha **F-225**) en lugar de volver a medir.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-223 · Una pasada ajena intentó cerrar la F-160; el escéptico lo revirtió y la decisión queda para el usuario

- **Fecha:** 2026-09-13
- **Origen:** lentes consuelo · revertido por el escéptico
- **Dónde:** `docs/fichas.md`, bloque **Estado** de la **F-160** y última frase
  de la **F-188** (`grep -n "F-160" docs/fichas.md`).
- **Qué pasó:** la pasada del texto de consuelo, además de lo suyo, **cerró la
  F-160** (el `beep: true` frente a la decisión D8) y **ajustó la F-188** para
  apuntar a ese cierre. Las dos fichas hablan del zumbador, no del texto del
  boleto. La evidencia que citaban es real —`docs/actas/2026-09-11-fase-2.md`
  §6, punto 2, y §10: el usuario decidió `beep: true` **después de oírlo** y lo
  confirmó en papel, «todas las pruebas salieron y se escucharon los beeps»—,
  pero **entre el 2026-09-11 y hoy no se midió nada nuevo sobre el zumbador**, y
  la F-160 quedaba abierta como vigilancia de la semana del evento: su texto
  decía «La ficha sigue abierta por si el usuario prefiere volver a `false`
  cuando lo oiga una noche entera de evento», y el acta lo repite en §6 punto 2,
  «Si en el evento molesta, se pone en `false` y basta reiniciar el servicio».
  Esa noche entera de evento todavía no pasa.
- **Qué se hizo:** el escéptico **revirtió los dos retoques antes del commit**:
  la **F-160** vuelve a estar **abierta** (conservando el puntero nuevo a la
  evidencia del 2026-09-11) y la **F-188** vuelve a decir «**F-160**, abierta».
  Así el commit del texto de consuelo no arrastra ninguna decisión del usuario y
  no hay que esperar su respuesta para commitear.
- **Por qué queda la ficha:** para que conste que el cierre se propuso, con qué
  evidencia, y por qué no se aplicó; y para que nadie lo vuelva a intentar desde
  una pasada que venía a otra cosa.
- **Riesgo si no se toca:** ninguno ya. El riesgo que se evitó era cerrar por
  conveniencia una vigilancia que nadie ejerció y sentar el precedente de cerrar
  fichas ajenas.
- **Propuesta:** preguntarle al usuario, al cerrar la Fase 4 o después de la
  primera noche de evento, si el pitido por boleto se queda. Si dice que sí,
  cerrar la **F-160** en la pasada que la tenga en su alcance. **Requiere al
  usuario.**
- **Estado:** cerrada en cuanto al retoque (revertido). La **F-160** sigue
  abierta.

---

## F-224 · La última frase de la F-188 se leía contradictoria: decía «NO cierra… F-160» y en el mismo renglón la daba por cerrada

- **Fecha:** 2026-09-13
- **Origen:** lentes consuelo
- **Dónde:** `docs/fichas.md`, cierre de la **F-188**
  (`grep -n "Lo que esta ficha NO cierra" docs/fichas.md`).
- **Qué pasaba:** la frase «**Lo que esta ficha NO cierra:** el cambio de rollo
  (**F-190**, abierta) y la decisión de dejar `beep` en `true` durante toda la
  semana del evento (**F-160**, cerrada el 2026-09-13…)» solo se entendía si el
  lector notaba que ese cierre era **posterior y de otra pasada**. A primera
  vista parecía que la ficha decía y se desdecía en la misma línea.
- **Por qué era residual:** era redacción, no un hecho falso: los dos datos eran
  correctos por separado.
- **Riesgo si no se toca:** ninguno ya.
- **Estado:** **resuelta** el 2026-09-13 al revertir el cierre de la F-160
  (**F-223**): la F-188 vuelve a decir «**F-160**, abierta» y la frase ya no se
  desdice.

---

## F-225 · La pasada del consuelo no dejó acta del 2026-09-13 ni fila en la bitácora del plan

- **Fecha:** 2026-09-13
- **Origen:** lentes consuelo
- **Dónde:** `docs/actas/` (solo hay tres archivos, los tres del 2026-09-11) y
  la §0 «Bitácora» de `docs/planes/fase-2-impresora.md`.
- **Qué pasa:** el §6 del protocolo pide actas escritas desde el archivo de
  hechos medidos y memoria actualizada en cada hito. El cambio del texto de
  consuelo —decisión del usuario viendo la demo, golden nuevo por igualdad y las
  fichas F-220 a F-226— no tiene acta ni fila de bitácora. **No se hizo porque
  el alcance de escritura de la pasada eran solo `config.json`,
  `tests/test_config.py` y `docs/fichas.md`.**
- **Por qué es residual:** nada de lo escrito es falso; lo que falta es el
  registro, y escribirlo no le tocaba al ejecutor de esta pasada.
- **Riesgo si no se toca:** en una semana nadie sabrá por qué el `config.json`
  dice `¡Gracias por jugar!` sin ir a leer las fichas, y el acta acabará
  escribiéndose de memoria.
- **Propuesta:** el orquestador escribe `docs/actas/2026-09-13-consuelo.md`
  desde el archivo de hechos de la sesión —los hechos medidos ya están en la
  **F-222**— y agrega la fila de bitácora antes de cerrar la fase.
- **Estado:** abierta, para el orquestador.

---

## F-226 · El golden del texto de consuelo vive en `test_config_json_del_proyecto_es_valido`, cuyo nombre no lo anuncia

- **Fecha:** 2026-09-13
- **Origen:** lentes consuelo
- **Dónde:** `tests/test_config.py:140-150`
  (`grep -n "consuelo" tests/test_config.py`).
- **Qué pasa:** las dos igualdades que anclan `juego.consuelo.titulo` y
  `juego.consuelo.texto` quedaron dentro de
  `test_config_json_del_proyecto_es_valido`, un test cuyo nombre habla de la
  **validez del archivo**, no del contenido del boleto de consuelo. Funciona y
  muerde (8 de 8 mutaciones en rojo, **F-222**), pero un lector futuro no lo
  buscaría ahí; justo debajo está
  `test_config_json_del_proyecto_apunta_a_la_impresora_usb`, que sí nombra lo
  que ancla.
- **Por qué es residual:** es cosmético; el golden existe, muerde y está en
  verde. El §5 manda que lo cosmético vaya a ficha, y los lentes no pidieron
  corrección.
- **Riesgo si no se toca:** alguien cambia el texto del consuelo, ve fallar un
  test llamado «…es_valido» y cree que rompió el JSON.
- **Propuesta:** mover las dos igualdades a un test propio, por ejemplo
  `test_config_json_del_proyecto_trae_el_consuelo_aprobado`, en la próxima
  pasada que toque `tests/test_config.py`.
- **Estado:** abierta (cosmética).

---

## F-227 · Verificado por el escéptico del consuelo: 10 mutaciones propias en rojo, 194 pruebas y los bytes del boleto

- **Fecha:** 2026-09-13
- **Origen:** escéptico consuelo
- **Dónde:** `config.json` (`juego.consuelo`), `tests/test_config.py`
  (`test_config_json_del_proyecto_es_valido`), el boleto de consuelo real
  (`ruleta.ticket.boleto_consuelo`) y las fichas **F-220**, **F-221** y
  **F-222**.
- **Qué pasa:** queda por escrito lo que midió el escéptico **por su cuenta**,
  después de los lentes y sin verlos, al intentar refutar la pasada del texto de
  consuelo. **No lo logró: el cambio en sí (config.json + golden) no tiene
  objeción.** Esta ficha no repite la **F-222**: la confirma con mediciones
  propias y añade el nivel de bytes.
  1. **Render medido:** con
     `ruleta.ticket.boleto_consuelo(ruleta.config.cargar("config.json"), Boleto(folio=7, premio=None, …))`
     y `ruleta.escpos.decodificar_vista(datos, codepage="cp858", ancho=48)`, la
     línea sale `   |              ¡Gracias por jugar!`: el texto **completo**,
     en **una sola línea**, **centrado exacto** (`center(48)`: 14 espacios a la
     izquierda, 19 caracteres, 15 a la derecha) y **sin renglón en blanco de
     más**. El título sale en 3x partido en dos renglones (en la vista se ve
     `SSSIIIGGGUUUEEE` / `PPPAAARRRTTTIIICCCIIIPPPAAANNNDDDOOO`, porque el visor
     repite cada carácter tantas veces como el multiplicador). `[BEEP]` y
     `[CORTE]` intactos al final.
  2. **La palabra «agotaron» no está en el papel:** no aparece en los bytes del
     boleto en ninguna de las cuatro codificaciones probadas (`cp858`, `cp850`,
     `utf-8`, `latin-1`). Los **15 785 bytes** del boleto se generaron con el
     `config.json` del repositorio tal como está en el árbol.
  3. **La «¡» sobrevive al camino a la impresora:** en `cp858` se codifica como
     **un solo byte `0xAD`** y no se translitera. `b"\xadGracias por jugar!"`
     está literalmente en el flujo; `b"!Gracias"` **no**. El byte `0xAD` aparece
     **exactamente una vez** en todo el boleto y antes va la secuencia
     `ESC t 19` (`b"\x1bt\x13"`), que es la tabla `cp858` que declara el
     `config.json` (`codepage_n = 19`). El tramo decodifica como
     `¡Gracias por jugar!`.
  4. **Suite completa en verde:** `python -m unittest discover -s tests -t .` →
     **Ran 194 tests, OK** (0.74 s).
  5. **Mutaciones propias: 10, todas en rojo.** Hechas **por copia**, sobre una
     copia íntegra del repositorio en el scratchpad —nunca en el repositorio—,
     con la copia en verde de partida y las mismas 194 pruebas. Las 10 fallan en
     `tests.test_config.TestCargar.test_config_json_del_proyecto_es_valido`:
     **M1** texto viejo con «agotaron»; **M2** espacio final; **M3** sin la «¡»;
     **M4** texto vacío; **M5** minúsculas; **M6** título
     `"SEGUI PARTICIPANDO"`; **M7** borrar el bloque `juego.consuelo` (cae al
     valor por omisión del código y da
     `'Por hoy se agotaron los premios. ¡Gracias por jugar!' != '¡Gracias por jugar!'`);
     **M8** título con espacio doble; **M9** quitar el «!» final; **M10**
     espacio duro (NBSP) en vez de espacio. Al restaurar el `config.json` de la
     copia, verde otra vez. **El golden muerde, y muerde por igualdad, no por
     presencia.**
  6. **Higiene del árbol:** solo tres archivos modificados (`config.json`,
     `tests/test_config.py`, `docs/fichas.md`), **cero archivos sin rastrear**
     (`git status --porcelain -uall`), los tres en **UTF-8 sin BOM y con LF** en
     índice y en árbol (`git ls-files --eol`: `i/lf w/lf attr/text eol=lf`),
     `config.json` es **JSON válido** y no trae secretos (la única MAC es el
     relleno `00:00:00:00:00:00`, que ya estaba).
  7. **Las citas de línea de las fichas nuevas, una por una, todas correctas:**
     `ruleta/config.py:95` (texto viejo por omisión), `ruleta/config.py:335-336`
     (`negocio.nombre` no puede estar vacío), `tests/test_config.py:99` (rechazo
     de `negocio.nombre = "  "`), `tests/test_config.py:140-150` (el golden
     nuevo), `tests/test_ticket.py:149` (el `assertIn` con el texto viejo),
     `config_base()` de `tests/test_ticket.py` sin bloque `juego` (por eso cae
     al valor por omisión), `instalar.sh:93` (usa `${DIR}/config.json` en la Pi),
     `README.md:231` (solo el título) y `README.md:346` (elide el valor con
     «…»). **Ningún documento del repositorio queda falso** por el cambio:
     «agotaron» no aparece en `README.md` ni en los planes.
  8. **El punto 5 de la F-222 se reproduce:** en `python -m ruleta vista-previa`
     lo único que pasa de 48 columnas son las tres líneas de corte (56
     caracteres), y el exceso son los 8 del marcador ` [CORTE]` que pone el
     visor. Descontándolo, el **ancho real máximo es 48** y son **exactamente 23
     las líneas que lo tocan** (20 + las 3 de corte). Con `--todos`, 38 + 9.
  9. **F-220 y F-221 siguen en pie:** `ruleta/config.py:95` mantiene el texto
     viejo como valor por omisión y `tests/test_ticket.py:149` lo ancla con
     `assertIn` (**F-220**); y `cargar()` acepta `juego.consuelo.texto = ""` y
     `"  "` sin protestar (**F-221**). Ninguno de esos dos archivos estaba en el
     alcance de escritura de esta pasada.
- **Por qué es residual:** nota de verificación independiente; no pide ningún
  cambio. El único cambio que el escéptico **sí** pidió —revertir el cierre de
  la **F-160**— ya está aplicado (ver **F-223** y **F-224**).
- **Riesgo si no se toca:** ninguno. El riesgo sería perder los hechos y volver
  a medirlos, o escribir el acta de memoria, que es lo que el §6 del protocolo
  prohíbe.
- **Propuesta:** copiar estos hechos, junto con los de la **F-222**, al acta del
  2026-09-13 que pide la **F-225**, en lugar de volver a medir.
- **Estado:** cerrada de entrada (nota de verificación).

---

## F-228 · La F-220 llama «mutación M9» a la de borrar `juego.consuelo`; la F-222 dice que fueron ocho y la lista en octavo lugar

- **Fecha:** 2026-09-13
- **Origen:** escéptico consuelo
- **Dónde:** `docs/fichas.md`, párrafo «Por qué es residual» de la **F-220** y
  punto 2 de la **F-222** (`grep -n "mutación M9" docs/fichas.md`).
- **Qué pasa:** la **F-220** dice que la mutación de borrar el bloque
  `juego.consuelo` fue la «**M9** de esta pasada», mientras que la **F-222**
  cuenta **ocho** mutaciones y la enumera en **octavo** lugar. Es numeración
  interna de la pasada del ejecutor, que no se ve desde fuera. **El hecho
  medido no está en duda:** esa mutación queda en rojo con el mensaje exacto
  `'Por hoy se agotaron los premios. ¡Gracias por jugar!' != '¡Gracias por jugar!'`,
  y el escéptico lo confirmó por su cuenta (es su **M7** de diez, **F-227**).
  Lo que no cuadra es el número, no el hecho.
- **Por qué es residual:** no es afirmación falsa contra el código, ni assert
  que no muerda, ni golden en rojo: es una etiqueta de conteo entre dos fichas.
  El escéptico no pidió corrección por ella.
- **Riesgo si no se toca:** quien audite el conteo de mutaciones busca una
  novena que no está en la lista y cree que falta evidencia.
- **Propuesta:** en la próxima pasada que toque estas fichas, sustituir en la
  **F-220** «mutación M9 de esta pasada» por «la mutación de borrar el bloque
  `juego.consuelo`» y remitir al punto 2 de la **F-222** y al punto 5 de la
  **F-227**. **No se hizo aquí:** la ronda correctiva del escéptico traía en su
  alcance solo sus cuatro correcciones exactas.
- **Estado:** abierta (cosmética).

---

## F-229 · El evento del 21 al 25 de septiembre ya tiene documento propio, y pide tres funciones que el programa no tiene

- **Fecha:** 2026-09-13
- **Origen:** evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` (documento nuevo);
  `config.json` (bloque `premios`, todavía con `test1`…`test7`);
  `ruleta/inventario.py` (`disponibles`, `probabilidades`, `sortear`);
  `ruleta/config.py` (`Premio`, `ConfigJuego`, `ConfigConsuelo`).
- **Qué pasa:** el usuario dictó el evento real el 2026-09-13 (fechas 21 al 25
  de septiembre de 2026, horario de 12:00 a 23:00 hora de Hermosillo y los siete
  premios con su stock y su cupo diario). Eso quedó escrito en
  **`docs/evento-2026-09-asadero-33.md`**, que desde hoy es **la fuente de
  verdad del evento**: si ese documento y `config.json` dicen cosas distintas,
  **gana el documento** y el `config.json` se rehace desde él. El documento trae
  además la propuesta de nombres para el boleto, el modelo de probabilidad
  («peso = cupo diario», consuelo con peso N − 33) con escenarios para
  N = 150 / 250 / 400 jugadas al día, las franjas propuestas y siete preguntas
  abiertas con su valor por omisión. **Nada de esto se aplicó todavía a
  `config.json`.**
- **Las tres funciones que faltan** (marcadas «PENDIENTE DE CONSTRUIR» en el
  documento):
  1. **A · Probabilidad propia del boleto de consuelo.** Hoy
     `Inventario.sortear` devuelve `None` **solo** cuando `disponibles()` está
     vacía, así que con los premios del evento **las primeras 33 jugadas del día
     ganan seguidas** (34 el 24 y el 25) y de ahí en adelante todo es consuelo.
     Medido el 2026-09-13 corriendo `sortear`/`emitir` con el bloque propuesto:
     el primer consuelo del lunes 21 es la jugada **34**, y el del jueves 24 la
     **35**. Propuesta de forma: `juego.consuelo.peso`.
  2. **B · Franjas horarias por premio, con tope por franja.** Hoy solo existen
     `tope_diario` y `desde`/`hasta`, que trabajan por día completo; **no hay
     manera de decir «de 19:00 a 23:00»**. Sin esto, la hielera puede salir a
     cualquier hora del 24 o del 25, en contra del dictado. Propuesta de forma:
     `franjas: [{desde_hora, hasta_hora, tope, peso}]` por premio, con el premio
     no disponible fuera de sus franjas y el `peso` de la franja mandando sobre
     el del premio.
  3. **C · Horario del evento.** El programa no conoce la hora de apertura ni la
     de cierre: juega a cualquier hora en que se apriete JUGAR con el mesero
     habilitando. Propuesta de forma:
     `juego.horario: {abre, cierra, fuera_de_horario}`, con
     `fuera_de_horario` = `"no_jugar"` o `"consuelo"` (pregunta 5 del documento).
- **Por qué es residual:** no es defecto de conducta del código ni afirmación
  falsa de ningún documento: hoy el programa hace exactamente lo que dice su
  documentación. Son **funciones que el evento pide y que no se han escrito**, y
  su construcción es una fase con su propio plan, no una corrección de esta
  pasada. Esta pasada solo podía escribir
  `docs/evento-2026-09-asadero-33.md` y `docs/fichas.md`.
- **Riesgo si no se toca:** grande, y con fecha. Si el evento abre el lunes 21
  con el `config.json` de hoy: (1) los premios `test1`…`test7` siguen puestos;
  (2) aunque se carguen los siete reales, **las 33 primeras jugadas de cada día
  regalan premio** y a media tarde ya no queda nada que dar; (3) la hielera, que
  es el premio mayor y solo hay dos, puede salir a las 12:30 del jueves en vez
  de por la noche.
- **Propuesta:** (a) que el usuario conteste las siete preguntas del §4 del
  documento —sobre todo **N**, las jugadas esperadas por día—; (b) abrir una
  fase de programación para A, B y C con plan prescriptivo y goldens; (c) recién
  entonces convertir el §5 del documento en `config.json`; (d) antes del lunes
  21, `python3 -m ruleta reiniciar --si` con el servicio detenido, y cotejar
  `python3 -m ruleta reporte` contra la tabla del §1 del documento.
- **Estado:** **abierta.** El documento existe y su aritmética está comprobada
  (cupo × días = stock para los siete premios, 167 piezas; el bloque JSON del
  §5.1 carga sin error en `ruleta/config.py`; los siete nombres se imprimen en
  tamaño ×4 a 48 columnas). Lo que queda abierto es A, B, C y las respuestas del
  usuario.
- **Nota del 2026-09-16 (Fase 4c):** de las tres piezas, **la A ya está
  construida** (llave `juego.consuelo.peso`, cargada con **217** en
  `config.json`; ficha **F-261**, resuelta), y los siete premios reales se
  cargaron en la Fase 4b. Por eso los puntos **(1)** y **(2)** del «Riesgo si no
  se toca» de arriba —los premios `test1`…`test7` y «las 33 primeras jugadas de
  cada día regalan premio»— **ya no son ciertos**: medido ese día con el
  `config.json` real, gana el **13.55 %** de las jugadas. Siguen abiertas las
  piezas **B** y **C**, la **D** (**F-241**) y las respuestas del §4, empezando
  por **N** (**F-263**).

---

## F-230 · El «Aviso 1» del documento del evento usa el modelo de Poisson y el programa real entrega un punto más

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §2, «Aviso 1 — el cupo es un
  **techo**, no una promesa» (tabla «Se entregan, en promedio»).
- **Qué pasa:** la tabla reproduce **exactamente** el modelo de Poisson
  E[min(X, cupo)]: agua 9.69, cerveza 8.75, tacos 3.22 cada uno, silla y set 1.46
  cada uno, total **27.79 de 33 = 84.2 %**. Pero el proceso real del programa
  **renormaliza los pesos** cuando un premio llega a su cupo y sale de la
  tómbola, así que los que quedan valen más y se entrega **un poco más**:
  simulación exacta del sorteo con N = 250 y 20 000 días → agua 9.77, cerveza
  8.85, tacos 3.25, silla 1.49, total **28.11 de 33 = 85.2 %** (≈ **140** piezas
  en los 5 días; sobrarían **~25** en vez de 26).
- **Por qué es residual:** la diferencia es de **~1 punto**, y cae dentro del
  «unas» con que está escrita la conclusión del documento («unas 139 piezas»,
  «sobrarían unas 26»). No es una afirmación falsa: es un modelo aproximado que
  se queda corto por el lado conservador. Corregirlo obliga a rehacer **toda** la
  tabla con otro modelo (simulación en vez de Poisson), y eso es una pasada
  entera, no una corrección de una celda.
- **Riesgo si no se toca:** ninguno operativo. A lo sumo, el día del evento
  sobran una o dos piezas menos de las anunciadas.
- **Propuesta:** cuando el usuario fije **N** y se rehaga el §2 con los números
  definitivos, recalcular esa tabla con la simulación del sorteo real (no con
  Poisson) y decirlo en una nota al pie.
- **Estado:** abierta.

---

## F-231 · La fila 2.0 de la tabla del factor de holgura dice 98 % y lo calculado es 98.9 %

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §2, tabla «Factor / Se entrega
  del cupo / Costo».
- **Qué pasa:** con el modelo de la propia tabla, el factor **2.0** da
  **98.93 %**; el documento escribe **98 %**. Redondeando serían 99.
- **Por qué es residual:** es **consistente con truncar**, que es lo que hacen
  las otras filas verificadas: 1.0 → 84.21 se escribe 84, y 1.25 → 92.39 se
  escribe 92. Con esa convención el 98 está bien. La única fila que quedaba
  realmente fuera de convención era la de **1.5** (decía 95 contra 96.29
  calculado), y ésa **sí** se pidió como corrección y ya se aplicó el
  2026-09-13.
- **Riesgo si no se toca:** ninguno; es un punto porcentual en una tabla que solo
  sirve para elegir entre cuatro opciones muy separadas entre sí.
- **Propuesta:** cuando se rehaga el §2, declarar la convención en una nota
  («los porcentajes van truncados») o pasar todas las filas a un decimal:
  84.2 / 92.4 / 96.3 / 98.9.
- **Estado:** abierta.

---

## F-232 · «Cuántas jugadas ganan algo» usa 34/N y con la hielera en la tómbola el total de papelitos es N+1

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §2, tabla «Cuántas jugadas ganan
  algo», renglón «Jueves 24 y viernes 25 (33 + la hielera)».
- **Qué pasa:** ese renglón calcula **34 ÷ N** (con N = 250 da **13.60 %**). Eso
  vale como **fracción de jugadas que ganan si se llenan todos los cupos del
  día**. Pero si la hielera también tiene su papelito en la tómbola **todo el
  día** —como en el bloque del §5.1, donde la hielera lleva `"peso": 1`— entonces
  el total de papelitos del jueves y del viernes no es N sino **N + 1**, y la
  cifra **por jugada** baja a 34 ÷ 251 = **13.55 %**.
- **Por qué es residual:** la diferencia es de **0.05 puntos** y las dos lecturas
  son legítimas; lo que falta es decir de cuál se habla. Además el número solo se
  usa para la frase de calle «gana más o menos 1 de cada 8 personas», que no
  cambia.
- **Riesgo si no se toca:** confusión menor si alguien rehace la cuenta y no le
  da igual.
- **Propuesta:** al rehacer el §2, aclarar en una nota que el renglón supone que
  **se llenan los cupos**, y que la probabilidad por jugada del jueves y el
  viernes se reparte entre **N + 1** papelitos mientras la hielera esté en la
  tómbola.
- **Estado:** abierta.

---

## F-233 · El párrafo del reloj está en «lo que YA se puede cargar hoy» pero habla de las franjas, que son la pieza B

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §5.1, párrafo que empieza
  «**Sobre el reloj:** las franjas dependen de la hora de la Pi…».
- **Qué pasa:** el §5.1 se titula «Lo que YA se puede cargar hoy» y ese párrafo
  habla de **las franjas**, que son la **pieza B**, todavía **pendiente de
  construir**. El contenido es correcto y el aviso importa mucho (en producción
  la Pi va sin red, así que la **batería del RTC** tiene que estar puesta y la
  hora correcta antes del lunes 21), pero está en la sección equivocada.
- **Por qué es residual:** no es una afirmación falsa —lo que dice del reloj es
  cierto— sino un problema de **ubicación**. Y el aviso del RTC vale igual aunque
  no haya franjas: la fecha del día operativo y los `desde`/`hasta` de los
  premios también dependen del reloj de la Pi.
- **Riesgo si no se toca:** que alguien lea el §5.1 y crea que las franjas ya
  funcionan.
- **Propuesta:** mover el párrafo al §5.2 (junto a la pieza B), **o** dejarlo
  donde está con la marca **PENDIENTE DE CONSTRUIR · pieza B** y separar en un
  renglón aparte el aviso del RTC, que sí aplica hoy.
- **Estado:** abierta.

---

## F-234 · El documento del evento no dice en ninguna parte qué tiene `config.json` hoy

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §6 («Cómo se modifica este
  documento y qué pasa después»); `config.json`, bloque `premios`.
- **Qué pasa:** el documento explica cómo se convertirá en `config.json`, pero
  **nunca dice qué hay cargado hoy**. Medido el 2026-09-13 en el `config.json`
  del repo: **siete premios de prueba, `TEST 1`…`TEST 7`**, con pesos
  **4 / 4 / 1 / 25 / 25 / 25 / 25**, stocks **10 / 10 / 1 / 50 / 50 / 50 / 50**,
  topes diarios **2 / 2 / 1 / 10 / 10 / 10 / 10** y **sin** `desde` ni `hasta`.
  Nada de eso se parece al evento.
- **Por qué es residual:** el documento no afirma lo contrario en ningún lado; es
  una **ausencia**, no una falsedad. La **F-229** ya deja constancia de que los
  `test1`…`test7` siguen puestos, pero lo hace en `docs/fichas.md`, que el dueño
  del restaurante no lee.
- **Riesgo si no se toca:** que el dueño edite el documento, vea que «todo
  cuadra» y suponga que la Pi ya está cargada con sus siete premios. Si el evento
  abriera así, la ruleta repartiría `TEST 1`…`TEST 7`.
- **Propuesta:** agregar al §6 un renglón corto al principio: «**Hoy la Pi tiene
  premios de prueba** (`TEST 1` a `TEST 7`). Lo de este documento **todavía no
  está cargado**», y remitir al paso 5 del mismo §6
  (`python3 -m ruleta reiniciar --si`).
- **Estado:** abierta.

---

## F-235 · La marca * del §1 dice «propuesta mía» sobre nombres que en realidad salen del dictado

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §1, columna «NOMBRE EN EL
  BOLETO» y la nota «**\*** = propuesta mía, **a confirmar**».
- **Qué pasa:** los siete nombres llevan la marca **\***, o sea «propuesta mía»,
  pero **los nombres salen del dictado del usuario** (Hielera Igloo, Silla de
  playa, Set BBQ, tacos de pastor, cerveza, agua fresca). Lo único que de verdad
  se propone es **la redacción para el boleto**: las mayúsculas y la forma corta
  («3 TACOS DE PASTOR» en vez de «Plato 3 tacos pastor»), más el **texto del
  detalle**.
- **Por qué es residual:** la marca peca **por exceso de prudencia**, no por
  falsedad: marcar de más como «a confirmar» no le hace creer al dueño que algo
  suyo ya está decidido, que es el daño que sí importa. Y la pregunta 6 del §4
  invita justamente a corregir esa tabla.
- **Riesgo si no se toca:** que el dueño crea que **nada** de esa tabla es suyo y
  se ponga a revisar de cero lo que ya dictó.
- **Propuesta:** precisar en la nota del §1: «**\*** = **la redacción** es
  propuesta mía (mayúsculas, forma corta y texto del detalle); **los premios y
  sus cantidades son tu dictado**».
- **Estado:** abierta.

---

## F-236 · «Peso del consuelo = N − 33» no contempla que el jueves y el viernes hay 34 premios

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §2, «La regla que propongo: el
  peso es el cupo» y «Aviso 2» (la nota «(150 → 117 · 200 → 167 · 250 → 217 ·
  300 → 267 · 400 → 367)»); §5.2, bloque **PENDIENTE A**.
- **Qué pasa:** la regla se justifica porque deja la tómbola en **exactamente N
  papelitos**, y eso es cierto de lunes a miércoles (33 premios + N − 33). Pero
  **el jueves 24 y el viernes 25 hay 34 premios** (entra la hielera), así que
  esos dos días la tómbola tiene **N + 1** papelitos. Para que la propiedad
  limpia se cumpliera también esos dos días, el peso del consuelo tendría que ser
  **N − 34**. La lista de equivalencias tampoco lo contempla.
- **Por qué es residual:** el efecto es de **un papelito entre N** (con N = 250,
  0.4 %), y el peso del consuelo es **un solo número en el `config.json`** que no
  puede cambiar por día. Elegir N − 33 para los cinco días es lo simple y lo
  correcto de operar; lo que falta es **decirlo**.
- **Riesgo si no se toca:** que alguien rehaga la cuenta del jueves, vea N + 1 y
  crea que hay un error en la regla.
- **Propuesta:** agregar media línea al §2: «el jueves y el viernes entra la
  hielera, así que la tómbola tiene N + 1 papelitos; dejamos N − 33 los cinco
  días porque el peso del consuelo es un solo valor y la diferencia es de un
  papelito».
- **Estado:** abierta.

---

## F-237 · La etiqueta «el cupo, sin ajustar» de la tabla de la silla nombra el cupo diario, no el de la franja

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §3, tabla «Peso de la silla en
  su franja», primera fila: «2 (el cupo, sin ajustar)».
- **Qué pasa:** dentro de esa franja el **cupo es 1** (así está en la tabla de
  franjas del mismo §3: «Cupo en esa franja | 1»). El **2** es el **cupo
  diario** del premio, que es también el `peso` que lleva la silla en el bloque
  del §5.1. La etiqueta mezcla los dos.
- **Por qué es residual:** **el número del cálculo está bien** —la fila compara
  qué pasaría si se usara el peso 2 sin ajustar por la duración de la franja— y
  la conclusión de la tabla no cambia. Es la **etiqueta** la que confunde.
- **Riesgo si no se toca:** que el dueño lea «el cupo» y crea que puede salir más
  de una silla por franja.
- **Propuesta:** reescribir la etiqueta como «2 (el **cupo diario**, sin ajustar
  por la franja)».
- **Estado:** abierta.

---

## F-238 · Los `id` de los siete premios son invención mía y no llevan la marca *

- **Fecha:** 2026-09-13
- **Origen:** lente doc evento
- **Dónde:** `docs/evento-2026-09-asadero-33.md` §1, primera columna
  (`hielera`, `silla`, `bbq`, `tacos3`, `tacos2`, `cerveza`, `agua`); también en
  el bloque JSON del §5.1.
- **Qué pasa:** esos siete `id` **no salen del dictado**: los propuse yo, y sin
  embargo son de las pocas celdas del §1 **sin** la marca **\***, que según la
  nota del propio §1 significa «tu dictado, literal».
- **Por qué es residual:** son **internos**: nunca los ve el cliente, no se
  imprimen en el boleto y el dueño no los va a escribir a mano. Aun así aparecen
  en `datos/boletos.csv` y en el reporte de inventario
  (`python3 -m ruleta reporte`), que sí se leen en el asadero.
- **Riesgo si no se toca:** ninguno operativo; a lo sumo el dueño ve `tacos3` en
  un reporte y no sabe de dónde salió.
- **Propuesta:** una línea bajo la tabla del §1: «los `id` de la primera columna
  son nombres cortos internos que yo elegí; solo aparecen en la bitácora y en el
  reporte de inventario, nunca en el boleto».
- **Estado:** abierta.

---

## F-239 · Las patitas del pulsador HABILITAR van metidas en terminales de cuchilla que no las sujetan

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · cableado de los botones, observado durante la sesión en vivo
- **Dónde:** el hardware: el pulsador chico metálico de tapa roja que hace de
  botón HABILITAR, en sus dos cables (azul y negro).
- **Qué pasa:** ese pulsador tiene **dos patitas planas y delgadas**, y los
  cables llevan **terminales de crimpar tipo cuchilla**, que son para cuchillas
  **anchas**. La patita entra, hace contacto y **funcionó durante toda la sesión
  del 2026-09-15** —las pulsaciones en GPIO 27 se registraron limpias—, pero el
  contacto **se sostiene por presión de una pieza que no está hecha para esa
  patita**.
- **Por qué es residual:** no es un defecto del programa ni de la documentación,
  y **hoy funciona**: los tres boletos de prueba salieron con ese cableado. Es un
  riesgo mecánico, no un fallo medido.
- **Riesgo si no se toca:** que el botón del mesero deje de responder **en medio
  del evento**, con el primer tirón del cable al mover la caja. El síntoma sería
  el peor posible para el personal: la ruleta «no hace nada» al apretar JUGAR, y
  el journal diría `Pulsación ignorada: el botón HABILITAR no está presionado`,
  que es exactamente lo mismo que dice cuando el mesero simplemente no está
  sosteniendo el botón.
- **Propuesta:** **soldar el cable a la patita**, o enrollar bien el cobre
  alrededor de ella y aislarlo, **antes del lunes 21**. Ya está anotado como
  casilla 17 de la bitácora del plan de la Fase 3 y como nota en el `README.md`
  §2 («Pulsadores con patitas delgadas»).
- **Estado:** abierta. **Requiere al usuario** (es trabajo físico sobre su
  hardware).

---

## F-240 · `config.json` dice `"led": 22` y no hay ningún LED conectado

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · estado final del cableado
- **Dónde:** `config.json` § `gpio` (`grep -n '"led"' config.json` → **44**);
  `ruleta/hardware.py` líneas **81** y **93-105**.
- **Qué pasa:** la instalación quedó **sin LED**: no hay nada conectado al pin
  15. Y `config.json` sigue diciendo `"led": 22`. **No falla**: `gpiozero` crea
  el objeto `LED(22)` sin comprobar que haya algo enchufado, y el 2026-09-15 el
  servicio arrancó `active` con `GPIO listo: jugar=17 habilitar=27 led=22`. El
  programa cree que tiene LED, lo enciende y lo apaga, y no lo ve nadie.
- **Por qué es residual:** no rompe nada, no gasta nada y el valor `null` ya está
  contemplado por el código (`ruleta/config.py`, la lista `pines` de la línea
  **313**, acepta `None` en `led`; y `EntradasGPIO.led()` sale sin hacer nada si
  `self._led is None`). Es una **decisión del usuario**, no un defecto.
- **Riesgo si no se toca:** con el pin 15 libre, como está hoy, ninguno. Pero no
  es «ninguno técnico»: con `"led": 22` el programa deja **GPIO 22 (pin físico
  15) configurado como salida** todo el tiempo y lo pone **en alto** en el estado
  «listo» (`ruleta/hardware.py`, líneas **81** y **93-105**), que es exactamente
  la situación que la decisión **D5** del plan de la Fase 3 y la ficha **F-246**
  llaman **cortocircuito** cuando un cable de botón a tierra acaba en ese pin. Y
  la casilla 17 de la bitácora está abierta —hay que **soldar** los cables de
  HABILITAR—, así que alguien va a volver a manipular el header antes del 21: de
  ahí que valga la regla de mover cables **con la Pi apagada y sin corriente**
  (README §2 y aviso 1 del diagrama), y que `"led": null` sea la única de las
  tres opciones que quita el pin de en medio. El otro riesgo, el que ya estaba
  anotado, es de
  **documentación**: el `README.md` §2 explica qué significa cada estado del LED
  («apagado = HABILITAR suelto · fijo = listo · parpadeo lento = imprimiendo ·
  parpadeo rápido = error») y en el kiosco de hoy **esa señal no existe**. Si se
  acaba el papel o falla la impresora, el mesero no tiene ningún aviso visual:
  solo el papel que no sale.
- **Propuesta:** que el usuario elija una de tres — **(a)** dejarlo como está a
  sabiendas; **(b)** poner `"led": null` para que la configuración diga la verdad;
  **(c)** conectar un LED de verdad al pin 15 con su resistencia de 330 Ω, como
  describe el README §2, y recuperar el aviso visual. La opción (c) es la única
  que **añade** algo al evento. Cualquiera de las tres cierra esta ficha.
- **Estado:** abierta. **Decisión del usuario.**

---

## F-241 · Pieza D: el programa debería esperar a que la hora esté sincronizada antes de imprimir y de aceptar jugadas

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · decisión del usuario sobre la batería RTC, y lo medido al
  arrancar la Pi esa mañana
- **Dónde:** el arranque del programa: `ruleta/app.py` (el inventario de arranque
  sale de la línea **270**, `Inventario impreso (%s). Folio actual %05d`, y el
  bucle de jugadas empieza tras `Lista. Esperando jugadas.`, línea **117**);
  `docs/evento-2026-09-asadero-33.md` §«Tres cosas que el programa TODAVÍA NO
  SABE HACER» (piezas A, B y C), donde ésta sería la **D**.
- **Qué pasa:** el usuario decidió el 2026-09-15 que **no habrá batería RTC** (no
  la consigue a tiempo) y que **la Pi llevará el internet del asadero**, de modo
  que **NTP le pone la hora al arrancar**. Pero la hora **no llega instantánea**:
  medido ese mismo día, la Pi arrancó a las **11:44:42** con el reloj en «Sep 13
  17:09» y **NTP no lo corrigió hasta las 11:47** — unos **tres minutos** con la
  fecha equivocada, y el journal de esos minutos lo muestra. El programa, hoy,
  **no mira el reloj**: arranca, imprime el inventario y acepta jugadas con la
  fecha que haya.
- **Por qué es residual:** **es una función que no existe**, no un defecto de
  conducta del código actual: el programa hace exactamente lo que está escrito.
  Y el riesgo tiene una mitigación manual que ya está documentada (encender unos
  minutos antes y mirar la fecha del boleto de inventario, `README.md` §2).
- **Riesgo si no se toca:** durante los primeros minutos tras encender —**unos
  tres** el 2026-09-15, que es la única medición que hay—, **la Pi cree que es
  otro día**, y la fecha no es decorativa en este programa:
  - el **boleto** sale con fecha y hora equivocadas, y ése es el papel que el
    cliente presenta en caja;
  - el **día operativo** se calcula mal (`juego.hora_inicio_dia` = 6), y de él
    dependen los **topes diarios** de cada premio: una jugada contada en el día
    equivocado gasta cupo de un día que no es;
  - de la fecha dependen también los campos **`desde`/`hasta`** con los que el
    documento del evento piensa repartir los premios grandes por día;
  - y el **boleto de inventario de arranque** —el papel que el dueño mira para
    saber cómo empieza el día— sale con esa fecha falsa.
- **Propuesta:** **pieza D**, como fase de programación con su propio plan: al
  arrancar, **esperar hasta unos 2 minutos** a que la hora esté sincronizada
  antes de imprimir el inventario y antes de aceptar la primera jugada; si al
  cabo de ese tiempo no lo consiguió, **arrancar igual pero avisarlo en el
  boleto** (el kiosco no se puede quedar muerto porque falle la red). Los dos
  números —los 2 minutos y qué se considera «sincronizada»— se deciden al
  planear la pieza: lo único medido hoy son los ~3 minutos del 2026-09-15, y en
  una red que **no** es la del asadero.
- **Estado:** **resuelta** el **2026-09-16** (Fase 4d, pieza D; plan
  `docs/planes/fase-4d-horas.md`). Se construyó exactamente lo que esta ficha
  proponía: al arrancar, y **solo al arrancar**, el kiosco espera hasta
  `juego.espera_hora_seg` segundos —**120** en `config.json`— preguntando **cada
  2 s** si el sistema ya sincronizó la hora (el archivo
  `/run/systemd/timesync/synchronized` y, si no existe, `timedatectl show -p
  NTPSynchronized --value`). Si lo consigue, sigue normal; si se agota el tiempo,
  **arranca igual** —el kiosco nunca se queda muerto— y escribe en el boleto de
  inventario de arranque la línea `HORA SIN CONFIRMAR: revisar fecha`, además de
  registrarlo como aviso. **Ninguna jugada espera nada.** Goldens con el
  comprobador inyectado: `tests/test_app.py`,
  `test_arranque_espera_a_que_la_hora_se_sincronice` y
  `test_arranque_avisa_en_el_boleto_si_la_hora_no_se_confirma`. **Lo que esta
  ficha pedía y NO se hizo:** no se bloquean las jugadas mientras la hora no esté
  confirmada, solo la impresión del inventario de arranque; el kiosco arranca y
  juega igual. **Falta medirlo en la Pi**: hasta el despliegue, esto solo está
  probado en la PC.
- **Nota fechada (2026-09-16, Fase 4e). YA ESTÁ MEDIDO EN LA PI, y en el caso
  duro.** El usuario **desenchufó la Pi** unos minutos y la volvió a enchufar
  —arranque en frío real, sin batería RTC—. Lo medido: el reloj arrancó en
  `1970-01-01` y **systemd** le puso encima la última hora guardada en
  `/var/lib/systemd/timesync/clock`, **4 min 54 s atrasada** (`fake-hwclock`
  **no está instalado** en esta Pi, así que no es él quien la restaura). Con esa
  fecha falsa el kiosco **no imprimió nada**: esperó **28.3 s**, NTP corrigió el
  reloj a los **34.28 s** del arranque y **el inventario salió 0.6 s después, con
  la fecha correcta** y **sin** la línea `HORA SIN CONFIRMAR`. `NRestarts=0`, 0
  ERROR/WARNING de la ruleta, `estado.json` intacto (el inventario de arranque no
  consume folio). **El riesgo que abrió esta ficha —que la Pi juegue e imprima
  creyendo que es otro día— está cerrado en hardware.** Lo que esta ficha pedía y
  **sigue sin hacerse** es bloquear también las **jugadas** mientras la hora no
  esté confirmada: el kiosco acepta jugadas desde que arranca. Evidencia:
  `docs/actas/2026-09-16-hechos-medidos-fase-4e.md` (medición 2). En la misma
  pasada el tope subió de **120 a 300 s** y la espera pasó a **verse en el
  journal** (**F-273**).

---

## F-242 · El «Contexto del producto» de `CLAUDE.md` dice «producción sin red» y «batería RTC necesaria», y desde el 2026-09-15 es falso

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · decisión del usuario sobre la batería RTC
- **Dónde:** `CLAUDE.md`, sección «Contexto del producto», la viñeta que empieza
  por **Red:** (`grep -n "En producción la Pi va sin red" CLAUDE.md`).
- **Qué pasa:** ese párrafo dice que **en producción la Pi va sin red** y que
  **por eso la batería RTC es necesaria**. El 2026-09-15 el usuario decidió lo
  contrario: **no habrá batería RTC** —no la consigue a tiempo— y **la Pi llevará
  el internet del asadero durante el evento**, que es lo que le pondrá la hora al
  encender. `CLAUDE.md` es el documento que **se lee al empezar cada sesión**: si
  se queda así, cada agente nuevo arranca con un hecho falso sobre el producto.
- **Por qué es residual (aquí):** no es que nadie lo haya medido mal —era verdad
  cuando se escribió, y el propio párrafo dice de dónde salía—, es que **la
  decisión del usuario lo derogó**. Y el ejecutor de esta fase **no podía
  arreglarlo**: `CLAUDE.md` estaba **fuera del conjunto de archivos permitido**
  del brief, y tocarlo habría sido saltarse la compuerta del commit.
- **Riesgo si no se toca:** que la próxima sesión planifique contando con la
  batería RTC —o peor, que repita la receta vieja del README y ponga
  `timedatectl set-ntp false`, que es justo lo que impediría que la hora se
  corrigiera sola—.
- **Propuesta:** **lo actualiza el orquestador**, que sí puede tocar los
  documentos de memoria y de protocolo: reescribir esa viñeta con la decisión
  del 2026-09-15, citando como evidencia `docs/actas/2026-09-15-fase-3.md` §7, y
  **sin borrar** lo que decía antes (mismo formato de nota fechada que ya usa el
  propio `CLAUDE.md` para la corrección del 2026-09-11). **En el `README.md` ya
  está hecho** en esta misma pasada: §3 («El SSH y el Wi-Fi son solo para
  instalar y probar»), §4 paso 7 y §9 («Hora o fecha incorrectas»), los tres con
  nota fechada.
- **Aviso para quien lo haga:** `CLAUDE.md` no es el único sitio con esa premisa
  derogada. `grep -n "sin red\|sin internet\|batería RTC" docs/fichas.md`
  devuelve **más de una docena** de líneas en fichas viejas que razonan a partir
  de «la Pi va sin red» o de «la batería RTC es necesaria» —entre ellas la
  **F-153**, que ya lleva su nota fechada del 2026-09-15—. No hay que reescribir
  esas fichas (su texto histórico vale y sus conclusiones no dependen todas de la
  premisa), pero quien actualice `CLAUDE.md` conviene que sepa que existen.
- **Estado:** abierta. **Le toca al orquestador** (fuera del alcance del ejecutor
  de la Fase 3).
- **Nota de cierre del 2026-09-15 (cierre documental de la Fase 4a).**
  **RESUELTA: el orquestador actualizó `CLAUDE.md` en este mismo cambio.** Se
  editó **únicamente** la sección «Contexto del producto» —las secciones 1 a 7 y
  «Convenciones de este repo» no se tocaron ni una letra—, con la decisión del
  usuario del 2026-09-15 escrita como **nota fechada que conserva lo que decía
  antes**: en el evento la Pi tendrá **el internet del asadero** (NTP le pone la
  hora al arrancar) y **no habrá batería RTC**, con el riesgo del primer minuto
  tras encender nombrado y remitido a la **pieza D** (**F-241**). De paso, esa
  misma sección recogió lo demás que faltaba del producto: los **botones
  cableados** (JUGAR GPIO 17 / pin 11, HABILITAR GPIO 27 / pin 13, tierras en los
  pines 9 y 25, **sin LED conectado**), lo que la impresora contesta de verdad
  (`DLE EOT 2` es la única que se entera del rollo agotado) y el recordatorio de
  **reiniciar el inventario**, que iba por el folio 16. El **`README.md` ya
  estaba corregido** desde la pasada anterior. **Lo que esta ficha avisaba y
  sigue siendo cierto:** hay más de una docena de líneas en fichas viejas que
  razonan desde «la Pi va sin red»; **no se reescriben**, pero quien las lea que
  sepa que la premisa está derogada.

---

## F-243 · Las tres jugadas de prueba dejaron el inventario real en folio 3

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · estado de los datos al cerrar la sesión
- **Dónde:** en la Pi, `datos/estado.json` y `datos/boletos.csv`.
- **Qué pasa:** las jugadas del 2026-09-15 no fueron una simulación: **gastaron
  folio e inventario**. Medido al cerrar la sesión de hardware (12:31):
  `estado.json` con **folio 3**, `test4`, `test7` y `test6` **entregados una vez
  cada uno** y `boletos_por_dia` del **2026-09-15 en 3**; `boletos.csv` con **6
  líneas** (`emitido` + `impreso` por cada boleto). **Pero el día siguió:** el
  usuario jugó por su cuenta entre las 12:31 y las 13:18 (folios **4 a 8**, todos
  impresos), hubo la prueba sin papel de las 13:29 (folio **9**, descontado sin
  boleto, **F-091**) y una jugada final a las 13:33:23 (folio **10**). **El
  estado real al cerrar el día es folio 10**, con `test4`=1, `test7`=4,
  `test6`=3 y `test5`=2.
- **Por qué es residual:** era **el precio conocido** de probar en hardware real
  —la Fase 2 ya lo había dejado escrito: «cada pulsación de prueba gasta papel y
  consume un folio»— y tiene un comando de una línea que lo deshace.
- **Riesgo si no se toca:** que el evento empiece con **diez premios contados
  como ya entregados** y el folio arrancando en el 11. Con los premios de prueba
  (`test1`…`test7`) da igual, pero **la Fase 4 va a cargar los premios reales**,
  y ahí diez piezas de inventario fantasma sí se notan —y una de ellas, el folio
  9, es un premio que **el programa cree entregado y del que no existe boleto**
  (**F-091**)—. Además el primer boleto del lunes no diría 00001.
- **Propuesta:** **antes del lunes 21**, con el servicio parado:
  `python3 -m ruleta reiniciar --si` (respalda lo anterior y deja folio y
  contadores en cero) y volver a arrancar. Es el mismo paso 5 que ya pide el §6
  del documento del evento, y la casilla 19 de la bitácora del plan de la Fase 3.
  Conviene hacerlo **junto con** la carga de los premios reales, no antes, para
  no tener que repetirlo.
- **Estado:** **CERRADA** el **2026-09-16** (Fase 4e, deploy de las 14:44). La
  fecha límite era el lunes 21 y **se cumplió cinco días antes**: ver la última
  nota fechada de esta ficha. Antes decía: «abierta (pendiente, con fecha límite:
  el lunes 21 de septiembre)».
- **Nota fechada (2026-09-16, cierre documental de las Fases 4b, 4c y 4d).**
  **El folio ya no es 16, y el inventario se reinició DOS veces el 2026-09-16,
  pero esta ficha SIGUE ABIERTA.** Primero en el deploy de la Fase 4b, a las
  **00:10**, con los premios reales ya cargados: la salida literal fue «Folio
  actual: 00016. Premios entregados registrados: 0. Respaldo:
  `datos/estado_20260916_001053.json` / `datos/boletos_20260916_001053.csv`.
  Inventario reiniciado. Folio en 00000.». Y otra vez a las **12:46**, ya con
  la Fase 4d desplegada, para que el usuario probara limpio el reparto por
  horas: antes iba en **folio 6** —agua 3, bbq 1, cerveza 1 y el consuelo
  00006 de las 12:46:12—, con respaldos
  `datos/estado_20260916_124629.json` y `datos/boletos_20260916_124629.csv`.
  **Después de ese segundo reinicio el usuario volvió a jugar** («salieron
  consuelos y una cerveza»), así que el inventario **no está en cero** y
  **hay que reiniciarlo otra vez el lunes 21 antes de abrir**, en la misma
  pasada que carga las fechas de la **F-259**. Lo que sí se puede tachar de
  esta ficha es el número: **los premios de prueba `test1`…`test7` ya no
  existen** y los diez boletos que esta ficha contaba **ya no cuentan como
  premios entregados**. **Ojo:** `reiniciar` respalda `estado.json` y
  `boletos.csv`, **no `ruleta.log`**, y `boletos.csv` se **mueve** al
  respaldo y se vuelve a crear con el primer boleto. La continuación con
  fecha límite vive en **F-262**. Evidencia:
  `docs/actas/2026-09-16-fase-4bcd.md` §3.4 y §5.6.
- **Nota fechada (2026-09-16, cierre documental de la Fase 4e). ESTA FICHA QUEDA
  CERRADA.** El inventario se reinició **por tercera y última vez** el
  2026-09-16, en el **deploy de las 14:44**, con el servicio parado y **después
  de que el usuario dijera que ya había terminado de probar** («listo, ya terminé
  las pruebas, reinicia el inventario para que quede listo»). Salida literal:
  «Folio actual: 00010. Premios entregados registrados: **2**. Respaldo:
  `datos/estado_20260916_144415.json` / `datos/boletos_20260916_144415.csv`.
  Inventario reiniciado. **Folio en 00000**.» Los dos premios que se borraron
  eran **una cerveza y un agua** de esas pruebas. El servicio volvió a arrancar a
  las **14:44:37** y el verificador leyó en vivo «Inventario impreso (arranque).
  Folio actual **00000**». **Ya no hace falta el reinicio del lunes 21**, ni
  siquiera por el motivo original: con las fechas de la **F-259** cargadas,
  ningún premio puede salir antes del 21, así que lo único que podría moverse es
  el **folio**, y eso es **decisión del usuario** (**F-262**). Lo que sí conviene
  saber, y no es un fallo: **`boletos.csv` se movió al respaldo** y no vuelve a
  existir hasta el primer boleto (**F-277**). Evidencia:
  `docs/actas/2026-09-16-fase-4e.md` §7.2 y §7.3.

---

## F-244 · `pkill -f` dentro de un `ssh 'bash -c …'` que contiene el patrón literal mata al propio bash

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · trampa medida en la sesión (pasó tres veces)
- **Dónde:** cualquier comando de la forma
  `ssh ruleta 'bash -c "pkill -f /tmp/monitor-botones.py; …"'`.
- **Qué pasa:** el `bash` remoto **se ve a sí mismo** en la tabla de procesos —su
  línea de comando contiene el patrón que se le está pidiendo matar—, así que
  `pkill -f` lo mata, y **nada de lo que venía detrás del `;` se ejecuta**.
  El síntoma engaña: el comando «termina» sin error visible y el trabajo no se
  hizo. **Pasó tres veces** la mañana del 2026-09-15 antes de que se entendiera.
- **Por qué es residual:** es una trampa del entorno, no del repositorio: no hay
  ningún archivo del proyecto que esté mal.
- **Riesgo si no se toca:** se vuelve a perder media hora la próxima vez que
  alguien tenga que limpiar un proceso en la Pi por SSH.
- **Propuesta:** ya está escrita como **trampa 1** de la §5 del plan de la Fase 3.
  La receta: escribir el patrón con corchetes (`[m]onitor-botones`), que no
  coincide consigo mismo, y **no repetir la ruta literal** en el mismo comando
  —guardarla en una variable (`M=/tmp/monitor-botones.py`) y usar la variable—.
- **Estado:** **cerrada de entrada** (nota de trampa: queda documentada en el
  plan §5, no hay nada que arreglar en el repositorio).

---

## F-245 · Un proceso lanzado por SSH en segundo plano cuelga la sesión hasta el timeout, pero sobrevive

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · trampa medida en la sesión
- **Dónde:** los lanzamientos del monitor y de los escáneres en la Pi
  (`/tmp/monitor-botones.py`, `/tmp/scan-pines.py`).
- **Qué pasa:** aunque se use `setsid` + `nohup` y se redirijan las tres salidas,
  **la conexión SSH no devuelve el control**: se queda colgada hasta que salta el
  timeout. El proceso, en cambio, **sí arranca y sí sigue vivo**. Es decir: la
  señal que uno mira para saber si funcionó (que el comando vuelva) miente en las
  dos direcciones.
- **Por qué es residual:** trampa del entorno; no hay nada mal en el repositorio.
- **Riesgo si no se toca:** que alguien concluya que el proceso no arrancó, lo
  relance, y acabe con **dos monitores** peleándose por los mismos pines GPIO —lo
  que en `gpiozero` significa que el segundo falla al reservar el pin, o peor,
  que se mezclen dos registros en el mismo archivo—.
- **Propuesta:** ya está escrita como **trampa 2** de la §5 del plan de la Fase 3.
  La receta: no esperar a que vuelva el `ssh`; **abrir una conexión nueva** y
  comprobar el proceso y su archivo de log desde ahí.
- **Estado:** **cerrada de entrada** (nota de trampa).

---

## F-246 · Los escáneres de pines deben declarar SOLO entradas: el primer monitor ponía GPIO 22 como salida

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · desviación detectada durante la propia sesión
- **Dónde:** el primer `/tmp/monitor-botones.py` de la sesión, que además de los
  dos `Button` creaba un `LED(22)` y lo ponía a parpadear.
- **Qué pasa:** ese monitor dejaba **GPIO 22 (pin físico 15) configurado como
  salida**. Un pin de salida en alto, conectado a tierra a través de un botón,
  es un **cortocircuito**. Y el motivo por el que se estaba corriendo el monitor
  era, precisamente, que **no se sabía dónde estaban conectados los cables**: la
  sesión terminó descubriendo un cable en un pin que nadie esperaba (el 23). Si
  esa noche hubiera habido un cable en el **pin 15**, la herramienta de
  diagnóstico habría provocado el daño que venía a evitar.
- **Por qué es residual:** **no llegó a pasar** —no había nada en el pin 15— y se
  corrigió de raíz en la misma sesión: los dos escáneres posteriores
  (`/tmp/scan-pines.py`, 17 pines primero y 26 después) declararon **todos** los
  pines como **entrada con pull-up**, ninguno como salida.
- **Riesgo si no se toca:** que la próxima vez que alguien improvise una
  herramienta de diagnóstico de GPIO copie el patrón del LED y sí queme algo. La
  Pi 5 no es barata y el evento es en menos de una semana.
- **Propuesta:** queda como **regla escrita**, no como recordatorio: decisión
  **D5** y **trampa 3** de la §5 del plan de la Fase 3, y **prohibición 3** de su
  §8 — «no se declara ningún pin como salida en una herramienta de diagnóstico».
- **Estado:** **cerrada** el 2026-09-15: corregida en la misma sesión y escrita
  como decisión, trampa y prohibición en `docs/planes/fase-3-botones.md`.

---

## F-247 · El diagrama de cableado lo generó el orquestador, y lo verificó un agente distinto

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · desviación de rol, anotada por el propio orquestador
- **Dónde:** `docs/cableado-botones.svg` (18 638 bytes); su generador,
  `gen_cableado.py`, vive **solo en el scratchpad de la sesión**, que es efímero.
- **Qué pasa:** el §1 del protocolo dice que **Fable no escribe código** y que
  solo toca documentos de memoria y archivos efímeros de sesión. El SVG del
  cableado lo produjo **un programa que escribió Fable**. La atenuante, que es
  real: el generador es **un archivo efímero del scratchpad**, nunca entró al
  repositorio, y **Fable no verificó su propia salida** — la verificó un **agente
  independiente** contra el pinout oficial J8 del conector de 40 pines, contra
  `config.json` y contra el `README.md` §2, y **encontró un defecto real**: las
  etiquetas de los pines 11 y 13 se encimaban. Se corrigió y se volvió a
  verificar.
- **Por qué es residual:** el resultado está verificado por un tercero y el
  código que lo produjo no vive en el repositorio; no hay nada que mantener ni
  que probar. Es una desviación de procedimiento, anotada para que no siente
  precedente.
- **Riesgo si no se toca:** que la próxima vez se dé por bueno que «el
  orquestador escriba un script rápido» sin pasar por la verificación
  independiente, que es la parte que de verdad atrapó el error.
- **Propuesta:** dejarlo anotado aquí y en la §8 del acta de la Fase 3. Si alguna
  vez hay que **regenerar** el diagrama (por ejemplo si se conecta el LED o
  cambian los pines), que sea un **ejecutor** quien escriba el generador y lo
  deje en `herramientas/`, con su verificación.
- **Estado:** **cerrada** el 2026-09-15 (desviación anotada; el diagrama está
  verificado y en el repositorio).

---

## F-248 · El SVG del cableado entra al repositorio con finales de línea CRLF, y `.gitattributes` no dice nada de `*.svg`

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · medición del ejecutor al copiar el diagrama al repositorio
- **Dónde:** `docs/cableado-botones.svg` y `.gitattributes`
  (`grep -n "svg" .gitattributes` → **no devuelve nada**).
- **Qué pasa:** el archivo se copió **byte a byte** desde el scratchpad —mismo
  tamaño, 18 638 bytes, y mismo `sha256` (`b238da27…`), comprobado— y trae
  **finales de línea CRLF** (214 de 214). Pero `.gitattributes` solo declara
  `*.sh`, `*.service`, `*.py`, `*.json` y `*.md` como texto con LF, y en esta PC
  `core.autocrlf` está en `true`: `git check-attr text -- docs/cableado-botones.svg`
  responde **`unspecified`**, así que **git normalizará esos CRLF a LF al
  guardarlo**. El archivo del repositorio y el archivo del disco no tendrán el
  mismo hash.
- **Por qué es residual:** **el dibujo se ve exactamente igual** con CRLF o con
  LF; un SVG es texto XML y ningún visor se entera. No afecta a nada que se
  ejecute.
- **Riesgo si no se toca:** confusión al verificar. Quien compare el `sha256` del
  archivo desplegado con el de este documento verá dos números distintos y
  pensará que alguien tocó el diagrama. Es la misma historia que la **F-219**,
  la de `logo.png`.
- **Propuesta:** añadir `*.svg text eol=lf` a `.gitattributes` (una línea, junto
  a las otras cinco) **o**, si se prefiere no tocar ese archivo, dejar constancia
  —como aquí— de que el hash que manda es el de la copia de trabajo y que git
  guarda la versión con LF. `.gitattributes` estaba **fuera del conjunto de
  archivos permitido** de esta fase, por eso no se hizo.
- **Estado:** abierta (decisión menor; cualquiera de las dos salidas la cierra).

---

## F-249 · Muchas fichas viejas remiten «a la Fase 3» para arreglos de CÓDIGO, y la Fase 3 que se ejecutó fue solo de cableado

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · cierre documental, al repasar `docs/fichas.md`
- **Dónde:** `docs/fichas.md`, las entradas que dicen «Fase 3» en su
  **Propuesta** o en su **Estado** (`grep -n "Fase 3" docs/fichas.md`): entre
  ellas rechazar rutas inexistentes bajo `/dev/` (**F-152**, cuyo Estado dice
  literalmente «abierta (Fase 3)», y su ficha madre **F-090**), distinguir
  «papel: no contestó» de «papel: hay», llamar a `beep()` tantas veces como
  pitidos se quieran, los valores por defecto duplicados entre constructor y
  llamadores, y el zumbador propio en un GPIO (**F-194**).
- **Qué pasa:** cuando se escribieron esas fichas, «la Fase 3» era el nombre de
  *la siguiente vez que alguien toque código*. La Fase 3 que **de verdad se
  ejecutó** el 2026-09-15 fue **solo de hardware**: cablear los dos botones y
  demostrarlos. **No se tocó ni una línea de código, ni `config.json`, ni los
  tests**, y por tanto **ninguna de esas fichas se resolvió ni se cerró**.
- **Por qué es residual:** ninguna de ellas es un defecto de conducta ni un
  golden en rojo; son mejoras aplazadas, y siguen exactamente igual de aplazadas
  que ayer. Lo único que cambió es que **el número de fase al que apuntan ya está
  gastado**.
- **Riesgo si no se toca:** que alguien lea «Estado: abierta (Fase 3)», vea que
  la Fase 3 está cerrada en el plan y en el acta, y **dé la ficha por resuelta**
  sin que nadie haya tocado nada.
- **Propuesta:** no reescribir las fichas una a una —son varias y el texto
  histórico vale—, sino dejar **esta** como aviso cruzado, y que la próxima fase
  de código empiece por `grep -n "Fase 3" docs/fichas.md` y reasigne a mano las
  que siga teniendo sentido hacer. Las dos fichas cuyo **Estado** hablaba de la
  Fase 3 como momento de decisión —**F-185** y **F-194**— sí llevan ya una nota
  fechada del 2026-09-15.
- **Estado:** abierta (aviso cruzado; se cierra cuando una fase de código las
  reasigne).

---

## F-250 · Con el rollo agotado el kiosco emite, descuenta y da por impreso un boleto que no sale

- **Fecha:** 2026-09-15
- **Origen:** Fase 3 · prueba deliberada sin papel de las 13:29, con el usuario
  en vivo
- **Dónde:** `ruleta/escpos.py`, la consulta de estado de `ImpresoraArchivo`
  (`grep -n "CMD_ESTADO_PAPEL\|CMD_ESTADO_IMPRESORA\|_MASCARA_FIJA_ESTADO" ruleta/escpos.py`)
  y su uso antes de cada boleto.
- **Qué pasa:** la consulta `DLE EOT` que añadió la sub-fase 2b **no protege
  nada cuando de verdad hace falta**. Medido el 2026-09-15 a las 13:29:17, con el
  servicio `active`: con la impresora **sin papel**, el journal dijo
  `Boleto 00009 emitido: TEST 7` → `WARNING … reporta poco papel` →
  `Boleto 00009 impreso: TEST 7`. **Ni «sin papel» ni «fuera de línea» se
  detectaron.** La causa es la que ya se diagnosticó el 2026-09-13: **la
  impresora repite el último byte de estado y el programa lee la respuesta a la
  pregunta anterior**; un desfase de un comando basta para derrotar a las dos
  guardias. El resultado: `boletos.csv` con el folio 00009 `emitido` **e**
  `impreso`, `estado.json` en folio 9 y el premio **TEST 7 descontado del
  inventario sin que saliera papel**. El proceso ni siquiera se enteró —`wchan`
  en `hrtimer_nanosleep`, `NRestarts=0`—: la escritura al nodo `usblp` no se
  bloquea porque la impresora **acepta los bytes en su búfer** y los retiene.
- **Por qué está aquí y no como parada de fase:** **no es residual por su
  gravedad, lo es por su alcance.** La Fase 3 era de cableado: no tocó código, ni
  `config.json`, ni los tests, y el arreglo **espera la autorización del
  usuario**, igual que el del aviso falso de poco papel. Se anota aquí, con la
  medición entera, para que la Fase 4 no empiece sin saberlo. Es hermana de la
  **F-091**, que es donde vive la historia de esta consulta.
- **Riesgo si no se toca:** durante la semana del evento, **cada jugada con el
  rollo agotado regala un folio y un premio sin entregar boleto**, en silencio.
  El cliente se va sin nada, el inventario baja igual, y el descuadre solo
  aparece si alguien cuadra `boletos.csv` contra los boletos que llegaron a caja.
  Con 33 premios al día y una impresora que ya avisa de poco papel desde el
  2026-09-11 (**F-190**), no es un caso raro: es el caso de cualquier tarde en
  que nadie mire el rollo.
- **Atenuante medida, que no resuelve nada:** al reponer el papel (13:31–13:33)
  la impresora **soltó sola** el boleto retenido en su búfer, cortado. Depende de
  que nadie apague nada: si se apaga la impresora o la Pi antes de reponer, el
  trabajo se pierde y el programa ya lo dio por impreso; y si el papel se acaba a
  media impresión, sale un boleto incompleto. Ninguno de esos dos límites se
  provocó: están razonados en el archivo de hechos, no medidos.
- **Propuesta (la que deja escrita el archivo de hechos):** en la **Fase 4**,
  **leer la respuesta FRESCA**: tras mandar el `DLE EOT`, leer hasta unos **64
  bytes o 150 ms** y quedarse con el **último byte válido**, o **drenar el búfer
  con un tope** antes de preguntar. Eso, **además** de la máscara estricta que ya
  estaba propuesta. Mientras no exista el arreglo, la única defensa es de
  procedimiento: **rollo de repuesto junto a la Pi y mirar el papel** (**F-190**),
  y cuadrar `boletos.csv` contra la caja al cerrar el día.
- **Estado:** abierta. **Riesgo abierto más grande que deja la Fase 3.**
  **Requiere autorización del usuario** para tocar código.
- **Nota del 2026-09-15 (Fase 4a).** El usuario autorizó el arreglo y **el
  código ya está escrito**: `leer_estado_fresco` en `ruleta/escpos.py` (drenar,
  preguntar, quedarse con el **último** byte válido) y la pregunta `DLE EOT 2`
  en `verificar_estado`, que es la única que en esta impresora se entera del
  rollo agotado (`0x32`). La suite pasa de **194** a **214** pruebas y **9 de
  las 10 mutaciones** del plan quedaron en rojo (la décima, **M6**, no puede
  ponerse en rojo: ver **F-252**). **Esta ficha NO se cierra todavía:** se cierra
  con la **prueba en vivo sin papel** del Paso 11 del plan, que al escribir esto
  no se ha hecho. Hasta entonces, lo medido es que el arreglo funciona **contra
  los dobles de prueba**, no contra la impresora.
- **RESUELTA el 2026-09-15 a las 21:32, por
  `2a0aba3e01dcd15878579f1d02a64457b1834046` y su prueba en vivo.** La prueba en
  vivo del Paso 11 **ya se hizo**, contra la impresora, con el usuario sacando y
  reponiendo el rollo, y **los cinco criterios salieron en verde**:
  (1) el journal dijo `Boleto 00013 NO impreso (premio devuelto al inventario):
  la impresora /dev/ruleta-impresora no tiene papel`, **sin un solo «poco
  papel»**, y lo repitió con el **00014** a las 21:32:28; (2) **no hubo ninguna
  línea «impreso»** para esos dos folios; (3) `boletos.csv` los marcó
  `emitido` + `error_conexion` y `estado.json` conservó `test5` = **2**, o sea
  que **el premio volvió al inventario las dos veces**; (4) **al reponer el
  rollo no salió ningún boleto retenido** —que es justo lo contrario de lo que
  pasó a las 13:29, cuando la impresora soltó sola el 00009—; y (5) las jugadas
  siguientes imprimieron normal (**00015** a las 21:32:59 y **00016** a las
  21:33:23). El servicio no se reinició en ningún momento (`NRestarts=0`, PID
  1115). Antes de eso, el deploy había dejado **214 pruebas OK en la Pi** y
  **cero** avisos de poco papel desde el restart de las 21:26:42. Evidencia:
  `docs/actas/2026-09-15-fase-4a.md` §7 y §8, y
  `docs/actas/2026-09-15-hechos-medidos-fase-4a.md`. **Lo que esta ficha NO
  cubre y se va a otra:** sin LED conectado, el personal **no percibe** que la
  jugada fue rechazada —el usuario dijo «no vi ninguna diferencia realmente»—;
  eso es **F-256**. Y el caso de que el papel se acabe **a media impresión**
  sigue sin provocarse: `ErrorEnvio` no revierte el premio, a propósito.

---

## F-251 · Se abre la Fase 4a (papel) con su plan prescriptivo, y hay cuatro afirmaciones de documento que siguen siendo falsas hasta que la fase las corrija

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · redacción del plan prescriptivo, desde el archivo de
  hechos del orquestador
- **Dónde:** `docs/planes/fase-4a-papel.md` (nuevo) y
  `docs/actas/2026-09-15-hechos-medidos-fase-4a.md` (copia literal del archivo
  de hechos, 4979 bytes,
  `sha256 2efbe4c10cbda88eda3382d607bc887008b9e5bfac7c6ec6c94d4e7e4b2bf300`).
- **Qué pasa:** queda **abierta la Fase 4a**, una sub-fase de programación que
  arregla el camino del papel y **solo** eso: leer la respuesta **fresca** del
  `DLE EOT` (drenar, preguntar y quedarse con el **último** byte), añadir la
  consulta **`DLE EOT 2`** —la única que en esta impresora cambia de verdad
  cuando se acaba el papel: `0x12` con papel, **`0x32`** sin papel, medido el
  2026-09-15— y endurecer la máscara de «poco papel» a la **pareja** de bits.
  Cierra las filas **21** y **21-ter** de la bitácora de la Fase 3 y resuelve
  las fichas **F-250** y la parte de **F-091** que quedó en rojo el 2026-09-15 a
  las 13:29, cuando el kiosco emitió el boleto **00009**, descontó **TEST 7** y
  lo dio por impreso sin que saliera papel.
- **Por qué está aquí y no es una parada de fase:** es el **registro de apertura**
  de la fase, no un hallazgo. Se anota para que quede fechado quién abrió la
  fase, con qué evidencia y con qué alcance, y para que la lista de abajo no se
  pierda si la cadena se interrumpe a medias.
- **Lo que sigue siendo FALSO en el repositorio mientras la fase no termine**
  (son las correcciones C1 a C8 del escéptico del 2026-09-13, que nunca llegaron
  a aplicarse, y están detalladas una por una en el **Paso 8** del plan):
  1. **F-091**, línea de Estado: dice «así que la consulta funciona de verdad
     por cable y lanzada desde systemd». Lo demostrado por cable es que el nodo
     **acepta la escritura** del comando, no que la respuesta leída sea la suya.
  2. **F-190**, título y «Qué pasa»: atribuyen el aviso al **sensor *near-end***.
     No hubo sensor: era `0x16`, la respuesta sana de `DLE EOT 1`, leída con la
     tabla de `DLE EOT 4`. Y lo medido el 2026-09-15 va más lejos: en esta
     impresora `DLE EOT 4` contesta `0x12` **incluso con el rollo fuera**.
  3. **`docs/planes/fase-2-impresora.md`**, tabla de pendientes (filas «Aviso de
     «sin papel» por USB» y «Cambiar el rollo de papel»): la primera da por
     funcionando en hardware real algo que falló, y la segunda manda cambiar un
     rollo que está bien.
  4. **`docs/actas/2026-09-11-fase-2.md`**, tabla de cierre, fila «Impresora»:
     dice «avisando de **poco papel** (sensor *near-end*)». **Esa fila no se
     reescribe** —las actas son evidencia—: lleva una **nota fechada** debajo.

  Se suma una quinta, que no es del escéptico sino de esta fase:
  **`docs/planes/fase-2-impresora.md:2392`** fija los números de línea de
  `escpos.py` («58-60 y 64-66, 104, 118-125 y 661-662») y de `__main__.py`
  («351-355»), y **esta fase los mueve todos**: hay que re-medirlos en el mismo
  commit.
- **Riesgo si no se toca:** el evento empieza el **lunes 21 de septiembre de
  2026** y dura una semana. Cada jugada con el rollo agotado **regala un folio y
  un premio**, en silencio, y el aviso falso de poco papel enseña al personal a
  ignorar los avisos del programa, que es exactamente lo contrario de lo que
  hace falta.
- **Propuesta:** ejecutar el plan `docs/planes/fase-4a-papel.md` completo, con su
  cadena: ejecutor, lentes en paralelo, escéptico, commit compuertado, deploy
  observado y **prueba en vivo sin papel** con el usuario delante (Paso 11), que
  es el único criterio que de verdad cierra la fase.
- **Estado:** **abierta** el 2026-09-15 (plan escrito, ninguna casilla de la
  bitácora marcada, ninguna línea de código tocada). Se cierra cuando el §7 del
  plan esté entero en verde.
- **Nota del 2026-09-15 (fin del paso del ejecutor).** Las **cinco**
  afirmaciones falsas de la lista de arriba están **corregidas** en este mismo
  cambio: la 1 en **F-091** (C1 y C1-bis), la 2 en **F-190** (C2 y C3), la 3 en
  las dos filas de la tabla de pendientes de la Fase 2 (C5 y C6), la 4 con la
  **nota fechada** debajo de la tabla del acta —la fila no se tocó— (C7) y la 5
  con los números de línea **re-medidos** de `escpos.py` y `__main__.py` (C9).
  La ficha **sigue abierta**: lo que la cierra es el §7 entero, y el **Paso 11**
  —la prueba en vivo sin papel— todavía no se ha hecho.

---

## F-252 · La mutación M6 del plan de la Fase 4a NO puede ponerse en rojo: en Python `&` liga MÁS fuerte que `==`

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · ejecutor, corriendo la tabla de mutaciones del §6 sobre
  copias del repositorio
- **Dónde:** `docs/planes/fase-4a-papel.md` §2 (**D3**), §3 (**trampa 3**) y §6
  (fila **M6**); el código afectado es `ruleta/escpos.py` (`verificar_estado`) y
  `ruleta/__main__.py` (`interpretar_estado_papel`).
- **Qué pasa:** el plan daba por cierto que «en Python `==` liga **más fuerte**
  que `&`» —§2 (**D3**), §3 (**trampa 3**) y la fila **M6** del §6, **corregidos
  en este mismo cambio**—, y de ahí deducía que sin paréntesis
  `papel & BITS_POCO_PAPEL == BITS_POCO_PAPEL` se evaluaría como `papel & True`,
  es decir `papel & 1`. **Eso es falso en Python** (es cierto en C, que es de
  donde viene la costumbre). En Python las comparaciones tienen precedencia
  **menor** que los operadores de bits, así que las dos formas son la **misma
  expresión**. Medido el 2026-09-15 en la PC (Python 3.14.4), comparando el
  árbol de sintaxis de las dos:

  ```
  con paréntesis: Compare(left=BinOp(Name papel, BitAnd, Name BITS_POCO_PAPEL), ops=[Eq], ...)
  sin paréntesis: Compare(left=BinOp(Name papel, BitAnd, Name BITS_POCO_PAPEL), ops=[Eq], ...)
  mismo AST: True
  ```

  Y con los vectores de los goldens: `0x1e` da `True` de las dos formas y `0x16`
  da `False` de las dos formas; lo que el plan suponía (`papel & True`) daría
  `0` en los dos casos.
- **Consecuencia medida:** **M6 sobrevive en verde** (las **214** pruebas pasan
  con los paréntesis quitados), y **ningún golden puede evitarlo**: no es que el
  assert no muerda, es que la mutación **no cambia el comportamiento**. Las
  otras **nueve** mutaciones del §6 sí quedaron en rojo.
- **Por qué es residual:** no hay defecto en el código. Los paréntesis **se
  quedan** (los manda **D3** y se leen mejor), pero son de **legibilidad**, no
  de corrección. Lo que M6 quería proteger —que la máscara sea una igualdad de
  **pareja** y no un «algún bit»— ya lo protege **M5**, que cae con **3**
  pruebas (`test_el_byte_medido_0x16_no_avisa_de_poco_papel` en los dos
  transportes y `TestLecturaFrescaAOMU.test_poco_papel_de_verdad_avisa_y_el_byte_medido_no`).
- **Propuesta:** la **trampa 3**, la justificación de **D3** y la fila **M6** del
  §6 de `docs/planes/fase-4a-papel.md` **ya no afirman nada falso sobre el
  lenguaje**: el ejecutor corrigió ese texto en este mismo cambio, porque una
  afirmación de documento falsa sí entra en la parada del §5 del protocolo. Lo
  que **sigue pendiente del orquestador** es qué se hace con **M6**: retirarla de
  la tabla, sustituirla por una mutación que sí muerda o aceptar el nueve de
  diez. Eso el ejecutor **no lo decidió por su cuenta**, porque el §6 y el
  criterio **7.2** son decisiones cerradas y el plan manda detenerse y preguntar.
- **Estado:** **abierta**. Bloquea, tal como está escrito, el criterio **7.2**
  del plan («las diez en rojo»): lo medido es **nueve en rojo y una imposible**.

---

## F-253 · `tests/__init__.py` apaga el registro, y con eso `assertLogs` y `assertNoLogs` no ven nada

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · ejecutor, al escribir los primeros goldens de registro
  del repositorio
- **Dónde:** `tests/__init__.py` (`logging.disable(logging.CRITICAL)`) y
  `tests/test_escpos.py` (el ayudante `registro_activo`).
- **Qué pasa:** el paquete de pruebas apaga el registro entero al importarse,
  para que las pruebas que provocan errores a propósito no ensucien la salida.
  Con eso puesto, `assertLogs` **falla siempre** (no ve ningún registro) y
  `assertNoLogs` **pasa siempre** (tampoco ve ninguno): los dos darían su
  veredicto **por el motivo equivocado**. La trampa 12 del plan de la Fase 4a
  avisaba de que estos eran los primeros `assertLogs` del repositorio, pero no
  de esto. Medido el 2026-09-15: con el golden de «poco papel» recién escrito,
  `assertLogs` falló con `no logs of level WARNING or higher triggered on
  ruleta.escpos` **aunque el aviso sí se emitía**.
- **Cómo se resolvió en esta fase:** un `contextmanager` local,
  `registro_activo()`, que hace `logging.disable(logging.NOTSET)` mientras dura
  el bloque y vuelve a dejarlo como estaba en el `finally`. **No se tocó
  `tests/__init__.py`**: está fuera del conjunto de archivos permitido de la
  fase, y apagar el registro en el resto de la suite es deliberado.
- **Por qué es residual:** ya está resuelto donde hacía falta. Queda escrito
  porque **cualquier golden de registro futuro** (en `test_app.py`, en
  `test_instalacion.py`) va a tropezar con lo mismo, y porque el ayudante vive
  hoy en un solo archivo de pruebas.
- **Propuesta:** cuando haga falta el segundo, mover `registro_activo()` a un
  sitio compartido de `tests/`. Mientras tanto, no tocar nada.
- **Estado:** **cerrada como hallazgo, viva como aviso** (2026-09-15).

---

## F-254 · Por Bluetooth, un fallo al ESCRIBIR el `DLE EOT` ya no se traga: sube como `OSError`

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · ejecutor, al reescribir `ImpresoraBluetooth._leer_estado`
- **Dónde:** `ruleta/escpos.py`, `ImpresoraBluetooth._leer_estado` y
  `leer_estado_fresco`.
- **Qué pasa:** antes, todo el cuerpo de `_leer_estado` estaba dentro de un
  `except (socket.timeout, TimeoutError): return None`, así que un
  **`sendall` que expirara** se contaba como «la impresora no contesta» y el
  boleto se imprimía igual. Ahora el `try` solo envuelve la **lectura**: el
  plan de la Fase 4a (§5, Paso 1, punto 5) manda que un fallo de **escritura**
  del comando **siga subiendo**, para que lo conviertan en `ErrorConexion` los
  sitios que ya lo hacen. Por USB eso no cambia nada (ya era así). Por
  Bluetooth, el `OSError` lo recoge el `except OSError` que ya existe en
  `imprimir`, que reintenta el trabajo y, si se acaban los intentos, lanza
  `ErrorConexion` **sin haber mandado ni un byte del boleto** (el premio se
  revierte, que es la política correcta).
- **Por qué es residual:** el cambio es el que pide el plan y es el seguro (si
  no se puede ni escribir el comando, el enlace está roto). **No está medido en
  hardware**: el transporte Bluetooth está escrito pero nunca se ha ejercido con
  la impresora real, y el `SocketFalso` de las pruebas no simula un `sendall`
  que expire.
- **Propuesta:** si algún día el Bluetooth deja de ser respaldo y se usa de
  verdad, añadir un golden con un `SocketFalso` que expire al enviar y decidir
  ahí si se prefiere reintentar o imprimir igual.
- **Estado:** **abierta como aviso** (2026-09-15). No bloquea: hoy la impresora
  va por cable USB.

---

## F-255 · Por USB, el rechazo del nodo al escribir el `DLE EOT` (write devuelve 0) no tiene golden

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · ejecutor, al comprobar la propiedad del §5, Paso 1,
  punto 5 del plan («si la escritura del comando falla, el `OSError` sube»)
- **Dónde:** `ruleta/escpos.py`, el cierre `escribir` de
  `ImpresoraArchivo._leer_estado`:
  `raise OSError(errno.EIO, f"{self.ruta} no aceptó la consulta de estado")`.
- **Qué pasa:** esa rama salta cuando `f.write()` devuelve **0** (el nodo no
  acepta ni un byte de la consulta) y es la que convierte un enlace roto en
  `ErrorConexion` —por `consultar_papel`, que la envuelve, o por `imprimir` con
  `enviados == 0`—. La Fase 4a la **conservó tal cual** y la usa, pero **ninguna
  prueba la ejercita**: medido el 2026-09-15, el texto «no aceptó la consulta de
  estado» solo aparece en `ruleta/escpos.py`, en ninguna de las 214 pruebas. Los
  goldens que tocan escrituras a medias son otros: `acepta=4` y `limite=10`
  (`test_fallo_a_mitad_no_cuenta_la_consulta`), que ejercitan el `OSError` del
  **límite**, no el del `write` que devuelve 0.
- **Por qué es residual:** no es un defecto: el comportamiento es el correcto y
  es el de antes de esta fase. Lo que falta es la **red** que lo sujete, y una
  mutación que borrara ese `raise` sobreviviría hoy en verde.
- **Riesgo si no se toca:** bajo. Un `write` que devuelve 0 sin excepción es
  raro en `usblp`; si alguien «simplifica» esa rama, nadie se entera hasta que
  el kiosco imprima con el nodo rechazando la consulta.
- **Propuesta:** un golden con el doble de siempre (`DispositivoFalso` con
  `acepta=0`) que compruebe que `consultar_papel` lanza `ErrorConexion` y que
  `imprimir` no manda ni un byte del boleto. Cuesta poco; no se hizo aquí
  porque está fuera de lo que manda el plan de esta fase y el árbol ya estaba
  cerrado cuando se vio.
- **Estado:** **abierta** (2026-09-15). No bloquea la Fase 4a.

---

## F-256 · Sin LED, el rechazo por falta de papel es INVISIBLE para el personal: el usuario no vio ninguna diferencia

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · prueba en vivo sin papel de las 21:32, observación del
  usuario
- **Dónde:** el kiosco entero. `config.json` sigue diciendo `"led": 22` y **no
  hay ningún LED conectado** (**F-240**); el LED de error lo enciende
  `_terminar_accion` en `ruleta/app.py`, y es **el único aviso perceptible** que
  el programa tiene previsto para una jugada rechazada.
- **Qué pasa:** desde `2a0aba3e01dcd15878579f1d02a64457b1834046` el kiosco **sí**
  se niega a jugar sin papel, y está medido: boletos **00013** y **00014**
  revertidos, premio devuelto, nada retenido en la impresora (**F-250**,
  resuelta). Pero **hacia fuera no se nota nada**. El usuario, que estaba
  delante de las dos jugadas rechazadas, lo dijo tal cual: **«no vi ninguna
  diferencia realmente»**. No sale boleto, no se enciende nada, no suena nada; la
  impresora enciende su foco rojo, que es lo mismo que hacía antes del arreglo.
  Desde la mesa, una jugada rechazada se parece a una jugada en la que el botón
  no hizo contacto.
- **Por qué es residual:** **no es un defecto de conducta**: el programa hace
  exactamente lo que el plan de la Fase 4a le pidió, y los cinco criterios del
  Paso 11 se cumplieron medidos. Lo que falta es una **pieza de hardware o una
  decisión de producto**, y las tres opciones cuestan dinero o requieren medir
  algo que nadie ha medido. No entra en el alcance de esta fase.
- **Riesgo si no se toca:** durante la semana del evento, cuando se acabe el
  rollo el kiosco **dejará de dar boletos en silencio**. Ya no se regalan
  premios —eso está arreglado—, pero **nadie se entera de por qué dejó de
  funcionar**: el mesero pensará que el botón falla, seguirá habilitando, y la
  fila seguirá jugando sin recibir nada hasta que alguien mire el rollo.
- **Propuesta (tres opciones; la decisión es del usuario):**
  1. **LED real en GPIO 22.** Es lo que el programa ya espera y lo que el
     `README.md` §2 describe: LED normal con resistencia de 330 Ω al pin 15, o el
     LED del propio botón arcade a través de un transistor. **Cero código.** El
     parpadeo rápido de error dura unos segundos, así que hay que mirarlo cuando
     pasa.
  2. **Zumbador propio en un GPIO** (la idea de **F-194**). Se oye aunque nadie
     esté mirando, que es la ventaja sobre el LED. Requiere pieza, cable y
     **código nuevo**: hoy no existe ninguna salida de audio en el programa.
  3. **Un pitido `ESC B` a la impresora antes de abortar**, aprovechando el
     zumbador que la impresora ya trae y que está confirmado en hardware (un
     pitido corto por comando, 2026-09-11). **Cuesta casi nada de código**, pero
     **NO ESTÁ MEDIDO** que el zumbador de la impresora funcione **con el rollo
     agotado y el foco rojo encendido**: hay que probarlo antes de prometerlo. Y
     hay que decidir si un pitido más, encima del que ya da por cada boleto,
     confunde en vez de avisar.
- **Estado:** **abierta.** **Requiere decisión del usuario.** No bloquea nada
  técnico: el kiosco es correcto sin esto. Relacionadas: **F-240** (qué se hace
  con `"led": 22` sin LED), **F-194** (el zumbador en GPIO) y **F-250** (el
  arreglo que esta ficha hace perceptible).

---

## F-257 · El alias `ruleta` de SSH intenta IPv6 y cuelga la sesión 30 s cuando la Pi está en el punto de acceso

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · noche del deploy y de la prueba en vivo
- **Dónde:** la configuración de SSH de la PC (el alias `ruleta` de
  `~/.ssh/config`), con la Pi en el punto de acceso móvil de Windows.
- **Qué pasa:** esa noche el alias `ruleta` **intentó IPv6 y dejó la sesión
  colgada unos 30 segundos** antes de rendirse. Lo que sí funcionó, medido, fue
  forzar IPv4 con la llave y la IP explícitas:
  `ssh -4 -i ~/.ssh/id_ruleta asadero@192.168.137.22`.
- **Por qué es residual:** no rompe nada del producto; es una trampa del entorno
  de trabajo. Pero **se paga en minutos cada vez**, y un agente sin contexto que
  vea la sesión colgada va a diagnosticar «la Pi está caída» cuando la Pi está
  perfectamente.
- **Riesgo si no se toca:** cada sesión futura sobre el punto de acceso vuelve a
  perder medio minuto por comando, o peor: alguien concluye que hay que reiniciar
  la Pi.
- **Propuesta:** añadir `AddressFamily inet` (y, si hace falta, `HostName` con la
  IP del punto de acceso) al bloque `Host ruleta` de `~/.ssh/config`; o, mientras
  tanto, que los briefs de agente escriban el respaldo con `-4`, `-i` y la IP,
  como ya hace la convención de comandos de los planes. **Ojo:** la IP del punto
  de acceso **cambia** —el 2026-09-13 fue `192.168.137.123` y el 2026-09-15,
  `192.168.137.22`—, así que fijarla en el `config` obliga a revisarla.
- **Estado:** abierta (configuración de la PC del usuario). Familia: **F-244** y
  **F-245**, las otras dos trampas de SSH que ya costaron tiempo medido.

---

## F-258 · La nota de pausa `docs/PAUSA-2026-09-15.md` quedó commiteada dentro del commit de CÓDIGO

- **Fecha:** 2026-09-15
- **Origen:** Fase 4a · escriba, comparando el diff real de
  `2a0aba3e01dcd15878579f1d02a64457b1834046` contra la lista del Paso 9 del plan
- **Dónde:** `docs/PAUSA-2026-09-15.md`, y el conjunto de archivos del Paso 9 de
  `docs/planes/fase-4a-papel.md`.
- **Qué pasa:** el Paso 9 fija por adelantado **doce** rutas permitidas y la nota
  de pausa **no está entre ellas**. El commit `2a0aba3` llevó **once** archivos, y
  uno de ellos fue `docs/PAUSA-2026-09-15.md`. La decisión fue del orquestador:
  la nota se había escrito durante la pausa de las 15:25 y quedarse sin
  commitearla habría dejado el árbol sucio, que es lo que la compuerta del §4 del
  protocolo prohíbe («nada pendiente de push antes de commitear»). Se metió para
  no bloquear el gate.
- **Por qué es residual:** no es un defecto de conducta ni de código: **el
  contenido del commit es correcto y está verificado contra el remoto**. Lo que
  falla es la correspondencia entre el conjunto declarado y el conjunto real, que
  es justo lo que la compuerta existe para comprobar «por igualdad».
- **Riesgo si no se toca:** un verificador futuro que compare el commit contra la
  lista del plan encuentra una diferencia y no sabe si fue una decisión o un
  descuido. Por eso queda escrito aquí y en el acta (§9.4).
- **Propuesta:** para la próxima pausa, o bien la nota entra en la lista de
  archivos permitidos **antes** de commitear, o bien se escribe fuera del
  repositorio, en el scratchpad de la sesión, como el resto de los archivos
  efímeros.
- **Estado:** **cerrada el 2026-09-15.** La pausa **se retomó** (~19:50, sin
  rehacer nada) y **se cerró** con el acta `docs/actas/2026-09-15-fase-4a.md`;
  el propio `docs/PAUSA-2026-09-15.md` lo dice en negrita justo debajo de su
  título. Lo que queda es la lección para la próxima, no una acción pendiente.

---

## F-259 · Los siete premios se cargaron SIN `desde`/`hasta`: hay que ponerlos antes del lunes 21

- **Fecha:** 2026-09-15
- **Origen:** Fase 4b · decisión **D1** del plan
  `docs/planes/fase-4b-config-oficial.md`
- **Dónde:** `config.json`, lista `premios` (los siete objetos, ninguno con
  `desde` ni `hasta`), contra el bloque `"premios"` del §5.1 de
  `docs/evento-2026-09-asadero-33.md`, que **sí** las trae.
- **Qué pasa:** el bloque del documento fija `"desde": "2026-09-21"` y
  `"hasta": "2026-09-25"` para seis premios, y `2026-09-24` / `2026-09-25` para
  la `hielera`. **Esta fase las omitió a propósito.** La razón es de calendario:
  el usuario iba a probar el kiosco el **2026-09-16** y el evento abre el **21**.
  Con el `desde` puesto, **ningún premio estaría disponible** el día 16: el
  filtro de fechas los sacaría a todos de la tómbola y **el usuario solo habría
  visto boletos de consuelo** en todas sus pruebas —exactamente lo contrario de
  lo que pidió, que era ver en papel los nombres y los detalles reales para
  corregirlos—.
- **Por qué es residual:** no es un defecto ni una afirmación falsa. Es una
  decisión cerrada, escrita en el plan (**D1**), anclada por un golden
  (`tests/test_config.py`,
  `TestPremiosOficialesDelEvento.test_los_premios_del_config_todavia_no_traen_fechas`)
  y con fecha límite conocida. El programa se comporta correctamente sin fechas:
  un premio sin `desde`/`hasta` está disponible todos los días.
- **Riesgo si no se toca:** **alto, y con fecha.** Sin `desde`, **la hielera
  puede salir el lunes 21**, cuando el dictado del usuario dice que es del
  **jueves 24 y el viernes 25**. Son dos piezas, las más caras del evento, y una
  vez impreso el boleto el premio está comprometido.
- **Propuesta:** en la **pasada final antes del lunes 21**, copiar `desde` y
  `hasta` del §5.1 del documento a los siete premios de `config.json`. El golden
  está escrito para **caerse** en ese momento y lo dice en su propio docstring:
  se **borra** ese test y se añaden `"desde"` y `"hasta"` a
  `CLAVES_DEL_DOCUMENTO`, con lo que la comparación por igualdad pasa a cubrir
  también las fechas. **No se relaja la comparación.**
- **Estado:** **resuelta** el **2026-09-16** (Fase 4e; plan
  `docs/planes/fase-4e-final.md`, decisión **D1**), **cuatro días antes de la
  fecha límite**. Se copiaron del §5.1 del documento a `config.json` las siete
  parejas de fechas: **hielera 2026-09-24 → 2026-09-25** y **silla, bbq, tacos3,
  tacos2, cerveza y agua 2026-09-21 → 2026-09-25**. El golden que anclaba la
  ausencia (`test_los_premios_del_config_todavia_no_traen_fechas`) **se cayó**,
  como estaba escrito que pasara, y se sustituyó por
  `test_los_premios_del_config_traen_las_fechas_del_evento`, que ancla **el censo
  real por igualdad**; además `desde` y `hasta` entraron en
  `CLAVES_DEL_DOCUMENTO`, así que la comparación campo por campo contra el §5.1
  las cubre (mutaciones **M8** y **M9** del plan, las dos en rojo). **No se
  relajó ninguna comparación.** El calendario se ancla también con el motor de
  producción en
  `tests/test_instalacion.py::test_las_fechas_del_evento_deciden_que_dias_hay_premios`:
  el **19** no hay ningún premio, el **21** los seis sin hielera, el **24** y el
  **25** los siete, el **26** ninguno. **Consecuencia aceptada y escrita** en el
  §5.1 del documento y en el §5 del `README.md`: **hasta el lunes 21 toda jugada
  sale de consuelo**, y eso no es una avería. Relacionadas: **F-241** (cerrada en
  hardware el mismo día) y **F-262**, que gracias a esto **deja de ser
  obligatoria**.

---

## F-260 · Los siete nombres y detalles cargados llevan asterisco en el documento: son propuesta, no confirmación

- **Fecha:** 2026-09-15
- **Origen:** Fase 4b · decisión **D1** del plan; tabla del §1 y pregunta **6**
  del §4 de `docs/evento-2026-09-asadero-33.md`
- **Dónde:** `config.json`, llaves `nombre` y `detalle` de los siete premios.
- **Qué pasa:** en la tabla del §1 del documento del evento, **los siete nombres
  y los siete detalles llevan `*`**, y el propio documento explica qué significa
  esa marca: «es **una propuesta mía** y está **a confirmar**». La pregunta 6 del
  §4 sigue **sin marcar**. Es decir: `HIELERA IGLOO`, `SILLA DE PLAYA`,
  `SET BBQ`, `3 TACOS DE PASTOR`, `2 TACOS DE PASTOR`, `CERVEZA`, `AGUA FRESCA`
  y sus siete textos chicos **se cargaron tal cual**, sin que el usuario los haya
  confirmado. Lo que **no** lleva asterisco —los stocks, los cupos y los ids— es
  dictado del usuario del 2026-09-13 y se cargó igual de literal.
- **Por qué es residual:** cargarlos era justo lo que el usuario pidió («cambiar
  la Pi al programa oficial que usaremos; haré pruebas en ese mañana para hacer
  algunos cambios»): los prueba en papel y decide. No es una invención del
  ejecutor: está escrito, revisado y commiteado desde el 2026-09-13.
- **Riesgo si no se toca:** que la semana del evento se imprima un nombre que el
  dueño no eligió. El `id` **no** puede cambiarse a media semana (lleva los
  contadores, `README.md` §6), pero el `nombre` y el `detalle` sí: son solo
  texto del boleto.
- **Propuesta:** que el usuario, tras ver los boletos del **2026-09-16**, corrija
  **la tabla del §1 del documento** (no `config.json`: lo dice el §6, paso 1) y
  avise. La regla para que quepan está medida y escrita en el §1: **ninguna
  palabra de más de 12 letras** y como mucho 3 renglones de 12. Después basta
  volver a derivar `config.json` del documento. **Ojo con qué mira el golden:**
  `test_config_json_lleva_exactamente_los_premios_del_documento` compara
  `config.json` contra el **bloque JSON del §5.1**, no contra la tabla del §1.
  Medido el 2026-09-15 sobre una copia: cambiando **solo** la tabla del §1
  (`CERVEZA` → `CHELA`) la suite sigue en **verde** (216 OK). Así que hay que
  corregir **las dos cosas** —la tabla del §1 y el bloque del §5.1— y después
  `config.json`: solo entonces el golden vigila el cambio y se pone en rojo
  mientras los dos no coincidan.
- **Estado:** **resuelta** el **2026-09-16** (Fase 4d). El usuario confirmó los
  siete nombres y los siete detalles, con dos cambios suyos: **CERVEZA** →
  «Tecate Light, Tecate Roja o Indio» y **AGUA FRESCA** → «Horchata, Jamaica o
  Cebada». Se quitaron **todos los asteriscos** de la tabla del §1 y se anotó la
  confirmación con fecha; los dos detalles nuevos se copiaron al bloque del §5.1
  y de ahí a `config.json`, que es el orden que esta misma ficha pedía. Del §4
  siguen abiertas **solo la pregunta 7** (factor de holgura, que con el reparto
  por horas casi no aplica); las preguntas **1**, **2**, **3**, **4** y **5**
  quedaron respondidas ese mismo día. **El aviso de esta ficha sigue vivo como
  regla:** el golden compara `config.json` contra el **bloque del §5.1**, no
  contra la tabla del §1, así que un nombre corregido solo en el §1 deja la suite
  en verde.
- **Nota fechada (2026-09-16, cierre documental).** **Confirmado contra el diff
  real de `613f875`, no contra el informe del ejecutor:** en `config.json` el
  `detalle` de `cerveza` pasó de «Una cerveza» a **«Tecate Light, Tecate Roja o
  Indio»** y el de `agua`, de «Vaso de 1/2 litro» a **«Horchata, Jamaica o
  Cebada»**; los otros cinco nombres y detalles quedaron **idénticos** a los que
  la Fase 4b había cargado. Los siete siguen anclados **campo por campo y en
  orden** contra el bloque del §5.1 por
  `test_config_json_lleva_exactamente_los_premios_del_documento`. **Lo que esta
  ficha deja vivo como regla permanente** —el golden **no** vigila la tabla del
  §1— no caduca con el cierre. Evidencia: `docs/actas/2026-09-16-fase-4bcd.md`
  §5.1.

---

## F-261 · Pieza A: mientras el consuelo no tenga peso propio, las primeras 33 jugadas del día ganan premio seguro

- **Fecha:** 2026-09-15
- **Origen:** Fase 4b · trampa 4 del plan, al cargar los premios reales
- **Dónde:** `ruleta/inventario.py` (cabecera del módulo: «Si no hay ninguno
  disponible, el sorteo devuelve None (boleto de consuelo)») y el §5.2,
  **PENDIENTE A**, de `docs/evento-2026-09-asadero-33.md`.
- **Qué pasa:** el motor **no tiene** un peso para el boleto de consuelo. El
  consuelo sale **solo** cuando **ningún** premio está disponible. Con los
  premios que esta fase acaba de cargar —`peso = cupo`, 34 de cupo diario
  sumado y **sin `desde`/`hasta`** (D1)— eso significa que **las primeras 34
  jugadas del día entregan premio, una tras otra** los dos primeros días en que
  se juegue (la hielera entra todos los días mientras le queden sus dos piezas) y
  **33** de ahí en adelante, y después todo es consuelo. Medido el 2026-09-15
  corriendo el sorteo real con este mismo `config.json`: 34, 34, 33, 33, 33, y
  las 167 piezas se agotan en cinco días de juego. Cuando se carguen las fechas
  (**F-259**) vuelve a ser 33 al día y 34 el jueves 24 y el viernes 25, que es lo
  que dice el documento. Está medido el 2026-09-13 corriendo el sorteo
  real con estos mismos premios, y el documento lo marca como **«lo más
  importante de este documento»**: «**no se debe abrir el evento sin la pieza
  A**».
- **Por qué es residual:** **no es un defecto nuevo ni un defecto de esta fase.**
  El motor se comporta exactamente como está documentado desde el 2026-09-13, y
  construir la pieza A es **programar**, que es justo lo que el §6 del plan de la
  Fase 4b prohíbe hacer aquí. Se anota porque **cargar los premios reales es lo
  que vuelve visible la consecuencia**: en las pruebas del 2026-09-16 el usuario
  va a ver que **gana todo el mundo**, y eso es lo esperado, no una avería.
- **Riesgo si no se toca:** si se abre el evento así, el lunes 21 se regalan
  **los 33 premios del día en las primeras 33 jugadas**, probablemente en la
  primera media hora, y las once horas restantes son puro consuelo. Se acaba el
  inventario del día antes de la cena.
- **Propuesta:** construir la **pieza A** en una fase de programación propia,
  con la forma que el §5.2 ya propone: `"peso"` dentro de `juego.consuelo`, con
  valor **N − 33** (N = jugadas esperadas por día; la propuesta por omisión del
  documento es **N = 250**, o sea **217**). **Requiere antes la decisión del
  usuario sobre N** (pregunta 1 del §4).
- **Estado:** **RESUELTA el 2026-09-16** (Fase 4c, plan
  `docs/planes/fase-4c-consuelo-peso.md`). **Ya no bloquea la apertura del
  evento.** Lo que disparó la fase fue el propio usuario probando en vivo ese
  día: «no ha salido ningún boleto de gracias por participar, solo premios» —
  exactamente lo que esta ficha anunciaba—. Se construyó la **pieza A** con la
  forma que el §5.2 del documento proponía, **sin cambiarla**: llave nueva
  `juego.consuelo.peso` (entero ≥ 0, **por omisión 0** = el comportamiento
  viejo), cargada en `config.json` con **217**. `Inventario.sortear` hace ahora
  **UNA sola** elección ponderada entre los premios disponibles **y** el
  consuelo; el consuelo **no** descuenta stock ni tope, pero **sí** gasta folio,
  como siempre. Medido el 2026-09-16 con el `config.json` real: la tómbola tiene
  **251** papelitos (34 de premio + 217) y **gana el 13.55 % de las jugadas**, 1
  de cada 7 u 8, en vez del 100 % de las primeras 34. La afirmación de la
  cabecera de `ruleta/inventario.py` que esta ficha citaba —«Si no hay ninguno
  disponible, el sorteo devuelve None (boleto de consuelo)»— quedó **reescrita**.
  **Sigue siendo cierta con `"peso": 0`**, que es lo que pasa en cualquier
  instalación que no cargue la llave nueva. Lo que queda abierto es **el número**,
  no el mecanismo: ver **F-263**. Hermanas todavía abiertas: **piezas B**
  (franjas), **C** (horario) y **D** (**F-241**, esperar a que la hora esté
  sincronizada).
- **Nota fechada (2026-09-16, cierre documental de las Fases 4b, 4c y 4d).**
  **El mecanismo que cerró esta ficha se construyó en `d01a0ca` y quedó SUPERADO
  el mismo día por `613f875`.** El peso del consuelo dejó de ser el único freno:
  desde la Fase 4d **el cupo diario ya no está disponible entero desde el primer
  minuto**, sino que se abre por horas, así que lo que esta ficha temía —«las
  primeras 34 jugadas del día entregan premio, una tras otra»— **ya no puede
  pasar aunque el peso fuera 0**: a las 12:30 solo hay **una** pieza abierta. Por
  eso `juego.consuelo.peso` **bajó de 217 a 10** en el mismo commit: con el
  reparto por horas el consuelo compite contra **una o dos piezas abiertas**, no
  contra los 34 papelitos del día. Las **tres piezas hermanas que esta ficha
  dejaba abiertas** —**B** (franjas), **C** (horario) y **D** (la hora,
  **F-241**)— quedaron **construidas** en `613f875`. Medido por el programa: con
  el modelo de esta ficha, y **acertando N**, se entregaba el **84 %** del cupo;
  con el reparto por horas se entrega **34 de 34** con 1 980, 660 o 220 jugadas
  al día, y **31.7 de 34** con solo 66. Evidencia:
  `docs/actas/2026-09-16-fase-4bcd.md` §5.

---

## F-262 · El inventario de pruebas se reinicia en esta fase, y hay que volver a reiniciarlo el lunes si el 16 se juega

- **Fecha:** 2026-09-15
- **Origen:** Fase 4b · decisión **D6** del plan (paso 5 del deploy)
- **Dónde:** en la Pi, `/home/asadero/ruleta/datos/estado.json` y
  `/home/asadero/ruleta/datos/boletos.csv`; el comando es
  `python3 -m ruleta reiniciar --si` (`ruleta/__main__.py`, `cmd_reiniciar`).
- **Qué pasa:** las pruebas de la Fase 4a (papel agotado) dejaron el inventario
  real en **folio 16**, con premios `TEST 1`…`TEST 7` descontados. El deploy de
  esta fase lo pone en cero **una vez**, para que el boleto de inventario de
  arranque salga con los siete premios reales y **folio 00000**. Pero el usuario
  va a **jugar el 2026-09-16** para revisar nombres y detalles: **cada boleto de
  esas pruebas descuenta stock real y gasta folio**. Si nadie lo reinicia otra
  vez, el lunes 21 el evento abre con piezas ya «entregadas» que están en la
  bodega.
- **Por qué es residual:** no es un defecto: el programa cuenta bien: cuenta
  **todo**, que es lo que debe hacer. Es un paso de operación con fecha, igual
  que el que ya está escrito en el §6, paso 5 del documento del evento.
- **Riesgo si no se toca:** el inventario del lunes arranca corto, los cupos
  diarios se agotan antes de tiempo y el reporte impreso no cuadra con la tabla
  del §1 —lo que, según el propio §6 paso 6 del documento, significa que **no se
  abre el evento**—.
- **Propuesta:** el **lunes 21, antes de abrir**, con el servicio detenido:
  `sudo systemctl stop ruleta`, `python3 -m ruleta reiniciar --si` (respalda
  `estado.json` y `boletos.csv` con marca de tiempo; **no toca `ruleta.log`**),
  `sudo systemctl start ruleta`, y comprobar con `python3 -m ruleta reporte` que
  los stocks y los cupos son **exactamente** los de la tabla del §1. Conviene
  hacerlo en la **misma pasada** que carga las fechas de la **F-259**.
- **Estado:** **abierta.** Fecha límite: **lunes 21 de septiembre de 2026, antes
  de abrir.** Es la continuación de **F-243** (que anotó el mismo pendiente
  cuando el folio iba en 3, y luego en 16); **F-243 sigue abierta** por la misma
  razón.
- **Nota fechada (2026-09-16, cierre documental de las Fases 4b, 4c y 4d).**
  **Lo que esta ficha anunciaba pasó, y sigue abierta.** El inventario se
  reinició **dos** veces el 2026-09-16 y **las dos veces el usuario volvió a
  jugar después**: a las **00:10** (deploy de la Fase 4b, de folio 16 a
  00000, respaldos `datos/estado_20260916_001053.json` y
  `datos/boletos_20260916_001053.csv`) y a las **12:46** (ya con la Fase 4d
  desplegada, de folio 6 a 00000, respaldos
  `datos/estado_20260916_124629.json` y `datos/boletos_20260916_124629.csv`).
  Entre el primero y el segundo el usuario jugó y se llevó **agua 3, bbq 1 y
  cerveza 1**, todos **premios reales**; después del segundo volvió a jugar
  («salieron consuelos y una cerveza»). **Nadie ha contado cuántos boletos
  salieron después de las 12:46:48**, así que el estado exacto del inventario
  al cerrar la sesión **no está medido**. Por eso la fecha límite no se
  mueve: **lunes 21 de septiembre, antes de abrir**, con el servicio parado, y
  en la **misma pasada** que carga las fechas de la **F-259**. Evidencia:
  `docs/actas/2026-09-16-fase-4bcd.md` §3.4, §5.6, §6 y §10.
- **Nota fechada (2026-09-16, Fase 4e). Deja de ser obligatoria, y sigue siendo
  decisión del usuario.** Dos cosas cambiaron. (1) **El inventario se reinicia en
  el deploy de esta fase** (paso 4 del §8 del plan `docs/planes/fase-4e-final.md`:
  servicio parado, `python3 -m ruleta reiniciar --si`, arranque y comprobación),
  y esta vez **el usuario ya terminó de probar**: no va a haber jugadas detrás.
  (2) **Con las fechas de la F-259 cargadas, ningún premio puede salir antes del
  lunes 21**: cualquier boleto de estos días es de **consuelo**, y el consuelo
  **no descuenta stock ni cupo**. Es decir: aunque alguien jugara el 17, el 18 o
  el 20, **el inventario de premios del lunes no se movería**. Lo único que sí
  avanzaría es el **folio**. **Qué queda para el lunes 21, entonces:** reiniciar
  **solo si el usuario quiere abrir con el folio en 00000**; ya no hace falta
  «para que las pruebas no cuenten como premios entregados», que era el motivo
  original de esta ficha. Lo que **no** cambia: si se reinicia, se hace con el
  servicio parado y se comprueba con `python3 -m ruleta reporte` que los stocks y
  los cupos son los de la tabla del §1 (§6, paso 6 del documento del evento).

---

## F-263 · La pieza A se construyó con N = 250 por omisión: el número sigue esperando la respuesta del usuario

- **Fecha:** 2026-09-16
- **Origen:** Fase 4c · decisión **D1** del plan
  `docs/planes/fase-4c-consuelo-peso.md`
- **Dónde:** `config.json`, `juego.consuelo.peso` = **217**; el §5.2 (PENDIENTE
  A) y la **pregunta 1 del §4** de `docs/evento-2026-09-asadero-33.md`.
- **Qué pasa:** el peso del consuelo es **N − 33**, donde **N** son las jugadas
  que se esperan en un día. La pregunta 1 del §4 —«¿Cuántas jugadas esperas por
  día?»— **sigue sin marcar**. Se cargó **217**, que es **N = 250**, la
  **propuesta por omisión** que el propio documento escribe en tres sitios (§2
  «Mi propuesta por omisión: N = 250», la tabla de escenarios y el §5.2). Es
  decir: el mecanismo está decidido y probado; **el número no lo ha dicho el
  dueño.**
- **Por qué es residual:** no es un defecto ni una invención. El documento dice
  con todas sus letras que «si no respondes una, se aplica la propuesta por
  omisión», y 217 es esa propuesta, literal, sin redondear ni ajustar. Además el
  documento explica por qué equivocarse no rompe nada: si vienen más jugadas que
  N los premios llegan a su cupo más temprano, y si vienen menos, quedan piezas
  en la bodega. **El cupo manda en los dos casos.**
- **Riesgo si no se toca:** que la proporción de ganadores no sea la que el dueño
  quiere. Medido el 2026-09-16 con el `config.json` real: con 217 gana el
  **13.55 %** de las jugadas (1 de cada 7 u 8). Si el asadero hace **150**
  jugadas al día y no 250, con 217 los premios **no se acaban**: saldrían unos 20
  de los 33 del día. Si hace **400**, se acaban antes de la cena.
- **Propuesta:** preguntarle a sdurazo **cuántas veces se va a apretar el botón
  en un día** y cambiar **un solo número**, en el §5.2 del documento **y** en
  `config.json` (150 → 117 · 200 → 167 · 250 → 217 · 300 → 267 · 400 → 367). Los
  pesos de los premios **no se tocan nunca**: son los cupos que él fijó. Un
  golden compara los dos archivos por igualdad, así que cambiar uno solo deja la
  suite en rojo (`tests/test_config.py`,
  `test_config_json_lleva_el_peso_de_consuelo_del_documento`), y otro comprueba
  que el peso del §5.2 obedezca la regla **N − 33** del §2 y sea una de las N que
  ese §2 tabula (cambiar N NO obliga a tocar la tabla de escenarios del §2). **Ya
  arrancado el evento el número se puede medir**, no adivinar: el renglón
  `Boletos emitidos hoy` del reporte impreso dice cuántas jugadas hubo.
- **Estado:** **cerrada por derogación** el **2026-09-16** (Fase 4d). **La
  pregunta ya no existe:** el usuario contestó que **es imposible saber cuántas
  jugadas habrá**, y de ahí salió el reparto por horas, que **no usa N**. El peso
  del consuelo dejó de ser «N − 33» y pasó a **10**, un número que ya no depende
  de la asistencia sino de contra cuántas piezas abiertas compite. Todo lo que
  esta ficha decía sobre el riesgo de errar N —«si hace 400 jugadas, los premios
  se acaban antes de la cena»— **dejó de aplicar**: medido el 2026-09-16
  simulando un día entero, con 1 980, 660 o 220 jugadas se entregan **las 34
  piezas**. Lo que **sí** hereda esta ficha es que **el 10 lo propuse yo**, no el
  usuario: ver **F-270**. El golden de la regla N − 33 se sustituyó por
  `test_las_probabilidades_del_2_las_calcula_el_programa`, y la regla vieja
  sobrevive, vigilada, en la nota histórica del §2
  (`test_la_nota_historica_del_2_sigue_obedeciendo_su_regla_N_menos_33`).

---

## F-264 · `juego.consuelo.peso` acepta cualquier entero: un cero de más y no gana casi nadie, sin un solo aviso

- **Fecha:** 2026-09-16
- **Origen:** Fase 4c · ejecutor, al escribir la validación de la decisión **D1**
- **Dónde:** `ruleta/config.py`, `validar()` (`grep -n "consuelo.peso" ruleta/config.py`).
- **Qué pasa:** la validación que se escribió rechaza el peso **negativo** y los
  tipos malos (texto entre comillas, decimal, `true`, `null`), con mensaje en
  español que nombra la llave. Lo que **no** hay es ningún tope por arriba ni
  ninguna comparación con los pesos de los premios. Con `"peso": 2170` en vez de
  `217` —un cero de más al teclear— la tómbola pasa de 251 papelitos a 2204 y la
  probabilidad de ganar cae del **13.55 %** al **1.5 %**: en un día de 250
  jugadas saldrían unos **cuatro** premios de los 33. El programa arranca
  contento y no dice nada.
- **Por qué es residual:** no es un defecto de conducta: el valor es legítimo
  —hay quien querría justo eso— y el dato **sí** está a la vista, porque el
  boleto de inventario de arranque imprime la línea del consuelo con su peso y su
  porcentaje. Además la validación cubre lo que el protocolo pide: tipo y rango,
  con mensaje en español.
- **Riesgo si no se toca:** medio. El error no se detecta al arrancar sino
  mirando el papel, y el único que mira ese papel es quien sepa qué número
  esperar. Con el kiosco ya abierto, la señal sería «casi nadie gana».
- **Propuesta:** dos ideas, ninguna urgente. (a) Que `validar()` avise —o falle—
  si el peso del consuelo pasa de, por ejemplo, **cien veces** la suma de los
  pesos de los premios; hay que decidir si es error o solo aviso en el log.
  (b) Que el boleto de inventario de arranque **destaque** la línea del consuelo
  cuando su probabilidad pase del 95 %. Mientras tanto, la defensa es de
  procedimiento y ya está escrita: **mirar el boleto de inventario de arranque**
  y comprobar que dice el porcentaje que se espera.
- **Estado:** **abierta.** Relacionada con **F-263** (el número lo decide el
  usuario) y con **F-221** (`juego.consuelo.texto` admite la cadena vacía sin
  queja: el mismo bloque de configuración, la misma clase de hueco).

---

## F-265 · La decisión D2 del brief decía que `app.py` construye el Inventario, y quien lo construye es `__main__.py`

- **Fecha:** 2026-09-16
- **Origen:** Fase 4c · contradicción entre el brief del orquestador (**D2**) y
  el código real, detectada por el ejecutor **antes** de escribir nada
- **Dónde:** `ruleta/__main__.py`, `abrir_inventario()`; `ruleta/app.py`,
  `Ruleta.__init__` (`grep -rn "Inventario(" ruleta`).
- **Qué pasa:** la decisión **D2** del brief decía «`app.py` pasa
  `cfg.juego.consuelo.peso` al construir el Inventario». **`ruleta/app.py` no
  construye ningún `Inventario`:** lo recibe ya hecho. El único sitio de
  producción que lo construye es `abrir_inventario()`, en `ruleta/__main__.py`,
  y de ahí salen **los seis** comandos que tocan el inventario (`jugar`,
  `vista-previa`, `reporte`, `liberar`, `reiniciar` y `diagnostico`, que solo
  lee folio y pendientes). El ejecutor **no
  improvisó una fábrica nueva en `app.py`**: cableó el parámetro donde el código
  ya lo hacía con `hora_inicio_dia`, y lo reportó.
- **Por qué es residual:** el efecto buscado por D2 se consiguió entero —los
  seis comandos reciben el peso— y la diferencia es de redacción del brief, no
  de conducta. Se anota para que un verificador futuro que compare el brief con
  el diff lo lea como una decisión y no como un descuido. `app.py` **sí** se tocó
  en esta fase, pero por otra cosa: su `log.warning("Sin premios disponibles…")`
  dejaba de ser cierto en cuanto el consuelo tiene peso, y se partió en dos ramas.
- **Riesgo si no se toca:** ninguno hoy. El riesgo real es futuro: que alguien
  añada una segunda fábrica de `Inventario` y se olvide de un parámetro. Contra
  eso se escribió un **censo derivado** que cuenta las construcciones en
  `ruleta/*.py` y exige que siga habiendo **exactamente una**
  (`tests/test_instalacion.py`,
  `test_solo_hay_un_sitio_de_produccion_que_construye_el_inventario`), más un
  golden que comprueba que `abrir_inventario` **deriva** el peso del `cfg` que
  recibe (mutación **M9**: quitando el parámetro, en rojo).
- **Propuesta:** que el orquestador confirme el cableado en `__main__.py` (o
  pida moverlo). Si algún día `app.py` necesitara construir el inventario, el
  censo derivado se pondrá en rojo y obligará a revisarlo, que es justo lo que se
  quiere.
- **Estado:** **abierta como confirmación del orquestador.** Técnicamente hecho
  y probado.

---

## F-266 · El §5.1 del documento del evento sigue diciendo que la Pi va sin red y que por eso hace falta la batería RTC

- **Fecha:** 2026-09-16
- **Origen:** Fase 4c · el ejecutor leyó entero el documento del evento para la
  pieza A y se topó con el párrafo
- **Dónde:** `docs/evento-2026-09-asadero-33.md`, §5.1, párrafo «**Sobre el
  reloj:**» (`grep -n "va sin red" docs/evento-2026-09-asadero-33.md`).
- **Qué pasa:** ese párrafo dice que «las franjas dependen de la hora de la Pi, y
  en producción la Pi **va sin red**. Por eso **la batería del reloj (RTC) tiene
  que estar puesta y la hora correcta antes del lunes 21**». **El usuario derogó
  esa premisa el 2026-09-15:** en el evento la Pi tendrá el internet del asadero,
  que es lo que le pone la hora al arrancar (NTP), y **no habrá batería RTC**.
  Está escrito así en `CLAUDE.md` y en la bitácora del §7 del propio documento,
  con su ficha (**F-242**), pero el §5.1 no se actualizó y **se contradice con su
  propio §7**.
- **Por qué es residual:** no es un defecto de código ni una afirmación sobre el
  programa: es una premisa de operación que cambió de dueño. Y estaba **fuera
  del alcance literal** de esta fase, que del §5.1 solo podía tocar la línea del
  campo nuevo (decisión **D5**). Corregirlo aquí habría sido meter mano de más en
  el documento que el usuario edita a mano.
- **Riesgo si no se toca:** que alguien lea el §5.1 antes que el §7 y salga a
  comprar una batería RTC, o peor, que dé por hecho que la hora está garantizada
  sin red. La consecuencia real —que en los primeros minutos tras encender, la Pi
  cree que es otro día, y del día dependen los topes diarios y las fechas
  `desde`/`hasta`— es la que persigue la **pieza D** (**F-241**).
- **Propuesta:** en la pasada que cargue las fechas `desde`/`hasta` (**F-259**),
  que ya va a tocar ese mismo §5.1, reescribir el párrafo del reloj con la
  decisión del 2026-09-15 y remitir a la **pieza D**. **Requiere visto bueno del
  usuario**, porque es su documento.
- **Estado:** **resuelta** el **2026-09-16** (Fase 4d). El párrafo «Sobre el
  reloj» del §5.1 se reescribió con la decisión del 2026-09-15 —la Pi llevará el
  internet del asadero y **no habrá batería RTC**— y ahora remite a la **pieza
  D**, que esa misma fase construyó: al arrancar, el kiosco espera hasta
  `juego.espera_hora_seg` (120 s) a que la hora esté sincronizada y, si no lo
  consigue, escribe en el boleto `HORA SIN CONFIRMAR: revisar fecha`. La nota
  fechada del párrafo viejo se conserva dentro del propio §5.1. Hermanas:
  **F-242** (la derogación) y **F-241** (la pieza D, ahora construida).

---

## F-267 · El reparto por horas cambia la conducta de `tope_diario` también donde NO hay `juego.horario`

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · decisión **D3** del plan `docs/planes/fase-4d-horas.md`
- **Dónde:** `ruleta/inventario.py`, `ventana_del_dia()` e `instantes_del_dia()`
  (`grep -n "ventana_del_dia" ruleta/inventario.py`).
- **Qué pasa:** hasta el 2026-09-16, un premio con `tope_diario` tenía su cupo
  **disponible entero desde el primer minuto del día operativo**. Desde esta
  fase el cupo **se abre poco a poco**, y eso vale **también cuando no hay bloque
  `juego.horario`**: en ese caso el tramo es el **día operativo completo**, de
  `hora_inicio_dia` a 24 horas después. Con el valor por omisión (6:00) y un
  premio de una pieza al día, esa pieza **no se puede ganar hasta las 18:00**.
  Medido y anclado por igualdad en `tests/test_inventario.py`,
  `test_stock_y_tope_diario`: a las 12:00 el motivo es `se libera a las 18:00`.
- **Por qué es residual:** es **exactamente** lo que la decisión D3 manda —«sin
  horario configurado, el reparto se hace sobre el día operativo completo»— y en
  el Asadero 33 no cambia nada, porque su `config.json` **sí** trae horario. No
  hay ninguna otra instalación de este programa.
- **Riesgo si no se toca:** que alguien copie este programa a otro negocio, no
  ponga `juego.horario`, y se extrañe de que su premio del día no salga por la
  mañana. Está escrito en el `README.md` §7, entre paréntesis y con la fecha,
  pero es el tipo de cambio que se lee después de sufrirlo.
- **Propuesta:** dejarlo como está y que lo confirme el orquestador. La
  alternativa —no repartir cuando no hay horario— también es defendible, pero
  contradice la decisión D3 y el ejecutor **no improvisó**: implementó lo escrito
  y lo anotó aquí. Si algún día se prefiere la otra, el cambio es de una línea en
  `instantes_del_dia()` y el golden que se pone en rojo es ese mismo.
- **Estado:** **abierta como confirmación del orquestador.** Técnicamente hecho,
  probado y documentado. **Cerrada el 2026-09-16 como confirmación del
  orquestador: ver la nota fechada al pie de esta ficha.**
- **Nota fechada (2026-09-16, cierre documental de las Fases 4b, 4c y 4d).**
  **CONFIRMADA: el orquestador ACEPTÓ la lectura del ejecutor.** El reparto se
  hace sobre el **día operativo completo** cuando no hay `juego.horario`, tal y
  como manda la decisión **D3** del plan; **no se cambia nada**. La razón de la
  aceptación es la que la propia ficha escribe: **en el Asadero 33 no cambia
  nada**, porque su `config.json` sí trae horario, y **no hay ninguna otra
  instalación de este programa**. Queda vivo el aviso para el día en que la
  haya, que ya está en el `README.md` §7 con su fecha. **Esta ficha se cierra
  como confirmación**; si algún día se prefiere la conducta contraria, el cambio
  es de una línea en `instantes_del_dia()` y el golden que se pone en rojo es
  `test_stock_y_tope_diario`. Evidencia:
  `docs/actas/2026-09-16-fase-4bcd.md` §7.

---

## F-268 · La separación mínima solo la marca un boleto CONFIRMADO: un boleto «incierto» no frena al siguiente premio

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · decisión **D4** del plan; el ejecutor, al elegir dónde
  colgar el instante del último premio
- **Dónde:** `ruleta/inventario.py`, `confirmar()`
  (`grep -n "_ultimo_premio" ruleta/inventario.py`).
- **Qué pasa:** la decisión D4 dice, literal, «si el **último boleto con premio
  (impreso)** se imprimió hace menos de esos minutos…», así que el instante se
  apunta en `confirmar()`, que es el evento `impreso`. Pero hay un tercer estado:
  **`incierto`**, el boleto cuya impresión se cortó a medio envío y que **pudo
  salir en papel** (por eso el premio se queda contado como entregado). Ese
  boleto **no** apunta el instante, así que la jugada siguiente puede dar otro
  premio de inmediato.
- **Por qué es residual:** no es un defecto de conducta ni una afirmación falsa:
  es la decisión implementada al pie de la letra. Y el caso es raro —por **cable
  USB** un `ErrorEnvio` es mucho menos probable que por Bluetooth— y benigno: lo
  peor que pasa es que salgan dos premios seguidos, que es justo la molestia que
  la regla quiere evitar, no un premio de más (el stock ya se descontó).
- **Riesgo si no se toca:** que en el único caso en que se corta una impresión,
  dos premios salgan pegados. Nadie lo notaría salvo el mesero.
- **Propuesta:** que el orquestador decida si `marcar_incierto()` debe apuntar
  también el instante. Son dos líneas y un golden; el ejecutor **no lo hizo por
  su cuenta** porque la decisión decía «impreso».
- **Estado:** **abierta como confirmación del orquestador.** **Sin golden:**
  `test_la_separacion_solo_la_marca_un_boleto_impreso` ancla el boleto
  **revertido** y el **consuelo confirmado**, pero **ninguna prueba llama a
  `marcar_incierto()` junto a `espera_separacion()`** (comprobado el 2026-09-16:
  las cinco llamadas a `marcar_incierto` de la suite están en pruebas de
  pendientes y de stock, no de separación). Hoy este comportamiento se puede
  cambiar **sin que la suite se ponga en rojo**; si el orquestador lo confirma tal
  cual está, hace falta el golden que lo fije.
- **Nota fechada (2026-09-16, cierre documental de las Fases 4b, 4c y 4d).**
  **La CONDUCTA queda confirmada: el orquestador ACEPTÓ la lectura del
  ejecutor** —la separación la marca **solo un boleto impreso con premio**, que
  es lo que dice la decisión **D4** al pie de la letra—; `marcar_incierto()`
  **no** apunta el instante y **no se toca**. **Pero la ficha SIGUE ABIERTA por
  la otra mitad:** falta el golden que fije esa conducta. Mientras no exista,
  alguien puede cambiarla sin que la suite se ponga en rojo, que es justo lo que
  el §5 del protocolo llama «un assert que no muerde». **Lo que falta, en una
  línea:** una prueba que llame a `marcar_incierto()` y compruebe que
  `espera_separacion()` sigue en `0.0`. Evidencia:
  `docs/actas/2026-09-16-fase-4bcd.md` §7.

---

## F-269 · El tope de una franja se puede pasar cruzando franjas: lo abierto y no ganado se arrastra

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · tensión entre las decisiones **D2** y **D3** del plan,
  vista por el ejecutor al implementar `liberadas()`
- **Dónde:** `ruleta/inventario.py`, `motivo_no_disponible()` y `liberadas()`
  (`grep -n "franja_activa" ruleta/inventario.py`).
- **Qué pasa:** la **D2** dice que el `tope` de una franja es «el máximo **de esa
  franja, ese día**», y la **D3** dice que «una pieza liberada y no ganada sigue
  disponible hasta el cierre». Las dos no caben a la vez. El programa cuenta
  **piezas abiertas menos entregadas hoy**, sin llevar la cuenta por franja, así
  que: si la silla de la franja de la comida (13:00–16:00, tope 1) **no se gana**,
  a las 19:00 se abre la de la cena y quedan **dos** disponibles; las dos pueden
  salir esa noche. **El tope de una sola franja tampoco se respeta cuando lo que
  se arrastra se gasta dentro de ella:** medido el 2026-09-16 con el `config.json`
  real, a las 19:00 sin nada entregado la silla tiene **dos** piezas abiertas y
  las **dos** pueden salir entre las 19:00 y las 22:00, dentro de una franja de
  `tope` 1. Lo único que nunca se pasa es el `tope_diario` del premio, que sigue
  cortando el día en 2. El golden `test_el_tope_de_una_franja_se_respeta` ancla el
  otro caso, el que sí se cumple: ganada la silla de la comida, no sale otra hasta
  las 19:00.
- **Por qué es residual:** el efecto es el que el usuario pidió —«las piezas no
  se acumulan por adelantado» se cumple, porque nada se arrastra al día
  siguiente— y lo que se arrastra dentro del día es justo lo que la D3 llama «no
  se pierde». Respetar el tope por franja al pie de la letra obligaría a llevar
  un contador **por franja y por día** en `estado.json`, es decir, estado nuevo y
  persistido, en la fase que abre el evento el lunes.
- **Riesgo si no se toca:** que un jueves flojo salgan **las dos sillas del día
  entre las 19:00 y las 22:00**, en vez de una en la comida y otra en la cena. No
  se regala ninguna pieza de más.
- **Propuesta:** que el orquestador confirme que el arrastre dentro del día es lo
  querido. Si no lo es, hace falta un contador por franja en `estado.json` y su
  migración de estados viejos.
- **Estado:** **abierta como confirmación del orquestador.** Documentado en el §2
  del documento del evento («si nadie juega en un buen rato, se juntan varias
  piezas abiertas»). **Cerrada el 2026-09-16 como confirmación del orquestador:
  ver la nota fechada al pie de esta ficha.**
- **Nota fechada (2026-09-16, cierre documental de las Fases 4b, 4c y 4d).**
  **CONFIRMADA: el orquestador ACEPTÓ la lectura del ejecutor.** El arrastre
  dentro del día **es lo querido** y **no se cambia**: lo que una franja abre y
  nadie gana sigue disponible hasta el cierre, aunque eso signifique que a las
  19:00 puedan quedar **dos sillas** y que las dos salgan esa noche. Las dos
  razones de la aceptación son las que la propia ficha escribe: **no se regala
  ninguna pieza de más** —lo que corta el día sigue siendo el `tope_diario`— y
  la alternativa exigiría un **contador por franja y por día en `estado.json`**,
  es decir, estado nuevo y persistido con su migración, **en la semana en que el
  evento abre**. En el mismo commit se corrigieron el comentario y el mensaje de
  error de `ruleta/config.py` que llamaban al `tope` «el máximo de esa franja ese
  día», porque con esta lectura **era falso**: los encontró el escéptico.
  **Esta ficha se cierra como confirmación.** Evidencia:
  `docs/actas/2026-09-16-fase-4bcd.md` §7.

---

## F-270 · El peso 10 del consuelo lo propuse yo, no el usuario (hereda lo que quedaba de F-263)

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · decisión **D5** del plan
- **Dónde:** `config.json`, `juego.consuelo.peso` = **10**; §2 y §5.2 (PENDIENTE
  A) de `docs/evento-2026-09-asadero-33.md`.
- **Qué pasa:** con el reparto por horas, el consuelo ya no compite contra los 34
  papelitos del día sino contra **lo que esté abierto en ese instante**, que
  normalmente es **una o dos piezas**. El **10** sale de ahí: con un agua abierta
  (peso 11) gana el **52.4 %** de las jugadas, y con solo la hielera (peso 1), el
  **9.1 %**. El usuario **no eligió ese número**: dictó la tabla de premios, las
  franjas, el horario y la regla de que los premios no salgan seguidos, pero del
  peso del consuelo no dijo nada.
- **Por qué es residual:** es el único número del modelo que no cambia **cuántos**
  premios se entregan —eso lo fija el reloj—, solo **cada cuántas jugadas** toca.
  Medido el 2026-09-16 simulando un día entero: con 1 980, 660 o 220 jugadas se
  entregan **las 34 piezas** igual; por debajo de eso se queda alguna pieza en la
  bodega (**33.6 de 34** con 99 jugadas, **31.7 de 34** con 66).
- **Riesgo si no se toca:** que en las horas flojas gane demasiada gente seguida
  —a las 12:30, con una sola agua abierta, gana **1 de cada 2**— y el boleto
  pierda gracia. Subirlo a 20 bajaría esa primera jugada al 35 %.
- **Propuesta:** enseñarle al usuario la tabla del §2 del documento («qué tan
  seguido se gana») y preguntarle si le gusta el 52 % del momento en que hay una
  pieza abierta. Se cambia **un solo número**, en el §5.1 y el §5.2 del documento
  **y** en `config.json`: dos goldens comparan los dos archivos por igualdad.
- **Estado:** **abierta. Requiere decisión del usuario.** Sustituye a **F-263**,
  que quedó cerrada por derogación el mismo día.

---

## F-271 · Un horario que cruce la medianoche no se puede escribir, y nadie avisa de que `hora_inicio_dia` y `horario` pueden pelearse

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · ejecutor, al escribir la validación de la decisión **D1**
- **Dónde:** `ruleta/config.py`, `validar()`, la rama de `juego.horario`
  (`grep -n "horario.abre" ruleta/config.py`).
- **Qué pasa:** la validación exige **`abre` < `cierra`**, así que un horario de
  bar —«de 20:00 a 02:00»— **no se puede expresar**: el mensaje dice que la
  apertura tiene que ser anterior al cierre y no explica que no hay forma de
  cruzar la medianoche. Además, nadie comprueba que el horario **quepa dentro del
  día operativo**: con `hora_inicio_dia` en 6 y un horario de 02:00 a 05:00, todo
  el evento caería en el día operativo **anterior**, los topes diarios se
  contarían al revés y el programa **no diría nada**.
- **Por qué es residual:** el Asadero 33 abre de **12:00 a 23:00**, dentro de su
  día operativo (que empieza a las 6:00), y el propio documento del evento lo
  deja comprobado: «el día operativo siempre coincide con el día del calendario».
  Ninguno de los dos casos puede darse hoy.
- **Riesgo si no se toca:** que alguien copie el programa a un negocio nocturno y
  se lleve un reparto por horas contado en el día equivocado, **sin un solo
  aviso**. Es el mismo tipo de trampa silenciosa que la **F-264**.
- **Propuesta:** dos validaciones baratas en `validar()`: (a) si `abre` es mayor
  o igual que `cierra`, decir en el mensaje que **el horario no puede cruzar la
  medianoche**; y (b) si los minutos de `abre` quedan por debajo de
  `hora_inicio_dia`, avisar de que ese horario cae en el día operativo anterior.
  Las dos con golden, como el resto.
- **Estado:** **abierta.** Hermanas: **F-264** (un cero de más en el peso del
  consuelo tampoco avisa).

---

## F-272 · `ruleta/hardware.py` estaba en el conjunto de archivos permitido y no hizo falta tocarlo

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · brief del orquestador (lista de archivos esperados al
  terminar)
- **Dónde:** `ruleta/hardware.py`, sin cambios; §7 del plan
  `docs/planes/fase-4d-horas.md`.
- **Qué pasa:** el brief de la fase esperaba ver `ruleta/hardware.py` entre los
  archivos modificados. **No se tocó:** nada de lo que esta fase construye —el
  horario, las franjas, el reparto, la separación y la espera de la hora— pasa
  por los botones ni por el LED. El comprobador de la hora vive en
  `ruleta/app.py`, que es donde está el ciclo de arranque, y entra **inyectado**
  por el constructor de `Ruleta`, igual que el reloj.
- **Por qué es residual:** el conjunto de archivos del §7 de un plan es una
  **compuerta** —«como mucho estos»—, no una obligación de tocarlos todos.
  Inventar un cambio en `hardware.py` para que la lista cuadrara habría sido
  peor: ese módulo está **verificado en hardware** desde la Fase 3 y las
  prohibiciones de las fases anteriores lo protegen.
- **Riesgo si no se toca:** ninguno técnico. El único riesgo es de proceso: que
  el agente de commit o un verificador lea la lista del brief como un censo
  exacto y se extrañe de que falte un archivo.
- **Propuesta:** que el orquestador lo dé por bueno. Queda anotado aquí para que
  el acta de la fase no tenga que reconstruirlo de memoria.
- **Estado:** **abierta como confirmación del orquestador.**

---

## F-273 · Cuando la hora SÍ se sincroniza, la pieza D no deja ni una línea en el journal

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · cierre documental; lo señaló el verificador en vivo del
  deploy de las 12:42:46
- **Dónde:** `ruleta/app.py`, `esperar_hora_sincronizada()` y
  `hora_sincronizada_del_sistema()`
  (`grep -n "esperar_hora_sincronizada" ruleta/app.py`).
- **Qué pasa:** la pieza D **solo registra el fallo**. Si la hora está
  sincronizada —o si no hay ninguna señal que preguntar, como en una PC—, la
  función devuelve `True` **en silencio**: no hay `log.info`, no hay nada. Los
  únicos rastros que deja son el `log.warning` **«HORA SIN CONFIRMAR: el sistema
  no sincronizó la hora en %.0f s…»** cuando se agota el tope, el
  `log.warning` de `timedatectl` inalcanzable y el `log.exception` del
  comprobador que revienta. Medido el 2026-09-16 en el arranque de las 12:42:46,
  con `NTPSynchronized=yes`: el journal trae `Ruleta arrancando. Premios: …`,
  `Inventario impreso (arranque). Folio actual 00005` y `Lista. Esperando
  jugadas.`, y **ninguna línea sobre la hora**.
- **Por qué es residual:** **no es un defecto de conducta.** El programa hace
  exactamente lo que el plan pedía, y el boleto de inventario **sí** lleva la
  fecha impresa, que es la señal que el personal mira. Un `log.info` de más en
  cada arranque es ruido para quien lee el journal buscando errores.
- **Riesgo si no se toca:** que nadie pueda distinguir, leyendo el journal, entre
  «la hora se confirmó a la primera», «se confirmó a los 90 segundos» y «el
  programa ni siquiera preguntó porque `espera_hora_seg` estaba en 0». En una Pi
  **sin batería RTC**, y el día que un boleto salga con la fecha mal, esa
  distinción es justo lo primero que alguien va a querer saber. Hoy hay que
  deducirlo de la ausencia de líneas, que es la peor forma de evidencia.
- **Propuesta:** un `log.info` de una línea al final de
  `esperar_hora_sincronizada()` cuando devuelve `True`, diciendo **cuántos
  segundos costó** (por ejemplo, «Hora del sistema confirmada en 0.0 s» o «Hora
  no comprobada: juego.espera_hora_seg = 0»), con su golden; o, si se prefiere no
  añadir ruido, dejarlo como está **por decisión escrita**. **Lo decide el
  orquestador**, que es quien lee los journals de los deploys.
- **Estado:** **resuelta** el **2026-09-16** (Fase 4e; plan
  `docs/planes/fase-4e-final.md`, decisión **D3**). El orquestador decidió
  **añadir el registro**, y decidió bien: en el arranque en frío de ese mismo día
  la espera duró **28.3 s** y en el journal **no dejó ni una línea**, de modo que
  esos 28 s de silencio **aparentaban 5 minutos** por el salto del reloj.
  `esperar_hora_sincronizada()` ahora escribe: (1) `Esperando a que la hora se
  sincronice (hasta 300 s)…` al empezar; (2) `Sigo esperando la hora: llevo 10 s
  de 300 s` **cada 10 segundos** —`PERIODO_AVISO_HORA`, que **no** es la cadencia
  de consulta, que sigue siendo de 2 s—; y (3) `Hora sincronizada tras 28 s` al
  terminar, o el `WARNING` **HORA SIN CONFIRMAR** de siempre si se agota el tope.
  **Con `espera_hora_seg` = 0 no registra nada**, porque no espera nada: un
  `log.info` ahí sería ruido en cada arranque de cualquier instalación que no use
  la pieza D. Goldens por **igualdad de lista** con el registro reencendido
  (`registro_activo()`, ficha **F-253**) y el reloj falso:
  `test_la_espera_de_la_hora_se_ve_en_el_journal` (0, 10, 20 y 22 s),
  `test_la_hora_que_ya_estaba_puesta_tambien_deja_su_linea`,
  `test_el_tope_agotado_se_ve_en_el_journal` y
  `test_sin_espera_configurada_no_se_registra_nada`; siete mutaciones sobre copia
  (M1 a M7 del plan), **las siete en rojo**. **Lo que esta ficha dejaba dicho y
  ya no es cierto:** la pieza D **sí** se ha visto morder en la Pi (**F-241**,
  cerrada en hardware). **Lo que sigue siendo cierto:** la línea
  `HORA SIN CONFIRMAR: revisar fecha` **nunca se ha impreso en papel**, porque
  hasta hoy la hora siempre llegó dentro del tope.

---

## F-274 · El acta del 2026-09-16 cubre TRES fases en un solo documento

- **Fecha:** 2026-09-16
- **Origen:** Fase 4d · cierre documental; decisión del orquestador (C1 del brief
  del escriba)
- **Dónde:** `docs/actas/2026-09-16-fase-4bcd.md` y
  `docs/actas/2026-09-16-hechos-medidos-fase-4bcd.md`.
- **Qué pasa:** las Fases 1, 2, 3 y 4a tienen **un acta por fase**
  (`docs/actas/2026-09-11-fase-1.md`, `…-fase-2.md`, `2026-09-15-fase-3.md`,
  `…-fase-4a.md`). Las Fases **4b**, **4c** y **4d** comparten **una sola**, con
  una sección por fase, y **un solo** archivo de hechos medidos para las tres.
  Es una desviación de la convención del `CLAUDE.md`, que pide
  `docs/actas/<AAAA-MM-DD>-<fase>.md`.
- **Por qué es residual:** las tres fases se hicieron **el mismo día**, sobre el
  **mismo archivo de hechos**, con el **mismo usuario probando en vivo** entre
  una y otra, y cada una **deshace o supera** algo de la anterior: la 4c corrige
  lo que la 4b hizo visible, y la 4d cambia el peso que la 4c acababa de cargar.
  Contadas por separado, las tres actas se pasarían la mitad del texto
  remitiéndose entre sí. El nombre del archivo lo dice (`fase-4bcd`) y el
  encabezado nombra los tres commits, así que **nada queda sin dirección**.
- **Riesgo si no se toca:** que alguien busque `docs/actas/2026-09-16-fase-4c.md`
  y crea que esa fase no tiene acta; y que un índice futuro que cuente actas por
  fase salga descuadrado. También pierde granularidad: los tres planes remiten a
  la **misma** acta, así que hay que leerla entera para encontrar lo de una fase.
- **Propuesta:** dejarlo como está —partirla ahora obligaría a triplicar el
  contexto común y a decidir dónde vive la prueba en vivo del usuario, que cierra
  las tres— y, si alguien quiere el índice limpio, añadir tres archivos de una
  línea (`2026-09-16-fase-4b.md`, `…-4c.md`, `…-4d.md`) que apunten a la acta
  única. **No se hizo aquí** para no inventar documentos que nadie pidió.
- **Estado:** **abierta como confirmación del orquestador.** Hermana: **F-258**
  (la nota de pausa que entró en un commit de código), la otra desviación de
  convención documental de esta serie de fases.

---

## F-275 · La Pi no tiene el Wi-Fi del asadero dado de alta: hay que hacerlo EN SITIO, y de él depende la fecha

- **Fecha:** 2026-09-16
- **Origen:** Fase 4e · brief del orquestador (inventario de perfiles de red de
  la Pi hecho en la sesión del 2026-09-16, antes de lanzar la fase)
- **Dónde:** en la Pi, los perfiles de red guardados (`nmcli connection show`);
  hoy solo hay **dos**: `casa` (prioridad **20**) y `miltimex` (prioridad **10**).
  **El perfil que apuntaba al Wi-Fi del asadero ya no existe.**
- **Qué pasa:** el kiosco del evento **necesita internet para saber qué día es**.
  La Pi **no tiene batería RTC** (decisión del usuario del 2026-09-15): al
  encender arranca con la última hora que guardó y **la corrige por NTP en
  cuanto entra a una red**. Si en el asadero no encuentra ninguna red conocida,
  **no corrige nada**. En las pruebas la Pi se conecta a la red de casa
  (`SL-Durazo`, medido el 2026-09-16), que es la que tiene el perfil `casa`.
- **Por qué es residual:** **no es un defecto del programa ni una afirmación
  falsa de ningún documento**: es un paso de instalación que solo se puede hacer
  **en el lugar y con la contraseña del usuario**, y **ningún agente teclea
  credenciales** (§6 de `CLAUDE.md`). El programa se comporta bien sin red:
  espera sus 300 s, arranca igual e **imprime el aviso** en el boleto.
- **Riesgo si no se toca:** **alto, y desde la Fase 4e es peor que antes.** Sin
  red, la Pi cree que es **el día en que se apagó**. Y ahora que los premios
  llevan `desde`/`hasta` (**F-259**), una fecha equivocada **saca de la tómbola a
  los siete premios**: el kiosco no falla, no avisa —no hay LED (**F-240**,
  **F-256**)— y simplemente **reparte consuelos toda la noche**. El boleto de
  inventario de arranque lo delata de dos formas: la línea
  `HORA SIN CONFIRMAR: revisar fecha` y, sobre todo, **la fecha impresa**.
- **Propuesta:** el usuario, **en el asadero y antes del lunes 21**, da de alta
  el Wi-Fi del restaurante en la Pi (por ejemplo con `nmcli device wifi connect`,
  tecleando **él** la contraseña) y comprueba **en ese momento** dos cosas:
  `timedatectl` dice `System clock synchronized: yes`, y **el boleto de
  inventario sale con la fecha de hoy**. Alternativa, por si el Wi-Fi
  del local se resiste: el **punto de acceso móvil de Windows** de la laptop, con
  el mismo nombre y contraseña que el Wi-Fi del asadero. **Ojo: hoy la Pi tampoco
  entra sola en ese punto de acceso.** Justamente por llevar el mismo nombre, el
  perfil que servía para los dos es el que ya no existe: el punto de acceso hay
  que darlo de alta igual, y la contraseña la teclea el usuario. **Requiere al
  usuario.**
- **Estado:** **abierta.** Fecha límite: **lunes 21 de septiembre de 2026, antes
  de abrir.** Hermanas: **F-241** (de dónde sale la hora) y **F-257** (el alias
  de SSH y la red del punto de acceso).

---

## F-276 · La Fase 4e deja tres afirmaciones de `CLAUDE.md` desfasadas, y `CLAUDE.md` no se toca

- **Fecha:** 2026-09-16
- **Origen:** Fase 4e · el ejecutor, al re-grepear la espera de la hora
  (`grep -n "120" CLAUDE.md`)
- **Dónde:** `CLAUDE.md`, sección «Contexto del producto», la viñeta **Red y
  hora** y la lista de lo desplegado.
- **Qué pasa:** esta fase cambió tres cosas que `CLAUDE.md` afirma con números:
  1. «el kiosco espera hasta `juego.espera_hora_seg` segundos —hoy **120**…»
     y «**Al arrancar, el kiosco espera hasta 120 s**»: desde esta fase son
     **300**.
  2. «**Las fechas `desde`/`hasta` TODAVÍA NO están cargadas** (ficha F-259):
     hasta que se carguen, los siete premios están disponibles **todos los
     días**»: **ya están cargadas** (F-259, cerrada), así que es al revés.
  3. «**la pieza D nunca se ha visto morder en la Pi**»: se vio morder el
     2026-09-16 en un **arranque en frío real** (F-241).
- **Por qué es residual:** **el protocolo prohíbe que esta fase toque
  `CLAUDE.md`** (§7 del plan `docs/planes/fase-4e-final.md`, y la misma
  prohibición venía de la Fase 4d). No es un error de nadie: es el desfase normal
  entre un documento de contexto y la fase que acaba de cambiar el código. Y
  ninguna de las tres afirmaciones hace que el programa se comporte mal.
- **Riesgo si no se toca:** que la **próxima sesión** —o el próximo agente sin
  contexto— lea `CLAUDE.md` como fuente de verdad, dé por hecho que faltan las
  fechas y **vuelva a cargarlas**, o que calcule con 120 s la espera del arranque
  y crea que la Pi tardó de más. El riesgo es de **desinformación**, no de
  conducta.
- **Propuesta:** que **el orquestador** actualice esas tres frases de
  `CLAUDE.md` al cerrar la fase, con la fórmula que ya se usó el 2026-09-15 y el
  2026-09-16: **nota fechada**, sin borrar lo viejo, citando
  `docs/actas/2026-09-16-hechos-medidos-fase-4e.md` y el plan de esta fase.
- **Estado:** **CERRADA** el **2026-09-16**, en el cierre documental de la Fase
  4e. Hermana: **F-242** (la vez anterior que `CLAUDE.md` se quedó atrás, con lo
  de «producción sin red» y «la batería RTC es necesaria»).
- **Nota fechada (2026-09-16, cierre documental de la Fase 4e).** El escriba
  actualizó **solo** la sección «Contexto del producto» de `CLAUDE.md` —las
  secciones 1 a 7 y «Convenciones de este repo» **no se tocaron**— con las tres
  frases que esta ficha señalaba: los **300 s** en los dos sitios donde decía
  120, las fechas `desde`/`hasta` **ya cargadas** (hielera 24-25, los otros seis
  21-25, commit `70bcaa6`) con la consecuencia de que **hasta el lunes 21 toda
  jugada da consuelo**, y la pieza D **vista morder** en el arranque en frío del
  2026-09-16. Se añadió además el estado del inventario tras el reinicio de las
  **14:44**. Se siguió la fórmula de siempre: **nota fechada, sin borrar lo
  viejo**, citando `docs/actas/2026-09-16-hechos-medidos-fase-4e.md` y
  `docs/actas/2026-09-16-fase-4e.md`.

---

## F-277 · `boletos.csv` se MUEVE al respaldo en cada `reiniciar`, y hasta el primer boleto ese archivo no existe

- **Fecha:** 2026-09-16
- **Origen:** Fase 4e · deploy de las **14:44** (paso 4 del §8 del plan
  `docs/planes/fase-4e-final.md`), leyendo la salida literal del comando
- **Dónde:** en la Pi, `/home/asadero/ruleta/datos/boletos.csv`; el comando es
  `python3 -m ruleta reiniciar --si` (`ruleta/__main__.py`, `cmd_reiniciar`).
- **Qué pasa:** `reiniciar` **no copia** `boletos.csv`: lo **renombra** al
  respaldo con marca de tiempo. Medido el 2026-09-16 a las 14:44, con la salida
  literal «Folio actual: 00010. Premios entregados registrados: 2. Respaldo:
  `datos/estado_20260916_144415.json` / `datos/boletos_20260916_144415.csv`.
  Inventario reiniciado. Folio en 00000.». Después de eso, y **hasta que salga el
  primer boleto**, en `datos/` **no hay ningún `boletos.csv`**: el programa lo
  vuelve a crear, con su encabezado, cuando escribe la primera línea. Con
  `estado.json` no pasa: ese sí se vuelve a escribir enseguida. Y **`ruleta.log`
  no se respalda**, que es otra cosa que la salida del comando no dice.
- **Por qué es residual:** **no es un defecto**: es exactamente lo que el comando
  promete y lo que conviene —un archivo de bitácora no se parte por la mitad—, y
  además el respaldo queda con nombre fechado, al lado. El acta de las Fases 4b,
  4c y 4d ya lo anotó como **desviación 2**; esta ficha existe para que deje de
  vivir solo dentro de un acta.
- **Riesgo si no se toca:** que alguien —el usuario, o un agente sin contexto—
  abra `datos/` el lunes 21 antes de la primera jugada, **no encuentre
  `boletos.csv`**, lo lea como «se perdió la bitácora» o «el programa está roto»
  y **reinicie o reinstale algo** que está perfectamente bien. En un evento de
  cinco días, ese susto cuesta más que el archivo.
- **Propuesta:** dejarlo escrito donde se lee, no cambiar el comando. En
  `README.md` §5, en la tabla de «Archivos que genera», una línea que diga que
  **tras un `reiniciar` el archivo reaparece con el primer boleto**. Si alguna
  vez se toca el comando, lo barato es que **cree el archivo vacío con su
  encabezado** justo después de mover el viejo. **No urge**: no afecta a ninguna
  jugada.
- **Estado:** **abierta** (informativa). Evidencia:
  `docs/actas/2026-09-16-fase-4e.md` §7.2 y §8; y
  `docs/actas/2026-09-16-fase-4bcd.md` §9, desviación 2.

---

## F-278 · Lo que hay que hacer EN EL ASADERO antes de abrir: red, corriente y la fecha del boleto

- **Fecha:** 2026-09-16
- **Origen:** Fase 4e · cierre documental, desde el **estado final del kiosco**
  del archivo de hechos de la sesión
- **Dónde:** en el asadero, con la Pi encendida allá. Nada de esto se puede hacer
  desde casa ni desde un agente.
- **Qué pasa:** el 2026-09-16 el kiosco quedó **listo** —`70bcaa6` desplegado,
  servicio `active`, inventario en **folio `00000`**, fechas cargadas y espera de
  hora probada en frío—, pero **todo lo medido se midió en la red de casa**
  (`SL-Durazo`). Quedan tres cosas que **solo existen en el sitio**:
  1. **La Pi no tiene el Wi-Fi del asadero dado de alta.** Hoy solo conoce
     `casa` (prioridad **20**) y `miltimex` (**10**, el punto de acceso de la
     laptop); **el perfil que apuntaba al restaurante ya no existe** (ficha
     **F-275**).
  2. **Nadie ha encendido la Pi allá.** La prueba de corriente —enchufar,
     esperar y ver qué sale— **no está hecha**.
  3. **De esas dos depende la fecha**, y de la fecha dependen los premios: sin
     hora buena, **los siete premios quedan fuera de fechas** y el kiosco
     reparte consuelos toda la noche sin avisar (no hay LED: **F-240**,
     **F-256**).
- **Por qué es residual:** **no es un defecto del programa ni una afirmación
  falsa de ningún documento.** Son pasos de instalación y de operación, y el
  primero **exige la contraseña del Wi-Fi, que teclea el usuario**: ningún agente
  teclea credenciales (§6 de `CLAUDE.md`).
- **Riesgo si no se toca:** **alto.** Es, de todo lo que queda, lo único que
  puede arruinar el primer día del evento sin que nadie se dé cuenta a tiempo.
- **Propuesta · la lista, en orden, para el día que la Pi vaya al asadero:**
  1. **Dar de alta la red.** Con la Pi allá, por SSH o con teclado, y
     **tecleando el usuario la contraseña**. Lo más corto es que la pida el
     propio `nmcli`, que **no la muestra en pantalla ni la deja escrita en la
     línea de comandos**:

     ```bash
     sudo nmcli --ask device wifi connect "NOMBRE_DE_LA_RED"
     sudo nmcli connection modify "NOMBRE_DE_LA_RED" connection.id asadero
     sudo nmcli connection modify asadero connection.autoconnect yes
     sudo nmcli connection modify asadero connection.autoconnect-priority 30
     sudo nmcli connection up asadero
     ```

     Si esa forma no sirve —pasa cuando la red no sale en el escaneo—, la larga,
     leyendo la contraseña **sin eco** y borrándola de la sesión al terminar:

     ```bash
     read -s -p "Contrasena del wifi: " PSK; echo
     sudo nmcli connection add type wifi con-name asadero ifname wlan0 ssid "NOMBRE_DE_LA_RED"
     sudo nmcli connection modify asadero wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$PSK"
     sudo nmcli connection modify asadero connection.autoconnect yes connection.autoconnect-priority 30
     unset PSK
     sudo nmcli connection up asadero
     ```

     La **prioridad 30** la deja por encima de `casa` (20) y `miltimex` (10), que
     es lo que se quiere en el local. Si el Wi-Fi del restaurante se resiste,
     la alternativa es el **punto de acceso móvil de Windows** de la laptop, que
     lleva el mismo nombre y la misma contraseña: **también hay que darlo de
     alta**, por lo mismo (**F-275**).
  2. **Comprobar la hora, no suponerla:** `timedatectl` tiene que decir
     **`System clock synchronized: yes`**.
  3. **Prueba de corriente:** enchufar la Pi y la impresora **como van a quedar
     el lunes**, esperar a que salga el **boleto de inventario de arranque** y
     **leerle la fecha**. Tiene que ser **la de hoy**. Con la espera de 5 minutos
     puesta, lo normal es que tarde un poco: **eso es que está funcionando**.
  4. **Si el boleto trae la línea `HORA SIN CONFIRMAR: revisar fecha`, o si la
     fecha está mal: NO reiniciar la Pi.** Revisar que el internet del asadero
     esté funcionando, esperar un par de minutos y **pedir otro inventario**
     —el mesero mantiene **HABILITAR 6 segundos** sin que nadie toque JUGAR—.
     **No se abre hasta que ese boleto salga con la fecha correcta.**
  5. Aprovechar el viaje para **asegurar o soldar el pulsador HABILITAR**
     (**F-239**) y para decidir la **señal cuando una jugada se rechaza**
     (**F-256**).
  **Requiere al usuario.**
- **Estado:** **abierta.** Fecha límite: **lunes 21 de septiembre de 2026, antes
  de abrir.** Hermanas: **F-275** (la red), **F-241** (de dónde sale la hora),
  **F-239** (el pulsador) y **F-256** (la señal sin LED). Evidencia del estado
  con el que sale el kiosco de casa: `docs/actas/2026-09-16-fase-4e.md` §9.

---
