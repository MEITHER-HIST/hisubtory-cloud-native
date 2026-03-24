# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장 및 Vite 에러 방지용 환경 변수
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
ENV CI=false

WORKDIR /app

# 💡 GitHub Actions 컨텍스트인 프로젝트 루트(.)를 기준으로 파일을 정확히 복사합니다.
# package.json 복사
COPY web-service/package*.json ./

# 💡 피어 의존성 무시 및 유연한 설치
RUN npm install --legacy-peer-deps

# 💡 web-service 폴더 내의 모든 소스 파일(index.html, src 등)을 컨테이너 루트(/app)로 복사
COPY web-service/ .

# 💡 이제 index.html이 확실히 루트에 있는지 로그로 확인
RUN ls -al index.html

# 💡 타입 체크 건너뛰고 Vite 빌드 실행
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사 (정확한 경로 참조)
COPY web-service/nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
