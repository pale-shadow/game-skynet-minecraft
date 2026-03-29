#!/usr/bin/env bash
# Compare Hailo-8L vs Google Coral vs Tinker Edge-T

# Use $HOME instead of ~ inside quotes
PROJECT_ROOT="$HOME/workspace/gaming/game-skynet-minecraft"
BIN="${PROJECT_ROOT}/bin/schem-gen"

echo "⚔️ Starting the AI Grid-Tie Competition..."

# Launch parallel builders
"${BIN}" --mode weave --hardware hailo & 
"${BIN}" --mode weave --hardware coral &
"${BIN}" --mode weave --hardware tinker &

wait

echo "Competition Complete. Check BlueMap for visual differences."
