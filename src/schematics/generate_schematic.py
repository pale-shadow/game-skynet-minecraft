import json
import os
import sys
import time

import mcschematic

# Add the parent directory of this script to sys.path so 'builders' can be imported
# This assumes generate_schematic.py is in src/schematics/
# and 'builders' is in src/schematics/builders/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from builders import BUILDERS
from skynet_core import Config

VERSION_MAP = {
    v: getattr(mcschematic.Version, v)
    for v in dir(mcschematic.Version)
    if v.startswith("JE_")
}
DEFAULT_VERSION = "JE_1_21_1"


def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        prompt = json.load(f)
    if "type" not in prompt:
        prompt["type"] = "house"
    if "name" not in prompt:
        prompt["name"] = os.path.splitext(os.path.basename(path))[0]
    return prompt


def generate(prompt, output_dir=Config.SCHEM_DIR):
    build_type = prompt.get("type", "house")
    name = prompt.get("name", "untitled")
    version_str = prompt.get("version", DEFAULT_VERSION)
    mc_version = VERSION_MAP.get(version_str, VERSION_MAP[max(VERSION_MAP.keys())])

    builder = BUILDERS.get(build_type)
    if not builder:
        print(f"  ERROR: Unknown build type '{build_type}'")
        return None

    schem = mcschematic.MCSchematic()
    print(f"  Building [{build_type}] '{name}'...")
    start = time.time()
    builder(schem, prompt)
    elapsed = time.time() - start
    print(f"  Build completed in {elapsed:.2f}s")

    os.makedirs(output_dir, exist_ok=True)
    schem.save(output_dir, name, mc_version)
    return os.path.join(output_dir, f"{name}.schem")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_schematic.py <prompt.json> [--output <dir>]")
        sys.exit(1)

    prompt_path = sys.argv[1]
    output_dir = Config.SCHEM_DIR
    if "--output" in sys.argv:
        output_dir = sys.argv[sys.argv.index("--output") + 1]

    prompt = load_prompt(prompt_path)
    generate(prompt, output_dir)
