import argparse
import sys

def query_traversability(coords, hardware_mode):
    """
    Returns a cost weight for a specific voxel.
    Lower weight = More 'attractive' path for the Weaver.
    """
    # Logic to switch between accelerators
    if hardware_mode == "hailo":
        # Access the Hailo-8L (Pi 5)
        # weight = hailo_inference(coords)
        pass
    elif hardware_mode == "coral":
        # Access the USB TPU or Tinker Edge-T
        # weight = coral_inference(coords)
        pass
        
    # Return a mock value for now based on 'height' (Y-coord)
    # We prefer paths at Y=70 (Mid-air conduit height)
    y_val = int(coords.split(',')[1])
    return 0.1 if y_val == 70 else 5.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str)
    parser.add_argument("--pos", type=str)
    parser.add_argument("--hardware", type=str, default="hailo")
    args = parser.parse_args()

    if args.query == "traversability":
        weight = query_traversability(args.pos, args.hardware)
        print(weight)
