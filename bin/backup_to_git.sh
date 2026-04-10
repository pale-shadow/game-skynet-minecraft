#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: ©2012-2026 franklin
#
# SPDX-License-Identifier: MIT

# ChangeLog:

# v 0.1 02/07/2026 franklin - initial version
# v0.2 03/29/2026 franklin - skynet version
# v 0.3 04/10/2026 franklin -fix the robot screw ups

set -euo pipefail
IFS=$' '
LRED='\033[0;31m'
NC='\033[0m' # No Color

PROJECT_ROOT="/home/skynet"
SERVER_DIR="${PROJECT_ROOT}/src/servers"
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
  if [ -f "${PROJECT_ROOT}/bin/common.sh" ]; then
    source "${PROJECT_ROOT}/bin/common.sh"
  else
    echo -e "${LRED}Cannot find ${SERVER_DIR}/bin/common.sh.${NC}"
    exit 1
  fi
  log_info "Successfully sourced ${SERVER_DIR}/bin/common.sh"

  if [[ "$MY_HOSTNAME" == "chonk.lab.bitsmasher.net" ]]; then   
    world_backup
  else
    host_backup
  fi 
}

main "$@"
