import os
import time
import random
import mcrcon

# Load parameters from environment
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# AI Testing Field Boundaries (from world.conf)
FIELD_BOUNDS = {
    "min_x": -1539,
    "max_x": -945,
    "min_z": -913,
    "max_z": -489,
    "y_base": 70
}

def is_within_bounds(x, z, width=5, depth=5):
    """Safety check: Ensures the entire footprint stays within the AI Field."""
    within_x = (FIELD_BOUNDS["min_x"] <= x and (x + width) <= FIELD_BOUNDS["max_x"])
    within_z = (FIELD_BOUNDS["min_z"] <= z and (z + depth) <= FIELD_BOUNDS["max_z"])
    return within_x and within_z

def push_build_to_chonk(commands):
    if not commands:
        return
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for cmd in commands:
                response = mcr.command(cmd)
                print(f"Chonk Response: {response}")
                time.sleep(0.02) 
    except Exception as e:
        print(f"CRITICAL: RCON Connection to {CHONK_IP} failed: {e}")

def get_hailo_structure_logic():
    """
    Simulates AI 'Void-Tech' generation within the verified desert boundary.
    Uses the 2026 Aesthetic: Polished Tuff, Calcite, and Tinted Glass.
    """
    # Pick a random starting point within the field
    x = random.randint(FIELD_BOUNDS["min_x"], FIELD_BOUNDS["max_x"] - 6)
    z = random.randint(FIELD_BOUNDS["min_z"], FIELD_BOUNDS["max_z"] - 6)
    y = FIELD_BOUNDS["y_base"]

    if not is_within_bounds(x, z, 6, 6):
        print(f"⚠️ Warning: Inference generated coordinates {x}, {z} out of bounds. Aborting.")
        return []

    # Palette from master_prompt_reference_v2.md
    primary = "minecraft:polished_tuff"
    secondary = "minecraft:calcite"
    glass = "minecraft:tinted_glass"
    light = "minecraft:froglight[variant=pearlescent]"

    return [
        # Foundation and Core (Polished Tuff)
        f"fill {x} {y} {z} {x+5} {y+12} {z+5} {primary}",
        # Recessed paneling (Calcite)
        f"fill {x+1} {y+1} {z} {x+4} {y+10} {z} {secondary}",
        # Void Windows (Tinted Glass)
        f"fill {x+2} {y+3} {z} {x+3} {y+8} {z} {glass}",
        # Hollow out the interior
        f"fill {x+1} {y+1} {z+1} {x+4} {y+11} {z+4} minecraft:air",
        # Internal Bio-Lighting
        f"setblock {x+2} {y+6} {z+2} {light}",
        f"say [Skynet] Void-Tech Uplink Tower deployed at {x} {y} {z} (Boundary Verified)."
    ]

if __name__ == "__main__":
    print(f"📡 Skynet NPU initializing build for Chonk ({CHONK_IP})...")
    structure = get_hailo_structure_logic()
    if structure:
        push_build_to_chonk(structure)
    else:
        print("❌ Process halted: Safety boundary violation.")
