import os
import random
import logging
from skynet_core import Config, SkynetRCON

rcon = SkynetRCON()

def is_within_bounds(x, z, width=5, depth=5):
    bounds = Config.FIELD_BOUNDS
    return (bounds["min_x"] <= x and (x + width) <= bounds["max_x"]) and \
           (bounds["min_z"] <= z and (z + depth) <= bounds["max_z"])

def push_build_to_chonk(commands):
    if not commands: return
    rcon.send(commands)

def get_node_logic(node="node_hailo", sector="Shroomville", metadata=None):
    """
    Unified logic for the 4-node AI cluster.
    Delegates builds based on hardware specialty [378, 381, Conversation].
    """
    logging.info(f"🧠 Selecting spatial inference logic for {node}...")
    
    NODE_PROMPTS = {
        "node_hailo": ["void_rail_v2.json", "crafter_hub_v2.json"],     # Industry
        "node_edgetpu": ["void_uplink_v2.json", "growth_chamber_v2.json"], # Organic
        "node_vision": ["sentry_prism_v2.json"],                          # Security
        "node_stargate": ["crafter_hub_master_control_v5.json"]          # High-Density [2]
    }

    try:
        prompts = NODE_PROMPTS.get(node, ["void_rail_v2.json"])
        selected_prompt = random.choice(prompts)
        logging.info(f"📡 {node} using prompt: {selected_prompt}")

        # 1. Base Commands
        commands = [f"say §b[Skynet]§f Node {node} deploying {selected_prompt} to {sector}..."]

        # 2. Add Build-Specific Commands (Placeholder for actual schematic logic)
        # In production, this would call your decoration.py engine
        commands.append(f"say §d[Inference]§f Spatial Sync complete for {node}.")

        # 3. Corrected Metadata Signage (v2) [423, Conversation]
        if metadata:
            f, b = metadata['front'], metadata['back']
            # Accessing list indices safely
            sign_nbt = (
                f'{{front_text:{{messages:[\"{f}\",\"{f[3]}\",\"{f[1]}\",\"{f[4]}\"]}}, '
                f'back_text:{{messages:[\"{b}\",\"{b[3]}\",\"{b[1]}\",\"{b[4]}\"]}}}}'
            )
            # Place sign at center of build origin
            commands.append(f"setblock ~ ~1 ~ minecraft:oak_sign{sign_nbt} replace")

        return commands

    except Exception as e:
        logging.error(f"Failed to generate logic for {node}: {e}")
        return None
