#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: ©2012-2026 franklin <smoooth.y62wj@passmail.net>
#
# SPDX-License-Identifier: MIT

PROJECT_DIR="/home/minecraft/src/schematics"
GO_GEN_DIR="/home/minecraft/src/schematic-go"
PROMPT_FILE="${PROJECT_DIR}/prompts/crafter_hub_v5.json"

# 1. Verify Go Binary exists
if [ ! -f "${GO_GEN_DIR}/schem-gen" ]; then
    echo "ERROR: Go binary not found at ${GO_GEN_DIR}/schem-gen"
    echo "Please run 'go build -o schem-gen main.go' in the schematic-go directory."
    exit 1
fi

pushd "${GO_GEN_DIR}" > /dev/null || exit 1

# 2. Run the generator
echo "Generating v5 Industrial Station via Go Toolchain..."
./schem-gen "${PROMPT_FILE}"

# 3. Check for successful output via the symlink
if [ $? -eq 0 ]; then
    echo "Success! Schematic generated in ${PROJECT_DIR}/schem_files/"
else
    echo "CRITICAL: Generation failed."
    popd > /dev/null
    exit 1
fi

popd > /dev/null
