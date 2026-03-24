import json
import os
import math
import random
from skynet_core import Config

class NPUSpatialEngine:
    """
    Simulates Hailo-8L NPU Spatial Inference for Skynet.
    Analyzes existing voxel density to find optimal 'Neural Nodes'.
    """
    def __init__(self):
        self.history_file = Config.HISTORY_FILE
        self.history = self._load_history()
        self.bounds = Config.FIELD_BOUNDS
        self.grid_res = 10 # 10x10 block cells for the density map
        
        self.width = abs(self.bounds["max_x"] - self.bounds["min_x"])
        self.depth = abs(self.bounds["max_z"] - self.bounds["min_z"])
        self.cols = self.width // self.grid_res
        self.rows = self.depth // self.grid_res
        self.density_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self._generate_density_map()

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def _world_to_grid(self, x, z):
        col = (x - self.bounds["min_x"]) // self.grid_res
        row = (z - self.bounds["min_z"]) // self.grid_res
        return max(0, min(col, self.cols - 1)), max(0, min(row, self.rows - 1))

    def _generate_density_map(self):
        """Populates the grid with 'energy' from existing builds."""
        for build in self.history:
            if "x" in build and "z" in build:
                col, row = self._world_to_grid(build["x"], build["z"])
                # Add density with a falloff (simulating neural signal spread)
                radius = 3 # 3-cell radius (30 blocks)
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        r, c = row + dr, col + dc
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            dist = math.sqrt(dr**2 + dc**2)
                            if dist < radius:
                                self.density_map[r][c] += (radius - dist)

    def get_optimal_vector(self, width, depth, preference="cluster"):
        """
        Infers the best build site using NPU Density Logic.
        """
        best_score = -1.0 if preference == "cluster" else 9999.0
        best_coord = (None, None)
        
        # Sample 100 random points to simulate NPU inference passes
        for _ in range(100):
            x = random.randint(self.bounds["min_x"] + width, self.bounds["max_x"] - width)
            z = random.randint(self.bounds["min_z"] + depth, self.bounds["max_z"] - depth)
            
            # Check for direct collision
            collision = False
            for build in self.history:
                if "x" in build and "z" in build:
                    bx, bz = build["x"], build["z"]
                    bw, bd = build.get("w", 10), build.get("d", 10)
                    if (x < bx + bw and x + width > bx and
                        z < bz + bd and z + depth > bz):
                        collision = True
                        break
            if collision: continue

            col, row = self._world_to_grid(x, z)
            density = self.density_map[row][col]

            if preference == "cluster":
                # High density is good, but not too high
                score = density if density < 10 else 0
                if score > best_score:
                    best_score = score
                    best_coord = (x, z)
            else: # 'void' preference
                if density < best_score:
                    best_score = density
                    best_coord = (x, z)

        return best_coord

if __name__ == "__main__":
    print("📡 Hailo-8L NPU: Initializing Spatial Engine...")
    engine = NPUSpatialEngine()
    x, z = engine.get_optimal_vector(30, 30, preference="cluster")
    print(f"🧠 Inference Result (Neural Cluster): X={x}, Z={z}")
