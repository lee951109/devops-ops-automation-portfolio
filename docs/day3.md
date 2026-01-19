# Day 3 - 운영 대상 애플리케이션 컨테이너화 + 실행 이슈 정리

오늘은 운영 자동화의 "대상"이 될 애플리케이션을 만들고, EC2에서 Docker로 실제 실행까지 해보는 날이었다.

목표는 서비스 자체를 잘 만드는게 아니라,
앞으로 Python 모니터링/자동 조치가 판단할 기준점을 만드는 것이었다.
그래서 `/health` 엔드포인트를 가진 아주 단순한 Web App을 준비했다.

---

## 오늘 한 작업

- Flask(파이썬 웹 프레임워크)로 최소 Web App 작성
  - `/health` 엔드포인트: 정상 상태 확인용(200 OK) 
- Dockerfile 작성 후 이미지 빌드
- EC2에서 Docker로 컨테이너 실행 시도

--- 

## 발생한 문제: 컨테이너가 바로 종료됨(Exited)

EC2에서 `docker ps -a`로 확인하니 컨테이너가 `Exited (0)` 상태였다.
특이하게도 `docker logs`에 로그가 없었다.

정리하면
- 컨테이너는 에러 로그 없이 종료
- 포트(80)도 떠있지 않음
- 브라우저에서 접근해도 당연히 응답 없음

즉 "웹 서버 프로세스가 컨테이너 안에서 계속 떠 있어야 하는데, 그게 유지되지 않았다"는 문제였다.

---

## 해결 방향: Flask 개발 서버 대신 Gunicorn(WSGI 서버) 사용

컨테이너 환경에서는 Flask의 개발 서버 (`app.run`)대신 Gunicorn 같은 Web Service Gateway Interface 서버로 실행하는 방식이 더 안정적이다.

그래서 다음과 같이 바꾸는 쪽으로 방향을 잡았다.

- requirements.txt에 `gunicorn` 추가
- Dockerfile의 CMD를 `python app.py`에서 `gunicorn --bind 0.0.0.0:80 app:app`로 변경

이 방식은 운영 환경에서 흔히 쓰는 형태라고 한다.