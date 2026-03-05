FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# collectstatic 실행 시 필요한 최소한의 환경 변수 제공 및 PYTHONPATH 설정
RUN PYTHONPATH="/app:/app/activity-service:/app/user-service:/app/story-service" \
    SUPABASE_URL="https://dummy.co" \
    SUPABASE_KEY="dummy" \
    AWS_ACCESS_KEY_ID="dummy" \
    AWS_SECRET_ACCESS_KEY="dummy" \
    python manage.py collectstatic --noinput

ENV PYTHONPATH="/app:/app/activity-service:/app/user-service:/app/story-service"

# 마이그레이션 실행 후 Gunicorn 시작
CMD ["sh", "-c", "PYTHONPATH=$PYTHONPATH:/app/user-service python user-service/manage.py migrate --database=default && gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 --access-logfile - --error-logfile - project.wsgi:application"]