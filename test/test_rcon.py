import os
from mcrcon import MCRcon

CHONK_IP = "10.10.8.60"
RCON_PASS = os.getenv("RCON_PASS")
RCON_PORT = 25575

print(f"Connecting to {CHONK_IP}:{RCON_PORT} with pass: {RCON_PASS}")
try:
    with MCRcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as mcr:
        resp = mcr.command("list")
        print(f"Success! Response: {resp}")
except Exception as e:
    print(f"Failed: {e}")
