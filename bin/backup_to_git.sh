#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: © 2025 franklin
#
# SPDX-License-Identifier: MIT

# ChangeLog:
# v 0.1 02/07/2026 franklin - initial version
# v0.2 03/29/2026 franklin - skynet version

set -euo pipefail
IFS=$'\n\t'
LRED='\033[0;31m'
NC='\033[0m' # No Color
SERVER_DIR="~/workspace/gaming/game-skynet-minecraft"

function world_backup() {
    while true; do
        log_header "[$(date)] Starting skynet backup."
        
        git add "${SERVER_DIR}/"
        git commit -m "Skynet Backup: $(date)"
        git push origin $(git rev-parse --abbrev-ref HEAD)
        
        log_info "[$(date)] Backup complete."
    done
}

function main() {
  echo -e "\n" && figlet -f /usr/share/figlet/fonts/pagga Backup to GitHub && echo -e "\n"
  if [ -f "${SERVER_DIR}/bin/common.sh" ]; then
    source "${SERVER_DIR}/bin/common.sh"
  else
    echo -e "${LRED}can not find ${SERVER_DIR}/bin/common.sh.${NC}"
    exit 1
  fi
  log_info "successfully sourced ${SERVER_DIR}/bin/common.sh" && echo -e "\n"

  world_backup
}

main "$@"

