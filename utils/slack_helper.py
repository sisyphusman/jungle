import requests
from config import Config
import logging
import sys
import os
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
            print(f"✅ Slack 연결 성공!")
            print(f"   봇 이름: {data.get('user')}")
            print(f"   팀 이름: {data.get('team')}")
            print(f"   팀 ID: {data.get('team_id')}")
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
    


def create_dm_conversation(user1_slack_id, user2_slack_id):
    """두 사용자 간 DM 채널 생성"""
    try:
        url = "https://slack.com/api/conversations.open"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # 두 사용자의 Slack ID를 쉼표로 구분하여 전송
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
            
            # 환영 메시지 발송 (선택사항)
            send_welcome_message(channel_id)
            
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


def send_welcome_message(channel_id):
    """DM 채널에 환영 메시지 발송"""
    try:
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": channel_id,
            "text": "👋 안녕하세요! TIL Jungle 질문방이 생성되었습니다. 궁금한 점을 자유롭게 물어보세요!"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        if data.get('ok'):
            logger.info("환영 메시지 발송 성공")
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