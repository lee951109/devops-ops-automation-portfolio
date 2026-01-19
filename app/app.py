from flask import Flask, jsonify

# Flask App 생성
app = Flask(__name__)

@app.route("/health")
def health_check():
    """
    Health Check 엔드포인트
    - 모니터링 스크립트가 이 URL을 호출해서
      서비스 정상 여부를 판단한다.
    """
    return jsonify(status="ok"), 200

@app.route("/")
def index():
    """
    기본 페이지
    - 단순히 서비스가 실행 중임을 확인하기 위한 용도
    """
    return "Ops automation target app is running", 200

if __name__ == "__name__":
    # 0.0.0.0으로 바인딩해야 Docker 컨테이너 외부에서 접근 가능
    app.run(host="0.0.0.0", port=80)