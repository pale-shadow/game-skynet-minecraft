import mcschematic
from .config_utils import Config, SkynetRCON, SkynetUnifiedDaemon, setup_logging
from src.schematics.adaptive_mutation_v7 import AdaptiveMutator
from src.schematics.place_ai_warning_signs import place_random_warning
from src.schematics.skynet_orchestrator import get_node_logic, push_build_to_chonk

# Setup standardized logging
logger = setup_logging("skynet_unified")


class SkynetController(SkynetUnifiedDaemon):
    """
    The Master Controller for Skynet, running on Stargate host.
    Delegates inference to remote agents.
    """
    def __init__(self):
        super().__init__()
        self.agent_hosts = Config.AGENT_HOSTS
        logger.info(f"📡 Controller initialized with agents: {self.agent_hosts}")


class SkynetCore:
    """
    The core logic for Skynet daemons, providing shared utilities.
    """
    def __init__(self, name="skynet_core"):
        self.name = name
        self.logger = setup_logging(name)
        self.rcon = SkynetRCON()
        self.last_rcon_check = 0
        self.last_player_check = 0
        self.players_in_zone = {}

    @staticmethod
    def is_within_bounds(x, z, width=5, depth=5):
        bounds = Config.FIELD_BOUNDS
        return (bounds["min_x"] <= x and (x + width) <= bounds["max_x"]) and (
            bounds["min_z"] <= z and (z + depth) <= bounds["max_z"]
        )

    @staticmethod
    def generate_build_metadata(build_name, sector_name):
        """Generates text for the mandatory Archival Signs based on the 2026 protocol."""
        date_str = datetime.now().strftime("%b %d, %2026")
        return {
            "front": [
                f"&b&l{build_name}",
                f"&3Built: {date_str}",
                "&0Hardware: Pi5 / Hailo AI",
                "",
            ],
            "back": [
                "&8Daemon: Skynet v1.5",
                f"&0Sector: {sector_name}",
                "&2Status: Urbanized",
                "",
            ],
        }

    def get_temp(self):
        try:
            res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            return float(res.replace("temp=", "").replace("C", ""))
        except Exception as e:
            self.logger.error(f"Thermal Hardware Failure: {e}")
            return 0.0

    def check_thermal(self):
        temp = self.get_temp()
        if temp > Config.TEMP_THRESHOLD:
            self.logger.warning(
                f"⚠️ Thermal Throttling: {temp}°C > {Config.TEMP_THRESHOLD}°C"
            )
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
            if not pos_resp:
                continue
            match = re.search(
                r"\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]", str(pos_resp)
            )
            if not match:
                continue
            px, _, pz = map(float, match.groups())
            for sector_name, bounds in Config.SECTORS.items():
                x_b, z_b = bounds["x"], bounds["z"]
                if x_b[0] <= px <= x_b[1] and z_b[0] <= pz <= z_b[1]:
                    self.logger.info(
                        f"👤 Player '{name}' detected in restricted sector: {sector_name}"
                    )
                    detected.add(name)
                    break
        return detected

    def transfer_file(self, local_path, remote_path):
        """Transfers a file to the Minecraft server (chonk) via scp if needed."""
        if os.path.abspath(local_path) == os.path.abspath(remote_path):
            self.logger.info(f"📁 File already at destination (NFS): {remote_path}")
            return True
        try:
            # Ensure the destination directory exists (optional, but scp needs it)
            # cmd_mkdir = ["ssh", f"minecraft@{self.rcon.host}", f"mkdir -p {os.path.dirname(remote_path)}"]
            # subprocess.run(cmd_mkdir, check=True)
            
            cmd = ["scp", local_path, f"minecraft@{self.rcon.host}:{remote_path}"]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.logger.info(f"📤 Transferred {local_path} to {self.rcon.host}:{remote_path}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"❌ Transfer Failure (scp): {e.stderr}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Transfer Failure: {e}")
            return False

    def send_warning(self, player_name):
        msg = f"tellraw {player_name} [SKYNET] Restricted Zone Incursion Detected. Proceed with caution."
        self.rcon.send(msg)
        self.players_in_zone[player_name] = time.time()

    # --- SkynetCore specific methods ---
    def run_loop(self):
        """Main daemon loop for core functionalities."""
        logger.info(f"🚀 Skynet Core Daemon '{self.name}': ACTIVE")
        Config.log_config(logger)

        while True:
            now = time.time()

            # 1. RCON Health Check
            if now - self.last_rcon_check >= Config.RCON_CHECK_INTERVAL:
                if self.rcon.check_health():
                    logger.info("📡 RCON Link: ACTIVE")
                self.last_rcon_check = now

            # 2. Player Check in Zones
            if now - self.last_player_check >= Config.PLAYER_CHECK_INTERVAL:
                detected = self.get_players_in_zones()
                for name in detected:
                    last_warn = self.players_in_zone.get(name, 0)
                    if now - last_warn >= Config.WARNING_INTERVAL:
                        self.send_warning(name)
                self.last_player_check = now
            
            # Add more core daemon tasks here if needed
            
            time.sleep(10) # Short sleep to avoid busy-waiting


# --- Main Execution Block ---
if __name__ == "__main__":
    # Example of how to run core daemon components if needed
    # core = SkynetCore()
    # core.run_loop() # This would need to be managed by systemd or similar
    pass # Placeholder if this file is imported elsewhere
