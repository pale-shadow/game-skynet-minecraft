package builders

import (
	"github.com/Tnze/go-mc/nbt"
	"github.com/Tnze/go-mc/level/schematic"
)

// BuildStation generates the v5 Industrial Station logic
func BuildStation(width, height, length int) *schematic.Schematic {
	schem := schematic.New(int16(width), int16(height), int16(length))

	// Define Palette Mapping
	// In Go, we map these to the Palette index in the schematic
	schem.Palette["minecraft:purpur_pillar[axis=y]"] = 1
	schem.Palette["minecraft:dark_prismarine"] = 2
	schem.Palette["minecraft:purpur_stairs[facing=north,half=bottom]"] = 3
	schem.Palette["minecraft:pearlescent_froglight"] = 4

	// 1. Foundation
	for x := 0; x < width; x++ {
		for z := 0; z < length; z++ {
			schem.SetBlock(x, 0, z, 1) // Using Purpur as base
		}
	}

	// 2. Fluted Pillar Logic (Indented 1,1)
	pillarLocs := [][]int{{1, 1}, {1, length - 2}, {width - 2, 1}, {width - 2, length - 2}}
	for _, loc := range pillarLocs {
		px, pz := loc[0], loc[1]
		for py := 1; py < height-2; py++ {
			// Central Core
			schem.SetBlock(px, py, pz, 1)
			// Fluting (Stairs) - simplified index call
			schem.SetBlock(px+1, py, pz, 3) 
		}
	}

	return schem
}
