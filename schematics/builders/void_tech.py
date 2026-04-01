"""
void_tech.py — Core 'Void-Tech' architectural logic for Skynet.

Provides helper functions to apply the V7/V8 standards (Ribbing, Hydro-Pods,
Kinetic Signaling) to any structure.
"""

import math
import random


def apply_void_palette(prompt):
    """Overrides the prompt materials with V7 Void-Tech standards."""
    mats = prompt.get("materials", {})
    mats.update(
        {
            "primary": "minecraft:polished_tuff",
            "secondary": "minecraft:chiseled_tuff",
            "panel": "minecraft:calcite",
            "energy": "minecraft:crying_obsidian",
            "window": "minecraft:tinted_glass",
            "glow": "minecraft:pearlescent_froglight",
            "detail": "minecraft:purpur_pillar",
            "conduit": "minecraft:end_rod",
            "antenna": "minecraft:lightning_rod",
            "rail": "minecraft:powered_rail",
            "mutation": [
                "minecraft:magenta_carpet",
                "minecraft:cherry_leaves",
                "minecraft:sculk_vein",
            ],
        }
    )
    prompt["materials"] = mats
    return prompt


def build_ribbed_structure(schem, x, y, z, radius, height, materials):
    """Generates the V7 'Fractal Rib' geometry."""
    primary = materials.get("primary", "minecraft:polished_tuff")
    secondary = materials.get("secondary", "minecraft:chiseled_tuff")

    for ry in range(0, height):
        is_rib = ry % 2 == 0
        mat = secondary if is_rib else primary

        # Draw a circular ring for the rib
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            bx = x + int(radius * math.cos(rad))
            bz = z + int(radius * math.sin(rad))

            # Use stairs for ribs to create the sharp, fractured look
            if is_rib:
                schem.setBlock(
                    (bx, y + ry, bz),
                    f"minecraft:polished_tuff_stairs[facing=north,half=top]",
                )
            else:
                schem.setBlock((bx, y + ry, bz), mat)


def add_hydro_pod(schem, x, y, z, materials):
    """Integrates a v5 'Hydro-Pod' module (Automated Economy)."""
    glass = materials.get("window", "minecraft:tinted_glass")
    tech = materials.get("detail", "minecraft:purpur_pillar")

    # Small 3x3x3 pod
    for dx in range(-1, 2):
        for dy in range(0, 3):
            for dz in range(-1, 2):
                if dy == 1 and dx == 0 and dz == 0:
                    schem.setBlock((x + dx, y + dy, z + dz), "minecraft:crafter")
                elif dy == 2 and dx == 0 and dz == 0:
                    schem.setBlock((x + dx, y + dy, z + dz), tech)
                else:
                    schem.setBlock((x + dx, y + dy, z + dz), glass)


def add_kinetic_signaling(schem, x, y, z):
    """Adds proximity-based sculk/copper bulb logic."""
    schem.setBlock((x, y, z), "minecraft:sculk_sensor")
    schem.setBlock((x + 1, y, z), "minecraft:oxidized_copper_bulb[lit=false]")


def apply_mutation(schem, x, y, z, radius, materials):
    """Spreads the mycelial mutation (Purple Carpet/Sculk)."""
    mutation_list = materials.get("mutation", ["minecraft:magenta_carpet"])
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if random.random() > 0.8:
                block = random.choice(mutation_list)
                schem.setBlock((x + dx, y, z + dz), block)
