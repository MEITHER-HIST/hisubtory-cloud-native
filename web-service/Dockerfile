# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장 및 Vite 에러 방지용 환경 변수
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
# 💡 CI=false로 설정하여 사소한 경고(Warning)가 빌드를 멈추지 않게 함
ENV CI=false

WORKDIR /app

# 종속성 파일 복사
COPY package*.json ./

# 💡 피어 의존성 무시 및 유연한 설치
RUN npm install --legacy-peer-deps

# 소스 복사
COPY . .

# 💡 상세 로그와 함께 빌드 실행 (빌드 실패 시 원인 파악 용이)
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
