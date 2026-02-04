from flask import Flask
import time

# Flask App 생성
app = Flask(__name__)

# 앱의 상태를 저장하는 전역 변수
is_healthy = True

@app.route("/")
def hello():
    return "Hello, DevOps World!"

@app.route("/health")
def health_check():
    if is_healthy:
        return "OK", 200
    else:
        #상태가 좋지 않을 때 500 에러 반환
        return "Internal Server Error", 500

@app.route("/make-zombie")
def make_zombie():
    global is_healthy
    is_healthy = False
    return "App is now in Zombie state (Health check will fali)", 200

if __name__ == "__main__":
    # 0.0.0.0으로 바인딩해야 Docker 컨테이너 외부에서 접근 가능
    app.run(host="0.0.0.0", port=80)