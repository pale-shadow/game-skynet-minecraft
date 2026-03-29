import argparse
import sys
import os
import json
import math
import random

# Ensure we can import skynet_core if run as a script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from skynet_core import Config
except ImportError:
    # Fallback for different execution contexts
    from .skynet_core import Config

class NPUSpatialEngine:
    """
    Simulates Hailo-8L NPU Spatial Inference for Skynet.
    Analyzes existing voxel density to find optimal 'Neural Nodes'.
    """
    def __init__(self, hardware_mode="hailo"):
        self.hardware_mode = hardware_mode
        self.history_file = Config.HISTORY_FILE
        self.history = self._load_history()
        self.bounds = Config.FIELD_BOUNDS
        self.grid_res = 10 # 10x10 block cells for the density map
        
        # Grid dimensions based on bounds
        self.width = abs(self.bounds["max_x"] - self.bounds["min_x"])
        self.depth = abs(self.bounds["max_z"] - self.bounds["min_z"])
        self.cols = self.width // self.grid_res
        self.rows = self.depth // self.grid_res
        self.density_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self._generate_density_map()
        
        print(f"🚀 NPUSpatialEngine initialized on hardware: {self.hardware_mode}")

    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
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
            # Coordinates must be within bounds minus build dimensions
            tx = random.randint(self.bounds["min_x"] + 10, self.bounds["max_x"] - width - 10)
            tz = random.randint(self.bounds["min_z"] + 10, self.bounds["max_z"] - depth - 10)
            
            # Check for direct collision with existing builds
            collision = False
            for build in self.history:
                if "x" in build and "z" in build:
                    bx, bz = build["x"], build["z"]
                    bw, bd = build.get("w", 10), build.get("d", 10)
                    if (tx < bx + bw and tx + width > bx and
                        tz < bz + bd and tz + depth > bz):
                        collision = True
                        break
            if collision: continue

            col, row = self._world_to_grid(tx, tz)
            density = self.density_map[row][col]

            if preference == "cluster":
                # High density is good, but not too high
                score = density if density < 10 else 0
                if score > best_score:
                    best_score = score
                    best_coord = (tx, tz)
            else: # 'void' preference (prefers empty areas)
                if density < best_score:
                    best_score = density
                    best_coord = (tx, tz)

        return best_coord

    def query_traversability(self, coords):
        """
        Returns a cost weight for a specific voxel.
        Lower weight = More 'attractive' path for the Weaver (Rail Builder).
        Input format: "x,y,z" or "label,x,z,y" (handling legacy split[3])
        """
        try:
            parts = coords.split(',')
            # Standardize coordinate parsing
            if len(parts) == 3:
                x, y, z = map(int, parts)
            elif len(parts) >= 4:
                # Legacy support for split[3] if it's label,x,z,y
                x, z, y = int(parts[1]), int(parts[2]), int(parts[3])
            else:
                return 10.0

            # Boundary Checks
            if not (self.bounds["min_x"] <= x <= self.bounds["max_x"] and 
                    self.bounds["min_z"] <= z <= self.bounds["max_z"]):
                return 100.0 # Out of bounds is very unattractive
            
            # Y-Level Preference Check
            return 0.1 if y == self.bounds["y_base"] else 5.0
            
        except (IndexError, ValueError):
            return 10.0 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--pos", type=str, required=True)
    parser.add_argument("--hardware", type=str, default="hailo")
    args = parser.parse_args()
    engine = NPUSpatialEngine(hardware_mode=args.hardware)
    
    if args.query == "traversability":
        weight = engine.query_traversability(args.pos)
        print(weight)
    elif args.query == "optimal_vector":
        x, z = engine.get_optimal_vector(30, 30)
        print(f"{x},{z}")
