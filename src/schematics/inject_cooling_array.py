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

    await log_deployment(f"DEPLOYMENT INITIATED: {data['metadata']['name']} at {anchor}")

    try:
        # Sector Wake-up
        await rcon(f"execute in minecraft:overworld run forceload add {anchor['x']} {anchor['z']}", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        
        # User Notification
        await rcon(f"say [Skynet] Vertex AI greebling layer received. Manifesting Cooling Array...", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)

        for v in data['voxels']:
            fx, fy, fz = anchor['x'] + v['x'], anchor['y'] + v['y'], anchor['z'] + v['z']
            cmd = f"execute in minecraft:overworld run setblock {fx} {fy} {fz} {v['block']}"
            await rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            await asyncio.sleep(0.05) 

        await rcon(f"say [Skynet] Build complete. Cooling Array online at {anchor['x']}, {anchor['z']}.", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await log_deployment("STATUS: VERIFIED SUCCESS")
        
    except Exception as e:
        await log_deployment(f"STATUS: FAILED - {e}")

if __name__ == "__main__":
    # Standard Surface Level Y=64
    anchor = {'x': -1200, 'y': 64, 'z': -660}
    asyncio.run(inject_schematic('config/schem-gen/cooling_array_delta.json', anchor))
