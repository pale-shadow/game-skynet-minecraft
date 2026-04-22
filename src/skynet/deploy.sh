#!/bin/bash
# Deployment script for skynet host
# Run with: sudo ./deploy.sh

SERVICE_NAME="skynet-daemon"
SOURCE_SERVICE="/home/minecraft/game-skynet-minecraft/servers/skynet/${SERVICE_NAME}.service"
TARGET_SERVICE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "Deploying ${SERVICE_NAME}..."

# Symlink service file
ln -sf "$SOURCE_SERVICE" "$TARGET_SERVICE"

# Reload and restart
systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo "${SERVICE_NAME} deployed and restarted."
