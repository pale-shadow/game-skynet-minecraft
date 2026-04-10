import argparse
import json
import os
import sys
import time

# Add project root to sys.path for correct module resolution
# PROJECT_ROOT is calculated relative to the location of this script (src/schematics/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

# Import necessary modules after adjusting sys.path
try:
    from npu_spatial_engine import NPUSpatialEngine
    from skynet_core import Config

    from mcrcon import (
        MCRcon,
    )  # Assuming mcrcon is installed or available in the environment
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(
        "Please ensure the project is set up correctly and dependencies are installed."
    )
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)


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
        print(
            "Usage: python src/schematics/batch_generate.py <prompt.json> [--output <dir>]"
        )
        sys.exit(1)

    prompt_path = sys.argv[1]
    output_dir = Config.SCHEM_DIR
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[sys.argv.index("--output") + 1]

    prompt = load_prompt(prompt_path)
    generate(prompt, output_dir)
