# Stargate Node: Central Architectural Agent

Stargate is the specialized inference node for complex structures within the Skynet AI cluster. It leverages high-speed NVMe storage and Raspberry Pi 5 processing power to act as the primary orchestrator for Text-to-Building (T2BM) operations.

## Roles and Responsibilities

*   **LLM Inference Hub:** Executes T2BM models for architectural design.
*   **MCP Orchestrator:** Hosts the Model Context Protocol (MCP) servers that bridge AI reasoning with server-side tools.
*   **Technical Ledger:** Manages the Git-based history of all AI-generated builds.

## Setup and Deployment

1.  **Environment Sync:**
    Run `make stargate` from the project root to prepare the virtual environment and install dependencies.

2.  **Service Management:**
    Use `deploy.sh` to install and start the `stargate-daemon.service`.

3.  **MCP Configuration:**
    Ensure `src/mcp_server/mcp-servers.json` reflects the correct paths for the Stargate node.

## Hardware Profile
- **Compute:** Raspberry Pi 5 (8GB RAM)
- **Storage:** 476.9G NVMe SSD
- **Network ID:** Hub-01 (Inference Nexus)

---
*Created for theDevilsVoice | Last Updated: April 14, 2026*
