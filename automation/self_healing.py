import subprocess
import time
import requests
import json
from datetime import datetime
import os


# 모니터링할 대상 컨테이너 이름
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
TARGET_CONTAINER = "ops-target"

if not SLACK_WEBHOOK_URL:
    print("[Error] Salck Webhook URL이 설정되지 않았습니다! 환경 변수를 확인하세요.")

def send_slack_message(message):
    """Slack으로 메시지 전송"""
    headers = {'Content=Type': 'application/json'}
    payload = {"text": message}

    try:
        # json=payload 를 사용하면 Content-Type과 dumps를 알아서 처리
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)

        if response.status_code != 200:
            print(f"[Warning] Slack send failed: {response.status_code}, Reason: {response.text}")
    except Exception as e:
        print(f"[Warning] Slack error: {e}") 

def check_container_status(container_name):
    """컨테이너가 실행 중인지 확인(True/False)"""
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
            universal_newlines=True
        ).strip()
        return output == "true"
    except subprocess.CalledProcessError:
        return False

def restart_container(container_name):
    """죽은 컨테이너를 재시작하고 알림 발송"""
    # 1. 감지 로그
    msg_down = f"[Emergency] '{container_name}' is down! ({datetime.now()})"
    print(msg_down, flush=True)
    send_slack_message(msg_down) # Slack 전송

    try:
        # 2. 복구 시도
        subprocess.run(["docker", "restart", container_name], check=True)

        # 3. 성공 로그        
        msg_up = f"[Resolved] {container_name} has been restared successfully."
        print(msg_up, flush=True)
        send_slack_message(msg_up)

    except Exception as e:
        # 4. 실패 로그
        msg_fail = f"[Critical] Failed to restart {container_name}: {e}"
        print(msg_fail, flush=True)
        send_slack_message(msg_fail)

if __name__ == "__main__":
    start_msg = f"Monitoring started for: {TARGET_CONTAINER}"
    print(start_msg, flush=True)
    send_slack_message(start_msg)

    while True:
        if not check_container_status(TARGET_CONTAINER):
            restart_container(TARGET_CONTAINER)
        else:
            # 정상일 때는 로그만 남기고 슬랙은 안 보냄.(너무 많이 보내지기떄문)
            print(f"{TARGET_CONTAINER} is running healthy", flush=True)

        # 10초마다 체크 (테스트용이니까)
        time.sleep(10)