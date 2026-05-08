import math
import sys
import json
import os

import pytest

SKYNET_HUBS = {
    "Hub 01": {"x": -1340, "z": -664},
    "Hub 02": {"x": -1458, "z": -623},
    "Hub 03": {"x": -1283, "z": -658},
    "Hub 04": {"x": -1161, "z": -536},
    "Hub 05": {"x": -1133, "z": -749},
    "Hub 06": {"x": -1212, "z": -670},
    "Hub 07": {"x": -1144, "z": -631},
}


def check_hub_collision(pos, radius=10):
    """
    Calculates proximity to established Skynet Hubs to prevent
    overlapping 'Void-Tech' mutations.
    """
    for hub_name, coords in SKYNET_HUBS.items():
        distance = math.sqrt(
            (pos["x"] - coords["x"]) ** 2 + (pos["z"] - coords["z"]) ** 2
        )
        if distance < radius:
            return True, hub_name
    return False, None


def test_schematic_boundary_safety(file_path=None):
    """
    Ensures new schematics do not overlap with critical Skynet Hub infrastructure.
    If file_path is provided, it validates the voxels within.
    """
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # New position in the Abyssal Reef sector, far from known hubs
        # We offset the relative voxels by this anchor
        anchor = {"x": 1950, "y": 84, "z": 750}
        
        for voxel in data.get("voxels", []):
            pos = {
                "x": anchor["x"] + voxel["x"],
                "y": anchor["y"] + voxel["y"],
                "z": anchor["z"] + voxel["z"]
            }
            collision, hub = check_hub_collision(pos, radius=10)
            if collision:
                pytest.fail(f"Safety Breach: Voxel at {pos} overlaps with {hub}!")
        
        print(f"[√] All {len(data.get('voxels', []))} voxels passed boundary safety at anchor {anchor}.")
    else:
        # Default safety check for the anchor point itself
        new_schem_pos = {"x": 1950, "y": 84, "z": 750}
        collision, hub = check_hub_collision(new_schem_pos, radius=10)
        assert (
            collision is False
        ), f"Safety Breach: Schematic anchor at {new_schem_pos} overlaps with {hub}!"

if __name__ == "__main__":
    # If run as a script, check the provided file
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        try:
            test_schematic_boundary_safety(test_file)
            print("[+] Boundary Safety Validation: SUCCESS")
        except Exception as e:
            print(f"[-] Boundary Safety Validation: FAILED - {e}")
            sys.exit(1)
    else:
        # Run default test
        test_schematic_boundary_safety()
        print("[+] Boundary Safety Validation: SUCCESS (Default Anchor)")
