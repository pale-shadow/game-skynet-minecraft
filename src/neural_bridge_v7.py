import os
import time
import random
import json
import math
import mcrcon
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

def generate_neural_bridge_v7(start_node, end_node):
    """
    Generates a procedural Neural Bridge between two points.
    Features: math.sin sway, v7.1 palette, Hydro-Pods, and Mutation layers.
    """
    cmds = []
    x1, z1 = start_node["x"], start_node["z"]
    x2, z2 = end_node["x"], end_node["z"]
    y_base = FIELD_BOUNDS["y"] + 12 # Elevated deck height

    # Calculate distance and direction
    dx = x2 - x1
    dz = z2 - z1
    dist = math.sqrt(dx**2 + dz**2)
    steps = int(dist)
    
    # Palette v7.1
    p = {
        "base": "minecraft:polished_tuff",
        "plating": "minecraft:chiseled_tuff",
        "panel": "minecraft:calcite",
        "tech": "minecraft:purpur_pillar",
        "window": "minecraft:tinted_glass",
        "glow": "minecraft:pearlescent_froglight",
        "mutation_1": "minecraft:magenta_carpet",
        "mutation_2": "minecraft:cherry_leaves",
        "conduit": "minecraft:end_rod",
        "antenna": "minecraft:lightning_rod",
        "accent": "minecraft:dark_prismarine_stairs"
    }

    print(f"🌉 Constructing Neural Bridge from ({x1}, {z1}) to ({x2}, {z2})...")

    for i in range(steps):
        # Interpolate position
        progress = i / steps
        curr_x = x1 + (dx * progress)
        curr_z = z1 + (dz * progress)
        
        # Apply organic math.sin sway (perpendicular to direction)
        sway = math.sin(progress * math.pi * 3) * 4 # 3 waves, 4 blocks max sway
        
        # Calculate perpendicular vector for sway
        perp_x = -dz / dist
        perp_z = dx / dist
        
        final_x = int(curr_x + perp_x * sway)
        final_z = int(curr_z + perp_z * sway)
        final_y = y_base + int(math.sin(progress * math.pi * 2) * 2) # Slight vertical undulation

        # --- PHASE 1: THE DECK (Tuff & Calcite) ---
        cmds.append(f"fill {final_x-2} {final_y} {final_z-2} {final_x+2} {final_y} {final_z+2} {p['base']}")
        cmds.append(f"setblock {final_x} {final_y} {final_z} {p['panel']}")
        
        # Rail Line
        cmds.append(f"setblock {final_x} {final_y+1} {final_z} minecraft:powered_rail")
        if i % 10 == 0:
            cmds.append(f"setblock {final_x} {final_y-1} {final_z} minecraft:redstone_block")

        # --- PHASE 2: MUTATION LAYER (Randomized) ---
        if random.random() > 0.7:
            mx = final_x + random.randint(-2, 2)
            mz = final_z + random.randint(-2, 2)
            block = p['mutation_1'] if random.random() > 0.5 else p['mutation_2']
            cmds.append(f"setblock {mx} {final_y+1} {mz} {block}")

        # --- PHASE 3: SUSPENSION PYLONS (End Rods / Lightning Rods) ---
        if i % 15 == 0:
            cmds.append(f"fill {final_x} {final_y-1} {final_z} {final_x} {final_y-10} {final_z} {p['antenna']}")
            cmds.append(f"setblock {final_x} {final_y-11} {final_z} {p['glow']}")

        # --- PHASE 4: HYDRO-POD MODULE (Every 20 blocks) ---
        if i > 0 and i % 20 == 0:
            cmds.append(f"fill {final_x-3} {final_y-1} {final_z-3} {final_x+3} {final_y+4} {final_z+3} {p['window']}")
            cmds.append(f"fill {final_x-2} {final_y} {final_z-2} {final_x+2} {final_y+3} {final_z+2} minecraft:air")
            cmds.append(f"setblock {final_x} {final_y+1} {final_z} minecraft:crafter") # Automated Economy Core
            cmds.append(f"setblock {final_x} {final_y+2} {final_z} {p['tech']}")
            cmds.append(f"say [Skynet] Hydro-Pod v7.1 synchronized at {final_x} {final_z}.")

        # --- PHASE 5: SIGNAL CORE SILHOUETTE (Every 50 blocks) ---
        if i > 0 and i % 50 == 0:
            cmds.append(f"fill {final_x-5} {final_y+5} {final_z-5} {final_x+5} {final_y+15} {final_z+5} {p['window']}")
            cmds.append(f"fill {final_x-4} {final_y+6} {final_z-4} {final_x+4} {final_y+14} {final_z+4} minecraft:air")
            cmds.append(f"setblock {final_x} {final_y+10} {final_z} minecraft:beacon")
            cmds.append(f"say [Skynet] Signal Core Data Hub silhouette projected.")

    cmds.append(f"say [Hailo-NPU] Neural Bridge V7.1 link established. Sway vector optimized.")
    return cmds

if __name__ == "__main__":
    history = load_history()
    if len(history) < 2:
        print("❌ Error: Need at least 2 nodes in history to bridge. Run neural_rail_v7_nexus.py first.")
    else:
        # Connect the last two nodes
        start_node = history[-2]
        end_node = history[-1]
        commands = generate_neural_bridge_v7(start_node, end_node)
        push_build_to_chonk(commands)
        save_to_history({
            "start": start_node["label"],
            "end": end_node["label"],
            "type": "Neural_Bridge_V7",
            "timestamp": time.time()
        })
        
        # Deploy BlueMap POI at midpoint
        mid_x = (start_node.get("x", 0) + end_node.get("x", 0)) // 2
        mid_z = (start_node.get("z", 0) + end_node.get("z", 0)) // 2
        marker_id = f"bridge_{int(time.time())}"
        create_bluemap_marker(marker_id, "Neural Bridge V7.1", mid_x, FIELD_BOUNDS["y"] + 15, mid_z, 
                             detail=f"Automated Rail Link connecting {start_node.get('label', 'Node')} and {end_node.get('label', 'Node')}.")
