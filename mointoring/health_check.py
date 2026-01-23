import requests
import datetime
import os

# ==============================
# 설정 영역
# ==============================

# 운영 대상 서비스 Health Check URL
HEALTH_CHECK_URL = "http://localhost/health"

# 로그 파일 경로
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "health.log")



# ==============================
# 사전 준비
# ==============================

# 로그 디렉토리가 없으면 생성
os.makedirs(LOG_DIR, exist_ok=True)

def write_log(message: str):
    """
    로그 파일에 한 줄 기록
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def check_health():
    """
    /health 엔드포인트 호출 후 상태 판단
    """
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=3)

        if response.status_code == 200:
            write_log("STATUS=OK (200)")
            return True
        else:
            write_log(f"STATUS=ERROR ({response.status_code})")
            return False
        
    except requests.exceptions.RequestException as e:
        # 네트워크 오류, 타임아웃 등
        write_log(f"STATUS=DOWN ({e})")
        return False

if __name__ == "__main__":
    check_health()