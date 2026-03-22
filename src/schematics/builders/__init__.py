# Modular builder functions for different structure types
from .primitives import *
from .house import build_house
from .wall import build_wall
from .tower import build_tower
from .bridge import build_bridge
from .terrain import build_terrain
from .decoration import build_decoration
from .castle import build_castle
from .bank import build_bank
from .cyberdyne import build_cyberdyne
from .station2 import build as build_station

BUILDERS = {
    "house": build_house,
    "wall": build_wall,
    "tower": build_tower,
    "bridge": build_bridge,
    "terrain": build_terrain,
    "decoration": build_decoration,
    "castle": build_castle,
    "bank": build_bank,
    "cyberdyne": build_cyberdyne,
    "station": build_station,  # ADD THIS LINE
}
