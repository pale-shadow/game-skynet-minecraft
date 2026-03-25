import os
import time
import random
import logging
import subprocess
from datetime import datetime
from adaptive_mutation_v7 import AdaptiveMutator
from skynet_process import push_build_to_chonk, get_node_logic
from place_ai_warning_signs import place_random_warning

# Unified Configuration: Phase 2.1 [378, 416, Conversation]
SLEEP_INTERVAL = 3600  # Exact 1-hour cycle
TEMP_THRESHOLD = 75.0  # Pi 5 Thermal Limit
LOG_FILE = "../logs/skynet_daemon.log"
SECTORS = ["Shroomville Urban District", "Silicon Ridge (Beta-Zone)", "Abyssal Reef (Ocean Sector)"]

# AI Cluster Node Definitions [Conversation]
AI_CLUSTER = {
    "node_hailo": {"hardware": "Pi5 / Hailo-8L", "focus": "Heavy Industry"},
    "node_edgetpu": {"hardware": "ASUS Edge-t", "focus": "Organic Mutation"},
    "node_vision": {"hardware": "AI Vision Node", "focus": "Perimeter Security"}
}

# Professional Logging Configuration [Conversation]
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_temp():
    try:
        res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        return float(res.replace("temp=", "").replace("'C\n", ""))
    except Exception as e:
        logging.error(f"Thermal Hardware Failure: {e}")
        return 0.0

def generate_unified_metadata(build_name, node_info, sector):
    """Generates sign data for the Bitsmasher Historical Ledger [423, Conversation]."""
    return {
        "front": [f"&b&l{build_name}", f"&3Built: {datetime.now().strftime('%b %d, 2026')}", f"&0HW: {node_info['hardware']}", ""],
        "back": ["&8Skynet Unified Brain", f"&0Sector: {sector}", "&2Status: Urbanized", ""]
    }

def run_unified_brain():
    logging.info("🧠 Skynet Unified AI Brain: ONLINE")
    logging.info(f"📡 Monitoring Nodes: {', '.join([n['hardware'] for n in AI_CLUSTER.values()])}")
    
    mutator = AdaptiveMutator()
    mutator.engine.history_file = "input/build_history.json"
    
    cycle_count = 0
    while True:
        cycle_count += 1
        temp = get_temp()
        logging.info(f"--- Unified Cycle {cycle_count} | Temp: {temp}'C ---")
        
        if temp > TEMP_THRESHOLD:
            logging.warning("⚠ Thermal Throttling: High NPU load detected. Waiting 60s...")
            time.sleep(60)
            continue

        # 1. World State Scan (Adaptive Mutation)
        try:
            logging.info("👁 Scanning world state for Phase 2.1 mutations...")
            mutator.run_cycle()
        except Exception as e: logging.error(f"Mutation Error: {e}")

        # 2. Void Reclamation Signage [424, Conversation]
        try:
            logging.info("🚩 Deploying randomized Void Reclamation warning...")
            place_random_warning()
        except Exception as e: logging.error(f"Signage Error: {e}")

        # 3. Randomized Cluster Construction [378, 381, Conversation]
        try:
            node_id = random.choice(list(AI_CLUSTER.keys()))
            node_info = AI_CLUSTER[node_id]
            sector = random.choice(SECTORS)
            build_name = f"Void-Tech {random.randint(100, 999)}"
            
            logging.info(f"🏗 Delegating {build_name} to {node_info['hardware']}...")
            metadata = generate_unified_metadata(build_name, node_info, sector)
            
            cmds = get_node_logic(node=node_id, sector=sector, metadata=metadata)
            if cmds:
                push_build_to_chonk(cmds)
                logging.info(f"✅ Successfully urbanized {sector}")
        except Exception as e: logging.error(f"Build Error: {e}")

        logging.info(f"💤 Cycle complete. Next sequence in {SLEEP_INTERVAL}s.")
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    run_unified_brain()
