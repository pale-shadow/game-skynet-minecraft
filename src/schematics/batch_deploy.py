import argparse
import json
import os
import sys
import time
import mcschematic # Added import for mcschematic
from config_utils import Config
from npu_spatial_engine import NPUSpatialEngine

# Import MCRcon if it's an external library; otherwise, it might need mocking.
# Assuming MCRcon is an external library for RCON communication.
try:
    from mcrcon import MCRcon
except ImportError:
    # Mock MCRcon if the library is not available
    class MCRcon:
        def __init__(self, host, password, port=25575):
            self.host = host
            self.password = password
            self.port = port
            print(f"Mock MCRcon initialized for {host}:{port}")
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def command(self, cmd):
            print(f"Mock RCON command: {cmd}")
            return "(Mock response)"

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

    # Use RCON_PASS and RCON_PORT from Config, Chonk IP is also needed
    rcon_pass = os.environ.get("RCON_PASS", Config.RCON_PASS)
    rcon_ip = Config.CHONK_IP # This needs to be defined in Config
    rcon_port = Config.RCON_PORT

    if not rcon_pass:
        print("Error: RCON_PASS is not set. Please set the environment variable or ensure Config.RCON_PASS is valid.")
        return

    try:
        # The schematic loading path needs to be correct for the RCON commands
        # Assuming schematics are accessible via RCON commands from the server's perspective
        schematic_base_path = "/mnt/clusterfs/minecraft/schematics" # User specified path

        with MCRcon(rcon_ip, rcon_pass, port=rcon_port) as mcr:
            for build in build_queue:
                # Infer optimal coordinates at the Y:63 baseline
                # Use origin from JSON if available and valid, otherwise infer
                x, y, z = None, 63, None # Default y to 63 if not specified in JSON
                width, depth = build.get("w", 10), build.get("d", 10) # Default dimensions

                if "x" in build and "z" in build:
                    x, z = build["x"], build["z"]
                    # Use provided Y if available and not 0
                    if "y" in build and build["y"] != 0:
                        y = build["y"]
                    # Update width and depth if specified in JSON and non-zero
                    if "w" in build and build["w"] != 0:
                        width = build["w"]
                    if "d" in build and build["d"] != 0:
                        depth = build["d"]
                else:
                    # Fallback to inferring location if origin is not in history
                    x, z = engine.get_optimal_vector(width, depth, preference="void")

                if x is not None and z is not None:
                    print(f"==> Deploying {build.get('name', 'Unnamed Build')} to {x}, {y}, {z}")
                    
                    # Execute FAWE placement sequence
                    schematic_name = build.get('schematic_name')
                    if not schematic_name:
                        print(f"Skipping {build.get('name', 'Unnamed Build')}: Missing 'schematic_name'.")
                        continue

                    # Construct the full path for schem load command
                    # Assumes schematic_name is just the filename and path is server-side
                    schem_load_path = f"{schematic_base_path}/{schematic_name}" 
                    
                    mcr.command(f"//schem load {schem_load_path}")
                    mcr.command(f"//pos1 {x},{y},{z}")
                    mcr.command("//paste -a")
                    
                    # Log placement back to the Neural-Data Vault (Hub 07)
                    # This part might need adjustment based on how 'engine.history' is intended to be used.
                    # Assuming it's for tracking deployed items for future inference.
                    engine.history.append({"name": build['name'], "x": x, "y": y, "z": z})
                else:
                    print(f"Skipping {build.get('name', 'Unnamed Build')}: Could not determine placement coordinates.")

        # Update the local history for future inference passes
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(engine.history, f, indent=4)
            print("Build history updated.")
        except Exception as e:
            print(f"Error writing updated build history: {e}")

    except Exception as e:
        print(f"Error during RCON communication or deployment: {e}")

if __name__ == "__main__":
    deploy_batch()
