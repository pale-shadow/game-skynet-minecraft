#!/bin/bash
# Skynet Process Monitor

PID_FILE="/home/franklin/.gemini/tmp/game-chonk-minecraft/skynet.pid"
LOG_FILE="/home/franklin/workspace/gaming/game-chonk-minecraft/logs/skynet_daemon.log"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "✅ Skynet Process is ALIVE (PID: $PID)"
        tail -n 5 "$LOG_FILE"
    else
        echo "❌ Skynet Process is DEAD. Removing stale PID file."
        rm "$PID_FILE"
    fi
else
    echo "⭕ Skynet Process is NOT RUNNING."
fi
