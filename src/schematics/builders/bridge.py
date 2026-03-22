"""
bridge.py — Bridge and walkway builder.

Generates flat or arched bridges with optional railings.
"""
import math
import mcschematic
from .primitives import cuboid_filled, flat_plane, line_z


def build_bridge(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 5)       # width of bridge (X)
    h = dims.get("height", 8)      # arch height
    l = dims.get("length", 25)     # span of bridge (Z)
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    primary  = mats.get("primary",  "minecraft:stone_bricks")
    secondary= mats.get("secondary","minecraft:stone_brick_slab")
    slab     = mats.get("secondary","minecraft:stone_brick_slab")
    fence    = mats.get("fence",    "minecraft:stone_brick_wall")
    roof_mat = mats.get("roof",     primary)
    light    = mats.get("light",    "minecraft:lantern")

    has_railing     = feats.get("has_railing", True)
    arch_style      = feats.get("arch_style", "round")
    has_rail_bed    = feats.get("has_rail_bed", False)
    vaulted_ceiling = feats.get("vaulted_ceiling", False)
    side_walkways   = feats.get("side_walkways", False)

    if arch_style == "none" or (has_rail_bed and arch_style == "round"):
        # Flat bridge or rail bed
        flat_plane(schem, 0, 0, 0, w - 1, l - 1, primary)
        
        if has_rail_bed:
            # Place track bed in middle
            mid_x = w // 2
            line_z(schem, mid_x, 0, 0, l - 1, "minecraft:gray_concrete")
            line_z(schem, mid_x, 1, 0, l - 1, "minecraft:powered_rail[powered=true]")
            
        if side_walkways:
            line_z(schem, 0, 0, 0, l - 1, secondary)
            line_z(schem, w - 1, 0, 0, l - 1, secondary)

        # Vaulted Ceiling
        if vaulted_ceiling:
            for z in range(l):
                from .primitives import arch_xz
                arch_xz(schem, 0, 1, z, w - 1, h, roof_mat)
                # Interior lighting
                if z % 4 == 0:
                    schem.setBlock((w // 2, h, z), light)

        # Railings
        if has_railing and not vaulted_ceiling:
            for z in range(l):
                schem.setBlock((0, 1, z), fence)
                schem.setBlock((w - 1, 1, z), fence)
    else:
        # Arched bridge
        mid_z = l / 2.0
        radius_z = l / 2.0

        for z in range(l):
            # Calculate arch height at this z position
            dz = z - mid_z
            if arch_style == "round":
                if abs(dz) <= radius_z:
                    arch_y = int(math.sqrt(max(0, radius_z * radius_z - dz * dz)) * (h / radius_z))
                else:
                    arch_y = 0
            elif arch_style == "pointed":
                arch_y = int(h * (1.0 - abs(dz) / radius_z))
            else:
                arch_y = 0

            # Deck at arch height
            for x in range(w):
                schem.setBlock((x, arch_y, z), primary)
                # Slab on top for walkway
                schem.setBlock((x, arch_y + 1, z), f"{slab}[type=bottom]" if slab else primary)

            # Support pillars underneath (every 5 blocks)
            if z % 5 == 0:
                for y in range(0, arch_y):
                    schem.setBlock((0, y, z), primary)
                    schem.setBlock((w - 1, y, z), primary)

            # Railings
            if has_railing:
                schem.setBlock((0, arch_y + 2, z), fence)
                schem.setBlock((w - 1, arch_y + 2, z), fence)

    return schem
