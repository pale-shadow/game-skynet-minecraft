import os
import sys


def check_models():
    print("--- Skynet Neural Core Health Check ---")

    models = {
        "Spatial Inference (Hailo-8L)": "yolov8s_h8l.hef",
        "Visual Cortex (Edge TPU)": "mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite",
    }

    all_ok = True
    for name, filename in models.items():
        path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(path):
            size = os.path.getsize(path) / (1024 * 1024)
            status = "✅ FOUND"
            if os.path.islink(path):
                status += " (Symlink)"
            print(f"{status} [{name}]: {filename} ({size:.2f} MB)")
        else:
            print(f"❌ MISSING [{name}]: {filename}")
            all_ok = False

    if all_ok:
        print("\n🧠 Neural Core status: OPTIMAL")
    else:
        print("\n⚠️ Neural Core status: DEGRADED")
        sys.exit(1)


if __name__ == "__main__":
    check_models()
