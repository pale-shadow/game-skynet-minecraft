import os

import tflite_runtime.interpreter as tflite
from src.utils.config_utils import setup_logging

logger = setup_logging("test_tpu")


def test_tpu_hardware():
    # Update this path if 'find' showed something different!
    LIB_PATH = "/usr/lib/aarch64-linux-gnu/libedgetpu.so.1"

    logger.info("--- Attempting Manual Delegate Load ---")
    if not os.path.exists(LIB_PATH):
        logger.error(f"❌ Critical Error: {LIB_PATH} not found on filesystem.")
        return

    try:
        # Load delegate using the ABSOLUTE path
        delegate = tflite.load_delegate(LIB_PATH)
        logger.info("✔️ SUCCESS: Skynet Vision Cortex is LIVE.")
        logger.info("The Edge TPU is ready for Neural Bridge v7.1 classification.")
    except Exception as e:
        logger.error(f"❌ Failed to load delegate. \nDetails: {e}")


if __name__ == "__main__":
    test_tpu_hardware()
