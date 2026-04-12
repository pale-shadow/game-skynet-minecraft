#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: ©2025 franklin <smoooth.y62wj@passmail.net>
#
# SPDX-License-Identifier: MIT

# ChangeLog:
#
# v0.1 02/25/2025 initial version

DEB_PKG=(git git-delta gnupg keyringer pass logiops)
LRED='\033[1;31m'

function required_files() {
  log_header "# --- Check GNU Autotools files ----------------------------------------"
  local required_files=("AUTHORS" "ChangeLog" "NEWS")

  for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
      log_info "Creating required file ${file} since it is not found."
      ln -sf README.md "$file"
    else
      log_info "Found required file: ${file}"
    fi
  done
}

function run_aclocal() {
  log_header "# --- Running aclocal -------------------------------------------------"
  # if [ "${MY_OS}" != "openbsd" ]; then
  #   log_info "Checking aclocal version..."
  #   acl_ver=$(aclocal --version | awk '{print $NF; exit}')
  #   echo "    $acl_ver"
  #   log_info "Running aclocal..."
  #   aclocal || exit 1
  # else
    AUTOCONF_VERSION=2.71 AUTOMAKE_VERSION=1.16 aclocal || exit 1
  # fi
  log_info ".. done with aclocal."
}

function run_automake() {
  log_header "# --- Running automake ------------------------------------------------"
  # if [ "${MY_OS}" != "openbsd" ]; then
    log_info "Checking automake version..."
    am_ver=$(automake --version | awk '{print $NF; exit}')
    echo "    $am_ver"

    log_info "Running automake..."
    automake -a -c --add-missing || exit 1
    #automake --force --copy --add-missing || exit 1
  # else
  #   AUTOCONF_VERSION=2.71 AUTOMAKE_VERSION=1.16 automake -a -c --add-missing || exit 1
  # fi
  log_info "... done with automake."
}

function run_autoconf() {
  log_header "# --- Running autoconf ------------------------------------------------"
  # if [ "${MY_OS}" != "openbsd" ]; then
    log_info "Checking autoconf version..."
    ac_ver=$(autoconf --version | awk '{print $NF; exit}')
    log_info "Autoconf version: $ac_ver"
    log_info "Running autoconf..."
    autoreconf -fi || exit 1
  # else
  #   ac_ver="2.71"
  #   log_info "Running autoconf..." # this is for OpenBSD systems
  #   AUTOCONF_VERSION=2.71 AUTOMAKE_VERSION=1.16 autoreconf -i || exit 1
  # fi
  log_info "... done with autoconf."
}

function main() {
  if [ -d "${HOME}/workspace/fonts/figlet" ] && [ "$(which figlet)" ]; then
    echo -e "\n\n" && figlet -f "${HOME}/workspace/fonts/figlet/pagga" ENGREEBLENATOR && echo -e "\n"
  fi
  
  if [ -f "${HOME}/workspace/bin/common.sh" ]; then
    source "${HOME}/workspace/bin/common.sh"
  else
    echo -e "${LRED}can not find ${HOME}/workspace/bin/common.sh.${NC}"
    exit 1
  fi

  log_info "successfully sourced ${HOME}/workspace/bin/common.sh" && echo -e "\n"

  if [ ! -d "aclocal" ]; then
    log_info "create aclocal dir"
    mkdir -p aclocal
  fi

  if [ ! -f "Makefile.in" ] && [ -f "./config.status" ]; then
    rm config.status
    log_warn "Makefile.in is missing: erasing stale config.status"
  fi

  required_files

  if [ ! -f "./config.status" ]; then
    log_warn "no config.status$"
    if [ ! -d "aclocal" ]; then mkdir aclocal; fi
    run_aclocal
    run_autoconf
    run_automake
    ./configure
  else
    ./config.status
  fi
}

main "$@"