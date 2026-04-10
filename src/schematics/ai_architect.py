import json
import os
import random
import time

import mcrcon

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
HISTORY_FILE = "build_history.json"

# Boundaries from world.conf
# Directive: Anchor new builds at Y=63
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}

# Palette based on the "Station Reference" (image_4.png)
PALETTE = {
    "primary": "polished_deepslate_bricks",
    "pillar": "purpur_pillar",
    "accent": "purpur_block",
    "teal": "dark_prismarine",
    "floor": "magenta_carpet",
    "light": "sea_lantern",
}


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    # Seed with the tower from image_2.png for spatial registry
    return [{"x": -1147, "z": -621, "w": 3, "d": 3, "label": "Initial_Stone_Tower"}]


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def check_collision(x, z, w, d, history):
    padding = 2  # Directive: Larger spacing between high-density builds
    for b in history:
        if not (
            x + w + padding < b["x"]
            or x > b["x"] + b["w"] + padding
            or z + d + padding < b["z"]
            or z > b["z"] + b["d"] + padding
        ):
            return True
    return False


def build_void_tech_station(x, z):
    """
    Directive: High-density, detailed station based on reference image_4.png.
    Bounding Box: approx 9x7x11.
    """
    y = FIELD_BOUNDS["y"]

    commands = [
        # Foundation: Polished Deepslate Plinth (larger footprint)
        f"fill {x-1} {y-1} {z-1} {x+7} {y-1} {z+5} smooth_stone_slab",
        f"fill {x} {y} {z} {x+6} {y} {z+4} {PALETTE['primary']}",
        # Bioluminescent Purple Floor Panels (Matching reference lighting)
        f"setblock {x+1} {y} {z+1} {PALETTE['light']}",
        f"setblock {x+1} {y+1} {z+1} {PALETTE['floor']}",
        f"setblock {x+5} {y} {z+1} {PALETTE['light']}",
        f"setblock {x+5} {y+1} {z+1} {PALETTE['floor']}",
        f"setblock {x+3} {y} {z+3} {PALETTE['light']}",
        f"setblock {x+3} {y+1} {z+3} {PALETTE['floor']}",
        # Grand Deepslate Pillars and purpur accents
        f"fill {x} {y+1} {z} {x} {y+7} {z+4} {PALETTE['pillar']}",
        f"fill {x+6} {y+1} {z} {x+6} {y+7} {z+4} {PALETTE['pillar']}",
        f"setblock {x} {y+2} {z+2} purple_stained_glass",
        f"setblock {x+6} {y+2} {z+2} purple_stained_glass",
        # Teal Girders (Industrial details from reference image)
        f"fill {x} {y+8} {z+2} {x+6} {y+8} {z+2} {PALETTE['teal']}",
        # Vaulted purpur roof (Based on purpur roofing from image_4.png)
        f"fill {x} {y+9} {z-1} {x+6} {y+9} {z+5} purpur_slab",
        f"fill {x} {y+10} {z} {x+6} {y+10} {z+4} purpur_stairs[facing=south,half=bottom]",
        f"say [AI Architect] Void-Tech Station Prototype deployed at {x} {y} {z} (High-Density, Y:63).",
    ]

    with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
        for cmd in commands:
            mcr.command(cmd)
            time.sleep(0.05)


if __name__ == "__main__":
    history = load_history()
    # New bounding box to account for increased voxel density (approx 9x7 footprint)
    width, depth = 9, 7

    placed = False
    for _ in range(50):
        # Pick random coordinates, constrained within safe bounds for the larger build size
        tx = random.randint(
            FIELD_BOUNDS["min_x"] + 10, FIELD_BOUNDS["max_x"] - width - 10
        )
        tz = random.randint(
            FIELD_BOUNDS["min_z"] + 10, FIELD_BOUNDS["max_z"] - depth - 10
        )

        if not check_collision(tx, tz, width, depth, history):
            print(
                f"🚀 Found clear site for Void-Tech density build at {tx}, {tz}. Commencing..."
            )
            build_void_tech_station(tx, tz)
            history.append(
                {
                    "x": tx,
                    "z": tz,
                    "w": width,
                    "d": depth,
                    "label": "Void_Tech_Station_A",
                }
            )
            save_history(history)
            placed = True
            break

    if not placed:
        print(
            "⚠️ Field is too crowded for this build density! Spatial collision imminent."
        )
