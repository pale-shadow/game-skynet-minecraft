import os
import random
import time

import mcrcon

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# Boundaries (Desert Research Field)
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 70}


def push_build_to_chonk(commands):
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for cmd in commands:
                mcr.command(cmd)
                time.sleep(0.01)  # Sustained RCON throughput
    except Exception as e:
        print(f"CRITICAL: RCON Connection failed: {e}")


def get_void_tech_hub_logic():
    """
    V4 ARCHITECT: Logistics Hub
    Features: 30x30 footprint, suspended rails, crying obsidian accents.
    """
    # Boundary-safe random placement for 30x30 footprint
    x = random.randint(FIELD_BOUNDS["min_x"] + 30, FIELD_BOUNDS["max_x"] - 30)
    z = random.randint(FIELD_BOUNDS["min_z"] + 30, FIELD_BOUNDS["max_z"] - 30)
    y = FIELD_BOUNDS["y"]

    p = {
        "base": "minecraft:polished_deepslate",
        "wall": "minecraft:polished_tuff",
        "energy": "minecraft:crying_obsidian",
        "rail_support": "minecraft:dark_prismarine_stairs",
        "trim": "minecraft:purpur_pillar",
        "glow": "minecraft:pearlescent_froglight",
        "detail": "minecraft:amethyst_block",
    }

    commands = [
        # --- PHASE 1: MASSIVE FOUNDATION & DRAINAGE ---
        f"fill {x-12} {y-1} {z-12} {x+12} {y-1} {z+12} {p['base']}",
        f"fill {x-11} {y} {z-11} {x+11} {y} {z+11} minecraft:polished_andesite_slab",
        # --- PHASE 2: INTEGRATED RAILWAY PLATFORM (Image 4/5 Style) ---
        # Elevated rail line cutting through the hub
        f"fill {x-15} {y+4} {z-2} {x+15} {y+4} {z+2} {p['rail_support']}",
        f"fill {x-15} {y+5} {z} {x+15} {y+5} {z} minecraft:powered_rail",
        f"setblock {x} {y+4} {z} minecraft:redstone_block",  # Power the rail
        f"summon minecart {x} {y+6} {z} {{CustomName:'\"Skynet Logistics\"'}}",
        # --- PHASE 3: SUSPENDED GEOMETRY (The "Floating" Look) ---
        # Large Crying Obsidian pillars with chains (Image 3 style)
        f"fill {x-8} {y} {z-8} {x-8} {y+12} {z-8} {p['energy']}",
        f"fill {x-8} {y+13} {z-8} {x-8} {y+18} {z-8} minecraft:chain",
        f"fill {x+8} {y} {z+8} {x+8} {y+12} {z+8} {p['energy']}",
        f"fill {x+8} {y+13} {z+8} {x+8} {y+18} {z+8} minecraft:chain",
        # --- PHASE 4: VOID RADIATORS (Detailed detailing) ---
        f"fill {x-3} {y+1} {z-3} {x+3} {y+6} {z+3} {p['wall']}",
        f"fill {x-2} {y+2} {z-4} {x+2} {y+5} {z-4} {p['detail']}",  # Amethyst Core
        f"setblock {x} {y+3} {z-5} {p['glow']}",  # Central Hub Light
        # --- PHASE 5: ATMOSPHERIC PIPING ---
        f"fill {x-10} {y+10} {z-10} {x+10} {y+10} {z-10} minecraft:lightning_rod[facing=east]",
        f"say [Skynet] V4 Logistics Hub Online at {x} {y} {z}. Rail link established.",
    ]
    return commands


if __name__ == "__main__":
    print(f"📡 Skynet NPU: Generating V4 High-Density Infrastructure...")
    structure = get_void_tech_hub_logic()
    push_build_to_chonk(structure)
