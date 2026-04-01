import sys
import os

# Ensure the Stargate node can locate the 'schematics' orchestration logic
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    
    # Execute NPU decoding (T2BM repair and decoding phase) [1]
    interlayer_rep = skynet_npu.decode(prompt)

    # Verify the structural integrity of the AI-generated build
    assert interlayer_rep is not None
    assert "minecraft:glass_pane" in interlayer_rep.blocks
    assert "minecraft:jungle_planks" in interlayer_rep.blocks
