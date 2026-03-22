import os
import mcrcon
import time

def ai_stress_test():
    # Utilizing your .envrc variables
    with mcrcon.MCRcon(os.getenv("CHONK_IP"), os.getenv("RCON_PASS"), port=int(os.getenv("RCON_PORT"))) as mcr:
        # AI generates a 50-block pillar
        for i in range(50):
            # Using /execute to ensure we hit loaded chunks near a player
            mcr.command(f"execute at @a run setblock ~ ~{i} ~ minecraft:glass")
            time.sleep(0.01) # 10ms delay (100 commands/sec)
        mcr.command("say [Skynet] Stress test complete. NPU-accelerated structure deployed.")

if __name__ == "__main__":
    ai_stress_test()
