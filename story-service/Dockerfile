# 1. Build Stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY story-service/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 2. Run Stage
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 공유 모듈 복사 (루트 컨텍스트에서 실행됨)
COPY accounts/ ./accounts/
COPY stories/ ./stories/
COPY library/ ./library/
COPY pages/ ./pages/
COPY subway/ ./subway/
COPY supabase/ ./supabase/

# 서비스 특정 코드 복사
COPY story-service/ ./

# 설정 폴더 이름을 project로 통일 (이미 존재하면 건너뜀)
RUN if [ -d "story_config" ]; then mv story_config project; fi

ENV PYTHONPATH=/app
# Static 파일 수집 (필요시)
RUN SB_DB_PASSWORD=dummy python manage.py collectstatic --noinput || true

CMD ["gunicorn", "--bind", "0.0.0.0:80", "project.wsgi:application"]
