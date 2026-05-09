import json
import math

def generate_cooling_array():
    voxels = []
    # 1. THERMAL SINK (5x5 Base)
    for x in range(0, 5):
        for z in range(0, 5):
            voxels.append({"x": x, "y": 0, "z": z, "block": "minecraft:dark_prismarine"})
            # Maintenance Hatches (Iron Trapdoors)
            if (x == 0 or x == 4 or z == 0 or z == 4) and (x+z) % 2 == 0:
                voxels.append({"x": x, "y": 1, "z": z, "block": "minecraft:iron_trapdoor[half=bottom]"})

    # 2. RADIATOR FINS (Copper Spiral Greebling)
    for y in range(1, 6):
        # Central Core
        voxels.append({"x": 2, "y": y, "z": 2, "block": "minecraft:purpur_pillar"})
        
        # Spiral Fins
        angle = y * (math.pi / 2)
        offset_x = int(round(math.cos(angle)))
        offset_z = int(round(math.sin(angle)))
        voxels.append({"x": 2 + offset_x, "y": y, "z": 2 + offset_z, "block": "minecraft:waxed_exposed_copper_stairs[facing=south]"})
        
        # Ion Discharge Needles
        if y == 3 or y == 5:
            voxels.append({"x": 2 - offset_x, "y": y, "z": 2 - offset_z, "block": "minecraft:end_rod"})

    # 3. PULSE CAP (Froglight)
    voxels.append({"x": 2, "y": 6, "z": 2, "block": "minecraft:pearlescent_froglight"})
    
    return voxels

if __name__ == "__main__":
    schema = {
        "metadata": {"name": "Vortex Cooling Array", "version": "v5-Industrial-Vertex"},
        "voxels": generate_cooling_array()
    }
    with open("config/schem-gen/cooling_array_delta.json", "w") as f:
        json.dump(schema, f, indent=4)
    print(f"[+] Vertex-augmented voxel map generated: {len(schema['voxels'])} voxels.")
