import asyncio
import json
import logging
from mcrcon import MCRcon

# Configuration - typically loaded from env
RCON_HOST = "10.10.8.60" # Chonk
RCON_PORT = 25575
RCON_PASS = "dinosaurExTraVaGanZa1969"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RCON_TEST")

async def test_rcon_bridge():
    logger.info(f"Connecting to RCON at {RCON_HOST}:{RCON_PORT}...")
    try:
        with MCRcon(RCON_HOST, RCON_PASS, port=RCON_PORT) as mcr:
            resp = mcr.command("list")
            logger.info(f"Server Response: {resp}")
            
            # Test sending a command
            # resp = mcr.command("say AI Telemetry Bridge Test")
            # logger.info(f"Command Response: {resp}")
            
    except Exception as e:
        logger.error(f"RCON Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_rcon_bridge())
