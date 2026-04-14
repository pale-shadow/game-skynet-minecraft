import pytest
from src.mcp_server.mcp_server import get_system_load

@pytest.mark.asyncio
async def test_get_system_load():
    """Test that get_system_load returns a string representing load average."""
    load = await get_system_load()
    assert isinstance(load, str)
    # Load average is usually 3 numbers in a tuple-like string, e.g., "(0.5, 0.6, 0.7)"
    assert "(" in load and ")" in load
    assert "," in load
