import os
import json
from mcrcon import MCRcon
from npu_spatial_engine import NPUSpatialEngine

# Configuration from Technical Ledger
RCON_IP = "127.0.0.1"  # Hub 02 Local Loopback
RCON_PASS = "your_secure_password"
HISTORY_FILE = "data/cleaned_build_history.json"

def deploy_batch():
    # Initialize NPU Engine for spatial inference
    engine = NPUSpatialEngine(hardware_mode="hailo")
    with open(HISTORY_FILE, 'r') as f:
        build_queue = json.load(f)

    with MCRcon(RCON_IP, RCON_PASS) as mcr:
        for build in build_queue:
            # Infer optimal coordinates at the Y:63 baseline
            width, depth = build.get("w", 10), build.get("d", 10)
            x, z = engine.get_optimal_vector(width, depth, preference="void")
            
            if x and z:
                print(f"==> Deploying {build['name']} to {x}, 63, {z}")
                
                # Execute FAWE placement sequence
                mcr.command(f"//schem load {build['schematic_name']}")
                mcr.command(f"//pos1 {x},63,{z}")
                mcr.command("//paste -a")
                
                # Log placement back to the Neural-Data Vault (Hub 07)
                engine.history.append({"name": build['name'], "x": x, "y": 63, "z": z})

    # Update the local history for future inference passes
    with open(HISTORY_FILE, 'w') as f:
        json.dump(engine.history, f, indent=4)

if __name__ == "__main__":
    deploy_batch()
