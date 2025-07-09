from datetime import datetime
from bson import ObjectId
from models.database import users_collection
from utils.password_helper import hash_password, check_password

def create_user(name, email, password):
    """새 사용자 생성"""
    try:
        # 이메일 중복 확인
        if users_collection.find_one({"email": email}):
            return {"success": False, "message": "이미 존재하는 이메일입니다"}
        
        # 비밀번호 해싱
        hashed_password = hash_password(password)
        
        # 사용자 데이터 구성
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # DB에 저장
        result = users_collection.insert_one(user_data)
        
        return {
            "success": True, 
            "message": "회원가입 성공",
            "user_id": str(result.inserted_id)
        }
        
    except Exception as e:
        return {"success": False, "message": f"회원가입 실패: {str(e)}"}

def authenticate_user(email, password):
    """사용자 인증 (로그인)"""
    try:
        # 이메일로 사용자 찾기
        user = users_collection.find_one({"email": email})
        if not user:
            return {"success": False, "message": "존재하지 않는 이메일입니다"}
        
        # 비밀번호 검증
        if not check_password(password, user["password"]):
            return {"success": False, "message": "비밀번호가 틀렸습니다"}
        
        return {
            "success": True,
            "message": "로그인 성공",
            "user": {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"]
            }
        }
        
    except Exception as e:
        return {"success": False, "message": f"로그인 실패: {str(e)}"}

def find_user_by_id(user_id):
    """사용자 ID로 사용자 찾기"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "created_at": user["created_at"]
            }
        return None
        
    except Exception as e:
        print(f"사용자 조회 실패: {e}")
        return None

def find_user_by_email(email):
    """이메일로 사용자 찾기"""
    try:
        user = users_collection.find_one({"email": email})
        if user:
            return {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"]
            }
        return None
        
    except Exception as e:
        print(f"사용자 조회 실패: {e}")
        return None
    

def create_or_update_slack_user(slack_user_data):
    """Slack OAuth로 로그인한 사용자 생성 또는 업데이트 - 안전한 버전"""
    try:
        slack_user_id = slack_user_data['id']
        slack_team_id = slack_user_data.get('team', {}).get('id')
        
        if not slack_team_id:
            return {"success": False, "message": "Slack 팀 정보를 찾을 수 없습니다"}
        
        # 프로필 정보 안전하게 추출
        profile = slack_user_data.get('profile', {})
        
        # 이름 우선순위: display_name > real_name > name
        user_name = (
            profile.get('display_name') or 
            profile.get('real_name') or 
            slack_user_data.get('name') or 
            f"User_{slack_user_id[:8]}"  # 최후의 대안
        )
        
        # 기존 사용자 찾기
        existing_user = users_collection.find_one({
            "slack_user_id": slack_user_id,
            "slack_team_id": slack_team_id
        })
        
        user_data = {
            "slack_user_id": slack_user_id,
            "slack_team_id": slack_team_id,
            "name": user_name.strip(),
            "email": profile.get('email'),  # None일 수 있음
            "avatar_url": profile.get('image_192'),  # 보통 있음
            "slack_profile": {
                "real_name": profile.get('real_name'),
                "display_name": profile.get('display_name'),
                "title": profile.get('title', ''),  # 빈 문자열 기본값
                "phone": profile.get('phone', ''),  # 빈 문자열 기본값
                "status_text": profile.get('status_text', ''),
                "status_emoji": profile.get('status_emoji', ''),
                "first_name": profile.get('first_name', ''),
                "last_name": profile.get('last_name', ''),
                # 추가 이미지 URL들
                "image_24": profile.get('image_24'),
                "image_32": profile.get('image_32'),
                "image_48": profile.get('image_48'),
                "image_72": profile.get('image_72'),
                "image_512": profile.get('image_512'),
            },
            "is_active": True,
            "login_method": "slack_oauth",
            "updated_at": datetime.utcnow()
        }
        
        if existing_user:
            # 기존 사용자 업데이트
            users_collection.update_one(
                {"_id": existing_user["_id"]},
                {"$set": user_data}
            )
            user_id = str(existing_user["_id"])
            message = "사용자 정보 업데이트 완료"
        else:
            # 새 사용자 생성
            user_data["created_at"] = datetime.utcnow()
            user_data["total_posts"] = 0
            user_data["total_likes_received"] = 0
            
            result = users_collection.insert_one(user_data)
            user_id = str(result.inserted_id)
            message = "새 사용자 생성 완료"
        
        return {
            "success": True,
            "message": message,
            "user_id": user_id,
            "user": {
                "id": user_id,
                "name": user_data["name"],
                "email": user_data.get("email"),  # None일 수 있음
                "avatar_url": user_data.get("avatar_url"),
                "slack_user_id": slack_user_id,
                "slack_team_id": slack_team_id
            }
        }
        
    except KeyError as e:
        return {"success": False, "message": f"필수 Slack 데이터 누락: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": f"Slack 사용자 처리 실패: {str(e)}"}

# 실제 Slack API 응답 예시 (디버깅용)
def print_slack_user_data_structure(slack_user_data):
    """Slack API 응답 구조 확인용 함수"""
    print("=== Slack User Data 구조 ===")
    print(f"ID: {slack_user_data.get('id')}")
    print(f"Name: {slack_user_data.get('name')}")
    print(f"Team ID: {slack_user_data.get('team', {}).get('id')}")
    
    profile = slack_user_data.get('profile', {})
    print(f"Real Name: {profile.get('real_name')}")
    print(f"Display Name: {profile.get('display_name')}")
    print(f"Email: {profile.get('email')}")
    print(f"Title: {profile.get('title')}")
    print(f"Phone: {profile.get('phone')}")
    print(f"Status Text: {profile.get('status_text')}")
    print(f"Status Emoji: {profile.get('status_emoji')}")
    print(f"Avatar URLs:")
    for size in ['24', '32', '48', '72', '192', '512']:
        url = profile.get(f'image_{size}')
        if url:
            print(f"  image_{size}: {url}")
            

def find_user_by_slack_id(slack_user_id, slack_team_id):
    """Slack ID로 사용자 찾기"""
    try:
        user = users_collection.find_one({
            "slack_user_id": slack_user_id,
            "slack_team_id": slack_team_id,
            "is_active": True
        })
        
        if user:
            return {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "avatar_url": user.get("avatar_url"),
                "slack_user_id": user["slack_user_id"],
                "slack_team_id": user["slack_team_id"],
                "created_at": user["created_at"]
            }
        return None
        
    except Exception as e:
        print(f"Slack 사용자 조회 실패: {e}")
        return None

def deactivate_user(user_id):
    """사용자 비활성화 (삭제 대신)"""
    try:
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "is_active": False,
                    "deactivated_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"사용자 비활성화 실패: {e}")
        return False