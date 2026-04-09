import numpy as np
import mcschematic

class T2BMExpander:
    """
    T2BM (Text-to-Building Minecraft) Expander logic for 'Void-Tech' urbanization.
    Translates high-level architectural intents into voxel-density structures.
    """

    PALETTE = {
        "foundation": "minecraft:deepslate_tiles",
        "framework": "minecraft:polished_tuff",
        "core": "minecraft:crying_obsidian",
        "detail": "minecraft:pearlescent_froglight",
        "accent": "minecraft:purpur_pillar",
        "glass": "minecraft:tinted_glass"
    }

    @staticmethod
    def generate(intent: str, coords: list, size: list):
        """
        Main entry point for generating a T2BM structure.
        """
        builder = T2BMExpander()
        schem = mcschematic.MCSchematic()
        
        if intent == "neural_anchor":
            return builder.build_neural_anchor(schem, coords, size)
        elif intent == "neural_vault":
            return builder.build_neural_vault(schem, coords, size)
        elif intent == "structural_frame":
            return builder.build_structural_frame(schem, coords, size)
        else:
            print(f"Unknown T2BM intent: {intent}")
            return schem

    def build_neural_anchor(self, schem, coords, size):
        """
        Builds a Neural Anchor: A stabilized core with external bracing.
        """
        w, h, l = size
        # 1. Foundation
        for x in range(w):
            for z in range(l):
                schem.setBlock((x, 0, z), self.PALETTE["foundation"])

        # 2. Structural Pillars (Rule of Three)
        for y in range(h):
            # Corners
            schem.setBlock((0, y, 0), self.PALETTE["framework"])
            schem.setBlock((w-1, y, 0), self.PALETTE["framework"])
            schem.setBlock((0, y, l-1), self.PALETTE["framework"])
            schem.setBlock((w-1, y, l-1), self.PALETTE["framework"])
            
            # Central Core (every 3rd block or central)
            if y > 0 and y < h - 1:
                schem.setBlock((w//2, y, l//2), self.PALETTE["core"])
                # Glow/Detail
                if y % 4 == 0:
                    schem.setBlock((w//2, y, l//2 - 1), self.PALETTE["detail"])
                    schem.setBlock((w//2, y, l//2 + 1), self.PALETTE["detail"])

        # 3. Accents / Girders
        for x in range(w):
            schem.setBlock((x, h-1, l//2), self.PALETTE["accent"] + "[axis=x]")
        
        return schem

    def build_neural_vault(self, schem, coords, size):
        """
        Builds a Neural Vault: A secure storage or data nexus.
        """
        w, h, l = size
        # Foundation and shell
        for x in range(w):
            for y in range(h):
                for z in range(l):
                    if y == 0:
                        schem.setBlock((x, y, z), self.PALETTE["foundation"])
                    elif x == 0 or x == w-1 or z == 0 or z == l-1 or y == h-1:
                        # Walls and Roof
                        if (x+y+z) % 5 == 0:
                            schem.setBlock((x, y, z), self.PALETTE["detail"])
                        else:
                            schem.setBlock((x, y, z), self.PALETTE["framework"])
                    else:
                        # Interior Core
                        if x == w//2 and z == l//2:
                            schem.setBlock((x, y, z), self.PALETTE["core"])
                        else:
                            schem.setBlock((x, y, z), "minecraft:air")
        return schem

    def build_structural_frame(self, schem, coords, size):
        """
        Builds just the structural frame for a future building.
        """
        w, h, l = size
        for y in range(h):
            for x in [0, w-1]:
                for z in [0, l-1]:
                    schem.setBlock((x, y, z), self.PALETTE["framework"])
            
            if y == 0 or y == h-1 or y == h//2:
                # Horizontal beams
                for x in range(w):
                    schem.setBlock((x, y, 0), self.PALETTE["framework"])
                    schem.setBlock((x, y, l-1), self.PALETTE["framework"])
                for z in range(l):
                    schem.setBlock((0, y, z), self.PALETTE["framework"])
                    schem.setBlock((w-1, y, z), self.PALETTE["framework"])
        return schem

def build_t2bm(schem, prompt):
    """
    Wrapper for generate_schematic.py to use the T2BMExpander.
    """
    intent = prompt.get("intent", "neural_anchor")
    dims = prompt.get("dimensions", {"width": 7, "height": 12, "length": 7})
    size = [dims.get("width", 7), dims.get("height", 12), dims.get("length", 7)]
    coords = [0, 0, 0] # Internal schematic coords
    
    expander = T2BMExpander()
    if intent == "neural_anchor":
        expander.build_neural_anchor(schem, coords, size)
    elif intent == "neural_vault":
        expander.build_neural_vault(schem, coords, size)
    elif intent == "structural_frame":
        expander.build_structural_frame(schem, coords, size)
    else:
        print(f"Unknown T2BM intent: {intent}")
    
    return schem

if __name__ == "__main__":
    # Test generation
    try:
        from skynet_core import Config
        output_dir = Config.SCHEM_DIR
    except ImportError:
        output_dir = "."

    expander = T2BMExpander()
    test_schem = expander.generate("neural_anchor", [0, 64, 0], [7, 12, 7])
    test_schem.save(output_dir, "test_t2bm_anchor", mcschematic.Version.JE_1_21_1)
    print(f"Test schematic 'test_t2bm_anchor.schem' generated in {output_dir}.")
