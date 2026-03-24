import os
import time
import random
from skynet_core import Config, SkynetRCON

# Unified RCON Client
rcon = SkynetRCON()

def is_within_bounds(x, z, width=5, depth=5):
    """Safety check: Ensures the entire footprint stays within the AI Field."""
    bounds = Config.FIELD_BOUNDS
    within_x = (bounds["min_x"] <= x and (x + width) <= bounds["max_x"])
    within_z = (bounds["min_z"] <= z and (z + depth) <= bounds["max_z"])
    return within_x and within_z

def push_build_to_chonk(commands):
    """Deploys build commands to the server via standardized RCON client."""
    if not commands:
        return
    rcon.send(commands)

def get_hailo_structure_logic(sector=None, metadata=None):
    """
    Simulates AI 'Void-Tech' generation within the verified desert boundary.
    Uses the 2026 Aesthetic: Polished Tuff, Calcite, and Tinted Glass.
    """
    bounds = Config.FIELD_BOUNDS
    # Pick a random starting point within the field
    x = random.randint(bounds["min_x"], bounds["max_x"] - 6)
    z = random.randint(bounds["min_z"], bounds["max_z"] - 6)
    y = bounds["y_base"]

    if not is_within_bounds(x, z, 6, 6):
        print(f"⚠️ Warning: Inference generated coordinates {x}, {z} out of bounds. Aborting.")
        return []

    # Palette from master_prompt_reference_v2.md
    primary = "minecraft:polished_tuff"
    secondary = "minecraft:calcite"
    glass = "minecraft:tinted_glass"
    light = "minecraft:froglight[variant=pearlescent]"
    
    sector_msg = f" in sector: {sector}" if sector else ""

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
        f"say [Skynet] Void-Tech Uplink Tower deployed at {x} {y} {z}{sector_msg} (Boundary Verified)."
    ]

if __name__ == "__main__":
    print(f"📡 Skynet NPU initializing build for Chonk ({Config.CHONK_IP})...")
    structure = get_hailo_structure_logic()
    if structure:
        push_build_to_chonk(structure)
    else:
        print("❌ Process halted: Safety boundary violation.")
