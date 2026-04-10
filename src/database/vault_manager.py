import mariadb
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from skynet_core import Config
except ImportError:
    # Fallback for environments where the script is executed from the project root
    sys.path.append(os.path.join(os.getcwd(), "src"))
    from skynet_core import Config

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
