The **MC Schematics - Gemini Project Organizer** (`gemini.md`) has been updated to reflect the integration of the `station2.py` builder and the elevated architectural standards required for v5-tier schematics.

### Updated `gemini.md`

# MC Schematics - Gemini Project Organizer

This document tracks progress, generated schematics, and custom scripts for the Minecraft Schematic generation project using Anti-Gravity.

## Project Structure

It is critical to **always keep prompts and schematics organized** within the project directory.

- `/prompts/` - JSON prompt configurations describing structures to generate.
- `/output/` - All generated `.schem` files are saved here (flat, no subfolders).
- `/scripts/` - Core generation engine and utility scripts.
- `/scripts/builders/` - Modular builder functions for different structure types.

## Schematic Generation Workflow

1. Create a JSON prompt file in `/prompts/`.
2. Run the generator: `python scripts/generate_schematic.py prompts/my_build.json`.
3. Output `.schem` files appear in `/output/`.

## Scripts Log

| Script Name | Purpose | Status |
| :--- | :--- | :--- |
| `scripts/builders/station2.py` | **New:** High-fidelity industrial station builder featuring fluted pillars, grid-iron girders, and integrated lighting. | **Active** |
| `scripts/builders/house.py` | House/cabin structure builder. | Active |
| `scripts/builders/interiors.py` | Interior furnishing system and room templates. | Active |
| `scripts/builders/bank.py` | Grand bank builder with full interior. | Active |

## v5 & Emerald Mirror Architectural Standards

To match high-fidelity reference aesthetics and the "Emerald Mirror" project goals, schematics must adhere to the following:

* **Emerald Mirror Mutation:** Transitioning from procedural generation to context-aware greebling and spatial mutation. Ingest spatial voxel snapshots and output highly detailed, structurally complex updates.
* **Greebling Density**: Minimum bounding box of $20 \times 15 \times 25$ with high visual density. Functional logic (pipes connect to ports, vents face outward) mixed with microscopic detailing (rivets, seams).
* **Voxel Density**: Minimum bounding box of $20 \times 15 \times 25$ to allow for geometric resolution of details, while preventing excessively large or dense structures that could impact TPS.
* **Structural Depth**: Mandatory use of the "Rule of Three" (Base Layer, Structural Pillar Layer, and Accent Girder Layer) to prevent flat surfaces.
* **Fluted Pillars**: 3x3 footprint utilizing `minecraft:purpur_pillar[axis=y]` cores surrounded by oriented stairs for recessed shadowing.
* **Industrial Lighting**: Integration of `minecraft:pearlescent_froglight` within girder intersections for a native purple-white temperature glow.
* **Grid-Iron Girders**: Intersecting longitudinal and transverse beams using `dark_prismarine` and `warped_fences`.

## Debugging & Health Check

- **Emerald Mirror Pipeline:** (Active) Spatial snapshots are being routed via Stargate to Skynet for Vertex AI mutation. Resulting `.schem` deltas are pushed to Chonk via automated pipeline tasks.
- **Robust Deployment & Validation:** The schematic generation and deployment pipeline (including `skynet_core.py` and `skynet_unified.py`) is fully operational. It includes comprehensive build metadata storage and pre-deployment 3D AABB overlap detection.
- **NFS Mount Standardization:** All schematic and metadata storage is standardized to the `/mnt/clusterfs/minecraft/schematics` NFS mount.
- **Documentation Audit:** (May 8, 2026) Updated all GEMINI.md files to reflect the Emerald Mirror project pivot.
- **Announcement & Logging Standards**: Implemented mandatory coordinate and name reporting for all builds.
- **Hardware Status**: Confirmed Hailo-8L NPU is operational for spatial inference; Edge TPU for aesthetic validation.

## Technical Notes

* Uses the **Sponge Schematic v3** format (`.schem`) compatible with WorldEdit.
* **Block rotation system** (`blocks.py`) handles all facing/axis/half/hinge properties.
* **Registry Requirement**: All new builders must be mapped in `builders/__init__.py`.
* **Security & Environment**: Use `direnv` for `RCON_PASS`. Never hardcode credentials.

## Networked AI Infrastructure (Emerald Cluster)

- **Minecraft Server (`chonk`)**: `10.10.8.60` - Target for spatial injections.
- **Skynet Core (Orchestrator)**: `10.10.16.10` - Central node for spatial analysis and Vertex AI coordination.
- **AI Hardware (NPU Cluster)**: `10.10.16.10` - Hailo-8L NPUs for architectural inference.
- **Vision Overseer (Edge TPU)**: `10.10.16.4` - Aesthetic validation and mutation scans.
- **Stargate MCP (Master Control)**: `10.10.16.66` - API bridge between LLM logic and RCON deployment tools.
---
*Created for theDevilsVoice | Last Updated: May 8, 2026*
