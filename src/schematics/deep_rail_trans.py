import nbtlib
from nbtlib.tag import Compound, Int, Short, ByteArray, String

def generate_industrial_bridge():
    # A 7x5x12 segment that can be repeated
    width, height, length = 7, 5, 12
    
    palette = {
        "minecraft:air": 0,
        "minecraft:polished_deepslate": 1,
        "minecraft:oxidized_copper": 2,
        "minecraft:shroomlight": 3,
        "minecraft:iron_bars": 4,
        "minecraft:polished_deepslate_slab[type=bottom]": 5,
        "minecraft:gray_concrete": 6
    }

    block_data = [0] * (width * height * length)

    for y in range(height):
        for z in range(length):
            for x in range(width):
                index = (y * length + z) * width + x
                
                # Base Floor (Industrial Concrete & Rail Bed)
                if y == 0:
                    if 2 <= x <= 4: set_val = 6 # Concrete center
                    else: set_val = 1 # Deepslate edges
                    block_data[index] = set_val
                
                # Side Railings & Support Pillars
                elif y == 1:
                    if x == 0 or x == 6:
                        block_data[index] = 1 # Deepslate base for railing
                
                # The "Glow" Accents (Y=2)
                elif y == 2:
                    if (x == 0 or x == 6) and z % 4 == 0:
                        block_data[index] = 3 # Shroomlight pillars
                    elif x == 0 or x == 6:
                        block_data[index] = 4 # Iron Bars between lights
                
                # Copper Capping (Y=4)
                elif y == 4:
                    if x == 0 or x == 6:
                        block_data[index] = 2 # Oxidized Copper trim

    schem = nbtlib.File({'': Compound({
        'Version': Int(2),
        'Width': Short(width), 'Height': Short(height), 'Length': Short(length),
        'Palette': Compound({name: Int(val) for name, val in palette.items()}),
        'BlockData': ByteArray(block_data),
        'Metadata': Compound({'Name': String('Industrial_Rail_Bridge')})
    })})

    schem.save('rail_bridge.schem')
    print("Bridge segment 'rail_bridge.schem' generated.")

if __name__ == "__main__":
    generate_industrial_bridge()
