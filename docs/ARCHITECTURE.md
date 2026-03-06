# Hisubtory 아키텍처 및 API 명세서

## 1. 서비스 분리 논거 및 책임 범위
본 프로젝트는 도메인 주도 설계(DDD)를 기반으로 3개의 독립적인 마이크로서비스로 분리되었습니다.

| 서비스명 | 책임 범위 | 데이터베이스 | 주요 특징 |
| :--- | :--- | :--- | :--- |
| **User** | 회원가입, 인증(JWT), 프로필 관리 | Supabase (PostgreSQL) | 외부 Auth 서비스 연동 및 보안 강화 |
| **Story** | 웹툰, 에피소드, 지하철 역 데이터 관리 | AWS RDS (MySQL) | 읽기 최적화 및 대용량 이미지 메타데이터 관리 |
| **Activity** | 북마크, 시청 기록, 개인 라이브러리 | AWS RDS (MySQL) + Redis | 쓰기 빈도가 높으며 캐싱을 통한 성능 최적화 |

## 2. API 명세 (Gateway: Port 80)

### 2.1 User Service (`/api/user/`)
- `POST /api/user/accounts/signup/`: 회원가입
- `POST /api/user/accounts/login/`: 로그인 및 토큰 발급
- `GET /api/user/accounts/profile/`: 사용자 정보 조회

### 2.2 Story Service (`/api/stories/`)
- `GET /api/stories/webtoons/`: 전체 웹툰 목록 조회
- `GET /api/stories/episodes/{id}/`: 에피소드 상세 및 컷 데이터 조회
- `GET /api/stories/subway/stations/`: 역별 스토리 매핑 정보

### 2.3 Activity Service (`/api/bookmarks/`, `/api/activity/`)
- `POST /api/bookmarks/`: 즐겨찾기 추가/삭제
- `GET /api/activity/history/`: 최근 본 에피소드 목록 조회

## 3. 에러 코드 정의
- `400 Bad Request`: 요청 파라미터 누락 또는 유효성 검사 실패
- `401 Unauthorized`: 인증 토큰 만료 또는 유효하지 않음
- `404 Not Found`: 존재하지 않는 엔드포인트 또는 리소스
- `500 Internal Server Error`: 마이크로서비스 내부 오류 (Jaeger 추적 필요)
