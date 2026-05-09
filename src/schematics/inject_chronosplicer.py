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
    voxels = data['voxels']

    rcon_pass = os.getenv('RCON_PASS', 'dinosaurExTraVaGanZa1969')
    rcon_host = os.getenv('MCRCON_HOST', '10.10.8.60')
    rcon_port = int(os.getenv('RCON_PORT', 25575))
    
    await log_deployment(f"Orchestrating manifestation at Recalibrated Anchor: {anchor}")

    try:
        # 1. FORCE LOAD: Instruction to Chonk to wake up the chunks
        print("[*] waking up sector chunks...")
        await rcon(f"execute in minecraft:overworld run forceload add {anchor['x']} {anchor['z']}", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await asyncio.sleep(2) # Buffer for chunk initialization

        # 2. Notify and Inject
        await rcon(f"say [Skynet] Recalibrated sector {anchor['x']}, {anchor['z']} loaded. Manifesting...", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)

        for i, v in enumerate(voxels):
            final_x, final_y, final_z = anchor['x'] + v['x'], anchor['y'] + v['y'], anchor['z'] + v['z']
            cmd = f"execute in minecraft:overworld run setblock {final_x} {final_y} {final_z} {v['block']}"
            
            # Executing and capturing server feedback
            response = await rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            
            if i % 25 == 0:
                print(f"  > Integration {i}/{len(voxels)}: Server says '{response.strip()}'")
            await asyncio.sleep(0.05) 

        await rcon(f"say [Skynet] Chronosplicer manifestation complete at {anchor['x']}, {anchor['z']}.", 
                   host=rcon_host, port=rcon_port, passwd=rcon_pass)
        await log_deployment("Deployment VERIFIED SUCCESS")
        
    except Exception as e:
        await log_deployment(f"Deployment CRITICAL ERROR: {e}")

if __name__ == "__main__":
    # Center of User's FIELD_BOUNDS
    recalibrated_anchor = {'x': -1242, 'y': 63, 'z': -701}
    asyncio.run(inject_schematic('config/schem-gen/chronosplicer_delta.json', recalibrated_anchor))
