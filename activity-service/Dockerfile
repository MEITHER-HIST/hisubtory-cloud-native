FROM python:3.12-slim

WORKDIR /app

# 1. 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Python 라이브러리 설치
COPY activity-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. 공유 모듈 복사
COPY accounts/ ./accounts/
COPY stories/ ./stories/
COPY library/ ./library/
COPY pages/ ./pages/
COPY subway/ ./subway/
COPY supabase/ ./supabase/
COPY templates/ ./templates/

# 4. 서비스 코드 및 스크립트 복사
COPY activity-service/ ./
COPY create_missing_tables.py .
COPY seed_episodes.py .
COPY docker-entrypoint.sh /usr/local/bin/

# 💡 스크립트 권한 부여 및 줄바꿈 처리
RUN chmod +x /usr/local/bin/docker-entrypoint.sh && \
    sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh

# 💡 설정 폴더 이름을 project로 통일
RUN if [ -d "activity_config" ]; then mv activity_config project; fi

# 5. 정적 파일 수집
RUN SB_DB_PASSWORD=dummy SECRET_KEY=dummy python manage.py collectstatic --noinput || true

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 80

# 💡 Entrypoint를 통해 DB 마이그레이션 및 시딩 자동화
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
