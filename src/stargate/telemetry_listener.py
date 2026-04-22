import asyncio
import json
import logging
from src.stargate.handlers.cart_handler import handle_cart_pass
from src.stargate.internal.telemetry.validator import validate_telemetry_packet

logger = logging.getLogger(__name__)

# Map event types to their respective handlers
EVENT_HANDLERS = {
    "CART_PASS": handle_cart_pass,
}

class TelemetryListener:
    def __init__(self, host='0.0.0.0', port=5005):
        self.host = host
        self.port = port

    async def _dispatch_event(self, payload):
        if not validate_telemetry_packet(payload):
            logger.warning("Dropping invalid telemetry packet.")
            return

        event_type = payload.get("EVENT")
        handler = EVENT_HANDLERS.get(event_type)
        
        if handler:
            await handler(payload)
        else:
            logger.warning(f"No handler registered for event type: {event_type}")

    async def handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f"Connected to telemetry source: {addr}")

        try:
            data = await reader.read(2048)
            if not data:
                return

            message = data.decode().strip()
            logger.debug(f"Received raw telemetry: {message}")

            payload = json.loads(message)
            await self._dispatch_event(payload)

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from {addr}")
        except Exception as e:
            logger.exception(f"Error processing telemetry from {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(
            self.handle_connection, self.host, self.port
        )
        
        addr = server.sockets[0].getsockname()
        logger.info(f"Telemetry listener started on {addr}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    import sys
    import os
    # Add the project root to sys.path to resolve absolute imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '''..''', '''..''')))
    # Basic standalone test run
    logging.basicConfig(level=logging.INFO)
    listener = TelemetryListener()
    try:
        asyncio.run(listener.start())
    except KeyboardInterrupt:
        pass
