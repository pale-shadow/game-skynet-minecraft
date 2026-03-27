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
    """
    Sends a list of commands to the Minecraft server via RCON.
    Includes centralized logging for build deployment.
    """
    if not commands:
        return
        
    try:
        rcon.send(commands)
        # Attempt to extract coordinates and building name for more detailed logging if possible
        # This is a generic push, so we just log that a deployment happened.
        logging.info(f"🚀 Deployed AI-generated structure logic to chonk.")
    except Exception as e:
        logging.error(f"❌ Failed to push build to chonk: {e}")

def get_hailo_structure_logic(sector=None, metadata=None):
    """
    Simulates AI structure generation using the Hailo NPU.
    Returns a list of RCON commands.
    """
    x = random.randint(Config.FIELD_BOUNDS["min_x"], Config.FIELD_BOUNDS["max_x"])
    z = random.randint(Config.FIELD_BOUNDS["min_z"], Config.FIELD_BOUNDS["max_z"])
    y = Config.FIELD_BOUNDS["y_base"] 

    build_name = "Void-Tech Structure"
    if metadata and "front" in metadata:
        # Extract name from sign metadata if available
        first_line = metadata["front"][0]
        build_name = first_line.replace("&b&l", "").strip()

    cmds = [
        f"fill {x} {y} {z} {x+3} {y+15} {z+3} minecraft:polished_tuff",
        f"fill {x+1} {y+1} {z+1} {x+2} {y+14} {z+2} minecraft:air",
        f"say [Skynet] Void-Tech '{build_name}' deployed at {x} {y} {z} in {sector if sector else 'default zone'}."
    ]
    
    # If metadata/signs are provided, we should ideally add them to cmds here, 
    # but for now we follow the existing pattern in skynet_daemon.py
    
    return cmds

def get_node_logic(node="node_hailo", sector="Shroomville", metadata=None):
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
        logging.info(f"📡 {node} using prompt: {selected_prompt}")
        commands = [f"say §b[Skynet]§f Node {node} deploying {selected_prompt} to {sector}..."]

        if metadata:
            # Senior Admin Tip: Ensure indices 1, 3, and 4 exist to avoid IndexError!
            f, b = metadata['front'], metadata['back']
            sign_nbt = (
                f'{{front_text:{{messages:[\"{f}\",\"{f[3]}\",\"{f[4]}\",\"{f[5]}\"]}}, '
                f'back_text:{{messages:[\"{b}\",\"{b[3]}\",\"{b[4]}\",\"{b[5]}\"]}}}}'
            )
            commands.append(f"setblock ~ ~1 ~ minecraft:oak_sign{sign_nbt} replace")

        commands.append(f"say §d[Inference]§f Spatial Sync complete for {node}.")
        return commands

    except Exception as e:
        logging.error(f"❌ Failed to generate logic for {node}: {e}")
        return None
