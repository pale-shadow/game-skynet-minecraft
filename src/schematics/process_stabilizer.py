import json
import math

def generate_stabilizer():
    voxels = []
    # 1. THE FOUNDATION (15x15 Heavy Plate)
    for x in range(0, 15):
        for z in range(0, 15):
            # Outer ring of heavy plating
            if x == 0 or x == 14 or z == 0 or z == 14:
                voxels.append({"x": x, "y": 0, "z": z, "block": "minecraft:gilded_blackstone"})
            else:
                voxels.append({"x": x, "y": 0, "z": z, "block": "minecraft:red_nether_bricks"})

    # 2. THE REACTION CORE (5x5x8 Pillar in Center)
    for y in range(1, 9):
        for x in range(5, 10):
            for z in range(5, 10):
                # Hollow core with pulse lights
                if x == 7 and z == 7:
                    voxels.append({"x": x, "y": y, "z": z, "block": "minecraft:shroomlight"})
                else:
                    voxels.append({"x": x, "y": y, "z": z, "block": "minecraft:crimson_hyphae"})

    # 3. REDSTONE VEINS (Inverted Artery System)
    # Four massive external pipes snaking upward
    pipe_anchors = [(2, 2), (12, 2), (2, 12), (12, 12)]
    for px, pz in pipe_anchors:
        for y in range(1, 12):
            voxels.append({"x": px, "y": y, "z": pz, "block": "minecraft:redstone_block"})
            # Connector struts
            if y % 4 == 0:
                step = 1 if px < 7 else -1
                voxels.append({"x": px + step, "y": y, "z": pz, "block": "minecraft:lightning_rod[facing=up]"})

    # 4. GREEBLING OVERLAY (Aesthetic Density)
    for i in range(20):
        # Scattering maintenance hatches and buttons
        rx = (i * 7) % 15
        rz = (i * 3) % 15
        voxels.append({"x": rx, "y": 1, "z": rz, "block": "minecraft:warped_trapdoor[half=bottom]"})
        voxels.append({"x": rx, "y": 0, "z": rz, "block": "minecraft:polished_blackstone_button[face=floor]"})

    return voxels

if __name__ == "__main__":
    schema = {
        "metadata": {"name": "Anti-Entropy Siphon", "version": "v15-Macro-Inverted"},
        "voxels": generate_stabilizer()
    }
    with open("config/schem-gen/stabilizer_delta.json", "w") as f:
        json.dump(schema, f, indent=4)
    print(f"[+] Macro-scale voxel map generated: {len(schema['voxels'])} voxels.")
