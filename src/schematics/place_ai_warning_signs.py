import logging
import os
import random
import time

from skynet_core import Config

import mcrcon

# Void Reclamation Project Messages [378, 423, Conversation]
VOID_MESSAGES = [
    ["[Skynet AI]", "VOID RECLAMATION", "PHASE 2.1 ACTIVE", "RESTRICTED AREA"],
    ["[Skynet AI]", "NPU SPATIAL SYNC", "DETERRING VOID", "PLEASE WAIT..."],
    ["[System]", "RECONSTRUCTION", "IN PROGRESS", "PROCEED WITH CAUTION"],
    ["[Archival]", "VOID TECH OVERGROWTH", "FROM SPORES TO", "CIRCUITS - 2026"],
    ["[DANGER]", "RECLAMATION CORE", "HIGH RADIATION", "VOID LEAK DETECTED"],
]


def get_sign_nbt(messages):
    """Formats sign lines into 1.21.1 JSON component syntax."""
    json_lines = [f'\'{{"text":"{line}"}}\'' for line in messages]
    return f'{{front_text:{{messages:[{",".join(json_lines)}]}}}}'


def place_random_warning():
    """Places a randomized sign within the AI containment bounds [Conversation]."""
    # Use bounds from your NPU Spatial Engine config
    bounds = Config.FIELD_BOUNDS
    target_x = random.randint(bounds["min_x"], bounds["max_x"])
    target_z = random.randint(bounds["min_z"], bounds["max_z"])
    y_level = bounds["y_base"]

    msg_set = random.choice(VOID_MESSAGES)
    nbt = get_sign_nbt(msg_set)

    logging.info(f"🚩 Deploying warning to {target_x}, {target_z}...")

    try:
        # Utilizing the RCON credentials from your environment [1]
        with mcrcon.MCRcon(
            Config.CHONK_IP, os.getenv("RCON_PASS"), port=Config.RCON_PORT
        ) as mcr:
            mcr.command(f"forceload add {target_x} {target_z}")
            time.sleep(1)

            # Place Sign and Industrial Lighting (Torch)
            mcr.command(
                f"setblock {target_x} {y_level} {target_z} minecraft:oak_sign{nbt} replace"
            )
            mcr.command(
                f"setblock {target_x} {y_level + 1} {target_z} minecraft:torch replace"
            )

            mcr.command(f"forceload remove {target_x} {target_z}")
            logging.info(f"✅ Void Reclamation sign successfully placed.")
    except Exception as e:
        logging.error(f"❌ Signage Deployment Failure: {e}")
