import glob
import json
import os


def check_overlaps(schem_files_dir, proposed_build=None):
    json_files = glob.glob(os.path.join(schem_files_dir, "*.json"))
    builds = []

    if proposed_build:
        builds.append(proposed_build)

    for file_path in json_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            build_id = data.get("build_id", os.path.basename(file_path))
            spatial = data.get("spatial_data", {})
            origin = spatial.get("origin", {})
            dims = spatial.get("dimensions", {})

            x = origin.get("x", 0)
            y = origin.get("y", 0)
            z = origin.get("z", 0)
            w = dims.get("width", 0)
            h = dims.get("height", 0)
            l = dims.get("length", 0)

            # Ignore builds with 0 dimensions or origins (likely unplaced)
            if w == 0 or h == 0 or l == 0:
                continue

            builds.append(
                {
                    "id": build_id,
                    "x1": x,
                    "y1": y,
                    "z1": z,
                    "x2": x + w,
                    "y2": y + h,
                    "z2": z + l,
                    "file": file_path,
                }
            )
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    overlaps = []
    # If proposed_build exists, it's the first element in 'builds'
    start_index_for_comparison = 1 if proposed_build else 0

    for i in range(len(builds)):
        # If proposed_build, only compare it to existing builds (from index 1 onwards)
        # Otherwise, compare all builds against each other from their respective positions
        current_comparison_start = (
            start_index_for_comparison if i == 0 and proposed_build else i + 1
        )

        for j in range(current_comparison_start, len(builds)):
            b1 = builds[i]
            b2 = builds[j]

            # Skip comparing a build with itself
            if b1["id"] == b2["id"] and b1["file"] == b2["file"]:
                continue

            # AABB Overlap Check
            if (
                b1["x1"] < b2["x2"]
                and b1["x2"] > b2["x1"]
                and b1["y1"] < b2["y2"]
                and b1["y2"] > b2["y1"]
                and b1["z1"] < b2["z2"]
                and b1["z2"] > b2["z1"]
            ):
                overlaps.append((b1, b2))

    if overlaps:
        print(f"⚠️  Detected {len(overlaps)} build conflicts:")
        for b1, b2 in overlaps:
            print(f"  [CONFLICT] {b1['id']} overlaps with {b2['id']}")
            print(
                f"    - {b1['id']}: ({b1['x1']}, {b1['y1']}, {b1['z1']}) to ({b1['x2']}, {b1['y2']}, {b1['z2']})"
            )
            print(
                f"    - {b2['id']}: ({b2['x1']}, {b2['y1']}, {b2['z1']}) to ({b2['x2']}, {b2['y2']}, {b2['z2']})"
            )
        return overlaps  # Return conflicts
    else:
        print("✅ No build conflicts detected among placed structures.")
        return []  # Return empty list if no conflicts


if __name__ == "__main__":
    schem_dir = os.path.join(os.path.dirname(__file__), "schem_files")
    print("Running overlap check on existing schematics...")
    check_overlaps(schem_dir)

    # Example of how to use with a proposed build
    print("\n--- Testing with a proposed new build ---")
    test_proposed_build = {
        "id": "TEST_PROPOSED_HOUSE",
        "x1": -1060,
        "y1": 60,
        "z1": -530,
        "x2": -1040,
        "y2": 80,
        "z2": -510,
        "file": "/home/minecraft/schematics/build_metadata/TEST_PROPOSED_HOUSE.json",
    }
    print(f"Proposing build: {test_proposed_build['id']}")
    conflicts = check_overlaps(schem_dir, test_proposed_build)
    if conflicts:
        print(f"Proposed build CONFLICTS: {len(conflicts)} conflicts found.")
    else:
        print("Proposed build has NO conflicts.")
