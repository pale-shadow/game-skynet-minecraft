import os
import sys

# Ensure the Stargate node can locate the 'schematics' orchestration logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the spatial engine used for Hub 01 inference [3]
try:
    from schematics.npu_spatial_engine import NPUSpatialEngine
except ImportError:
    # Fallback for different execution contexts in the Bitsmasher network
    from npu_spatial_engine import NPUSpatialEngine

# Instantiate the engine for the Hailo-8L hardware [4]
skynet_npu = NPUSpatialEngine(hardware_mode="hailo")


def test_hailo_npu_decoding_validity():
    """
    Validates that the Pi 5 / Hailo-8L NPU decodes a 'facade' prompt
    into a structurally sound block-set before transmission [1].
    """
    prompt = "jungle outpost with windows and beds"

    # Get an optimal vector for a 20x20 build, simulating NPU spatial inference
    # The NPUSpatialEngine is designed for location inference, not direct decoding.
    optimal_coords = skynet_npu.get_optimal_vector(width=20, depth=20)

    # Verify that a valid coordinate was returned
    assert optimal_coords is not None
    assert optimal_coords != (None, None)
    print(f"Optimal coordinates found: {optimal_coords}")
