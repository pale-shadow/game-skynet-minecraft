package minecraft

import (
	"compress/gzip"
	"fmt"
	"os"
	"path/filepath"
	"runtime"

	"github.com/Tnze/go-mc/level/schematic"
)

type Location struct {
	X, Y, Z int
}

func SaveSchematic(schem *schematic.Schematic, filename string) error {
	path := filepath.Join("schematic-agent", "schem_files", filename)
	
	f, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("failed to create schematic file: %v", err)
	}
	defer f.Close()

	gw := gzip.NewWriter(f)
	defer gw.Close()

	if err := schem.Encode(gw); err != nil {
		return fmt.Errorf("failed to encode NBT schematic: %v", err)
	}

	fmt.Printf("✔ Phase 2.1: Schematic saved to %s\n", path)
	return nil
}

func Check_Minecraft_Install() {
	var minecraftPath string

	switch runtime.GOOS {
	case "windows":
		appData := os.Getenv("APPDATA")
		minecraftPath = filepath.Join(appData, ".minecraft")
	case "darwin": // macOS
		homeDir, err := os.UserHomeDir()
		if err != nil {
			fmt.Println("Error getting home directory:", err)
			return
		}
		minecraftPath = filepath.Join(homeDir, "Library", "Application Support", "minecraft")
	case "linux":
		homeDir, err := os.UserHomeDir()
		if err != nil {
			fmt.Println("Error getting home directory:", err)
			return
		}
		minecraftPath = filepath.Join(homeDir, ".minecraft")
	default:
		fmt.Println("Unsupported operating system:", runtime.GOOS)
		return
	}

	info, err := os.Stat(minecraftPath)
	if os.IsNotExist(err) {
		fmt.Println("Minecraft is not installed ('.minecraft' folder not found).")
	} else if err != nil {
		fmt.Println("Error checking Minecraft installation:", err)
	} else if info.IsDir() {
		fmt.Println("Minecraft is installed at:", minecraftPath)
	} else {
		fmt.Println("Found a file named '.minecraft', but it's not a directory.")
	}
}

