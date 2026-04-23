#!/bin/bash
# Deployment script for stargate host
# Run with: sudo ./deploy.sh

SERVICE_NAME="stargate-daemon"
SOURCE_SERVICE="/mnt/clusterfs2/workspace/gaming/game-skynet-minecraft/src/stargate/${SERVICE_NAME}.service"
TARGET_SERVICE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "Deploying ${SERVICE_NAME}..."

# Symlink service file
ln -sf "$SOURCE_SERVICE" "$TARGET_SERVICE"

# Reload and restart
systemctl daemon-reload
systemctl enable --now "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo "${SERVICE_NAME} deployed and restarted."
