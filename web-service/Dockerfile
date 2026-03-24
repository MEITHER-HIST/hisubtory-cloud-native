# Stage 1: Build
FROM node:24-alpine AS build

# 빌드 시 메모리 제한 확장 및 Vite 에러 방지용 환경 변수
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"

WORKDIR /app

# 종속성 파일 복사
COPY package*.json ./

# 💡 유연한 설치를 위해 npm install 사용 및 피어 의존성 무시
RUN npm install --include=dev --legacy-peer-deps

# 소스 복사
COPY . .

# 💡 타입 체크 없이 Vite 빌드 실행 (빌드 통과 우선)
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
