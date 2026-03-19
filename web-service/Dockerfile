# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app
# 종속성 파일 복사 및 설치
COPY package*.json ./
RUN npm install
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
