"""
blocks.py — Block orientation and rotation utilities.

Provides helper functions that return properly formatted block state strings
with correct facing, axis, half, and other blockstate properties.
Every builder should use these instead of hand-writing block strings.
"""

# ── Direction Utilities ─────────────────────────────────────────────
CARDINALS = ["north", "east", "south", "west"]


def opposite(facing):
    return CARDINALS[(CARDINALS.index(facing) + 2) % 4]


def cw(facing):
    return CARDINALS[(CARDINALS.index(facing) + 1) % 4]


def ccw(facing):
    return CARDINALS[(CARDINALS.index(facing) - 1) % 4]


# ── Stair / Slab / Log helpers ──────────────────────────────────────
def stair(mat, facing="south", half="bottom", shape="straight"):
    base = mat if ":" in mat else f"minecraft:{mat}_stairs"
    return f"{base}[facing={facing},half={half},shape={shape}]"


def slab(mat, typ="bottom"):
    base = mat if ":" in mat else f"minecraft:{mat}_slab"
    return f"{base}[type={typ}]"


def log(mat, axis="y"):
    base = mat if ":" in mat else f"minecraft:{mat}_log"
    return f"{base}[axis={axis}]"


def wood(mat, axis="y"):
    base = mat if ":" in mat else f"minecraft:{mat}_wood"
    return f"{base}[axis={axis}]"


def pillar(mat, axis="y"):
    """Quartz pillar or similar pillared block."""
    base = mat if ":" in mat else f"minecraft:{mat}"
    return f"{base}[axis={axis}]"


# ── Doors / Trapdoors / Gates ───────────────────────────────────────
def door(mat, facing="south", half="lower", hinge="left"):
    base = mat if ":" in mat else f"minecraft:{mat}_door"
    return f"{base}[facing={facing},half={half},hinge={hinge}]"


def iron_door(facing="south", half="lower", hinge="left"):
    return f"minecraft:iron_door[facing={facing},half={half},hinge={hinge}]"


def trapdoor(mat, facing="south", half="bottom", open_state=False):
    base = mat if ":" in mat else f"minecraft:{mat}_trapdoor"
    o = "true" if open_state else "false"
    return f"{base}[facing={facing},half={half},open={o}]"


def iron_trapdoor(facing="south", half="bottom", open_state=False):
    o = "true" if open_state else "false"
    return f"minecraft:iron_trapdoor[facing={facing},half={half},open={o}]"


def fence(mat):
    return mat if ":" in mat else f"minecraft:{mat}_fence"


def fence_gate(mat, facing="south", open_state=False):
    base = mat if ":" in mat else f"minecraft:{mat}_fence_gate"
    o = "true" if open_state else "false"
    return f"{base}[facing={facing},open={o}]"


# ── Lighting ────────────────────────────────────────────────────────
def lantern(hanging=False):
    h = "true" if hanging else "false"
    return f"minecraft:lantern[hanging={h}]"


def soul_lantern(hanging=False):
    h = "true" if hanging else "false"
    return f"minecraft:soul_lantern[hanging={h}]"


def wall_torch(facing="south"):
    return f"minecraft:wall_torch[facing={facing}]"


def soul_wall_torch(facing="south"):
    return f"minecraft:soul_wall_torch[facing={facing}]"


def chain(axis="y"):
    return f"minecraft:chain[axis={axis}]"


# ── Containers / Functional ─────────────────────────────────────────
def chest(facing="south"):
    return f"minecraft:chest[facing={facing}]"


def trapped_chest(facing="south"):
    return f"minecraft:trapped_chest[facing={facing}]"


def barrel(facing="up"):
    return f"minecraft:barrel[facing={facing}]"


def furnace(facing="south", lit=False):
    l = "true" if lit else "false"
    return f"minecraft:furnace[facing={facing},lit={l}]"


def smoker(facing="south", lit=False):
    l = "true" if lit else "false"
    return f"minecraft:smoker[facing={facing},lit={l}]"


def blast_furnace(facing="south", lit=False):
    l = "true" if lit else "false"
    return f"minecraft:blast_furnace[facing={facing},lit={l}]"


# ── Decorative ──────────────────────────────────────────────────────
def bed(color="red", facing="south", part="foot"):
    return f"minecraft:{color}_bed[facing={facing},part={part}]"


def banner(color="white", rotation=0):
    return f"minecraft:{color}_banner[rotation={rotation}]"


def wall_banner(color="white", facing="south"):
    return f"minecraft:{color}_wall_banner[facing={facing}]"


def carpet(color="red"):
    return f"minecraft:{color}_carpet"


def wall_sign(mat, facing="south"):
    base = mat if ":" in mat else f"minecraft:{mat}_wall_sign"
    return f"{base}[facing={facing}]"


def button(mat, facing="south", face="wall"):
    base = mat if ":" in mat else f"minecraft:{mat}_button"
    return f"{base}[facing={facing},face={face}]"


def pressure_plate(mat):
    return mat if ":" in mat else f"minecraft:{mat}_pressure_plate"


def glazed_terracotta(color, facing="south"):
    return f"minecraft:{color}_glazed_terracotta[facing={facing}]"


# ── Common block constants ──────────────────────────────────────────
AIR = "minecraft:air"
STONE = "minecraft:stone"
STONE_BRICKS = "minecraft:stone_bricks"
MOSSY_STONE_B = "minecraft:mossy_stone_bricks"
CRACKED_STONE_B = "minecraft:cracked_stone_bricks"
CHISELED_STONE_B = "minecraft:chiseled_stone_bricks"
SMOOTH_STONE = "minecraft:smooth_stone"
COBBLESTONE = "minecraft:cobblestone"
BRICKS = "minecraft:bricks"
POLISHED_ANDESITE = "minecraft:polished_andesite"
POLISHED_GRANITE = "minecraft:polished_granite"
POLISHED_DIORITE = "minecraft:polished_diorite"
POLISHED_DEEPSLATE = "minecraft:polished_deepslate"
DEEPSLATE_BRICKS = "minecraft:deepslate_bricks"
DEEPSLATE_TILES = "minecraft:deepslate_tiles"
QUARTZ_BLOCK = "minecraft:quartz_block"
SMOOTH_QUARTZ = "minecraft:smooth_quartz"
QUARTZ_BRICKS = "minecraft:quartz_bricks"
QUARTZ_PILLAR = "minecraft:quartz_pillar"
CHISELED_QUARTZ = "minecraft:chiseled_quartz_block"
IRON_BLOCK = "minecraft:iron_block"
GOLD_BLOCK = "minecraft:gold_block"
DIAMOND_BLOCK = "minecraft:diamond_block"
EMERALD_BLOCK = "minecraft:emerald_block"
BOOKSHELF = "minecraft:bookshelf"
CRAFTING_TABLE = "minecraft:crafting_table"
ENCHANTING_TABLE = "minecraft:enchanting_table"
ANVIL = "minecraft:anvil"
CAULDRON = "minecraft:cauldron"
BREWING_STAND = "minecraft:brewing_stand"
JUKEBOX = "minecraft:jukebox"
REDSTONE_BLOCK = "minecraft:redstone_block"
REDSTONE_LAMP = "minecraft:redstone_lamp"
REDSTONE_WIRE = "minecraft:redstone_wire"
GLOWSTONE = "minecraft:glowstone"
SEA_LANTERN = "minecraft:sea_lantern"
SHROOMLIGHT = "minecraft:shroomlight"
TORCH = "minecraft:torch"
IRON_BARS = "minecraft:iron_bars"
GLASS = "minecraft:glass"
GLASS_PANE = "minecraft:glass_pane"
OAK_PLANKS = "minecraft:oak_planks"
SPRUCE_PLANKS = "minecraft:spruce_planks"
DARK_OAK_PLANKS = "minecraft:dark_oak_planks"
BIRCH_PLANKS = "minecraft:birch_planks"
POTTED_FERN = "minecraft:potted_fern"
POTTED_OAK = "minecraft:potted_oak_sapling"
POTTED_POPPY = "minecraft:potted_poppy"
POTTED_AZALEA = "minecraft:potted_azalea_bush"
POTTED_CACTUS = "minecraft:potted_cactus"
FLOWER_POT = "minecraft:flower_pot"
