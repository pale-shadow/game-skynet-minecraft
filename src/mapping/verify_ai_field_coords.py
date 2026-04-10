import os
import time

import mcrcon
import requests

# Load from .envrc
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
BLUEMAP_API = f"http://{CHONK_IP}:8100/api/v2/maps/world/markers"

# Coordinates from your Desert Testing Field definition
CORNERS = [
    {"x": -945, "z": -913, "label": "Corner_NW"},
    {"x": -1539, "z": -913, "label": "Corner_SW"},
    {"x": -1539, "z": -489, "label": "Corner_SE"},
    {"x": -945, "z": -489, "label": "Corner_NE"},
]


def verify_boundary_node(corner):
    """Deploys a pillar and a BlueMap marker at a specific boundary vertex."""
    x, z, label = corner["x"], corner["z"], corner["label"]

    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS) as mcr:
            # 1. Physical Build: 5-block Glowstone pillar for visibility
            mcr.command(f"fill {x} 100 {z} {x} 105 {z} glowstone")
            mcr.command(f"say [Skynet] Verifying Boundary Node: {label} at {x}, {z}")

            # 2. BlueMap WebSocket/API Notification
            payload = {
                "id": f"verify_{label}",
                "type": "poi",
                "label": f"Build Verified: {label}",
                "position": {"x": x, "y": 100, "z": z},
                "detail": "NPU-mapped boundary vertex for Desert Testing Field.",
            }
            requests.post(BLUEMAP_API, json=payload, timeout=2)
            print(f"✅ {label} synchronized at {x}, {z}")

    except Exception as e:
        print(f"❌ Failed to verify {label}: {e}")


if __name__ == "__main__":
    print("🚀 Initializing Skynet Boundary Verification...")
    for corner in CORNERS:
        verify_boundary_node(corner)
        time.sleep(1)  # Prevent RCON flood
