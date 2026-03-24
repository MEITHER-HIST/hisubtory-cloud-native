# Stage 1: Build
FROM node:22-alpine AS build

# 빌드 시 메모리 제한 확장 및 Vite 에러 방지용 환경 변수
ENV NODE_OPTIONS="--max-old-space-size=4096"
ENV VITE_API_URL="/api"
ENV CI=false

WORKDIR /app

# 💡 빌드 컨텍스트가 루트(.)이므로, web-service 폴더 내의 파일을 명시적으로 가져옵니다.
# (루트에서 빌드되든, 폴더에서 빌드되든 안전하게 복사)
COPY package*.json ./
COPY web-service/package*.json ./

# 💡 피어 의존성 무시 및 유연한 설치
RUN npm install --legacy-peer-deps

# 💡 모든 소스 파일을 복사한 후, web-service 하위 파일을 /app 루트로 이동시켜 빌드 환경을 정렬합니다.
COPY . .
# 만약 web-service 폴더가 있다면 그 내부 파일들을 현재 위치(/app)로 끌어올립니다.
RUN if [ -d "web-service" ]; then cp -r web-service/* . && cp web-service/index.html . 2>/dev/null || true; fi

# 💡 이제 index.html이 확실히 루트에 있는지 확인합니다.
RUN ls -al index.html

# 💡 타입 체크 건너뛰고 Vite 빌드 실행
RUN npx vite build --emptyOutDir

# Stage 2: Serve
FROM nginx:stable-alpine
# 빌드 결과물(build)을 Nginx 경로로 복사
COPY --from=build /app/build /usr/share/nginx/html
# Nginx 설정 파일 복사
# (web-service 내부에 있던 설정 파일을 정확히 참조)
COPY web-service/nginx/default.conf /etc/nginx/conf.d/default.conf || COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
