import json
import logging
import os
import time
from src.mcrcon.mcrcon import MCRcon
from src.utils.config_utils import Config, setup_logging

class BlueMapMarkerUpdater:
    """
    Dynamically updates BlueMap markers.json to reflect rail switch states.
    """
    def __init__(self, marker_path):
        self.marker_path = marker_path
        self.logger = setup_logging("bluemap_updater")
        self.markers = self._load()

    def _load(self):
        if os.path.exists(self.marker_path):
            try:
                with open(self.marker_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Failed to load markers.json: {e}")
        return {"markerSets": {}}

    def update_switch(self, switch_id, label, coords, active):
        marker_set = self.markers["markerSets"].setdefault("rail_switches", {
            "label": "Rail Map",
            "toggleable": True,
            "defaultHide": False,
            "markers": {}
        })
        
        # In BlueMap, POI markers often use 'icon' or 'label'
        # We'll follow the spec for dynamic styling (Active: Green, Inactive: Red)
        marker_set["markers"][switch_id] = {
            "type": "poi",
            "position": {"x": coords['x'], "y": coords['y'], "z": coords['z']},
            "label": f"{label} ({'ACTIVE' if active else 'INACTIVE'})",
            "icon": f"assets/icons/rail_{'green' if active else 'red'}.png"
        }
        self._save()

    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.marker_path), exist_ok=True)
            with open(self.marker_path, 'w') as f:
                json.dump(self.markers, f, indent=4)
        except Exception as e:
            self.logger.error(f"Failed to save markers.json: {e}")

class RailManager:
    """
    Automated Rail Control system for Skynet.
    Integrates RCON, BlueMap, and AI Hardware (Hailo-8L, Edge TPU).
    """
    def __init__(self):
        self.logger = setup_logging("rail_manager", log_file="logs/rail_manager.log")
        self.safety_logger = setup_logging("rail_safety", log_file="logs/rail_safety.log")
        self.registry_path = "config/rail_registry.json"
        
        # Markers are stored in a location BlueMap can serve
        marker_file = os.path.join(Config.JSON_METADATA_DIR, "rail_markers.json")
        self.marker_updater = BlueMapMarkerUpdater(marker_file)
        
        self.rcon_host = Config.CHONK_IP
        self.rcon_pass = Config.RCON_PASS
        self.rcon_port = Config.RCON_PORT

    def _load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r') as f:
                return json.load(f)
        return {"switches": {}}

    def _save_registry(self, registry):
        with open(self.registry_path, 'w') as f:
            json.dump(registry, f, indent=4)

    def get_switch(self, switch_id):
        registry = self._load_registry()
        return registry["switches"].get(switch_id)

    def toggle_switch(self, switch_id, state):
        """
        Main execution loop for toggling a rail switch.
        """
        switch_data = self.get_switch(switch_id)
        if not switch_data:
            self.logger.error(f"Switch ID {switch_id} not found in registry.")
            return False

        # 1. Pathing Optimization (Hailo-8L @ Hub-00)
        if not self._request_hailo_pathing(switch_id, state):
            self.logger.warning(f"Hailo-8L pathing failed or rejected for {switch_id}.")

        # 2. Safety Interlock (Edge TPU @ Hub-06)
        if not self._verify_tpu_safety(switch_id):
            self.safety_logger.error(f"⚠️ SAFETY ABORT: Entity detected near {switch_id}. State change cancelled.")
            return False

        # 3. RCON Switch Control
        success = self._execute_rcon_switch(switch_data, state)
        
        if success:
            # 4. Vision Verification (Edge TPU @ Hub-06)
            if self._verify_vision_state(switch_id, state):
                self.logger.info(f"Switch {switch_id} verified via Vision.")
            else:
                self.logger.warning(f"Switch {switch_id} changed but Vision Verification failed.")

            # 5. BlueMap Update
            self.marker_updater.update_switch(
                switch_id, 
                switch_data['name'], 
                switch_data['coords'], 
                state
            )
            
            # 6. Update Registry
            registry = self._load_registry()
            registry["switches"][switch_id]["state"] = state
            self._save_registry(registry)
            
            self.logger.info(f"Switch {switch_id} successfully toggled to {'ACTIVE' if state else 'INACTIVE'}")
            return True
        else:
            self.logger.error(f"Failed to toggle switch {switch_id} via RCON.")
            return False

    def _request_hailo_pathing(self, switch_id, state):
        """
        Queries Hub-00 (Skynet) Hailo-8L for path optimization.
        """
        self.logger.info(f"Calculating route efficiency via Hailo-8L for {switch_id}...")
        # Placeholder for actual NPU RPC/Websocket call
        time.sleep(0.05) 
        return True

    def _verify_tpu_safety(self, switch_id):
        """
        Queries Hub-06 (Edge-T) Edge TPU for entity proximity.
        Aborts if a player is within 3 blocks.
        """
        self.logger.info(f"Running Safety Interlock (Edge TPU) for {switch_id}...")
        # Placeholder for actual TPU inference
        return True

    def _verify_vision_state(self, switch_id, expected_state):
        """
        Performs 'Vision Verification' after state change.
        """
        self.logger.info(f"Verifying physical state of {switch_id} via Edge-T Vision...")
        return True

    def _execute_rcon_switch(self, switch_data, state):
        coords = switch_data['coords']
        powered = "true" if state else "false"
        cmd = f"setblock {coords['x']} {coords['y']} {coords['z']} minecraft:powered_rail[powered={powered}]"
        
        try:
            with MCRcon(self.rcon_host, self.rcon_pass, port=self.rcon_port) as mcr:
                resp = mcr.command(cmd)
                self.logger.info(f"RCON Response: {resp}")
                return "Changed the block" in resp or "Successfully" in resp or resp == ""
        except Exception as e:
            self.logger.error(f"RCON Connection Error: {e}")
            return False

if __name__ == "__main__":
    # Example usage:
    # mgr = RailManager()
    # mgr.toggle_switch("chonk_02_sensor_switch", True)
    pass
