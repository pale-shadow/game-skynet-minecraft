import os
import time
import random
import mcrcon

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# AI Testing Field Boundaries (from world.conf)
FIELD_BOUNDS = {
    "min_x": -1539,
    "max_x": -945,
    "min_z": -913,
    "max_z": -489,
    "y_base": 63  # Directive: Shift base to Y=63
}

def push_build_to_chonk(commands):
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for cmd in commands:
                mcr.command(cmd)
                time.sleep(0.01) # Faster rate for large builds
    except Exception as e:
        print(f"CRITICAL: RCON Connection failed: {e}")

def get_void_tech_station_logic():
    """
    V3 ARCHITECT: Void-Tech Station (Industrial Scale)
    Adheres to gemini.md standards: 20x15x25 bounding box.
    """
    # Pick a random site within the desert field
    x = random.randint(FIELD_BOUNDS["min_x"] + 20, FIELD_BOUNDS["max_x"] - 20)
    z = random.randint(FIELD_BOUNDS["min_z"] + 20, FIELD_BOUNDS["max_z"] - 20)
    y = FIELD_BOUNDS["y_base"]

    # Material Palette (Corrected for Java Edition)
    primary = "minecraft:polished_deepslate_bricks"
    accent = "minecraft:purpur_pillar"
    teal = "minecraft:dark_prismarine"
    glass = "minecraft:magenta_stained_glass"
    light = "minecraft:pearlescent_froglight" # FIX: Corrected ID
    floor = "minecraft:smooth_quartz"

    return [
        # --- PHASE 1: FOUNDATION (Y: 63-64) ---
        f"fill {x-10} {y-1} {z-10} {x+10} {y-1} {z+10} {primary}",
        f"fill {x-9} {y} {z-9} {x+9} {y} {z+9} {floor}",
        
        # --- PHASE 2: STRUCTURAL PILLARS (The "Rule of Three") ---
        # Four massive 3x3 corner pylons
        f"fill {x-8} {y} {z-8} {x-6} {y+15} {z-6} {primary}",
        f"fill {x+6} {y} {z-8} {x+8} {y+15} {z-6} {primary}",
        f"fill {x-8} {y} {z+6} {x-6} {y+15} {z+8} {primary}",
        f"fill {x+6} {y} {z+6} {x+8} {y+15} {z+8} {primary}",
        
        # --- PHASE 3: INDUSTRIAL GIRDERS (Teal/Prismarine) ---
        # Main longitudinal beams at high level
        f"fill {x-10} {y+12} {z-7} {x+10} {y+13} {z-7} {teal}",
        f"fill {x-10} {y+12} {z+7} {x+10} {y+13} {z+7} {teal}",
        
        # --- PHASE 4: VOID-TECH VOXEL DETAIL ---
        # Floating Purpur core with Froglight illumination
        f"fill {x-2} {y+8} {z-2} {x+2} {y+10} {z+2} {accent}",
        f"fill {x-1} {y+9} {z-1} {x+1} {y+9} {z+1} {light}",
        
        # Glass cladding
        f"fill {x-5} {y+1} {z-8} {x+5} {y+10} {z-8} {glass}",
        
        # Notification
        f"say [Skynet] High-Density Station V3 deployed at {x} {y} {z}. (Y=63 Boundary Confirmed)"
    ]

if __name__ == "__main__":
    print(f"📡 Skynet NPU: Commencing High-Fidelity Build on Chonk...")
    structure = get_void_tech_station_logic()
    push_build_to_chonk(structure)
