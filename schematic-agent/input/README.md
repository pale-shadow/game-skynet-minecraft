# Skynet Architect (NPU-Driven Minecraft Architecture)

This directory contains the core logic for the **Skynet Architect** system, powered by a **Raspberry Pi 5 and Hailo-8L NPU**.

## Dual-Inference Architecture (Hailo-8L + USB TPU)

The project now utilizes a dual-inference model to manage complex world interactions:
- **`vision_lite_overseer.py`**: A simulated **USB Edge TPU** 'Visual Cortex' that scans for human incursions (Oak, Cobblestone, etc.).
- **`adaptive_mutation_v7.py`**: Executes the **v7.1-RECLAMATION** protocol, infecting detected human areas with Sculk and Crying Obsidian based on incursion scores.

### Key Logic:
- **`INTENSION_HIGH`**: Triggered when the TPU detects dense human activity. Leads to aggressive territory reclamation.
- **`CLASS_B_INCURSION`**: Triggers mycelial overgrowth to slowly assimilate the environment.

## Architectural Standard (v7+)
All builds adhere to the **"Void-Tech" Tier**:
- **Foundation**: Polished/Chiseled Tuff and Calcite.
- **Energy**: Crying Obsidian and Tinted Glass housing redstone cores.
- **Girders**: Dark Prismarine suspended via lightning rods and end rods.
- **Kinetic Logic**: Sculk Sensors linked to Copper Bulbs for proximity-based bioluminescence.
- **Economic Integration**: `minecraft:crafter` blocks ("Hydro-Pods") every 20m on all bridges.

## NPU Integration Details
The **Hailo-8L NPU** on the Raspberry Pi 5 is used to accelerate spatial density inference and pathfinding, allowing for complex, real-time architectural growth that adapts to existing world features.
