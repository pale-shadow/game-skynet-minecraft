import os
import mcrcon
import time

CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

MIN_X, MAX_X = -1539, -945
MIN_Z, MAX_Z = -913, -489
Y = 64

CORNERS = [
    (MIN_X, Y, MIN_Z),
    (MIN_X, Y, MAX_Z),
    (MAX_X, Y, MIN_Z),
    (MAX_X, Y, MAX_Z)
]

sign_nbt = '{front_text:{messages:[\'{"text":"[Skynet AI]","color":"dark_red","bold":true}\',\'{"text":"RECONSTRUCTION"}\',\'{"text":"IN PROGRESS"}\',\'{"text":"PROCEED WITH CAUTION"}\']}}'

def place_signs_with_force():
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            for x, y, z in CORNERS:
                # 1. Force load the chunk
                mcr.command(f"forceload add {x} {z}")
                print(f"Force-loading chunk at {x}, {z}")
                time.sleep(1) # Give it a second to load
                
                # 2. Place sign and torch
                mcr.command(f"setblock {x} {y} {z} minecraft:oak_sign{sign_nbt} replace")
                mcr.command(f"setblock {x} {y+1} {z} minecraft:torch replace")
                print(f"Placed sign at {x}, {y}, {z}")
                
                # 3. Remove force load
                mcr.command(f"forceload remove {x} {z}")
                print(f"Removed force-loading for {x}, {z}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    place_signs_with_force()
