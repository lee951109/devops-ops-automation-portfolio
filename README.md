# DevOps 운영 자동화 포트폴리오

이 프로젝트는 Kubernetes 없이,
EC2 환경에서 실제 운영 자동화를 어떻게 구현할 수 있는지에 초점을 둔 포트폴리오다.

이미 Kubernetes와 GitOps는 다른 포트폴리오에서 충분히 다뤘기 때문에  
이번에는 추상화를 줄이고,  
운영 중 발생하는 문제를 Python 코드로 직접 감지하고 대응하는 데 집중한다.

---

## 프로젝트 목표

- 운영 중인 서버 상태를 코드로 감지한다
- 장애 발생 시 사람이 아닌 코드가 먼저 반응한다
- 비용을 고려한 운영 종료(destroy)까지 포함한다

---

## 사용 기술

- AWS EC2 (Elastic Compute Cloud)
- Docker (컨테이너 실행 환경)
- Python (운영 자동화 및 모니터링)
- Terraform (Infrastructure as Code)

---

## 디렉토리 구조

```text
devops-ops-automation-portfolio/
├─ infra/        # Terraform (EC2 생성)
├─ app/          # Docker 기반 애플리케이션
├─ monitoring/   # Python 모니터링 스크립트
├─ automation/   # 자동 조치 스크립트
├─ scripts/      # start / stop / destroy
├─ docs/         # Day별 정리 및 블로그 초안
└─ README.md
```

## 왜 Kubernetes를 사용하지 않았는가

Kubernetes는 이미 이전 포트폴리오에서 사용해봤다.
이번 프로젝트에서는 오히려 추상화를 줄이고,
운영 중 서버에서 실제로 어떤 일이 벌어지는지를 더 직접적으로 다루고 싶었다.

DevOps에서 중요한 건 도구의 화려함이 아니라,
문제를 인식하고 자동화로 풀어내는 능력이라고 생각한다.
