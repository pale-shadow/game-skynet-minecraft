import json
import os
import random
import sys
import time

import mcschematic

# Ensure project paths are correct
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src/schematics"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src/servers/skynet"))

from builders.station2 import build as build_station
from npu_spatial_engine import NPUSpatialEngine
from skynet_core import Config, SkynetRCON


def main():
    print("🧠 Initializing Hailo NPU Spatial Inference...")
    engine = NPUSpatialEngine(hardware_mode="hailo")
    rcon = SkynetRCON()

    # Load high-fidelity v5 prompt
    prompt_path = "src/schematics/prompts/crafter_hub_v5.json"
    with open(prompt_path, "r") as f:
        prompt = json.load(f)

    w = prompt["dimensions"]["width"]
    h = prompt["dimensions"]["height"]
    l = prompt["dimensions"]["length"]
    build_name = f"HAILO_V5_{random.randint(1000, 9999)}"
    prompt["name"] = build_name

    print(f"📍 Inferring optimal spatial vector for {build_name} ({w}x{h}x{l})...")
    tx, tz = engine.get_optimal_vector(w, l, preference="void")
    
    if tx is None:
        print("❌ NPU Inference Error: No safe spatial vector found.")
        return

    # Survey site for Y-level
    ty = rcon.survey_site(tx, tz)
    print(f"✅ Inferred optimal build site: ({tx}, {ty}, {tz})")

    # Generate schematic using v5 builder standards
    print(f"🏗 Generating voxel array on Hailo hardware...")
    schem = mcschematic.MCSchematic()
    start_time = time.time()
    build_station(schem, prompt)
    generation_time = (time.time() - start_time) * 1000
    
    output_dir = Config.SCHEM_DIR
    os.makedirs(output_dir, exist_ok=True)
    schem.save(output_dir, build_name, mcschematic.Version.JE_1_21_1)
    schem_path = os.path.join(output_dir, f"{build_name}.schem")
    print(f"✅ Voxel synthesis complete ({generation_time:.2f}ms). Schematic saved: {schem_path}")

    # RCON Deployment Sequence
    print(f"🚀 Deploying to AI Field...")
    rcon.send(f"say [Hailo-NPU] Deploying v5 Architecture '{build_name}' at {tx} {ty} {tz}.")
    
    # WorldEdit Sequence
    rcon.send(f"//schem load {build_name}.schem")
    # Paste using the inferred coordinates
    paste_resp = rcon.send(f"//paste -a -t {tx} {ty} {tz}")
    
    # Retry with execute if -t fails (standard Skynet retry logic)
    if not paste_resp or "Incorrect" in str(paste_resp):
        rcon.send(f"execute positioned {tx} {ty} {tz} run worldedit:paste -a")

    print(f"✅ Deployment cycle complete.")

if __name__ == "__main__":
    main()
