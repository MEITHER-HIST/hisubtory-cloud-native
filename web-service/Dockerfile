# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
ENV CI=false

WORKDIR /app

# 💡 프로젝트 전체 복사
COPY . .

# 💡 작업 디렉토리를 web-service 폴더 내부로 고정
WORKDIR /app/web-service

# 💡 의존성 설치 및 빌드
RUN npm install --legacy-peer-deps
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
COPY --from=build /app/web-service/build /usr/share/nginx/html
COPY web-service/nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
