#!/bin/bash
set -e

echo "Starting Entrypoint Script..."

# DB 에러가 나더라도 Gunicorn 실행을 방해하지 않도록 background 또는 에러 무시 처리
echo "Running DB migrations..."
python manage.py migrate --noinput || echo "⚠️ Migration failed, but starting server anyway..."

echo "Ensuring Admin Superuser exists..."
python create_admin_user.py || echo "⚠️ Admin superuser check failed..."

echo "Fixing Episode 2 Data & Thumbnails on RDS..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from stories.models import Episode
try:
    episodes_to_fix = Episode.objects.filter(episode_num=2)
    for ep in episodes_to_fix:
        ep1 = Episode.objects.filter(episode_num=1, webtoon__station_id=ep.webtoon.station_id).first()
        if ep1 and ep.webtoon_id != ep1.webtoon_id:
            print(f'Syncing EP {ep.episode_id}: {ep.webtoon_id} -> {ep1.webtoon_id}')
            ep.webtoon_id = ep1.webtoon_id
            ep.save()
    print('✅ Episode 2 data sync complete.')
except Exception as e:
    print(f'❌ Episode 2 fix error: {str(e)}')
" || echo "⚠️ Data fix failed..."

echo "Checking episode seed state..."
python seed_episodes.py || echo "⚠️ Episode seeding check failed..."

echo "Starting Gunicorn (Web Server)..."
# 로드밸런서 헬스체크를 위해 즉시 실행
exec gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --log-level info project.wsgi:application
