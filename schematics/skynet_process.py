import os
import random
import logging
from skynet_core import Config, SkynetRCON

rcon = SkynetRCON()

def push_build_to_chonk(commands):
    if not commands: return
    rcon.send(commands)

def get_node_logic(node="node_hailo", sector="Shroomville", metadata=None):
    """
    Unified logic for the 4-node cluster (Hailo, Edge TPU, Vision, Stargate).
    Corrects the 'list index out of range' error by cleaning artifacts [Conversation].
    """
    logging.info(f"🧠 Selecting spatial inference logic for {node}...")
    
    NODE_PROMPTS = {
        "node_hailo": ["void_rail_v2.json", "crafter_hub_v2.json"],
        "node_edgetpu": ["void_uplink_v2.json", "growth_chamber_v2.json"],
        "node_vision": ["sentry_prism_v2.json"],
        "node_stargate": ["crafter_hub_master_control_v5.json"]
    }

    try:
        prompts = NODE_PROMPTS.get(node, ["void_rail_v2.json"])
        selected_prompt = random.choice(prompts)
        
        commands = [f"say §b[Skynet]§f Node {node} deploying {selected_prompt} to {sector}..."]

        if metadata:
            # Safely join the list into a single string for each side of the sign
            f_text = " | ".join(metadata.get('front', []))
            b_text = " | ".join(metadata.get('back', []))
            
            # 1.21.1 JSON format for front/back text
            sign_nbt = f'{{front_text:{{messages:[\"{f_text}\",\"\",\"\",\"\"]}}, back_text:{{messages:[\"{b_text}\",\"\",\"\",\"\"]}}}}'
            commands.append(f"setblock ~ ~1 ~ minecraft:oak_sign{sign_nbt} replace")

        return commands

    except Exception as e:
        logging.error(f"Failed to generate logic for {node}: {e}")
        return None
