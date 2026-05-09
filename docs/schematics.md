# Schematic Standards & Emerald Mirror Pipeline

This document formalizes the architectural and technical standards for Minecraft schematics within the Bitsmasher network, specifically for the **v5 Industrial** era.

## 🏛️ v5 Industrial Aesthetic
Transitioning away from mycelial growth, the v5 standard prioritizes industrial complexity and structural depth.

### **Official Palette**
- **Primary Support:** `minecraft:purpur_pillar` (3x3 fluted cores)
- **Structural Accents:** `minecraft:dark_prismarine` (grid-iron girders)
- **Industrial Lighting:** `minecraft:pearlescent_froglight` (integrated intersections)
- **Temporal Details:** `minecraft:waxed_copper_block` and variants.
- **Foundations:** `minecraft:polished_deepslate_bricks` and `polished_andesite`.

### **Architectural Specifications**
- **Greebling Density**: Minimum bounding box of $20 \times 15 \times 25$ with high visual density.
- **Rule of Three**: All builds must feature a distinct Base Layer, Structural Pillar Layer, and Accent Girder Layer to prevent flat surfaces.
- **Fluted Pillars**: 3x3 footprint utilizing vertical pillar cores surrounded by oriented stairs for recessed shadowing.

## 🔄 The Emerald Mirror Pipeline
A four-stage distributed process for world evolution:

1.  **Inference (Stargate Hub-01):** Ollama/Vertex AI generates high-concept architectural instructions from spatial snapshots.
2.  **Refinement (Jetson Cluster Edge-J):** CUDA-accelerated nodes convert abstract instructions into precise block coordinate deltas (Heavy Voxel Math).
3.  **Validation (Skynet Hub-00):** Hailo-8L NPU performs a boundary safety and structural integrity audit.
4.  **Injection (Stargate Hub-01):** Validated deltas are pushed to the target server (chonk) via RCON with asynchronous throttling.

## 📊 Metadata & Schematic Types
Every schematic must include a corresponding `.json` metadata file.

### **Schematic Types**
- **Foundation Schematics**: Core structural elements (e.g., towers, bridge foundations). These are the skeletal "Anchors."
- **Delta Schematics**: AI-generated aesthetic layers (greebles). These contain high percentages of Air blocks and "wrap" around foundations.

### **Mandatory Metadata Fields**
To prevent safety interlocks from clearing existing structures, the `schematic_type` field is mandatory:
```json
{
  "build_id": "example_build_01",
  "schematic_type": "Foundation",
  "spatial_data": {
    "origin": {"x": 0, "y": 63, "z": 0},
    "dimensions": {"width": 20, "height": 15, "length": 25}
  }
}
```
*Valid `schematic_type` values: `Foundation`, `Delta`.*
