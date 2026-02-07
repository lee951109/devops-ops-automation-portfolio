# 🏁 AWS Ops-Automation Pipeline: 최종 기술 보고서

## 1. 프로젝트 개요 (Overview)
본 프로젝트는 **"1인 DevOps 엔지니어를 위한 무중단 운영 자동화"**를 목표로 합니다.
Terraform을 이용한 인프라 프로비저닝(IaC)부터, Python 기반의 비용 최적화 로직, Slack ChatOps를 통한 제어, 그리고 GitHub Actions를 활용한 CI/CD 파이프라인까지 **End-to-End 자동화**를 구현했습니다.

* **Repository**: [https://github.com/lee951109/devops-ops-automation-portfolio](https://github.com/lee951109/devops-ops-automation-portfolio)
* **Role**: 1인 개발 (Infrastructure, Backend, DevOps)

## 2. 아키텍처 (Architecture)
시스템은 크게 **제어 계층(GitHub/Slack)**, **컴퓨팅 계층(EC2/Systemd)**, **리소스 계층(AWS Cloud)**으로 구성됩니다.

### 데이터 흐름
1. **Developer**가 코드를 Push하면 **GitHub Actions**가 트리거됩니다.
2. **GitHub Actions**는 SSH를 통해 **EC2**에 접속하여 최신 코드를 배포(Git Pull)하고 서비스를 재시작합니다.
3. **EC2(OpsBot)**은 **Systemd**에 의해 24/7 구동되며, **Slack Socket Mode**로 명령을 대기합니다.
4. 사용자가 명령("점검")을 내리면 **AWS SDK(Boto3)**가 미사용 리소스(EBS, EIP)를 탐지하여 보고합니다.

## 3. 핵심 기술 스택 (Tech Stack)
| 분류 | 기술 | 선정 이유 |
| :--- | :--- | :--- |
| **IaC** | **Terraform** | 인프라 형상 관리 및 재사용성 확보 (Standard VPC, EC2) |
| **Language** | **Python (Boto3)** | AWS 리소스 제어 라이브러리가 가장 풍부하고 간결함 |
| **Interface** | **Slack Bolt SDK** | **Socket Mode**를 사용하여 방화벽(Inbound Port) 개방 없이 안전한 양방향 통신 구현 |
| **CI/CD** | **GitHub Actions** | 별도 Jenkins 서버 구축 없이 GitHub 레포지토리와 즉시 연동되는 관리형 파이프라인 사용 |
| **OS Mgmt** | **Systemd** | 단순 스크립트 실행이 아닌, OS 레벨의 프로세스 자동 재시작(Auto-restart) 및 생명주기 관리 |

## 4. 주요 트러블슈팅 (Troubleshooting Log)

### 🔴 Issue 1: AWS 권한 관리 (Security)
* **문제**: Boto3 실행 시 `NoCredentialsError` 발생. Access Key를 코드에 하드코딩하는 것은 보안상 위험.
* **해결**: AWS **IAM Role**을 생성하여 EC2 인스턴스에 부여(`AmazonEC2ReadOnlyAccess`). 코드 수정 없이 안전하게 권한을 획득하는 **Best Practice** 적용.

### 🔴 Issue 2: Systemd 환경 변수 격리 (OS)
* **문제**: 터미널에선 작동하던 봇이 Systemd 서비스 등록 후 `KeyError: 'SLACK_APP_TOKEN'` 발생.
* **원인**: 리눅스 쉘(Shell)의 `export` 변수는 Systemd 데몬 환경으로 상속되지 않음.
* **해결**: `.service` 파일 내 `[Service]` 섹션에 `EnvironmentFile` 또는 `Environment` 키워드로 변수를 명시적으로 주입하여 해결.

### 🔴 Issue 3: CI/CD 배포 경로 불일치 (Deployment)
* **문제**: GitHub Actions 배포 시 `No such file or directory` 에러 발생.
* **원인**: 로컬 개발 환경(Windows Git Bash)의 경로 표기법(`/d/...`)을 리눅스 서버에 그대로 적용함.
* **해결**: EC2 서버의 절대 경로(`/home/ec2-user/...`)를 파악하여 배포 스크립트를 표준화함.

## 5. 결론 및 성과
* **비용 절감**: 잊혀진 EBS 볼륨 및 EIP를 즉시 탐지하여 클라우드 비용 낭비 방지.
* **운영 효율성**: 터미널 접속 없이 슬랙(Slack)만으로 인프라 상태 점검 가능.
* **배포 자동화**: 코드 수정부터 실서버 반영까지 **1분 미만** 소요 (Zero-Touch Deployment 달성).