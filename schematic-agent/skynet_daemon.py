import os
import time
import random
import logging
import subprocess
from datetime import datetime
from adaptive_mutation_v7 import AdaptiveMutator
from skynet_process import get_hailo_structure_logic, push_build_to_chonk

# Configuration for 2026 Urbanization Phase [Conversation]
SLEEP_INTERVAL = 3600  # Hourly Build Cycle
RCON_CHECK_INTERVAL = 300 # 5 Minute Connectivity Check
TEMP_THRESHOLD = 75.0  # Celsius
SECTORS = ["Shroomville Urban District", "Silicon Ridge (Beta-Zone)", "Abyssal Reef (Ocean Sector)"]

# Robust Logging Path [Conversation]
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "skynet_daemon.log")

# Setup Professional Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def check_rcon_connectivity():
    """Verifies RCON connectivity to the Minecraft server [Conversation]."""
    from skynet_process import CHONK_IP, RCON_PASS, RCON_PORT
    import mcrcon
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            resp = mcr.command("list")
            if resp:
                logging.info(f"📡 RCON Connectivity Verified: {resp}")
                return True
    except Exception as e:
        logging.error(f"❌ RCON Connectivity Failed: {e}")
    return False

def generate_sign_metadata(build_name, sector_name):
    """Generates text for the mandatory Archival Signs [423, Conversation]."""
    date_str = datetime.now().strftime("%b %d, 2026")
    return {
        "front": [f"&b&l{build_name}", f"&3Built: {date_str}", "&0Hardware: Pi5 / Hailo AI", ""],
        "back": ["&8Daemon: Skynet v1.2", f"&0Sector: {sector_name}", "&2Status: Urbanized", ""]
    }

def get_temp():
    """Monitors Pi 5 hardware temperature for thermal safety [161, Conversation]."""
    try:
        res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        return float(res.replace("temp=", "").replace("'C\n", ""))
    except Exception as e:
        logging.error(f"Thermal Monitoring Failure: {e}")
        return 0.0

def run_skynet_loop():
    logging.info("🚀 Skynet Daemon v1.2: INITIALIZED")
    logging.info(f"📡 Monitoring Pi 5 + Hailo-8L (Threshold: {TEMP_THRESHOLD}'C)")

    mutator = AdaptiveMutator()
    # Correcting history path to align with urbanization workspace [Conversation]
    mutator.engine.history_file = "input/build_history.json"
    mutator.engine.history = mutator.engine._load_history()

    last_build_time = 0
    last_rcon_check_time = 0
    
    while True:
        now = time.time()
        temp = get_temp()

        # 1. RCON Health Check (Every 5 Minutes)
        if now - last_rcon_check_time >= RCON_CHECK_INTERVAL:
            check_rcon_connectivity()
            last_rcon_check_time = now

        # 2. Forced Hourly Build Cycle
        if now - last_build_time >= SLEEP_INTERVAL:
            logging.info(f"--- Starting Build Cycle | Temp: {temp}'C ---")
            
            if temp > TEMP_THRESHOLD:
                logging.warning(f"⚠ Thermal Throttling: Temp {temp}'C exceeds threshold. Skipping cycle.")
            else:
                # 2.1 Adaptive Mutation (World State Scan)
                logging.info("👁 Running Adaptive Mutation Cycle...")
                try:
                    mutator.run_cycle()
                except Exception as e:
                    logging.error(f"❌ Mutation Error: {e}")

                # 2.2 Forced Hourly Build with Void-Tech Palette [378, 416, Conversation]
                logging.info("🏗 NPU Spatial Inference: Generating New Randomized Build...")
                try:
                    sector = "AI Containment Area"
                    build_id = random.randint(100, 999)
                    build_name = f"Void-Tech {build_id}"
                    sign_data = generate_sign_metadata(build_name, sector)
                    
                    # Offloading procedural math to Hailo AI [1-3]
                    cmds = get_hailo_structure_logic(sector=sector, metadata=sign_data)
                    if cmds:
                        # Extract coordinates from first command for logging if possible
                        import re
                        coord_match = re.search(r"fill (-?\d+) (-?\d+) (-?\d+)", cmds[0])
                        coords = coord_match.groups() if coord_match else ("?", "?", "?")
                        
                        push_build_to_chonk(cmds)
                        logging.info(f"✅ Successfully deployed '{build_name}' at {coords[0]} {coords[1]} {coords[2]} to {sector}")
                    else:
                        logging.warning("Build logic generated no commands. Skipping deployment.")
                except Exception as e:
                    logging.error(f"❌ Build Error: {e}")

            last_build_time = now
            logging.info(f"💤 Cycle complete. Next autonomous build in {SLEEP_INTERVAL}s.")
        
        # Main loop idle sleep
        time.sleep(10)

if __name__ == "__main__":
    run_skynet_loop()
