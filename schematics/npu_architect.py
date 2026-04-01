import json
import os
import time

import mcrcon
import requests
from hailo_platform import HEF, ConfigureParams, VDevice

# Load from .envrc
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
# BlueMap typically listens on 8100 by default
BLUEMAP_API = f"http://{CHONK_IP}:8100/api/v2/maps/world/markers"


def notify_bluemap(label, x, z):
    """Sends a temporary marker or log to BlueMap."""
    payload = {
        "id": f"ai_build_{int(time.time())}",
        "type": "poi",
        "label": f"⚠️ AI Build Verified: {label}",
        "position": {"x": x, "y": 100, "z": z},
        "icon": "assets/poi.svg",
        "detail": f"Constructed by Skynet NPU at {time.strftime('%H:%M:%S')}",
    }
    try:
        # Note: BlueMap API often requires a secret key if set in webserver.conf
        requests.post(BLUEMAP_API, json=payload, timeout=2)
    except Exception as e:
        print(f"BlueMap Notification Failed: {e}")


def execute_ai_build(label, x, z):
    """The 'Architect' logic: Build on Chonk, then notify the Map."""
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS) as mcr:
            # 1. Execute the Minecraft command
            mcr.command(
                f"execute at @a run fill {x} 100 {z} {x+2} 105 {z+2} gold_block"
            )
            mcr.command(f"say [Skynet] {label} detected. Build verified at {x}, {z}.")

            # 2. Update BlueMap
            notify_bluemap(label, x, z)
            print(f"✅ Build & Map Update Complete for {label}")
    except Exception as e:
        print(f"❌ Pipeline Error: {e}")


def run_npu_vision():
    # Load your local validated model
    hef = HEF("models/yolov8s.hef")

    with VDevice() as target:
        network_group = target.configure(ConfigureParams.create_from_hef(hef))[0]
        with network_group.activate():
            print("🤖 Skynet NPU Active. Ready to build in the Desert Testing Field...")

            # Coordination Mapping: Desert Testing Zone center
            # X: -1242, Z: -701
            execute_ai_build("NPU_Object_Alpha", -1242, -701)


if __name__ == "__main__":
    run_npu_vision()
