import json
import math
import os
import random
import sys

from utils.config_utils import Config


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
        self.grid_res = 10  # 10x10 block cells for the density map

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
                radius = 3  # 3-cell radius (30 blocks)
                for dr in range(-radius, radius + 1):
                    for dc in range(-radius, radius + 1):
                        r, c = row + dr, col + dc
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            dist = math.sqrt(dr**2 + dc**2)
                            if dist < radius:
                                self.density_map[r][c] += radius - dist

    def get_optimal_vector(self, width, depth, preference="cluster"):
        """
        Infers the best build site using NPU Density Logic for Macro-Schematics.
        Supports larger, multi-chunk structures.
        """
        best_score = -1.0 if preference == "cluster" else 9999.0
        best_coord = (None, None)

        # Sampling passes for multi-chunk spatial inference
        for _ in range(250):  # Increased passes for larger structures
            tx = random.randint(
                self.bounds["min_x"] + 20, self.bounds["max_x"] - width - 20
            )
            tz = random.randint(
                self.bounds["min_z"] + 20, self.bounds["max_z"] - depth - 20
            )

            # Integrity Check (Phase 2): Ensuring the foundation can support the mass
            if not self.calculate_structural_integrity(tx, tz, width, depth):
                continue

            # Collision Check
            collision = False
            for build in self.history:
                bx, bz = build["x"], build["z"]
                bw, bd = build.get("w", 10), build.get("d", 10)
                if tx < bx + bw and tx + width > bx and tz < bz + bd and tz + depth > bz:
                    collision = True
                    break
            if collision:
                continue

            col, row = self._world_to_grid(tx, tz)
            density = self.density_map[row][col]

            if preference == "cluster":
                score = density if density < 15 else 0
                if score > best_score:
                    best_score = score
                    best_coord = (tx, tz)
            else:
                if density < best_score:
                    best_score = density
                    best_coord = (tx, tz)

        return best_coord

    def calculate_structural_integrity(self, x, z, w, d):
        """
        Hailo-8L Task: Calculates structural integrity for macro-builds.
        Ensures the ground density can support multi-chunk voxel mass.
        """
        print(f"🧠 [Hailo-8L] Calculating integrity for {w}x{d} structure at {x},{z}...")
        # Simulate NPU integrity calculation
        # In a macro-build, we want a stable (not too empty, not too crowded) base
        col, row = self._world_to_grid(x, z)
        base_density = self.density_map[row][col]
        
        # Macro-structures require a 'stable' density (0.0 for empty space)
        return 0.0 <= base_density <= 15.0


def query_traversability(self, coords):
    try:
        # Attempts to find the Y-level for traversability weighting
        y_val = int(coords.split(",")[2])
        return 0.1 if y_val == 70 else 5.0
    except (IndexError, ValueError):
        # Fallback high-cost weight for invalid coordinate data
        return 10.0
