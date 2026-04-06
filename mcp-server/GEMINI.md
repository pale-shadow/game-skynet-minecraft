# MCP (Model Context Protocol) - Technical Deep Dive

This document provides a detailed technical overview of the Model Context Protocol (MCP) setup, focusing on the MCP servers hosted on the Stargate MCP (`stargate.research.bitsmasher.net`) and their integration with the Skynet AI Brain and the Minecraft server (`chonk`, `10.10.8.60`).

## 1. MCP Architecture and Goals

The MCP is designed to bridge high-level LLM reasoning (specifically the T2BM - Text to Building in Minecraft pipeline) with the Minecraft server's low-level administrative tools. Its primary goals are:

*   **Low-Latency I/O:** Leveraging Stargate's 476.9G NVMe SSD (`/mnt/clusterfs2/`) for fast access to model weights, schematics, and intermediate data.
*   **Standardized Tool Interface:** Abstracting complex operations (like RCON commands, file manipulation, Git commits) into standardized MCP "Tool Calls" that the LLM can invoke.
*   **Performance Optimization:** Offloading heavy AI inference and orchestration to Stargate to maintain the Minecraft server's target 20 TPS.
*   **Safety and Heritage Preservation:** Integrating with server-side plugins (WorldGuard, CoreProtect) to prevent AI constructions from overwriting critical game assets or historical sites.

## 2. MCP Server Configurations (`mcp-servers.json`)

The `mcp-servers.json` file defines the MCP servers running on Stargate and their configurations.

### `filesystem-stargate`

*   **Purpose:** Manages file system access for the AI. Grants read/write capabilities to `schematics/`, `models/`, and `internal/` directories on the NVMe mount.
*   **Command:** `npx -y @modelcontextprotocol/server-filesystem`
*   **Arguments:**
    *   `/home/minecraft/game-skynet-minecraft/schematics`: Source directory for schematics.
    *   `/home/minecraft/schematics`: Target directory for schematics.
*   **Environment Variables:**
    *   `SERVER_DIR`: `/home/minecraft` (Sets the base server directory).

### `rcon-chonk`

*   **Purpose:** Acts as an RCON client interface, translating LLM commands into Minecraft RCON protocol calls (`setblock`, `fill`, etc.).
*   **Command:** `python3 /home/minecraft/game-skynet-minecraft/mcp-server/rcon_service.py`
*   **Environment Variables:**
    *   `RCON_HOST`: `10.10.8.60` (The Minecraft server's IP address).
    *   `RCON_PORT`: `25575` (The RCON port).
    *   `HUB_ID`: `Hub-02` (Identifier for this service/node).

### `git-ledger`

*   **Purpose:** Automates the Git backup process for successful AI-generated designs and world state changes.
*   **Command:** `python3 /home/minecraft/game-skynet-minecraft/mcp-server/git_service.py`
*   **Environment Variables:**
    *   `BACKUP_SCRIPT`: `/home/minecraft/bin/backup_to_git.sh` (Path to the backup script).

### `vision-edge-t`

*   **Purpose:** (Runs remotely on `edge-t` host `10.10.16.4`) Provides vision and terrain audit capabilities using Edge TPUs. This server exposes tools like `audit_terrain` and `get_traversability_map`.
*   **Command:** `python3 /home/minecraft/game-skynet-minecraft/mcp-server/vision_service.py`
*   **Environment Variables:**
    *   `EDGETPU_SHARED_LIB`: `libedgetpu.so.1` (Path to the Edge TPU shared library).
    *   `MODEL_PATH`: `/home/minecraft/game-skynet-minecraft/models/vision_v1.tflite` (Path to the vision model).
    *   `SENSE_NET_HUB`: `Hub-06` (Identifier for the vision sense network).
*   **Remote Configuration:**
    *   `host`: `10.10.16.4`
    *   `user`: `minecraft`

### `npu-skynet`

*   **Purpose:** Orchestrates AI inference using Hailo-8L NPUs for schematic generation and other AI tasks.
*   **Command:** `python3 /home/minecraft/game-skynet-minecraft/mcp-server/npu_service.py`
*   **Environment Variables:**
    *   `HAILO_NPU_ACTIVE`: `true` (Enables NPU hardware acceleration).
    *   `SCHEM_GEN_PATH`: `/home/minecraft/game-skynet-minecraft/schem-gen` (Path for schematic generation tools).
    *   `LOGIC_CORE`: `Hub-01` (Identifier for the core logic unit).

## 3. T2BM Pipeline Integration

The MCP is central to the T2BM pipeline, facilitating three key stages:

1.  **Prompt Refining:** The AI uses the `filesystem-stargate` MCP to access environmental requirements and refine them into detailed architectural prompts.
2.  **Decoding Interlayer Representation:** The LLM translates conceptual designs into spatial block data.
3.  **Repairing:** The AI identifies and fixes structural errors. This stage utilizes the `rcon-chonk` server to deploy blocks and the `vision-edge-t` server for integrity checks.

## 4. Safety and Heritage Safeguards

*   **WorldGuard Regions:** The `database-context` server queries WorldGuard to identify and avoid building within protected heritage zones (e.g., 2012 Washington Station).
*   **CoreProtect Auditing:** CoreProtect logs AI block mutations, enabling rollbacks if the "Repairing" stage fails.
## 5. Repository Structure and File Roles

*   **`mcp-server/`**: Contains the Python scripts and configuration for the MCP servers.
    *   `rcon_service.py`: Implements the RCON tool server.
    *   `git_service.py`: Implements the Git automation server.
    *   `vision_service.py`: Implements the vision MCP service on the `edge-t` host.
    *   `npu_service.py`: Implements the NPU service on Stargate.
    *   `mcp-servers.json`: Configuration file for all MCP servers.
    *   `setup.txt`: High-level setup instructions.
    *   `mcp-notes.txt`: Detailed notes on MCP setup and integration.
    *   `README.md`: Original README for MCP.
    *   `__init__.py`: Python package initialization file (currently empty).

## 6. Alternative Considerations (vs. Zapier)

Native Python/Node.js scripts for MCP services are preferred over external automation tools like Zapier due to:
*   **Reduced Latency:** Direct communication over the local subnet (`10.10.16.x`) avoids external API calls and webhooks.
*   **Enhanced Security:** Keeps RCON and database access restricted to trusted IPs/localhost, minimizing attack surface.
*   **Performance:** Native services can be monitored and optimized using tools like Spark, ensuring stable TPS.

Tools like DiscordSRV are recommended for remote monitoring and console access, while GitHub Actions are suggested for CI/CD and automated backup workflows.

## 7. Build Coordination Enhancements

*   **Overlap Prevention:** The T2BM pipeline now incorporates pre-deployment 3D AABB overlap detection using `schematics/validate_no_overlaps.py`. This ensures that new schematic generation and deployment are validated against existing build metadata, preventing spatial conflicts and maintaining overall world integrity.

---
