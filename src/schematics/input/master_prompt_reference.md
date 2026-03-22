# MC Schematics - Master JSON Prompt Reference Guide

This guide defines the JSON schema for generating Minecraft schematics (.schem) programmatically. Each JSON prompt file describes a structure to build — the generator reads it and produces a WorldEdit-compatible schematic.

## Quick Start

1. Create a `.json` file in `/prompts/` using the schema below
2. Run: `python scripts/generate_schematic.py prompts/my_build.json`
3. Find your `.schem` in `/output/<category>/`
4. Copy to `plugins/WorldEdit/schematics/` and `//schem load <name>` in-game

---

## The JSON Schema

```json
{
  "name": "string - Name of the schematic (used as filename)",
  "category": "string - Output subfolder: house, wall, tower, bridge, terrain, decoration, castle",
  "type": "string - Builder to use: house, wall, tower, bridge, terrain, decoration, castle",
  "version": "string - Minecraft version target, e.g. 'JE_1_20_4' (default: JE_1_20_4)",

  "dimensions": {
    "width": "integer - Size along X-axis",
    "height": "integer - Size along Y-axis (vertical)",
    "length": "integer - Size along Z-axis"
  },

  "materials": {
    "primary": "string - Main block, e.g. 'minecraft:stone_bricks'",
    "secondary": "string - Accent block, e.g. 'minecraft:dark_oak_planks'",
    "tertiary": "string - Third block for detail, e.g. 'minecraft:cobblestone'",
    "floor": "string - Floor material, e.g. 'minecraft:oak_planks'",
    "roof": "string - Roof material, e.g. 'minecraft:dark_oak_stairs'",
    "glass": "string - Window material, e.g. 'minecraft:glass_pane'",
    "door": "string - Door block, e.g. 'minecraft:oak_door'",
    "light": "string - Lighting block, e.g. 'minecraft:lantern'",
    "fence": "string - Fence/railing, e.g. 'minecraft:oak_fence'",
    "slab": "string - Slab variant, e.g. 'minecraft:stone_brick_slab'",
    "stairs": "string - Stair variant, e.g. 'minecraft:stone_brick_stairs'"
  },

  "features": {
    "has_roof": "boolean - Generate a roof (default: true for houses)",
    "roof_style": "string - flat, peaked, gabled, hip, dome",
    "has_floor": "boolean - Generate a floor (default: true)",
    "has_door": "boolean - Place a door (default: true for houses)",
    "door_position": "string - north, south, east, west",
    "has_windows": "boolean - Place windows (default: true for houses)",
    "window_spacing": "integer - Blocks between windows (default: 3)",
    "has_chimney": "boolean - Add a chimney (default: false)",
    "interior_lit": "boolean - Place interior light sources (default: true)",
    "has_foundation": "boolean - 1-block depth foundation (default: true)",
    "wall_thickness": "integer - Wall thickness in blocks (default: 1)",
    "hollow": "boolean - Make interior hollow (default: true for houses)",
    "crenellations": "boolean - Add castle-top crenellations (towers/castles)",
    "has_railing": "boolean - Add railings (bridges)",
    "arch_style": "string - none, pointed, round (bridges)",
    "fill_block": "string - Block to fill terrain with (terrain builder)",
    "surface_block": "string - Block for terrain surface (terrain builder)",
    "scatter_decorations": "boolean - Add random surface decorations like flowers (terrain)"
  },

  "decorations": [
    {
      "type": "string - torch, lantern, chest, crafting_table, bed, furnace, bookshelf, flower_pot, painting, banner, barrel, etc.",
      "position": "string - auto (builder decides), or specific: 'corners', 'center', 'walls'",
      "block": "string - Override the block used, e.g. 'minecraft:soul_lantern'"
    }
  ],

  "metadata": {
    "author": "string - Optional author name",
    "description": "string - Optional description of the build"
  }
}
```

---

## Supported Structure Types

### `house` — Houses & Cabins
Generates rectangular or square buildings with walls, floors, roofs, doors, and windows.

```json
{
  "name": "oak_cabin",
  "category": "house",
  "type": "house",
  "dimensions": { "width": 9, "height": 6, "length": 11 },
  "materials": {
    "primary": "minecraft:oak_log",
    "secondary": "minecraft:oak_planks",
    "floor": "minecraft:spruce_planks",
    "roof": "minecraft:dark_oak_stairs",
    "glass": "minecraft:glass_pane",
    "door": "minecraft:oak_door",
    "light": "minecraft:lantern"
  },
  "features": {
    "has_roof": true,
    "roof_style": "peaked",
    "has_door": true,
    "door_position": "south",
    "has_windows": true,
    "has_chimney": true,
    "interior_lit": true
  }
}
```

### `wall` — Walls & Fences
Generates straight walls or borders of configurable height and length.

```json
{
  "name": "stone_wall_20",
  "category": "wall",
  "type": "wall",
  "dimensions": { "width": 20, "height": 5, "length": 1 },
  "materials": {
    "primary": "minecraft:stone_bricks",
    "secondary": "minecraft:stone_brick_stairs",
    "slab": "minecraft:stone_brick_slab"
  },
  "features": {
    "crenellations": true
  }
}
```

### `tower` — Towers & Spires
Generates cylindrical or square towers with optional pointed roofs.

```json
{
  "name": "watchtower",
  "category": "tower",
  "type": "tower",
  "dimensions": { "width": 7, "height": 20, "length": 7 },
  "materials": {
    "primary": "minecraft:stone_bricks",
    "secondary": "minecraft:spruce_planks",
    "stairs": "minecraft:stone_brick_stairs",
    "glass": "minecraft:glass_pane",
    "light": "minecraft:torch"
  },
  "features": {
    "has_roof": true,
    "roof_style": "peaked",
    "hollow": true,
    "crenellations": true,
    "interior_lit": true
  }
}
```

### `bridge` — Bridges & Walkways
Generates arched or flat bridges with optional railings.

```json
{
  "name": "stone_arch_bridge",
  "category": "bridge",
  "type": "bridge",
  "dimensions": { "width": 5, "height": 8, "length": 25 },
  "materials": {
    "primary": "minecraft:stone_bricks",
    "secondary": "minecraft:stone_brick_slab",
    "fence": "minecraft:stone_brick_wall"
  },
  "features": {
    "has_railing": true,
    "arch_style": "round"
  }
}
```

### `terrain` — Terrain, Landscapes & Gardens
Generates shaped terrain blobs, hills, or flat gardens.

```json
{
  "name": "flower_garden",
  "category": "terrain",
  "type": "terrain",
  "dimensions": { "width": 15, "height": 3, "length": 15 },
  "features": {
    "fill_block": "minecraft:dirt",
    "surface_block": "minecraft:grass_block",
    "scatter_decorations": true
  }
}
```

### `decoration` — Interior Decoration & Furniture
Generates furniture groupings or decorative setups.

```json
{
  "name": "bedroom_set",
  "category": "decoration",
  "type": "decoration",
  "decorations": [
    { "type": "bed", "position": "center" },
    { "type": "chest", "position": "walls" },
    { "type": "lantern", "position": "corners" },
    { "type": "bookshelf", "position": "walls" }
  ]
}
```

### `castle` — Castles & Fortifications
Generates full castles with walls, towers at corners, and a courtyard.

```json
{
  "name": "small_keep",
  "category": "castle",
  "type": "castle",
  "dimensions": { "width": 25, "height": 12, "length": 25 },
  "materials": {
    "primary": "minecraft:stone_bricks",
    "secondary": "minecraft:mossy_stone_bricks",
    "tertiary": "minecraft:cracked_stone_bricks",
    "floor": "minecraft:stone",
    "stairs": "minecraft:stone_brick_stairs",
    "slab": "minecraft:stone_brick_slab",
    "light": "minecraft:torch",
    "fence": "minecraft:stone_brick_wall"
  },
  "features": {
    "crenellations": true,
    "has_floor": true,
    "interior_lit": true
  }
}
```

---

## Block ID Reference

All block IDs use the modern **namespaced** format: `minecraft:<block_name>`. Block states go in brackets:

| Block | ID |
|-------|-----|
| Stone | `minecraft:stone` |
| Stone Bricks | `minecraft:stone_bricks` |
| Oak Planks | `minecraft:oak_planks` |
| Oak Log (Y-axis) | `minecraft:oak_log[axis=y]` |
| Oak Log (X-axis) | `minecraft:oak_log[axis=x]` |
| Oak Stairs (East) | `minecraft:oak_stairs[facing=east]` |
| Oak Slab (Bottom) | `minecraft:oak_slab[type=bottom]` |
| Oak Slab (Top) | `minecraft:oak_slab[type=top]` |
| Glass Pane | `minecraft:glass_pane` |
| Oak Door (Lower) | `minecraft:oak_door[half=lower,facing=south]` |
| Oak Door (Upper) | `minecraft:oak_door[half=upper,facing=south]` |
| Torch | `minecraft:torch` |
| Wall Torch (South) | `minecraft:wall_torch[facing=south]` |
| Lantern | `minecraft:lantern` |
| Lantern (Hanging) | `minecraft:lantern[hanging=true]` |
| Cobblestone | `minecraft:cobblestone` |
| Grass Block | `minecraft:grass_block` |
| Dirt | `minecraft:dirt` |
| Oak Fence | `minecraft:oak_fence` |
| Iron Bars | `minecraft:iron_bars` |
| Chest | `minecraft:chest[facing=south]` |
| Crafting Table | `minecraft:crafting_table` |
| Furnace | `minecraft:furnace[facing=south]` |
| Bed (Head) | `minecraft:red_bed[facing=south,part=head]` |
| Bed (Foot) | `minecraft:red_bed[facing=south,part=foot]` |
| Bookshelf | `minecraft:bookshelf` |
| Cobblestone Wall | `minecraft:cobblestone_wall` |
| Stone Brick Wall | `minecraft:stone_brick_wall` |
| Air | `minecraft:air` |

### Stair Facing Values
Stairs use `facing` (north/south/east/west) and `half` (top/bottom):
- `minecraft:oak_stairs[facing=south,half=bottom]`

### Log Axis Values
Logs use `axis` (x/y/z):
- `minecraft:oak_log[axis=y]` — vertical
- `minecraft:oak_log[axis=x]` — east-west
- `minecraft:oak_log[axis=z]` — north-south

---

## Tips

1. **Keep it simple** — Start with basic dimensions and materials, add features incrementally.
2. **Test small** — Build a 5x5x5 test before a 50x50x50 castle.
3. **Namespaced IDs** — Always use `minecraft:` prefix. Check [Minecraft Wiki](https://minecraft.wiki/w/Java_Edition_data_values#Blocks) for valid IDs.
4. **Drop unused fields** — Only include what you need; the builders use sensible defaults.
5. **Coordinates are relative** — `(0,0,0)` is the paste origin point in WorldEdit.
