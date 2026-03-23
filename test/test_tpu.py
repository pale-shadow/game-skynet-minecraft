import tflite_runtime.interpreter as tflite
import os

def test_tpu_hardware():
    # Update this path if 'find' showed something different!
    LIB_PATH = '/usr/lib/aarch64-linux-gnu/libedgetpu.so.1'
    
    print(f"--- Attempting Manual Delegate Load ---")
    if not os.path.exists(LIB_PATH):
        print(f"❌ Critical Error: {LIB_PATH} not found on filesystem.")
        return

    try:
        # Load delegate using the ABSOLUTE path
        delegate = tflite.load_delegate(LIB_PATH)
        print("✔️ SUCCESS: Skynet Vision Cortex is LIVE.")
        print("The Edge TPU is ready for Neural Bridge v7.1 classification.")
    except Exception as e:
        print(f"❌ Failed to load delegate. \nDetails: {e}")

if __name__ == "__main__":
    test_tpu_hardware()
