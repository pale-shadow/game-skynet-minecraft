"""
primitives.py — Core geometric primitive helpers.

These functions place blocks into an MCSchematic using basic geometry:
filled/hollow cuboids, cylinders, spheres, arches, lines, and circles.
All coords are relative to the schematic origin (0,0,0).
"""
import math
import mcschematic


def cuboid_filled(schem, x1, y1, z1, x2, y2, z2, block):
    """Fill a box from (x1,y1,z1) to (x2,y2,z2) inclusive."""
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            for z in range(min(z1, z2), max(z1, z2) + 1):
                schem.setBlock((x, y, z), block)


def cuboid_hollow(schem, x1, y1, z1, x2, y2, z2, block):
    """Place only the outer shell of a box (6 faces)."""
    xlo, xhi = min(x1, x2), max(x1, x2)
    ylo, yhi = min(y1, y2), max(y1, y2)
    zlo, zhi = min(z1, z2), max(z1, z2)
    for x in range(xlo, xhi + 1):
        for y in range(ylo, yhi + 1):
            for z in range(zlo, zhi + 1):
                if x in (xlo, xhi) or y in (ylo, yhi) or z in (zlo, zhi):
                    schem.setBlock((x, y, z), block)


def cuboid_walls(schem, x1, y1, z1, x2, y2, z2, block):
    """Place only the 4 vertical walls (no floor/ceiling)."""
    xlo, xhi = min(x1, x2), max(x1, x2)
    ylo, yhi = min(y1, y2), max(y1, y2)
    zlo, zhi = min(z1, z2), max(z1, z2)
    for x in range(xlo, xhi + 1):
        for y in range(ylo, yhi + 1):
            for z in range(zlo, zhi + 1):
                if x in (xlo, xhi) or z in (zlo, zhi):
                    schem.setBlock((x, y, z), block)


def flat_plane(schem, x1, y, z1, x2, z2, block):
    """Fill a horizontal plane at height y."""
    for x in range(min(x1, x2), max(x1, x2) + 1):
        for z in range(min(z1, z2), max(z1, z2) + 1):
            schem.setBlock((x, y, z), block)


def line_x(schem, y, z, x1, x2, block):
    """Line along X axis."""
    for x in range(min(x1, x2), max(x1, x2) + 1):
        schem.setBlock((x, y, z), block)


def line_y(schem, x, z, y1, y2, block):
    """Line along Y axis (pillar)."""
    for y in range(min(y1, y2), max(y1, y2) + 1):
        schem.setBlock((x, y, z), block)


def line_z(schem, x, y, z1, z2, block):
    """Line along Z axis."""
    for z in range(min(z1, z2), max(z1, z2) + 1):
        schem.setBlock((x, y, z), block)


def circle_xz(schem, cx, y, cz, radius, block, filled=False):
    """Draw a circle in the XZ plane at height y."""
    r2 = radius * radius
    ri2 = (radius - 1) * (radius - 1) if not filled else -1
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            dist = x * x + z * z
            if dist <= r2 and (filled or dist >= ri2):
                schem.setBlock((cx + x, y, cz + z), block)


def cylinder(schem, cx, y1, cz, radius, height, block, filled=False):
    """Vertical cylinder centered at (cx, cz) from y1 to y1+height-1."""
    for y in range(y1, y1 + height):
        circle_xz(schem, cx, y, cz, radius, block, filled=filled)


def sphere(schem, cx, cy, cz, radius, block, filled=False):
    """Sphere centered at (cx, cy, cz)."""
    r2 = radius * radius
    ri2 = (radius - 1) * (radius - 1) if not filled else -1
    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            for z in range(-radius, radius + 1):
                dist = x * x + y * y + z * z
                if dist <= r2 and (filled or dist >= ri2):
                    schem.setBlock((cx + x, cy + y, cz + z), block)


def dome(schem, cx, cy, cz, radius, block, filled=False):
    """Upper hemisphere centered at (cx, cy, cz)."""
    r2 = radius * radius
    ri2 = (radius - 1) * (radius - 1) if not filled else -1
    for x in range(-radius, radius + 1):
        for y in range(0, radius + 1):
            for z in range(-radius, radius + 1):
                dist = x * x + y * y + z * z
                if dist <= r2 and (filled or dist >= ri2):
                    schem.setBlock((cx + x, cy + y, cz + z), block)


def arch_xz(schem, x1, y, z, x2, height, block):
    """Semi-circular arch spanning from x1 to x2 at z, peaking at y + height."""
    span = abs(x2 - x1)
    radius = span / 2.0
    cx = (x1 + x2) / 2.0
    base_y = y
    for xi in range(min(x1, x2), max(x1, x2) + 1):
        dx = xi - cx
        if abs(dx) <= radius:
            arch_h = int(math.sqrt(max(0, radius * radius - dx * dx)) * (height / radius))
            for yi in range(base_y, base_y + arch_h + 1):
                schem.setBlock((xi, yi, z), block)


def cone(schem, cx, y_base, cz, base_radius, height, block):
    """Cone shape tapering from base_radius at y_base to point at y_base + height."""
    for y_off in range(height):
        r = max(0, int(base_radius * (1.0 - y_off / height)))
        if r == 0:
            schem.setBlock((cx, y_base + y_off, cz), block)
        else:
            circle_xz(schem, cx, y_base + y_off, cz, r, block, filled=True)


def pyramid(schem, x1, y_base, z1, x2, z2, height, block):
    """Square pyramid rising from the base rectangle."""
    for y_off in range(height):
        shrink = y_off
        nx1 = min(x1, x2) + shrink
        nz1 = min(z1, z2) + shrink
        nx2 = max(x1, x2) - shrink
        nz2 = max(z1, z2) - shrink
        if nx1 > nx2 or nz1 > nz2:
            break
        flat_plane(schem, nx1, y_base + y_off, nz1, nx2, nz2, block)
