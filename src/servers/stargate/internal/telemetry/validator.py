import logging

logger = logging.getLogger(__name__)

def validate_telemetry_packet(payload):
    """
    Validates the structure and content of a telemetry packet.
    """
    required_fields = ["EVENT", "timestamp"]
    for field in required_fields:
        if field not in payload:
            logger.error(f"Missing required field: {field}")
            return False
    
    # Specific validation for EVENT types
    event_type = payload.get("EVENT")
    if event_type == "CART_PASS":
        if "coords" not in payload:
            logger.error("CART_PASS event missing 'coords'")
            return False
            
    return True
