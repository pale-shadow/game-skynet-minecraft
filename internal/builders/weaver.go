package builders

import (
	"encoding/json"
	"fmt"
	"math"
	"os/exec"
	"strings"

	"github.com/pale-shadow/game-skynet-minecraft/internal/minecraft"
)

type Node struct {
	X, Y, Z int
	G, H, F float64
	Parent  *Node
}

type Weaver struct {
	Config     string
	Threshold  float64
}

// GenerateGridPath connects two SKYNET landmarks (e.g. Station to Tower)
func (w *Weaver) GenerateGridPath(start, end minecraft.Location) ([]minecraft.Location, error) {
	openList := []Node{{X: start.X, Y: start.Y, Z: start.Z}}
	closedList := make(map[string]bool)

	for len(openList) > 0 {
		current := w.getLowestF(&openList)
		
		if w.dist(current, end) < 1.5 {
			return w.reconstruct(current), nil
		}

		closedList[w.key(current)] = true

		// 6-Directional search for conduit placement
		for _, neighbor := range w.getNeighbors(current) {
			if closedList[w.key(neighbor)] { continue }

			// NPU INFERENCE CALL
			// Weights the path to prefer "snapping" to existing structures
			npuWeight := w.getNPUAestheticWeight(neighbor)
			
			tentativeG := current.G + 1.0 + npuWeight
			if tentativeG < neighbor.G || !w.listContains(openList, neighbor) {
				neighbor.Parent = &current
				neighbor.G = tentativeG
				neighbor.H = w.heuristic(neighbor, end)
				neighbor.F = neighbor.G + neighbor.H
				openList = append(openList, neighbor)
			}
		}
	}
	return nil, fmt.Errorf("SIGNAL_LOST: No viable path for conduit")
}

func (w *Weaver) getNPUAestheticWeight(n Node) float64 {
	// Call the Python NPU Spatial Engine specifically for the Hailo-8L
	cmd := exec.Command("python3", "schematic-agent/npu_spatial_engine.py", 
		"--query", "traversability", 
		"--pos", fmt.Sprintf("%d,%d,%d", n.X, n.Y, n.Z))
	
	out, err := cmd.Output()
	if err != nil { return 5.0 } // Default penalty if NPU is busy
	
	// Implementation note: The NPU should return lower values for blocks 
	// adjacent to existing SKYNET walls to encourage "cable management" looks.
	return w.parseWeight(string(out))
}

func (w *Weaver) heuristic(n Node, target minecraft.Location) float64 {
	return math.Abs(float64(n.X-target.X)) + math.Abs(float64(n.Y-target.Y)) + math.Abs(float64(n.Z-target.Z))
}

// Helper methods: getLowestF, dist, key, getNeighbors, reconstruct...
