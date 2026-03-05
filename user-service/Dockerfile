# 1. Build Stage
FROM python:3.12-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 2. Run Stage
FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq5 default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 공통 앱 복사 (root 폴더 기준)
COPY subway/ ./subway/
COPY stories/ ./stories/
COPY library/ ./library/

# 서비스 코드 복사 (빌드 컨텍스트 root 기준)
COPY user-service/ ./

# main.html (루트 폴더) 복사 - index 뷰를 위해 필요
COPY main.html ./

# PYTHONPATH 설정
ENV PYTHONPATH="/app:/app/user-service"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
