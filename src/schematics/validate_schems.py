import os
import nbtlib
from pathlib import Path

# Path to your FAWE schematics folder
SCHEM_DIR = "/home/minecraft/minecraft/plugins/FastAsyncWorldEdit/schematics"

def validate_all_schematics():
    files = list(Path(SCHEM_DIR).glob("*.*"))
    print(f"--- Validating {len(files)} Schematic Files ---")
    
    for f in files:
        if f.suffix not in ['.schem', '.schematic']:
            continue
            
        try:
            # Attempt to load the NBT structure
            data = nbtlib.load(str(f))
            
            # Check for standard headers
            if 'Palette' in data.root or 'Blocks' in data.root or 'Schematic' in data.root:
                print(f"✅ {f.name}: Valid NBT Structure")
            else:
                print(f"⚠️  {f.name}: Unknown structure (possible legacy MCEdit)")
                
        except Exception as e:
            print(f"❌ {f.name}: CORRUPT FILE - {str(e)}")

if __name__ == "__main__":
    validate_all_schematics()
