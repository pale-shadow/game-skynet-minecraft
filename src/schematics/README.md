# Schematics

## go

```sh
mkdir -p ~/src/schematic-go
cd ~/src/schematic-go
go mod init github.com/chonk/minecraft-station
go get github.com/Tnze/go-mc@master
```

## python

```sh
python3 generate_signal_core.py
# mv signal_core.schem ~/minecraft/config/worldedit/schematics/
```

- Run: `//schem load signal_core`
- Run: `//paste` (The core will be lit up and visible through the cyan glass).

## Installing Schematics

- Download schematics from [https://www.minecraft-schematics.com/](https://www.minecraft-schematics.com/)
- Place the schematics in `/home/minecraft/minecraft/config/worldedit/schematics` folder. 
- list the schematics in the game chat `/schem list`
- load it in the game chat `/schem load name`
- go where you want it and `//paste`
