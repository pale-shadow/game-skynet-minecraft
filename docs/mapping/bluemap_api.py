import os
import requests
import json
import mcrcon

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
BLUEMAP_API = f"http://{CHONK_IP}:8100/api/v2/maps/world/markers"

def create_bluemap_marker(marker_id, label, x, y, z, detail="Skynet AI Generated Structure", marker_type="poi"):
    """
    Creates a BlueMap marker via the REST API or RCON fallback.
    """
    payload = {
        "id": marker_id,
        "type": marker_type,
        "label": label,
        "position": {"x": x, "y": y, "z": z},
        "detail": detail
    }
    
    # 1. Attempt REST API (Fastest)
    try:
        response = requests.post(BLUEMAP_API, json=payload, timeout=2)
        if response.status_code in [200, 201, 204]:
            print(f"✅ BlueMap API: Marker '{label}' created successfully.")
            return True
    except Exception as e:
        print(f"⚠️ BlueMap API failed: {e}. Falling back to RCON...")

    # 2. RCON Fallback (Using /bluemap marker command)
    # Note: Command syntax varies by BlueMap version. 
    # v2/v3 often uses /bm-marker or /bluemap marker add
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            # Standard BlueMap marker add command format:
            # /bluemap marker add <id> <label> <world> <x> <y> <z>
            cmd = f"bluemap marker add {marker_id} \"{label}\" world {x} {y} {z}"
            mcr.command(cmd)
            print(f"✅ BlueMap RCON: Marker '{label}' command sent.")
            return True
    except Exception as e:
        print(f"❌ BlueMap RCON Fallback failed: {e}")
    
    return False

if __name__ == "__main__":
    # Test Marker
    create_bluemap_marker("test_marker", "Skynet Test POI", -1200, 70, -700, "Verification of BlueMap Automation.")
