import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure schematic-agent is in the path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../schematics"))
)

from skynet_core import Config, SkynetCore
from skynet_unified import SkynetUnifiedDaemon


def test_skynet_core_initialization():
    """Verify that SkynetCore initializes properly with its logger and RCON client."""
    core = SkynetCore(name="test_core")
    assert core.name == "test_core"
    assert core.rcon is not None
    assert core.logger is not None


def test_skynet_core_thermal_throttling():
    """Verify that check_thermal handles safe and unsafe temperatures correctly."""
    core = SkynetCore(name="test_core")

    with patch.object(core, "get_temp", return_value=60.0):
        assert core.check_thermal() is True

    with patch.object(core, "get_temp", return_value=85.0):
        assert core.check_thermal() is False


def test_skynet_unified_daemon_logic():
    """Verify that the unified daemon handles cycles correctly (mocked)."""
    with patch("skynet_core.setup_logging"):
        daemon = SkynetUnifiedDaemon()
        daemon.rcon = MagicMock()

        # Test thermal check in urbanization cycle
        with patch.object(daemon, "check_thermal", return_value=False):
            daemon.run_urbanization_cycle()
            daemon.rcon.send.assert_not_called()

        # Test basic player detection call
        daemon.rcon.send.return_value = "There are 0 of a max 20 players online:"
        players = daemon.get_players_in_zones()
        assert isinstance(players, set)
        assert len(players) == 0
