"""
house.py — House/cabin structure builder.

Generates rectangular buildings with walls, floor, roof, windows, door, chimney, and lighting.
"""

import mcschematic

from .primitives import cuboid_filled, cuboid_walls, flat_plane, line_y


def build_house(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 9)
    h = dims.get("height", 6)
    l = dims.get("length", 11)
    mats = prompt.get("materials", {})
    feats = prompt.get("features", {})

    primary = mats.get("primary", "minecraft:oak_planks")
    secondary = mats.get("secondary", "minecraft:oak_log[axis=y]")
    floor_mat = mats.get("floor", "minecraft:spruce_planks")
    roof_mat = mats.get("roof", "minecraft:dark_oak_stairs")
    glass = mats.get("glass", "minecraft:glass_pane")
    door_blk = mats.get("door", "minecraft:oak_door")
    light = mats.get("light", "minecraft:lantern")
    accent = mats.get("accent", None)
    tertiary = mats.get("tertiary", mats.get("foundation", "minecraft:cobblestone"))
    slab_mat = mats.get(
        "slab",
        (
            roof_mat.replace("stairs", "slab")
            if "stairs" in roof_mat
            else "minecraft:oak_slab"
        ),
    )

    has_roof = feats.get("has_roof", True)
    roof_style = feats.get("roof_style", "peaked")
    has_floor = feats.get("has_floor", True)
    has_door = feats.get("has_door", True)
    door_pos = feats.get("door_position", "south")
    has_windows = feats.get("has_windows", True)
    win_spacing = feats.get("window_spacing", 3)
    has_chimney = feats.get("has_chimney", False)
    interior_lit = feats.get("interior_lit", True)
    has_found = feats.get("has_foundation", True)
    wall_thick = feats.get("wall_thickness", 1)
    hollow = feats.get("hollow", True)

    # Foundation (one layer below at y=-1)
    if has_found:
        flat_plane(schem, 0, -1, 0, w - 1, l - 1, tertiary)

    # Accent floor (e.g. water-logged leaves)
    floor_y = 0
    if accent:
        if "cherry_leaves" in accent:
            # Special case for growth chamber
            flat_plane(
                schem,
                0,
                0,
                0,
                w - 1,
                l - 1,
                "minecraft:cherry_leaves[waterlogged=true]",
            )
            floor_y = 1
        else:
            flat_plane(schem, 0, 0, 0, w - 1, l - 1, accent)
            floor_y = 1

    # Floor
    if has_floor:
        flat_plane(schem, 0, floor_y, 0, w - 1, l - 1, floor_mat)

    # Walls
    wall_h = h - 1
    for t in range(wall_thick):
        cuboid_walls(schem, t, floor_y + 1, t, w - 1 - t, wall_h, l - 1 - t, primary)

    # Fill interior if not hollow
    if not hollow:
        cuboid_filled(
            schem,
            wall_thick,
            floor_y + 1,
            wall_thick,
            w - 1 - wall_thick,
            wall_h,
            l - 1 - wall_thick,
            primary,
        )

    # Crafter Core
    if tertiary == "minecraft:crafter":
        schem.setBlock(
            (w // 2, floor_y + 1, l // 2), "minecraft:crafter[orientation=up_north]"
        )

    # Corner pillars with secondary material
    for cx, cz in [(0, 0), (w - 1, 0), (0, l - 1), (w - 1, l - 1)]:
        line_y(schem, cx, cz, 1, wall_h, secondary)

    # Ceiling
    flat_plane(schem, 0, wall_h + 1, 0, w - 1, l - 1, primary)

    # Windows
    if has_windows:
        window_y = 2  # 2 blocks up from floor
        # North wall (z=0)
        for x in range(2, w - 2, win_spacing):
            schem.setBlock((x, window_y, 0), glass)
            schem.setBlock((x, window_y + 1, 0), glass)
        # South wall (z=l-1)
        for x in range(2, w - 2, win_spacing):
            schem.setBlock((x, window_y, l - 1), glass)
            schem.setBlock((x, window_y + 1, l - 1), glass)
        # East wall (x=w-1)
        for z in range(2, l - 2, win_spacing):
            schem.setBlock((w - 1, window_y, z), glass)
            schem.setBlock((w - 1, window_y + 1, z), glass)
        # West wall (x=0)
        for z in range(2, l - 2, win_spacing):
            schem.setBlock((0, window_y, z), glass)
            schem.setBlock((0, window_y + 1, z), glass)

    # Door
    if has_door:
        door_facing = door_pos
        if door_pos == "south":
            dx, dz = w // 2, l - 1
        elif door_pos == "north":
            dx, dz = w // 2, 0
        elif door_pos == "east":
            dx, dz = w - 1, l // 2
        else:
            dx, dz = 0, l // 2
        schem.setBlock((dx, 1, dz), f"{door_blk}[half=lower,facing={door_facing}]")
        schem.setBlock((dx, 2, dz), f"{door_blk}[half=upper,facing={door_facing}]")

    # Roof
    if has_roof:
        roof_base_y = wall_h + 2
        if roof_style == "peaked":
            # Gabled roof along the length (Z axis)
            for layer in range(w // 2 + 1):
                y = roof_base_y + layer
                x_left = layer
                x_right = w - 1 - layer
                if x_left > x_right:
                    break
                for z in range(0, l):
                    if x_left == x_right:
                        # Peak — use slab
                        schem.setBlock((x_left, y, z), slab_mat)
                    else:
                        schem.setBlock(
                            (x_left, y, z), f"{roof_mat}[facing=east,half=bottom]"
                        )
                        schem.setBlock(
                            (x_right, y, z), f"{roof_mat}[facing=west,half=bottom]"
                        )
        elif roof_style == "flat":
            flat_plane(schem, 0, roof_base_y, 0, w - 1, l - 1, slab_mat)
        else:
            # Default flat
            flat_plane(schem, 0, roof_base_y, 0, w - 1, l - 1, slab_mat)

    # Chimney
    if has_chimney:
        chimney_x = w - 2
        chimney_z = 1
        chimney_top = (
            (wall_h + 2 + w // 2 + 2) if roof_style == "peaked" else wall_h + 4
        )
        for y in range(wall_h + 1, chimney_top):
            schem.setBlock((chimney_x, y, chimney_z), "minecraft:bricks")
        schem.setBlock(
            (chimney_x, chimney_top, chimney_z), "minecraft:campfire[lit=true]"
        )

    # Interior lighting
    if interior_lit:
        # Hang lanterns from ceiling
        ceil_y = wall_h
        for x in range(2, w - 2, 4):
            for z in range(2, l - 2, 4):
                schem.setBlock(
                    (x, ceil_y, z),
                    f"{light}[hanging=true]" if "lantern" in light else light,
                )

    return schem
