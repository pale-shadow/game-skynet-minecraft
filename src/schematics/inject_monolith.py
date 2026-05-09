import json
import asyncio
import os
import datetime
from rcon.source import rcon

async def log_deployment(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open("logs/deployment.log", "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

async def inject_schematic(delta_path, anchor):
    with open(delta_path, 'r') as f:
        data = json.load(f)
    
    rcon_pass = os.getenv('RCON_PASS')
    rcon_host = os.getenv('MCRCON_HOST')
    rcon_port = int(os.getenv('RCON_PORT', 25575))

    await log_deployment(f"TITAN DEPLOYMENT: {data['metadata']['name']} at {anchor}")

    try:
        # Wake up a massive 45x45 area
        await rcon(f"execute in minecraft:overworld run forceload add {anchor['x']-22} {anchor['z']-22} {anchor['x']+22} {anchor['z']+22}", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        
        await rcon(f"say [Skynet] WARNING: Manifesting Titan-Class Monolith. Expect localized temporal lag...", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)

        for i, v in enumerate(data['voxels']):
            fx, fy, fz = anchor['x'] + v['x'], anchor['y'] + v['y'], anchor['z'] + v['z']
            cmd = f"execute in minecraft:overworld run setblock {fx} {fy} {fz} {v['block']}"
            await rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            
            if i % 250 == 0:
                print(f"  > Titan Integration: {i}/{len(data['voxels'])} voxels...")
            await asyncio.sleep(0.02) 

        await rcon(f"say [Skynet] Titan Manifestation Complete. The Monolith is online.", host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await log_deployment("STATUS: TITAN SUCCESS")
        
    except Exception as e:
        await log_deployment(f"STATUS: TITAN FAILED - {e}")

if __name__ == "__main__":
    # Anchored at Y=64 to ensure it stands on the surface
    anchor = {'x': -1242, 'y': 64, 'z': -750}
    asyncio.run(inject_schematic('config/schem-gen/monolith_delta.json', anchor))
