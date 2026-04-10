# SPDX-FileCopyrightText: © 2022-2025 franklin <franklin@bitsmasher.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import logging
from mcrcon import MCRcon

logger = logging.getLogger("mcserver")


def main():
    """_summary_"""
    mc_pass = os.environ.get("MC_PASS", "dinosaurExTraVaGanZa1969%%")
    with MCRcon("127.0.0.1", mc_pass) as mcr:
        resp = mcr.command("/whitelist add bob")
        logger.debug(resp)


if __name__ == "__main__":
    main()

# detect browser
# detect MC client version (?)
# detect OS
# check mods folder

