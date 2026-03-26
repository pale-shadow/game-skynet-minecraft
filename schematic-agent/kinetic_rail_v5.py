import os
import time
import random
import mcrcon
from npu_spatial_engine import NPUSpatialEngine
from bluemap_api import create_bluemap_marker

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}

def push_build_to_chonk(commands):
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for cmd in commands:
                mcr.command(cmd)
                time.sleep(0.01)
    except Exception as e:
        print(f"CRITICAL: RCON Connection failed: {e}")

def get_v5_kinetic_terminal():
    # Site selection using NPU Engine
    engine = NPUSpatialEngine()
    width, depth = 35, 35
    x, z = engine.get_optimal_vector(width, depth, preference="void")
    
    if not x:
        print("❌ NPU Inference Error: No safe spatial vector found.")
        return []

    y = FIELD_BOUNDS["y"]
    commands = []

    # 1. SKYNET SPREAD: Ground Corruption (5-block radius)
    # Replaces desert sand with Mycelium, Purple Carpet and Sculk Veins
    for dx in range(-15, 16):
        for dz in range(-15, 16):
            if random.random() > 0.7:
                commands.append(f"setblock {x+dx} {y-1} {z+dz} minecraft:mycelium")
                if random.random() > 0.5:
                    commands.append(f"setblock {x+dx} {y} {z+dz} minecraft:purple_carpet")
                if random.random() > 0.8:
                    commands.append(f"setblock {x+dx} {y} {z+dz} minecraft:sculk_vein")

    # 2. THE RAIL DECK
    commands.append(f"fill {x-12} {y+4} {z-4} {x+12} {y+4} {z+4} minecraft:polished_tuff")
    commands.append(f"fill {x-12} {y+5} {z-1} {x+12} {y+5} {z+1} minecraft:chiseled_tuff") # Upgraded Track Bed
    commands.append(f"fill {x-12} {y+6} {z} {x+12} {y+6} {z} minecraft:powered_rail")
    commands.append(f"setblock {x} {y+4} {z} minecraft:redstone_block") # Rail Power

    # 3. KINETIC ENERGY CORE (Image 3 Style)
    # A central column of Amethyst and Crying Obsidian
    commands.append(f"fill {x-2} {y} {z-2} {x+2} {y+12} {z+2} minecraft:crying_obsidian")
    commands.append(f"fill {x-1} {y+1} {z-1} {x+1} {y+11} {z+1} minecraft:amethyst_block")
    
    # REACTIVE SENSORS: Places sculk sensors that trigger Copper Bulbs
    commands.append(f"setblock {x+3} {y+5} {z} minecraft:sculk_sensor")
    commands.append(f"setblock {x+4} {y+5} {z} minecraft:oxidized_copper_bulb[lit=false]")
    commands.append(f"setblock {x-3} {y+5} {z} minecraft:sculk_sensor")
    commands.append(f"setblock {x-4} {y+5} {z} minecraft:oxidized_copper_bulb[lit=false]")

    # 4. INDUSTRIAL VERTICALITY (Image 5 Style)
    # Suspended lightning rod "antennae" and fluted Purpur pillars
    for px, pz in [(-10, -10), (10, -10), (-10, 10), (10, 10)]:
        commands.append(f"fill {px+x} {y} {pz+z} {px+x} {y+15} {pz+z} minecraft:purpur_pillar")
        commands.append(f"setblock {px+x} {y+16} {pz+z} minecraft:lightning_rod")

    # 5. MINE CART DEPLOYMENT
    commands.append(f"summon minecart {x+5} {y+7} {z} {{CustomName:'\"Skynet-V5-Express\"'}}")

    commands.append(f"say [Skynet] V5 Kinetic Terminal Online. Reaction field active at {x} {z}.")
    
    # BlueMap POI
    create_bluemap_marker(f"kinetic_{int(time.time())}", "V5 Kinetic Terminal", x, y + 10, z, 
                         detail="Skynet-V5 Architecture featuring reactive sculk cores.")
    
    return commands

if __name__ == "__main__":
    print("📡 Skynet NPU: Initiating V5 Kinetic Build (Industrial Scaling)...")
    push_build_to_chonk(get_v5_kinetic_terminal())
