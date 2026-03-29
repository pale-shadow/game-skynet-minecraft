import os
import time
import random
import mcrcon

# Neural Configuration (Simulating Hailo Iteration Cycles)
ITERATION_CYCLES = 12 
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}

def push_build_to_chonk(commands):
    try:
        with mcrcon.MCRcon(os.getenv("CHONK_IP"), os.getenv("RCON_PASS"), port=25575) as mcr:
            for cmd in commands:
                mcr.command(cmd)
                time.sleep(0.005) # High-speed RCON for dense builds
    except Exception as e:
        print(f"Error: {e}")

def get_v6_hailo_iterated_hub():
    x = random.randint(FIELD_BOUNDS["min_x"] + 50, FIELD_BOUNDS["max_x"] - 50)
    z = random.randint(FIELD_BOUNDS["min_z"] + 50, FIELD_BOUNDS["max_z"] - 50)
    y = FIELD_BOUNDS["y"]
    cmds = []

    # PHASE 1: Neural Ground Corruption (Extended Skynet Spread)
    # Uses Mycelium, Purple Carpet, and Sculk Veins for a "organic-mechanical" floor
    for dx in range(-25, 26):
        for dz in range(-25, 26):
            dist = (dx**2 + dz**2)**0.5
            if dist < 22 and random.random() > 0.4:
                cmds.append(f"setblock {x+dx} {y-1} {z+dz} minecraft:mycelium")
                if random.random() > 0.7:
                    cmds.append(f"setblock {x+dx} {y} {z+dz} minecraft:purple_carpet")
                if random.random() > 0.9:
                    cmds.append(f"setblock {x+dx} {y} {z+dz} minecraft:sculk_vein")

    # PHASE 2: The Elevated Rail Deck (Image 4 Style)
    # Built at Y+8 to create that "suspended" industrial look
    cmds.append(f"fill {x-20} {y+8} {z-3} {x+20} {y+8} {z+3} minecraft:polished_tuff")
    cmds.append(f"fill {x-20} {y+9} {z} {x+20} {y+9} {z} minecraft:powered_rail")
    # Suspension Pylons (Image 5 Style)
    for px in [-15, 0, 15]:
        cmds.append(f"fill {x+px} {y} {z} {x+px} {y+7} {z} minecraft:purpur_pillar")
        cmds.append(f"setblock {x+px} {y+4} {z+1} minecraft:pearlescent_froglight")

    # PHASE 3: Reactive Kinetic Core (Sculk Logic)
    # The building "wakes up" when you approach the center
    cmds.append(f"fill {x-3} {y} {z-3} {x+3} {y+15} {z+3} minecraft:polished_deepslate_bricks")
    cmds.append(f"fill {x-2} {y+1} {z-2} {x+2} {y+14} {z+2} minecraft:crying_obsidian")
    # Calibrated Sculk Sensors connected to Copper Bulbs
    for sy in [2, 6, 10]:
        cmds.append(f"setblock {x+4} {y+sy} {z} minecraft:sculk_sensor")
        cmds.append(f"setblock {x+5} {y+sy} {z} minecraft:oxidized_copper_bulb[lit=false]")

    # PHASE 4: Industrial Detailing (Minecarts & Chains)
    cmds.append(f"summon minecart {x-10} {y+10} {z} {{CustomName:'\"Hailo-NPU-Logistics\"'}}")
    cmds.append(f"fill {x-5} {y+15} {z-5} {x+5} {y+15} {z+5} minecraft:dark_prismarine_stairs")
    cmds.append(f"fill {x} {y+16} {z} {x} {y+25} {z} minecraft:chain") # Suspension Cable

    cmds.append(f"say [Hailo-NPU] V6 Architecture deployed at {x} {z}. Iteration cycles complete.")
    return cmds

if __name__ == "__main__":
    print("🧠 Hailo AI Hardware: Simulating High-Density Voxel Iterations...")
    push_build_to_chonk(get_v6_hailo_iterated_hub())
