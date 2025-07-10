import requests
from config import Config
import logging
import sys
import os
import json  # 추가: JSON 디버깅용
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


logger = logging.getLogger(__name__)

def get_slack_members():
    """관리자 토큰으로 워크스페이스 멤버 정보 가져오기"""
    try:
        url = "https://slack.com/api/users.list"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if not data.get('ok'):
            logger.error(f"Slack API 오류: {data.get('error')}")
            return None
            
        members = []
        for member in data.get('members', []):
            # 봇이나 삭제된 사용자 제외
            if member.get('deleted') or member.get('is_bot'):
                continue
                
            profile = member.get('profile', {})
            
            # 이메일이 있는 멤버만 포함
            if profile.get('email'):
                member_info = {
                    'slack_user_id': member.get('id'),
                    'slack_team_id': member.get('team_id'),
                    'name': profile.get('display_name') or profile.get('real_name') or member.get('name'),
                    'email': profile.get('email'),
                    'avatar_url': profile.get('image_192') or profile.get('image_512'),
                    'real_name': profile.get('real_name'),
                    'display_name': profile.get('display_name'),
                    'title': profile.get('title', ''),
                    'phone': profile.get('phone', ''),
                    'is_active': not member.get('deleted', False)
                }
                members.append(member_info)
                
        logger.info(f"Slack에서 {len(members)}명의 멤버 정보를 가져왔습니다.")
        return members
        
    except Exception as e:
        logger.error(f"Slack 멤버 정보 가져오기 실패: {str(e)}")
        return None

def test_slack_connection():
    """Slack 연결 테스트"""
    try:
        url = "https://slack.com/api/auth.test"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data.get('ok'):

            return True
        else:
            print(f"❌ Slack 연결 실패: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Slack 연결 테스트 실패: {str(e)}")
        return False

def sync_slack_to_users():
    """Slack 멤버 정보를 기존 users 컬렉션과 매칭하여 업데이트"""
    from models.user import update_user_slack_info, find_user_by_email
    
    try:
        # 1. Slack 멤버 정보 가져오기
        slack_members = get_slack_members()
        if not slack_members:
            return {"success": False, "message": "Slack 멤버 정보를 가져올 수 없습니다"}
        
        matched_count = 0
        unmatched_count = 0
        updated_count = 0
        
        # 2. 각 Slack 멤버를 기존 사용자와 매칭
        for member in slack_members:
            email = member['email']
            existing_user = find_user_by_email(email)
            
            if existing_user:
                # 기존 사용자가 있으면 Slack 정보 업데이트
                slack_data = {
                    'slack_user_id': member['slack_user_id'],
                    'slack_team_id': member['slack_team_id'],
                    'avatar_url': member['avatar_url'],
                    'real_name': member['real_name'],
                    'display_name': member['display_name']
                }
                
                result = update_user_slack_info(email, slack_data)
                if result['success']:
                    matched_count += 1
                    updated_count += 1
                    logger.info(f"매칭 성공: {member['name']} ({email})")
                else:
                    logger.warning(f"업데이트 실패: {email} - {result['message']}")
            else:
                # 기존 사용자가 없으면 스킵
                unmatched_count += 1
                logger.info(f"매칭 실패: {member['name']} ({email}) - 회원가입 안함")
        
        result_message = f"동기화 완료: 매칭 {matched_count}명, 미매칭 {unmatched_count}명"
        logger.info(result_message)
        
        return {
            "success": True,
            "message": result_message,
            "matched_count": matched_count,
            "unmatched_count": unmatched_count,
            "updated_count": updated_count
        }
        
    except Exception as e:
        error_message = f"Slack 동기화 실패: {str(e)}"
        logger.error(error_message)
        return {"success": False, "message": error_message}

def create_dm_conversation(user1_slack_id, user2_slack_id, questioner_name=None, author_name=None, post_title=None, card_id=None):
    """두 사용자 간 DM 채널 생성"""
    try:
        url = "https://slack.com/api/conversations.open"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "users": f"{user1_slack_id},{user2_slack_id}"
        }
        
        print(f"[DEBUG] Slack API 호출 - users: {payload['users']}")
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        print(f"[DEBUG] Slack API 응답: {data}")
        
        if data.get('ok'):
            channel_id = data['channel']['id']
            logger.info(f"DM 채널 생성 성공: {channel_id}")
            
            # 환영 메시지 발송 (카드 ID 포함)
            if questioner_name and author_name and post_title and card_id:
                send_welcome_message(channel_id, questioner_name, author_name, post_title, card_id)
            
            return {
                "success": True,
                "message": "DM 채널 생성 완료",
                "channel_id": channel_id
            }
        else:
            error_msg = data.get('error', 'Unknown error')
            logger.error(f"DM 채널 생성 실패: {error_msg}")
            return {
                "success": False,
                "message": f"Slack API 오류: {error_msg}"
            }
            
    except Exception as e:
        logger.error(f"DM 채널 생성 중 오류: {str(e)}")
        return {
            "success": False,
            "message": f"서버 오류: {str(e)}"
        }

def send_welcome_message(channel_id, questioner_name, author_name, post_title, card_id):
    """DM 채널에 환영 메시지 발송 (카드 ID 메타데이터 포함)"""
    try:
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": channel_id,
            "text": f"👋 안녕하세요 {author_name}님, {questioner_name}입니다.\n\n'{post_title}' 포스트에 대해 질문이 있습니다!\n\n💬 이제 자유롭게 대화해보세요. 나중에 이 대화는 Q&A 게시판에 공유될 수 있습니다.",
            "metadata": {
                "event_type": "til_question_start",
                "event_payload": {
                    "card_id": card_id,
                    "post_title": post_title,
                    "questioner_name": questioner_name,
                    "author_name": author_name
                }
            }
        }
        
        print(f"[DEBUG] 메타데이터와 함께 환영 메시지 발송: {payload}")
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get('ok'):
            logger.info(f"환영 메시지 발송 성공 (카드 ID: {card_id})")
        
        else:
            logger.warning(f"환영 메시지 발송 실패: {data.get('error')}")           
            
    except Exception as e:
        logger.error(f"환영 메시지 발송 중 오류: {str(e)}")

def test_dm_creation():
    """DM 생성 테스트 함수 (개발용)"""
    # 테스트용 사용자 ID들 (실제 워크스페이스의 사용자 ID로 변경)
    test_user1 = "U094NS7Q535"  # 실제 사용자 ID로 변경
    test_user2 = "U094WG67NFN"  # 실제 사용자 ID로 변경
    
    result = create_dm_conversation(test_user1, test_user2)
    print(f"테스트 결과: {result}")
    return result

def collect_conversation_history(channel_id):
    """Slack 대화 히스토리 수집 (메타데이터 포함)"""
    try:
        url = "https://slack.com/api/conversations.history"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        params = {
            "channel": channel_id,
            "limit": 20,
            "include_all_metadata": "true"  # 🔥 핵심 수정: 메타데이터 포함!
        }
                
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if data.get('ok'):
            messages = data.get('messages', [])            
            # 메타데이터 있는 메시지 확인
            metadata_count = 0
            for msg in messages:
                if msg.get('metadata'):
                    metadata_count += 1

            return messages
        else:
            logger.error(f"대화 수집 실패: {data.get('error')}")
            return []
            
    except Exception as e:
        logger.error(f"대화 수집 중 오류: {str(e)}")
        return []

def format_conversation_messages(messages, questioner_slack_id, author_slack_id):
    """메시지를 읽기 쉬운 형태로 포맷팅"""
    formatted = []

    
    for i, msg in enumerate(reversed(messages)):
        user_id = msg.get('user')
        
        # 1. 봇 메시지 제외
        if msg.get('subtype') == 'bot_message':
            continue
            
        # 2. 질문자/작성자가 아닌 사용자 메시지 제외
        if user_id != questioner_slack_id and user_id != author_slack_id:
            continue
        
        # 텍스트 추출
        text = extract_text_from_message(msg)
        if not text:
            continue
            
        # 사용자 구분
        if user_id == questioner_slack_id:
            role = "질문자"
        elif user_id == author_slack_id:
            role = "작성자"
        else:
            continue
            
        formatted.append({
            "role": role,
            "text": text,
            "timestamp": msg.get('ts')
        })
    
    print(f"[DEBUG] 최종 포맷된 메시지 수: {len(formatted)}")
    return formatted

def extract_text_from_message(msg):
    """복잡한 Slack 메시지에서 텍스트 추출"""
    text = ""
    
    # 일반 텍스트
    if msg.get('text'):
        return msg.get('text')
    
    # blocks 구조에서 추출
    if msg.get('blocks'):
        for block in msg.get('blocks', []):
            if block.get('type') == 'rich_text':
                for element in block.get('elements', []):
                    if element.get('type') == 'rich_text_section':
                        for elem in element.get('elements', []):
                            if elem.get('type') == 'text':
                                text += elem.get('text', '')
    
    return text

def find_dm_channel(user1_id, user2_id):
    """두 사용자 간 DM 채널 찾기"""
    try:
        url = "https://slack.com/api/conversations.open"
        headers = {"Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}"}
        payload = {"users": f"{user1_id},{user2_id}"}
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get('ok'):
            return data['channel']['id']
        return None
        
    except Exception as e:
        logger.error(f"DM 채널 찾기 오류: {str(e)}")
        return None

def extract_conversation_by_card(messages, target_card_id):
    """특정 카드 ID 관련 대화만 추출"""
    print(f"[DEBUG] 🎯 타겟 카드 ID로 대화 필터링: {target_card_id}")
    
    # 1. 해당 카드 ID의 봇 메시지들과 그 타임스탬프 찾기
    bot_message_timestamps = []
    
    for i, msg in enumerate(messages):
        # 메타데이터 상세 분석
        metadata = msg.get('metadata')
        if metadata:
            print(f"[DEBUG] 메시지 {i} 메타데이터: {json.dumps(metadata, indent=2)}")
            
            # 메타데이터 구조 확인
            event_payload = metadata.get('event_payload', {})
            card_id_in_metadata = event_payload.get('card_id')
            
            # 다양한 경우 확인
            if card_id_in_metadata == target_card_id:
                bot_timestamp = float(msg.get('ts'))
                bot_message_timestamps.append(bot_timestamp)
                
        # 봇 메시지 여부 확인
        if msg.get('subtype') == 'bot_message':
            print(f"[DEBUG] 🤖 봇 메시지 발견 (메타데이터 {'있음' if metadata else '없음'})")
    
    if not bot_message_timestamps:
        print(f"[DEBUG] ❌ 해당 카드 ID({target_card_id})의 봇 메시지를 찾을 수 없음")
        # return []
    
    # 2. 가장 최근 봇 메시지 이후의 대화만 추출
    latest_bot_timestamp = max(bot_message_timestamps)

    # 3. 해당 타임스탬프 이후의 메시지들만 필터링
    filtered_messages = []
    for msg in messages:
        msg_timestamp = float(msg.get('ts'))
        
        # 봇 메시지 이후의 메시지만 포함
        if msg_timestamp > latest_bot_timestamp:
            filtered_messages.append(msg)    
    return filtered_messages