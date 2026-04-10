"""
interiors.py — Reusable furniture placement & room furnishing functions.

Individual furniture pieces (desk, chair, table, chandelier, etc.) and
complete room furnishing routines (office, vault, conference, etc.).
All placement uses blocks.py helpers for correct orientation.
"""

import random

from . import blocks as B
from .primitives import cuboid_filled, flat_plane, line_y

# ═══════════════════════════════════════════════════════════════════
#  INDIVIDUAL FURNITURE PIECES
# ═══════════════════════════════════════════════════════════════════


def place_desk(schem, x, y, z, facing="south", length=3, mat="dark_oak"):
    """L-shaped or straight desk using slabs on fence legs."""
    dx, dz = 0, 0
    if facing in ("south", "north"):
        for i in range(length):
            schem.setBlock((x + i, y, z), B.fence(mat))
            schem.setBlock((x + i, y + 1, z), B.slab(mat, "bottom"))
    else:
        for i in range(length):
            schem.setBlock((x, y, z + i), B.fence(mat))
            schem.setBlock((x, y + 1, z + i), B.slab(mat, "bottom"))


def place_chair(schem, x, y, z, facing="south", mat="dark_oak"):
    """Chair = stair block facing away from desk."""
    schem.setBlock((x, y, z), B.stair(mat, facing))


def place_bookshelf_wall(schem, x1, y, z, x2, height=3, axis="x"):
    """Wall of bookshelves. axis='x' means along x, axis='z' means along z."""
    if axis == "x":
        for bx in range(min(x1, x2), max(x1, x2) + 1):
            for by in range(y, y + height):
                schem.setBlock((bx, by, z), B.BOOKSHELF)
    else:
        for bz in range(min(x1, x2), max(x1, x2) + 1):  # x1/x2 used as z range
            for by in range(y, y + height):
                schem.setBlock((x1, by, bz), B.BOOKSHELF)


def place_chandelier(schem, cx, y, cz, size=3):
    """Hanging chandelier: chains + sea lanterns + fence frame."""
    # Central chain column
    for dy in range(3):
        schem.setBlock((cx, y - dy, cz), B.chain())
    # Lantern at bottom
    schem.setBlock((cx, y - 3, cz), B.SEA_LANTERN)
    # Cross arms
    for dx, dz in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        schem.setBlock((cx + dx, y - 2, cz + dz), B.fence("dark_oak"))
        schem.setBlock((cx + dx, y - 3, cz + dz), B.lantern(hanging=True))
    if size >= 5:
        for dx, dz in [
            (2, 0),
            (-2, 0),
            (0, 2),
            (0, -2),
            (1, 1),
            (-1, 1),
            (1, -1),
            (-1, -1),
        ]:
            schem.setBlock((cx + dx, y - 2, cz + dz), B.fence("dark_oak"))
            schem.setBlock((cx + dx, y - 3, cz + dz), B.lantern(hanging=True))


def place_table(schem, x1, y, z1, x2, z2, mat="dark_oak"):
    """Rectangular table: fence legs at corners, slab surface."""
    xlo, xhi = min(x1, x2), max(x1, x2)
    zlo, zhi = min(z1, z2), max(z1, z2)
    # Legs
    for lx, lz in [(xlo, zlo), (xhi, zlo), (xlo, zhi), (xhi, zhi)]:
        schem.setBlock((lx, y, lz), B.fence(mat))
    # Surface
    for tx in range(xlo, xhi + 1):
        for tz in range(zlo, zhi + 1):
            schem.setBlock((tx, y + 1, tz), B.slab(mat, "bottom"))


def place_counter(schem, x1, y, z, x2, mat="smooth_quartz", facing="south"):
    """Service counter: solid block base + slab top, spans along X."""
    lo, hi = min(x1, x2), max(x1, x2)
    for cx in range(lo, hi + 1):
        schem.setBlock((cx, y, z), mat if ":" in mat else f"minecraft:{mat}")
        schem.setBlock(
            (cx, y + 1, z),
            B.slab(mat.replace("minecraft:", "") if ":" in mat else mat, "bottom"),
        )


def place_counter_z(schem, x, y, z1, z2, mat="smooth_quartz"):
    """Service counter along Z axis."""
    lo, hi = min(z1, z2), max(z1, z2)
    for cz in range(lo, hi + 1):
        schem.setBlock((x, y, cz), mat if ":" in mat else f"minecraft:{mat}")
        schem.setBlock(
            (x, y + 1, cz),
            B.slab(mat.replace("minecraft:", "") if ":" in mat else mat, "bottom"),
        )


def place_potted_plant(schem, x, y, z, plant=None):
    """Place a potted plant, random if no plant specified."""
    plants = [B.POTTED_FERN, B.POTTED_POPPY, B.POTTED_OAK, B.POTTED_AZALEA]
    schem.setBlock((x, y, z), plant or random.choice(plants))


def place_carpet_area(schem, x1, y, z1, x2, z2, color="red"):
    """Place carpet over an area."""
    for cx in range(min(x1, x2), max(x1, x2) + 1):
        for cz in range(min(z1, z2), max(z1, z2) + 1):
            schem.setBlock((cx, y, cz), B.carpet(color))


def place_wall_lights(
    schem, x1, y, z, x2, facing="south", spacing=4, light_type="lantern"
):
    """Place wall-mounted lights along a wall (X axis)."""
    for lx in range(min(x1, x2), max(x1, x2) + 1, spacing):
        if light_type == "lantern":
            schem.setBlock((lx, y, z), B.lantern(hanging=False))
        else:
            schem.setBlock((lx, y, z), B.wall_torch(facing))


def place_floor_pattern(schem, x1, y, z1, x2, z2, block_a, block_b):
    """Checkerboard floor pattern."""
    for fx in range(min(x1, x2), max(x1, x2) + 1):
        for fz in range(min(z1, z2), max(z1, z2) + 1):
            schem.setBlock((fx, y, fz), block_a if (fx + fz) % 2 == 0 else block_b)


def place_pillar_row(schem, positions, y_base, height, block):
    """Place vertical pillars at given (x,z) positions."""
    for px, pz in positions:
        for py in range(y_base, y_base + height):
            schem.setBlock((px, py, pz), block)


def place_wall(schem, x1, y1, z1, x2, y2, z2, block):
    """Generic wall fill — just a cuboid_filled alias with clearer name."""
    cuboid_filled(schem, x1, y1, z1, x2, y2, z2, block)


def place_door_pair(schem, x, y, z, facing="south", mat="dark_oak"):
    """Place a door (lower + upper half)."""
    schem.setBlock((x, y, z), B.door(mat, facing, "lower", "left"))
    schem.setBlock((x, y + 1, z), B.door(mat, facing, "upper", "left"))


def place_double_door(schem, x, y, z, facing="south", mat="dark_oak"):
    """Place a double door (2 blocks wide)."""
    schem.setBlock((x, y, z), B.door(mat, facing, "lower", "right"))
    schem.setBlock((x, y + 1, z), B.door(mat, facing, "upper", "right"))
    schem.setBlock((x + 1, y, z), B.door(mat, facing, "lower", "left"))
    schem.setBlock((x + 1, y + 1, z), B.door(mat, facing, "upper", "left"))


def place_iron_door_pair(schem, x, y, z, facing="south"):
    """Place an iron door."""
    schem.setBlock((x, y, z), B.iron_door(facing, "lower", "left"))
    schem.setBlock((x, y + 1, z), B.iron_door(facing, "upper", "left"))


def place_windows(
    schem, x1, y, z, x2, height=2, block="minecraft:glass_pane", spacing=3
):
    """Place windows along a wall (X axis) with spacing."""
    for wx in range(min(x1, x2) + 1, max(x1, x2), spacing):
        for wy in range(y, y + height):
            schem.setBlock((wx, wy, z), block)


def place_windows_z(
    schem, x, y, z1, z2, height=2, block="minecraft:glass_pane", spacing=3
):
    """Place windows along a wall (Z axis) with spacing."""
    for wz in range(min(z1, z2) + 1, max(z1, z2), spacing):
        for wy in range(y, y + height):
            schem.setBlock((x, wy, wz), block)


# ═══════════════════════════════════════════════════════════════════
#  COMPLETE ROOM FURNISHING FUNCTIONS
# ═══════════════════════════════════════════════════════════════════


def furnish_office(schem, x1, y, z1, x2, z2, facing="south"):
    """Standard office: desk, chair, bookshelf wall, lighting, plant, carpet."""
    w = x2 - x1
    d = z2 - z1
    cx = (x1 + x2) // 2
    cz = (z1 + z2) // 2
    # Carpet
    place_carpet_area(schem, x1 + 1, y, z1 + 1, x2 - 1, z2 - 1, "gray")
    # Desk against back wall
    if facing == "south":
        place_desk(schem, cx - 1, y, z1 + 1, "south", 3)
        place_chair(schem, cx, y, z1 + 2, "north")
    elif facing == "north":
        place_desk(schem, cx - 1, y, z2 - 1, "north", 3)
        place_chair(schem, cx, y, z2 - 2, "south")
    # Bookshelf on side wall
    place_bookshelf_wall(schem, x1 + 1, y + 1, z1 + 1, x1 + 1 + min(4, w - 3), 2, "x")
    # Lantern on desk
    schem.setBlock(
        (cx + 1, y + 2, z1 + 1 if facing == "south" else z2 - 1), B.lantern()
    )
    # Potted plant
    place_potted_plant(schem, x2 - 1, y + 1, z1 + 1)
    # Ceiling light
    schem.setBlock((cx, y + 6, cz), B.lantern(hanging=True))


def furnish_conference_room(schem, x1, y, z1, x2, z2):
    """Conference room: long table, chairs around it, bookshelves, banner."""
    cx = (x1 + x2) // 2
    cz = (z1 + z2) // 2
    tw = min(6, (x2 - x1) - 4)  # table width
    td = min(3, (z2 - z1) - 4)  # table depth
    # Table
    place_table(schem, cx - tw // 2, y, cz - td // 2, cx + tw // 2, cz + td // 2)
    # Chairs on each side
    for i in range(tw + 1):
        tx = cx - tw // 2 + i
        if i % 2 == 0:
            place_chair(schem, tx, y, cz - td // 2 - 1, "south")
            place_chair(schem, tx, y, cz + td // 2 + 1, "north")
    # Head chairs
    place_chair(schem, cx - tw // 2 - 1, y, cz, "east")
    place_chair(schem, cx + tw // 2 + 1, y, cz, "west")
    # Bookshelves along north wall
    place_bookshelf_wall(schem, x1 + 1, y + 1, z1 + 1, x2 - 1, 2, "x")
    # Banner
    schem.setBlock((cx, y + 4, z1 + 1), B.wall_banner("blue", "south"))
    # Ceiling lights
    schem.setBlock((cx - 2, y + 6, cz), B.lantern(hanging=True))
    schem.setBlock((cx + 2, y + 6, cz), B.lantern(hanging=True))
    # Carpet
    place_carpet_area(schem, x1 + 1, y, z1 + 1, x2 - 1, z2 - 1, "blue")


def furnish_vault(schem, x1, y, z1, x2, z2):
    """Bank vault: iron walls, chests in rows, gold display, heavy lighting."""
    w = x2 - x1
    d = z2 - z1
    # Iron block inner walls (1 block layer)
    cuboid_filled(schem, x1, y, z1, x2, y + 5, z1, B.IRON_BLOCK)
    cuboid_filled(schem, x1, y, z2, x2, y + 5, z2, B.IRON_BLOCK)
    cuboid_filled(schem, x1, y, z1, x1, y + 5, z2, B.IRON_BLOCK)
    cuboid_filled(schem, x2, y, z1, x2, y + 5, z2, B.IRON_BLOCK)
    # Clear interior
    cuboid_filled(schem, x1 + 1, y + 1, z1 + 1, x2 - 1, y + 5, z2 - 1, B.AIR)
    # Floor
    flat_plane(schem, x1 + 1, y, z1 + 1, x2 - 1, z2 - 1, B.IRON_BLOCK)
    # Ceiling
    flat_plane(schem, x1 + 1, y + 6, z1 + 1, x2 - 1, z2 - 1, B.IRON_BLOCK)
    # Chest rows along walls
    for rx in range(x1 + 2, x2 - 1, 2):
        schem.setBlock((rx, y + 1, z1 + 1), B.chest("south"))
        schem.setBlock((rx, y + 1, z2 - 1), B.chest("north"))
        schem.setBlock((rx, y + 2, z1 + 1), B.chest("south"))
        schem.setBlock((rx, y + 2, z2 - 1), B.chest("north"))
    # Center display: gold + diamond blocks
    cx = (x1 + x2) // 2
    cz = (z1 + z2) // 2
    schem.setBlock((cx, y + 1, cz), B.GOLD_BLOCK)
    schem.setBlock((cx - 1, y + 1, cz), B.GOLD_BLOCK)
    schem.setBlock((cx + 1, y + 1, cz), B.GOLD_BLOCK)
    schem.setBlock((cx, y + 2, cz), B.DIAMOND_BLOCK)
    schem.setBlock((cx, y + 1, cz - 1), B.EMERALD_BLOCK)
    schem.setBlock((cx, y + 1, cz + 1), B.EMERALD_BLOCK)
    # Iron bars cage around display
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) == 2 or abs(dz) == 2:
                schem.setBlock((cx + dx, y + 1, cz + dz), B.IRON_BARS)
                schem.setBlock((cx + dx, y + 2, cz + dz), B.IRON_BARS)
                schem.setBlock((cx + dx, y + 3, cz + dz), B.IRON_BARS)
    # Glowstone ceiling recessed
    for lx in range(x1 + 2, x2 - 1, 3):
        for lz in range(z1 + 2, z2 - 1, 3):
            schem.setBlock((lx, y + 6, lz), B.GLOWSTONE)
    # Iron door entrance (south wall center, pre-cleared)
    dcx = (x1 + x2) // 2
    schem.setBlock((dcx, y + 1, z2), B.AIR)
    schem.setBlock((dcx, y + 2, z2), B.AIR)
    place_iron_door_pair(schem, dcx, y + 1, z2, "north")


def furnish_break_room(schem, x1, y, z1, x2, z2):
    """Break room: table, chairs, furnace, barrel, crafting table, cauldron."""
    cx = (x1 + x2) // 2
    cz = (z1 + z2) // 2
    # Small table with chairs
    place_table(schem, cx - 1, y, cz - 1, cx + 1, cz)
    place_chair(schem, cx - 2, y, cz, "east")
    place_chair(schem, cx + 2, y, cz, "west")
    place_chair(schem, cx, y, cz - 2, "south")
    place_chair(schem, cx, y, cz + 1, "north")
    # Kitchen counter along north wall
    schem.setBlock((x1 + 1, y + 1, z1 + 1), B.furnace("south"))
    schem.setBlock((x1 + 2, y + 1, z1 + 1), B.smoker("south"))
    schem.setBlock((x1 + 3, y + 1, z1 + 1), B.CRAFTING_TABLE)
    # Storage
    schem.setBlock((x2 - 1, y + 1, z1 + 1), B.barrel("up"))
    schem.setBlock((x2 - 2, y + 1, z1 + 1), B.barrel("up"))
    schem.setBlock((x2 - 1, y + 2, z1 + 1), B.barrel("up"))
    # Cauldron (water cooler)
    schem.setBlock((x2 - 1, y + 1, z2 - 1), B.CAULDRON)
    # Potted plant
    place_potted_plant(schem, x1 + 1, y + 1, z2 - 1)
    # Lighting
    schem.setBlock((cx, y + 6, cz), B.lantern(hanging=True))
    # Carpet
    place_carpet_area(schem, x1 + 1, y, z1 + 1, x2 - 1, z2 - 1, "brown")


def furnish_restroom(schem, x1, y, z1, x2, z2):
    """Restroom: cauldrons as sinks, iron trapdoor mirrors, carpet."""
    w = x2 - x1
    # Sinks along one wall
    for i in range(min(3, w - 2)):
        sx = x1 + 2 + i * 2
        schem.setBlock((sx, y + 1, z1 + 1), B.CAULDRON)
        schem.setBlock((sx, y + 3, z1 + 1), B.iron_trapdoor("south", "top", True))
    # Stalls (trapdoor dividers)
    cz = (z1 + z2) // 2
    for i in range(min(3, w - 2)):
        sx = x1 + 2 + i * 3
        if sx < x2 - 1:
            schem.setBlock((sx, y + 1, z2 - 1), B.CAULDRON)
            line_y(schem, sx + 1, cz, y + 1, y + 3, B.SPRUCE_PLANKS)
    # Floor
    place_carpet_area(schem, x1 + 1, y, z1 + 1, x2 - 1, z2 - 1, "white")
    # Light
    schem.setBlock(((x1 + x2) // 2, y + 6, (z1 + z2) // 2), B.lantern(hanging=True))


def furnish_storage(schem, x1, y, z1, x2, z2):
    """Storage: barrels, chests, shelving."""
    # Row of barrels along walls
    for bx in range(x1 + 1, x2, 2):
        schem.setBlock((bx, y + 1, z1 + 1), B.barrel("up"))
        schem.setBlock((bx, y + 2, z1 + 1), B.barrel("up"))
    for bx in range(x1 + 1, x2, 2):
        schem.setBlock((bx, y + 1, z2 - 1), B.chest("north"))
    # Light
    schem.setBlock(((x1 + x2) // 2, y + 5, (z1 + z2) // 2), B.lantern(hanging=True))
