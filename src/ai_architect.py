import os
import mcrcon
import time
from hailo_platform import VDevice, HEF, ConfigureParams

# Settings from .envrc
CHONK_IP = os.getenv("CHONK_IP")
RCON_PASS = os.getenv("RCON_PASS")

def build_from_vision(label):
    """Translates an AI label into a Chonk world edit."""
    try:
        with mcrcon.MCRcon(CHONK_IP, RCON_PASS) as mcr:
            # Simple mapping: Person = Gold Monolith
            if label == "person":
                mcr.command("execute at @a run fill ~1 ~ ~1 ~1 ~5 ~1 gold_block")
                mcr.command("say [Skynet] AI Architect: Biological entity detected. Constructing gold monument.")
            print(f"✅ AI Action Sent: {label}")
    except Exception as e:
        print(f"❌ RCON Error: {e}")

def run_architect():
    # 1. Load the local model we just copied
    MODEL_PATH = "models/yolov8s.hef"
    hef = HEF(MODEL_PATH)
    
    with VDevice() as target:
        network_group = target.configure(ConfigureParams.create_from_hef(hef))[0]
        
        with network_group.activate():
            print("🤖 Skynet Brain is live. Monitoring PCIe bus for vision data...")
            
            # This is where you feed your camera frames. 
            # For the first test, let's trigger a 'person' detection build.
            build_from_vision("person")

if __name__ == "__main__":
    run_architect()
