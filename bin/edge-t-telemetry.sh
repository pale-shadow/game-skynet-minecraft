#!/usr/bin/env bash

# Senior Admin Diagnostic Script v2.3 (Edge TPU / Hub 06 Edition)
# Purpose: Extract telemetry for Mendel-based Mono-Eye Sensor infrastructure.

set -uo pipefail

# Ensure local mcrcon path is established
MCRCON_BIN="/usr/bin/mcrcon"

echo "--- [Node Environment: Hub 06 Mono-Eye Sensor] ---"
if [[ -f "/etc/os-release" ]]; then
    grep "PRETTY_NAME" /etc/os-release | cut -d'"' -f2
fi
uname -sr

echo -e "\n--- [Remote Server Status: Chonk] ---"
# Utilizing unblocked RCON credentials for remote indexing
if [[ -n "${RCON_PASS:-}" && -n "${CHONK_IP:-}" ]]; then
    VERSION_QUERY=$($MCRCON_BIN -H "${CHONK_IP}" -P "${RCON_PORT}" -p "${RCON_PASS}" "version" | grep -i "Paper")
    echo "Remote Engine: ${VERSION_QUERY:-Connection Failed}"
else
    echo "ERROR: RCON credentials not found. Run 'direnv allow'."
fi

echo -e "\n--- [Hardware Thermals & TPU Status] ---"
# Replacing bc with awk for Mendel 5 compatibility
if [[ -f "/sys/class/thermal/thermal_zone0/temp" ]]; then
    CPU_TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo -n "i.MX 8M CPU Temp: "
    echo "$CPU_TEMP 1000" | awk '{printf "%.1f°C\n", $1/$2}'
fi

if [[ -f "/sys/class/apex/apex_0/temp" ]]; then
    TPU_TEMP=$(cat /sys/class/apex/apex_0/temp)
    echo -n "Google Edge TPU Temp: "
    echo "$TPU_TEMP 1000" | awk '{printf "%.1f°C\n", $1/$2}'
else
    echo "Edge TPU: Apex driver temperature node not found."
fi

echo -e "\n--- [Resource Allocation] ---"
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_RAM_GB=$(echo "$TOTAL_RAM_KB 1048576" | awk '{printf "%.2f", $1/$2}')
echo "Node Total RAM: ${TOTAL_RAM_GB}GB"

# T2BM Vision Buffer: 1.0GB headroom for architectural inference
VISION_BUFFER=1.0
OS_OVERHEAD=0.5
AVAILABLE_COMPUTE=$(echo "$TOTAL_RAM_GB $OS_OVERHEAD $VISION_BUFFER" | awk '{printf "%.2f", $1 - ($2 + $3)}')
echo "Available Compute Headroom: ${AVAILABLE_COMPUTE}GB"

echo -e "\n--- [Performance Protocol] ---"
if [[ -n "${RCON_PASS:-}" ]]; then
    echo "Triggering Spark Sampler on Chonk..."
    $MCRCON_BIN -H "${CHONK_IP}" -P "${RCON_PORT}" -p "${RCON_PASS}" "spark sampler --timeout 60"
    echo "ACTION: Review the Spark link generated in the Chonk console."
fi
