import os
import sys
from hailo_platform import VDevice, HailoRTException

def verify_hailo_npu():
    print(f"--- Hailo NPU Verification on {os.uname().nodename} ---")
    
    try:
        # VDevice() without arguments scans for the first available NPU (PCIe)
        with VDevice() as target:
            # Retrieve identification info from the physical chip
            ident = target.get_identification()
            
            print(f"[SUCCESS] Hailo NPU detected and initialized.")
            print(f"  - Architecture: {ident.architecture}")
            print(f"  - Device ID:    {ident.device_id}")
            print(f"  - FW Version:   {ident.fw_version}")
            
            # Check the current status
            print(f"[STATUS] Hardware is ready for inference.")
            
    except ImportError:
        print("[ERROR] 'hailo_platform' module not found.")
        print("        Fix: Ensure you've installed the HailoRT wheel in your venv.")
    except HailoRTException as e:
        print(f"[ERROR] HailoRT was unable to communicate with the NPU.")
        print(f"        Details: {e}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    verify_hailo_npu()
