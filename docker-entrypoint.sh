#!/bin/bash
set -e

echo "Starting Entrypoint Script..."

# DB 에러가 나더라도 Gunicorn 실행을 방해하지 않도록 처리
echo "Running DB migrations..."
python manage.py migrate --noinput || echo "⚠️ Migration failed, but starting server anyway..."

echo "Ensuring Admin Superuser exists..."
python create_admin_user.py || echo "⚠️ Admin superuser check failed..."

# 💡 [중요] 헬스체크 타임아웃 방지를 위해 무거운 로직은 백그라운드에서 실행
echo "Fixing RDS Data Integrity in background..."
python -c "
import os
import django
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from stories.models import Episode, Webtoon, Station, Cut
try:
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
    
    print('Re-mapping webtoons to correct stations by name...')
    for w in Webtoon.objects.all():
        match = re.search(r'(.+?)역', w.title)
        if match:
            s_name = match.group(1).strip()
            correct_s = Station.objects.filter(station_name__contains=s_name).first()
            if correct_s and w.station_id != correct_s.id:
                w.station_id = correct_s.id; w.save()
    print('✅ RDS Data Integrity Fix Complete.')
except Exception as e:
    print(f'❌ Data fix error: {str(e)}')
" &

echo "Starting Gunicorn (Web Server) immediately for health check..."
# 로드밸런서 헬스체크를 위해 즉시 실행
exec gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --log-level info project.wsgi:application
