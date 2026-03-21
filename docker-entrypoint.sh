#!/bin/bash
set -e

echo "Starting Entrypoint Script..."

# DB 에러가 나더라도 Gunicorn 실행을 방해하지 않도록 background 또는 에러 무시 처리
echo "Running DB migrations..."
python manage.py migrate --noinput || echo "⚠️ Migration failed, but starting server anyway..."

echo "Ensuring Admin Superuser exists..."
python create_admin_user.py || echo "⚠️ Admin superuser check failed..."

echo "Checking episode seed state..."
python seed_episodes.py || echo "⚠️ Episode seeding check failed..."

echo "Starting Gunicorn (Web Server)..."
# 로드밸런서 헬스체크를 위해 즉시 실행
exec gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --log-level info project.wsgi:application
