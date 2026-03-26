package builders

import (
	"fmt"
	"math"
	"os/exec"
	"strconv"
	"strings"

	"github.com/pale-shadow/game-skynet-minecraft/internal/minecraft"
)

// Node represents a 3D coordinate in the pathfinding grid
type Node struct {
	X, Y, Z int
	G, H, F float64
	Parent  *Node
}

// Weaver handles the high-density connectivity between SKYNET modules
type Weaver struct {
	ConfigPath string
	TPSGuard   float64
}

// GenerateGridPath initiates the A* search with NPU-weighted heuristics
func (w *Weaver) GenerateGridPath(start, end minecraft.Location) ([]minecraft.Location, error) {
	// Pre-flight check: Ensure 24G Heap is stable and TPS is > 19.5
	if !w.checkServerHealth() {
		return nil, fmt.Errorf("STABILITY_RISK: TPS below threshold")
	}

	openList := []Node{{X: start.X, Y: start.Y, Z: start.Z}}
	closedList := make(map[string]bool)

	for len(openList) > 0 {
		// Pop node with lowest F cost
		current := w.getLowestF(&openList)
		
		// Target Reached
		if w.isAtTarget(current, end) {
			return w.reconstructPath(current), nil
		}

		closedList[w.coordKey(current.X, current.Y, current.Z)] = true

		// Neighbors: Standard 6-way adjacency (Up, Down, North, South, East, West)
		for _, next := range w.getNeighbors(current) {
			if closedList[w.coordKey(next.X, next.Y, next.Z)] {
				continue
			}

			// NPU INFERENCE: Call Python NPU Spatial Engine for aesthetic weighting
			// This prevents the weaver from floating conduits mid-air
			npuWeight := w.getNPUWeight(next)

			tentativeG := current.G + 1.0 + npuWeight
			
			if w.shouldUpdatePath(next, tentativeG, openList) {
				next.Parent = &current
				next.G = tentativeG
				next.H = w.heuristic(next, end)
				next.F = next.G + next.H
				openList = append(openList, next)
			}
		}
	}

	return nil, fmt.Errorf("PATH_NOT_FOUND: Spatial occlusion detected")
}

// getNPUWeight interfaces with schematic-agent/n
