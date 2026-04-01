import mcschematic
import pytest


def test_house_builder():
    """Verify that the house builder runs without error and modifies the schematic."""
    from builders.house import build_house

    schem = mcschematic.MCSchematic()

    prompt = {
        "dimensions": {"width": 10, "height": 10, "length": 10},
        "features": {"void_tech": True, "has_roof": True},
    }

    # Check that it doesn't crash
    build_house(schem, prompt)

    # Check that blocks were added
    assert len(schem._blocks) > 0


def test_station2_builder():
    """Verify that the advanced industrial station builder runs correctly."""
    from builders.station2 import build

    schem = mcschematic.MCSchematic()

    prompt = {
        "name": "TEST_STATION",
        "dimensions": {"width": 15, "height": 20, "length": 15},
    }

    build(schem, prompt)

    # Check that blocks were added
    assert len(schem._blocks) > 0
