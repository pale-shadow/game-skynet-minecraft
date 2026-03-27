import re
import subprocess
import random
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
    
    handlers = [logging.FileHandler(log_file)]
    if not os.getenv("INVOCATION_ID"):
        handlers.append(logging.StreamHandler())
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        handlers=handlers
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
    def survey_site(self, x, z, radius=5):
        self.logger.info(f"🔍 Surveying site at ({x}, {z}) with radius {radius}...")
        return Config.FIELD_BOUNDS["y_base"]

class SkynetCore:
    def __init__(self, name="skynet_core"):
        self.name = name
        self.logger = setup_logging(name)
        self.rcon = SkynetRCON()
        self.last_thermal_check = 0
        self.last_player_check = 0
        self.players_in_zone = {}

    def get_temp(self):
        try:
            res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            return float(res.replace("temp=", "").replace("\x27C\\n", ""))
        except Exception:
            return 0.0

    def check_thermal(self):
        temp = self.get_temp()
        if temp > Config.TEMP_THRESHOLD:
            self.logger.warning(f"⚠️ Thermal Throttling: {temp}°C > {Config.TEMP_THRESHOLD}°C")
            return False
        return True

    def get_players_in_zones(self):
        detected = set()
        resp = self.rcon.send("list", silent=True)
        if not resp or ":" not in str(resp):
            return detected
        try:
            player_names = str(resp).split(":")[1].strip().split(", ")
            if not player_names or player_names == [""]:
                return detected
        except IndexError:
            return detected
        for name in player_names:
            name = name.strip()
            pos_resp = self.rcon.send(f"data get entity {name} Pos", silent=True)
            if not pos_resp: continue
            match = re.search(r"\\[(-?[\\d\\.]+)d, (-?[\\d\\.]+)d, (-?[\\d\\.]+)d\\]", str(pos_resp))
            if not match: continue
            px, _, pz = map(float, match.groups())
            for sector_name, bounds in Config.SECTORS.items():
                x_b, z_b = bounds["x"], bounds["z"]
                if x_b[0] <= px <= x_b[1] and z_b[0] <= pz <= z_b[1]:
                    self.logger.info(f"👤 Player \x27{name}\x27 detected in restricted sector: {sector_name}")
                    detected.add(name)
                    break
        return detected

    def send_warning(self, player_name):
        msg = f"tellraw {player_name} [SKYNET] Restricted Zone Incursion Detected. Proceed with caution."
        self.rcon.send(msg)
        self.players_in_zone[player_name] = time.time()
