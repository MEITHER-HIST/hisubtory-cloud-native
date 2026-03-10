# 1. Build Stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY activity-service/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 2. Run Stage
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 필수 모듈 복사
COPY subway/ ./subway/
COPY story-service/stories/ ./stories/
COPY activity-service/ ./

# 설정 폴더 이름을 project로 통일 (이미 존재하면 건너뜀)
RUN if [ -d "activity_config" ]; then mv activity_config project; fi

ENV PYTHONPATH=/app
CMD ["gunicorn", "--bind", "0.0.0.0:80", "project.wsgi:application"]
