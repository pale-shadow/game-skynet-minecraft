import argparse
import json
import os
import sys
import time

import mcschematic # Added import for mcschematic
from src.schematics.npu_spatial_engine import NPUSpatialEngine # Corrected import path
from src.schematics.skynet_core import Config # Corrected import path

# Configuration from Technical Ledger
# Use Config.HISTORY_FILE which should now resolve correctly to the project root
# e.g., '/home/franklin/workspace/gaming/game-skynet-minecraft/input/build_history.json'
HISTORY_FILE = Config.HISTORY_FILE

def deploy_batch():
    """Deploys schematics based on build history."""
    print(f"Using history file: {HISTORY_FILE}")
    
    # Initialize NPU Engine for spatial inference
    try:
        engine = NPUSpatialEngine()
    except Exception as e:
        print(f"Error initializing NPUSpatialEngine: {e}")
        return

    if not os.path.exists(HISTORY_FILE):
        print(f"Error: Build history file not found at {HISTORY_FILE}")
        return

    try:
        with open(HISTORY_FILE, 'r') as f:
            build_queue = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {HISTORY_FILE}")
        return
    except Exception as e:
        print(f"Error reading build history file: {e}")
        return

    if not build_queue:
        print("No builds found in the history file. Nothing to deploy.")
        return

    # Use RCON_PASS and RCON_PORT from Config if available, otherwise use environment variables
    rcon_pass = os.environ.get("RCON_PASS", Config.RCON_PASS) # Fallback to Config if env var not set
    rcon_ip = Config.CHONK_IP
    rcon_port = Config.RCON_PORT

    if not rcon_pass:
        print("Error: RCON_PASS is not set. Please set the environment variable or ensure Config.RCON_PASS is valid.")
        return

    try:
        with MCRcon(rcon_ip, rcon_pass, port=rcon_port) as mcr:
            for build in build_queue:
                # Infer optimal coordinates at the Y:63 baseline
                width, depth = build.get("w", 10), build.get("d", 10)
                x, z = engine.get_optimal_vector(width, depth, preference="void")
                
                if x is not None and z is not None:
                    print(f"==> Deploying {build.get('name', 'Unnamed Build')} to {x}, 63, {z}")
                    
                    # Execute FAWE placement sequence
                    # Ensure schematic_name is correct and exists in the server's schematics directory
                    schematic_name = build.get('schematic_name')
                    if not schematic_name:
                        print(f"Skipping {build.get('name', 'Unnamed Build')}: Missing 'schematic_name'.")
                        continue

                    mcr.command(f"//schem load {schematic_name}")
                    mcr.command(f"//pos1 {x},63,{z}")
                    mcr.command("//paste -a")
                    
                    # Log placement back to the Neural-Data Vault (Hub 07)
                    # Note: This assumes engine.history is the correct place to append.
                    # If build_history.json is read-only or meant to be historical, this might need adjustment.
                    # For now, assume it's for tracking deployed items.
                    engine.history.append({"name": build['name'], "x": x, "y": 63, "z": z})
                else:
                    print(f"Skipping {build.get('name', 'Unnamed Build')}: No optimal vector found.")

        # Update the local history for future inference passes
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(engine.history, f, indent=4)
            print("Build history updated.")
        except Exception as e:
            print(f"Error writing updated build history: {e}")

    except Exception as e:
        print(f"Error during RCON communication: {e}")

if __name__ == "__main__":
    deploy_batch()
