import asyncio
import json
import logging
import sys
import os

# Add the project root to sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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
        """
        Validates the incoming packet and routes it to the appropriate handler.
        """
        if not validate_telemetry_packet(payload):
            logger.warning("Dropping invalid telemetry packet due to validation failure.")
            return

        event_type = payload.get("EVENT")
        handler = EVENT_HANDLERS.get(event_type)
        
        if handler:
            try:
                await handler(payload)
                logger.info(f"Successfully processed {event_type} from {payload.get('NODE')}")
            except Exception as e:
                logger.error(f"Handler for {event_type} failed: {e}")
        else:
            logger.warning(f"No handler registered for event type: {event_type}")

    async def handle_connection(self, reader, writer):
        """
        Handles incoming TCP streams with line-buffered reading for JSON packets.
        """
        addr = writer.get_extra_info('peername')
        logger.info(f"Connected to telemetry source: {addr}")

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                message = data.decode().strip()
                if not message:
                    continue

                logger.debug(f"Received raw telemetry: {message}")

                try:
                    payload = json.loads(message)
                    await self._dispatch_event(payload)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON fragment received from {addr}: {message[:50]}...")

        except Exception as e:
            logger.exception(f"Error processing telemetry from {addr}: {e}")
        finally:
            logger.info(f"Closing connection from {addr}")
            writer.close()
            await writer.wait_closed()

    async def start(self):
        """
        Starts the asyncio TCP server.
        """
        try:
            server = await asyncio.start_server(
                self.handle_connection, 
                self.host, 
                self.port,
                reuse_address=True
            )
        except OSError as e:
            if e.errno == 98:
                logger.critical(f"Port {self.port} is already in use. Ensure stargate-daemon.py is stopped.")
            raise e
        
        addr = server.sockets[0].getsockname()
        logger.info(f"Telemetry listener operational on {addr}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    # Configure logging for standalone execution
    from src.utils.config_utils import setup_logging
    setup_logging("stargate_telemetry_listener")
    
    listener = TelemetryListener()
    try:
        asyncio.run(listener.start())
    except KeyboardInterrupt:
        logger.info("Stargate listener shutdown by user.")
    except OSError:
        # Silent exit on bind error as it is logged in start()
        sys.exit(1)
