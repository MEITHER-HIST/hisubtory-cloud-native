#!/bin/bash
set -e

echo "Running DB migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

echo "Ensuring Admin Superuser exists..."
# 💡 DB가 아직 준비 안 됐을 수도 있으니 에러가 나도 Gunicorn은 뜨게 합니다.
python create_admin_user.py || echo "Admin superuser creation failed, continuing..."

echo "Seeding subway data (Skipped if exists)..."
python manage.py seed_subway_integrated || echo "Subway seeding skipped or failed."

echo "Checking episode seed state..."
python seed_episodes.py || echo "Episode seeding skipped or failed."

# echo "Restoring database from restore.sql..."
# python restore_db.py || echo "Database restore failed, continuing..."

echo "Starting Gunicorn..."
# 💡 --preload를 빼서 연결 지연 시에도 부팅이 멈추지 않게 합니다.
exec gunicorn --bind 0.0.0.0:80 --workers 1 --timeout 120 --log-level debug project.wsgi:application
