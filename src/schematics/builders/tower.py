"""
tower.py — Tower and spire builder.

Generates cylindrical towers with hollow interior, windows, and optional
peaked/dome roofs and crenellations.
"""

import math

import mcschematic

from .primitives import circle_xz, cone, cylinder, flat_plane, line_y


def build_tower(schem: mcschematic.MCSchematic, prompt: dict):
    # Use v5 Industrial Standards
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 7)
    h = dims.get("height", 20)
    l = dims.get("length", 7)
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    primary = mats.get("primary", "minecraft:stone_bricks")
    secondary = mats.get("secondary", "minecraft:spruce_planks")
    stairs = mats.get("stairs", "minecraft:stone_brick_stairs")
    glass = mats.get("glass", "minecraft:glass_pane")
    light = mats.get("light", "minecraft:torch")
    accent = mats.get("accent", primary)
    tertiary = mats.get("tertiary", primary)
    roof_mat = mats.get("roof", primary)
    water_mat = mats.get("water", "minecraft:water")

    has_roof = feats.get("has_roof", True)
    roof_style = feats.get("roof_style", "peaked")
    hollow = feats.get("hollow", True)
    crenellations = feats.get("crenellations", False)
    interior_lit = feats.get("interior_lit", True)
    has_water = feats.get("has_water", False)
    has_antenna = feats.get("has_antenna", False)
    top_deck = feats.get("top_deck", False)

    radius = min(w, l) // 2
    cx = w // 2
    cz = l // 2

    # Main tower body — hollow cylinder
    cylinder(schem, cx, 0, cz, radius, h, primary, filled=True)
    if hollow and radius > 1:
        cylinder(schem, cx, 1, cz, radius - 1, h - 1, "minecraft:air", filled=True)

    # Floor
    circle_xz(schem, cx, 0, cz, radius - 1, secondary, filled=True)

    # Water feature at base
    if has_water:
        circle_xz(schem, cx, 0, cz, radius + 2, water_mat, filled=False)

    # Floor platforms every 5 blocks (interior floors for a multi-story tower)
    if hollow and h > 8:
        for floor_y in range(5, h - 2, 5):
            circle_xz(schem, cx, floor_y, cz, radius - 1, secondary, filled=True)

    # Windows (cardinal directions at regular intervals)
    if hollow:
        for wy in range(3, h - 2, 5):
            schem.setBlock((cx + radius, wy, cz), glass)
            schem.setBlock((cx - radius, wy, cz), glass)
            schem.setBlock((cx, wy, cz + radius), glass)
            schem.setBlock((cx, wy, cz - radius), glass)

    # Top Deck
    if top_deck:
        circle_xz(schem, cx, h - 1, cz, radius - 1, secondary, filled=True)
        # Railing
        circle_xz(schem, cx, h, cz, radius, accent, filled=False)

    # Crenellations
    if crenellations:
        top_y = h
        for angle_step in range(0, 360, 15):
            rad = math.radians(angle_step)
            bx = cx + int(round(radius * math.cos(rad)))
            bz = cz + int(round(radius * math.sin(rad)))
            if angle_step % 30 == 0:
                schem.setBlock((bx, top_y, bz), primary)

    # Roof
    if has_roof and not top_deck:
        roof_y = h
        if roof_style == "peaked":
            cone(schem, cx, roof_y, cz, radius + 1, radius + 2, stairs)
        elif roof_style == "dome":
            from .primitives import dome

            dome(schem, cx, roof_y, cz, radius, roof_mat, filled=False)
        else:
            circle_xz(schem, cx, roof_y, cz, radius, stairs, filled=True)

    # Antenna
    if has_antenna:
        ant_y = h + (radius + 2 if has_roof and roof_style == "peaked" else 0)
        line_y(schem, cx, cz, ant_y, ant_y + 5, tertiary)

    # Interior lighting (torches on walls)
    if interior_lit and hollow:
        for wy in range(2, h - 1, 4):
            schem.setBlock(
                (cx + radius - 1, wy, cz), f"minecraft:wall_torch[facing=west]"
            )
            schem.setBlock(
                (cx - radius + 1, wy, cz), f"minecraft:wall_torch[facing=east]"
            )

    # Door opening at ground level (south side)
    if hollow:
        schem.setBlock((cx, 1, cz + radius), "minecraft:air")
        schem.setBlock((cx, 2, cz + radius), "minecraft:air")

    return schem
