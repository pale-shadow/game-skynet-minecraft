import math
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
        distance = math.sqrt((pos["x"] - coords["x"])**2 + (pos["z"] - coords["z"])**2)
        if distance < radius:
            return True
    return False

def test_schematic_boundary_safety():
    """
    Ensures new schematics do not overlap with Hub 01 (Logic Core)
    or Hub 02 (Transmission Core) coordinates.
    """
    # New position in the Abyssal Reef sector, far from known hubs
    new_schem_pos = {"x": 1950, "y": 84, "z": 750} 
    
    collision = check_hub_collision(new_schem_pos, radius=10)

    assert (
        collision is False
    ), f"Safety Breach: Schematic overlaps with critical Skynet Hub infrastructure!"
