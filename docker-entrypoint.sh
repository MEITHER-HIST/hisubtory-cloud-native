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
from stories.models import Episode, Webtoon, Station
try:
    # 1. 에피소드 2번 웹툰 ID 동기화 (썸네일 해결)
    episodes_to_fix = Episode.objects.filter(episode_num=2)
    for ep in episodes_to_fix:
        ep1 = Episode.objects.filter(episode_num=1, webtoon__station_id=ep.webtoon.station_id).first()
        if ep1 and ep.webtoon_id != ep1.webtoon_id:
            ep.webtoon_id = ep1.webtoon_id
            ep.save()
    
    # 2. 역 이름 기준으로 Webtoon의 station_id 자동 보정 (일원역-주엽역 문제 해결)
    webtoons = Webtoon.objects.select_related('station').all()
    for w in webtoons:
        # 제목에서 역 이름을 추출 (예: '일원역의 역사' -> '일원')
        import re
        match = re.search(r'(.+?)역', w.title)
        if match:
            s_name = match.group(1)
            correct_s = Station.objects.filter(station_name__contains=s_name).first()
            if correct_s and w.station_id != correct_s.id:
                print(f'Syncing Webtoon {w.webtoon_id}: {w.station.station_name} -> {correct_s.station_name}')
                w.station_id = correct_s.id
                w.save()
    print('✅ RDS data & Station mapping sync complete.')
except Exception as e:
    print(f'❌ Data fix error: {str(e)}')
" || echo "⚠️ Data fix failed..."

echo "Checking episode seed state..."
python seed_episodes.py || echo "⚠️ Episode seeding check failed..."

echo "Starting Gunicorn (Web Server)..."
# 로드밸런서 헬스체크를 위해 즉시 실행
exec gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --log-level info project.wsgi:application
