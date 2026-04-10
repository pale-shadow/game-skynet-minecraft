"""
To match the Dreamland 2026 aesthetic, this script generates the "Rail-Bound Sentinel."
This is a large-scale (15x27x15) industrial statue of a humanoid figure constructed
from Polished Deepslate and Oxidized Copper. The figure holds a massive, 27-block tall
"Golden Rail Spike" (representing the server's 2012 foundation) and features a glowing
Shroomlight Core in its chest to match the bioluminescent theme of Shroomville.

🏛️ Statue Symbolism for the Website

You can add this flavor text to your Latest News or District Guide:

    "The Rail-Bound Sentinel stands as a silent guardian over the Deep-Rail network. Forged from the deepslate of the 2012 foundation and armored in the oxidized copper of the modern era, it holds the 'Golden Spike'—a symbol of the line that connects our past at Washington Station to our future in Shroomville."

🛠️ How to Deploy

    Run the script on your Debian terminal: python3 generate_rail_sentinel.py.

    Move it to your WorldEdit folder: cp rail_sentinel.schem ~/minecraft/config/worldedit/schematics/.

    In-game, go to a prominent plaza (like the Cathedral Plaza or the Rail Yard entrance).

    Run: //schem load rail_sentinel and //paste.

"""

import nbtlib
from nbtlib.tag import ByteArray, Compound, Int, Short, String


def generate_rail_sentinel():
    # Dimensions: 15 (W) x 27 (H) x 15 (L)
    width, height, length = 15, 27, 15

    # Define the 1.21.1 Dreamland Palette
    palette = {
        "minecraft:air": 0,
        "minecraft:polished_deepslate": 1,
        "minecraft:oxidized_copper": 2,
        "minecraft:shroomlight": 3,
        "minecraft:cyan_stained_glass": 4,
        "minecraft:gold_block": 5,
        "minecraft:gray_concrete": 6,
        "minecraft:copper_bulb{lit:true,powered:true}": 7,
        "minecraft:polished_deepslate_stairs[facing=north]": 8,
    }

    block_data = [0] * (width * height * length)

    def set_block(x, y, z, block_name):
        if 0 <= x < width and 0 <= y < height and 0 <= z < length:
            index = (y * length + z) * width + x
            block_data[index] = palette[block_name]

    # --- 1. The Industrial Pedestal (Y: 0-3) ---
    for x in range(2, 13):
        for z in range(2, 13):
            for y in range(4):
                if y == 0:
                    set_block(x, y, z, "minecraft:gray_concrete")
                else:
                    set_block(x, y, z, "minecraft:polished_deepslate")

    # --- 2. The Legs (Y: 4-10) ---
    for y in range(4, 11):
        # Left Leg
        for x in range(4, 7):
            for z in range(6, 9):
                set_block(x, y, z, "minecraft:polished_deepslate")
        # Right Leg
        for x in range(8, 11):
            for z in range(6, 9):
                set_block(x, y, z, "minecraft:polished_deepslate")

    # --- 3. The Torso & Power Core (Y: 11-18) ---
    for y in range(11, 19):
        for x in range(4, 11):
            for z in range(5, 10):
                # Core Placement (Bioluminescent Heart)
                if 13 <= y <= 15 and 6 <= x <= 8 and z == 5:
                    set_block(x, y, z, "minecraft:shroomlight")
                    set_block(x, y, z - 1, "minecraft:cyan_stained_glass")
                else:
                    set_block(x, y, z, "minecraft:oxidized_copper")

    # --- 4. The Arms (Y: 14-20) ---
    for y in range(14, 21):
        # Left Arm (Holding Staff)
        for x in range(1, 4):
            for z in range(6, 9):
                set_block(x, y, z, "minecraft:polished_deepslate")
        # Right Arm (Posed)
        for x in range(11, 14):
            for z in range(6, 9):
                set_block(x, y, z, "minecraft:polished_deepslate")

    # --- 5. The "Golden Rail Spike" Staff (Full Height) ---
    for y in range(0, 27):
        # Massive vertical rail staff
        set_block(2, y, 5, "minecraft:gold_block")
        # Topped with a Signal Light
        if y == 26:
            set_block(2, y, 5, "minecraft:copper_bulb{lit:true,powered:true}")

    # --- 6. The Head (Y: 19-24) ---
    for y in range(19, 25):
        for x in range(5, 10):
            for z in range(5, 10):
                # Eyes (Cyan Glow)
                if y == 22 and (x == 6 or x == 8) and z == 5:
                    set_block(x, y, z, "minecraft:cyan_stained_glass")
                else:
                    set_block(x, y, z, "minecraft:polished_deepslate")

    # Finalize NBT
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
                            "Name": String("Rail_Bound_Sentinel"),
                            "Author": String("Gemini_AI"),
                            "Project": String("Dreamland_2026"),
                        }
                    ),
                }
            )
        }
    )

    from skynet_core import Config
    import os
    output_path = os.path.join(Config.SCHEM_DIR, "rail_sentinel.schem")
    schem.save(output_path)
    print(f"Statue generated: {output_path}")


if __name__ == "__main__":
    generate_rail_sentinel()
