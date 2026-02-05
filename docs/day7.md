# Day 7: AWS 비용 최적화 및 운영 자동화 시스템 (Cost Optimization System)

## 1. 개요
클라우드 운영 비용(OpEx) 절감을 위해, 인스턴스 종료 후 방치되기 쉬운 **미사용 자원(Unused Resources)**을 자동으로 탐지하고 관리자에게 정기 리포팅하는 시스템을 구축함.

## 2. 시스템 아키텍처
- **언어 및 라이브러리**: Python 3.11, AWS SDK for Python (Boto3)
- **실행 환경**: AWS EC2 (Amazon Linux 2023)
- **스케줄링**: Linux Crontab (매일 09:00 자동 실행)
- **알림 채널**: Slack Incoming Webhook
- **보안 구성**: IAM Role (`AmazonEC2ReadOnlyAccess`)을 사용하여 Access Key 노출 없는 안전한 권한 제어 구현.

## 3. 핵심 기능 및 구현 로직

### 3.1. 탐지 대상 리소스
비용 누수가 가장 빈번한 두 가지 리소스를 추적 대상으로 선정.

1.  **EBS 볼륨 (Elastic Block Store)**
    -   **탐지 조건**: `State == 'available'`
    -   **설명**: 인스턴스와 연결이 해제되어 어떤 서버에서도 사용하지 않는 유휴 볼륨.
2.  **Elastic IP (EIP)**
    -   **탐지 조건**: `AssociationId` 또는 `InstanceId` 속성 부재.
    -   **설명**: 할당은 받았으나 실행 중인 인스턴스에 연결되지 않아 비용이 발생하는 고정 IP.

### 3.2. 자동화 구성 (Cron)
-   **스케줄**: 매일 오전 9시 (KST 기준 서버 시간 확인 필요)
-   **환경 변수 주입**: Crontab은 쉘 환경 변수를 로드하지 않으므로, 실행 구문 내에 `export SLACK_WEBHOOK_URL=...`을 명시하여 보안성과 동작성을 동시에 확보.
-   **로그 관리**: 표준 출력 및 에러를 로그 파일(`cost.log`)로 리다이렉션하여 실행 이력 추적.

## 4. 트러블슈팅 (Troubleshooting)

### 이슈 1: 인스턴스 가용 영역(AZ) 불일치
-   **현상**: 비용 절감을 위해 `t3.micro`에서 프리티어인 `t2.micro`로 변경 시, `ap-northeast-2d` 영역에서 생성 실패.
-   **원인**: 서울 리전의 D존은 비교적 최신 데이터센터로, 구형 인스턴스 타입(`t2`)을 물리적으로 지원하지 않음.
-   **해결**: Terraform 코드에서 Subnet 필터를 수정하여 `ap-northeast-2a`, `ap-northeast-2c`로 배치 변경.

### 이슈 2: Crontab 미동작
-   **현상**: 스케줄 설정 후에도 스크립트가 실행되지 않음.
-   **원인**: EC2(Amazon Linux 2023)에서 `crond` 서비스가 기본적으로 비활성화(`inactive`) 상태임.
-   **해결**: `sudo systemctl start crond` 및 `enable` 명령어로 데몬 활성화.
-   **교훈**: 자동화 스크립트 구현뿐만 아니라, 이를 구동하는 OS 레벨의 데몬 상태 점검이 필수적임.

## 5. 향후 고도화 계획 (Next Step)
-   **원클릭 삭제 (ChatOps)**: Slack 알림 메시지에 [삭제] 버튼을 추가하여, 모바일에서도 즉시 리소스를 정리할 수 있도록 기능 확장 예정.