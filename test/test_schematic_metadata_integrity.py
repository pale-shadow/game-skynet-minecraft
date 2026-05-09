import json
import os

import pytest
from skynet_core import Config

SCHEM_DIR = Config.SCHEM_DIR


def get_schematic_files():
    """Retrieve all schematic files from the project directory."""
    schem_files = []
    for root, _, files in os.walk(SCHEM_DIR):
        for f in files:
            if f.endswith((".schem", ".schematic")):
                schem_files.append(os.path.join(root, f))
    return schem_files


@pytest.mark.parametrize("schem_path", get_schematic_files())
def test_metadata_integrity(schem_path):
    """
    Validates that every schematic has a corresponding JSON metadata file
    and that the JSON structure is complete and valid.
    Checks both the side-by-side location and the centralized build_metadata directory.
    """
    schem_filename = os.path.basename(schem_path)
    schem_name = os.path.splitext(schem_filename)[0]

    # Path 1: Side-by-side
    json_path_side = os.path.splitext(schem_path)[0] + ".json"

    # Path 2: Centralized metadata dir
    json_path_central = os.path.join(Config.JSON_METADATA_DIR, f"{schem_name}.json")

    # 1. Check for existence in either location
    json_path = None
    if os.path.exists(json_path_side):
        json_path = json_path_side
    elif os.path.exists(json_path_central):
        json_path = json_path_central

    assert (
        json_path is not None
    ), f"Missing metadata for {schem_path} (checked side-by-side and {Config.JSON_METADATA_DIR})"

    # 2. Validate JSON formatting
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON format in {json_path}: {e}")

    # 3. Validate mandatory top-level fields
    required_top_level = [
        "build_id",
        "provenance",
        "hardware_telemetry",
        "spatial_data",
        "performance_impact",
    ]
    for field in required_top_level:
        assert (
            field in data
        ), f"Missing required top-level field '{field}' in {json_path}"

    # 4. Validate Spatial Data (Critical for overlap detection)
    spatial = data.get("spatial_data", {})
    assert "origin" in spatial, f"Missing 'origin' in spatial_data for {json_path}"
    assert (
        "dimensions" in spatial
    ), f"Missing 'dimensions' in spatial_data for {json_path}"

    origin = spatial.get("origin", {})
    dimensions = spatial.get("dimensions", {})

    for axis in ["x", "y", "z"]:
        assert axis in origin, f"Missing origin axis '{axis}' in {json_path}"
        assert isinstance(
            origin[axis], (int, float)
        ), f"Origin axis '{axis}' must be numeric in {json_path}"

    for dim in ["width", "height", "length"]:
        assert dim in dimensions, f"Missing dimension '{dim}' in {json_path}"
        assert isinstance(
            dimensions[dim], (int, float)
        ), f"Dimension '{dim}' must be numeric in {json_path}"

    # 5. Validate Schematic Type (Foundation vs. Delta)
    # v5 Requirement: Distinguish between the building core and greebling layers
    schem_type = data.get("schematic_type", "unknown")
    assert schem_type in [
        "Foundation",
        "Delta",
    ], f"Invalid or missing 'schematic_type' in {json_path}. Must be 'Foundation' or 'Delta'."

    # 6. Validate Hardware Telemetry (Attribution)
    telemetry = data.get("hardware_telemetry", {})
    inf_node = telemetry.get("inference_node", "unknown")
    assert (
        inf_node != "unknown"
    ), f"Inference node is 'unknown' in {json_path}. Must be attributed to a valid host."
    assert inf_node in [
        "Skynet-Pi5-Hailo8L",
        "Pi5 / NVMe (Stargate)",
        "retroactive_generator",
    ], f"Invalid inference node '{inf_node}' in {json_path}"
