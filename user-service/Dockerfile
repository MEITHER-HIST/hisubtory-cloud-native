FROM python:3.12-slim

WORKDIR /app

# 1. 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Python 라이브러리 설치 (Context는 프로젝트 루트)
COPY user-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 서비스 핵심 코드 복사 (project 디렉토리 보존)
COPY user-service/manage.py ./
COPY user-service/project/ ./project/

# 4. 공유 모듈 복사 (프로젝트 루트에서 가져옴)
COPY accounts/ ./accounts/
COPY stories/ ./stories/
COPY library/ ./library/
COPY pages/ ./pages/
COPY subway/ ./subway/
COPY supabase/ ./supabase/
COPY templates/ ./templates/

# 5. 스크립트 복사
COPY create_missing_tables.py .
COPY create_admin_user.py .
COPY seed_episodes.py .
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# 스크립트 권한 부여 및 줄바꿈 처리
RUN chmod +x /usr/local/bin/docker-entrypoint.sh && \
    sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh

# 6. 정적 파일 수집 (빌드 시 더미 키 주입)
RUN SB_DB_PASSWORD=dummy SECRET_KEY=dummy python manage.py collectstatic --noinput || true

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 80

# Entrypoint를 통해 실행
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
