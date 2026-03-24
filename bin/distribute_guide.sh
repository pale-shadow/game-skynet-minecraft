#!/usr/bin/env bash
# Bitsmasher Network: Player Guide Distribution Script (v1.21.11)
# Ref: 2026 Urbanization Phase

# 1. Automatically detect the repository root relative to this script
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)"
COMMON_SH="${REPO_ROOT}/bin/common.sh"
RCON_BIN="${REPO_ROOT}/bin/rcon.sh"

# Standard Linux service user (usually 'minecraft' instead of OpenBSD's '_minecraft')
MC_USER="minecraft"

# 2. Source Common Logic for Logging
if [ -f "$COMMON_SH" ]; then
    source "$COMMON_SH"
else
    echo "Error: common.sh not found at $COMMON_SH"
    exit 1
fi

function distribute_book() {
    log_header "Distributing Traveler's Guide to All Players"

    # Define the book data using 1.21.11 Data Components syntax
    BOOK_COMMAND="give @a written_book[written_book_content={ \
        title:\"Traveler Guide\", \
        author:\"UnvaluedShoe79\", \
        pages:[ \
            '{\"text\":\"\\\\n\\\\nWelcome to Bitsmasher.\\\\n\\\\nEstablished 2012.\\\\n\\\\nYou stand at Washington Station, the Zero Point of the legacy network.\"}', \
            '{\"text\":\"\\\\n\\\\n§lURBAN DISTRICT§r\\\\n\\\\nExplore Shroomville at Y:63 and Deep Station at Y:31.\\\\n\\\\nUse the Vertical Sump for transit.\"}', \
            '{\"text\":\"\\\\n\\\\n§lAI FIELDS§r\\\\n\\\\nNew structures in Silicon Ridge and Abyssal Reef are built by our Skynet AI daemon on Pi5 hardware.\"}'] \
        }]"

    # 1. Announce distribution to the server
    log_info "Announcing distribution..."
    # Replacing 'doas -u _minecraft' with Linux standard 'sudo -u minecraft'
    sudo -u "$MC_USER" "$RCON_BIN" "say §b[System]§f Distributing the 2026 Modern Era Traveler's Guide to all players..."

    # 2. Execute the give command
    log_info "Pushing RCON give command..."
    sudo -u "$MC_USER" "$RCON_BIN" "$BOOK_COMMAND"

    # 3. Final Log
    log_info "Distribution complete."
}

distribute_book
