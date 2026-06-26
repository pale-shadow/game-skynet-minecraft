# note_block_registry.py
# Reference structure definitions for the Shroomville piano generation script

PIANO_MATERIAL_MAP = {
    "harp": "minecraft:oak_planks",       # Standard piano strings
    "bass_drum": "minecraft:stone",       # Kick drum accents
    "snare": "minecraft:sand",            # High crisp percussion lines
    "bass": "minecraft:oak_log",          # Deep string bass backing
    "bell": "minecraft:gold_block",       # Resonant melodic highlights
    "chime": "minecraft:packed_ice",      # Clean high-register tones
    "flute": "minecraft:clay",            # Pure wind emulation
    "guitar": "minecraft:white_wool",     # Mid-range acoustic modeling
    "xylophone": "minecraft:bone_block",  # High sharp staccato
    "iron_xylophone": "minecraft:iron_block" # Industrial metallic chime
}

def generate_piano_octave_delta(base_x, base_y, base_z, instrument="harp"):
    """
    Calculates exact spatial block coordinate deltas for an 8-key piano array.
    """
    support_block = PIANO_MATERIAL_MAP.get(instrument, "minecraft:oak_planks")
    schematic_payload = []
    
    # Generate sequential keys spaced along the X-axis
    for note_id in range(8):
        target_x = base_x + (note_id * 2)
        
        # Bottom Layer: Instrument timbre modifiers
        schematic_payload.append({
            "coords": (target_x, base_y, base_z),
            "block": support_block
        })
        # Top Layer: Dynamic Note Block with tuned pitch states [0-24]
        schematic_payload.append({
            "coords": (target_x, base_y + 1, base_z),
            "block": f"minecraft:note_block[note={note_id}]"
        })
        
    return schematic_payload
