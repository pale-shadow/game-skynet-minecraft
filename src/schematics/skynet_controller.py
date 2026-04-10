import json
import logging
import os
import random
import time
import requests
from config_utils import Config, setup_logging
from skynet_unified import SkynetUnifiedDaemon

logger = setup_logging("skynet_controller")


class SkynetController(SkynetUnifiedDaemon):
    """
    The Master Controller for Skynet, running on Stargate host.
    Delegates inference to remote agents.
    """

    def __init__(self):
        super().__init__()
        self.agent_hosts = Config.AGENT_HOSTS
        logger.info(f"📡 Controller initialized with agents: {self.agent_hosts}")

    def run_void_tech_cycle(self):
        """Delegates Void-Tech logic to a remote NPU agent."""
        logger.info("🏗 Delegating Void-Tech Mutation to remote agent...")

        target_agent = random.choice(self.agent_hosts)
        agent_url = f"http://{target_agent}:5000/infer"

        try:
            payload = {"node": "void_tech", "sector": "AI Containment Area"}
            resp = requests.post(agent_url, json=payload, timeout=10)

            if resp.status_code == 200:
                cmds = resp.json().get("commands", [])
                if cmds:
                    self.rcon.send(cmds)
                    logger.info(f"✅ Remote mutation via {target_agent} complete.")
                else:
                    logger.warning(f"⚠️ No commands returned from agent {target_agent}")
            else:
                logger.error(
                    f"❌ Agent {target_agent} failed with status {resp.status_code}"
                )

        except Exception as e:
            logger.error(f"❌ Failed to reach agent {target_agent}: {e}")

    def run_node_delegation(self):
        """Standard node inference delegation."""
        target_agent = random.choice(self.agent_hosts)
        agent_url = f"http://{target_agent}:5000/infer"
        node_type = "node_hailo" if target_agent == "10.10.16.10" else "node_edgetpu"

        logger.info(
            f"🧠 Requesting inference from {target_agent} (Type: {node_type})..."
        )

        try:
            payload = {"node": node_type, "sector": "Shroomville"}
            resp = requests.post(agent_url, json=payload, timeout=10)

            if resp.status_code == 200:
                cmds = resp.json().get("commands", [])
                if cmds:
                    self.rcon.send(cmds)
                    logger.info(f"✅ Inferred logic from {target_agent} deployed.")
            else:
                logger.error(f"❌ Agent {target_agent} inference failed.")
        except Exception as e:
            logger.error(f"❌ Agent {target_agent} error: {e}")

    def run_loop(self):
        logger.info("🚀 Skynet Master Controller: ACTIVE")
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

            # 3. Urbanization Cycle (Local .schem generation is fine on Stargate)
            if now - self.last_urbanization_build >= Config.BUILD_COOLDOWN:
                self.run_urbanization_cycle()
                self.last_urbanization_build = now

            # 4. Void-Tech Delegation (Remote)
            if now - self.last_void_tech_build >= Config.BUILD_COOLDOWN:
                self.run_void_tech_cycle()
                self.last_void_tech_build = now

            time.sleep(10)


if __name__ == "__main__":
    controller = SkynetController()
    controller.run_loop()
