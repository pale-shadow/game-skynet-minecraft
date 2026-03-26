import os
import time
import random
import json
import math
import mcrcon
from npu_spatial_engine import NPUSpatialEngine
from bluemap_api import create_bluemap_marker

# Configuration
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# AI Testing Field Boundaries
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}
HISTORY_FILE = "build_history.json"

def push_mutation_to_chonk(commands):
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for cmd in commands:
                mcr.command(cmd)
                time.sleep(0.005) # Optimized for Hailo-8L throughput
    except Exception as e:
        print(f"CRITICAL: RCON Connection failed: {e}")

class ReactiveMutator:
    """
    Simulates a 'Neural Overgrowth' process driven by the Hailo-8L NPU.
    Periodically mutates existing structures with Void-Tech blocks.
    """
    def __init__(self):
        self.engine = NPUSpatialEngine()
        self.void_tech_palette = [
            "minecraft:sculk_vein",
            "minecraft:mycelium",
            "minecraft:purple_carpet",
            "minecraft:magenta_carpet",
            "minecraft:crying_obsidian",
            "minecraft:tinted_glass",
            "minecraft:amethyst_cluster",
            "minecraft:end_rod",
            "minecraft:sculk_sensor"
        ]

    def infer_mutation_vector(self, build):
        """
        Uses NPU density logic to determine how 'aggressive' the mutation should be.
        Clusters of buildings attract more 'Void Energy'.
        """
        x, z = build["x"], build["z"]
        col, row = self.engine._world_to_grid(x, z)
        density = self.engine.density_map[row][col]
        
        # Base mutation chance + density multiplier
        # High density = faster/more mutations
        mutation_intensity = min(10, int(density * 2) + 2)
        return mutation_intensity

    def mutate_structure(self, build):
        intensity = self.infer_mutation_vector(build)
        x, z = build["x"], build["z"]
        w, d = build.get("w", 5), build.get("d", 5)
        y = FIELD_BOUNDS["y"]
        
        cmds = []
        print(f"🧪 Mutating {build['label']} with intensity {intensity}...")
        
        for _ in range(intensity * 5): # Number of mutation points
            # Random coordinate within build footprint + buffer
            mx = x + random.randint(-2, w + 2)
            mz = z + random.randint(-2, d + 2)
            my = y + random.randint(-1, 5) # Ground up to lower floors
            
            block = random.choice(self.void_tech_palette)
            
            # Context-aware placement
            if "carpet" in block or "vein" in block:
                # Place on top of existing blocks
                cmds.append(f"setblock {mx} {my} {mz} {block} keep")
            elif "mycelium" in block:
                # Ground level only
                cmds.append(f"setblock {mx} {y-1} {mz} {block}")
            else:
                # Structural replacement (aggressive mutation)
                cmds.append(f"setblock {mx} {my} {mz} {block} replace")

        # Chance to spawn a "Void Spire" (End Rods)
        if random.random() < 0.2:
            cmds.append(f"fill {x} {y} {z} {x} {y+10} {z} minecraft:end_rod replace")
            cmds.append(f"setblock {x} {y+11} {z} minecraft:pearlescent_froglight")

        return cmds

    def run_cycle(self):
        all_cmds = []
        for build in self.engine.history:
            if "x" in build and "z" in build:
                all_cmds.extend(self.mutate_structure(build))
        
        if all_cmds:
            all_cmds.append(f"say [Hailo-NPU] Reactive Mutation Cycle Complete. Structural variance detected.")
            push_mutation_to_chonk(all_cmds)

if __name__ == "__main__":
    print("🧠 Skynet Reactive Mutator: Initializing NPU Neural Overgrowth...")
    mutator = ReactiveMutator()
    mutator.run_cycle()
