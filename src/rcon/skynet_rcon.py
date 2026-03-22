import mcrcon
import time

CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

def send_to_chonk(command):
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            response = mcr.command(command)
            return response
    except Exception as e:
        return f"Connection Error: {e}"

# Example: AI Architect building a structure based on Hailo output
def build_ai_tower(x, y, z):
    # We use a batch of commands to reduce RCON overhead
    commands = [
        f"fill {x} {y} {z} {x+2} {y+10} {z+2} stone_bricks",
        f"fill {x+1} {y+1} {z+1} {x+1} {y+9} {z+1} air", # Hollow it out
        f"setblock {x+1} {y} {z} oak_door"
    ]
    
    for cmd in commands:
        print(f"Executing on Chonk: {cmd}")
        print(send_to_chonk(cmd))
        time.sleep(0.05) # Small delay to prevent RCON packet flood
