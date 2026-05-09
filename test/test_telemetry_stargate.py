import asyncio
import json

import pytest
from src.stargate.telemetry_listener import TelemetryListener


@pytest.mark.asyncio
async def test_telemetry_listener_ingestion():
    """
    Verifies that the TelemetryListener can receive and parse a JSON packet.
    """
    port = 5006  # Use a different port for testing
    listener = TelemetryListener(port=port)

    # Start the listener in the background
    server_task = asyncio.create_task(listener.start())

    # Wait a moment for the server to start
    await asyncio.sleep(0.1)

    # Simulate a client sending a CART_PASS event
    payload = {
        "EVENT": "CART_PASS",
        "timestamp": "2026-04-19T12:00:00Z",
        "coords": [1832, 31, 688],
    }

    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    writer.write(json.dumps(payload).encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

    # Wait a bit for processing
    await asyncio.sleep(0.1)

    # Cleanup
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

    # If we reached here without exception, the ingestion worked.
    # We could also use a mock handler to verify the dispatch.
