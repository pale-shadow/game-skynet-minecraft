from src.utils.config_utils import setup_logging
from src.rail.telemetry_receiver import RailTelemetryProcessor # Import the new processor

logger = setup_logging("stargate")

# Instantiate the processor once
rail_telemetry_processor = RailTelemetryProcessor()

async def handle_cart_pass(payload):
    """
    Handles the CART_PASS event from the Chonk host.
    Delegates to RailTelemetryProcessor for logging and LLM orchestration.
    """
    logger.info(f"Processing CART_PASS event: {payload}")
    coords_raw = payload.get('coords', 'unknown')
    node = payload.get('NODE', 'unknown')
    
    print(f"[HANDLER] Minecart detected at {coords_raw} on node {node}")
    
    # Delegate the event processing to the RailTelemetryProcessor
    await rail_telemetry_processor.process_rail_event(payload)


