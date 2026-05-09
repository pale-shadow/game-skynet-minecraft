"""
tower.py — Tower and spire builder.

Generates cylindrical towers with hollow interior, windows, and optional
peaked/dome roofs and crenellations.
"""

import math

import mcschematic

from .primitives import circle_xz, cone, cylinder, flat_plane, line_y


def build_tower(schem: mcschematic.MCSchematic, prompt: dict):
    # Use v5 Industrial Standards (Emerald Mirror Project)
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 9) # Increased default for fluted structure
    h = dims.get("height", 24)
    l = dims.get("length", 9)
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    # v5 Industrial Palette
    primary = mats.get("primary", "minecraft:polished_deepslate_bricks")
    secondary = mats.get("secondary", "minecraft:dark_prismarine")
    pillar_mat = mats.get("pillar", "minecraft:purpur_pillar")
    girder_mat = mats.get("girder", "minecraft:dark_prismarine")
    light_mat = mats.get("light", "minecraft:pearlescent_froglight")
    accent = mats.get("accent", "minecraft:warped_fence")
    roof_mat = mats.get("roof", "minecraft:purpur_block")

    has_roof = feats.get("has_roof", True)
    roof_style = feats.get("roof_style", "peaked")
    hollow = feats.get("hollow", True)
    crenellations = feats.get("crenellations", False)
    interior_lit = feats.get("interior_lit", True)
    has_antenna = feats.get("has_antenna", True)
    top_deck = feats.get("top_deck", False)

    radius = min(w, l) // 2
    cx = w // 2
    cz = l // 2

    # 1. Structural Pillar Layer: 3x3 Fluted Pillars in Corners
    # For a cylindrical tower, we use fluted pillars around the perimeter
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        px = cx + int(round(radius * math.cos(rad)))
        pz = cz + int(round(radius * math.sin(rad)))
        # 3x3 core at each point
        for ix in range(px-1, px+2):
            for iz in range(pz-1, pz+2):
                line_y(schem, ix, iz, 0, h, pillar_mat)

    # 2. Base Layer: Main tower body (Inner shell)
    cylinder(schem, cx, 0, cz, radius - 1, h, primary, filled=True)
    if hollow:
        cylinder(schem, cx, 1, cz, radius - 2, h - 1, "minecraft:air", filled=True)

    # 3. Accent Girder Layer: Grid-iron horizontal rings
    for floor_y in range(0, h, 6):
        circle_xz(schem, cx, floor_y, cz, radius, girder_mat, filled=False)
        # Add lighting within girder intersections
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            lx = cx + int(round(radius * math.cos(rad)))
            lz = cz + int(round(radius * math.sin(rad)))
            schem.setBlock((lx, floor_y, lz), light_mat)

    # Interior floors every 6 blocks
    if hollow and h > 8:
        for floor_y in range(6, h - 2, 6):
            circle_xz(schem, cx, floor_y, cz, radius - 2, secondary, filled=True)

    # Windows (Glass Panes)
    if hollow:
        for wy in range(3, h - 2, 6):
            schem.setBlock((cx + radius - 1, wy, cz), "minecraft:glass_pane")
            schem.setBlock((cx - radius + 1, wy, cz), "minecraft:glass_pane")
            schem.setBlock((cx, wy, cz + radius - 1), "minecraft:glass_pane")
            schem.setBlock((cx, wy, cz - radius + 1), "minecraft:glass_pane")

    # Roof / Top Deck
    if has_roof:
        roof_y = h
        if roof_style == "peaked":
            cone(schem, cx, roof_y, cz, radius + 1, radius + 2, "minecraft:purpur_stairs")
        else:
            circle_xz(schem, cx, roof_y, cz, radius, roof_mat, filled=True)

    # Antenna (Industrial detailing)
    if has_antenna:
        ant_y = h + (radius + 2 if has_roof else 0)
        line_y(schem, cx, cz, ant_y, ant_y + 8, "minecraft:lightning_rod")

    # Door opening at ground level
    if hollow:
        schem.setBlock((cx, 1, cz + radius - 1), "minecraft:air")
        schem.setBlock((cx, 2, cz + radius - 1), "minecraft:air")

    return schem
