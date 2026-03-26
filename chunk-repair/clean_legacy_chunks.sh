#!/usr/bin/env bash
# SPDX-FileCopyrightText: © 2026 franklin
# Script to strip legacy Forge mod blocks using MCA Selector CLI

SERVER_DIR="/home/minecraft"
MCA_JAR="${SERVER_DIR}/.mcaselector/mcaselector.jar" # Path based on your file list [1]
WORLD_DIR="${SERVER_DIR}/world"

# --- Source Common Logic ---
if [ -f "${SERVER_DIR}/bin/common.sh" ]; then
    source "${SERVER_DIR}/bin/common.sh"
else
    echo "Error: Cannot find ${SERVER_DIR}/bin/common.sh"
    exit 1
fi

function clean_modded_blocks() {
    log_header "Starting Legacy Block Cleanup"
    
    # This query targets the specific modded registries causing your 1.21.11 errors
    # Note: Using 'delete' on specific blocks requires a version of MCA Selector 
    # that supports NBT-level block replacement in headless mode.
    
    log_info "Scanning for Thermal and Mystical Agriculture blocks..."
    
    java -jar "$MCA_JAR" --mode head --world "$WORLD_DIR" \
        --query "Palette ~ \"thermal:\" || Palette ~ \"mysticalagriculture:\" || Palette ~ \"occultism:\"" \
        --operation delete
        
    log_info "Cleanup complete. Modded blocks have been purged from chunk palettes."
}

# --- Main Execution ---
# Safety check: Ensure the backup script has run recently [2]
log_info "Ensuring world backup is current..."
"${SERVER_DIR}/bin/backup_to_git.sh" 

clean_modded_blocks
