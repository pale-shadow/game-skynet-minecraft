"""
castle.py — Castle and fortification builder.

Generates a castle with outer walls, corner towers, a courtyard, and a gate.
Combines wall and tower primitives for a complete fortification.
"""
import mcschematic
from .primitives import cuboid_filled, cuboid_walls, flat_plane, line_y, cylinder, circle_xz, cone


def build_castle(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 25)
    h = dims.get("height", 12)
    l = dims.get("length", 25)
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    primary   = mats.get("primary",   "minecraft:stone_bricks")
    secondary = mats.get("secondary", "minecraft:mossy_stone_bricks")
    tertiary  = mats.get("tertiary",  "minecraft:cracked_stone_bricks")
    floor_mat = mats.get("floor",     "minecraft:stone")
    stairs    = mats.get("stairs",    "minecraft:stone_brick_stairs")
    slab      = mats.get("slab",      "minecraft:stone_brick_slab")
    light     = mats.get("light",     "minecraft:torch")
    fence     = mats.get("fence",     "minecraft:stone_brick_wall")

    crenellations = feats.get("crenellations", True)
    has_floor     = feats.get("has_floor", True)
    interior_lit  = feats.get("interior_lit", True)

    wall_h = h
    wall_t = 2  # wall thickness

    # ---- Courtyard floor ----
    if has_floor:
        flat_plane(schem, 0, 0, 0, w - 1, l - 1, floor_mat)

    # ---- Outer walls ----
    # North wall (z=0..wall_t-1)
    cuboid_filled(schem, 0, 1, 0, w - 1, wall_h, wall_t - 1, primary)
    # South wall
    cuboid_filled(schem, 0, 1, l - wall_t, w - 1, wall_h, l - 1, primary)
    # West wall (x=0..wall_t-1)
    cuboid_filled(schem, 0, 1, 0, wall_t - 1, wall_h, l - 1, primary)
    # East wall
    cuboid_filled(schem, w - wall_t, 1, 0, w - 1, wall_h, l - 1, primary)

    # ---- Interior is air (clear inside walls) ----
    cuboid_filled(schem, wall_t, 1, wall_t, w - wall_t - 1, wall_h - 1, l - wall_t - 1, "minecraft:air")

    # ---- Walkway on top of walls ----
    for x in range(w):
        for z in range(wall_t):
            schem.setBlock((x, wall_h, z), f"{slab}[type=top]")
            schem.setBlock((x, wall_h, l - 1 - z), f"{slab}[type=top]")
    for z in range(l):
        for t in range(wall_t):
            schem.setBlock((t, wall_h, z), f"{slab}[type=top]")
            schem.setBlock((w - 1 - t, wall_h, z), f"{slab}[type=top]")

    # ---- Crenellations ----
    if crenellations:
        top_y = wall_h + 1
        # North and south walls
        for x in range(0, w, 2):
            schem.setBlock((x, top_y, 0), primary)
            schem.setBlock((x, top_y, l - 1), primary)
        # East and west walls
        for z in range(0, l, 2):
            schem.setBlock((0, top_y, z), primary)
            schem.setBlock((w - 1, top_y, z), primary)

    # ---- Corner towers ----
    tower_r = 3
    tower_h = wall_h + 5
    corners = [
        (tower_r, tower_r),              # NW
        (w - 1 - tower_r, tower_r),      # NE
        (tower_r, l - 1 - tower_r),      # SW
        (w - 1 - tower_r, l - 1 - tower_r),  # SE
    ]
    for tx, tz in corners:
        # Tower body
        cylinder(schem, tx, 0, tz, tower_r, tower_h, primary, filled=True)
        # Hollow interior
        cylinder(schem, tx, 1, tz, tower_r - 1, tower_h - 1, "minecraft:air", filled=True)
        # Floor
        circle_xz(schem, tx, 0, tz, tower_r - 1, floor_mat, filled=True)
        # Peaked roof
        cone(schem, tx, tower_h, tz, tower_r + 1, tower_r + 1, stairs)
        # Torch inside
        if interior_lit:
            schem.setBlock((tx, 3, tz), light)

    # ---- Gate (south wall center) ----
    gate_x = w // 2
    gate_z_start = l - wall_t
    for dy in range(1, 5):
        for dx in range(-1, 2):
            for dz in range(wall_t):
                schem.setBlock((gate_x + dx, dy, gate_z_start + dz), "minecraft:air")
    # Arch top
    schem.setBlock((gate_x - 1, 5, l - 1), f"{stairs}[facing=east,half=bottom]")
    schem.setBlock((gate_x,     5, l - 1), primary)
    schem.setBlock((gate_x + 1, 5, l - 1), f"{stairs}[facing=west,half=bottom]")
    # Repeat for inner face
    schem.setBlock((gate_x - 1, 5, l - wall_t), f"{stairs}[facing=east,half=bottom]")
    schem.setBlock((gate_x,     5, l - wall_t), primary)
    schem.setBlock((gate_x + 1, 5, l - wall_t), f"{stairs}[facing=west,half=bottom]")

    # ---- Interior torches ----
    if interior_lit:
        for x in range(wall_t + 1, w - wall_t - 1, 5):
            for z in range(wall_t + 1, l - wall_t - 1, 5):
                schem.setBlock((x, 1, z), light)

    # ---- Weathering — sprinkle mossy/cracked bricks on walls ----
    import random
    random.seed(hash(prompt.get("name", "castle")) % 10000)
    for x in range(w):
        for z in [0, l - 1]:
            for y in range(1, wall_h + 1):
                if random.random() < 0.15:
                    schem.setBlock((x, y, z), secondary)
                elif random.random() < 0.10:
                    schem.setBlock((x, y, z), tertiary)
    for z in range(l):
        for x in [0, w - 1]:
            for y in range(1, wall_h + 1):
                if random.random() < 0.15:
                    schem.setBlock((x, y, z), secondary)
                elif random.random() < 0.10:
                    schem.setBlock((x, y, z), tertiary)

    return schem
