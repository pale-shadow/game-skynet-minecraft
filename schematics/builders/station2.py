import mcschematic


def build(schem, config):
    """
    Industrial Station Builder
    Handles fluted pillars, hanging girders, and vaulted ceiling logic.
    """
    w, h, l = (
        config["dimensions"]["width"],
        config["dimensions"]["height"],
        config["dimensions"]["length"],
    )
    palette = config.get(
        "palette",
        {
            "primary": "minecraft:purpur_pillar",
            "secondary": "minecraft:dark_prismarine",
            "trim": "minecraft:purpur_stairs",
            "floor": "minecraft:polished_andesite",
        },
    )

    # 1. Platform Foundation
    for x in range(w):
        for z in range(l):
            schem.setBlock((x, 0, z), palette["floor"])

    # 2. Fluted Pillar Logic (3x3 footprint for depth)
    # Placing pillars at corners and midpoints for structural stability
    pillar_locs = [(1, 1), (1, l - 2), (w - 2, 1), (w - 2, l - 2)]
    if l > 15:
        pillar_locs.extend([(1, l // 2), (w - 2, l // 2)])

    for px, pz in pillar_locs:
        for py in range(1, h - 2):
            # Central Core
            schem.setBlock((px, py, pz), f"{palette['primary']}[axis=y]")
            # Fluting (Recessed depth using stairs)
            schem.setBlock(
                (px + 1, py, pz), f"{palette['trim']}[facing=west,half=bottom]"
            )
            schem.setBlock(
                (px - 1, py, pz), f"{palette['trim']}[facing=east,half=bottom]"
            )
            schem.setBlock(
                (px, py, pz + 1), f"{palette['trim']}[facing=north,half=bottom]"
            )
            schem.setBlock(
                (px, py, pz - 1), f"{palette['trim']}[facing=south,half=bottom]"
            )

    """
    # 3. Grid-Iron Girders & Light Boxes
    girder_y = int(h * 0.8)
    for z in range(l):
        for x in [1, w-2]: # Longitudinal beams
            schem.setBlock((x, girder_y, z), palette.get('secondary', 'minecraft:dark_prismarine'))
            # Integrated Lighting at intervals
            if z % 6 == 0:
                schem.setBlock((x, girder_y, z), "minecraft:pearlescent_froglight")
                # Structural framing
                schem.setBlock((x, girder_y + 1, z), "minecraft:purpur_slab[type=bottom]")

    # 4. Vaulted Ceiling Greebling
    for x in range(w):
        for z in range(l):
            if x % 4 == 0 or z % 4 == 0: # Creates a coffered ceiling look
                schem.setBlock((x, h-1, z), "minecraft:purpur_slab[type=top]")
            else:
                schem.setBlock((x, h-1, z), "minecraft:stone_brick_slab[type=top]")
    """

    """
    # 3. Hanging Girders (Warped/Prismarine support beams)
    girder_y = int(h * 0.8)
    for z in range(l):
        # Longitudinal beams connecting the pillars
        schem.setBlock((1, girder_y, z), palette['secondary'])
        schem.setBlock((w-2, girder_y, z), palette['secondary'])
        # Hanging supports (Fences/Slabs)
        schem.setBlock((1, girder_y - 1, z), "minecraft:warped_fence")
        schem.setBlock((w-2, girder_y - 1, z), "minecraft:warped_fence")
    """
    # 3. Grid-Iron Girder System (Intersection logic)
    girder_y = int(h * 0.8)
    # Longitudinal (Length-wise)
    for z in range(l):
        for x in [1, w - 2]:
            schem.setBlock((x, girder_y, z), palette["secondary"])
            schem.setBlock((x, girder_y - 1, z), "minecraft:warped_fence")

    # Transverse (Width-wise) - Every 5 blocks for greebling
    for z in range(0, l, 5):
        for x in range(1, w - 1):
            schem.setBlock((x, girder_y, z), palette["secondary"])

    """
    # 4. Ceiling Vault (Simple arch logic)
    for x in range(w):
        for z in range(l):
            schem.setBlock((x, h-1, z), "minecraft:stone_brick_slab")
    """
    # 4. Enhanced Ceiling & Light Box Logic
    for x in range(w):
        for z in range(l):
            # Base Ceiling layer
            schem.setBlock((x, h - 1, z), "minecraft:stone_brick_slab[type=top]")

            # Integrated Purple Light Boxes (Place at girder intersections)
            if (x == 1 or x == w - 2) and z % 5 == 0:
                # The 'Light Box' - Pearlescent Froglight for that purple glow
                schem.setBlock(
                    (x, h - 2, z),
                    palette.get("lighting", "minecraft:pearlescent_froglight"),
                )
                # Decorative framing around the light
                schem.setBlock(
                    (x + 1, h - 2, z), "minecraft:purpur_stairs[facing=west]"
                )
                schem.setBlock(
                    (x - 1, h - 2, z), "minecraft:purpur_stairs[facing=east]"
                )

    print(f"DEBUG: Station '{config['name']}' compiled with fluted pillar geometry.")
