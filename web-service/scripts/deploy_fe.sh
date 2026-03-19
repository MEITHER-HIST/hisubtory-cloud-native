#!/bin/bash
set -e

SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)/build"
DEST_DIR="/var/www/hisubtory-fe"

mkdir -p "$DEST_DIR"
rm -rf "$DEST_DIR"/*
cp -a "$SRC_DIR"/. "$DEST_DIR"/

chown -R www-data:www-data "$DEST_DIR" || true

nginx -t
systemctl reload nginx
