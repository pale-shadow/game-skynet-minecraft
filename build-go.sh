#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: ©2012-2026 franklin <smoooth.y62wj@passmail.net>
#
# SPDX-License-Identifier: MIT

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${PROJECT_ROOT}/bin"
CONFIG_DIR="${PROJECT_ROOT}/schematic-agent/configs"

# 1. Compile the toolchain
echo "Rebuilding Skynet Go Toolchain..."
go build -o "${BIN_DIR}/schem-gen" "${PROJECT_ROOT}/cmd/main.go"

# 2. Run the Grid Tie Weaver
# Example: Connecting Station 4478 to Tower 2196
echo "Initiating Grid Tie Weaver: Connecting Urban Nodes..."
"${BIN_DIR}/schem-gen" weave --config "${CONFIG_DIR}/grid_tie_weaver.yaml"

if [ $? -eq 0 ]; then
    echo "Success: Urban power grid extended."
else
    echo "ERROR: Pathfinding failed. Check schematic-agent/logs/hailort.log"
    exit 1
fi
