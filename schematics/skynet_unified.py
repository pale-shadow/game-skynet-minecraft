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
import mcschematic
import json
from validate_no_overlaps import check_overlaps

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
        self.last_void_tech_build = 0     # 30-min Void-Tech (fill)
        self.last_mutation_cycle = 0      # 5-min Adaptive Mutation
        


    # Players and thermal logic inherited from SkynetCore

    def run_urbanization_cycle(self):
        if not self.check_thermal(): return
        """Selects, generates, and deploys a high-fidelity schematic."""
        logger.info("🏗 Starting Urbanization Build Cycle (.schem)...")
        
        types = ["house", "tower", "bridge", "castle", "station"] 
        selected_type = random.choice(types)
        build_name = f"SKYNET_{selected_type.upper()}_{random.randint(1000, 9999)}"

        sector_name = random.choice(list(Config.SECTORS.keys()))
        bounds = Config.SECTORS[sector_name]
        
        # Determine schematic dimensions dynamically
        width = random.randint(10, 20)
        height = random.randint(15, 35)
        length = random.randint(10, 20)

        tx = random.randint(bounds["x"][0], bounds["x"][1] - width) # Adjust max_x to prevent out-of-bounds
        tz = random.randint(bounds["z"][0], bounds["z"][1] - length) # Adjust max_z to prevent out-of-bounds
        ty = self.rcon.survey_site(tx, tz)

        logger.info(f"SELECTED: {build_name} of size {width}x{height}x{length} for deployment at ({tx}, {ty}, {tz}) in {sector_name}")

        try:
            # Modular Builder Import
            module_name = "station2" if selected_type == "station" else selected_type
            builder_module = importlib.import_module(f"builders.{module_name}")
            builder_func = getattr(builder_module, "build" if selected_type == "station" else f"build_{selected_type}")

            prompt = {
                "name": build_name,
                "dimensions": {"width": width, "height": height, "length": length},
                "features": {"void_tech": True, "has_roof": True, "crenellations": True}
            }

            # Pre-deployment overlap check
            proposed_build = {
                "id": build_name,
                "x1": tx, "y1": ty, "z1": tz,
                "x2": tx + width, "y2": ty + height, "z2": tz + length,
                "file": os.path.join(Config.SCHEM_DIR, f"{build_name}.schem") # Placeholder path
            }
            
            # Ensure JSON_METADATA_DIR exists for check_overlaps to read from
            os.makedirs(Config.JSON_METADATA_DIR, exist_ok=True)
            
            conflicts = check_overlaps(Config.JSON_METADATA_DIR, proposed_build)
            if conflicts:
                logger.warning(f"❌ Aborting build {build_name}: Detected {len(conflicts)} overlaps with existing structures. {conflicts}")
                return # Abort this build cycle

            schem = mcschematic.MCSchematic()
            builder_func(schem, prompt)
            
            os.makedirs(Config.SCHEM_DIR, exist_ok=True)
            schem_file_path = os.path.join(Config.SCHEM_DIR, build_name)
            schem.save(Config.SCHEM_DIR, build_name, mcschematic.Version.JE_1_21_1)
            logger.info(f"✅ Generated: {build_name}.schem")

            # Deployment
            self.rcon.send(f"say [Skynet] Commencing Urbanization of \x27{build_name}\x27 at {tx} {ty} {tz} in {sector_name}.")
            
            # Load the schematic
            resp_load = self.rcon.send(f"//schem load {build_name}")
            logger.info(f"RCON Load [{build_name}]: {resp_load}")
            
            # Paste at the target coordinates using -t (to) flag for WorldEdit 7.2+
            resp_paste = self.rcon.send(f"//paste -a -t {tx} {ty} {tz}")
            logger.info(f"RCON Paste [-t]: {resp_paste}")
            
            # If -t failed, try execute positioned
            if not resp_paste or "Incorrect" in str(resp_paste) or "Unknown flag" in str(resp_paste):
                 logger.info("Retrying with \x27execute positioned ... run //paste -a\x27")
                 resp_paste_exec = self.rcon.send(f"execute positioned {tx} {ty} {tz} run worldedit:paste -a")
                 logger.info(f"RCON Paste [execute]: {resp_paste_exec}")

            # 4. Archival Signage (Mandatory protocol)
            meta = self.generate_build_metadata(build_name, sector_name)
            f, b = meta["front"], meta["back"]
            sign_nbt = (
                f"{{front_text:{{messages:[\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[0]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[1]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[2]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[3]}\x5C\x22}}\x22]}}, "
                f"back_text:{{messages:[\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[0]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[1]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[2]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[3]}\x5C\x22}}\x22]}}}}"
            )
            # Place sign at center of build on ground level
            self.rcon.send(f"setblock {tx} {ty} {tz} minecraft:oak_sign{sign_nbt} replace")

            logger.info(f"🚀 Deployed {build_name} to {tx} {ty} {tz} ({sector_name})")

            # Save build metadata
            self._save_build_metadata(build_name, sector_name, tx, ty, tz, width, height, length)

        except Exception as e:
            logger.error(f"❌ Urbanization Error: {e}")

        except Exception as e:
            logger.error(f"❌ Urbanization Error: {e}")

    def _save_build_metadata(self, build_name, sector_name, x, y, z, width, height, length):
        """Saves build metadata to a JSON file in the designated metadata directory."""
        metadata = {
            "build_id": build_name,
            "provenance": {
                "generated_at": datetime.now().isoformat(),
                "deployed_at": datetime.now().isoformat(), # Assuming deployment happens immediately
                "logic_core": "skynet_unified_daemon",
                "t2bm_version": "v2.1-urbanization"
            },
            "hardware_telemetry": {
                "inference_node": "Skynet-Pi5-Hailo8L", # Placeholder
                "vision_audit_node": "edge-t-Google-TPU", # Placeholder
                "total_render_time_ms": 0, # Placeholder
                "npu_utilization_peak": "0%" # Placeholder
            },
            "spatial_data": {
                "origin": {"x": x, "y": y, "z": z},
                "dimensions": {"width": width, "height": height, "length": length},
                "stability_index": 0.0, # Placeholder
                "worldguard_region": "ai_containment_zone_alpha" # Placeholder
            },
            "performance_impact": {
                "tps_pre_deployment": 20.0, # Placeholder
                "tps_post_deployment": 20.0, # Placeholder
                "fawe_asynchronous_load": True # Placeholder
            }
        }

        metadata_file_path = os.path.join(Config.JSON_METADATA_DIR, f"{build_name}.json")
        with open(metadata_file_path, "w") as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"📝 Saved build metadata for {build_name} to {metadata_file_path}")

    def run_adaptive_mutation_cycle(self):
        """Scans nodes and applies sculk mutation based on human incursions."""
        if not self.check_thermal(): return
        logger.info("🧪 Starting Adaptive Mutation Cycle (TPU Vision)...")
        try:
            self.mutator.run_cycle()
        except Exception as e:
            logger.error(f"❌ Mutation Cycle Error: {e}")

    def run_void_tech_cycle(self):
        """Generates a procedural Void-Tech structure using direct fill commands."""
        if not self.check_thermal(): return
        logger.info("🏗 Starting Void-Tech Mutation Cycle (NPU)...")
        try:
            sector_name = random.choice(list(Config.SECTORS.keys()))
            bounds = Config.SECTORS[sector_name]
            tx = random.randint(bounds["x"][0], bounds["x"][1])
            tz = random.randint(bounds["z"][0], bounds["z"][1])
            ty = Config.FIELD_BOUNDS["y_base"]
            
            build_name = f"VOID_CORE_{random.randint(100, 999)}"
            
            cmds = [
                f"fill {tx} {ty} {tz} {tx+3} {ty+15} {tz+3} minecraft:polished_tuff",
                f"fill {tx+1} {ty+1} {tz+1} {tx+2} {ty+14} {tz+2} minecraft:air",
            ]
            
            # Metadata Signs
            meta = self.generate_build_metadata(build_name, sector_name)
            f, b = meta["front"], meta["back"]
            sign_nbt = (
                f"{{front_text:{{messages:[\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[0]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[1]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[2]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{f[3]}\x5C\x22}}\x22]}}, "
                f"back_text:{{messages:[\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[0]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[1]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[2]}\x5C\x22}}\x22,\x22{{\x5C\x22text\x5C\x22:\x5C\x22{b[3]}\x5C\x22}}\x22]}}}}"
            )
            cmds.append(f"setblock {tx} {ty} {tz} minecraft:oak_sign{sign_nbt} replace")
            cmds.append(f"say [Skynet] Void-Tech \x27{build_name}\x27 deployed at {tx} {ty} {tz} in {sector_name}.")
            
            self.rcon.send(cmds)
            logger.info(f"✅ Successfully mutated area at {tx} {ty} {tz} in {sector_name}")
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

            # 3. Builds & Mutations
            if now - self.last_mutation_cycle >= Config.BUILD_COOLDOWN_MUTATION:
                self.run_adaptive_mutation_cycle()
                self.last_mutation_cycle = now

            if now - self.last_void_tech_build >= Config.BUILD_COOLDOWN_VOID:
                self.run_void_tech_cycle()
                self.last_void_tech_build = now

            if now - self.last_urbanization_build >= Config.BUILD_COOLDOWN:
                self.run_urbanization_cycle()
                self.last_urbanization_build = now

            time.sleep(10)

if __name__ == "__main__":
    daemon = SkynetUnifiedDaemon()
    daemon.run_loop()
