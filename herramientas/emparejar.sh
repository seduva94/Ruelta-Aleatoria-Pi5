#!/usr/bin/env bash
# Empareja la impresora térmica Bluetooth con la Raspberry, la marca como
# confiable y escribe su MAC en config.json. Se corre UNA vez (o si cambias
# de impresora). Ejecutar como usuario normal:
#     ./herramientas/emparejar.sh                 (busca y pregunta)
#     ./herramientas/emparejar.sh AA:BB:CC:DD:EE:FF
#
# Si no aparece en la búsqueda: apaga y enciende la impresora, o imprime su
# página de autoprueba (mantén FEED presionado al encenderla): ahí vienen su
# nombre Bluetooth, la MAC y el PIN (normalmente 0000 o 1234).
set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${DIR}/config.json"
MAC="${1:-}"
AGENTE=""
PINS=""

limpiar() {
  if [[ -n "${AGENTE}" ]]; then kill "${AGENTE}" 2>/dev/null || true; fi
  if [[ -n "${PINS}" ]]; then rm -f "${PINS}"; fi
}
trap limpiar EXIT INT TERM

if ! command -v bluetoothctl >/dev/null; then
  echo "Falta bluetoothctl. Corre primero: sudo ./instalar.sh" >&2
  exit 1
fi

sudo rfkill unblock bluetooth 2>/dev/null || true
bluetoothctl power on >/dev/null 2>&1
bluetoothctl pairable on >/dev/null 2>&1
if ! bluetoothctl show | grep -q "Powered: yes"; then
  echo "El adaptador Bluetooth no encendió. Revisa: rfkill list bluetooth ; systemctl status bluetooth" >&2
  exit 1
fi

# bluetoothd olvida los dispositivos vistos y no emparejados ~30 s después de
# terminar la búsqueda, así que se busca justo antes de cada intento.
conocida() { ! bluetoothctl info "${MAC}" 2>&1 | grep -q "not available"; }
emparejada() { bluetoothctl info "${MAC}" 2>/dev/null | grep -q "Paired: yes"; }
buscar() {
  local seg="${1:-15}"
  echo "Buscando la impresora durante ${seg} segundos..."
  timeout $((seg + 5)) bluetoothctl --timeout "${seg}" scan on >/dev/null 2>&1 || true
}

if [[ -z "${MAC}" ]]; then
  echo "Enciende la impresora."
  buscar 20
  echo
  echo "Dispositivos vistos:"
  bluetoothctl devices | sed 's/^Device //' | nl -w2 -s') '
  echo
  read -rp "Escribe la MAC de la impresora (AA:BB:CC:DD:EE:FF) o el número de la lista: " ENTRADA
  if [[ "${ENTRADA}" =~ ^[0-9]+$ ]]; then
    MAC="$(bluetoothctl devices | sed -n "${ENTRADA}p" | awk '{print $2}')"
  else
    MAC="${ENTRADA}"
  fi
fi
MAC="$(echo "${MAC}" | tr '[:lower:]' '[:upper:]' | tr -d ' ')"
if ! [[ "${MAC}" =~ ^([0-9A-F]{2}:){5}[0-9A-F]{2}$ ]]; then
  echo "MAC inválida: '${MAC}'" >&2
  exit 1
fi
echo "Impresora: ${MAC}"

if emparejada; then
  echo "Ya estaba emparejada."
else
  if command -v bt-agent >/dev/null; then
    # bt-agent (bluez-tools) contesta el PIN automáticamente; probamos los PIN típicos.
    PINS="$(mktemp)"
    for PIN in 0000 1234; do
      if ! conocida; then buscar 15; fi
      if ! conocida; then
        echo "La impresora ${MAC} no aparece. Revisa que esté encendida, cerca y sin un celular conectado." >&2
        break
      fi
      printf '%s %s\n' "${MAC}" "${PIN}" > "${PINS}"
      bt-agent -c NoInputNoOutput -p "${PINS}" >/dev/null 2>&1 &
      AGENTE=$!
      sleep 1
      echo "Emparejando (PIN ${PIN} si lo pide)..."
      timeout 40 bluetoothctl pair "${MAC}" || true
      sleep 1
      kill "${AGENTE}" 2>/dev/null || true
      wait "${AGENTE}" 2>/dev/null || true
      AGENTE=""
      if emparejada; then break; fi
      bluetoothctl remove "${MAC}" >/dev/null 2>&1 || true
    done
  else
    echo "No está instalado bt-agent (paquete bluez-tools); se intenta sin agente automático."
    if ! conocida; then buscar 15; fi
    timeout 40 bluetoothctl pair "${MAC}" || true
  fi
  if ! emparejada; then
    echo
    echo "No se pudo emparejar automáticamente. Hazlo a mano (enciende la impresora primero):"
    echo "    bluetoothctl"
    echo "    scan on               (espera a que aparezca ${MAC}, luego:)"
    echo "    agent on"
    echo "    default-agent"
    echo "    pair ${MAC}        (teclea el PIN de la impresora si lo pide: 0000 o 1234)"
    echo "    trust ${MAC}"
    echo "    quit"
    echo "y vuelve a correr: ./herramientas/emparejar.sh ${MAC}"
    exit 1
  fi
fi

bluetoothctl trust "${MAC}" >/dev/null 2>&1 || true
echo
bluetoothctl info "${MAC}" | grep -E "Name|Paired|Trusted|Serial Port" | sed 's/^/   /'
if ! bluetoothctl info "${MAC}" | grep -q "Serial Port"; then
  echo "   AVISO: la impresora no anuncia el perfil 'Serial Port'. Si la conexión falla,"
  echo "   puede ser una impresora solo BLE; en ese caso conéctala por USB (ver README)."
fi

echo
echo "Guardando la MAC en ${CONFIG}..."
python3 - "${CONFIG}" "${MAC}" <<'EOF'
import json, sys
ruta, mac = sys.argv[1], sys.argv[2]
with open(ruta, encoding="utf-8") as f:
    cfg = json.load(f)
cfg.setdefault("impresora", {})
cfg["impresora"]["mac"] = mac
cfg["impresora"]["tipo"] = "bluetooth"
with open(ruta, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
print("   impresora.mac =", mac)
EOF

echo
echo "Probando la conexión y el canal RFCOMM..."
cd "${DIR}" && python3 -m ruleta diagnostico || true
echo
echo "Si el diagnóstico salió bien, imprime la prueba:  python3 -m ruleta probar-impresora"
