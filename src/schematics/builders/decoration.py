"""
decoration.py — Interior decoration and furniture builder.

Generates furniture groupings: beds, chests, bookshelves, lanterns,
crafting tables, furnaces, flower pots, barrels, etc.
"""

import mcschematic

# Decoration templates — relative block placements for each furniture type
DECORATION_BLOCKS = {
    "bed": [
        ((0, 0, 0), "minecraft:red_bed[facing=south,part=foot]"),
        ((0, 0, 1), "minecraft:red_bed[facing=south,part=head]"),
    ],
    "chest": [((0, 0, 0), "minecraft:chest[facing=south]")],
    "crafting_table": [((0, 0, 0), "minecraft:crafting_table")],
    "furnace": [((0, 0, 0), "minecraft:furnace[facing=south]")],
    "bookshelf": [((0, 0, 0), "minecraft:bookshelf")],
    "lantern": [((0, 0, 0), "minecraft:lantern")],
    "torch": [((0, 0, 0), "minecraft:torch")],
    "flower_pot": [((0, 0, 0), "minecraft:potted_poppy")],
    "barrel": [((0, 0, 0), "minecraft:barrel[facing=up]")],
    "painting": [
        ((0, 0, 0), "minecraft:air")
    ],  # Paintings are entities; place frame block
    "banner": [((0, 0, 0), "minecraft:white_banner")],
    "anvil": [((0, 0, 0), "minecraft:anvil[facing=south]")],
    "cauldron": [((0, 0, 0), "minecraft:cauldron")],
    "brewing_stand": [((0, 0, 0), "minecraft:brewing_stand")],
    "enchanting_table": [((0, 0, 0), "minecraft:enchanting_table")],
    "armor_stand": [((0, 0, 0), "minecraft:air")],  # Entity-based
    "jukebox": [((0, 0, 0), "minecraft:jukebox")],
    "bell": [((0, 0, 0), "minecraft:bell")],
}


def _get_positions(position_hint, count, w=7, l=7):
    """Generate block positions based on placement hints."""
    positions = []
    if position_hint == "center":
        positions.append((w // 2, 0, l // 2))
    elif position_hint == "corners":
        corners = [(1, 0, 1), (w - 2, 0, 1), (1, 0, l - 2), (w - 2, 0, l - 2)]
        positions.extend(corners[:count])
    elif position_hint == "walls":
        # Spread along north wall
        step = max(1, (w - 2) // max(1, count))
        for i in range(count):
            positions.append((1 + i * step, 0, 0))
    else:  # "auto" or unrecognized
        x, z = 1, 1
        for _ in range(count):
            positions.append((x, 0, z))
            x += 2
            if x >= w - 1:
                x = 1
                z += 2
    return positions


import re

from .t2bm_expander import T2BMExpander

T2BM_Expander = T2BMExpander

# ... (rest of imports and DECORATION_BLOCKS)


def _get_positions(position_hint, count, w=7, l=7):
    """Generate block positions based on placement hints."""
    positions = []
    if position_hint == "center":
        positions.append((w // 2, 0, l // 2))
    elif position_hint == "corners":
        corners = [(1, 0, 1), (w - 2, 0, 1), (1, 0, l - 2), (w - 2, 0, l - 2)]
        positions.extend(corners[:count])
    elif position_hint == "walls":
        # Spread along north wall
        step = max(1, (w - 2) // max(1, count))
        for i in range(count):
            positions.append((1 + i * step, 0, 0))
    else:  # "auto" or unrecognized
        x, z = 1, 1
        for _ in range(count):
            positions.append((x, 0, z))
            x += 2
            if x >= w - 1:
                x = 1
                z += 2
    return positions


def build_decoration(schem: mcschematic.MCSchematic, prompt: dict):
    decorations = prompt.get("decorations", [])
    dims = prompt.get("dimensions", {})
    mats = prompt.get("materials", {})
    w = dims.get("width", 7)
    l = dims.get("length", 7)

    # Regex to parse loop expressions like "x0to12" or "y0,2,4"
    range_parser = re.compile(r"([xyz])(-?\d+)(?:to(-?\d+))?|([xyz])(-?\d+(?:,-?\d+)*)")

    for dec in decorations:
        dec_type = dec.get("type", "lantern")

        if dec_type == "complex_structure":
            pos_offset = dec.get("position", {"x": 0, "y": 0, "z": 0})
            blocks = dec.get("blocks", {})
            for coord_str, mat_key in blocks.items():
                try:
                    # Resolve material key first
                    mat_parts = mat_key.split(".")
                    if len(mat_parts) == 2 and mat_parts[0] == "materials":
                        block_str = mats.get(mat_parts[1], "minecraft:air")
                    else:
                        block_str = mat_key  # Assume literal block string

                    # Handle loops or single points
                    if coord_str.startswith("loop_"):
                        loop_str = coord_str[5:].replace("_", "")
                        matches = range_parser.finditer(loop_str)

                        ranges = {}
                        for match in matches:
                            if match.group(1):  # x0to12 format
                                axis, start, end = (
                                    match.group(1),
                                    int(match.group(2)),
                                    match.group(3),
                                )
                                ranges[axis] = (
                                    range(start, int(end) + 1) if end else [start]
                                )
                            elif match.group(4):  # x0,2,4 format
                                axis, vals = match.group(4), match.group(5)
                                ranges[axis] = [int(v) for v in vals.split(",")]

                        x_coords = ranges.get("x", [0])
                        y_coords = ranges.get("y", [0])
                        z_coords = ranges.get("z", [0])

                        for x in x_coords:
                            for y in y_coords:
                                for z in z_coords:
                                    px = x + pos_offset.get("x", 0)
                                    py = y + pos_offset.get("y", 0)
                                    pz = z + pos_offset.get("z", 0)
                                    schem.setBlock((px, py, pz), block_str)

                    else:  # Handle single coordinate: x1_y2_z3
                        parts = coord_str.split("_")
                        coords = {}
                        for part in parts:
                            if len(part) > 1:
                                coords[part[0]] = int(part[1:])

                        px = coords.get("x", 0) + pos_offset.get("x", 0)
                        py = coords.get("y", 0) + pos_offset.get("y", 0)
                        pz = coords.get("z", 0) + pos_offset.get("z", 0)
                        schem.setBlock((px, py, pz), block_str)

                except (ValueError, IndexError) as e:
                    print(
                        f"  WARN: Could not parse complex_structure item '{coord_str}': {mat_key} -> {e}"
                    )
            continue

        # --- Legacy simple decoration logic ---
        position = dec.get("position", "auto")
        override_block = dec.get("block", None)

        template = DECORATION_BLOCKS.get(dec_type, [((0, 0, 0), "minecraft:lantern")])
        positions = _get_positions(position, 1, w, l)
        if not positions:
            continue
        px, py, pz = positions[0]
        for (dx, dy, dz), block in template:
            final_block = override_block if override_block else block
            schem.setBlock((px + dx, py + dy, pz + dz), final_block)

    return schem
