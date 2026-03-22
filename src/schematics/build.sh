#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: ©2012-2026 franklin <smoooth.y62wj@passmail.net>
#
# SPDX-License-Identifier: MIT

SCHEM_DIR="/home/minecraft/src/schematics"
VENV_PATH="/tmp/venv"


if [ ! -d "$VENV_PATH" ]; then
    echo "Initializing fresh environment..."
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"
pushd ${SCHEM_DIR} || exit 1

if ! python3 -c "import mcschematic" &> /dev/null; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt || echo "PIP Failed - Check SSL"
fi

echo "Generating v5 Industrial Station..."
python3 generate_schematic.py prompts/crafter_hub_v5.json

popd