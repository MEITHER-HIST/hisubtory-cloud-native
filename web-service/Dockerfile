# Stage 1: Build
FROM node:20-alpine AS build

# 빌드 시 메모리 제한 확장 (Vite 빌드 안정성 확보)
ENV NODE_OPTIONS="--max-old-space-size=4096"

WORKDIR /app

# 종속성 파일 복사 및 설치 (확실한 빌드 도구 설치를 위해 devDependencies 포함)
COPY package*.json ./
RUN npm install --include=dev

# 소스 복사 및 빌드
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:stable-alpine
# Vite 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
