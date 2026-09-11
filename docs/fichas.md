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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
