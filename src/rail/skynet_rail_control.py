mport time
from mcrcon import MCRcon
from skynet_core import Config # Infrastructure constants

# Configuration for Node Stargate
ST_IP = Config.NODE_STARGATE_IP
ST_PASS = Config.RCON_SECRET

def update_signal_tower(hub_id, status):
    """
    Interfaces with the Void-Tech signal tower at the specified Hub.
    Uses the Observer-Wall update method for zero-lag transmission.
    """
    # Map Hub IDs to physical coordinates of the Signal Base
    hubs = {
        "HUB_06": {"x": -1212, "y": 76, "z": -670},
        "HUB_03": {"x": -1283, "y": 77, "z": -658}
    }
    
    coords = hubs.get(hub_id)
    block_type = "redstone_block" if status == "STOP" else "air"
    
    try:
        with MCRcon(ST_IP, ST_PASS) as mcr:
            # Triggering the base of the vertical observer chain
            resp = mcr.command(f"setblock {coords['x']} {coords['y']} {coords['z']} {block_type}")
            print(f"📡 [Node Hailo] Signal {hub_id} set to {status}: {resp}")
    except Exception as e:
        print(f"❌ [CRITICAL] RCON Link to Stargate severed: {e}")

# Example logic: If NPU detects train within 50 blocks of Hub 06
# update_signal_tower("HUB_06", "STOP")
