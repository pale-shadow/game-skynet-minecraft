import os
import time
import random
import json
import math
import mcrcon
from neural_pathfinder import NeuralPathfinder
from bluemap_api import create_bluemap_marker

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# AI Testing Field Boundaries
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}
HISTORY_FILE = "build_history.json"

def push_build_to_chonk(commands):
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for cmd in commands:
                mcr.command(cmd)
                time.sleep(0.005) # Optimized for Hailo-8L throughput
    except Exception as e:
        print(f"CRITICAL: RCON Connection failed: {e}")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_to_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def generate_v8_pathfinded_bridge(path):
    """
    Generates bridge commands following the path provided by NeuralPathfinder.
    """
    cmds = []
    y_base = FIELD_BOUNDS["y"] + 12 # Elevated deck height
    
    # Palette v7.1
    p = {
        "base": "minecraft:polished_tuff",
        "plating": "minecraft:chiseled_tuff",
        "panel": "minecraft:calcite",
        "glow": "minecraft:pearlescent_froglight",
        "mutation": "minecraft:magenta_carpet"
    }

    print(f"🌉 Constructing Intelligent Neural Bridge...")

    for i, node in enumerate(path):
        final_x, final_z = node
        
        # --- PHASE 1: THE DECK ---
        cmds.append(f"fill {final_x-2} {y_base} {final_z-2} {final_x+2} {y_base} {final_z+2} {p['base']}")
        cmds.append(f"setblock {final_x} {y_base} {final_z} {p['panel']}")
        
        # Rail Line
        cmds.append(f"setblock {final_x} {y_base+1} {final_z} minecraft:powered_rail")
        if i % 10 == 0:
            cmds.append(f"setblock {final_x} {y_base-1} {final_z} minecraft:redstone_block")

        # Suspension Pylons (Thin)
        if i % 20 == 0:
            cmds.append(f"fill {final_x} {y_base-1} {final_z} {final_x} {y_base-10} {final_z} minecraft:end_rod")
            cmds.append(f"setblock {final_x} {y_base-11} {final_z} {p['glow']}")

    cmds.append(f"say [Hailo-NPU] V8 Neural Pathfinder Bridge link established. Path Optimized.")
    return cmds

if __name__ == "__main__":
    history = load_history()
    if len(history) < 2:
        print("❌ Error: Need at least 2 nodes in history to bridge.")
    else:
        start_node = history[-2]
        end_node = history[-1]
        
        pathfinder = NeuralPathfinder()
        start_coords = (start_node["x"], start_node["z"])
        end_coords = (end_node["x"], end_node["z"])
        
        print(f"🧠 Calculating path from {start_node['label']} to {end_node['label']}...")
        path = pathfinder.get_path(start_coords, end_coords)
        
        if path:
            commands = generate_v8_pathfinded_bridge(path)
            push_build_to_chonk(commands)
            
            # Save to history
            save_to_history({
                "start": start_node["label"],
                "end": end_node["label"],
                "type": "Neural_Bridge_V8_Pathfinded",
                "timestamp": time.time()
            })
            
            # Midpoint marker
            mid_node = path[len(path)//2]
            create_bluemap_marker(f"bridge_v8_{int(time.time())}", "Neural Pathfinded Bridge", 
                                 mid_node[0], FIELD_BOUNDS["y"] + 15, mid_node[1], 
                                 detail="Bridge path dynamically calculated by NPU to avoid obstacles.")
        else:
            print("❌ Pathfinding Failed: Target node is unreachable.")
