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
- **Neural-Data Vault (MariaDB)**: `10.10.12.15` @ blowfish (OpenBSD 7.8)
- **Partner Node (femputer)**: `10.10.15.15` (Owner: slyb0rg). Migrated from Digital Ocean on Jan 26, 2026. Backup: [slyb0t/Stream-Minecraft-Server-](https://github.com/slyb0t/Stream-Minecraft-Server-)

- **Performance Profile (2026 Audit):**
 - **Redstone:** `ALTERNATE_CURRENT` implementation enabled, utilizing optimized plugin settings (e.g., `paper.yml` redstone-dust-lag-compensate) for reduced tick impact.
  - **Villager Logic:** Optimized POI pings (`60` ticks) and inactive ticking disabled, configured in `paper.yml` to minimize entity processing overhead.
  - **Chunk System:** Async loading with auto-detecting IO threads, configured via `paper.yml` (`chunk-loading.async` and `chunk-loading.auto-config-by-distance`) for smoother world generation and reduced server strain.
- **Directory Structure:** - `~/bin/`: Custom management scripts (`common.sh`, `backup_to_git.sh`).
  - `~/config/`: Centralized Paper/Spigot/Global configuration hub.
  - `~/docs/`: Historical records (HISTORY.md) and BlueMap manifests.
- **Environment Management:** Use `direnv` for local environment variable management. Storing sensitive information like `RCON_PASS` securely in `.envrc` ensures consistent, secure, and efficient access for all scripts and tools, preventing authentication issues and streamlining automated tasks that impact TPS.

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

### 6. AI Interaction Best Practices for TPS
- **Batch Commands:** When interacting via RCON, consolidate multiple `setblock` or `fill` operations into single, batched commands to reduce command overhead and minimize server ticks. 
- **Spatial Cohesion:** AI-driven builds should prioritize contiguous placement and avoid fragmented, sparse constructions that can lead to inefficient chunk loading.
- **Rate Limiting:** Implement rate limits for AI-initiated RCON commands and schematic deployments to prevent command spam and sudden TPS drops. 
- **Asynchronous Operations:** Whenever possible, AI tasks that do not require immediate server feedback (e.g., complex calculations, metadata updates) should be offloaded to asynchronous processes or dedicated AI nodes to avoid blocking the main server thread.

### 7. 2026 Landmark Registry (Shroomville District)
- **Logistics:** Deep-Rail Station ($1832, 31, 688$) and Rail Yard/Repair Shed ($1618, 63, 676$).
- **Defense:** Western Gate ($1484, 63, 750$) - Automated Night-Lock.
- **Culture:** SS Shroomville Museum, Aviary, and Cathedral Plaza.
- **Industry:** Western Blacksmith and Villager Hutt (Staff Housing).

### 7. Administrative Workflows
- **Autonomous Operation:** The "Skynet" daemon (`skynet_unified.py`) runs as a systemd service (`skynet-daemon.service`) from the Stargate MCP (`10.10.16.66`). It manages daily procedural urbanization builds and monitors restricted zones. 
- **RCON Integrity:** Authentication for RCON is robust, with `RCON_PASS` managed via `direnv` to prevent quoting issues. The RCON link is active and verifies with `list` and `data get` commands.
- **Urbanization Cycle:** Automated deployment of high-fidelity v5 schematics (e.g., houses, bridges) to the AI Containment Area is functional and includes pre-deployment validation to prevent overlaps.
- **Chunk Regeneration:** `bluemap fix-edges` is used for visual continuity after terrain resets.
- **Region Management:** `WorldGuard` is utilized to prevent "Ghost" chunk corruption in legacy zones.
- **Schematic & Metadata Management:** All schematic (`.schem`) files and their corresponding JSON metadata are stored and managed via the standardized `/mnt/clusterfs/minecraft/schematics` NFS mount. This ensures consistent state awareness and eliminates manual transfers across AI nodes.

### 8. Multi-Host Repository & Artifact Organization
- **Unified Codebase:** The entire `game-skynet-minecraft` repository is cloned on every host in the network (Chonk, Stargate, Skynet, Edge-T), ensuring version parity and simplified deployment.
- **Artifact Registry (`/src/servers/`):** Host-specific configurations, systemd units, and local daemon scripts are stored in subdirectories of `/src/servers/`.
  - **Organization Standard:** Each host folder (e.g., `/src/servers/skynet/`) must contain:
    - `[host]-daemon.service`: The systemd unit file (symlinked to `/etc/systemd/system/`).
    - `[host]-daemon.py`: The host's primary entry point (if not using a shared core script).
    - `README.md`: Host-specific hardware requirements, OS details (Debian/Mendel/OpenBSD), and setup steps.
- **Service Deployment:** To deploy a service on a specific host:
  ```bash
  sudo ln -s /home/minecraft/game-skynet-minecraft/src/servers/[host]/[host]-daemon.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable --now [host]-daemon.service
  ```
---

*Created for theDevilsVoice | Last Updated: April 26, 2026*
