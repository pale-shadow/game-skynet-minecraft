#!/usr/bin/env python3
import json
import requests
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common, classify
from PIL import Image

# Hub 06 Config
STARGATE_HOST = "http://stargate.local:8080/api/t2bm/prompt"
MODEL_PATH = "models/biome_classifier_edgetpu.tflite"
LABELS_PATH = "models/biome_labels.txt"

def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

def generate_t2bm_constraint(image_path):
    """
    Analyzes visual data using the Edge TPU and converts classifications
    into a text-based environmental constraint for the T2BM LLM.
    """
    # Initialize Edge TPU
    interpreter = make_interpreter(MODEL_PATH)
    interpreter.allocate_tensors()
    labels = load_labels(LABELS_PATH)

    # Process simulated visual telemetry from the Mono-Eye Sensor
    size = common.input_size(interpreter)
    image = Image.open(image_path).convert('RGB').resize(size, Image.LANCZOS)
    common.set_input(interpreter, image)

    # Execute hardware inference
    interpreter.invoke()
    classes = classify.get_classes(interpreter, top_k=2, score_threshold=0.6)

    # Translate classification into a descriptive T2BM prompt
    if not classes:
        return "Design a standard building suited for a flat, unconstrained environment."

    primary_biome = labels.get(classes.id, "generic")
    environmental_prompt = f"Design a building optimized for a {primary_biome} environment. "
    
    if len(classes) > 1:
        secondary_feature = labels.get(classes[2].id, "mixed terrain")
        environmental_prompt += f"Incorporate architectural elements suitable for {secondary_feature}. "

    environmental_prompt += "Ensure the foundation accommodates the observed terrain elevation."
    return environmental_prompt

def transmit_to_stargate(prompt, coords):
    """
    Sends the refined T2BM prompt to the Stargate orchestrator.
    """
    payload = {
        "hardware_accelerator": "edge_tpu",
        "hub": "06_mono_eye",
        "coordinates": coords,
        "t2bm_environmental_prompt": prompt,
        "directive": "refine_t2bm_generation"
    }
    
    try:
        response = requests.post(STARGATE_HOST, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"SUCCESS: Transmitted visual constraints to Stargate -> '{prompt}'")
        else:
            print(f"ERROR: Stargate rejected payload. HTTP {response.status_code}")
    except requests.ConnectionError:
        print("FATAL: Connection to Stargate host lost.")

if __name__ == "__main__":
    # Simulated execution at Hub 06 (-1212, 76, -670)
    target_image = "chonk_telemetry/current_view_1212_670.jpg"
    target_coords = {"x": -1212, "y": 76, "z": -670}
    
    print("STATUS: Analyzing visual telemetry with Google Coral Edge TPU...")
    constraint_prompt = generate_t2bm_constraint(target_image)
    transmit_to_stargate(constraint_prompt, target_coords)
