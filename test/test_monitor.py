# test/test_monitor.py
import pytest


@pytest.mark.host("blowfish")
@pytest.mark.database
def test_mariadb_idle_connections():
    """Will only execute if the hostname resolves to 'blowfish'."""
    # DB connection logic here...
    pass


# test/test_lfs_hydration_state.py
import pytest


@pytest.mark.host("chonk")
@pytest.mark.world_state
def test_mca_binary_magic_bytes():
    """Will only execute on the Minecraft execution node."""
    # Read .mca chunk headers here...
    pass
