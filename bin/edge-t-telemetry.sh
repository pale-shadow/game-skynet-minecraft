#!/usr/bin/env bash

# Senior Admin Diagnostic Script v2.2 (Edge TPU / Hub 06 Edition)
# Purpose: Extract telemetry for Mendel-based Mono-Eye Sensor infrastructure.

set -uo pipefail

echo "--- [Node Environment: Hub 06 Mono-Eye Sensor] ---"
# Detect Mendel OS and Kernel
if [[ -f "/etc/os-release" ]]; then
    grep "PRETTY_NAME" /etc/os-release | cut -d'"' -f2
fi
uname -sr

echo -e "\n--- [Remote Server Status: Chonk] ---"
# Use mcrcon to verify the link to the simulation engine
if [[ -n "${RCON_PASS:-}" && -n "${CHONK_IP:-}" ]]; then
    VERSION_QUERY=$(mcrcon -H "${CHONK_IP}" -P "${RCON_PORT}" -p "${RCON_PASS}" "version" | grep -i "Paper")
    echo "Remote Engine: ${VERSION_QUERY:-Connection Failed}"
else
    echo "ERROR: RCON credentials not found. Run 'direnv allow'."
fi

echo -e "\n--- [Hardware Thermals & TPU Status] ---"
# i.MX 8M CPU Thermal Monitoring
if [[ -f "/sys/class/thermal/thermal_zone0/temp" ]]; then
    CPU_TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo "i.MX 8M CPU Temp: $(echo "scale=1; $CPU_TEMP / 1000" | bc)°C"
fi

# Edge TPU Apex Thermal Monitoring
if [[ -f "/sys/class/apex/apex_0/temp" ]]; then
    TPU_TEMP=$(cat /sys/class/apex/apex_0/temp)
    echo "Google Edge TPU Temp: $(echo "scale=1; $TPU_TEMP / 1000" | bc)°C"
else
    echo "Edge TPU: Apex driver temperature node not found."
fi

echo -e "\n--- [Resource Allocation] ---"
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_RAM_GB=$(echo "scale=2; $TOTAL_RAM_KB / 1024 / 1024" | bc)
echo "Node Total RAM: ${TOTAL_RAM_GB}GB"

# T2BM Vision Buffer: 1.0GB (Tailored for quantized .tflite architectural models)
VISION_BUFFER=1.0
OS_OVERHEAD=0.5
AVAILABLE_COMPUTE=$(echo "scale=2; $TOTAL_RAM_GB - ($OS_OVERHEAD + $VISION_BUFFER)" | bc)
echo "Available Compute Headroom: ${AVAILABLE_COMPUTE}GB"

echo -e "\n--- [Performance Protocol] ---"
if [[ -n "${RCON_PASS:-}" ]]; then
    echo "Triggering Spark Sampler on Chonk..."
    mcrcon -H "${CHONK_IP}" -P "${RCON_PORT}" -p "${RCON_PASS}" "spark sampler --timeout 60"
    echo "ACTION: Review the Spark link generated in the Chonk console."
fi
