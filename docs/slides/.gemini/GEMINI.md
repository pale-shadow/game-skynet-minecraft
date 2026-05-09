# GEMINI Directives: Chonk Minecraft Server Slide Deck

## Project Overview
This document serves as the generation guide and narrative foundation for the 20-minute LaTeX Beamer presentation detailing the Chonk Minecraft server integration. The talk focuses on the physical-to-digital telemetry bridge, specifically how in-game events are captured, encapsulated, and routed to the distributed bitsmasher.net AI orchestration network.

## Formatting & Style Directives
* **Framework:** LaTeX Beamer.
* **Theme:** Madrid (default) with standard bitsmasher.net aesthetic considerations.
* **Length:** 10-12 slides to accommodate a 20-minute presentation slot.
* **Tone:** Direct, technical, and engineering-focused.
* **Tooling Context:** Assume all configuration and LaTeX editing is performed locally using `vi`. Avoid referencing `nano` or GUI text editors.
* **Environment Context:** Target deployment and execution references should accurately reflect Debian 12 (Bookworm) and Java 21 environments.

## Narrative Arc & Technical Details

The presentation must trace the lifecycle of a signal from its physical origin in the Minecraft world-space to its ingestion by the Stargate control plane.

### 1. The Chonk Execution Environment
* **Role:** World-State Engine.
* **Stack:** Paper 1.21.11 / Forge on Debian Bookworm.
* **Function:** Handles the active game simulation and local redstone mechanics without being burdened by heavy NPU/TPU AI orchestration tasks.

### 2. Physical Detection (In-Game)
* **Mechanism:** Detector rails combined with 1-tick repeaters stabilize redstone pulses during high-speed minecart transits.
* **Trigger:** The stabilized pulse activates an adjacent Command Block (Impulse, Unconditional, Needs Redstone).

### 3. Telemetry Encapsulation
* **Action:** The Command Block executes a `tellraw` command.
* **Syntax Example:** `execute as @e[type=minecart,limit=1,sort=nearest] run tellraw @a {"text":"[TELEMETRY] NODE:CHONK-01 EVENT:CART_PASS DATA:SIGNAL_HIGH"}`
* **Purpose:** By using `tellraw`, the signal is written directly to the server log and RCON buffer without standard JVM or "Server" prefix clutter.

### 4. Local Bridge & Log Tailing
* **Service:** A Python/Go-based bridge script running locally on the Chonk host.
* **Action:** Tails `logs/latest.log` or monitors the active RCON stream for the `[TELEMETRY]` identifier.
* **Encapsulation:** Extracts metadata (NODE, EVENT, DATA) and wraps it into a network-routable JSON payload.

### 5. Network Transit & Stargate Ingestion
* **Transit:** The bridge script initiates asynchronous TCP/UDP socket communication to the Stargate host.
* **Ingestion:** The Stargate daemon listens on port 5005.
* **Execution:** Stargate maps the `CART_PASS` event to specific Model Context Protocol (MCP) handlers, allowing AI-driven manipulation of the world state (e.g., schematic injection) while ensuring boundary safety constraints are met.

### 6. Architectural Organization
* **Codebase:** Emphasize the `src/servers/chonk/` and `src/servers/stargate/` directory segregation.
* **Justification:** Keeps Hailo/Coral ML dependencies (Mendel Development Tool, .hef models) completely off the JVM-focused Chonk host, reducing overhead and limiting the attack surface.

## Proposed Slide Outline
1.  **Title Slide:** Bridging the Physical and Digital: AI Orchestration in Minecraft
2.  **System Topology:** Distributed nodes (Skynet, Stargate, Chonk, Edge-T)
3.  **Chonk Environment:** Debian Bookworm, Java 21, Paper/Forge
4.  **Physical Detection:** Redstone and 1-tick repeaters
5.  **Telemetry Encapsulation:** Command Blocks & `tellraw`
6.  **The Local Bridge:** Log tailing & JSON wrapping
7.  **Network Transit:** Asynchronous forwarding to Stargate
8.  **Stargate Ingestion:** Port 5005 & MCP Translation
9.  **Safe Schematic Deployment:** Intersection middleware
10. **Codebase Segregation:** `src/servers/chonk/` vs. `src/servers/stargate/`
11. **Future Hardware Acceleration:** TPU/NPU roadmap
12. **Questions & Discussion**

## Emerald Mirror & Slide Harvesting
* **Anecdote Vault:** Actively monitor for "teachable moments" and technical paradoxes within the Emerald Mirror pipeline (e.g., Block Update Cost (BUC) vs. 20 TPS).
* **Slide Generation Trigger:** Proactively suggest slide content for major Emerald Mirror milestones or complex concepts (e.g., "Abyss-Walking" design strategy).
* **Visual Standards:** Use high-contrast, modern CSS/HTML slide templates for technical breakdowns.

---
*Created for theDevilsVoice | Last Updated: May 8, 2026*
