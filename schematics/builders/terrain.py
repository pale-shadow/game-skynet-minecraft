"""
terrain.py — Terrain, landscape, and garden builder.

Generates natural-looking terrain blobs and flat gardens with scattered decorations.
Uses simplex-style noise approximation for organic shapes.
"""
import math
import random
import mcschematic


# Simple 2D noise approximation using sin/cos harmonics
def _terrain_height(x, z, w, l, max_h, seed=42):
    """Generate a pseudo-natural height value for (x, z) using layered sine waves."""
    random.seed(seed)
    offsets = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(4)]
    value = 0.0
    for i, (ox, oz) in enumerate(offsets):
        freq = (i + 1) * 0.3
        amp = 1.0 / (i + 1)
        value += amp * math.sin((x + ox) * freq * math.pi / w) * math.cos((z + oz) * freq * math.pi / l)
    # Normalize to 0..max_h
    norm = (value + 1.0) / 2.0
    return max(1, int(norm * max_h))


def build_terrain(schem: mcschematic.MCSchematic, prompt: dict):
    dims = prompt.get("dimensions", {})
    w = dims.get("width", 15)
    h = dims.get("height", 5)
    l = dims.get("length", 15)
    feats = prompt.get("features", {})

    fill_block    = feats.get("fill_block",    "minecraft:dirt")
    surface_block = feats.get("surface_block", "minecraft:grass_block")
    scatter       = feats.get("scatter_decorations", False)

    FLOWERS = [
        "minecraft:poppy",
        "minecraft:dandelion",
        "minecraft:cornflower",
        "minecraft:oxeye_daisy",
        "minecraft:azure_bluet",
        "minecraft:red_tulip",
        "minecraft:orange_tulip",
        "minecraft:white_tulip",
        "minecraft:pink_tulip",
        "minecraft:lily_of_the_valley",
        "minecraft:blue_orchid",
        "minecraft:allium",
    ]

    EXTRAS = [
        "minecraft:grass",
        "minecraft:grass",
        "minecraft:tall_grass",
        "minecraft:fern",
    ]

    seed = hash(prompt.get("name", "terrain")) % 10000

    for x in range(w):
        for z in range(l):
            col_h = _terrain_height(x, z, w, l, h, seed)
            # Fill column
            for y in range(col_h):
                schem.setBlock((x, y, z), fill_block)
            # Surface cap
            schem.setBlock((x, col_h, z), surface_block)

            # Scatter decorations on surface
            if scatter:
                random.seed(seed + x * 1000 + z)
                roll = random.random()
                if roll < 0.12:
                    schem.setBlock((x, col_h + 1, z), random.choice(FLOWERS))
                elif roll < 0.25:
                    schem.setBlock((x, col_h + 1, z), random.choice(EXTRAS))

    return schem
