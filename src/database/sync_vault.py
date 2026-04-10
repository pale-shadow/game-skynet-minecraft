import os
import sys

CURRENT_FILE = os.path.realpath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_FILE))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database.vault_manager import VaultManager


def run_orchestration_cycle():
    """
    Triggers the transition from flat-file JSON to MariaDB for Hub 07.
    """
    vault = VaultManager()

    legacy_json = os.path.join(PROJECT_ROOT, "history.json")
    if os.path.exists(legacy_json):
        print(f"STATUS: Migrating legacy architectural records from {legacy_json}...")
        vault.migrate_json(legacy_json)
    else:
        print("NOTICE: No legacy history.json found for migration.")

    print("STATUS: Committing architectural telemetry for Hub 06...")
    vault.log_build(
        x=-1212,
        y=76,
        z=-670,
        width=15,
        depth=15,
        schematic="mono_eye_sensor_v2.schem",
        hardware="edge_tpu",
    )


if __name__ == "__main__":
    run_orchestration_cycle()
    print("SUCCESS: Stargate vault synchronization complete.")
