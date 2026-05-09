import json
import asyncio
import os
import datetime
from rcon.source import rcon

async def log_deployment(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    os.makedirs("logs", exist_ok=True)
    with open("logs/deployment.log", "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

async def inject_schematic(delta_path, anchor):
    with open(delta_path, 'r') as f:
        data = json.load(f)
    
    rcon_pass = os.getenv('RCON_PASS')
    rcon_host = os.getenv('MCRCON_HOST')
    rcon_port = int(os.getenv('RCON_PORT', 25575))

    await log_deployment(f"EXTRATERRESTRIAL DEPLOYMENT: {data['metadata']['name']} at {anchor}")

    try:
        # 1. Wake up the massive 45x45 area
        await rcon(f"execute in minecraft:overworld run forceload add {anchor['x']-22} {anchor['z']-22} {anchor['x']+22} {anchor['z']+22}", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        
        await rcon(f"say [Skynet] WARNING: Unidentified Abyssal Voidcraft signature detected. Initiating materialization...", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)

        # 2. Multi-Pass Injection
        for i, v in enumerate(data['voxels']):
            fx, fy, fz = anchor['x'] + v['x'], anchor['y'] + v['y'], anchor['z'] + v['z']
            cmd = f"execute in minecraft:overworld run setblock {fx} {fy} {fz} {v['block']} replace"
            await rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            
            if i % 300 == 0:
                print(f"  > Materializing Sector: {i}/{len(data['voxels'])} voxels...")
            await asyncio.sleep(0.02) 

        await rcon(f"say [Skynet] Voidcraft hovering at {anchor['x']}, {anchor['z']}. Approach with caution.", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await log_deployment("STATUS: VOIDCRAFT SUCCESS")
        
    except Exception as e:
        await log_deployment(f"STATUS: VOIDCRAFT FAILED - {e}")

if __name__ == "__main__":
    # Base anchor at Y=64. The script naturally hovers the hull starting at Y+5.
    anchor = {'x': -1350, 'y': 64, 'z': -800}
    asyncio.run(inject_schematic('config/schem-gen/alien_craft_delta.json', anchor))
