# Schematics & Procedural Generation

This directory contains legacy schematics and the newer **Skynet Procedural Generators** for the 2026 "Void-Tech" era.

- [I like this tool craftmatic](https://github.com/tribixbite/craftmatic)

## Procedural Generators (Skynet v7+)
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
The 2026 architecture combines **pre-built schematics** with **NPU-driven procedural logic** to create an evolving, reactive environment in the AI Testing Field.