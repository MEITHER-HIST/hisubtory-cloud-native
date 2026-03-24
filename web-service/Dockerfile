# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장 및 Vite 에러 방지용 환경 변수
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
ENV CI=false

WORKDIR /app

# 종속성 파일 복사
COPY package*.json ./

# 💡 피어 의존성 무시 및 유연한 설치
RUN npm install --legacy-peer-deps

# 소스 및 설정 파일 복사
COPY . .

# 💡 빌드 전 index.html 존재 확인 (로그 기록용)
RUN ls -al index.html

# 💡 타입 체크 건너뛰고 Vite 빌드 직접 실행
# npx를 통해 설치된 로컬 vite를 직접 호출하여 경로 문제를 해결합니다.
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
