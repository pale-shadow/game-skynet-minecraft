# Gemini AI Context & Server Manifesto
## Project: Bitsmasher Minecraft (minecraft.bitsmasher.net)

### 1. Server Essence
- **Founded:** 2012
- **Current Core:** Paper 1.21.1 (Java 21)
- **Legacy:** Originally Paper/CraftBukkit -> Long Forge/Modded Era -> Modern Paper.
- **2026 Focus:** Urbanization of the Shroomville Biome and "Deep-Rail" connectivity.

### 2. Infrastructure & DevOps
- **Host Environment:** Debian 12 (Bookworm) @ chonk (`10.10.8.60`)
- **AI Hardware:** `10.10.16.10` (Pi 5 + Hailo-8L)
- **Stargate MCP:** `10.10.16.66` (Master Control Program for AI hardware)
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
- **Autonomous Operation:** The "Skynet" daemon (`skynet_unified.py`) runs as a systemd service (`skynet-daemon.service`) from the Stargate MCP (`10.10.16.66`). It manages hourly procedural urbanization builds and monitors restricted zones. 
- **RCON Integrity:** (Resolved Mar 26, 2026) Fixed authentication failure caused by corrupted `RCON_PASS` quoting in systemd environment definitions. Verified RCON link is active and responding to `list` and `data get` commands.
- **Urbanization Cycle:** Automated deployment of high-fidelity v5 schematics (e.g., houses, bridges) to the AI Containment Area is functional.
- **Chunk Regeneration:** Use `bluemap fix-edges` for visual continuity after terrain resets.
- **Region Management:** Use `WorldGuard` to prevent "Ghost" chunk corruption in legacy zones.
---
*Created for theDevilsVoice | Last Updated: March 26, 2026*
