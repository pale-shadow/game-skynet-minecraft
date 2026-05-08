import json
import time
import os
from rcon.source import rcon

def inject_schematic(delta_path, anchor):
    if not os.path.exists(delta_path):
        print(f"[!] Error: {delta_path} not found.")
        return

    with open(delta_path, 'r') as f:
        data = json.load(f)
    
    voxels = data['voxels']
    print(f"[*] Prepared to inject {len(voxels)} voxels into Chonk via Stargate Proxy...")

    # Properly targeting your .envrc variables
    rcon_pass = os.getenv('RCON_PASS', 'dinosaurExTraVaGanZa1969')
    rcon_host = os.getenv('MCRCON_HOST', '10.10.8.60')
    rcon_port = int(os.getenv('RCON_PORT', 25575))
    
    try:
        for i, v in enumerate(voxels):
            final_x = anchor['x'] + v['x']
            final_y = anchor['y'] + v['y']
            final_z = anchor['z'] + v['z']
            
            cmd = f"setblock {final_x} {final_y} {final_z} {v['block']}"
            
            # Executing the one-shot rcon function
            rcon(cmd, host=rcon_host, port=rcon_port, passwd=rcon_pass)
            
            # Progress update to ensure we aren't hanging
            if i % 25 == 0:
                print(f"  > Progressive Manifestation: {i}/{len(voxels)} voxels...")
            
            # Maintain 20 TPS target stability (network overhead + sleep)
            time.sleep(0.05) 

        print("[+] Chronosplicer Singularity successfully manifested at the Abyssal Reef.")
    except Exception as e:
        print(f"[!] Injection Failed: {e}")

if __name__ == "__main__":
    anchor_point = {'x': 1950, 'y': 84, 'z': 750}
    inject_schematic('config/schem-gen/chronosplicer_delta.json', anchor_point)
