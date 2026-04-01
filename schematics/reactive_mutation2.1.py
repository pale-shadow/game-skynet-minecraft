import os

from google import genai
from rcon.source import rcon

# Load from direnv / .envrc
API_KEY = os.environ.get("GEMINI_API_KEY")
RCON_PASS = os.environ.get("RCON_PASS")
RCON_PORT = int(os.environ.get("RCON_PORT", 25575))
CHONK_IP = os.environ.get("CHONK_IP", "127.0.0.1")

client = genai.Client(api_key=API_KEY)


def get_mutation_strategy(detection_data):
    """
    Asks Gemini to design a specific 'Infection' based on TPU detection.
    """
    prompt = f"""
    TPU detected human structures at {detection_data['coords']}. 
    Class: {detection_data['label']}. 
    Generate a V7.1 Void-Tech mutation strategy. 
    Focus on 'Aggressive Reclamation' using Sculk and Crying Obsidian.
    """

    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    return response.text


def apply_infection(coords, strategy_text):
    # Logic to parse Gemini's intent into RCON 'fill' commands
    print(f"[RECLAMATION] Applying Strategy: {strategy_text[:50]}...")
    with rcon(CHONK_IP, RCON_PASS, port=RCON_PORT) as server:
        # Example: Core infection block
        server.command(
            f"setblock {coords[0]} {coords[1]} {coords[2]} minecraft:sculk_sensor"
        )


# This would be triggered by your Edge TPU inference loop
if __name__ == "__main__":
    sample_detection = {"label": "HUMAN_BASE", "coords": [1720, 64, 710]}
    strategy = get_mutation_strategy(sample_detection)
    apply_infection(sample_detection["coords"], strategy)
