import boto3 # AWS 조작용 라이브러리
import os
import requests

# 슬랙 설정 (기존 환경 변수 활용)
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_report(message):
    if SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})

def check_unused_ebs():
    # EC2 서비스에 연결 (리전은 내가 사용하는 곳으로 설정)
    ec2 = boto3.resource('ec2', region_name='ap-northeast-2')

    unused_volumes = []

    # 모든 볼륨을 하나씩 확인
    for volume in ec2.volumes.all():
        # 상태가 'available'이면 아무 EC2에도 연결 안 된 상태
        if volume.state == 'available':
            unused_volumes.append(f"- 볼륨 ID: {volume.id} ({volume.size}GB)")

    return unused_volumes

if __name__ == "__main__":
    print("미사용 EBS 자원 점검 시작...")
    unused_list = check_unused_ebs()

    if unused_list:
        report = "[비용 최적화 알림] 사용하지 않은 EBS 볼륨이 발견되었습니다!\n"
        report += "\n".join(unused_list)
        report += "\n\n불필요하다면 삭제하여 비용을 절감하세요."

        print(report)
        send_slack_report(report)
    else:
        print("모든 자원이 정상 사용 중입니다.")