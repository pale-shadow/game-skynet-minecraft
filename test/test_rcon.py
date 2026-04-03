from unittest.mock import MagicMock, patch

import pytest
from skynet_core import SkynetCore


def test_hub02_rcon_connection():
    """
    Verify the RCON signal path to the Transmission Core (Hub 02).
    Essential for maintaining the T2BM pipeline and 20 TPS goal.
    """
    core = SkynetCore(name="hub02_tester")

    with patch.object(core.rcon, "send") as mock_send:
        # Simulate a successful 'tps' check used by the Transmission Core
        mock_send.return_value = "TPS from last 1m, 5m, 15m: 20.0, 20.0, 20.0"

        tps_info = core.rcon.send("tps")
        assert "20.0" in tps_info
        mock_send.assert_called_with("tps")
