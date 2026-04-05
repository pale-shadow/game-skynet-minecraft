import logging
import os
import random
import time
from datetime import datetime

import mcrcon

# Configuration [Conversation]
CHONK_IP = os.getenv("CHONK_IP", "chonk.lab.bitsmasher.net")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
SLEEP_INTERVAL = 3600  # Hourly cycle

# Area Bounds (derived from your CORNERS list)
MIN_X, MAX_X = -1539, -945
MIN_Z, MAX_Z = -913, -489
Y_LEVEL = 64

# Void Reclamation Project Messages [378, 423, Conversation]
VOID_MESSAGES = [
    ["[Skynet AI]", "VOID RECLAMATION", "PHASE 2.1 ACTIVE", "RESTRICTED AREA"],
    ["[Skynet AI]", "NPU SPATIAL SYNC", "DETERRING VOID", "PLEASE WAIT..."],
    ["[System]", "RECONSTRUCTION", "IN PROGRESS", "PROCEED WITH CAUTION"],
    ["[Archival]", "VOID TECH OVERGROWTH", "FROM SPORES TO", "CIRCUITS - 2026"],
    ["[DANGER]", "RECLAMATION CORE", "HIGH RADIATION", "VOID LEAK DETECTED"],
]

# Professional Logging Setup [Conversation]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[logging.FileHandler("../logs/ai_signs.log"), logging.StreamHandler()],
)


def get_sign_nbt(messages):
    """Formats sign lines into 1.21.1 JSON component syntax [1, 2]."""
    json_lines = [f'\'{{"text":"{line}"}}\'' for line in messages]
    # Set the first line to Dark Red for Skynet AI branding
    json_lines = f'\'{{"text":"{messages}","color":"dark_red","bold":true}}\''
    return f'{{front_text:{{messages:[{",".join(json_lines)}]}}}}'


def place_random_warning():
    if not RCON_PASS:
        logging.error("RCON_PASS environment variable is not set.")
        return

    # 1. Select Random Location & Message
    target_x = random.randint(MIN_X, MAX_X)
    target_z = random.randint(MIN_Z, MAX_Z)
    msg_set = random.choice(VOID_MESSAGES)
    nbt = get_sign_nbt(msg_set)

    logging.info(f"🔌 Connecting to Chonk RCON for Void Reclamation placement...")

    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            # 2. Safety: Forceload chunk
            mcr.command(f"forceload add {target_x} {target_z}")
            time.sleep(1)

            # 3. Execution: Place Sign & Torch for night visibility
            cmd_sign = f"setblock {target_x} {Y_LEVEL} {target_z} minecraft:oak_sign{nbt} replace"
            mcr.command(cmd_sign)
            mcr.command(
                f"setblock {target_x} {Y_LEVEL + 1} {target_z} minecraft:torch replace"
            )

            # 4. Cleanup
            mcr.command(f"forceload remove {target_x} {target_z}")
            logging.info(f"✅ Placed warning at {target_x}, {target_z}: {msg_set[3]}")

    except Exception as e:
        logging.error(f"❌ Void Reclamation RCON Error: {e}")


if __name__ == "__main__":
    logging.info("🚀 AI Warning Sign Daemon: INITIALIZED")
    while True:
        place_random_warning()
        logging.info(f"💤 Sleeping for {SLEEP_INTERVAL}s...")
        time.sleep(SLEEP_INTERVAL)
