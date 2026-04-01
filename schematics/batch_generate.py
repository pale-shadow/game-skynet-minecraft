"""
batch_generate.py — Batch processor for all JSON prompts.

Scans the /prompts/ directory for .json files and generates schematics for each.

Usage:
    python scripts/batch_generate.py
    python scripts/batch_generate.py --output ./custom_output
"""

import glob
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from scripts.generate_schematic import generate, load_prompt


def main():
    prompts_dir = os.path.join(PROJECT_ROOT, "prompts")
    output_dir = os.path.join(PROJECT_ROOT, "output")

    # Parse optional --output flag
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[idx + 1]

    if not os.path.isdir(prompts_dir):
        print(f"ERROR: Prompts directory not found: {prompts_dir}")
        print("Create it and add .json prompt files.")
        sys.exit(1)

    # Find all .json files recursively
    pattern = os.path.join(prompts_dir, "**", "*.json")
    prompt_files = sorted(glob.glob(pattern, recursive=True))

    if not prompt_files:
        print(f"No .json files found in {prompts_dir}")
        print("Create prompt files following the schema in master_prompt_reference.md")
        sys.exit(0)

    print(f"[MC Schematics Batch Generator]")
    print(f"  Prompts dir: {prompts_dir}")
    print(f"  Output dir:  {output_dir}")
    print(f"  Found {len(prompt_files)} prompt(s)")
    print()

    success = 0
    failed = 0
    start_all = time.time()

    for pf in prompt_files:
        rel = os.path.relpath(pf, PROJECT_ROOT)
        print(f"--- Processing: {rel} ---")
        try:
            prompt = load_prompt(pf)
            result = generate(prompt, output_dir)
            if result:
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1
        print()

    elapsed = time.time() - start_all
    print(f"{'=' * 40}")
    print(f"Batch complete in {elapsed:.2f}s")
    print(f"  Success: {success}")
    print(f"  Failed:  {failed}")
    print(f"  Total:   {len(prompt_files)}")


if __name__ == "__main__":
    main()
