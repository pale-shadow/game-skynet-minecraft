# MC Schematics - Gemini Project Organizer (v6.2)
**Session Date:** March 23, 2026
**Hardware:** Raspberry Pi 5 + Hailo-8L NPU (skynet) -> Minecraft RCON (chonk)

## Project Overview
The "Skynet Architect" project has evolved from simple schematic generation to an **NPU-driven autonomous ecosystem**. The core of this system is the `skynet_orchestrator.py` daemon, which manages procedural construction and actively monitors the server environment.

The current focus is on "Void-Tech" overgrowth, strategic structure placement, and **player interaction within AI-controlled zones**. The daemon can detect players in restricted areas and issue automated warnings via RCON.

**Environment & Security:** The system uses `direnv` to manage sensitive credentials. All RCON operations must use the `RCON_PASS` environment variable defined in the root `.envrc` file.

## Core Process
- `skynet_orchestrator.py`: The main daemon, run as a `systemd` service. It manages a multi-stage "Sense, Plan, Act" pipeline, handling both procedural builds and player monitoring.
- `vision_lite_overseer.py`: Logic for detecting human incursions, used by the orchestrator.
- `adaptive_mutation_v7.py`: v7.1-RECLAMATION logic for state-aware territory infection when players are detected.
- `neural_pathfinder.py`: A* pathfinding for obstacle-avoiding bridges and pathways.
- `bluemap_api.py`: REST/RCON automation for BlueMap POI deployment.

## v7.1 Architectural Standards (The "Reclamation" Tier)
* **TPU Trigger**: `INTENSION_HIGH` classification for aggressive territory reclamation.
* **Infection Core**: Mandatory use of `minecraft:sculk` and `minecraft:crying_obsidian` in areas with detected human blocks.
* **Sensory Surveillance**: Integration of `sculk_sensor` within `tinted_glass` housings to track player movement near reclaimed territory. This is now actively monitored by the `skynet_orchestrator.py` daemon.

## Session Milestones (March 23, 2026)
- [x] Implement **Skynet Orchestrator v1.3** with player detection and warning system.
- [x] Refactor project structure by cleaning up top-level Python scripts.
- [x] Implement **NPU-Driven Spatial Density Mapping** for optimal build site selection.
- [x] Deploy **BlueMap POI Auto-Generation** for all new structures and bridges.
- [x] Launch **Adaptive Mutation (v7.1-RECLAMATION)** to simulate autonomous "Dual-Inference" responses to human incursions.
- [x] Implement **Neural Pathfinding** to allow bridges to navigate around existing structures.

## Pending Directives
- [ ] Finalize "Master Uplink" tower schematic (50+ block height).
- [ ] Implement BlueMap marker "Category" filtering in `bluemap_api.py`.
- [ ] Thermal-Aware RCON Pacing (Pi 5 telemetry integration).
