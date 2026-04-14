import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image


def run_skynet_vision(image_path):
    # Path to your TPU hardware library
    LIB_PATH = "/usr/lib/aarch64-linux-gnu/libedgetpu.so.1"
    MODEL_PATH = "../models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite"

    # 1. Initialize the TPU Interpreter
    interpreter = tflite.Interpreter(
        model_path=MODEL_PATH, experimental_delegates=[tflite.load_delegate(LIB_PATH)]
    )
    interpreter.allocate_tensors()

    # 2. Prepare the Image (Simulation of BlueMap tile or Screenshot)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Load and resize image to 224x224 (required by MobileNetV2)
    img = Image.open(image_path).convert("RGB").resize((224, 224))
    input_data = np.expand_dims(img, axis=0)

    # 3. RUN INFERENCE ON THE TPU
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()

    # 4. Extract Results
    results = interpreter.get_tensor(output_details[0]["index"])
    top_result = np.argmax(results)

    print(f"✔️ Inference Complete. TPU Result Index: {top_result}")
    return top_result


if __name__ == "__main__":
    # In a real scenario, this would be a real-time feed from the server
    print("Inference Engine Standby...")
