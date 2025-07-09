from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일을 불러옴

bot_token = os.getenv("SLACK_BOT_TOEKN")

client = WebClient(token=bot_token)

user1 = "U094NS7Q535"
user2 = "U094G1CHSMV"

try:
    # conversations.open API 호출
    response = client.conversations_open(users=f"{user1},{user2}")
    channel_id = response['channel']['id']
    print(f"MPIM 채널 생성 완료, 채널 ID: {channel_id}")

    message_response = client.chat_postMessage(
        channel=channel_id,
        text="안녕하세요! TIL Bot입니다"
    )
    print("메시지 전송 성공!")

except SlackApiError as e:
    print(f"Error : {e.response['error']}")