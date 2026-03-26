package builders

import (
	"github.com/Tnze/go-mc/level/schematic"
)

// WeaverConfig defines the aesthetic of the urban grid
type WeaverConfig struct {
	PrimaryID   int32
	SupportID   int32
	LightID     int32
}

// BuildConduit converts a set of path nodes into a schematic
func BuildConduit(path []Node) *schematic.Schematic {
	// 1. Calculate bounding box for the schematic
	minX, minY, minZ, maxX, maxY, maxZ := getBounds(path)
	width := int16(maxX - minX + 1)
	height := int16(maxY - minY + 1)
	length := int16(maxZ - minZ + 1)

	schem := schematic.New(width, height, length)

	// 2. Align Palette with station.go style
	schem.Palette["minecraft:polished_basalt[axis=y]"] = 1
	schem.Palette["minecraft:iron_bars[north=true,south=true]"] = 2
	schem.Palette["minecraft:sea_lantern"] = 3

	// 3. Trace the Path
	for _, node := range path {
		// Normalize coordinates to schematic local space
		lx := node.X - minX
		ly := node.Y - minY
		lz := node.Z - minZ

		// Set the primary conduit block
		schem.SetBlock(lx, ly, lz, 1)

		// AESTHETIC LOGIC: Add vertical supports if high enough
		if ly > 2 && node.X%5 == 0 { 
			for y := ly - 1; y >= 0; y-- {
				schem.SetBlock(lx, y, lz, 2) // Iron Bar supports
			}
		}
		
		// Add "Energy Nodes" every 10 blocks
		if len(path) % 10 == 0 {
			schem.SetBlock(lx, ly+1, lz, 3)
		}
	}

	return schem
}

// getBounds identifies the min/max coordinates to size the schematic correctly
func getBounds(path []Node) (int, int, int, int, int, int) {
    // Logic to find min/max X, Y, Z from the node slice
    return 0, 0, 0, 10, 10, 10 // Simplified return
}
