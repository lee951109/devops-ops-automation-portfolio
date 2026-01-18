# Day 1 – 포트폴리오 방향 정리

오늘은 바로 코드를 치기보다는  
이번 포트폴리오를 왜 만드는지부터 정리했다.

이미 Kubernetes 기반 포트폴리오는 갖고 있기 때문에,  
이번에는 운영 자동화 그 자체에 집중하기로 했다.

EC2 위에서 Docker로 서비스 하나 올리고,  
그걸 Python 코드가 감시하고,  
문제가 생기면 자동으로 반응하게 만드는 구조가 목표다.

내가 만들고 싶은 건  
“잘 돌아가는 인프라”가 아니라  
“문제가 생겨도 스스로 반응하는 운영 환경”이다.


## EC2 인프라 최소 구성 (Terraform)

오늘은 운영 자동화의 “대상 서버”를 먼저 만들었다.
Kubernetes 없이 가는 대신, EC2(Elastic Compute Cloud)에서 실제 운영 흐름을 단순하게 드러내는 게 목표다.

- Terraform으로 EC2 1대 생성
- Security Group(보안 그룹)에서 SSH(Secure Shell) 22 포트는 내 IP만 허용
- HTTP(Hypertext Transfer Protocol) 80 포트는 이후 서비스 테스트를 위해 열어둠

중요한 건 테스트 끝나면 바로 terraform destroy로 비용을 정리하는 것.
