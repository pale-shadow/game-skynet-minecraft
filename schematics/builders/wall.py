"""
wall.py — Wall and fence builder.

Generates straight walls with optional crenellations (merlons).
"""
import mcschematic
from .primitives import cuboid_filled, flat_plane


def build_wall(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 20)     # length of wall along X
    h = dims.get("height", 5)
    t = dims.get("length", 1)     # thickness along Z
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    primary = mats.get("primary", "minecraft:stone_bricks")
    slab    = mats.get("slab",    "minecraft:stone_brick_slab")
    stairs  = mats.get("secondary", "minecraft:stone_brick_stairs")

    crenellations = feats.get("crenellations", False)

    # Main wall body
    cuboid_filled(schem, 0, 0, 0, w - 1, h - 1, t - 1, primary)

    # Crenellations on top (merlons every other block)
    if crenellations:
        top_y = h
        for x in range(0, w):
            if x % 2 == 0:
                for z in range(t):
                    schem.setBlock((x, top_y, z), primary)
            else:
                for z in range(t):
                    schem.setBlock((x, h - 1, z), f"{slab}[type=top]" if slab else primary)

    # Walkway on top (slab)
    if h >= 3 and t >= 2:
        for x in range(w):
            schem.setBlock((x, h - 1, t // 2), f"{slab}[type=top]")

    return schem
