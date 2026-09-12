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
