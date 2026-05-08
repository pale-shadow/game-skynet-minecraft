# Schematics & Emerald Mirror Pipeline

This directory is the operational hub for the **Emerald Mirror** project—a distributed AI pipeline that evolves the Bitsmasher Minecraft environment through context-aware architectural greebling.

## 🏛️ v5 Industrial Standards
To match the "Emerald Mirror" goals, all schematics must adhere to the following technical specifications:
*   **Voxel Density**: Minimum bounding box of $20 \times 15 \times 25$.
*   **Rule of Three**: Mandatory use of Base, Structural Pillar, and Accent Girder layers.
*   **Fluted Pillars**: 3x3 footprint utilizing `minecraft:purpur_pillar` cores.
*   **Industrial Lighting**: `minecraft:pearlescent_froglight` at girder intersections.

## 📊 Schematic Classification
Schematics are categorized into two types to support layered builds:
1.  **Foundation**: Core skeletal structures (Towers, Bridges, Hubs).
2.  **Delta**: AI-generated greebling layers that "wrap" around foundations.

**Mandatory Metadata**: Every `.schem` file must have a `.json` metadata file containing the `schematic_type` field.

## 🔄 Delivery Loop & Injection
Spatial data is processed via Vertex AI and the Edge-J Jetson cluster. Resulting deltas are pushed to the **chonk** server via automated RCON scripts.

### **Injection Throttling**
To maintain a stable **20 TPS server target**, all block injections must implement a **0.05s delay per block**.

## 🛠️ Procedural Generators
Active builders are documented in `src/schematics/GEMINI.md`.
- **`process_chronosplicer.py`**: Parses high-concept architectural prose into greebled JSON voxel maps.
- **`station2.py`**: High-fidelity industrial station builder.
- **`neural_bridge_v8_pathfinder.py`**: Intelligent rail link calculator.