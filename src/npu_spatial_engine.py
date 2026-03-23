import json
import os
import math
import random

# AI Testing Field Boundaries (from GEMINI.md)
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489, "y": 63}
HISTORY_FILE = "build_history.json"
GRID_RESOLUTION = 10 # 10x10 block cells for the density map

class NPUSpatialEngine:
    """
    Simulates Hailo-8L NPU Spatial Inference for Skynet.
    Analyzes existing voxel density to find optimal 'Neural Nodes'.
    """
    def __init__(self):
        self.history = self._load_history()
        self.width = abs(FIELD_BOUNDS["max_x"] - FIELD_BOUNDS["min_x"])
        self.depth = abs(FIELD_BOUNDS["max_z"] - FIELD_BOUNDS["min_z"])
        self.cols = self.width // GRID_RESOLUTION
        self.rows = self.depth // GRID_RESOLUTION
        self.density_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self._generate_density_map()

    def _load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        return []

    def _world_to_grid(self, x, z):
        col = (x - FIELD_BOUNDS["min_x"]) // GRID_RESOLUTION
        row = (z - FIELD_BOUNDS["min_z"]) // GRID_RESOLUTION
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
        'cluster' -> Near existing nodes (Neural Hubs)
        'void' -> Farthest from existing nodes (Outposts)
        """
        best_score = -1.0 if preference == "cluster" else 9999.0
        best_coord = (None, None)
        
        # Sample 100 random points to simulate NPU inference passes
        for _ in range(100):
            x = random.randint(FIELD_BOUNDS["min_x"] + width, FIELD_BOUNDS["max_x"] - width)
            z = random.randint(FIELD_BOUNDS["min_z"] + depth, FIELD_BOUNDS["max_z"] - depth)
            
            # Check for direct collision (hard constraint)
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
                # High density is good, but not too high (to avoid overlaps)
                score = density if density < 10 else 0
                if score > best_score:
                    best_score = score
                    best_coord = (x, z)
            else: # 'void' preference
                if density < best_score:
                    best_score = density
                    best_coord = (x, z)

        return best_coord

    def get_nearest_node(self, x, z):
        """Finds the closest existing build to a coordinate."""
        min_dist = 999999
        nearest = None
        for build in self.history:
            if "x" in build and "z" in build:
                dist = math.sqrt((x - build["x"])**2 + (z - build["z"])**2)
                if dist < min_dist:
                    min_dist = dist
                    nearest = build
        return nearest

if __name__ == "__main__":
    print("📡 Hailo-8L NPU: Initializing Spatial Engine...")
    engine = NPUSpatialEngine()
    x, z = engine.get_optimal_vector(30, 30, preference="cluster")
    print(f"🧠 Inference Result (Neural Cluster): X={x}, Z={z}")
    x_void, z_void = engine.get_optimal_vector(30, 30, preference="void")
    print(f"🧠 Inference Result (Void Outpost): X={x_void}, Z={z_void}")
