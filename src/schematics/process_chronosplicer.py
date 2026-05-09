import math
import json
import os

def generate_chronosplicer_map():
    """
    Parses the Visionary's prose into a JSON voxel map.
    
    Prose References:
    - 'braided copper coils': Double-helix using waxed_copper.
    - 'Entropic Loom': 3x3 core of crying_obsidian and beacon.
    - 'emerald alloy conduits': Branching paths of emerald_block and sea_lanterns.
    """
    voxels = []
    # Base boundary is 5x5x5 for the initial cube, but we'll expand for coils/conduits
    # Center of the 5x5x5 cube is (2, 2, 2)
    center_x, center_y, center_z = 2, 2, 2
    
    # 1. THE ENTROPIC LOOM (3x3x3 Core)
    # 'a shimmering, pulsating Entropic Loom hangs in a field of localized anti-gravity'
    # 'a spherical mass of interconnected, razor-thin metallic filaments'
    # Requirement: 3x3 core of crying_obsidian and beacon blocks.
    for x in range(center_x - 1, center_x + 2):
        for y in range(center_y - 1, center_y + 2):
            for z in range(center_z - 1, center_z + 2):
                block = "minecraft:crying_obsidian"
                if x == center_x and y == center_y and z == center_z:
                    block = "minecraft:beacon" # The Loom's heart
                voxels.append({"x": x, "y": y, "z": z, "block": block})

    # 2. BRAIDED COPPER COILS (Double Helix)
    # 'Primary "Gravito-Magnetic Containment" Coils: Enormous, braided copper coils... 
    # They twist around the Loom in an intricate, non-Euclidean helix'
    # Requirement: Translate 'braided copper coils' into a double-helix coordinate set using waxed_copper.
    steps = 40
    radius = 3
    height_max = 6
    for i in range(steps):
        t = (i / steps) * 2 * math.pi * 2 # 2 full rotations
        h = (i / steps) * height_max
        
        # Helix 1
        x1 = center_x + int(radius * math.cos(t))
        z1 = center_z + int(radius * math.sin(t))
        y1 = int(h)
        
        # Helix 2 (180 degree offset)
        x2 = center_x + int(radius * math.cos(t + math.pi))
        z2 = center_z + int(radius * math.sin(t + math.pi))
        y2 = int(h)
        
        # Using 'waxed_copper' as requested (mapped to minecraft:waxed_copper_block)
        voxels.append({"x": x1, "y": y1, "z": z1, "block": "minecraft:waxed_copper_block"})
        voxels.append({"x": x2, "y": y2, "z": z2, "block": "minecraft:waxed_copper_block"})

    # 3. EMERALD ALLOY CONDUITS (Branching Paths)
    # 'Chronostabilizer Fluid Conduits: ... deep, iridescent emerald alloy... 
    # branching into impossible angles'
    # Requirement: Map 'emerald alloy conduits' as branching paths of emerald_block and sea_lanterns.
    # We'll create branches along the axes from the center.
    for dist in range(2, 6):
        # Branch out in 6 directions
        for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            x = center_x + dx * dist
            y = center_y + dy * dist
            z = center_z + dz * dist
            
            # Alternate between emerald_block and sea_lantern
            block = "minecraft:emerald_block" if dist % 2 == 0 else "minecraft:sea_lantern"
            voxels.append({"x": x, "y": y, "z": z, "block": block})

    # Deduplicate voxels
    unique_voxels = {}
    for v in voxels:
        key = (v['x'], v['y'], v['z'])
        unique_voxels[key] = v
        
    return list(unique_voxels.values())

def main():
    schema_delta = {
        "metadata": {
            "name": "Chronosplicer Singularity", 
            "version": "v5-Industrial",
            "source": "Visionary Prose (Emerald Mirror)",
            "origin_node": "Skynet-Core"
        },
        "voxels": generate_chronosplicer_map()
    }
    
    output_path = "config/schem-gen/chronosplicer_delta.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(schema_delta, f, indent=4)
    
    print(f"[+] Chronosplicer voxel map generated at {output_path}")
    print(f"[+] Total voxels: {len(schema_delta['voxels'])}")

if __name__ == "__main__":
    main()
