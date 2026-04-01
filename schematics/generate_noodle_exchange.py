import nbtlib
from nbtlib.tag import ByteArray, Compound, Int, Short, String


def generate_noodle_exchange():
    # Modular 7x7 footprint, 6 blocks high
    width, height, length = 7, 6, 7

    # Define the 1.21.1 Palette
    palette = {
        "minecraft:air": 0,
        "minecraft:polished_deepslate": 1,
        "minecraft:gray_concrete": 2,
        "minecraft:shroomlight": 3,
        "minecraft:copper_bulb{lit:true,powered:true}": 4,
        "minecraft:rail[shape=east_west]": 5,
        "minecraft:iron_bars": 6,
        "minecraft:polished_deepslate_slab[type=top]": 7,
    }

    # BlockData array: (y * length + z) * width + x
    block_data = [0] * (width * height * length)

    for y in range(height):
        for z in range(length):
            for x in range(width):
                index = (y * length + z) * width + x

                # --- Y=0: Foundation & Tracks ---
                if y == 0:
                    # Industrial Track Bed (Center line)
                    if z == 3:
                        block_data[index] = palette["minecraft:gray_concrete"]
                    # Structural Frame
                    else:
                        block_data[index] = palette["minecraft:polished_deepslate"]

                # --- Y=1: Rails & Entrances ---
                elif y == 1:
                    # Place the rail on the concrete bed
                    if z == 3 and (0 < x < 6):
                        block_data[index] = palette["minecraft:rail[shape=east_west]"]
                    # Corner Pillars
                    elif (x == 0 or x == 6) and (z == 0 or z == 6):
                        block_data[index] = palette["minecraft:polished_deepslate"]

                # --- Y=2 to Y=4: Walls & Signalling ---
                elif 2 <= y <= 4:
                    is_corner = (x == 0 or x == 6) and (z == 0 or z == 6)
                    is_wall_x = x == 0 or x == 6
                    is_wall_z = z == 0 or z == 6

                    if is_corner:
                        block_data[index] = palette["minecraft:polished_deepslate"]
                    elif is_wall_x or is_wall_z:
                        # Copper Bulbs as "Status Indicators" in the center of walls
                        if (x == 3 or z == 3) and y == 3:
                            block_data[index] = palette[
                                "minecraft:copper_bulb{lit:true,powered:true}"
                            ]
                        # Security Iron Bars for industrial look
                        else:
                            block_data[index] = palette["minecraft:iron_bars"]

                # --- Y=5: Roof & Organic Lighting ---
                elif y == 5:
                    # Central Shroomlight (The "Organic" touch)
                    if x == 3 and z == 3:
                        block_data[index] = palette["minecraft:shroomlight"]
                    # Deepslate Slabs for the industrial roof capping
                    else:
                        block_data[index] = palette[
                            "minecraft:polished_deepslate_slab[type=top]"
                        ]

    # Construct the NBT
    schem = nbtlib.File(
        {
            "": Compound(
                {
                    "Version": Int(2),
                    "Width": Short(width),
                    "Height": Short(height),
                    "Length": Short(length),
                    "Palette": Compound(
                        {name: Int(val) for name, val in palette.items()}
                    ),
                    "BlockData": ByteArray(block_data),
                    "Metadata": Compound(
                        {
                            "Name": String("Noodle_Economy_Exchange"),
                            "Author": String("Gemini_AI"),
                            "Date": String("March_2026"),
                        }
                    ),
                }
            )
        }
    )

    schem.save("noodle_exchange.schem")
    print("Schematic 'noodle_exchange.schem' generated.")


if __name__ == "__main__":
    generate_noodle_exchange()
