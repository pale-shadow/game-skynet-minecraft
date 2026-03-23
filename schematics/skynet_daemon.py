import os
import time
import subprocess
from adaptive_mutation_v7 import AdaptiveMutator
from skynet_process import get_hailo_structure_logic, push_build_to_chonk

# Configuration
SLEEP_INTERVAL = 300 # 5 minutes
TEMP_THRESHOLD = 75.0 # Celsius

def get_temp():
    try:
        res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        return float(res.replace("temp=", "").replace("'C\n", ""))
    except:
        return 0.0

def run_skynet_loop():
    print("🚀 Skynet Daemon: INITIALIZED")
    print(f"📡 Monitoring Pi 5 + Hailo-8L (Threshold: {TEMP_THRESHOLD}'C)")
    
    mutator = AdaptiveMutator()
    
    # Patch the HISTORY_FILE path in the engine to match the actual location
    # Since skynet_daemon.py is in 'schematics/', the engine (in 'schematics/') 
    # will look for 'build_history.json'. 
    # But it's actually in 'input/build_history.json'.
    mutator.engine.history_file = "input/build_history.json"
    mutator.engine.history = mutator.engine._load_history()

    cycle_count = 0
    
    while True:
        cycle_count += 1
        temp = get_temp()
        print(f"\n--- Cycle {cycle_count} | Temp: {temp}'C ---")
        
        if temp > TEMP_THRESHOLD:
            print(f"⚠️ Thermal Throttling: Temp {temp}'C exceeds threshold. Sleeping...")
            time.sleep(60)
            continue

        # 1. Adaptive Mutation (Scan and Infect)
        print("👁️ Running Adaptive Mutation Cycle...")
        try:
            mutator.run_cycle()
        except Exception as e:
            print(f"❌ Mutation Error: {e}")

        # 2. Occasional Procedural Build (Every 4 cycles / 20 mins)
        if cycle_count % 4 == 0:
            print("🏗️ NPU Spatial Inference: Generating New Void-Tech...")
            try:
                # Use the logic from skynet_process.py
                cmds = get_hailo_structure_logic()
                if cmds:
                    push_build_to_chonk(cmds)
            except Exception as e:
                print(f"❌ Build Error: {e}")

        print(f"💤 Cycle complete. Sleeping for {SLEEP_INTERVAL}s...")
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    run_skynet_loop()
