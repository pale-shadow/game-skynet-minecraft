"""
cyberdyne.py — Cyberdyne Systems R&D Tower builder.

Generates a tall, redstone-infused tower with:
- Ground floor Railway Integration Lab (track beds, redstone indicators).
- Middle floors Redstone Workshop (circuit design areas).
- Top Mycelial Data Core.
- Mushroom-themed dome roof.
"""

import math

import mcschematic

from . import blocks as B
from . import interiors as I
from .primitives import circle_xz, cuboid_filled, cylinder, dome


def build_cyberdyne(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    W = dims.get("width", 13)
    H = dims.get("height", 40)
    L = dims.get("length", 13)

    radius = min(W, L) // 2
    cx, cz = W // 2, L // 2

    # Materials
    PRIMARY = B.POLISHED_DEEPSLATE
    INFUSION = B.REDSTONE_BLOCK
    INDICATOR = B.REDSTONE_LAMP
    GLASS = B.GLASS_PANE  # Will override with cyan in prompt
    LIGHT = B.SHROOMLIGHT
    ROOF_MAT = "minecraft:red_mushroom_block"
    STALK = "minecraft:mushroom_stem"

    # 1. Foundation & Outer Shell
    # Main stalk (hollow cylinder)
    cylinder(schem, cx, 0, cz, radius, H, PRIMARY, filled=True)
    cylinder(schem, cx, 1, cz, radius - 1, H - 1, B.AIR, filled=True)

    # Redstone "Veins" (Vertical stripes)
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        vx = cx + int(round(radius * math.cos(rad)))
        vz = cz + int(round(radius * math.sin(rad)))
        for vy in range(H):
            # Alternate redstone block and lamp
            mat = INFUSION if vy % 4 < 2 else INDICATOR
            schem.setBlock((vx, vy, vz), mat)

    # 2. Floor Layouts
    floor_height = 6
    for fy in range(0, H, floor_height):
        # Floor platform
        circle_xz(schem, cx, fy, cz, radius - 1, B.SMOOTH_STONE, filled=True)

        # Room logic based on height
        if fy == 0:
            # --- Ground Floor: Railway Integration Lab ---
            # Track bed in center
            for tx in range(cx - 1, cx + 2):
                for tz in range(0, L):
                    if (tx - cx) ** 2 + (tz - cz) ** 2 < radius**2:
                        schem.setBlock((tx, fy, tz), B.POLISHED_ANDESITE)
            # Redstone indicators on walls
            for wy in range(1, 4):
                for angle in range(45, 360, 90):
                    rad = math.radians(angle)
                    wx = cx + int(round((radius - 1) * math.cos(rad)))
                    wz = cz + int(round((radius - 1) * math.sin(rad)))
                    schem.setBlock((wx, fy + wy, wz), INDICATOR)

        elif fy < H - 10:
            # --- Middle Floors: Redstone Workshops ---
            # Placement of circuit tables (desks)
            for angle in [45, 135, 225, 315]:
                rad = math.radians(angle)
                dx = cx + int(round((radius - 3) * math.cos(rad)))
                dz = cz + int(round((radius - 3) * math.sin(rad)))
                I.place_desk(schem, dx, fy + 1, dz, length=2)

        else:
            # --- Top Floor: Mycelial Data Core ---
            # Central pillar of shroomlight and redstone
            for cy in range(fy + 1, fy + 5):
                schem.setBlock((cx, cy, cz), LIGHT)
                for dx, dz in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    schem.setBlock((cx + dx, cy, cz + dz), INFUSION)

    # 3. Windows (Bioluminescent Cyan)
    for wy in range(3, H - 5, 4):
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            wx = cx + int(round(radius * math.cos(rad)))
            wz = cz + int(round(radius * math.sin(rad)))
            schem.setBlock((wx, wy, wz), "minecraft:cyan_stained_glass")
            schem.setBlock((wx, wy + 1, wz), "minecraft:cyan_stained_glass")

    # 4. Mushroom Cap Roof
    roof_y = H
    dome(schem, cx, roof_y, cz, radius + 2, ROOF_MAT, filled=False)
    # Underside of the cap (Gills)
    circle_xz(schem, cx, roof_y, cz, radius + 1, STALK, filled=True)

    return schem
