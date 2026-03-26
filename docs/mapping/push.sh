#!/bin/bash
# skynet-to-chonk.sh
PASS="YourUltraSecurePassword"
HOST="chonk.lab.bitsmasher.net"

# Example: AI sends a message and sets a block
mcrcon -H $HOST -P 25575 -p $PASS "say [Skynet] NPU detected entity anomaly in Silicon Ridge. Deploying containment."
mcrcon -H $HOST -P 25575 -p $PASS "setblock 1487 64 787 redstone_lamp"
