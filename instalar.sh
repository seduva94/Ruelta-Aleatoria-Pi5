#!/usr/bin/env bash
# Instalador de la Ruleta Asadero 33 para Raspberry Pi OS (Bookworm o Trixie, 64 bits).
#
#   cd ~/ruleta && sudo ./instalar.sh
#
# Instala los paquetes del sistema (no usa pip: todo viene de apt), habilita el
# Bluetooth, deja una regla udev defensiva para el GPIO de la Pi 5, otra para la
# impresora USB (permisos y nombre fijo del dispositivo), registra el servicio
# systemd y lo habilita para que arranque solo al encender.
# Se puede volver a ejecutar las veces que haga falta.
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Ejecuta este instalador con sudo:  sudo ./instalar.sh" >&2
  exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USUARIO="${SUDO_USER:-}"
if [[ -z "${USUARIO}" || "${USUARIO}" == "root" ]]; then
  USUARIO="$(id -un 1000 2>/dev/null || true)"
fi
if [[ -z "${USUARIO}" ]]; then
  echo "No pude determinar el usuario normal. Ejecuta como: sudo -u TU_USUARIO sudo ./instalar.sh" >&2
  exit 1
fi

echo "== Carpeta del programa: ${DIR}"
echo "== El servicio correrá como el usuario: ${USUARIO}"

echo
echo "== 1/7 Paquetes del sistema"
apt-get update
apt-get install -y python3 python3-gpiozero python3-lgpio python3-pil bluez bluez-tools rfkill

echo
echo "== 2/7 Grupos del usuario (gpio para los botones)"
usermod -aG gpio "${USUARIO}"
getent group bluetooth >/dev/null && usermod -aG bluetooth "${USUARIO}" || true

echo
echo "== 3/7 Bluetooth encendido y habilitado al arranque (impresora de respaldo)"
rfkill unblock bluetooth 2>/dev/null || true
systemctl enable --now bluetooth
bluetoothctl power on >/dev/null 2>&1 || true

echo
echo "== 4/7 Regla udev para el chip GPIO de la Pi 5"
# El kernel ha cambiado el número del chip RP1 más de una vez (gpiochip4 -> 0 -> 15).
# gpiozero abre gpiochip4 si existe; este enlace lo garantiza aunque cambie el número.
cat > /etc/udev/rules.d/60-ruleta-rp1-gpiochip4.rules <<'EOF'
SUBSYSTEM=="gpio", KERNEL=="gpiochip*", DRIVERS=="pinctrl-rp1", SYMLINK+="gpiochip4"
EOF
udevadm control --reload 2>/dev/null || true
udevadm trigger --subsystem-match=gpio 2>/dev/null || true

echo
echo "== 5/7 Impresora USB (permisos y nombre fijo del dispositivo)"
# La impresora va por cable USB y el kernel (driver usblp) la expone como
# /dev/usb/lp0, con permisos 0660 root:lp. Dos cosas hacen falta y las dos se
# pierden al desconectar el cable si no estan en una regla: el grupo del nodo y
# un nombre que no dependa del numero (si algun dia sale lp1, config.json
# seguiria apuntando a /dev/ruleta-impresora y no habria que tocar nada).
# El VID:PID esta medido en la impresora del asadero (AOMU My-A1, familia POS-80).
cat > /etc/udev/rules.d/61-ruleta-impresora-usb.rules <<'EOF'
SUBSYSTEM=="usbmisc", KERNEL=="lp[0-9]*", ATTRS{idVendor}=="0418", ATTRS{idProduct}=="5011", MODE="0660", GROUP="lp", SYMLINK+="ruleta-impresora"
EOF
getent group lp >/dev/null && usermod -aG lp "${USUARIO}" || true
udevadm control --reload-rules 2>/dev/null || true
udevadm trigger --subsystem-match=usbmisc 2>/dev/null || true

echo
echo "== 6/7 Carpeta de datos y permisos"
mkdir -p "${DIR}/datos"
chown -R "${USUARIO}:" "${DIR}"
chmod +x "${DIR}/herramientas/"*.sh 2>/dev/null || true

echo
echo "== 7/7 Servicio systemd"
sed -e "s|@DIR@|${DIR}|g" -e "s|@USUARIO@|${USUARIO}|g" "${DIR}/ruleta.service" \
  > /etc/systemd/system/ruleta.service
systemctl daemon-reload
systemctl enable ruleta.service
if systemctl is-active --quiet ruleta.service; then
  systemctl restart ruleta.service
  echo "Servicio 'ruleta' actualizado y reiniciado (ya estaba corriendo)."
else
  echo "Servicio 'ruleta' habilitado (arranca solo al encender). Aún NO se inició."
fi

echo
echo "== Diagnóstico"
(cd "${DIR}" && sudo -u "${USUARIO}" env PYTHONIOENCODING=utf-8 python3 -m ruleta --config "${DIR}/config.json" diagnostico) || true

cat <<EOF

=====================================================================
 Instalación terminada. Siguientes pasos (como usuario ${USUARIO}, en ${DIR}):

 1. Conecta la impresora con su cable USB, enciéndela con papel y comprueba
    que el sistema la ve (debe decir [ok] impresora conectada):
       python3 -m ruleta diagnostico

 2. Imprimir el boleto de prueba (acentos, ancho, logo y corte):
       python3 -m ruleta probar-impresora

 3. Ver cómo quedarán los boletos sin gastar papel:
       python3 -m ruleta vista-previa --todos

 4. Poner tus premios reales en config.json (nano config.json) y dejar el
    inventario en cero para el evento:
       python3 -m ruleta reiniciar --si

 5. Arrancar (a partir de aquí arranca solo al encender la Pi):
       sudo systemctl start ruleta
       journalctl -u ruleta -f          (ver el log en vivo, Ctrl+C para salir)

 Si algún día la impresora tuviera que ir por Bluetooth (respaldo), empareja y
 pon "tipo": "bluetooth" en config.json:
       ./herramientas/emparejar.sh

 Cada vez que edites config.json:  sudo systemctl restart ruleta
 Si cambiaste de grupo (gpio, lp), cierra sesión y vuelve a entrar antes de
 correr el programa a mano; el servicio no lo necesita.
=====================================================================
EOF
