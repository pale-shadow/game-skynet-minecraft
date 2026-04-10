#!/usr/bin/env bash

# Senior Admin Diagnostic Script v2.1 (Urbanization Phase)
# Purpose: Extract telemetry for Skynet/Stargate infrastructure validation.

set -euo pipefail

echo "--- [Server Environment] ---"
JAR_PATH=$(ps aux | grep -E 'purpur|paper' | grep -v grep | awk '{print $NF}')
if [[ -z "$JAR_PATH" ]]; then
    echo "ERROR: Minecraft process not detected. Is the node offline?"
else
    echo "Detected Jar: $JAR_PATH"
    # Extract version from jar manifest or filename
    java -jar "$JAR_PATH" --version 2>/dev/null || echo "Version: Manual verification required (1.21.x suspected)"
fi

echo -e "\n--- [Resource Allocation] ---"
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_RAM_GB=$(echo "scale=2; $TOTAL_RAM_KB / 1024 / 1024" | bc)

XMX_VAL=$(ps aux | grep -v grep | grep -Po 'Xmx\K[0-9]+[GgMm]')
echo "Current Xmx Allocation: $XMX_VAL"

# OS_Overhead: 1.5GB, NPU/LLM_Buffer: 2GB (Standard for Hailo-8L + Llama-3-8B weights)
OS_OVERHEAD=1.5
NPU_LLM_BUFFER=2.0
IDEAL_XMX=$(echo "scale=2; $TOTAL_RAM_GB - ($OS_OVERHEAD + $NPU_LLM_BUFFER)" | bc)

echo "Node Total RAM: ${TOTAL_RAM_GB}GB"
echo "Calculated Protocol Xmx: ${IDEAL_XMX}GB"

echo -e "\n--- [Hardware Thermals] ---"
if [[ -f "/sys/class/thermal/thermal_zone0/temp" ]]; then
    PI_TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo "Pi 5 CPU Temp: $(echo "scale=1; $PI_TEMP / 1000" | bc)°C"
else
    echo "Pi 5 Thermal Zone: Not Found"
fi

if command -v hailo >/dev/null 2>&1; then
    echo "Hailo-8L NPU Temp: $(hailo monitor | grep -i 'Temperature' | awk '{print $2}')"
else
    echo "Hailo-8L: Tooling not found. Ensure 'hailortcli' is in PATH."
fi

echo -e "\n--- [Performance Protocol] ---"
echo "ACTION REQUIRED: Execute the following RCON command to generate the Spark link:"
echo ">> /spark sampler --timeout 60"
echo "Note: Ensure RCON is protected via SSH Tunnel or Cloudflare Spectrum."
