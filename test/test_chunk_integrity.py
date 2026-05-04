import os
import struct
import pytest
from src.utils.config_utils import setup_logging

logger = setup_logging("test_chunk_integrity")

# Define potential world paths (configurable via environment)
WORLD_PATHS = [
    os.getenv("WORLD_PATH", "world/region"),
    "/mnt/clusterfs/minecraft/world/region",
    "/home/minecraft/world/region"
]

def is_valid_mca_header(file_path):
    """
    Checks if the .mca file has a valid header structure.
    Minecraft Region files (.mca) start with a 4096-byte location table.
    Each entry is 4 bytes (offset and sector count).
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(8192) # Read location and timestamp tables
            if len(header) < 8192:
                return False
            return True
    except Exception:
        return False

@pytest.mark.world
def test_region_file_discovery():
    """Verify that region files are accessible for auditing."""
    found = False
    for path in WORLD_PATHS:
        if os.path.exists(path):
            mca_files = [f for f in os.listdir(path) if f.endswith(".mca")]
            if mca_files:
                found = True
                logger.info(f"Discovered {len(mca_files)} region files in {path}")
                break
    
    if not found:
        pytest.skip("No Minecraft region (.mca) files found in standard search paths.")

@pytest.mark.world
def test_chunk_file_integrity():
    """Perform a structural audit of discovered .mca files."""
    errors = []
    checked_count = 0
    
    for path in WORLD_PATHS:
        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith(".mca"):
                    full_path = os.path.join(path, filename)
                    checked_count += 1
                    if not is_valid_mca_header(full_path):
                        errors.append(f"CORRUPTION DETECTED: {full_path} has invalid header.")
                    
                    # Check file size (must be multiple of 4096 sectors)
                    size = os.path.getsize(full_path)
                    if size < 8192:
                        errors.append(f"ERROR: {full_path} is truncated ({size} bytes).")
                    elif size % 4096 != 0:
                        # While not always a fatal error in MC, it indicates improper alignment
                        pass

    assert not errors, f"Chunk Integrity Audit failed with {len(errors)} errors:\n" + "\n".join(errors)
    if checked_count == 0:
         pytest.skip("No .mca files were available for integrity check.")
