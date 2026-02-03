import subprocess
import time

# 모니터링할 대상 컨테이너 이름
TARGET_CONTAINER = "my-app"

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
    """죽은 컨테이너를 재시작"""
    print(f"[Waning] {container_name} is down! Attempting to restart...")
    try:
        subprocess.run(["docker", "restart", container_name], check=True)
        print(f"[Success] {container_name} has been restared.")
    except Exception as e:
        print(f"[Error] Failed to restart {container_name}: {e}")

if __name__ == "__main__":
    print(f"Monitoring started for: {TARGET_CONTAINER}")
    while True:
        if not check_container_status(TARGET_CONTAINER):
            restart_container(TARGET_CONTAINER)
        else:
            print(f"{TARGET_CONTAINER} is running healthy")

        # 10초마다 체크 (테스트용이니까)
        time.sleep(10)