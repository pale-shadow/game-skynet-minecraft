#!/bin/sh

# OpenBSD:
# doas pkg_add jdk minecraft

# A simple "rcon.sh" file to interactively issue commands to the server, helpful combined with tail
while true; do
    printf "RCON> "
    read input
    echo "$input" | doas -u _minecraft tee -a /var/run/minecraft >/dev/null
done

echo save-off > /var/run/minecraft # Disable writing updates
echo save-all > /var/run/minecraft # Flush pending writes to disk
# Perform backup, tar, etc.
echo save-on > /var/run/minecraft # Re-enable writing updates
