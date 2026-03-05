FROM python:3.12-slim-bookworm

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 패키지 설치 전 파일 복사
COPY requirements.txt .
COPY subway/ ./subway/
COPY stories/ ./stories/
COPY library/ ./library/
COPY pages/ ./pages/
COPY accounts/ ./accounts/
COPY story-service/ ./

# 모든 파일이 복사된 후 패키지 설치
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# PYTHONPATH 설정
ENV PYTHONPATH="/app"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
