FROM python:3.12-slim

WORKDIR /app

# 1. 시스템 의존성 설치 (캐시 최적화를 위해 한 번에 실행)
# 💡 빌드 시간 단축을 위해 필요한 것만 최소한으로 설치합니다.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Python 라이브러리 설치 (캐시 최적화를 위해 requirements.txt만 먼저 복사)
COPY user-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 공유 모듈 복사
COPY accounts/ ./accounts/
COPY stories/ ./stories/
COPY library/ ./library/
COPY pages/ ./pages/
COPY subway/ ./subway/
COPY supabase/ ./supabase/
COPY templates/ ./templates/

# 4. 서비스 코드 복사
COPY user-service/ ./

# 💡 설정 폴더 이름을 project로 통일 (이미 존재하면 건너뜀)
RUN if [ -d "user_config" ]; then mv user_config project; fi

# 5. 정적 파일 수집 (빌드 시 수행하여 런타임 성능 향상)
# 💡 DB 연결 없이 수집하도록 더미 환경변수 사용
RUN SB_DB_PASSWORD=dummy SECRET_KEY=dummy python manage.py collectstatic --noinput || true

# 6. 환경 변수 및 실행 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 80

# 💡 Gunicorn 최적화: workers는 Fargate 0.25 vCPU 환경을 고려하여 1로 설정, timeout은 충분히 늘림
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "1", "--timeout", "120", "--log-level", "debug", "project.wsgi:application"]
