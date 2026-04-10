import nbtlib
from nbtlib.tag import ByteArray, Compound, Int, Short, String


def generate_signal_core():
    # Dimensions: 11x9x11
    width, height, length = 11, 9, 11

    # Define the Block Palette (Minecraft 1.21.1 names)
    palette = {
        "minecraft:air": 0,
        "minecraft:polished_deepslate": 1,
        "minecraft:cyan_stained_glass": 2,
        "minecraft:sea_lantern": 3,
        "minecraft:copper_bulb{lit:true,powered:true}": 4,
        "minecraft:moss_carpet": 5,
        "minecraft:polished_deepslate_stairs[facing=north]": 6,
    }

    # Initialize the block data array (Width * Height * Length)
    # The array index formula: (y * length + z) * width + x
    block_data = [0] * (width * height * length)

    for y in range(height):
        for z in range(length):
            for x in range(width):
                index = (y * length + z) * width + x

                # 1. Floor (y=0)
                if y == 0:
                    block_data[index] = palette["minecraft:polished_deepslate"]

                # 2. Core Pillar (Central 3x3 from y=1 to y=7)
                elif 4 <= x <= 6 and 4 <= z <= 6 and 1 <= y <= 7:
                    block_data[index] = palette[
                        "minecraft:copper_bulb{lit:true,powered:true}"
                    ]

                # 3. Outer Walls (Glass and Columns)
                elif y < 8:
                    is_edge_x = x == 0 or x == width - 1
                    is_edge_z = z == 0 or z == length - 1

                    if is_edge_x or is_edge_z:
                        # Corner and Midpoint Columns
                        if (x % 5 == 0) and (z % 5 == 0):
                            block_data[index] = palette["minecraft:polished_deepslate"]
                        else:
                            block_data[index] = palette["minecraft:cyan_stained_glass"]

                # 4. Ceiling (y=8)
                elif y == 8:
                    if 4 <= x <= 6 and 4 <= z <= 6:
                        block_data[index] = palette["minecraft:sea_lantern"]
                    else:
                        block_data[index] = palette["minecraft:polished_deepslate"]

    # Construct the NBT structure for Sponge Schematic V2
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
                            "Name": String("Signal_Core_Data_Hub"),
                            "Author": String("Gemini_AI"),
                        }
                    ),
                }
            )
        }
    )

    import os

    from skynet_core import Config

    output_path = os.path.join(Config.SCHEM_DIR, "signal_core.schem")
    schem.save(output_path)
    print(f"Schematic '{output_path}' generated successfully.")


if __name__ == "__main__":
    generate_signal_core()
