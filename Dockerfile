FROM python:3.12-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 소스 복사 (root 기준)
COPY . .

# collectstatic 및 PYTHONPATH 설정
ENV PYTHONPATH="/app:/app/user-service:/app/activity-service:/app/story-service"

# 정적 파일 수집 (더미 환경변수 제공)
RUN SUPABASE_URL="https://dummy.co" \
    SUPABASE_KEY="dummy" \
    AWS_ACCESS_KEY_ID="dummy" \
    AWS_SECRET_ACCESS_KEY="dummy" \
    python user-service/manage.py collectstatic --noinput

# 마이그레이션 실행 후 Gunicorn 시작 (user-service 기준)
CMD ["sh", "-c", "python user-service/manage.py migrate --noinput && gunicorn --bind 0.0.0.0:80 --workers 2 --timeout 120 project.wsgi:application"]
