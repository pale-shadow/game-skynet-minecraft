import os
import json
import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from rail.rail_manager import RailManager, BlueMapMarkerUpdater
from src.stargate.handlers.cart_handler import handle_cart_pass
from src.rail.telemetry_receiver import RailTelemetryProcessor, rail_traffic_logger

def test_marker_file_integrity(tmp_path):
    """
    Verifies that the BlueMapMarkerUpdater correctly writes and formats the markers.json file.
    """
    marker_file = tmp_path / "markers.json"
    updater = BlueMapMarkerUpdater(str(marker_file))
    
    coords = {"x": -1212, "y": 76, "z": -670}
    updater.update_switch("washington_main", "Washington Main", coords, True)
    
    assert marker_file.exists()
    with open(marker_file, 'r') as f:
        data = json.load(f)
    
    assert "rail_switches" in data["markerSets"]
    markers = data["markerSets"]["markerSets"]["rail_switches"]["markers"]
    assert "washington_main" in markers
    assert markers["washington_main"]["position"] == coords
    assert "ACTIVE" in markers["washington_main"]["label"]

@patch("rail.rail_manager.MCRcon")
def test_rail_manager_rcon_integration(mock_rcon_class):
    """
    Tests the RailManager's ability to send RCON commands and handle responses.
    """
    mock_rcon = mock_rcon_class.return_value.__enter__.return_value
    mock_rcon.command.return_value = "Changed the block at -1212, 76, -670"
    
    manager = RailManager()
    
    # Mock registry data
    test_registry = {
        "switches": {
            "test_switch": {
                "name": "Test Switch",
                "coords": {"x": -1212, "y": 76, "z": -670},
                "state": False
            }
        }
    }
    
    with patch.object(manager, "_load_registry", return_value=test_registry):
        with patch.object(manager, "_save_registry"):
            # Mock marker updater to avoid file I/O
            with patch.object(manager.marker_updater, "_save"):
                success = manager.toggle_switch("test_switch", True)
                
                assert success is True
                # Verify RCON command was called with correct parameters
                args, _ = mock_rcon.command.call_args
                assert "setblock -1212 76 -670" in args[0]
                assert "powered=true" in args[0]

def test_rail_manager_safety_interlock():
    """
    Verifies that the safety interlock can abort a switch toggle.
    """
    manager = RailManager()
    
    test_registry = {
        "switches": {
            "test_switch": {
                "name": "Test Switch",
                "coords": {"x": 100, "y": 64, "z": 100},
                "state": False
            }
        }
    }
    
    with patch.object(manager, "_load_registry", return_value=test_registry):
        # Force safety failure
        with patch.object(manager, "_verify_tpu_safety", return_value=False):
            success = manager.toggle_switch("test_switch", True)
            assert success is False
            # Ensure RCON was NOT called (we can patch MCRcon here too if we want to be sure)

@pytest.mark.asyncio
@patch("src.rail.telemetry_receiver.RailManager", autospec=True) # Mock RailManager class in telemetry_receiver
@patch("src.rail.telemetry_receiver.rail_traffic_logger", autospec=True) # Mock the logger in telemetry_receiver
async def test_rail_telemetry_processor_orchestration_flow(
    mock_rail_traffic_logger, MockRailManagerClass
):
    """
    Verifies the internal flow of RailTelemetryProcessor:
    logging, LLM orchestration (placeholder), and calling RailManager.
    """
    # Arrange
    # Mock the RailManager instance that RailTelemetryProcessor will create
    mock_rail_manager_instance = MockRailManagerClass.return_value
    # Ensure toggle_switch is an awaitable mock
    mock_rail_manager_instance.toggle_switch = AsyncMock(return_value=True)

    processor = RailTelemetryProcessor()

    mock_telemetry_payload = {
        "EVENT": "CART_PASS",
        "NODE": "CHONK-01",
        "coords": {"x": 100, "y": 64, "z": 200},
        "timestamp": "2026-05-06T12:00:00Z",
    }

    expected_llm_decision = {"action": "toggle_switch", "switch_id": "chonk_01_sensor", "state": True}


    # Act
    await processor.process_rail_event(mock_telemetry_payload)

    # Assert
    # 1. Verify logging of received telemetry
    mock_rail_traffic_logger.info.assert_any_call(
        f"Received rail telemetry: {json.dumps(mock_telemetry_payload)}"
    )

    # 2. Verify logging of LLM orchestration input
    mock_rail_traffic_logger.info.assert_any_call(
        f"LLM Orchestration: Receiving event for analysis: {mock_telemetry_payload}"
    )

    # 3. Verify logging of LLM orchestration decision
    mock_rail_traffic_logger.info.assert_any_call(
        f"LLM Orchestration: Decision for CHONK-01: {expected_llm_decision}"
    )

    # 4. Verify RailManager.toggle_switch was called with the correct arguments
    mock_rail_manager_instance.toggle_switch.assert_called_once_with(
        expected_llm_decision["switch_id"], expected_llm_decision["state"]
    )

    # Ensure no error logs were made during this successful path
    mock_rail_traffic_logger.error.assert_not_called()


if __name__ == "__main__":
    pytest.main([__file__])
