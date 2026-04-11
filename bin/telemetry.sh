#!/usr/bin/env bash
# Senior Admin Distributed Telemetry v2.2
# Target: Node Chonk (Main Server) + Node Skynet (Pi 5/Hailo HAT)

set -euo pipefail

# --- CONFIGURATION ---
CHONK_USER="minecraft"
CHONK_HOST="chonk" # Ensure SSH keys are exchanged
SKYNET_CORE="/home/skynet/bin"

echo "--- [NODE CHONK: Minecraft Core Audit] ---"
ssh "${CHONK_USER}@${CHONK_HOST}" << 'EOF'
    # Environment Check
    JAR=$(ps aux | grep -E 'purpur|paper' | grep -v grep | awk '{print $NF}')
    echo "Detected Process: $JAR"
    
    # Memory Audit per Protocol
    TOTAL_RAM_GB=$(echo "scale=2; $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024" | bc)
    XMX=$(ps aux | grep -v grep | grep -Po 'Xmx\K[0-9]+[GgMm]')
    
    echo "Host Total RAM: ${TOTAL_RAM_GB}GB"
    echo "Current Xmx: $XMX"
    
    # Spark Trigger
    echo "ACTION: Execute '/spark sampler --timeout 60' in-game for the profile link."
EOF

echo -e "\n--- [NODE SKYNET: AI Hardware Audit] ---"
# Pi 5 Thermal Probe
if [[ -f "/sys/class/thermal/thermal_zone0/temp" ]]; then
    PI_TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo "Pi 5 CPU Temp: $(echo "scale=1; $PI_TEMP / 1000" | bc)°C"
fi

# Hailo-8L NPU Thermal Probe (Direct from hat)
if command -v hailortcli >/dev/null 2>&1; then
    echo -n "Hailo-8L NPU Status: "
    hailortcli monitor | grep "Temperature" || echo "NPU Idle/No Thermal Data"
else
    echo "ALERT: hailortcli not found. Ensure the NPU driver is active."
fi
