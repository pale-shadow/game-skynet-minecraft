import os
import mcrcon
import time

# Load parameters from environment variables
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

def send_to_chonk(command):
    try:
        # Validate that we actually have the required environment variables
        if not CHONK_IP or not RCON_PASS:
            return "Error: CHONK_IP or RCON_PASS environment variables not set."
            
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            response = mcr.command(command)
            return response
    except Exception as e:
        return f"Connection Error: {e}"

def build_ai_tower(x, y, z):
    """
    Simulates AI building logic translated to RCON commands.
    """
    commands = [
        f"fill {x} {y} {z} {x+2} {y+10} {z+2} stone_bricks",
        f"fill {x+1} {y+1} {z+1} {x+1} {y+9} {z+1} air", 
        f"setblock {x+1} {y} {z} oak_door",
        f"say [AI Architect] Tower deployed to coordinates {x} {y} {z}."
    ]
    
    for cmd in commands:
        print(f"Executing on Chonk: {cmd}")
        print(send_to_chonk(cmd))
        time.sleep(0.05) # Prevent RCON packet flood

if __name__ == "__main__":
    # Ensure variables are actually exported in your shell session
    print(f"Targeting {CHONK_IP}:{RCON_PORT}...")
    
    # Example: Build at specific coordinates (change these to suit your world)
    build_ai_tower(0, 70, 0)
