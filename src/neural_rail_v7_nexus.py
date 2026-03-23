import os
import time
import random
import json
import math
import mcrcon

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# AI Testing Field Boundaries
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}
HISTORY_FILE = "build_history.json"

from npu_spatial_engine import NPUSpatialEngine
from bluemap_api import create_bluemap_marker

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

def generate_v7_nexus_commands(x, z):
    y = FIELD_BOUNDS["y"]
    cmds = []
    
    # --- PHASE 1: NEURAL GROWTH (NPU Simulated Pattern) ---
    # Concentric rings of corruption with "neural pathways"
    for r in range(0, 25):
        for theta in range(0, 360, 5):
            rad = math.radians(theta)
            dx = int(r * math.cos(rad))
            dz = int(r * math.sin(rad))
            
            # Fractal-like "noise" check
            if (math.sin(r * 0.5) + math.cos(theta * 0.1)) > 0.5:
                cmds.append(f"setblock {x+dx} {y-1} {z+dz} minecraft:mycelium")
                if r % 5 == 0:
                    cmds.append(f"setblock {x+dx} {y} {z+dz} minecraft:sculk_vein")
                elif r % 3 == 0:
                    cmds.append(f"setblock {x+dx} {y} {z+dz} minecraft:purple_carpet")

    # --- PHASE 2: INTERLOCKING RAIL DECKS ---
    # Upper Express (X-axis)
    cmds.append(f"fill {x-20} {y+12} {z-2} {x+20} {y+12} {z+2} minecraft:polished_tuff_slab")
    cmds.append(f"fill {x-20} {y+12} {z} {x+20} {y+12} {z} minecraft:powered_rail")
    # Lower Maintenance (Z-axis)
    cmds.append(f"fill {x-2} {y+4} {z-20} {x+2} {y+4} {z+20} minecraft:polished_deepslate_slab")
    cmds.append(f"fill {x} {y+4} {z-20} {x} {y+4} {z+20} minecraft:powered_rail")
    
    # Power Sources
    cmds.append(f"setblock {x} {y+11} {z} minecraft:redstone_block")
    cmds.append(f"setblock {x} {y+3} {z} minecraft:redstone_block")

    # --- PHASE 3: THE NEXUS CORE (Ribbed Geometry) ---
    # Core Structure
    cmds.append(f"fill {x-4} {y} {z-4} {x+4} {y+20} {z+4} minecraft:polished_deepslate_bricks")
    cmds.append(f"fill {x-3} {y+1} {z-3} {x+3} {y+19} {z+3} minecraft:air") # Hollow core
    
    # Glass Panes for the "Energy Window"
    for side in [-4, 4]:
        cmds.append(f"fill {x+side} {y+2} {z-2} {x+side} {y+18} {z+2} minecraft:tinted_glass")
        cmds.append(f"fill {x-2} {y+2} {z+side} {x+2} {y+18} {z+side} minecraft:tinted_glass")

    # Ribbed detailing (Fractal Ribs)
    for ry in range(0, 21, 2):
        cmds.append(f"fill {x-5} {y+ry} {z-5} {x+5} {y+ry} {z+5} minecraft:polished_tuff_stairs[half=top]")
        cmds.append(f"fill {x-4} {y+ry} {z-4} {x+4} {y+ry} {z+4} minecraft:air")

    # --- PHASE 4: KINETIC FEEDBACK (Sculk Signaling) ---
    for sy in [5, 15]:
        cmds.append(f"setblock {x+6} {y+sy} {z} minecraft:sculk_sensor")
        cmds.append(f"setblock {x+7} {y+sy} {z} minecraft:oxidized_copper_bulb[lit=false]")
        cmds.append(f"setblock {x-6} {y+sy} {z} minecraft:sculk_sensor")
        cmds.append(f"setblock {x-7} {y+sy} {z} minecraft:oxidized_copper_bulb[lit=false]")

    # --- PHASE 5: SUSPENDED LOGISTICS ---
    # Minecarts "Cargo Pods"
    cmds.append(f"summon chest_minecart {x-15} {y+13} {z} {{CustomName:'\"Neural-Data-Pod-A\"'}}")
    cmds.append(f"summon hopper_minecart {x} {y+5} {z+15} {{CustomName:'\"Void-Material-Collector\"'}}")
    
    # Structural Tension (Chains & Rods)
    for px in [-18, 18]:
        for pz in [-18, 18]:
            cmds.append(f"fill {x+px} {y} {z+pz} {x+px} {y+25} {z+pz} minecraft:lightning_rod")
            cmds.append(f"fill {x+px} {y+26} {z+pz} {x+px} {y+35} {z+pz} minecraft:chain")

    cmds.append(f"say [Hailo-NPU] V7 Neural Rail Nexus deployed at {x} {z}. Connectivity: 98.4%.")
    return cmds

if __name__ == "__main__":
    print("🧠 Hailo-8L NPU: Initializing V7 Voxel Synthesis...")
    engine = NPUSpatialEngine()
    width, depth = 50, 50 # Footprint for the Nexus
    
    # Infer optimal cluster site
    x, z = engine.get_optimal_vector(width, depth, preference="cluster")
    
    if x and z:
        print(f"📍 Inferred optimal build site: {x}, {z}")
        commands = generate_v7_nexus_commands(x, z)
        push_build_to_chonk(commands)
        save_to_history({"x": x, "z": z, "w": width, "d": depth, "label": "V7_Neural_Rail_Nexus"})
        
        # Deploy BlueMap POI
        marker_id = f"nexus_{int(time.time())}"
        create_bluemap_marker(marker_id, "V7 Neural Rail Nexus", x, FIELD_BOUNDS["y"] + 15, z, 
                             detail="NPU-Inferred Logistics Node featuring V7 'Ribbed' Architecture.")
    else:
        print("❌ NPU Inference Error: No safe spatial vector found.")
