# Schematics & Procedural Generation

This directory contains legacy schematics and the newer **Skynet Procedural Generators** for the 2026 "Void-Tech" era.

- [I like this tool craftmatic](https://github.com/tribixbite/craftmatic)

## Procedural Generators (Skynet v7+)
The Skynet system now includes various modular builder functions for different structure types (e.g., high-fidelity industrial stations, houses, interiors, banks). For a comprehensive and up-to-date list of active builders, refer to `schematics/GEMINI.md`.
- **`neural_rail_v7_nexus.py`**: Procedurally generates logistics hubs with ribbed geometry.
- **`neural_bridge_v8_pathfinder.py`**: Dynamically calculates and builds intelligent rail links.
- **`generate_signal_core.py`**: Python-based generator for "Signal Core" data hubs.

## Legacy Schematics (WorldEdit)
Legacy schematics are located in `schem_files/` and can be loaded via WorldEdit.

### Installing Schematics
- Place `.schem` or `.schematic` files in `/home/minecraft/minecraft/config/worldedit/schematics`.
- Run `/schem load <name>` in-game.
- Run `//paste` to deploy.

## Go Tools (Legacy Generation)
The project originally used Go for large-scale schematic handling:
```sh
mkdir -p ~/src/schematic-go
cd ~/src/schematic-go
go mod init github.com/chonk/minecraft-station
go get github.com/Tnze/go-mc@master
```

## Hybrid Workflow
The 2026 architecture combines **pre-built schematics** with **NPU-driven procedural logic** to create an evolving, reactive environment in the AI Testing Field. This now includes robust pre-deployment 3D AABB overlap detection (`schematics/validate_no_overlaps.py`) to ensure structural integrity and prevent conflicting builds.

## v5 Architectural Standards (Industrial)
To match high-fidelity reference aesthetics, v5 schematics must adhere to the following technical specifications:
*   **Voxel Density**: Minimum bounding box of $20 \times 15 \times 25$.
*   **Structural Depth**: Mandatory use of the "Rule of Three" (Base Layer, Structural Pillar Layer, and Accent Girder Layer).
*   **Fluted Pillars**: 3x3 footprint utilizing `minecraft:purpur_pillar[axis=y]` cores.
*   **Industrial Lighting**: Integration of `minecraft:pearlescent_froglight` within girder intersections.
*   **Grid-Iron Girders**: Intersecting longitudinal and transverse beams using `dark_prismarine` and `warped_fences`.