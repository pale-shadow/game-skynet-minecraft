#!/usr/bin/env python3
import json
from flask import Flask, jsonify, request
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common, classify
from PIL import Image

app = Flask(__name__)

# Model configurations
MODEL_PATH = "models/biome_classifier_edgetpu.tflite"
LABELS_PATH = "models/biome_labels.txt"

def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

def execute_vision_pass(image_path):
    try:
        interpreter = make_interpreter(MODEL_PATH)
        interpreter.allocate_tensors()
        labels = load_labels(LABELS_PATH)

        size = common.input_size(interpreter)
        image = Image.open(image_path).convert('RGB').resize(size, Image.LANCZOS)
        common.set_input(interpreter, image)

        interpreter.invoke()
        classes = classify.get_classes(interpreter, top_k=2, score_threshold=0.6)

        if not classes:
            return "Design a standard building suited for a flat, unconstrained environment."

        primary_biome = labels.get(classes.id, "generic")
        prompt = f"Design a building optimized for a {primary_biome} environment. "
        
        if len(classes) > 1:
            secondary_feature = labels.get(classes[1].id, "mixed terrain")
            prompt += f"Incorporate architectural elements suitable for {secondary_feature}. "

        return prompt + "Ensure the foundation accommodates the observed terrain elevation."
    except Exception as e:
        return f"ERROR: TPU Hardware failure - {str(e)}"

@app.route('/api/vision/infer', methods=['POST'])
def handle_inference():
    # In a live environment, the path might be passed in the request payload
    data = request.get_json() or {}
    target_image = data.get("image_path", "chonk_telemetry/current_view_1212_670.jpg")
    
    constraint_prompt = execute_vision_pass(target_image)
    
    if constraint_prompt.startswith("ERROR"):
        return jsonify({"status": "failed", "error": constraint_prompt}), 500
        
    return jsonify({
        "status": "success",
        "hardware": "edge_tpu",
        "hub": "06_mono_eye",
        "t2bm_environmental_prompt": constraint_prompt
    }), 200

if __name__ == "__main__":
    # Bind to 0.0.0.0 to allow Stargate to connect over the local network
    app.run(host="0.0.0.0", port=5000)
