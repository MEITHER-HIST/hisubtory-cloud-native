#!/bin/bash
set -euo pipefail

APP_DIR="/home/ubuntu/HISUB/hisubtory"

echo "[Stop] Stopping Docker containers..."
if [ -d "$APP_DIR" ]; then
  cd "$APP_DIR"
  sudo docker compose down || true
else
  echo "[Stop] App directory not found. Skipping."
fi
echo "[Stop] Done."
