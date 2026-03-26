package main

import (
	"flag"
	"fmt"
	"log"
	"os"

	"github.com/pale-shadow/game-skynet-minecraft/internal/builders"
	"github.com/pale-shadow/game-skynet-minecraft/internal/minecraft"
)

func main() {
	// 1. Competition Flags
	hardware := flag.String("hardware", "hailo", "Target NPU: hailo, coral, or tinker")
	mode := flag.String("mode", "station", "Mode: station or weave")
	flag.Parse()

	fmt.Printf("🚀 Phase 2.1 Initiated | Hardware: %s | Mode: %s\n", *hardware, *mode)

	// 2. Initialize the Weaver with Hardware Context
	weaver := &builders.Weaver{
		Hardware:  *hardware,
		Threshold: 0.85, // Sensitivity for NPU aesthetic weighting
	}

	if *mode == "weave" {
		// Example: Connect Station 4478 to Tower 2196
		start := minecraft.Location{X: 100, Y: 70, Z: 100}
		end := minecraft.Location{X: 250, Y: 85, Z: 300}

		path, err := weaver.GenerateGridPath(start, end)
		if err != nil {
			log.Fatalf("Pathfinding failed on %s: %v", *hardware, err)
		}

		// Save unique schematic for this hardware's "Personality"
		schem := builders.BuildConduit(path)
		filename := fmt.Sprintf("GRID_%s_PERSONALITY.schem", *hardware)
		minecraft.SaveSchematic(schem, filename)
	}
}
