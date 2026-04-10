from unittest.mock import MagicMock, patch

import pytest
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


def test_skynet_core_transfer_file():
    """Verify that transfer_file calls scp with correct arguments and handles NFS optimization."""
    with patch("skynet_core.setup_logging"):
        core = SkynetCore(name="test_core")
        core.rcon = MagicMock()
        core.rcon.host = "10.10.8.60"

        # Test 1: Standard transfer (different paths)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)

            local_path = "/tmp/test.schem"
            remote_path = Config.MINECRAFT_SCHEM_DIR + "/test.schem"

            result = core.transfer_file(local_path, remote_path)

            assert result is True
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]
            assert "scp" in cmd
            assert local_path in cmd
            assert f"minecraft@10.10.8.60:{remote_path}" in cmd

        # Test 2: NFS Optimization (same paths)
        with patch("subprocess.run") as mock_run:
            path = Config.MINECRAFT_SCHEM_DIR + "/test.schem"
            result = core.transfer_file(path, path)
            assert result is True
            mock_run.assert_not_called()

        # Test 3: Failure handling
        with patch("subprocess.run") as mock_run:
            from subprocess import CalledProcessError

            mock_run.side_effect = CalledProcessError(
                1, "scp", stderr="Permission denied"
            )

            result = core.transfer_file("/tmp/test.schem", "/remote/test.schem")
            assert result is False
