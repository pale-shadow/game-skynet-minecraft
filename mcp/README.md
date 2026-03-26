# MCP

The preparation steps for the Stargate host (10.10.16.66) to connect to the Minecraft host "chonk" (10.10.8.60) via an MCP server.

  1. Environment & Infrastructure (Stargate Host)
   * Storage Migration: Move the project workspace to the high-speed NVMe mount at /mnt/clusterfs2/game-chonk-minecraft to handle T2BM (Text to Building in Minecraft) model weights and
     schematic I/O with low latency.
   * Virtual Environment: Create a fresh Python 11+ virtual environment on the NVMe drive and install dependencies, including the MCP Python SDK (pip install mcp).
   * Hardware Acceleration: Ensure direnv is configured to export CUDA and LD_LIBRARY_PATH for NPU-accelerated (Hailo-8L) inference.
   * Credential Management: Securely store the RCON_PASS in a root .envrc file, ensuring special characters (like %%) are properly escaped for the RCON client.

  2. MCP Server Configuration (Stargate Host)
  Deploy four specialized MCP servers to act as "tools" for the AI Brain:
   * Filesystem Server: Provides the AI with read/write access to schematics/, models/, and internal/ for blueprint management.
   * RCON Tool Server: Wraps the SkynetRCON client, allowing the LLM to execute setblock and fill commands as standardized protocol calls.
   * Git Server: Automates backup_to_git.sh to commit successful "Void-Tech" designs.
   * Database Context Server: Connects to the database/ folder to query WorldGuard regions and CoreProtect logs, preventing the AI from building over heritage sites.

  3. Orchestrator Migration (skynet_unified.py)
   * Primary Node Assignment: Update skynet_unified.py to designate Stargate as the Primary Orchestrator & LLM Inference Node.
   * T2BM Integration: Refactor the orchestrator to use MCP tool calls instead of direct shell commands for the "Sense, Plan, Act" cycle.
   * Systemd Update: Reconfigure the skynet-daemon.service on Stargate to point to the new /mnt/clusterfs2 working directory and its virtual environment.

  4. Target Host Preparation (Chonk Host)
   * Safety Guardrails: Ensure WorldGuard (for region protection), CoreProtect (for auditing/rollbacks), and Spark (for performance profiling) are active on the Minecraft server.
   * Network Access: Verify that RCON is enabled in server.properties and that Stargate’s IP is whitelisted/accessible on the RCON port (default 25575).

  By completing these steps, the Stargate host will be ready to act as the centralized MCP hub, orchestrating autonomous construction on chonk with full architectural awareness and safety
  protocols.

## MCP setup

Configure MCP on the `stargate.research.bitsmasher.net` host
