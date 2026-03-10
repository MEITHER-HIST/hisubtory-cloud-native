# 🛠 인프라 복구 및 MSA 전환 트러블슈팅 리포트

**일시:** 2026년 3월 10일  
**목표:** 꼬여있는 인프라 복구 및 명세서에 따른 3개 마이크로서비스(User, Story, Activity) 체제 전환

---

## 1. 접속 및 초기 동기화 문제

### [오류 1] ALB 접속 불가 (NXDOMAIN) 및 Bastion SSH 타임아웃
*   **증상:** ALB DNS 주소 해석 안 됨, 기존 Bastion IP(`43.202.54.108`) 접속 불가.
*   **원인:** 실제 인프라가 수동 삭제되거나 변경되어 테라폼 상태 파일(`tfstate`)과 불일치 발생.
*   **해결:** 
    1. `terraform apply`를 통해 Bastion 재생성.
    2. 새로운 Bastion IP(`3.36.72.213`) 확인.
    3. Amazon Linux 2 AMI 특성에 따라 사용자명을 `ubuntu`에서 **`ec2-user`**로 변경하여 접속 성공.

### [오류 2] 리소스 중복 생성 에러 (AlreadyExists)
*   **증상:** ALB, ECR, ECS 서비스 생성 시 "이미 존재함" 에러 발생.
*   **원인:** 콘솔에 이미 수동으로 만든 리소스들이 있으나 테라폼은 이를 인지하지 못함.
*   **해결:** **`terraform import`** 전략 사용.
    *   `ECR`, `ECS Cluster`, `ECS Service`, `ALB Target Group` 등 주요 자원들을 테라폼 장부에 강제로 등록하여 동기화 완료.

---

## 2. 인프라 정리 및 삭제 문제

### [오류 3] ECR 저장소 삭제 실패 (RepositoryNotEmptyException)
*   **증상:** 임시 저장소(`hisubtory-app`) 삭제 중 내부 이미지가 있어 삭제 거부됨.
*   **원인:** 테스트용 Nginx 이미지가 저장소 안에 남아 있음.
*   **해결:** AWS CLI를 사용하여 강제 삭제 옵션(`--force`)으로 저장소 비우기 및 삭제 완료.

### [오류 4] 타겟 그룹 삭제 실패 (ResourceInUse)
*   **증상:** 옛날 타겟 그룹(`web_tg`) 삭제 시 리스너가 사용 중이라며 거부됨.
*   **원인:** ALB 리스너의 **기본 액션(Default Action)**이 해당 타겟 그룹을 바라보고 있음.
*   **해결:** 
    1. 리스너의 기본 액션을 `Fixed-Response 404`로 강제 변경 (CLI 활용).
    2. 연결이 끊긴 `web_tg`를 테라폼이 안전하게 삭제하도록 처리.

---

## 3. ALB 리스너 규칙 충돌 문제

### [오류 5] 규칙 수정 시 유효성 검사 에러 (ValidationError)
*   **증상:** `You can specify both a target group list and a top-level target group ARN only if the ARNs match` 에러 발생.
*   **원인:** 테라폼 상태 파일의 규칙 메타데이터와 실제 AWS 규칙 설정 방식의 충돌.
*   **해결 (핵심 조치):**
    1. **가위로 자르기**: 문제가 된 리스너 규칙 3개를 AWS 콘솔(CLI)에서 직접 삭제.
    2. **장부 정리**: 테라폼 상태에서 해당 규칙 정보 제거 (`terraform state rm`).
    3. **새로 잇기**: `terraform apply`를 통해 설계도대로 깨끗하게 규칙 재생성 완료.

---

## 4. 데이터베이스(RDS) 잔여 문제

### [오류 6] 보안 그룹 상태 부적절 (InvalidDBSecurityGroupState)
*   **증상:** RDS 보안 그룹 업데이트 시 `Cannot authorize until it has been fully revoked` 발생.
*   **원인:** AWS 내부적으로 보안 그룹 교체 작업(Adding/Removing)이 'Pending' 상태에 멈춰 있음.
*   **해결:** 
    *   이는 AWS 시스템의 작업 완료를 기다려야 하는 문제임.
    *   **현재 상태:** DB 서비스 자체는 정상(Available)이며, 인프라 동맥(ALB-ECS) 연결에는 지장이 없음을 확인. 추후 시간이 경과한 뒤 `terraform apply` 시 자동 해결될 예정.

---

## 🏁 최종 결과
*   **인프라 구조:** 단일 EC2 방식에서 **ECS Fargate MSA** 체제로 100% 전환 성공.
*   **경로 기반 라우팅:** `/api/user/*`, `/api/stories/*`, `/api/activity/*` 경로가 각각의 독립된 서비스로 정상 연결됨.
*   **관리 효율성:** 모든 수동 자원이 테라폼 관리 하에 들어와 향후 `apply` 한 번으로 형상 관리가 가능해짐.
