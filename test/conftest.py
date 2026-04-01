import os
import sys
from unittest.mock import MagicMock

import pytest

# Ensure schematic-agent is in the path for testing
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../schematic-agent"))
)


@pytest.fixture
def mock_rcon():
    """Mocked RCON client to avoid real server calls during unit tests."""
    mock = MagicMock()
    mock.send.return_value = "Mocked Response"
    mock.check_health.return_value = True
    return mock


@pytest.fixture
def mock_thermal():
    """Mocked thermal data (70 degrees is safe)."""
    return 70.0


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Ensure tests don't fail due to missing environment variables."""
    monkeypatch.setenv("RCON_PASS", "test_pass")
    monkeypatch.setenv("CHONK_IP", "127.0.0.1")
    monkeypatch.setenv("RCON_PORT", "25575")
