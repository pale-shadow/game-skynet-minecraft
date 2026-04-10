import mariadb

import sys
import os

# Identify the physical location to bypass clusterfs symlink issues
CURRENT_FILE = os.path.realpath(__file__)
DATABASE_DIR = os.path.dirname(CURRENT_FILE)
SRC_DIR = os.path.dirname(DATABASE_DIR)
SCHEMATICS_DIR = os.path.join(SRC_DIR, "schematics")

# Inject the schematics directory to resolve skynet_core.py
if SCHEMATICS_DIR not in sys.path:
    sys.path.insert(0, SCHEMATICS_DIR)

try:
    from skynet_core import Config
except ImportError as e:
    print(f"FATAL: Database orchestrator could not load skynet_core from {SCHEMATICS_DIR}: {e}")
    sys.exit(1)

class VaultManager:
    """
    Orchestrates SQL operations for the skynet_vault on the blowfish host.
    """
    def __init__(self):
        self.config = {
            "host": "10.10.12.15",
            "port": 3306,
            "user": os.getenv("DB_USER", "skynet_admin"),
            "password": os.getenv("RCON_PASS"), # Shared credential for cluster auth
            "database": "skynet_vault"
        }

    def _get_connection(self):
        try:
            return mariadb.connect(**self.config)
        except mariadb.Error as e:
            print(f"ERROR: Connectivity failure to blowfish (Hub 07): {e}")
            return None

    def log_build(self, x, y, z, width, depth, schematic, hardware):
        """
        Commits architectural telemetry to Hub 07.
        """
        conn = self._get_connection()
        if not conn: return
        
        cursor = conn.cursor()
        query = ("INSERT INTO build_history "
                 "(x, y, z, w, d, schematic_name, ai_hardware) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        
        try:
            cursor.execute(query, (x, y, z, width, depth, schematic, hardware))
            conn.commit()
            print(f"Vault synchronized: {schematic} at ({x}, {z}) via {hardware}")
        except mariadb.Error as e:
            print(f"SQL Error: {e}")
        finally:
            conn.close()

    def fetch_history(self):
        """
        Retrieves build records for NPUSpatialEngine density map generation.
        """
        conn = self._get_connection()
        if not conn: return []
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT x, y, z, w, d FROM build_history")
        results = cursor.fetchall()
        conn.close()
        return results

    def migrate_json(self, json_path):
        """
        One-time migration from legacy flat-file JSON to MariaDB.
        """
        if not os.path.exists(json_path): return
        
        with open(json_path, 'r') as f:
            import json
            legacy_data = json.load(f)
            
        for entry in legacy_data:
            self.log_build(
                entry.get('x'), entry.get('y'), entry.get('z'),
                entry.get('w', 10), entry.get('d', 10),
                "legacy_import", "manual"
            )
