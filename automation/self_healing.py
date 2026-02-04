import subprocess
import time
import requests
import json
import os
from datetime import datetime

# ==========================================
# 설정 영역
# ==========================================
TARGET_CONTAINER = "ops-target"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
HELATH_CHECK_URL = "http://localhost/health" # Flask 앱의 헬스 체크 경로


def send_slack_message(message):
    """Slack으로 메시지 전송"""

    if not SLACK_WEBHOOK_URL:
        print("[Error] Salck Webhook URL이 설정되지 않았습니다! 환경 변수를 확인하세요.")
        return 
    
    payload = {"text": message}
    try:
        # json=payload 를 사용하면 Content-Type과 dumps를 알아서 처리
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)

        if response.status_code != 200:
            print(f"[Warning] Slack send failed: {response.status_code}, Reason: {response.text}")
    except Exception as e:
        print(f"[Warning] Slack error: {e}") 

def check_container_running(container_name):
    """1단계: 컨테이너 실행 여부 확인"""
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
            universal_newlines=True
        ).strip()
        return output == "true"
    except subprocess.CalledProcessError:
        return False

def check_app_health(url):
    """2단계: 앱 응답 여부 확인 (health_check.py 로직 활용)"""
    # 1. 감지 로그
    try:
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except:
        return False

def restart_with_log(container_name, reason):
    """장애 사유와 함께 재시작 및 알림"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[Emergency] '{container_name}' 장애 감지! \n- 사유: {reason}\n- 시간: {timestamp}"
    print(msg, flush=True)
    send_slack_message(msg)

    try:
        subprocess.run(["docker", "restart", container_name], check=True)
        success_msg = f"[Resolved] '{container_name}' 복구 완료."
        print(success_msg, flush=True)
        send_slack_message(success_msg)
    except Exception as e:
        send_slack_message(f"[Critical] 복구 실패: {e}")


if __name__ == "__main__":
    print(f"통합 모니터링 시작: {TARGET_CONTAINER}", flush=True)

    while True:
        # 인프라(컨테이너) 체크
        if not check_container_running(TARGET_CONTAINER):
            restart_with_log(TARGET_CONTAINER, "컨테이너 중단(Infra Down)")

        # 앱(좀비 프로세스) 체크
        elif not check_app_health(HELATH_CHECK_URL):
            restart_with_log(TARGET_CONTAINER, "앱 응답 없음(Zombie Process)")

        else:
            print(f"{TARGET_CONTAINER} 상태 정상", flush=True)

        # 10초마다 체크 (테스트용이니까)
        time.sleep(10)