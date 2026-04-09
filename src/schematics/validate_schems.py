import os

import nbtlib

file_path = (
    "/home/franklin/workspace/gaming/game-skynet-minecraft/schematics/schem_files/"
)


def validate_schematic(file_path):
    try:
        # Load the schematic using nbtlib
        nbt_file = nbtlib.load(file_path)

        # In nbtlib, the root is accessed via indexing or the .root attribute
        # depends on the specific library version in your venv.
        # For Sponge/WorldEdit schematics, check for the 'Palette' or 'Blocks' keys.
        if "Palette" in nbt_file or "Blocks" in nbt_file:
            return True
        return False
    except Exception as e:
        print(f"❌ {os.path.basename(file_path)}: ERROR - {e}")
        return False
