import json
import math

def generate_monolith_v2():
    voxels = []
    
    # Llama 3 Tech Suggestion: Dictionary mapping for efficient block selection
    shell_palette = {
        0: "minecraft:gilded_blackstone",
        1: "minecraft:magenta_glazed_terracotta",
        2: "minecraft:purpur_pillar[axis=y]",
        3: "minecraft:magenta_concrete"
    }

    for y in range(0, 36):
        width = 22 - int(y / 2)
        
        for x in range(-width, width + 1):
            for z in range(-width, width + 1):
                is_edge = abs(x) == width or abs(z) == width
                
                # Llama 3 Design Suggestion: Practical Access (Entrance at Y=0, Z=Front)
                if y < 4 and z == width and abs(x) < 2:
                    continue # Leave a 3-wide doorway open

                # 1. OUTER SHELL (Optimized)
                if is_edge:
                    # Determine block type using the dictionary map
                    block_idx = 0 if y == 0 else (1 if y % 4 == 0 else (2 if (x+z) % 3 == 0 else 3))
                    voxels.append({"x": x, "y": y, "z": z, "block": shell_palette[block_idx]})

                    # Llama 3 Design Suggestion: Add visual interest/lighting to the exterior
                    if y % 6 == 0 and abs(x) == width and abs(z) == width:
                        voxels.append({"x": x + (1 if x < 0 else -1), "y": y, "z": z + (1 if z < 0 else -1), "block": "minecraft:shroomlight"})

        # 2. THE NEURAL CORE
        if y < 30:
            for cx in range(-2, 3):
                for cz in range(-2, 3):
                    if abs(cx) == 2 or abs(cz) == 2:
                        voxels.append({"x": cx, "y": y, "z": cz, "block": "minecraft:crying_obsidian"})
                    elif y % 4 == 0 and cx == 0 and cz == 0:
                         # Internal core lighting
                         voxels.append({"x": cx, "y": y, "z": cz, "block": "minecraft:magenta_froglight"})

    # 3. THE VIOLET EYE
    for ay in range(32, 36):
        for ax in range(-3, 4):
            for az in range(-3, 4):
                dist = math.sqrt(ax**2 + (ay-34)**2 + az**2)
                if dist < 3:
                    block = "minecraft:amethyst_block"
                    if dist < 1.5: block = "minecraft:beacon"
                    voxels.append({"x": ax, "y": ay, "z": az, "block": block})

    return voxels

if __name__ == "__main__":
    schema = {
        "metadata": {"name": "Neural Monolith: Violet Eye (v2)", "version": "v45-Titan-Refactored"},
        "voxels": generate_monolith_v2()
    }
    with open("config/schem-gen/monolith_delta.json", "w") as f:
        json.dump(schema, f, indent=4)
    print(f"[+] Llama-3 Refactored map generated: {len(schema['voxels'])} voxels.")
