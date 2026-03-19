#!/bin/bash
set -e

echo "Running DB migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

echo "Ensuring Admin Superuser exists..."
python create_admin_user.py || echo "Admin superuser creation failed, continuing..."

# 💡 배포 안정성을 위해 시딩 작업은 선택적으로 실행하거나 주석 처리합니다.
# echo "Seeding subway data (Optional)..."
# python manage.py seed_subway_integrated || echo "Subway seeding skipped."

echo "Checking episode seed state..."
python seed_episodes.py || echo "Episode seeding skipped."

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --log-level info project.wsgi:application
