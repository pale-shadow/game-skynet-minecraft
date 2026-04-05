# Modular builder functions for different structure types
from .bank import build_bank
from .bridge import build_bridge
from .castle import build_castle
from .cyberdyne import build_cyberdyne
from .decoration import build_decoration
from .house import build_house
from .primitives import *
from .station2 import build as build_station
from .terrain import build_terrain
from .tower import build_tower
from .wall import build_wall

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
