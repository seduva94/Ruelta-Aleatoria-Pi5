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
- **Estado:** abierta, sin acción antes del evento.

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
- **Estado:** abierta. **Bloquea el camino USB de la Fase 2 hasta verificarse.**

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
- **Estado:** abierta.

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
