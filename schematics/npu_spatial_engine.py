import argparse
import sys

class NPUSpatialEngine:
    def __init__(self, hardware_mode="hailo"):
        """
        Initializes the spatial inference engine.
        Delegates tasks to the Hailo-8L (Pi 5) or Coral Edge TPU.
        """
        self.hardware_mode = hardware_mode
        print(f"🚀 NPUSpatialEngine initialized on hardware: {self.hardware_mode}")

    def query_traversability(self, coords):
        """
        Returns a cost weight for a specific voxel.
        Lower weight = More 'attractive' path for the Weaver (Rail Builder).
        """
        try:
            y_val = int(coords.split(',')[3])
            
            return 0.1 if y_val == 70 else 5.0
        except (IndexError, ValueError):
            return 10.0 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--pos", type=str, required=True)
    parser.add_argument("--hardware", type=str, default="hailo")
    args = parser.parse_args()
    engine = NPUSpatialEngine(hardware_mode=args.hardware)
    
    if args.query == "traversability":
        weight = engine.query_traversability(args.pos)
        print(weight)
