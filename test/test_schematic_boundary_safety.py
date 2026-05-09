import json
import sys

# Official Skynet AI Testing Field Boundaries 
BOUNDS = {
    "x": (-1539, -945),
    "z": (-1539, -945),
    "y_foundation": 63
}

def validate_anchor(anchor):
    x_in = BOUNDS["x"][0] <= anchor['x'] <= BOUNDS["x"][1]
    z_in = BOUNDS["z"][0] <= anchor['z'] <= BOUNDS["z"][1]
    
    if not (x_in and z_in):
        print(f"[!] SAFETY VIOLATION: Anchor {anchor} is outside the AI Testing Field.")
        print(f"    Allowed X: {BOUNDS['x']}, Allowed Z: {BOUNDS['z']}")
        return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    
    # Using a sample anchor for validation
    sample_anchor = {'x': -1200, 'y': 63, 'z': -700} # Suggested Secure Anchor 
    if validate_anchor(sample_anchor):
        print(f"[√] Anchor {sample_anchor} passed boundary safety.")
