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

    await log_deployment(f"MACRO DEPLOYMENT: {data['metadata']['name']} ({len(data['voxels'])} voxels)")

    try:
        # 1. Wake up the larger 15x15 sector
        await rcon(f"execute in minecraft:overworld run forceload add {anchor['x']} {anchor['z']} {anchor['x']+15} {anchor['z']+15}", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        
        await rcon(f"say [Skynet] Initiating Macro-Scale Construction: {data['metadata']['name']}...", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)

        for i, v in enumerate(data['voxels']):
            fx, fy, fz = anchor['x'] + v['x'], anchor['y'] + v['y'], anchor['z'] + v['z']
            cmd = f"execute in minecraft:overworld run setblock {fx} {fy} {fz} {v['block']}"
            await rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            
            if i % 100 == 0:
                print(f"  > Construction Progress: {i}/{len(data['voxels'])} voxels...")
            
            # Tighter sleep for large builds to prevent script timeouts while respecting TPS
            await asyncio.sleep(0.02) 

        await rcon(f"say [Skynet] construction complete. Siphon active at {anchor['x']}, {anchor['z']}.", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await log_deployment("STATUS: MACRO SUCCESS")
        
    except Exception as e:
        await log_deployment(f"STATUS: MACRO FAILED - {e}")

if __name__ == "__main__":
    anchor = {'x': -1180, 'y': 64, 'z': -640}
    asyncio.run(inject_schematic('config/schem-gen/stabilizer_delta.json', anchor))
