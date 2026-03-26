import os
import logging
import time
from datetime import datetime
from mcrcon import MCRcon

class Config:
    """Centralized configuration and spatial boundaries for Skynet."""
    # Infrastructure
    CHONK_IP = os.getenv("CHONK_IP", "10.10.8.60")
    AI_HARDWARE = "10.10.16.10"
    MCP_HOST = "10.10.16.66"

    # RCON Credentials
    RCON_PASS = os.getenv("RCON_PASS")
    RCON_PORT = int(os.getenv("RCON_PORT", 25575))

    @classmethod
    def log_config(cls, logger):
        logger.info(f"⚙️ Config: IP={cls.CHONK_IP}, Port={cls.RCON_PORT}, Pass={'***' + cls.RCON_PASS[-2:] if cls.RCON_PASS else 'None'}")

    # Spatial Boundaries (AI Field / Urbanization Zones)
    # The 'AI Field' (Desert)
    FIELD_BOUNDS = {
        "min_x": -1539,
        "max_x": -945,
        "min_z": -913,
        "max_z": -489,
        "y_base": 64
    }

    # The 'Urbanization' Sectors
    SECTORS = {
        "Shroomville Urban District": {"x": (1600, 1850), "z": (650, 900)},
        "Silicon Ridge (Beta-Zone)": {"x": (1400, 1575), "z": (700, 875)},
        "Abyssal Reef (Ocean Sector)": {"x": (1900, 2050), "z": (700, 850)}
    }

    # Operational Parameters
    TEMP_THRESHOLD = 75.0  # Celsius
    BUILD_COOLDOWN = 3600  # Hourly
    RCON_CHECK_INTERVAL = 300 # 5 Minutes
    PLAYER_CHECK_INTERVAL = 600 # 10 Minutes
    WARNING_INTERVAL = 30 # 30 Seconds

    # Project Paths
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
    SCHEM_DIR = os.path.join(PROJECT_ROOT, "schematics", "schem_files")
    HISTORY_FILE = os.path.join(PROJECT_ROOT, "schematics", "input", "build_history.json")

def setup_logging(script_name):
    """Standardizes logging to the logs/ folder with absolute paths."""
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    log_file = os.path.join(Config.LOG_DIR, f"{script_name}.log")
    
    # Clear existing handlers to avoid duplication
    logging.getLogger().handlers = []
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(script_name)

class SkynetRCON:
    """Unified, resilient RCON client for Skynet."""
    def __init__(self):
        self.host = Config.CHONK_IP
        self.password = Config.RCON_PASS
        self.port = Config.RCON_PORT
        self.logger = logging.getLogger("RCON")

    def send(self, command, silent=False):
        """Sends a single command or a list of commands."""
        if not isinstance(command, list):
            command = [command]
            
        responses = []
        try:
            with MCRcon(self.host, self.password, port=self.port) as mcr:
                for cmd in command:
                    resp = mcr.command(cmd)
                    responses.append(resp)
                    if not silent and resp:
                        self.logger.debug(f"RCON Response: {resp}")
                    # Throttle for Hailo-8L throughput or server stability
                    if len(command) > 1:
                        time.sleep(0.01)
            return responses if len(responses) > 1 else responses[0]
        except Exception as e:
            self.logger.error(f"RCON Failure: {e}")
            return None

    def check_health(self):
        """Verifies server connectivity."""
        resp = self.send("list", silent=True)
        return resp is not None
