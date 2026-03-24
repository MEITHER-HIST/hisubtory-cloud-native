# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
ENV CI=false

# 💡 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 💡 프로젝트 전체(루트)를 복사한 후, web-service 폴더 내부로 이동하여 빌드 환경을 고정합니다.
COPY . .

# 💡 작업 디렉토리를 web-service 폴더 내부로 강제 고정 (매우 중요!)
WORKDIR /app/web-service

# 💡 의존성 설치 및 빌드 시 상세 로그 출력
RUN npm install --legacy-peer-deps
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사 (web-service 내부의 build 폴더 참조)
COPY --from=build /app/web-service/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY web-service/nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
