# RCON Bridge (Skynet Execution Layer)

This directory contains the execution scripts for the **Skynet Architect** system, interfacing with the Minecraft server via RCON.

## Execution Tools
- **`rcon.sh`**: A manual shell script for direct RCON interaction and testing.
- **Automated RCON:** Primary automated RCON interaction is handled by the Model Context Protocol (MCP) via `mcp-server/rcon_service.py`, orchestrated by `skynet_unified.py`.

## Delivery Protocol
The system utilizes High-Speed RCON, often managed through the MCP, for efficient deployment of NPU-generated "Void-Tech" structures with minimal server lag.
