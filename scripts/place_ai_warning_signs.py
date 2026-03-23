import os
import mcrcon
import time

# Configuration
CHONK_IP = os.getenv("CHONK_IP", "chonk.lab.bitsmasher.net")
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))

# Field Bounds (from npu_spatial_engine.py)
# Corners: (MinX, MinZ), (MinX, MaxZ), (MaxX, MinZ), (MaxX, MaxZ)
# Y=64 (One block above desert floor)
CORNERS = [
    (-1539, 64, -913), # NW
    (-1539, 64, -489), # NE
    (-945, 64, -913),  # SW
    (-945, 64, -489)   # SE
]

# NBT Data for 1.21.1 Oak Sign
# front_text must be used.
SIGN_NBT = '{front_text:{messages:[\'{"text":"[Skynet AI]","color":"dark_red","bold":true}\',\'{"text":"RECONSTRUCTION"}\',\'{"text":"IN PROGRESS"}\',\'{"text":"PROCEED WITH CAUTION"}\']}}'

def place_signs():
    if not RCON_PASS:
        print("❌ Error: RCON_PASS environment variable is not set.")
        return

    print(f"🔌 Connecting to {CHONK_IP}:{RCON_PORT}...")
    
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
            print("✅ Connected. Placing signs...")
            
            for x, y, z in CORNERS:
                # 1. Force load the chunk to ensure we can edit it
                print(f"   ⏳ Force-loading chunk at {x}, {z}...")
                resp_force = mcr.command(f"forceload add {x} {z}")
                print(f"      Response: {resp_force}")
                time.sleep(1.5) # Increased delay for server to catch up
                
                # 2. Place the Sign
                cmd_sign = f"setblock {x} {y} {z} minecraft:oak_sign{SIGN_NBT} replace"
                resp_sign = mcr.command(cmd_sign)
                
                # 3. Place a Torch (for visibility at night)
                cmd_torch = f"setblock {x} {y+1} {z} minecraft:torch replace"
                resp_torch = mcr.command(cmd_torch)
                
                print(f"      👉 Sign Result: {resp_sign}")
                
                # 4. Cleanup: Remove force load
                mcr.command(f"forceload remove {x} {z}")
                print(f"      ✅ Chunk unloaded.")

    except Exception as e:
        print(f"❌ RCON Error: {e}")

if __name__ == "__main__":
    place_signs()
