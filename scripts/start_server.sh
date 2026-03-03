#!/bin/bash
set -euo pipefail

APP_DIR="/home/ubuntu/HISUB/hisubtory"

echo "[Start] Starting Docker containers..."
cd "$APP_DIR"

# 혹시 모를 포트 충돌 방지를 위해 시스템 기본 서비스 중지 (필요 시)
sudo systemctl stop redis-server || true

# Docker Compose 백그라운드 실행 및 강제 빌드
sudo docker compose up -d --build

# 실행 상태 확인
echo "[Start] Checking container status..."
sudo docker ps

echo "[Start] Deployment Complete!"
