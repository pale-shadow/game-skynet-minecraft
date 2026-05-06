from src.utils.config_utils import setup_logging
from src.rail.rail_manager import RailManager

logger = setup_logging("stargate")
rail_manager = RailManager()

async def handle_cart_pass(payload):
    """
    Handles the CART_PASS event from the Chonk host.
    """
    logger.info(f"Processing CART_PASS event: {payload}")
    coords_raw = payload.get('coords', 'unknown')
    node = payload.get('NODE', 'unknown')
    
    print(f"[HANDLER] Minecart detected at {coords_raw} on node {node}")
    
    # Map NODE to specific switch/sensor IDs
    node_mapping = {
        "CHONK-01": "chonk_01_sensor",
        "CHONK-02": "chonk_02_sensor",
        "CHONK-03": "chonk_03_sensor"
    }
    
    switch_id = node_mapping.get(node)
    
    if switch_id:
        logger.info(f"Triggering switch/sensor {switch_id} due to CART_PASS from {node}")
        # Toggle logic: For sensors, we might want to just 'activate' it (True)
        # or flip the state. Here we'll set to True to power the rail.
        success = rail_manager.toggle_switch(switch_id, True)
        
        if success:
            logger.info(f"Successfully toggled {switch_id} via RCON.")
        else:
            logger.error(f"Failed to toggle {switch_id} via RCON.")
    else:
        logger.warning(f"No mapping found for node {node}. Ignoring event.")

