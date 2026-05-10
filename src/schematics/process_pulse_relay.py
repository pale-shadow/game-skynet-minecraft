import json

def generate_pulse_relay():
    voxels = []
    # 1. THE FOUNDATION (3x3 Base at Y=0 relative to anchor)
    for x in range(0, 3):
        for z in range(0, 3):
            voxels.append({"x": x, "y": 0, "z": z, "block": "minecraft:dark_prismarine"})
    
    # 2. THE FLUTED SPIRE (Central column)
    for y in range(1, 8):
        # Core Pillar
        voxels.append({"x": 1, "y": y, "z": 1, "block": "minecraft:purpur_pillar[axis=y]"})
        # Decorative Ribs
        if y % 2 == 0:
            voxels.append({"x": 0, "y": y, "z": 1, "block": "minecraft:purpur_slab[type=top]"})
            voxels.append({"x": 2, "y": y, "z": 1, "block": "minecraft:purpur_slab[type=top]"})

    # 3. THE PULSE CORE (The Light)
    voxels.append({"x": 1, "y": 8, "z": 1, "block": "minecraft:pearlescent_froglight"})
    voxels.append({"x": 1, "y": 9, "z": 1, "block": "minecraft:dark_prismarine_stairs[facing=north,half=top]"})

    return voxels

if __name__ == "__main__":
    schema = {
        "metadata": {"name": "Emerald Mirror Pulse Relay", "version": "v5-Industrial"},
        "voxels": generate_pulse_relay()
    }
    with open("config/schem-gen/pulse_relay_delta.json", "w") as f:
        json.dump(schema, f, indent=4)
    print("[+] Pulse Relay voxel map generated.")
