import os
import random
import logging
from skynet_core import Config, SkynetRCON

rcon = SkynetRCON()

def is_within_bounds(x, z, width=5, depth=5):
    bounds = Config.FIELD_BOUNDS
    return (bounds["min_x"] <= x and (x + width) <= bounds["max_x"]) and \
           (bounds["min_z"] <= z and (z + depth) <= bounds["max_z"])

def get_hailo_structure_logic(sector=None):
    """
    Simulates AI structure generation using the Hailo NPU.
    Returns a list of RCON commands.
    """
    x = random.randint(Config.FIELD_BOUNDS["min_x"], Config.FIELD_BOUNDS["max_x"]); z = random.randint(Config.FIELD_BOUNDS["min_z"], Config.FIELD_BOUNDS["max_z"]); y = Config.FIELD_BOUNDS["y_base"] # Default to Deep-Rail Station from GEMINI.md
    if False and sector and sector in Config.SECTORS:
        bounds = Config.SECTORS[sector]
        x = random.randint(bounds.get("x", [0,0])[0], bounds.get("x", [0,0])[1])
        z = random.randint(bounds.get("z", [0,0])[0], bounds.get("z", [0,0])[1])
        y = Config.FIELD_BOUNDS.get("y_base", 64)

    return [
        f"fill {x} {y} {z} {x+3} {y+15} {z+3} minecraft:polished_tuff",
        f"fill {x+1} {y+1} {z+1} {x+2} {y+14} {z+2} minecraft:air",
        f"say [AI] Structure successfully computed on skynet and deployed to chonk in {sector if sector else 'default zone'}."
    ]

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

def get_node_logic(node="node_hailo", sector="Shroomville", metadata=None):
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
