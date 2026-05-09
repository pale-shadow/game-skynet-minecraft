import json
import math

def generate_monolith():
    voxels = []
    # Dimensions: 45 wide (offset -22 to 22), 36 tall
    for y in range(0, 36):
        # Scale step-in: Taper the building as it rises
        width = 22 - int(y / 2)
        
        for x in range(-width, width + 1):
            for z in range(-width, width + 1):
                # 1. OUTER SHELL (Hollowed for performance)
                is_edge = abs(x) == width or abs(z) == width
                
                if is_edge:
                    # Alternating Industrial Pattern
                    if y == 0:
                        block = "minecraft:gilded_blackstone"
                    elif y % 4 == 0:
                        block = "minecraft:magenta_glazed_terracotta"
                    elif (x + z) % 3 == 0:
                        block = "minecraft:purpur_pillar[axis=y]"
                    else:
                        block = "minecraft:magenta_concrete"
                    voxels.append({"x": x, "y": y, "z": z, "block": block})

                    # Add secondary greebling layer (Slabs/Stairs)
                    if y % 2 == 0:
                        voxels.append({"x": x + (1 if x < 0 else -1), "y": y, "z": z, "block": "minecraft:purpur_slab[type=bottom]"})

        # 2. THE NEURAL CORE (Central Spire)
        if y < 30:
            for cx in range(-2, 3):
                for cz in range(-2, 3):
                    if abs(cx) == 2 or abs(cz) == 2:
                        voxels.append({"x": cx, "y": y, "z": cz, "block": "minecraft:crying_obsidian"})
                    elif y % 5 == 0:
                         voxels.append({"x": cx, "y": y, "z": cz, "block": "minecraft:magenta_froglight"})

    # 3. SPECIAL TOUCH: "THE VIOLET EYE" (The Apex)
    # A floating amethyst geode at the top
    for ay in range(32, 36):
        for ax in range(-3, 4):
            for az in range(-3, 4):
                dist = math.sqrt(ax**2 + (ay-34)**2 + az**2)
                if dist < 3:
                    block = "minecraft:amethyst_block"
                    if dist < 1.5: block = "minecraft:beacon"
                    voxels.append({"x": ax, "y": ay, "z": az, "block": block})
                    # Shards
                    if ay == 35:
                        voxels.append({"x": ax, "y": ay+1, "z": az, "block": "minecraft:amethyst_cluster[facing=up]"})

    return voxels

if __name__ == "__main__":
    schema = {
        "metadata": {"name": "Neural Monolith: Violet Eye", "version": "v45-Titan-Ultraviolet"},
        "voxels": generate_monolith()
    }
    with open("config/schem-gen/monolith_delta.json", "w") as f:
        json.dump(schema, f, indent=4)
    print(f"[+] Titan-scale map generated: {len(schema['voxels'])} voxels.")
