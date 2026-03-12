#!/bin/bash
set -e

echo "Waiting for database connection..."
# DB 연결 확인 (옵션: 필요 시 nc 등 사용)

echo "Running migrations for default (Postgres/Supabase)..."
python manage.py migrate --database=default --noinput || echo "Default migration failed, continuing..."

echo "Running migrations for mysql..."
python manage.py migrate --database=mysql --noinput || echo "MySQL migration failed, continuing..."

echo "Creating missing tables in MySQL..."
python create_missing_tables.py || echo "Create tables failed, continuing..."

echo "Seeding subway data..."
python manage.py seed_subway_integrated || echo "Subway seeding failed, continuing..."

echo "Seeding episode data..."
python seed_episodes.py || echo "Episode seeding failed, continuing..."

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:80 --workers 1 --timeout 120 --log-level debug project.wsgi:application
