
# Python 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 먼저 복사
# (캐시 활용을 위해 코드보다 먼저 복사)
COPY requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app.py .

# 컨테이너가 사용하느 포트
EXPOSE 80

# 컨테이너 실행 시 Flask 앱 실행
CMD ["python", "app.py"]