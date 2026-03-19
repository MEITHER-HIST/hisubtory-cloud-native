# HISUBTORY Frontend (React)

지하철 역 기반 역사 숏스토리(웹툰) 서비스 **HISUBTORY**의 프론트엔드 레포지토리입니다.  
서비스 기능 소개보다 **AWS 인프라 설계 + 배포 자동화 + 운영 안정성(Front/Back 분리)** 관점에 맞춰 구성했습니다.

---

## 🧭 Overview

- **Frontend**: React (Vite)
- **Build & Serve**: `npm run build` 산출물(`dist/`)을 **Nginx가 정적 서빙**
- **API 연동**: Front 서버에서 `/api/*` 요청을 **Reverse Proxy**로 Backend로 전달
- **Images/Static**: 브라우저가 **CloudFront(S3 origin)** 로 직접 이미지 요청 (API는 JSON만 제공)
- **CI/CD**: GitHub Actions → AWS CodeDeploy → Front EC2 자동 배포

---

## 🏗 Architecture (High-level)

### Request Flow
1. Client → (ALB) → **Front EC2 (Nginx + React build)**
2. React 앱에서 `/api/*` 호출 → **Nginx Reverse Proxy** → Backend API
3. Backend는 JSON 응답에 `image_url`(CloudFront URL) 포함 → 브라우저가 **CloudFront**로 이미지 GET
4. CloudFront → S3(Origin)에서 이미지 제공 (캐시 Hit/Miss)

> **핵심**: 프론트는 “화면 렌더링 + 정적 파일 제공”, 백엔드는 “JSON API 제공”으로 역할을 분리했습니다.

---

## ✅ What this Front Server does

- React 빌드 산출물(`dist/`) **정적 서빙**
- SPA 라우팅을 위한 `try_files ... /index.html` 처리
- `/api/` 경로를 Backend로 전달하는 **Reverse Proxy**
- (선택) `/health` 같은 간단 헬스 체크 엔드포인트 제공

---

## 📁 Repo Structure (example)

> 프로젝트 구조에 맞게 실제 폴더명은 조정해서 사용하세요.
```
.
├─ src/
├─ public/
├─ vite.config.ts
├─ package.json
├─ appspec.yml
├─ scripts/
│ ├─ before_install.sh
│ ├─ after_install.sh
│ └─ application_start.sh
└─ dist/ # build output (배포 아티팩트에 포함)
```
---

## ⚙️ Local Development

### 1) Requirements
- Node.js 18+ 권장
- npm 9+ 권장

### 2) Install & Run
```bash
npm install
npm run dev
```

### 3) Dev 환경에서 API 연결(권장)

개발 서버에서 /api를 백엔드로 프록시하면 CORS 문제를 줄일 수 있습니다.

vite.config.ts 예시:
``` ts
export default defineConfig({
  server: {
    proxy: {
      "/api": "http://127.0.0.1:8000",
    },
  },
});
```

---

## 🔧 Environment Variables (Optional)

Vite 환경변수는 `VITE_`로 시작해야 합니다. (`import.meta.env.VITE_*`로 접근)

> ⚠️ 보안 주의: `.env`는 커밋하지 마세요. (`.gitignore`에 추가)

### (1) API Base URL (선택)
- 프론트에서 API를 절대경로로 호출할 때 사용합니다.
- **Nginx에서 `/api` 리버스 프록시를 쓰면** 굳이 필요 없고, 상대경로(`/api/...`)로 호출하는 게 깔끔합니다.

```env
VITE_API_BASE_URL=http://hisub-alb-xxxx.ap-northeast-2.elb.amazonaws.com
```
🔎 설명
- `VITE_API_BASE_URL`: API 요청 기본 URL  
  - 예: `http://hisub-alb-xxxx.ap-northeast-2.elb.amazonaws.com`  
  - 코드 예시: `fetch(`${import.meta.env.VITE_API_BASE_URL}/api/...`)`

---
### (2) CloudFront Domain (선택)

- 이미지 URL을 프론트에서 **직접 조합해야 하는 경우에만** 사용합니다.  
- 보통은 **백엔드가 JSON에 `image_url`을 내려주면**, 프론트는 그 값을 그대로 렌더링하면 됩니다.

```env
VITE_CLOUDFRONT_DOMAIN=d27nsin45nib0r.cloudfront.net
```
🔎 설명
- `VITE_CLOUDFRONT_DOMAIN`: 이미지 CDN 도메인(CloudFront)  
  - 예: `d27nsin45nib0r.cloudfront.net`  
  - 이미지 URL 조합이 필요할 때만 사용(대부분은 백엔드 JSON의 `image_url`을 그대로 사용)

---

### (3) Build Mode (선택)

배포 환경에 따라 분기 렌더링/로그를 제어하고 싶을 때 사용합니다.
``` env
VITE_APP_ENV=prod
```
🔎 설명
- VITE_APP_ENV: dev / stage / prod 등 임의로 정의해서 사용

---

## 🚀 Build & Deploy (CodeDeploy)

### Build
```bash
npm run build
```
- 빌드 산출물은 기본적으로 `dist/`에 생성됩니다.
- 배포 시 Nginx가 `dist/`를 정적 파일로 서빙합니다.

### 배포 아티팩트 포함 항목(예시)
- `dist/` (필수)
- `appspec.yml` (필수)
- `scripts/` (hooks, 필수)

---

## 🌐 Nginx (Front EC2) 핵심 설정 포인트

### 1) SPA 라우팅 처리

새로고침 시에도 React 라우트가 동작하도록 `try_files`를 사용합니다.

```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```
### 2) API Reverse Proxy (선택)

프론트 도메인에서 `/api/`로 들어온 요청을 백엔드로 전달합니다.

```nginx
location /api/ {
  proxy_pass http://<BACKEND_HOST>:8000;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
}
```
> <BACKEND_HOST>는 내부 IP 또는 NLB DNS 등, 실제 구성에 맞게 적용하세요.
---

## ✅ Request Flow (Summary)

1. User → (ALB) → **Front EC2 (Nginx)**
2. Nginx → `dist/` 정적 서빙 (React build)
3. `/api/*` 요청은 Nginx가 Backend로 프록시
4. 이미지는 JSON의 `image_url`을 통해 **CloudFront → S3**로 로딩

---

## 🧪 Quick Check

- 프론트 서버 헬스 체크(선택 구현): `GET /health` → `200 OK`
- API 호출 확인: `GET /api/...` → `200 OK` (JSON)
- 이미지 로딩 확인: `GET https://<cloudfront>/media/...png` → `200 OK` (+ `X-Cache` 확인)