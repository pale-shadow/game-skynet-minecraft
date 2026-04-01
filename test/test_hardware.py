import os

import pytest


@pytest.mark.hardware
def test_hailo_hardware():
    """Verify Hailo-8L NPU Presence."""
    try:
        from hailo_platform import Device

        devices = Device.scan()
        assert len(devices) > 0, "No physical Hailo devices found."
    except ImportError:
        pytest.skip("hailo_platform not installed")
    except Exception as e:
        pytest.fail(f"Hailo check failed: {e}")


@pytest.mark.hardware
def test_tpu_hardware():
    """Verify Edge TPU Presence."""
    LIB_PATH = "/usr/lib/aarch64-linux-gnu/libedgetpu.so.1"

    if not os.path.exists(LIB_PATH):
        pytest.skip(f"Edge TPU library {LIB_PATH} not found.")

    try:
        import tflite_runtime.interpreter as tflite

        delegate = tflite.load_delegate(LIB_PATH)
        assert delegate is not None
    except ImportError:
        pytest.skip("tflite_runtime not installed")
    except Exception as e:
        pytest.fail(f"TPU check failed: {e}")
