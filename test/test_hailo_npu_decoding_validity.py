def test_hailo_npu_decoding_validity():
    """
    Validates that the Pi 5 / Hailo-8L NPU decodes a 'facade' prompt
    into a structurally sound block-set before transmission.
    """
    prompt = "jungle outpost with windows and beds"
    # Logic migrated to Pi 5 NPU (Hub 01)
    interlayer_rep = skynet_npu.decode(prompt)

    assert interlayer_rep is not None
    assert "minecraft:glass_pane" in interlayer_rep.blocks
    assert "minecraft:jungle_planks" in interlayer_rep.blocks
    assert interlayer_rep.is_repaired is True  # Ensure 'repairing' phase completed
