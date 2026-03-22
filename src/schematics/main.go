package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/Tnze/go-mc/nbt"
)

// Sponge V3 Schematic Structure
type Schematic struct {
	Version     int32          `nbt:"Version"`
	DataVersion int32          `nbt:"DataVersion"`
	Width       int16          `nbt:"Width"`
	Height      int16          `nbt:"Height"`
	Length      int16          `nbt:"Length"`
	Palette     map[string]int32 `nbt:"Palette"`
	BlockData   []byte         `nbt:"BlockData"` // Varint encoded
}

type Prompt struct {
	Name       string            `json:"name"`
	Type       string            `json:"type"`
	Dimensions struct {
		Width  int `json:"width"`
		Height int `json:"height"`
		Length int `json:"length"`
	} `json:"dimensions"`
	Palette map[string]string `json:"palette"`
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Usage: ./schem-gen <path_to_json_or_dir>")
	}

	target := os.Args[1]
	fi, err := os.Stat(target)
	if err != nil {
		log.Fatal(err)
	}

	if fi.IsDir() {
		files, _ := ioutil.ReadDir(target)
		for _, f := range files {
			if strings.HasSuffix(f.Name(), ".json") {
				processFile(filepath.Join(target, f.Name()))
			}
		}
	} else {
		processFile(target)
	}
}

func processFile(path string) {
	plan, _ := ioutil.ReadFile(path)
	var p Prompt
	json.Unmarshal(plan, &p)

	// Initialize Schematic
	s := Schematic{
		Version:     3,
		DataVersion: 3953,
		Width:       int16(p.Dimensions.Width),
		Height:      int16(p.Dimensions.Height),
		Length:      int16(p.Dimensions.Length),
		Palette:     make(map[string]int32),
	}

	totalBlocks := int(s.Width) * int(s.Height) * int(s.Length)
	s.BlockData = make([]byte, totalBlocks)

	// Route to Builder
	if p.Type == "station" {
		generateStation(&s, p)
	} else {
		// Default to filling with primary block
		idx := int32(0)
		s.Palette[p.Palette["primary"]] = idx
		for i := range s.BlockData {
			s.BlockData[i] = byte(idx)
		}
	}

	// Save
	outName := strings.TrimSuffix(filepath.Base(path), ".json") + ".schem"
	f, _ := os.Create("output/" + outName)
	defer f.Close()

	nbt.NewEncoder(f).Encode(struct {
		Schematic Schematic `nbt:"Schematic"`
	}{Schematic: s}, "")

	fmt.Printf("✔ Generated: %s\n", outName)
}

func generateStation(s *Schematic, p Prompt) {
    w, h, l := int(s.Width), int(s.Height), int(s.Length)
    
    // Helper to set blocks by name
    setBlock := func(x, y, z int, blockName string) {
        if x < 0 || x >= w || y < 0 || y >= h || z < 0 || z >= l {
            return
        }
        
        // Ensure block is in palette
        idx, exists := s.Palette[blockName]
        if !exists {
            idx = int32(len(s.Palette))
            s.Palette[blockName] = idx
        }
        
        // Calculate Sponge V3 Index
        pos := (y*l + z)*w + x
        s.BlockData[pos] = byte(idx) // Simplified: assumes index < 128
    }

    // 1. Foundation & Ceiling
    for x := 0; x < w; x++ {
        for z := 0; z < l; z++ {
            setBlock(x, 0, z, p.Palette["floor"])
            setBlock(x, h-1, z, "minecraft:stone_brick_slab[type=top]")
        }
    }

    // 2. The v5 Pillars (Indented 3x3 with lighting)
    pillars := [][]int{{2, 2}, {2, l - 3}, {w - 3, 2}, {w - 3, l - 3}}
    for _, pLoc := range pillars {
        for y := 1; y < h-1; y++ {
            setBlock(pLoc[0], y, pLoc[1], p.Palette["primary"])
            // Add purple light boxes at mid-height
            if y == h/2 {
                setBlock(pLoc[0], y, pLoc[1], p.Palette["lighting"])
            }
        }
    }
}