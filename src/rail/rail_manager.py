import asyncio
import json
import logging
import os
import rcon
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class RailRegistry:
    def __init__(self, registry_file):
        self.registry_file = registry_file
        self.registry_data = None
        self.last_modified = 0

    async def load_registry(self):
        if not os.path.exists(self.registry_file):
            return {}

        with open(self.registry_file, 'r') as f:
            self.registry_data = json.load(f)
            self.last_modified = os.stat(self.registry_file).st_mtime

    def is_registry_changed(self):
        current_modified = os.stat(self.registry_file).st_mtime
        if current_modified != self.last_modified:
            self.last_modified = current_modified
            return True
        return False

class MarkerManager:
    def __init__(self, markers_file):
        self.markers_file = markers_file
        self.markers_data = None

    async def load_markers(self):
        with open(self.markers_file, 'r') as f:
            self.markers_data = json.load(f)

    def update_marker(self, marker_id, active):
        if not self.markers_data:
            return

        for mark in self.markers_data['markers']:
            if mark['id'] == marker_id:
                mark['color'] = 'green' if active else 'red'
                with open(self.markers_file, 'w') as f:
                    json.dump(self.markers_data, f)
                break

class RailManager:
    def __init__(self, rcon_host, rcon_port, registry_file, markers_file):
        self.rcon_host = rcon_host
        self.rcon_port = rcon_port
        self.registry_file = registry_file
        self.markers_file = markers_file
        self.rail_registry = RailRegistry(registry_file)
        self.marker_manager = MarkerManager(markers_file)

    async def check_safety(self, x, y, z):
        """
        Queries Edge-T (Hub-06) to ensure no players are within 5 blocks. 
        """
        try:
            # Connect to the Edge TPU vision daemon on Hub-06
            reader, writer = await asyncio.open_connection('10.10.8.66', 8808)
            query = json.dumps({"task": "proximity_check", "coords": [x, y, z], "radius": 5})
            writer.write(query.encode() + b'\n')
            await writer.drain()

            response = await reader.read(1024)
            data = json.loads(response.decode())
            writer.close()
            await writer.wait_closed()

            if data.get("detected_entities", 0) > 0:
                with open('logs/rail_safety.log', 'a') as log_file:
                    log_file.write(f"[{datetime.now()}] ABORT: Player detected near {x},{y},{z}\n")
                return False
            return True
        except Exception as e:
            logging.error(f"Safety Daemon Unreachable: {e}")
            return False # Fail-safe: assume unsafe if daemon is down

    async def sync_bluemap(self, marker_id, active):
        """
        Dynamically updates BlueMap markers to reflect switch state. [cite: 4501, 6131]
        """
        try:
            async with aiofiles.open(self.markers_file, mode='r') as f:
                content = await f.read()
                data = json.loads(content)

            # Update the specific POI color
            for marker in data.get('markers', []):
                if marker.get('id') == marker_id:
                    marker['color'] = "#00FF00" if active else "#FF0000"
                    break

            async with aiofiles.open(self.markers_file, mode='w') as f:
                await f.write(json.dumps(data, indent=4))
            logging.info(f"BlueMap POI '{marker_id}' synced.")
        except Exception as e:
            logging.warning(f"BlueMap Sync Failed: {e}")

    async def toggle_rail(self, x, y, z):
        await self.check_safety(x, y, z)
        if not await self.rail_registry.load_registry():
            return

        registry_data = self.rail_registry.registry_data
        powered_rail_block = f"{x},{y},{z}"
        for route in registry_data['routes']:
            if powered_rail_block in route['blocks']:
                try:
                    # Async RCON Controller: toggle powered_rail blocks using /execute
                    rcon_client = rcon.RCON(self.rcon_host, self.rcon_port)
                    await asyncio.sleep(0.05)  # delay to protect 20 TPS target
                    await rcon_client.send(f"/execute in minecraft:overworld run setblock {x} {y} {z} powered_rail")
                except Exception as e:
                    logging.error(f"Critical failure: {e}")
                    return

        self.marker_manager.update_marker(registry_data['marker_id'], True)

    async def main_loop(self):
        while True:
            if await self.rail_registry.is_registry_changed():
                await self.rail_registry.load_registry()
                registry_data = self.rail_registry.registry_data
                for route in registry_data['routes']:
                    powered_rail_block = f"{route['x']},{route['y']},{route['z']}"
                    await self.toggle_rail(*map(int, powered_rail_block.split(',')))
            await asyncio.sleep(1)  # poll registry every second

if __name__ == '__main__':
    rcon_host = 'localhost'
    rcon_port = 25575
    registry_file = 'config/rail_registry.json'
    markers_file = 'markers.json'

    rail_manager = RailManager(rcon_host, rcon_port, registry_file, markers_file)
    await rail_manager.main_loop()