import os
import time
import random
import logging
import subprocess
import importlib
import re
from datetime import datetime, timedelta
from skynet_core import Config, SkynetRCON, SkynetCore, setup_logging
from adaptive_mutation_v7 import AdaptiveMutator
from skynet_process import get_hailo_structure_logic
import mcschematic

# Setup standardized logging
logger = setup_logging("skynet_unified")

class SkynetUnifiedDaemon(SkynetCore):
    """
    The Unified Skynet Brain (2026 Urbanization Phase).
    Consolidates Urbanization, Mutation, Containment, and Health Monitoring.
    """
    def __init__(self):
        super().__init__("skynet_unified")
        self.mutator = AdaptiveMutator()
        
        # State Tracking
        self.last_rcon_check = 0
        self.last_player_check = 0
        self.last_urbanization_build = 0 # Hourly .schem
        self.last_void_tech_build = 0     # Hourly Void-Tech (fill)
        


    # Players and thermal logic inherited from SkynetCore

    def run_urbanization_cycle(self):
        if not self.check_thermal(): return
        """Selects, generates, and deploys a high-fidelity schematic."""
        logger.info("🏗 Starting Urbanization Build Cycle (.schem)...")
        
        types = ["house", "tower", "bridge", "castle", "station"] 
        selected_type = random.choice(types)
        build_name = f"SKYNET_{selected_type.upper()}_{random.randint(1000, 9999)}"

        sector_name = "AI Containment Area"
        bounds = {"x": (Config.FIELD_BOUNDS["min_x"], Config.FIELD_BOUNDS["max_x"]), "z": (Config.FIELD_BOUNDS["min_z"], Config.FIELD_BOUNDS["max_z"])}
        tx = random.randint(bounds["x"][0], bounds["x"][1])
        tz = random.randint(bounds["z"][0], bounds["z"][1])
        ty = self.rcon.survey_site(tx, tz)

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
            sector = "AI Containment Area"
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

            # 1. RCON Health Check
            if now - self.last_rcon_check >= Config.RCON_CHECK_INTERVAL:
                if self.rcon.check_health():
                    logger.info("📡 RCON Link: ACTIVE")
                self.last_rcon_check = now

            # 2. Player Check
            if now - self.last_player_check >= Config.PLAYER_CHECK_INTERVAL:
                detected = self.get_players_in_zones()
                for name in detected:
                    last_warn = self.players_in_zone.get(name, 0)
                    if now - last_warn >= Config.WARNING_INTERVAL:
                        self.send_warning(name)
                self.last_player_check = now

            # 3. Builds
            if now - self.last_urbanization_build >= Config.BUILD_COOLDOWN:
                self.run_urbanization_cycle()
                self.last_urbanization_build = now

            time.sleep(10)

if __name__ == "__main__":
    daemon = SkynetUnifiedDaemon()
    daemon.run_loop()
