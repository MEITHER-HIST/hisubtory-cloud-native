# 🚇 Hisubtory (하이섭토리) - Cloud Native Infrastructure

본 저장소는 지하철 역 기반 스토리텔링 서비스 'Hisubtory'의 마이크로서비스 인프라 및 배포 환경을 관리합니다.

## 🚀 시스템 접속 정보 (Dashboards)

모든 대시보드는 현재 운영 서버에서 실시간으로 가동 중입니다.

| 서비스 | 접속 주소 | 용도 | 비고 |
| :--- | :--- | :--- | :--- |
| **Main API** | [http://112.221.198.140](http://112.221.198.140) | 전체 서비스 게이트웨이 | /api/user, /api/stories 등 |
| **Grafana** | [http://112.221.198.140:3000](http://112.221.198.140:3000) | 통합 모니터링 (메트릭/로그) | 초기 ID: admin / admin |
| **Portainer** | [http://112.221.198.140:9000](http://112.221.198.140:9000) | 도커 컨테이너 시각적 관리 | 컨테이너 재시작/로그 확인 |
| **Jaeger** | [http://112.221.198.140:16686](http://112.221.198.140:16686) | 분산 트레이싱 (지연 시간 추적) | 서비스 간 병목 구간 확인 |
| **Prometheus** | [http://112.221.198.140:9090](http://112.221.198.140:9090) | 원천 메트릭 데이터 조회 | Prometheus Query 전용 |

---

## 📄 주요 기술 및 운영 문서

프로젝트 운영 및 개발을 위한 상세 명세서입니다.

1.  **[서비스 아키텍처 및 API 명세](./docs/ARCHITECTURE.md)**: 도메인 분리 기준 및 엔드포인트 구조
2.  **[SLO 및 가용성 명세서](./docs/SLO_SLA.md)**: 서비스 성능 목표 및 가용성 기준
3.  **[장애 대응 런북 (Runbook)](./docs/RUNBOOK.md)**: 문제 발생 시 Loki/Jaeger 활용 추적 가이드

---

## 🛠 인프라 특징
- **Microservices**: User, Story, Activity 서비스 독립 배포
- **Multi-stage Build**: Docker 이미지 최적화 및 보안 강화
- **Observability**: Prometheus, Loki, Jaeger를 통한 Full-stack 관측성 확보
- **Database**: Supabase(PostgreSQL) 및 AWS RDS(MySQL) 혼합 구성
