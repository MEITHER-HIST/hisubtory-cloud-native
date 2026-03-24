# Stage 1: Build
FROM node:24-alpine AS build

# 빌드 시 메모리 제한 확장 (Vite 빌드 안정성 확보)
ENV NODE_OPTIONS="--max-old-space-size=4096"

WORKDIR /app

# 종속성 파일 복사
COPY package*.json ./

# 💡 CI 환경에 최적화된 깨끗한 설치 (package-lock.json 기준)
RUN npm ci --include=dev

# 소스 복사 및 빌드
COPY . .

# 💡 빌드 실행 (TypeScript 에러 발생 시 로그를 확인하기 위해 verbose 모드 활용 가능)
RUN npm run build

# Stage 2: Serve
FROM nginx:stable-alpine
# Vite 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
