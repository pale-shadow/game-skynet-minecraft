# Gemini AI Context & Server Manifesto
## Project: Bitsmasher Minecraft (minecraft.bitsmasher.net)

### 1. Server Essence
- **Founded:** 2012
- **Current Core:** Paper 1.21.1 (Java 21)
- **Legacy:** Originally Paper/CraftBukkit -> Long Forge/Modded Era -> Modern Paper.
- **2026 Focus:** Urbanization of the Shroomville Biome and "Deep-Rail" connectivity.

### 2. Infrastructure & DevOps
- **Host Environment:** Debian 12 (Bookworm) @ chonk (`10.10.8.60`)
- **AI Hardware (NPU)**: `10.10.16.10` (Pi 5 + Hailo-8L)
- **Vision Overseer (Edge TPU)**: `10.10.16.4` (ASUS Tinker Edge-T / Mendel Linux)
- **Stargate MCP**: `10.10.16.66` (Master Control Program for AI hardware)
- **Partner Node (femputer)**: `10.10.15.15` (Owner: slyb0rg). Migrated from Digital Ocean on Jan 26, 2026. Backup: [slyb0t/Stream-Minecraft-Server-](https://github.com/slyb0t/Stream-Minecraft-Server-)

- **Performance Profile (2026 Audit):**
 - **Redstone:** `ALTERNATE_CURRENT` implementation enabled.
  - **Villager Logic:** Optimized POI pings (`60` ticks) and inactive ticking disabled.
  - **Chunk System:** Async loading with auto-detecting IO threads.
- **Directory Structure:** - `~/bin/`: Custom management scripts (`common.sh`, `backup_to_git.sh`).
  - `~/config/`: Centralized Paper/Spigot/Global configuration hub.
  - `~/docs/`: Historical records (HISTORY.md) and BlueMap manifests.
- **Environment Management:** Use `direnv` for local environment variable management. The RCON password must be stored as `RCON_PASS` in the `.envrc` file and referenced by all scripts and tools needing console access.

### 3. Current Permission Hierarchy (LuckPerms)
| Rank | Weight | Description |
| :--- | :--- | :--- |
| **Hobo** | 10 | Guest. No build/interact. `essentials.build: false`. |
| **Ninja** | 20 | Regular. Claims enabled. Access to ItemSorter. |
| **Hacker** | 30 | Advanced. Flight and Creative perks enabled. |
| **Sheriff** | 99 | Staff/Moderator. Audit power via CoreProtect. |
| **Janitor** | 100 | Owner/Admin. Full RCON/Console access. |

### 4. Critical Plugin & Resource Interdependencies
- **EssentialsX:** Core logic. (Chat/AntiBuild/Core).
- **LuckPerms:** Permission source of truth (MariaDB backend).
- **CoreProtect:** Logging and grief recovery.
- **BlueMap:** SQL-based web rendering (Port 8100).
- **SimpleClaimSystem:** Integrated with BlueMap for visual territory.
- **Maintenance Tools:** `spark` for profiling; `WorldGuard` for legacy protection.

### 5. Interaction Guidelines for AI
- **Strict Formatting:** Use Markdown for logs/code. Use LaTeX only for math/complex science (e.g., $X, Y, Z$ coordinates or performance formulas).
- **Security First:** Redact RCON passwords (e.g., `dinosaur...`) and private IPs.
- **Historical Awareness:** Prioritize the 2012 legacy (Washington Station); safeguard 2014 "Chunk Glitch" heritage sites.
- **No Discord:** Coordination is strictly in-game.

### 6. 2026 Landmark Registry (Shroomville District)
- **Logistics:** Deep-Rail Station ($1832, 31, 688$) and Rail Yard/Repair Shed ($1618, 63, 676$).
- **Defense:** Western Gate ($1484, 63, 750$) - Automated Night-Lock.
- **Culture:** SS Shroomville Museum, Aviary, and Cathedral Plaza.
- **Industry:** Western Blacksmith and Villager Hutt (Staff Housing).

### 7. Administrative Workflows
- **Autonomous Operation:** The "Skynet" daemon (`skynet_unified.py`) runs as a systemd service (`skynet-daemon.service`) from the Stargate MCP (`10.10.16.66`). It manages daily procedural urbanization builds and monitors restricted zones. 
- **RCON Integrity:** (Resolved Mar 26, 2026) Fixed authentication failure caused by corrupted `RCON_PASS` quoting in systemd environment definitions. Verified RCON link is active and responding to `list` and `data get` commands.
- **Urbanization Cycle:** Automated deployment of high-fidelity v5 schematics (e.g., houses, bridges) to the AI Containment Area is functional.
- **Chunk Regeneration:** Use `bluemap fix-edges` for visual continuity after terrain resets.
- **Region Management:** Use `WorldGuard` to prevent "Ghost" chunk corruption in legacy zones.

### 8. Multi-Host Repository & Artifact Organization
- **Unified Codebase:** The entire `game-skynet-minecraft` repository is cloned on every host in the network (Chonk, Stargate, Skynet, Edge-T). This ensures version parity and simplifies deployment.
- **Artifact Registry (`/servers/`):** Host-specific configurations, systemd units, and local daemon scripts are stored in subdirectories of `/servers/`.
  - **Organization Standard:** Each host folder (e.g., `/servers/skynet/`) must contain:
    - `[host]-daemon.service`: The systemd unit file (symlinked to `/etc/systemd/system/`).
    - `[host]-daemon.py`: The host's primary entry point (if not using a shared core script).
    - `README.md`: Host-specific hardware requirements, OS details (Debian/Mendel/OpenBSD), and setup steps.
- **Service Deployment:** To deploy a service on a specific host:
  ```bash
  sudo ln -s /home/minecraft/game-skynet-minecraft/servers/[host]/[host]-daemon.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable --now [host]-daemon.service
  ```
---
   - **Schematic Deployment:** (Resolved Mar 30, 2026) Corrected pathing for `.schem` files generated by `skynet_unified.py` to ensure they are saved directly into the **Stargate MCP's local schematic output directory** (configured for `filesystem-stargate` MCP service) for transfer to the `chonk` host. Future: Migrate `skynet_unified.py` to Stargate MCP and leverage Edge-T (`10.10.16.4`) for advanced schematic generation.
   - **Cross-Host Schematic Deployment (Implemented Mar 31, 2026, Refined Apr 2, 2026):** The `skynet_unified.py` daemon now uses the `MINECRAFT_SCHEM_DIR` environment variable (defaulting to `/home/minecraft/schematics`) to specify the target directory for `.schem` files on the `chonk` host. The systemd service `skynet-daemon.service` on the Stargate MCP must be updated to set this environment variable to ensure correct deployment. Schematics are generated locally on Stargate and then transferred. JSON metadata files may include a `"legacy_build_pre_overlap_detection": true` flag for builds created before overlap detection was fully implemented.
   - **JSON Metadata Generation (Implemented Apr 1, 2026):** All new builds now include a comprehensive JSON metadata file (e.g., `BUILD_ID.json`) stored in `MINECRAFT_SCHEM_DIR/build_metadata/`. This metadata includes spatial data, provenance, and hardware telemetry, crucial for build traceability and overlap prevention.
   - **Build Overlap Prevention (Implemented Apr 1, 2026):** Implemented pre-deployment 3D AABB overlap detection using `schematics/validate_no_overlaps.py`. New builds are now validated against existing metadata in `MINECRAFT_SCHEM_DIR/build_metadata/` before deployment, and any spatial conflicts will automatically abort the build cycle, ensuring structural integrity.
---
*Created for theDevilsVoice | Last Updated: April 5, 2026*
