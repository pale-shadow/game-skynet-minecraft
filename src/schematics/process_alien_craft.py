import json
import math

def generate_alien_craft():
    grid = {}
    
    # PASS 1: THE SAUCER HULL
    # Uses a parabolic taper to create a hovering disc
    for y in range(5, 32): 
        dy = abs(y - 18)
        # Radius expands to 22 at the equator (y=18) and tapers off
        max_r = 22 * (1 - (dy / 13)**2) 
        for x in range(-22, 23):
            for z in range(-22, 23):
                dist = math.sqrt(x**2 + z**2)
                # Hollow shell: only place blocks on the outer edge
                if max_r - 2 < dist <= max_r:
                    block = "minecraft:polished_blackstone_bricks"
                    # Stratified armor plating
                    if y % 3 == 0: 
                        block = "minecraft:cyan_terracotta"
                    grid[(x, y, z)] = block

    # PASS 2: PROPULSION CORE & THRUST COLUMN
    for y in range(0, 28):
        for x in range(-3, 4):
            for z in range(-3, 4):
                dist = math.sqrt(x**2 + z**2)
                if dist <= 3:
                    if dist <= 1.5:
                        grid[(x, y, z)] = "minecraft:sea_lantern"
                    else:
                        grid[(x, y, z)] = "minecraft:cyan_stained_glass"

    # PASS 3: BIO-MECHANICAL GREEBLING & CORRUPTION
    # Iterate over the existing grid to mutate and add details
    for (x, y, z), block in list(grid.items()):
        dist = math.sqrt(x**2 + z**2)
        
        # 3a. Equator Energy Ring
        if y == 18 and dist >= 20:
            grid[(x, y, z)] = "minecraft:sea_lantern"
            
        # 3b. Sculk Corruption on the ventral (bottom) hull
        elif y < 15 and "blackstone" in block:
            if (x + y + z) % 5 == 0:
                grid[(x, y, z)] = "minecraft:sculk"
            elif (x + z) % 9 == 0:
                grid[(x, y, z)] = "minecraft:sculk_sensor"
                
        # 3c. Dorsal (top) hull Ion Spikes
        elif y > 22 and (abs(x) == abs(z)) and "blackstone" in block:
            if x % 4 == 0:
                # Append a spike on top of the current block
                grid[(x, y + 1, z)] = "minecraft:end_rod[facing=up]"

    # Convert the 3D grid dictionary to the standard JSON list format
    voxels = [{"x": k[0], "y": k[1], "z": k[2], "block": v} for k, v in grid.items()]
    return voxels

if __name__ == "__main__":
    schema = {
        "metadata": {"name": "Abyssal Voidcraft", "version": "v45-Extraterrestrial-3Pass"},
        "voxels": generate_alien_craft()
    }
    with open("config/schem-gen/alien_craft_delta.json", "w") as f:
        json.dump(schema, f, indent=4)
    print(f"[+] Multi-Pass Voidcraft generated: {len(schema['voxels'])} voxels mapped.")
