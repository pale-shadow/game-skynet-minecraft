#!/usr/bin/env bash
# Bitsmasher Network: Player Guide Distribution Script (Linux/v1.21.11)

# 1. Path detection
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
COMMON_SH="${REPO_ROOT}/bin/common.sh"
RCON_BIN="${REPO_ROOT}/bin/rcon.sh"

# 2. Dynamic User Detection
# Checks if the 'minecraft' user exists; if not, falls back to the current user (franklin)
if id "minecraft" &>/dev/null; then
    MC_USER="minecraft"
else
    MC_USER="$(whoami)"
    # Optional: Log a warning that we are running in dev mode
fi

# 3. Source Common Logic
if [ -f "$COMMON_SH" ]; then
    source "$COMMON_SH"
else
    echo "Error: common.sh not found at $COMMON_SH"
    exit 1
fi

function distribute_book() {
    log_header "Distributing Traveler's Guide to All Players"

    # Define the book data using 1.21.11 Data Components
    BOOK_COMMAND="give @a written_book[written_book_content={ \
        title:\"Traveler Guide\", \
        author:\"UnvaluedShoe79\", \
        pages:[ \
            '{\"text\":\"\\\\n\\\\nWelcome to Bitsmasher.\\\\n\\\\nEstablished 2012.\\\\n\\\\nYou stand at Washington Station, the Zero Point.\"}', \
            '{\"text\":\"\\\\n\\\\n§lURBAN DISTRICT§r\\\\n\\\\nExplore Shroomville at Y:63 and Deep Station at Y:31.\"}', \
            '{\"text\":\"\\\\n\\\\n§lAI FIELDS§r\\\\n\\\\nNew structures in Silicon Ridge and Abyssal Reef are built by Skynet on Pi5 hardware.\"}'] \
        }]"

    log_info "Running as user: $MC_USER"
    
    # Execute RCON commands
    # On Chonk, this uses sudo to hit the pipe. On Skynet, it uses your local permissions.
    sudo -u "$MC_USER" "$RCON_BIN" "say §b[System]§f Distributing the 2026 Modern Era Traveler's Guide..."
    sudo -u "$MC_USER" "$RCON_BIN" "$BOOK_COMMAND"

    log_info "Distribution complete."
}

distribute_book
