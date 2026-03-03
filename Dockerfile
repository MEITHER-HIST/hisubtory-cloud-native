# Python 3.11 slim 이미지 사용
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 생성
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 후 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 소스 코드 복사
COPY . .

# 포트 노출 (예: Flask/Django 기본 포트)
EXPOSE 8000

# 컨테이너 실행 명령 (Flask 예시)
# Flask라면: CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
# Django라면: CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]

CMD ["python", "app.py"]

  
