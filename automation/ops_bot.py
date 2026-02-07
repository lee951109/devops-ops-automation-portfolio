import os
import boto3
import cost_saver
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


# 1. 토큰 설정 (환경 변수에서 가져옴)
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

# 2. 봇 앱 초기화
app = App(token=SLACK_BOT_TOKEN)

# 3. 이벤트 리스너: 앱이 멘션(@봇이름) 되었을 때 반응
@app.event("app_mention")
def handle_mention(body, say):
    user = body["event"]["user"]
    text = body["event"]["text"]

    say(f"🔍 <@{user}>님, AWS 자원을 정밀 점검하고 있습니다... (v2.0)")

    try:
        # 1. cost_saver 함수 호출
        results = cost_saver.check_unused_resources()
        
        # 2. 결과에 따른 응답 로직
        if results:
            response = "🚨 **미사용 자원 발견!**\n" + "\n".join(results)
        else:
            response = "✅ **모든 자원이 정상 사용 중입니다.**"
            
        say(response)
        
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
        say("죄송합니다. 점검 중 내부 에러가 발생했습니다.")
    
# 4. 봇 실행 (Socket Mode)
if __name__ == "__main__":
    print("🤖 OpsBot이 가동되었습니다! (Socket Mode)")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()