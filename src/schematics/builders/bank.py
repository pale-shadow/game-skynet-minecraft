"""
bank.py — Grand bank builder with full interior.

Generates a massive, highly detailed bank with:
- Grand double-height lobby with quartz pillars and chandeliers
- Teller counter area with individual stations
- Iron-walled vault with treasure display
- Multiple furnished offices, conference room, break room
- Upper floors with more offices and a manager suite
- Exterior columns, cornice detailing, grand staircase entrance
- Decorative roof with parapet
"""

import random

import mcschematic

from . import blocks as B
from . import interiors as I
from .primitives import cuboid_filled, flat_plane, line_x, line_y, line_z


def build_bank(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    W = dims.get("width", 80)
    H = dims.get("height", 60)
    L = dims.get("length", 80)

    # ═══════════════════════════════════════════════════════════════
    #  CONSTANTS
    # ═══════════════════════════════════════════════════════════════
    EXT = 2  # Exterior wall thickness
    FLOOR_SP = 9  # Floor spacing (1 slab + 8 air)
    GF = 2  # Ground floor slab Y
    F1 = GF + FLOOR_SP  # 11 - Second floor
    F2 = F1 + FLOOR_SP  # 20 - Third floor
    F3 = F2 + FLOOR_SP  # 29 - Fourth floor
    ROOF = F3 + FLOOR_SP  # 38 - Roof slab

    INT_H = 7  # Usable interior blocks above slab (y+1..y+7)
    IX1, IX2 = EXT, W - EXT - 1
    IZ1, IZ2 = EXT, L - EXT - 1

    # Materials
    WALL = B.STONE_BRICKS
    ACCENT = B.CHISELED_STONE_B
    TRIM = B.SMOOTH_QUARTZ
    PILR = B.QUARTZ_PILLAR
    FLOOR = B.POLISHED_DIORITE
    FLOOR2 = B.POLISHED_ANDESITE
    CARP = "red"
    CEIL = B.SMOOTH_STONE

    # ═══════════════════════════════════════════════════════════════
    #  1. FOUNDATION
    # ═══════════════════════════════════════════════════════════════
    flat_plane(schem, 0, 0, 0, W - 1, L - 1, B.COBBLESTONE)
    flat_plane(schem, 0, 1, 0, W - 1, L - 1, WALL)

    # ═══════════════════════════════════════════════════════════════
    #  2. EXTERIOR SHELL (all floors)
    # ═══════════════════════════════════════════════════════════════
    for floor_y in [GF, F1, F2, F3]:
        # Floor slab
        flat_plane(schem, 0, floor_y, 0, W - 1, L - 1, WALL)
        # Walls (4 faces, EXT thick)
        fy1, fy2 = floor_y + 1, floor_y + FLOOR_SP - 1
        # North
        cuboid_filled(schem, 0, fy1, 0, W - 1, fy2, EXT - 1, WALL)
        # South
        cuboid_filled(schem, 0, fy1, L - EXT, W - 1, fy2, L - 1, WALL)
        # West
        cuboid_filled(schem, 0, fy1, 0, EXT - 1, fy2, L - 1, WALL)
        # East
        cuboid_filled(schem, W - EXT, fy1, 0, W - 1, fy2, L - 1, WALL)
        # Clear interior air
        cuboid_filled(schem, IX1, fy1, IZ1, IX2, fy2, IZ2, B.AIR)

    # Roof slab
    flat_plane(schem, 0, ROOF, 0, W - 1, L - 1, WALL)

    # ═══════════════════════════════════════════════════════════════
    #  3. EXTERIOR DECORATION
    # ═══════════════════════════════════════════════════════════════
    _build_exterior_detail(
        schem, W, H, L, GF, F1, F2, F3, ROOF, EXT, WALL, ACCENT, TRIM, PILR
    )

    # ═══════════════════════════════════════════════════════════════
    #  4. GROUND FLOOR LAYOUT
    # ═══════════════════════════════════════════════════════════════
    _build_ground_floor(
        schem, W, L, GF, FLOOR_SP, IX1, IX2, IZ1, IZ2, WALL, FLOOR, CEIL, TRIM, CARP
    )

    # ═══════════════════════════════════════════════════════════════
    #  5. GRAND LOBBY (double height — remove F1 floor in lobby area)
    # ═══════════════════════════════════════════════════════════════
    _build_grand_lobby(schem, W, L, GF, F1, FLOOR_SP, IX1, IX2, FLOOR, TRIM, PILR, CARP)

    # ═══════════════════════════════════════════════════════════════
    #  6. UPPER FLOORS (F1, F2, F3)
    # ═══════════════════════════════════════════════════════════════
    _build_upper_floor(schem, W, L, F1, IX1, IX2, IZ1, IZ2, WALL, FLOOR2, CEIL, "F1")
    _build_upper_floor(schem, W, L, F2, IX1, IX2, IZ1, IZ2, WALL, FLOOR2, CEIL, "F2")
    _build_upper_floor(schem, W, L, F3, IX1, IX2, IZ1, IZ2, WALL, FLOOR2, CEIL, "F3")

    # ═══════════════════════════════════════════════════════════════
    #  7. ROOF STRUCTURE
    # ═══════════════════════════════════════════════════════════════
    _build_roof(schem, W, H, L, ROOF, WALL, ACCENT, TRIM)

    # ═══════════════════════════════════════════════════════════════
    #  8. GRAND ENTRANCE
    # ═══════════════════════════════════════════════════════════════
    _build_entrance(schem, W, L, GF, WALL, TRIM)

    return schem


# ═══════════════════════════════════════════════════════════════════
#  EXTERIOR DETAILS
# ═══════════════════════════════════════════════════════════════════
def _build_exterior_detail(
    schem, W, H, L, GF, F1, F2, F3, ROOF, EXT, WALL, ACCENT, TRIM, PILR
):
    # Cornice lines at each floor boundary
    for fy in [GF, F1, F2, F3, ROOF]:
        cy = fy
        # North/South cornices
        for x in range(W):
            schem.setBlock((x, cy, 0), TRIM)
            schem.setBlock((x, cy, L - 1), TRIM)
        # East/West cornices
        for z in range(L):
            schem.setBlock((0, cy, z), TRIM)
            schem.setBlock((W - 1, cy, z), TRIM)

    # Chiseled accents at corners of each floor
    for fy in [GF, F1, F2, F3]:
        for dy in range(1, 9):
            for cx, cz in [(0, 0), (W - 1, 0), (0, L - 1), (W - 1, L - 1)]:
                schem.setBlock((cx, fy + dy, cz), ACCENT)

    # Exterior columns on south facade (entrance side)
    col_spacing = W // 6
    for i in range(1, 6):
        cx = i * col_spacing
        if abs(cx - W // 2) < 4:
            continue  # skip near door
        for cy in range(GF + 1, ROOF):
            schem.setBlock((cx, cy, L - 1), B.pillar(PILR, "y"))

    # Windows on all exterior walls (floors 1-4)
    for fy in [GF, F1, F2, F3]:
        wy = fy + 3  # Window starts 3 above floor
        wh = 3  # Window height
        # North windows
        I.place_windows(schem, 4, wy, 0, W - 4, wh, B.GLASS_PANE, 5)
        # South windows (skip entrance area)
        for wx in range(4, W - 4, 5):
            if abs(wx - W // 2) > 5:
                for wdy in range(wh):
                    schem.setBlock((wx, wy + wdy, L - 1), B.GLASS_PANE)
        # East windows
        I.place_windows_z(schem, W - 1, wy, 4, L - 4, wh, B.GLASS_PANE, 5)
        # West windows
        I.place_windows_z(schem, 0, wy, 4, L - 4, wh, B.GLASS_PANE, 5)


# ═══════════════════════════════════════════════════════════════════
#  GROUND FLOOR INTERIOR LAYOUT
# ═══════════════════════════════════════════════════════════════════
def _build_ground_floor(
    schem, W, L, GF, FLOOR_SP, IX1, IX2, IZ1, IZ2, WALL, FLOOR_BLK, CEIL, TRIM, CARP
):
    fy = GF  # Floor slab Y
    cy = fy + 1  # Interior starts
    iw = IX2 - IX1  # Interior width
    il = IZ2 - IZ1  # Interior length

    # ── Room boundaries (Z divisions from north) ──
    # z=IZ1..IZ1+17:     North rooms (vault, offices)
    # z=IZ1+18:          Wall
    # z=IZ1+19..IZ1+31:  Mid section (corridor, break room, conf room)
    # z=IZ1+32:          Wall
    # z=IZ1+33..IZ1+47:  Teller section
    # z=IZ1+48:          Wall
    # z=IZ1+49..IZ2:     Grand lobby

    NR_Z2 = IZ1 + 17  # North rooms south edge
    MID_Z1 = IZ1 + 19  # Mid section north edge
    MID_Z2 = IZ1 + 31
    TLR_Z1 = IZ1 + 33  # Teller area north edge
    TLR_Z2 = IZ1 + 47
    LOB_Z1 = IZ1 + 49  # Lobby north edge

    # Side room east/west split
    SIDE_W = 18  # Width of side rooms
    WR_X2 = IX1 + SIDE_W - 1  # West rooms east edge
    ER_X1 = IX2 - SIDE_W + 1  # East rooms west edge

    # ── Horizontal walls ──
    cuboid_filled(schem, IX1, cy, IZ1 + 18, IX2, cy + INT_H, IZ1 + 18, WALL)
    cuboid_filled(schem, IX1, cy, IZ1 + 32, IX2, cy + INT_H, IZ1 + 32, WALL)
    cuboid_filled(schem, IX1, cy, IZ1 + 48, IX2, cy + INT_H, IZ1 + 48, WALL)

    # ── Clear door openings in horizontal walls ──
    mid_x = (IX1 + IX2) // 2
    # Lobby → Teller (wide opening)
    cuboid_filled(schem, mid_x - 8, cy, IZ1 + 48, mid_x + 8, cy + 4, IZ1 + 48, B.AIR)
    # Teller → Corridor
    cuboid_filled(schem, mid_x - 3, cy, IZ1 + 32, mid_x + 3, cy + 3, IZ1 + 32, B.AIR)
    # Corridor → Vault area
    cuboid_filled(schem, mid_x - 3, cy, IZ1 + 18, mid_x + 3, cy + 3, IZ1 + 18, B.AIR)

    # ── Vertical walls (side rooms) ──
    INT_H_VAL = 7
    # West side wall
    cuboid_filled(schem, WR_X2 + 1, cy, IZ1, WR_X2 + 1, cy + INT_H_VAL, TLR_Z2, WALL)
    # East side wall
    cuboid_filled(schem, ER_X1 - 1, cy, IZ1, ER_X1 - 1, cy + INT_H_VAL, TLR_Z2, WALL)

    # ── Side room horizontal dividers ──
    # West: Office NW / Break Room / Storage
    cuboid_filled(schem, IX1, cy, NR_Z2 + 1, WR_X2, cy + INT_H_VAL, NR_Z2 + 1, WALL)
    cuboid_filled(schem, IX1, cy, MID_Z2 + 1, WR_X2, cy + INT_H_VAL, MID_Z2 + 1, WALL)
    # East: Office NE / Conference / Restroom
    cuboid_filled(schem, ER_X1, cy, NR_Z2 + 1, IX2, cy + INT_H_VAL, NR_Z2 + 1, WALL)
    cuboid_filled(schem, ER_X1, cy, MID_Z2 + 1, IX2, cy + INT_H_VAL, MID_Z2 + 1, WALL)

    # ── Vault walls (thicker) ──
    VLT_X1 = WR_X2 + 3
    VLT_X2 = ER_X1 - 3
    VLT_Z1 = IZ1
    VLT_Z2 = NR_Z2
    # Vault side walls
    cuboid_filled(schem, VLT_X1 - 1, cy, VLT_Z1, VLT_X1 - 1, cy + 6, VLT_Z2, WALL)
    cuboid_filled(schem, VLT_X2 + 1, cy, VLT_Z1, VLT_X2 + 1, cy + 6, VLT_Z2, WALL)
    # Small offices flanking vault
    # Manager office: WR_X2+2..VLT_X1-2, z=IZ1..NR_Z2
    # Security office: VLT_X2+2..ER_X1-2, z=IZ1..NR_Z2

    # ── Room doors ──
    # West side doors (into corridor)
    for dz in [IZ1 + 9, MID_Z1 + 6, TLR_Z1 + 6]:
        if dz <= TLR_Z2:
            cuboid_filled(schem, WR_X2 + 1, cy, dz, WR_X2 + 1, cy + 2, dz, B.AIR)
            I.place_door_pair(schem, WR_X2 + 1, cy, dz, "east")
    # East side doors
    for dz in [IZ1 + 9, MID_Z1 + 6, TLR_Z1 + 6]:
        if dz <= TLR_Z2:
            cuboid_filled(schem, ER_X1 - 1, cy, dz, ER_X1 - 1, cy + 2, dz, B.AIR)
            I.place_door_pair(schem, ER_X1 - 1, cy, dz, "west")

    # ── Floor finishes ──
    # Lobby floor (polished diorite + carpet runner)
    I.place_floor_pattern(
        schem, IX1, fy, LOB_Z1, IX2, IZ2, B.POLISHED_DIORITE, B.POLISHED_GRANITE
    )
    I.place_carpet_area(schem, mid_x - 3, fy + 1, LOB_Z1 + 2, mid_x + 3, IZ2 - 2, CARP)
    # Teller area floor
    flat_plane(schem, IX1, fy, TLR_Z1, IX2, TLR_Z2, B.POLISHED_ANDESITE)
    # Corridor floor
    flat_plane(schem, WR_X2 + 2, fy, MID_Z1, ER_X1 - 2, MID_Z2, B.SMOOTH_STONE)
    # Side rooms — dark oak planks
    flat_plane(schem, IX1, fy, IZ1, WR_X2, NR_Z2, B.DARK_OAK_PLANKS)
    flat_plane(schem, ER_X1, fy, IZ1, IX2, NR_Z2, B.DARK_OAK_PLANKS)
    flat_plane(schem, IX1, fy, MID_Z1, WR_X2, MID_Z2, B.DARK_OAK_PLANKS)
    flat_plane(schem, ER_X1, fy, MID_Z1, IX2, MID_Z2, B.DARK_OAK_PLANKS)
    flat_plane(schem, IX1, fy, TLR_Z1, WR_X2, TLR_Z2, B.SPRUCE_PLANKS)
    flat_plane(schem, ER_X1, fy, TLR_Z1, IX2, TLR_Z2, B.SPRUCE_PLANKS)

    # ── FURNISH ROOMS ──
    # Office NW
    I.furnish_office(schem, IX1, fy, IZ1, WR_X2, NR_Z2, "south")
    # Office NE
    I.furnish_office(schem, ER_X1, fy, IZ1, IX2, NR_Z2, "south")
    # Vault
    I.furnish_vault(schem, VLT_X1, fy, VLT_Z1, VLT_X2, VLT_Z2)
    # Break room (west mid)
    I.furnish_break_room(schem, IX1, fy, MID_Z1, WR_X2, MID_Z2)
    # Conference room (east mid)
    I.furnish_conference_room(schem, ER_X1, fy, MID_Z1, IX2, MID_Z2)
    # Storage (west teller side)
    I.furnish_storage(schem, IX1, fy, TLR_Z1, WR_X2, TLR_Z2)
    # Restroom (east teller side)
    I.furnish_restroom(schem, ER_X1, fy, TLR_Z1, IX2, TLR_Z2)

    # ── Teller counter ──
    _build_teller_counter(schem, WR_X2 + 3, fy, TLR_Z1 + 3, ER_X1 - 3)

    # ── Corridor lighting ──
    for lx in range(WR_X2 + 4, ER_X1 - 2, 5):
        for lz in range(MID_Z1 + 2, MID_Z2, 5):
            schem.setBlock((lx, fy + INT_H_VAL + 1, lz), B.lantern(hanging=True))


INT_H = 7  # Module-level for helper access


def _build_teller_counter(schem, x1, fy, z, x2):
    """Teller counter with individual service windows."""
    # Counter base
    I.place_counter(schem, x1, fy + 1, z, x2, "minecraft:smooth_quartz")
    # Iron bars above counter (glass partition)
    for tx in range(x1, x2 + 1):
        schem.setBlock((tx, fy + 3, z), B.IRON_BARS)
        schem.setBlock((tx, fy + 4, z), B.IRON_BARS)
    # Service openings (every 8 blocks)
    for wx in range(x1 + 3, x2, 8):
        schem.setBlock((wx, fy + 3, z), B.AIR)
        schem.setBlock((wx, fy + 4, z), B.AIR)
    # Chairs behind counter
    for cx in range(x1 + 3, x2, 8):
        I.place_chair(schem, cx, fy + 1, z - 1, "south", "dark_oak")
    # Lanterns above each station
    for lx in range(x1 + 3, x2, 8):
        schem.setBlock((lx, fy + 6, z), B.lantern(hanging=True))


# ═══════════════════════════════════════════════════════════════════
#  GRAND LOBBY (double height)
# ═══════════════════════════════════════════════════════════════════
def _build_grand_lobby(
    schem, W, L, GF, F1, FLOOR_SP, IX1, IX2, FLOOR_BLK, TRIM, PILR, CARP
):
    LOB_Z1 = 2 + 49  # IZ1 + 49
    LOB_Z2 = L - 3  # IZ2

    # Remove second floor slab in lobby area to create double height
    cuboid_filled(schem, IX1, F1, LOB_Z1, IX2, F1, LOB_Z2, B.AIR)
    # Also clear second floor walls in lobby area
    cuboid_filled(schem, IX1, F1 + 1, LOB_Z1, IX2, F1 + FLOOR_SP - 1, LOB_Z2, B.AIR)

    # Grand pillars (floor to double-height ceiling)
    mid_x = (IX1 + IX2) // 2
    pillar_h = FLOOR_SP * 2 - 2  # Double height
    col_positions = []
    for px in range(IX1 + 6, IX2 - 4, 10):
        for pz in [LOB_Z1 + 4, LOB_Z2 - 4]:
            col_positions.append((px, pz))
    I.place_pillar_row(schem, col_positions, GF + 1, pillar_h, B.pillar(PILR, "y"))

    # Pillar bases and capitals
    for px, pz in col_positions:
        schem.setBlock((px, GF + 1, pz), TRIM)
        schem.setBlock((px, GF + pillar_h, pz), TRIM)

    # Chandeliers
    ceil_y = F1 + FLOOR_SP - 1
    for chx in range(IX1 + 10, IX2 - 8, 16):
        I.place_chandelier(schem, chx, ceil_y, (LOB_Z1 + LOB_Z2) // 2, 5)

    # Reception desk near entrance
    desk_z = LOB_Z2 - 6
    desk_x = mid_x - 5
    I.place_counter(
        schem, desk_x, GF + 1, desk_z, desk_x + 10, "minecraft:dark_oak_planks"
    )
    # Plants flanking desk
    I.place_potted_plant(schem, desk_x - 1, GF + 1, desk_z)
    I.place_potted_plant(schem, desk_x + 11, GF + 1, desk_z)

    # Waiting benches
    for bz in range(LOB_Z1 + 8, LOB_Z2 - 10, 5):
        for bx in [IX1 + 3, IX2 - 3]:
            facing = "east" if bx < mid_x else "west"
            I.place_chair(schem, bx, GF + 1, bz, facing)
            I.place_chair(schem, bx, GF + 1, bz + 1, facing)
            I.place_chair(schem, bx, GF + 1, bz + 2, facing)

    # Floor carpet runner (center)
    I.place_carpet_area(
        schem, mid_x - 4, GF + 1, LOB_Z1 + 2, mid_x + 4, LOB_Z2 - 2, CARP
    )

    # Wall banners
    for bx in range(IX1 + 8, IX2 - 6, 12):
        schem.setBlock((bx, GF + 8, LOB_Z1), B.wall_banner("blue", "south"))


# ═══════════════════════════════════════════════════════════════════
#  UPPER FLOORS
# ═══════════════════════════════════════════════════════════════════
def _build_upper_floor(
    schem, W, L, floor_y, IX1, IX2, IZ1, IZ2, WALL, FLOOR_BLK, CEIL, tag
):
    fy = floor_y
    cy = fy + 1
    mid_x = (IX1 + IX2) // 2
    mid_z = (IZ1 + IZ2) // 2

    # Skip lobby area for F1 (already double-height)
    LOB_Z1 = IZ1 + 49
    if tag == "F1":
        work_z2 = LOB_Z1 - 1
    else:
        work_z2 = IZ2

    # Floor
    flat_plane(schem, IX1, fy, IZ1, IX2, work_z2, FLOOR_BLK)

    # Central corridor (north-south)
    CORR_X1 = mid_x - 3
    CORR_X2 = mid_x + 3
    # West wall of corridor
    cuboid_filled(schem, CORR_X1 - 1, cy, IZ1, CORR_X1 - 1, cy + INT_H, work_z2, WALL)
    # East wall of corridor
    cuboid_filled(schem, CORR_X2 + 1, cy, IZ1, CORR_X2 + 1, cy + INT_H, work_z2, WALL)
    # Clear corridor
    cuboid_filled(schem, CORR_X1, cy, IZ1, CORR_X2, cy + INT_H, work_z2, B.AIR)

    # Divide west and east blocks into offices (every 16 blocks along Z)
    office_depth = 14
    room_idx = 0
    for rz1 in range(IZ1, work_z2 - office_depth + 1, office_depth + 1):
        rz2 = min(rz1 + office_depth, work_z2)
        # South wall of this room
        if rz2 < work_z2:
            cuboid_filled(
                schem, IX1, cy, rz2 + 1, CORR_X1 - 2, cy + INT_H, rz2 + 1, WALL
            )
            cuboid_filled(
                schem, CORR_X2 + 2, cy, rz2 + 1, IX2, cy + INT_H, rz2 + 1, WALL
            )

        # West room
        wx1, wx2 = IX1, CORR_X1 - 2
        # Door into corridor
        cuboid_filled(
            schem, CORR_X1 - 1, cy, rz1 + 5, CORR_X1 - 1, cy + 2, rz1 + 5, B.AIR
        )
        I.place_door_pair(schem, CORR_X1 - 1, cy, rz1 + 5, "east")
        # Floor
        flat_plane(schem, wx1, fy, rz1, wx2, rz2, B.DARK_OAK_PLANKS)

        # East room
        ex1, ex2 = CORR_X2 + 2, IX2
        cuboid_filled(
            schem, CORR_X2 + 1, cy, rz1 + 5, CORR_X2 + 1, cy + 2, rz1 + 5, B.AIR
        )
        I.place_door_pair(schem, CORR_X2 + 1, cy, rz1 + 5, "west")
        flat_plane(schem, ex1, fy, rz1, ex2, rz2, B.DARK_OAK_PLANKS)

        # Furnish alternating room types
        if room_idx % 3 == 0:
            I.furnish_office(schem, wx1, fy, rz1, wx2, rz2, "south")
            I.furnish_office(schem, ex1, fy, rz1, ex2, rz2, "south")
        elif room_idx % 3 == 1:
            I.furnish_conference_room(schem, wx1, fy, rz1, wx2, rz2)
            I.furnish_office(schem, ex1, fy, rz1, ex2, rz2, "south")
        else:
            I.furnish_office(schem, wx1, fy, rz1, wx2, rz2, "north")
            I.furnish_conference_room(schem, ex1, fy, rz1, ex2, rz2)
        room_idx += 1

    # Corridor lighting
    for lz in range(IZ1 + 3, work_z2, 5):
        schem.setBlock((mid_x, fy + INT_H + 1, lz), B.lantern(hanging=True))

    # Corridor carpet
    I.place_carpet_area(schem, CORR_X1, fy + 1, IZ1 + 1, CORR_X2, work_z2 - 1, "gray")

    # F1 mezzanine railing overlooking lobby
    if tag == "F1":
        for mx in range(IX1, IX2 + 1):
            schem.setBlock((mx, fy + 1, LOB_Z1), B.fence("dark_oak"))
            schem.setBlock((mx, fy + 2, LOB_Z1), B.fence("dark_oak"))


# ═══════════════════════════════════════════════════════════════════
#  GRAND ENTRANCE
# ═══════════════════════════════════════════════════════════════════
def _build_entrance(schem, W, L, GF, WALL, TRIM):
    mid_x = W // 2
    # Grand steps (5 blocks deep, 3 steps)
    for step in range(3):
        flat_plane(
            schem, mid_x - 8 + step, step, L, mid_x + 8 - step, L + 4 - step, TRIM
        )
    # Wide door opening
    cuboid_filled(schem, mid_x - 3, GF + 1, L - 2, mid_x + 3, GF + 5, L - 1, B.AIR)
    # Double doors
    I.place_double_door(schem, mid_x - 1, GF + 1, L - 1, "north", "dark_oak")
    # Flanking lanterns
    schem.setBlock((mid_x - 4, GF + 3, L - 1), B.lantern())
    schem.setBlock((mid_x + 4, GF + 3, L - 1), B.lantern())
    # Arch detail above door
    schem.setBlock((mid_x - 3, GF + 5, L - 1), B.stair("stone_brick", "east", "bottom"))
    for ax in range(mid_x - 2, mid_x + 3):
        schem.setBlock((ax, GF + 6, L - 1), TRIM)
    schem.setBlock((mid_x + 3, GF + 5, L - 1), B.stair("stone_brick", "west", "bottom"))


# ═══════════════════════════════════════════════════════════════════
#  ROOF STRUCTURE
# ═══════════════════════════════════════════════════════════════════
def _build_roof(schem, W, H, L, ROOF, WALL, ACCENT, TRIM):
    # Parapet walls
    for x in range(W):
        schem.setBlock((x, ROOF + 1, 0), WALL)
        schem.setBlock((x, ROOF + 1, L - 1), WALL)
    for z in range(L):
        schem.setBlock((0, ROOF + 1, z), WALL)
        schem.setBlock((W - 1, ROOF + 1, z), WALL)

    # Crenellations
    for x in range(0, W, 2):
        schem.setBlock((x, ROOF + 2, 0), ACCENT)
        schem.setBlock((x, ROOF + 2, L - 1), ACCENT)
    for z in range(0, L, 2):
        schem.setBlock((0, ROOF + 2, z), ACCENT)
        schem.setBlock((W - 1, ROOF + 2, z), ACCENT)

    # Corner pinnacles
    for cx, cz in [(1, 1), (W - 2, 1), (1, L - 2), (W - 2, L - 2)]:
        for py in range(ROOF + 1, ROOF + 6):
            schem.setBlock((cx, py, cz), WALL)
        schem.setBlock((cx, ROOF + 6, cz), B.slab("stone_brick", "bottom"))

    # Central dome
    dome_cx = W // 2
    dome_cz = L // 2
    dome_r = min(W, L) // 6
    dome_h = min(H - ROOF - 3, 18)
    for y_off in range(dome_h):
        r = max(0, int(dome_r * (1.0 - (y_off / dome_h) ** 1.5)))
        if r == 0:
            schem.setBlock((dome_cx, ROOF + 1 + y_off, dome_cz), TRIM)
            break
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if dx * dx + dz * dz <= r * r:
                    dist = dx * dx + dz * dz
                    if dist >= (r - 1) * (r - 1) or y_off == 0:
                        schem.setBlock(
                            (dome_cx + dx, ROOF + 1 + y_off, dome_cz + dz), WALL
                        )

    # Spire on top
    spire_base = ROOF + 1 + dome_h
    for sy in range(spire_base, min(spire_base + 5, H)):
        schem.setBlock((dome_cx, sy, dome_cz), ACCENT)
    if spire_base + 5 < H:
        schem.setBlock((dome_cx, spire_base + 5, dome_cz), B.lantern())
