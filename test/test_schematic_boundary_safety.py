def test_schematic_boundary_safety():
    """
    Ensures new schematics do not overlap with Hub 01 (Logic Core)
    or Hub 02 (Transmission Core) coordinates.
    """
    new_schem_pos = {"x": -1340, "y": 84, "z": -664}  # Hub 01 Location
    # Collision check against Hub 01-07
    collision = check_hub_collision(new_schem_pos, radius=10)

    assert (
        collision is False
    ), "Schematic overlaps with critical Skynet Hub infrastructure!"
