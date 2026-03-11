FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 💡 빌드를 방해하는 모든 gunicorn 설정 파일을 삭제합니다.
RUN find . -name "gunicorn.conf.py" -delete

ENV PYTHONPATH="/app:/app/user-service:/app/story-service:/app/activity-service"
EXPOSE 80

# 💡 --preload를 빼고 실행해 봅니다. (연결 지연으로 인한 부팅 멈춤 방지)
# 💡 대신 로그 레벨을 debug로 유지하여 워커 부팅 실패 시 이유를 확인합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "1", "--log-level", "debug", "--timeout", "120", "project.wsgi:application"]