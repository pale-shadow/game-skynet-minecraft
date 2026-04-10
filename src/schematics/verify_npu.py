import os

from hailo_platform import Device, VDevice


def verify_hailo_hardware():
    print(f"--- Hailo NPU Verification: {os.uname().nodename} ---")

    try:
        # 1. Scan for physical devices on the PCIe bus
        devices = Device.scan()
        if not devices:
            print("❌ No physical Hailo devices found. Check PCIe connection.")
            return

        print(f"✅ Physical Device Found: {devices[0]}")

        # 2. Try to initialize a Virtual Device (VDevice)
        # This confirms the driver can actually open the device for math
        with VDevice() as target:
            print("✅ VDevice initialized. NPU is ready for inference.")

    except Exception as e:
        print(f"❌ Verification Failed: {e}")


if __name__ == "__main__":
    verify_hailo_hardware()
