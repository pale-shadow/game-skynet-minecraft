import os
import nbtlib
from pathlib import Path

SCHEM_DIR = "/home/franklin/workspace/gaming/game-chonk-minecraft/schematics"

def validate_all_schematics():
    files = list(Path(SCHEM_DIR).glob("*.*"))
    print(f"--- Validating {len(files)} Schematic Files ---")
    
    for f in files:
        if f.suffix not in ['.schem', '.schematic']:
            continue
            
        try:
            data = nbtlib.load(str(f))
            
            if 'Palette' in data.root or 'Blocks' in data.root or 'Schematic' in data.root:
                print(f"✅ {f.name}: Valid NBT Structure")
            else:
                print(f"⚠️  {f.name}: Unknown structure (possible legacy MCEdit)")
                
        except Exception as e:
            print(f"❌ {f.name}: CORRUPT FILE - {str(e)}")

if __name__ == "__main__":
    validate_all_schematics()
