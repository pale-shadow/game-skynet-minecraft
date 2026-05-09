import os
import socket
import sys
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.utils.config_utils import setup_logging

# ==========================================
# TEST ROUTING AND EXECUTION LOGIC
# ==========================================


def pytest_configure(config):
    """Register custom markers to avoid Pytest warnings during suite initialization."""
    config.addinivalue_line(
        "markers", "host(name): mark test to run only on a specific host"
    )
    config.addinivalue_line(
        "markers", "database: mark test as requiring a database connection"
    )
    config.addinivalue_line(
        "markers", "world_state: mark test as requiring Minecraft .mca files"
    )


def pytest_runtest_setup(item):
    """Intercept tests marked with @pytest.mark.host and skip if executing on the wrong node."""
    host_marker = item.get_closest_marker("host")
    if host_marker:
        required_host = host_marker.args[0]
        # Strip domain suffix to match shortnames (e.g., 'chonk.lab.bitsmasher.net' -> 'chonk')
        current_host = socket.gethostname().split(".")[0]

        if current_host != required_host:
            pytest.skip(
                f"Skipped: Test requires host '{required_host}', but running on '{current_host}'"
            )


# ==========================================
# GLOBAL FIXTURES AND MOCKS
# ==========================================


@pytest.fixture(scope="session", autouse=True)
def global_setup():
    """Global setup for the test suite, including logging."""
    setup_logging("test", log_file="logs/test_suite.log")


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
    """Inject required environment variables for offline/isolated testing."""
    monkeypatch.setenv("RCON_PASS", "test_pass")
    monkeypatch.setenv("CHONK_IP", "127.0.0.1")
    monkeypatch.setenv("RCON_PORT", "25575")
    if "GOOGLE_API_KEY" not in os.environ:
        monkeypatch.setenv("GOOGLE_API_KEY", "testing_key")
