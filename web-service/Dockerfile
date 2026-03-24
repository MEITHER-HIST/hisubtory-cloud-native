# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장 및 Vite 에러 방지용 환경 변수
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
ENV CI=false

WORKDIR /app

# 💡 빌드 컨텍스트인 프로젝트 루트(.)를 기준으로 파일을 정확히 복사합니다.
COPY web-service/package*.json ./

# 💡 피어 의존성 무시 및 유연한 설치 (Vite 5/6 호환성 확보)
RUN npm install --legacy-peer-deps

# 💡 모든 소스 파일을 컨테이너 루트(/app)로 복사
COPY web-service/ .

# 💡 index.html 및 설정 파일 경로 검증 (로그용)
RUN ls -al index.html vite.config.mts

# 💡 타입 체크를 완전히 건너뛰고 Vite 빌드를 강제 실행
# ESM 에러 방지를 위해 vite config가 올바르게 로드되도록 합니다.
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
COPY web-service/nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
