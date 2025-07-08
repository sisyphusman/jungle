from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

bot_token = ""  # 봇 토큰 입력
client = WebClient(token=bot_token)

# user1, user2 는 Slack user ID 문자열 예: U12345678
user1 = "U094NS7Q535"
user2 = "U094WG67NFN"

try:
    # conversations.open API 호출
    response = client.conversations_open(users=f"{user1},{user2}")
    channel_id = response['channel']['id']
    print(f"MPIM 채널 생성 완료, 채널 ID: {channel_id}")

    message_response = client.chat_postMessage(
        channel=channel_id,
        text="안녕하세요! 이 채널이 새로 생성되었습니다."
    )
    print("메시지 전송 성공!")

except SlackApiError as e:
    print(f"Error creating MPIM channel: {e.response['error']}")