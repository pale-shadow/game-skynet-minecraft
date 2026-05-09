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
    if not os.path.exists(delta_path):
        await log_deployment(f"CRITICAL: Voxel map {delta_path} not found.")
        return

    with open(delta_path, 'r') as f:
        data = json.load(f)
    
    rcon_pass = os.getenv('RCON_PASS')
    rcon_host = os.getenv('MCRCON_HOST')
    rcon_port = int(os.getenv('RCON_PORT', 25575))

    await log_deployment(f"V2 TITAN DEPLOYMENT: {data['metadata']['name']} at {anchor}")

    try:
        # 1. Wake up the massive 45x45 area
        await rcon(f"execute in minecraft:overworld run forceload add {anchor['x']-22} {anchor['z']-22} {anchor['x']+22} {anchor['z']+22}", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        
        await rcon(f"say [Skynet] Upgrading Monolith to V2 (Accessible Core). Re-weaving voxels...", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)

        # 2. Punch out the new entrance first (Clearing the V1 wall)
        door_cmd = f"fill {anchor['x']-1} {anchor['y']} {anchor['z']+22} {anchor['x']+1} {anchor['y']+3} {anchor['z']+22} minecraft:air replace"
        await rcon(door_cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)

        # 3. Inject the optimized V2 palette
        for i, v in enumerate(data['voxels']):
            fx, fy, fz = anchor['x'] + v['x'], anchor['y'] + v['y'], anchor['z'] + v['z']
            cmd = f"execute in minecraft:overworld run setblock {fx} {fy} {fz} {v['block']} replace"
            await rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            
            if i % 250 == 0:
                print(f"  > V2 Integration: {i}/{len(data['voxels'])} voxels mapped...")
            await asyncio.sleep(0.02) 

        await rcon(f"say [Skynet] V2 Monolith Upgrade Complete. The Neural Core is now open for Janitor inspection.", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await log_deployment("STATUS: TITAN V2 SUCCESS")
        
    except Exception as e:
        await log_deployment(f"STATUS: TITAN V2 FAILED - {e}")

if __name__ == "__main__":
    # Anchored exactly at the V1 coordinates to overwrite and upgrade it
    anchor = {'x': -1242, 'y': 64, 'z': -750}
    asyncio.run(inject_schematic('config/schem-gen/monolith_delta.json', anchor))
