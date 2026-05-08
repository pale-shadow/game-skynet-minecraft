"""
bridge.py — Bridge and walkway builder.

Generates flat or arched bridges with optional railings.
"""

import math

import mcschematic

from .primitives import cuboid_filled, flat_plane, line_z


def build_bridge(schem: mcschematic.MCSchematic, prompt: dict):
    # Use v5 Industrial Standards (Emerald Mirror Project)
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 7)  # Increased default width for fluted pillars
    h = dims.get("height", 8)  # arch height
    l = dims.get("length", 25)  # span of bridge (Z)
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    # v5 Industrial Palette Defaults
    primary = mats.get("primary", "minecraft:polished_deepslate_bricks")
    secondary = mats.get("secondary", "minecraft:dark_prismarine")
    pillar_mat = mats.get("pillar", "minecraft:purpur_pillar")
    girder_mat = mats.get("girder", "minecraft:dark_prismarine")
    fence_mat = mats.get("fence", "minecraft:warped_fence")
    light_mat = mats.get("light", "minecraft:pearlescent_froglight")
    floor_mat = mats.get("floor", "minecraft:polished_andesite")

    has_railing = feats.get("has_railing", True)
    arch_style = feats.get("arch_style", "round")
    has_rail_bed = feats.get("has_rail_bed", False)
    vaulted_ceiling = feats.get("vaulted_ceiling", True) # v5 prefers vaulted industrial look
    side_walkways = feats.get("side_walkways", True)

    # Base Foundation (Rule of Three: Base Layer)
    flat_plane(schem, 0, 0, 0, w - 1, l - 1, floor_mat)

    # Grid-Iron Girders (Rule of Three: Accent Girder Layer)
    # Longitudinal girders
    line_z(schem, 0, 0, 0, l - 1, girder_mat)
    line_z(schem, w - 1, 0, 0, l - 1, girder_mat)
    # Transverse girders every 5 blocks
    for z in range(0, l, 5):
        for x in range(w):
            schem.setBlock((x, 0, z), girder_mat)

    if has_rail_bed:
        # Place track bed in middle
        mid_x = w // 2
        line_z(schem, mid_x, 0, 0, l - 1, "minecraft:polished_deepslate")
        line_z(schem, mid_x, 1, 0, l - 1, "minecraft:powered_rail[powered=true]")

    # Side Walkways with Industrial Lighting
    if side_walkways:
        for z in range(l):
            schem.setBlock((0, 0, z), primary)
            schem.setBlock((w - 1, 0, z), primary)
            # Integrated Lighting in the floor
            if z % 6 == 0:
                schem.setBlock((0, 0, z), light_mat)
                schem.setBlock((w - 1, 0, z), light_mat)

    # Vaulted Ceiling / Structure
    if vaulted_ceiling:
        for z in range(l):
            from .primitives import arch_xz
            arch_xz(schem, 0, 1, z, w - 1, h, girder_mat)
            # Accent Girder Layer (Warped Fences)
            if z % 2 == 0:
                schem.setBlock((0, 2, z), fence_mat)
                schem.setBlock((w - 1, 2, z), fence_mat)

    # Fluted Pillar Supports (Rule of Three: Structural Pillar Layer)
    # Every 8 blocks, place a 3x3 fluted pillar support
    for z in range(0, l, 8):
        # Support locations
        for sx in [0, w - 3]: # Left and Right supports
            # 3x3 Footprint for Fluted Pillars
            for px in range(sx, sx + 3):
                for pz in range(z, z + 3):
                    # Vertical pillar core
                    for py in range(-5, 0): # Support goes down into the 'foundation'
                        schem.setBlock((px, py, pz), pillar_mat)
            # Recessed Shadows (Stairs around the 3x3 core)
            # Simplified for now: just the core
            
    # Railings
    if has_railing:
        for z in range(l):
            schem.setBlock((0, 1, z), fence_mat)
            schem.setBlock((w - 1, 1, z), fence_mat)

    return schem

