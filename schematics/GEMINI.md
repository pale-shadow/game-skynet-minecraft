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

## v5 Architectural Standards (Industrial)

To match high-fidelity reference aesthetics, v5 schematics must adhere to the following technical specifications:

* **Voxel Density**: Minimum bounding box of $20 \times 15 \times 25$ to allow for geometric resolution of details.
* **Structural Depth**: Mandatory use of the "Rule of Three" (Base Layer, Structural Pillar Layer, and Accent Girder Layer) to prevent flat surfaces.
* **Fluted Pillars**: 3x3 footprint utilizing `minecraft:purpur_pillar[axis=y]` cores surrounded by oriented stairs for recessed shadowing.
* **Industrial Lighting**: Integration of `minecraft:pearlescent_froglight` within girder intersections to provide a native purple-white temperature glow.
* **Grid-Iron Girders**: Intersecting longitudinal and transverse beams using `dark_prismarine` and `warped_fences` for suspended structural realism.

## Technical Notes

* Uses the **Sponge Schematic v3** format (`.schem`) compatible with WorldEdit.
* **Block rotation system** (`blocks.py`) handles all facing/axis/half/hinge properties.
* **Registry Requirement**: All new builders must be mapped in `builders/__init__.py` under the `BUILDERS` dictionary to be accessible by the generator.

## Networked AI Infrastructure (MCP v1.5)

To coordinate decentralized processing, the system is segmented as follows:

- **Minecraft Server (`chonk`)**: `chonk.lab.bitsmasher.net` (`10.10.8.60`) - The destination for all generated builds.
- **AI Hardware (NPU Cluster)**: `10.10.16.10` - High-performance Pi 5 cluster with Hailo-8L NPUs for architectural inference.
- **Stargate MCP (Master Control)**: `10.10.16.66` - The primary server orchestrating all AI hardware and pushing build commands via RCON.