# Day 8 - ChatOps 구축 및 시스템 서비스 등록(Slack Bot & Systemd)

## 1. 개요
기존의 단방향 리포팅 시스템을 고도화하여, 운영자가 슬랙(Slack)을 통해 인프라 상태를 능동적으로 점검할 수 있는 **양방향 ChatOps** 환경을 구축함. 또한, 리눅스 `systemd`를 활용하여 프로세스의 무중단 운영 및 자동 복구 체계를 구현함.

## 2. 아키텍처 및 기술 스택
- **Interface**: Slack Bolt SDK (Python) + **Socket Mode**
  - **선정 이유**: Private Networ내에 있는 EC2가 인바운드 포트 개방 없이 안전하게 외부 슬랙 서버와 통신하기 위함.
- **Infrastructure Control**: AWS SDK (Boto3)
- **Process Management**: Linux **Systemd**
  - **선정 이유**: 단순 백그라운드 실행(`&`)과 달리, 프로세스 죽음 감지 시 자동 재시작(Auto-restart) 및 부팅 시 자동 실행을 보장하는 운영체제 표준 방식 채택.
- **Security**: **IAM Role**: (`AmazonEC2ReadOnlyAccess`)
  - **선정 이유**: 소슼 코드 내 Access Key 하드코딩을 방지하고, 인스턴스 단위의 권한 제어를 통해 보안 사고 예방.

## 3. 핵심 구현 내용
1.  **Event Driven Logic**: `@app.message("점검")` 리스너를 통해 사용자의 특정 키워드 명령을 감지하고 `cost_saver` 모듈을 트리거.
2.  **Error Handling**: AWS API 호출 중 발생할 수 있는 예외를 `try-except` 블록으로 처리하여 봇의 비정상 종료 방지.
3.  **Service Registration**: `/etc/systemd/system/opsbot.service` 작성을 통해 애플리케이션을 OS 데몬으로 등록.

## 4. 트러블슈팅 (Troubleshooting)

### 이슈 1: `botocore.exceptions.NoCredentialsError`
- **현상**: 봇 실행 시 AWS 리소스 조회 권한 없음 에러 발생.
- **원인**: EC2 인스턴스에 AWS 자격 증명(Credential)이 설정되지 않음.
- **해결**: IAM Role을 생성하여 EC2에 연결(Attach)함으로써, Key 관리 없이 안전하게 권한 획득 (Security Best Practice).

### 이슈 2: Systemd 실행 시 `KeyError: 'SLACK_APP_TOKEN'`
- **현상**: 수동 실행은 정상이나, `systemctl start`로 실행 시 환경 변수 누락 에러 발생.
- **원인**: 사용자의 Shell Session에 설정된 `export` 변수는 Systemd 데몬 환경으로 상속되지 않음.
- **해결**: `.service` 파일 내 `[Service]` 섹션에 `Environment=KEY=VALUE` 형태로 토큰을 명시하여 해결.

## 5. 결론
언제 어디서든 모바일 기기를 통해 인프라 상태를 점검할 수 있는 **상시 운영 체제(Always-on Operation)**를 확립함.