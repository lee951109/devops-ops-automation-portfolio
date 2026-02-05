import boto3 # AWS 조작용 라이브러리
import os
import requests
from datetime import datetime

# 슬랙 설정 (기존 환경 변수 활용)
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def send_slack_report(message):
    if SLACK_WEBHOOK_URL:
        requests.post(SLACK_WEBHOOK_URL, json={"text": message})

def check_unused_resources():
    # 리전 설정은 내 환경에 맞게
    ec2 = boto3.resource('ec2', region_name='ap-northeast-2')
    ec2_client = boto3.client('ec2', region_name='ap-northeast-2')

    report = []

   # 1. 미사용 EBS 볼륨 체크
    for volume in ec2.volumes.all():
        # 상태가 'available'이면 아무 EC2에도 연결 안 된 상태!
        if volume.state == 'available':
            report.append(f"[EBS] 미사용 볼륨: {volume.id} ({volume.size}GB)")
    
    # 2. 미사용 Elastic IP(EIP) 체크
    addresses = ec2_client.describe_addresses()
    for addr in addresses['Addresses']:
        # 'InstanceId'가 없으면 연결되지 않은 상태!
        if 'InstanceId' not in addr:
            report.append(f"[EIP] 미연결 고정 IP: {addr['PublicIp']}")
    
    return report

if __name__ == "__main__":
    print(f"🔍 [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 자원 점검 시작...")
    results = check_unused_resources()

    if results:
        header = "[비용 최적화 리포트] 미사용 자원이 발견되었습니다!\n"
        full_report = header + "\n".join(results)
        print(full_report)
        send_slack_report(full_report)
    else:
        print("모든 자원이 정상 사용 중입니다.")