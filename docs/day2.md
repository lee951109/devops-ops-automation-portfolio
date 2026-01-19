# Day 2 – EC2 인프라 최소 구성 (Terraform)

오늘은 운영 자동화의 “대상 서버”를 먼저 만들었다.
Kubernetes 없이 가는 대신, EC2(Elastic Compute Cloud)에서 실제 운영 흐름을 단순하게 드러내는 게 목표다.

- Terraform으로 EC2 1대 생성
- Security Group(보안 그룹)에서 SSH(Secure Shell) 22 포트는 내 IP만 허용
- HTTP(Hypertext Transfer Protocol) 80 포트는 이후 서비스 테스트를 위해 열어둠

중요한 건 테스트 끝나면 바로 terraform destroy로 비용을 정리하는 것.
