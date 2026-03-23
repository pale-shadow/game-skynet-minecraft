
import time
import random
from datetime import datetime, timedelta
import re
from mcrcon import MCRcon
import mcschematic
import importlib
import os

# --- Configuration ---
# TODO: Move to a dedicated config file (e.g., config.json)
RCON_HOST = "localhost"
RCON_PORT = 25575
RCON_PASSWORD = "YourUltraSecurePassword"  # Replace with your actual RCON password

BUILD_COOLDOWN_HOURS = 1
PLAYER_CHECK_SECONDS = 600  # 10 minutes
WARNING_INTERVAL_SECONDS = 30  # 30 seconds

# The AI containment fields / industrial areas
SECTORS = {
    "Shroomville Urban District": {"x": (1600, 1850), "z": (650, 900)},
    "Silicon Ridge (Beta-Zone)": {"x": (1400, 1575), "z": (700, 875)},
    "Abyssal Reef (Ocean Sector)": {"x": (1900, 2050), "z": (700, 850)}
}

# --- RCON Communication ---
def send_rcon_command(command):
    """Sends a command to the Minecraft server via RCON."""
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            return mcr.command(command)
    except Exception as e:
        print(f"[{datetime.now()}] RCON Error: {e}")
        return None

# --- Core Logic ---
def get_players_in_zones():
    """
    Checks for players in the designated zones.
    Returns a set of player names found in restricted areas.
    """
    players_in_restricted_zones = set()

    # 1. Get list of online players
    resp = send_rcon_command("/list")
    if not resp:
        return players_in_restricted_zones
        
    # Regex to find player names from the '/list' command output
    # Example: "There are 2 of a max 20 players online: player1, player2"
    try:
        player_names = resp.split(":")[1].strip().split(", ")
        if not player_names or player_names == ['']:
             return players_in_restricted_zones
    except IndexError:
        return players_in_restricted_zones # No players online

    # 2. For each player, get their position and check it
    for name in player_names:
        name = name.strip()
        pos_resp = send_rcon_command(f"/data get entity {name} Pos")
        if not pos_resp:
            continue
        
        # Regex to parse coordinates from /data command output
        # Example: 'player has the following entity data: [1700.5d, 64.0d, 750.5d]'
        match = re.search(r'\[(-?[\d\.]+)d, (-?[\d\.]+)d, (-?[\d\.]+)d\]', pos_resp)
        if not match:
            continue
            
        px, _, pz = map(float, match.groups())

        # 3. Check if the player's position is within any sector
        for sector_name, bounds in SECTORS.items():
            x_bounds, z_bounds = bounds["x"], bounds["z"]
            if x_bounds[0] <= px <= x_bounds[1] and z_bounds[0] <= pz <= z_bounds[1]:
                print(f"[{datetime.now()}] Player '{name}' detected in restricted sector: {sector_name}")
                players_in_restricted_zones.add(name)
                break # No need to check other sectors for this player
                
    return players_in_restricted_zones

def run_build_cycle():
    """Selects a random build, generates it, and deploys it via RCON."""
    print(f"[{datetime.now()}] Initiating hourly autonomous build cycle.")
    
    # --- 1. Randomization ---
    structure_types = ["house", "tower", "bridge", "castle"] # Removed 'terrain' as it may not have a dedicated builder
    palettes = ["Nature vs Engineering", "Void-Tech Overgrowth"]
    
    selected_type = random.choice(structure_types)
    selected_palette = random.choice(palettes)
    build_name = f"SKYNET_{selected_type.upper()}_{random.randint(1000, 9999)}"

    sector_name = random.choice(list(SECTORS.keys()))
    bounds = SECTORS[sector_name]
    target_x = random.randint(bounds["x"][0], bounds["x"][1])
    target_z = random.randint(bounds["z"][0], bounds["z"][1])
    target_y = 64 # Build at a standard ground level

    print(f"[{datetime.now()}] SELECTED: Build '{build_name}' of type '{selected_type}' in {sector_name}")

    # --- 2. Build Schematic ---
    try:
        # Dynamically import the correct builder module
        builder_module = importlib.import_module(f".builders.{selected_type}", "schematics")
        builder_function = getattr(builder_module, f"build_{selected_type}")

        # Create a prompt for the builder
        prompt = {
            "dimensions": {
                "width": random.randint(7, 15),
                "height": random.randint(12, 30),
                "length": random.randint(7, 15)
            },
            "features": {
                "void_tech": selected_palette == "Void-Tech Overgrowth",
                "has_roof": random.choice([True, False]),
                "crenellations": random.choice([True, False]),
                "has_railing": True
            }
        }

        # Generate the schematic object
        schem = mcschematic.MCSchematic()
        builder_function(schem, prompt)

        # Save the schematic to a file
        schem_dir = "schematics/schem_files"
        os.makedirs(schem_dir, exist_ok=True)
        schem.save(schem_dir, build_name, mcschematic.Version.JE_1_20_1)
        print(f"[{datetime.now()}] Successfully generated schematic: {build_name}.schem")

    except Exception as e:
        print(f"[{datetime.now()}] ERROR during schematic generation: {e}")
        return # Abort this build cycle

    # --- 3. Deploy via RCON (FAWE) ---
    print(f"[{datetime.now()}] Deploying schematic at ({target_x}, {target_y}, {target_z})")
    send_rcon_command(f"say [Skynet] Commencing construction of '{build_name}' in sector: {sector_name}.")
    
    # Use FAWE commands to load and paste the schematic
    # Assumes schematics are saved in the `plugins/FastAsyncWorldEdit/schematics` directory on the server
    # A server-side script might be needed to move the file to the correct location
    # For now, we assume the schematics directory is accessible.
    resp_load = send_rcon_command(f"//schem load {build_name}")
    print(f"[{datetime.now()}] SCHEM LOAD response: {resp_load}")

    # Use /execute to run the paste command at the correct coordinates
    resp_paste = send_rcon_command(f"/execute positioned {target_x} {target_y} {target_z} run //paste -a")
    print(f"[{datetime.now()}] PASTE response: {resp_paste}")

    print(f"[{datetime.now()}] Build cycle complete.")

def schedule_next_build_time(current_time):
    """Schedules the next build for a random minute within the next hour."""
    minutes_from_now = random.randint(0, 59)
    return current_time + timedelta(hours=BUILD_COOLDOWN_HOURS, minutes=minutes_from_now)
    
# --- Main Daemon Loop ---
def main():
    print("Skynet AI Orchestrator v1.3 Initializing...")

    # --- State Variables ---
    next_player_check_time = datetime.now()
    next_build_time = schedule_next_build_time(datetime.now())
    players_in_zone = {} # { "player_name": <last_warning_time> }
    
    print(f"Next build scheduled for: {next_build_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while True:
        now = datetime.now()

        # 1. Handle Hourly Random Build
        if now >= next_build_time:
            run_build_cycle()
            next_build_time = schedule_next_build_time(now)
            print(f"Next build scheduled for: {next_build_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 2. Handle 10-Minute Player Check
        if now >= next_player_check_time:
            print(f"[{now}] Running 10-minute player check in restricted zones...")
            detected_players = get_players_in_zones()

            # Add new players to the warning list
            for name in detected_players:
                if name not in players_in_zone:
                    print(f"[{now}] New player '{name}' detected. Adding to warning list.")
                    players_in_zone[name] = datetime.min # Send warning immediately

            # Remove players who have left
            for name in list(players_in_zone.keys()):
                if name not in detected_players:
                    print(f"[{now}] Player '{name}' has left the restricted zone.")
                    del players_in_zone[name]
            
            next_player_check_time = now + timedelta(seconds=PLAYER_CHECK_SECONDS)

        # 3. Handle 30-Second Warning Messages
        for name, last_warning_time in players_in_zone.items():
            if (now - last_warning_time).total_seconds() >= WARNING_INTERVAL_SECONDS:
                print(f"[{now}] Sending 30-second warning to '{name}'.")
                send_rcon_command(f'tellraw {name} ["", {{"text":"[SKYNET]","color":"dark_red"}}, {{"text":" WARNING: You are in a restricted automated construction zone. Please vacate the area.","color":"red"}}]')
                players_in_zone[name] = now
        
        # Main loop sleep
        time.sleep(5)

if __name__ == "__main__":
    main()
