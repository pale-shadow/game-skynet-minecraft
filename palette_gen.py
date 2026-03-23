import random

def get_neural_block(is_infected=False):
    """
    Returns a block ID based on v2.1 Void-Tech weighting.
    """
    if not is_infected:
        # Standard Void-Tech Bridge Weights
        weights = {
            "minecraft:polished_tuff": 60,
            "minecraft:calcite": 20,
            "minecraft:chiseled_tuff": 10,
            "minecraft:polished_tuff_bricks": 7,
            "minecraft:quartz_block": 3
        }
    else:
        # Aggressive Mutation (INTENSION_HIGH) Weights
        weights = {
            "minecraft:sculk": 40,
            "minecraft:crying_obsidian": 30,
            "minecraft:sculk_vein": 15,
            "minecraft:polished_tuff": 10,
            "minecraft:magenta_carpet": 5
        }

    blocks = list(weights.keys())
    probabilities = list(weights.values())
    return random.choices(blocks, weights=probabilities, k=1)[0]
