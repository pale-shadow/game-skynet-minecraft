import json
import logging
import os

logger = logging.getLogger("rail_manager")

class RailManager:
    def __init__(self, registry_path="/home/skynet/config/rail_registry.json"):
        self.registry_path = registry_path
        self.switches = {}  # Searchable index: { "switch_id": {metadata_dict} }
        self.load_registry()

    def load_registry(self):
        """
        Loads the rail_registry.json and converts the 'switches' list into 
        a dictionary to prevent 'list object has no attribute get' errors.
        """
        if not os.path.exists(self.registry_path):
            logger.error(f"Registry file not found at {self.registry_path}")
            return

        try:
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
                
                # Extract the list of switches
                raw_list = data.get("switches", [])
                
                if not isinstance(raw_list, list):
                    logger.error("Registry format invalid: 'switches' must be a list.")
                    return

                # Convert list to dictionary keyed by 'id'
                self.switches = {item['id']: item for item in raw_list if 'id' in item}
                
                logger.info(f"RailManager synchronized. Indexed {len(self.switches)} switches from registry.")
        except Exception as e:
            logger.error(f"Failed to load or parse rail registry: {e}")

    def get_switch_metadata(self, switch_id):
        """
        Returns metadata for a specific switch ID. 
        Safe to call .get() now that self.switches is a dict.
        """
        return self.switches.get(switch_id)

    def execute_toggle(self, switch_id, state):
        """
        Resolves a logical switch ID to physical coordinates and 
        prepares for RCON dispatch.
        """
        switch = self.get_switch_metadata(switch_id)
        
        if not switch:
            logger.error(f"Switch ID {switch_id} not found in registry.")
            return False
            
        coords = switch.get("coords")
        node = switch.get("node")
        
        logger.info(f"Orchestration: Toggling {switch_id} ({coords}) on {node} to {state}")
        
        # Implementation of RCON bridge call goes here
        # return rcon_client.send_command(node, f"setblock {coords.replace(',', ' ')} ...")
        return True
