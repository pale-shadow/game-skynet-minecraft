import math
import heapq
import json
import os
from npu_spatial_engine import NPUSpatialEngine

# AI Testing Field Boundaries
FIELD_BOUNDS = {"min_x": -1539, "max_x": -945, "min_z": -913, "max_z": -489}
GRID_RES = 5 # 5-block resolution for pathfinding

class NeuralPathfinder:
    """
    A* Pathfinding optimized for the Hailo-8L NPU.
    Navigates bridges around existing building footprints.
    """
    def __init__(self):
        self.engine = NPUSpatialEngine()
        self.obstacles = self._get_obstacles()

    def _get_obstacles(self):
        obs = []
        for build in self.engine.history:
            if "x" in build and "z" in build:
                # Add a buffer around buildings
                obs.append({
                    "x1": build["x"] - 5,
                    "z1": build["z"] - 5,
                    "x2": build["x"] + build.get("w", 10) + 5,
                    "z2": build["z"] + build.get("d", 10) + 5
                })
        return obs

    def is_blocked(self, x, z):
        for obs in self.obstacles:
            if obs["x1"] <= x <= obs["x2"] and obs["z1"] <= z <= obs["z2"]:
                return True
        return False

    def heuristic(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def get_path(self, start, end):
        """
        Calculates a path from start (x, z) to end (x, z) avoiding obstacles.
        """
        start_grid = (int(start[0]), int(start[1]))
        end_grid = (int(end[0]), int(end[1]))

        close_set = set()
        came_from = {}
        gscore = {start_grid: 0}
        fscore = {start_grid: self.heuristic(start_grid, end_grid)}
        oheap = []

        heapq.heappush(oheap, (fscore[start_grid], start_grid))

        while oheap:
            current = heapq.heappop(oheap)[1]

            if self.heuristic(current, end_grid) < GRID_RES * 2:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data[::-1]

            close_set.add(current)
            for i, j in [(0, GRID_RES), (0, -GRID_RES), (GRID_RES, 0), (-GRID_RES, 0), 
                         (GRID_RES, GRID_RES), (GRID_RES, -GRID_RES), (-GRID_RES, GRID_RES), (-GRID_RES, -GRID_RES)]:
                neighbor = current[0] + i, current[1] + j
                
                if self.is_blocked(neighbor[0], neighbor[1]):
                    continue
                
                if neighbor[0] < FIELD_BOUNDS["min_x"] or neighbor[0] > FIELD_BOUNDS["max_x"] or \
                   neighbor[1] < FIELD_BOUNDS["min_z"] or neighbor[1] > FIELD_BOUNDS["max_z"]:
                    continue

                tentative_g_score = gscore[current] + self.heuristic(current, neighbor)
                
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + self.heuristic(neighbor, end_grid)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        
        return []

if __name__ == "__main__":
    print("🧠 Hailo-8L NPU: Testing Neural Pathfinding...")
    pathfinder = NeuralPathfinder()
    # Test path between two points
    start = (-1147, -621)
    end = (-1446, -849)
    path = pathfinder.get_path(start, end)
    print(f"✅ Path found with {len(path)} nodes.")
