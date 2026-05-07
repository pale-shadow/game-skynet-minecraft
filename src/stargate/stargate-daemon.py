import asyncio
import json
import logging
import os
import sys

# Add the project root to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.stargate.telemetry_listener import TelemetryListener

from src.utils.config_utils import setup_logging

# Configure Logging
logger = setup_logging("stargate_daemon")

# Registry of remote construction hosts
REMOTE_HOSTS = {
    "skynet": "ws://skynet-pi5.local:8765",
    "edge-t": "ws://tpu-host.local:8765",
}

async def dispatch_build_intent(host_key, intent_type, location, dimensions):
    """
    Sends a T2BM 'Intent' to a specific hardware host.
    """
    import websockets
    payload = {
        "protocol": "T2BM_V1",
        "intent": intent_type,
        "coords": location,
        "size": dimensions,
        "metadata": {"origin": "STARGATE_MCP", "auth": "BAMA_DECK_01"},
    }

    uri = REMOTE_HOSTS.get(host_key)
    if not uri:
        logger.error(f"Unknown host key: {host_key}")
        return

    try:
        async with websockets.connect(uri) as websocket:
            logger.info(f"Dispatching {intent_type} to {host_key}...")
            await websocket.send(json.dumps(payload))
            response = await websocket.recv()
            logger.info(f"[{host_key}] Status: {response}")
    except Exception as e:
        logger.error(f"Failed to dispatch intent to {host_key}: {e}")

async def main():
    # Environment variables for configuration
    telemetry_port = int(os.getenv("TELEMETRY_PORT", 5005))
    
    logger.info("Initializing Stargate Daemon...")
    
    # Initialize Telemetry Listener
    listener = TelemetryListener(port=telemetry_port)
    
    # Start both the listener and any other background tasks
    await asyncio.gather(
        listener.start(),
        # We can add more async tasks here as needed
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stargate Daemon shutting down.")
