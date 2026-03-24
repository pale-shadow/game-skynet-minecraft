import os
import time
import random
import logging
import subprocess
import importlib
import re
from datetime import datetime, timedelta
from skynet_core import Config, SkynetRCON, setup_logging
from adaptive_mutation_v7 import AdaptiveMutator
from skynet_process import get_hailo_structure_logic
import mcschematic

# Setup standardized logging
logger = setup_logging("skynet_unified")

class SkynetUnifiedDaemon:
    """
    The Unified Skynet Brain (2026 Urbanization Phase).
    Consolidates Urbanization, Mutation, Containment, and Health Monitoring.
    """
    def __init__(self):
        self.rcon = SkynetRCON()
        self.mutator = AdaptiveMutator()
        
        # State Tracking
        self.last_rcon_check = 0
        self.last_player_check = 0
        self.last_urbanization_build = 0 # Hourly .schem
        self.last_void_tech_build = 0     # Hourly Void-Tech (fill)
        
        self.players_in_zone = {} # { "name": last_warning_time }
        
    def get_temp(self):
        """Monitors Pi 5 hardware temperature."""
        try:
            res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
            return float(res.replace("temp=", "").replace("'C\n", ""))
        except Exception as e:
            logger.error(f"Thermal Monitoring Failure: {e}")
            return 0.0

    def get_players_in_restricted_zones(self):
        """Audits all designated sectors for human presence."""
        detected = set()
        resp = self.rcon.send("list", silent=True)
        if not resp or ":" not in str(resp):
            return detected
            
        try:
            player_names = str(resp).split(":")[1].strip().split(", ")
            if not player_names or player_names == ['']:
                return detected
        except IndexError:
            return detected

        for name in player_names:
            name = name.strip()
            pos_resp = self.rcon.send(f"data get entity {name} Pos", silent=True)
            if not pos_resp: continue
            
            match = re.search(r'\[(-?[\d\.]+)d, (-?[\d\.]+)d, (-?[\d\.]+)d\]', str(pos_resp))
            if not match: continue
                
            px, _, pz = map(float, match.groups())

            for sector_name, bounds in Config.SECTORS.items():
                x_b, z_b = bounds["x"], bounds["z"]
                if x_b[0] <= px <= x_b[1] and z_b[0] <= pz <= z_b[1]:
                    logger.info(f"Player '{name}' detected in restricted sector: {sector_name}")
                    detected.add(name)
                    break
        return detected

    def run_urbanization_cycle(self):
        """Selects, generates, and deploys a high-fidelity schematic."""
        logger.info("🏗 Starting Urbanization Build Cycle (.schem)...")
        
        types = ["house", "tower", "bridge", "castle", "station"] 
        selected_type = random.choice(types)
        build_name = f"SKYNET_{selected_type.upper()}_{random.randint(1000, 9999)}"

        sector_name = random.choice(list(Config.SECTORS.keys()))
        bounds = Config.SECTORS[sector_name]
        tx = random.randint(bounds["x"][0], bounds["x"][1])
        tz = random.randint(bounds["z"][0], bounds["z"][1])
        ty = Config.FIELD_BOUNDS["y_base"]

        logger.info(f"SELECTED: {build_name} in {sector_name}")

        try:
            # Modular Builder Import
            module_name = "station2" if selected_type == "station" else selected_type
            builder_module = importlib.import_module(f"builders.{module_name}")
            builder_func = getattr(builder_module, "build" if selected_type == "station" else f"build_{selected_type}")

            prompt = {
                "name": build_name,
                "dimensions": {"width": random.randint(10, 20), "height": random.randint(15, 35), "length": random.randint(10, 20)},
                "features": {"void_tech": True, "has_roof": True, "crenellations": True}
            }

            schem = mcschematic.MCSchematic()
            builder_func(schem, prompt)
            
            os.makedirs(Config.SCHEM_DIR, exist_ok=True)
            schem.save(Config.SCHEM_DIR, build_name, mcschematic.Version.JE_1_21_1)
            logger.info(f"✅ Generated: {build_name}.schem")

            # Deployment
            self.rcon.send(f"say [Skynet] Commencing Urbanization of '{build_name}' in {sector_name}.")
            self.rcon.send(f"//schem load {build_name}")
            self.rcon.send(f"execute positioned {tx} {ty} {tz} run //paste -a")
            logger.info(f"🚀 Deployed {build_name} to {sector_name}")

        except Exception as e:
            logger.error(f"❌ Urbanization Error: {e}")

    def run_void_tech_cycle(self):
        """Generates a procedural Void-Tech structure using direct fill commands."""
        logger.info("🏗 Starting Void-Tech Mutation Cycle (NPU)...")
        try:
            sector = random.choice(list(Config.SECTORS.keys()))
            cmds = get_hailo_structure_logic(sector=sector)
            if cmds:
                self.rcon.send(cmds)
                logger.info(f"✅ Successfully mutated area in {sector}")
        except Exception as e:
            logger.error(f"❌ Void-Tech Error: {e}")

    def run_loop(self):
        logger.info("🚀 Skynet Unified Brain v1.5: INITIALIZED")
        logger.info(f"📡 Hardware: Pi 5 + Hailo-8L (Threshold: {Config.TEMP_THRESHOLD}'C)")
        Config.log_config(logger)
        
        while True:
            now = time.time()
            temp = self.get_temp()

            # 1. RCON Health Check (Every 5 mins)
            if now - self.last_rcon_check >= Config.RCON_CHECK_INTERVAL:
                if self.rcon.check_health():
                    logger.info("📡 RCON Link: ACTIVE")
                else:
                    logger.warning("📡 RCON Link: DOWN")
                self.last_rcon_check = now

            # 2. Player Monitoring & Warnings (Every 10 mins)
            if now - self.last_player_check >= Config.PLAYER_CHECK_INTERVAL:
                detected = self.get_players_in_restricted_zones()
                # Update tracking
                for name in detected:
                    if name not in self.players_in_zone:
                        self.players_in_zone[name] = 0 # Immediate warning
                for name in list(self.players_in_zone.keys()):
                    if name not in detected:
                        del self.players_in_zone[name]
                self.last_player_check = now

            # 3. Active Warning Broadcast (Every 30s)
            for name, last_warn in self.players_in_zone.items():
                if now - last_warn >= Config.WARNING_INTERVAL:
                    self.rcon.send(f'tellraw {name} ["", {{"text":"[SKYNET]","color":"dark_red"}}, {{"text":" WARNING: You are in a restricted automated construction zone. Please vacate.","color":"red"}}]')
                    self.players_in_zone[name] = now

            # 4. Thermal Safety Guard
            if temp > Config.TEMP_THRESHOLD:
                logger.warning(f"⚠ Thermal Throttling ({temp}'C). Build cycles suspended.")
                time.sleep(30)
                continue

            # 5. Build Cycles (Hourly)
            if now - self.last_urbanization_build >= Config.BUILD_COOLDOWN:
                # 5.1 Adaptive Mutation ( Sculk infection scan )
                try:
                    self.mutator.run_cycle()
                except Exception as e:
                    logger.error(f"❌ Mutation Error: {e}")
                
                # 5.2 High-Fidelity Urbanization
                self.run_urbanization_cycle()
                self.last_urbanization_build = now
                
            if now - self.last_void_tech_build >= Config.BUILD_COOLDOWN + 1800: # Staggered by 30 mins
                # 5.3 NPU Procedural Void-Tech
                self.run_void_tech_cycle()
                self.last_void_tech_build = now

            time.sleep(10)

if __name__ == "__main__":
    daemon = SkynetUnifiedDaemon()
    daemon.run_loop()
