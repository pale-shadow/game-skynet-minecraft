import argparse
import os
import sys

import mcschematic


def validate_schematics(directory):
    if not os.path.isdir(directory):
        print(f"Error: Directory not found: {directory}")
        return

    files = [
        f
        for f in os.listdir(directory)
        if f.endswith(".schematic") or f.endswith(".schem")
    ]
    print(f"Validating {len(files)} schematic files in {directory}...")

    success = 0
    failed = 0

    for f in files:
        path = os.path.join(directory, f)
        try:
            mcschematic.MCSchematic(path)
            print(f"  [OK] {f}")
            success += 1
        except Exception as e:
            print(f"  [FAIL] {f}: {e}")
            failed += 1

    print(f"\nSummary:")
    print(f"  Success: {success}")
    print(f"  Failed:  {failed}")
    print(f"  Total:   {len(files)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate Minecraft schematic files.")
    parser.add_argument(
        "--dir", type=str, required=True, help="Directory containing schematics."
    )
    args = parser.parse_args()
    validate_schematics(args.dir)
