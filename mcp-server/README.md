# MCP (Model Context Protocol) Setup Guide

This guide outlines the setup and configuration of the Model Context Protocol (MCP) servers on the Stargate host (`stargate.research.bitsmasher.net`), enabling it to act as the central architectural agent and orchestrator for the Skynet AI cluster. This setup leverages Stargate's high-speed NVMe SSD and integrates with the Minecraft server ("Chonk" host at `10.10.8.60`) for autonomous construction and management.

## Purpose

The MCP allows the Skynet AI Brain, particularly the T2BM (Text to Building in Minecraft) model, to interact with the Minecraft environment through specialized tools. This includes managing schematics, executing in-game commands via RCON, automating Git backups, and querying server data for safety and heritage preservation.

## Key Components

The MCP setup on Stargate involves deploying several specialized servers:

*   **Filesystem Server:** Provides read/write access to project directories like `schematics/`, `models/`, and `internal/` for blueprint management.
*   **RCON Tool Server:** Implemented by `mcp-server/rcon_service.py`, this server wraps the SkynetRCON client to allow the LLM to execute `setblock` and `fill` commands as standardized protocol calls.
*   **Git Automation Server:** Integrates `backup_to_git.sh` to automate commits of successful AI-generated designs to Git.

*   **Vision MCP Server:** (Configured on `edge-t` host `10.10.16.4`) Provides vision and terrain audit capabilities using Edge TPUs.
*   **NPU Skynet Server:** (Configured on Stargate) Leverages Hailo-8L NPUs for AI inference and schematic generation.

## Setup Steps

1.  **Environment Preparation on Stargate:**
    *   Move the project workspace to the NVMe mount (`/mnt/clusterfs2/game-skynet-minecraft`).
    *   Create and activate a Python 3 virtual environment.
    *   Install dependencies, including the MCP Python SDK (`pip install mcp`).
    *   Ensure hardware acceleration exports (CUDA, LD_LIBRARY_PATH) are active.
    *   Securely manage `RCON_PASS` in `.envrc`.

2.  **MCP Server Configuration:**
    Initialize the MCP servers as defined in `mcp-servers.json`.

3.  **Orchestrator Integration (`skynet_unified.py`):**
    *   Update the orchestrator to designate Stargate as the Primary Orchestrator & LLM Inference Node.
    *   Refactor the "Sense, Plan, Act" cycle to use MCP tool calls instead of direct shell commands.
    *   Integrate T2BM logic for prompt refining, decoding, and repairing.

4.  **Target Host Preparation (Chonk Host):**
    *   Ensure WorldGuard, CoreProtect, and Spark are active on the Minecraft server.
    *   Verify RCON is enabled and Stargate's IP is whitelisted.

5.  **Service Activation:**
    Update the `skynet-daemon.service` on Stargate to reflect the new working directory and virtual environment.

By following these steps, Stargate acts as a powerful, centralized hub for autonomous AI-driven construction and management within the Minecraft environment.
