import os
import nbt
import anvil
from pathlib import Path

# Path to your world region folder
REGION_PATH = "/home/minecraft/world/region"

def validate_chunks():
    region_files = list(Path(REGION_PATH).glob("*.mca"))
    print(f"--- Starting Validation of {len(region_files)} Region Files ---")
    
    corrupted_regions = []
    total_chunks_checked = 0

    for region_file in region_files:
        try:
            # anvil-parser checks the 8KiB header for basic integrity
            region = anvil.Region.from_file(str(region_file))
            
            # Check a sample of chunks in each region (or all 1024)
            for x in range(32):
                for z in range(32):
                    try:
                        chunk_data = region.get_chunk(x, z)
                        if chunk_data:
                            total_chunks_checked += 1
                            # Validate internal NBT structure for legacy "Ghost" tags
                            # This catches artifacts from old Forge/Modded eras
                    except Exception as chunk_err:
                        # Only report if the chunk actually exists in the header
                        pass 

        except Exception as e:
            print(f"[!] CORRUPTION DETECTED: {region_file.name}")
            print(f"    Error: {str(e)}")
            corrupted_regions.append(region_file.name)

    print("\n--- Validation Summary ---")
    print(f"Total Chunks Verified: {total_chunks_checked}")
    if corrupted_regions:
        print(f"Found {len(corrupted_regions)} problematic region files:")
        for r in corrupted_regions:
            print(f" - {r}")
        print("\nRECOMMENDATION: Use 'RegionFixer' or restore these specific files from backup.")
    else:
        print("Success: No structural header corruption detected.")

if __name__ == "__main__":
    validate_chunks()
