#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: ©2012-2026 franklin
#
# SPDX-License-Identifier: MIT

# ChangeLog:
# v 0.1 02/07/2026 franklin - initial version
# v0.2 03/29/2026 franklin - skynet version

set -euo pipefail
IFS=$'
	'
LRED='\033[0;31m'
NC='\033[0m' # No Color

# Corrected path to the project root where bin/common.sh is expected
PROJECT_ROOT="/home/minecraft/game-skynet-minecraft"
SERVER_DIR="${PROJECT_ROOT}/servers" # Assuming server configs are under src/servers/
MY_HOSTNAME=$(cat /proc/sys/kernel/hostname)

function world_backup() {
  while true; do
    log_header "[$(date)] Starting scheduled world backup."
    git add ${SERVER_DIR}/world/ ${SERVER_DIR}/world_nether/ ${SERVER_DIR}/world_the_end/
    git commit -m "World Backup: $(date)"
    git push origin $(git rev-parse --abbrev-ref HEAD)
    log_info "[$(date)] Backup complete."
  done
}

function host_backup() {
  # This path seems to refer to the cloned repository for configuration/scripts
  HOST_REPO_DIR="${PROJECT_ROOT}"
  while true; do
    log_header "[$(date)] Starting skynet host backup."
    git add "${HOST_REPO_DIR}/"
    git commit -m "Skynet Host Backup: $(date)"
    git push origin $(git rev-parse --abbrev-ref HEAD)
    log_info "[$(date)] Host backup complete."
  done
}

function main() {
  echo -e "
" && figlet -f /usr/share/figlet/fonts/pagga Backup to GitHub && echo -e "
"
  if [ -f "${SERVER_DIR}/bin/common.sh" ]; then
    source "${SERVER_DIR}/bin/common.sh"
  else
    echo -e "${LRED}Cannot find ${SERVER_DIR}/bin/common.sh.${NC}"
    exit 1
  fi
  log_info "Successfully sourced ${SERVER_DIR}/bin/common.sh" && echo -e "
"

  # Determine which backup function to run based on hostname
  # Assuming 'chonk.lab.bitsmasher.net' is the world server and others are host backups
  if [[ "$MY_HOSTNAME" == "chonk.lab.bitsmasher.net" ]]; then   
    world_backup
  else
   host_backup
  fi 
}

main "$@"
