# 장애 대응 런북 (Runbook)

## 1. 장애 인지 및 초기 대응
1. **Grafana 대시보드** 접속하여 지연 시간(Latency) 및 에러율(Error Rate) 급증 확인.
2. Portainer 또는 `docker ps`를 통해 컨테이너 중단 여부 확인.

## 2. 원인 파악 순서 (Troubleshooting)

### Step 1: 통합 로그 추적 (Loki)
- Grafana의 **Explore** 메뉴에서 `Loki` 선택.
- `{container="hisubtory-user"}` 필터를 사용하여 특정 서비스의 `Internal Server Error` 상세 로그 확인.

### Step 2: 분산 트레이싱 (Jaeger)
- `http://<Server-IP>:16686` 접속.
- 서비스 간 지연이 발생하는 특정 API 요청 선택.
- 어느 구간(Nginx -> Service -> DB)에서 병목이 발생하는지 타임라인 확인.

## 3. 조치 및 복구
- **일시적 오류:** `docker compose restart <service-name>` 명령어로 개별 서비스 재시작.
- **코드 오류 배포 시:** 이전 안정 버전 브랜치(`de`)로 롤백 후 재배포.
- **DB 연결 오류:** Supabase 또는 RDS 연결 설정(`.env`) 및 네트워크 상태 확인.

## 4. 백업 및 롤백 매뉴얼
- 매일 주기적으로 백업되는 Git 브랜치를 활용하여 소스 코드 복구.
- 데이터베이스는 Cloud(Supabase/AWS)의 자동 스냅샷 기능 활용.
