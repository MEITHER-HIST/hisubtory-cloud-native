#!/bin/bash
set -e

echo "Starting Entrypoint Script..."

# DB 에러가 나더라도 Gunicorn 실행을 방해하지 않도록 background 또는 에러 무시 처리
echo "Running DB migrations..."
python manage.py migrate --noinput || echo "⚠️ Migration failed, but starting server anyway..."

echo "Ensuring Admin Superuser exists..."
python create_admin_user.py || echo "⚠️ Admin superuser check failed..."

echo "Fixing RDS Data Integrity (Thumbnails, Mapping, and Control Characters)..."
python -c "
import os
import django
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from stories.models import Episode, Webtoon, Station, Cut
try:
    # 1. 모든 테이블의 경로 데이터에서 줄바꿈(\r, \n) 제거 (썸네일 404 해결)
    print('Cleaning control characters from paths...')
    for w in Webtoon.objects.all():
        if w.thumbnail:
            new_val = w.thumbnail.replace('\r', '').replace('\n', '').strip()
            if w.thumbnail != new_val:
                w.thumbnail = new_val; w.save()
    for e in Episode.objects.all():
        if e.source_url:
            new_val = e.source_url.replace('\r', '').replace('\n', '').strip()
            if e.source_url != new_val:
                e.source_url = new_val; e.save()
    for c in Cut.objects.all():
        if c.image:
            new_val = c.image.replace('\r', '').replace('\n', '').strip()
            if c.image != new_val:
                c.image = new_val; c.save()

    # 2. 에피소드 2번 웹툰 ID 동기화 (에피소드 2 썸네일 해결)
    print('Syncing Episode 2 webtoon IDs...')
    for ep in Episode.objects.filter(episode_num=2):
        ep1 = Episode.objects.filter(episode_num=1, webtoon__station_id=ep.webtoon.station_id).first()
        if ep1 and ep.webtoon_id != ep1.webtoon_id:
            ep.webtoon_id = ep1.webtoon_id; ep.save()
    
    # 3. 역 이름 기준으로 Webtoon의 station_id 전수 교정 (일원역-주엽역 등 매칭 해결)
    print('Re-mapping webtoons to correct stations by name...')
    for w in Webtoon.objects.all():
        match = re.search(r'(.+?)역', w.title)
        if match:
            s_name = match.group(1).strip()
            correct_s = Station.objects.filter(station_name__contains=s_name).first()
            if correct_s and w.station_id != correct_s.id:
                print(f'Correcting {w.title}: ID {w.station_id} -> {correct_s.id} ({correct_s.station_name})')
                w.station_id = correct_s.id; w.save()
    print('✅ RDS Data Integrity Fix Complete.')
except Exception as e:
    print(f'❌ Data fix error: {str(e)}')
" || echo "⚠️ Data fix failed..."

echo "Checking episode seed state..."
python seed_episodes.py || echo "⚠️ Episode seeding check failed..."

echo "Starting Gunicorn (Web Server)..."
# 로드밸런서 헬스체크를 위해 즉시 실행
exec gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --log-level info project.wsgi:application
