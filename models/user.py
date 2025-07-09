from datetime import datetime
from bson import ObjectId
from models.database import users_collection
from utils.password_helper import hash_password, check_password

def create_user(name, email, password, slack_data=None):
    """새 사용자 생성 (Slack 정보 선택적 포함)"""
    try:
        # 이메일 중복 확인
        if users_collection.find_one({"email": email}):
            return {"success": False, "message": "이미 존재하는 이메일입니다"}

        # 비밀번호 해싱
        hashed_password = hash_password(password)

        # 기본 사용자 데이터
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Slack 정보가 있으면 추가
        if slack_data:
            user_data.update({
                "slack_user_id": slack_data.get("slack_user_id"),
                "slack_team_id": slack_data.get("slack_team_id"),
                "avatar_url": slack_data.get("avatar_url"),
                "slack_real_name": slack_data.get("real_name"),
                "slack_display_name": slack_data.get("display_name"),
                "slack_synced_at": datetime.utcnow()
            })
        else:
            # Slack 정보가 없으면 기본값
            user_data.update({
                "slack_user_id": None,
                "slack_team_id": None,
                "avatar_url": None,
                "slack_real_name": None,
                "slack_display_name": None,
                "slack_synced_at": None
            })

        # DB에 저장
        result = users_collection.insert_one(user_data)

        return {
            "success": True,
            "message": "회원가입 성공",
            "user_id": str(result.inserted_id),
            "has_slack": slack_data is not None
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
    """사용자 ID로 사용자 찾기 (Slack 정보 포함)"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "created_at": user["created_at"],
                "avatar_url": user.get("avatar_url"),
                "slack_user_id": user.get("slack_user_id"),
                "slack_team_id": user.get("slack_team_id"),
                "slack_real_name": user.get("slack_real_name"),
                "slack_display_name": user.get("slack_display_name")
            }
        return None

    except Exception as e:
        print(f"사용자 조회 실패: {e}")
        return None

def find_user_by_name(name):
    """이름으로 사용자 찾기 (Slack 정보 포함)"""
    try:
        user = users_collection.find_one({"name": name})
        if user:
            return {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "created_at": user["created_at"],
                "avatar_url": user.get("avatar_url"),
                "slack_user_id": user.get("slack_user_id"),
                "slack_team_id": user.get("slack_team_id"),
                "slack_real_name": user.get("slack_real_name"),
                "slack_display_name": user.get("slack_display_name")
            }
        return None

    except Exception as e:
        print(f"이름으로 사용자 조회 실패: {e}")
        return None

def find_user_by_email(email):
    """이메일로 사용자 찾기 (Slack 정보 포함)"""
    try:
        user = users_collection.find_one({"email": email})
        if user:
            return {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "avatar_url": user.get("avatar_url"),
                "slack_user_id": user.get("slack_user_id"),
                "slack_team_id": user.get("slack_team_id")
            }
        return None

    except Exception as e:
        print(f"사용자 조회 실패: {e}")
        return None


def update_user_slack_info(email, slack_data):
    """사용자의 Slack 정보 업데이트"""
    try:
        update_data = {
            "slack_user_id": slack_data.get("slack_user_id"),
            "slack_team_id": slack_data.get("slack_team_id"),
            "avatar_url": slack_data.get("avatar_url"),
            "slack_real_name": slack_data.get("real_name"),
            "slack_display_name": slack_data.get("display_name"),
            "slack_synced_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        result = users_collection.update_one(
            {"email": email},
            {"$set": update_data}
        )

        if result.matched_count > 0:
            return {"success": True, "message": "Slack 정보 업데이트 성공"}
        else:
            return {"success": False, "message": "해당 이메일의 사용자를 찾을 수 없습니다"}

    except Exception as e:
        return {"success": False, "message": f"Slack 정보 업데이트 실패: {str(e)}"}


def get_users_without_slack():
    """Slack 정보가 없는 사용자들 조회"""
    try:
        users = list(users_collection.find({
            "slack_user_id": {"$in": [None, ""]}
        }))
        
        return [
            {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "created_at": user["created_at"]
            }
            for user in users
        ]
    except Exception as e:
        print(f"Slack 미연동 사용자 조회 실패: {e}")
        return []


def get_users_with_slack():
    """Slack 정보가 있는 사용자들 조회"""
    try:
        users = list(users_collection.find({
            "slack_user_id": {"$ne": None, "$ne": ""}
        }))
        
        return [
            {
                "id": str(user["_id"]),
                "name": user["name"],
                "email": user["email"],
                "slack_user_id": user["slack_user_id"],
                "avatar_url": user.get("avatar_url"),
                "slack_synced_at": user.get("slack_synced_at")
            }
            for user in users
        ]
    except Exception as e:
        print(f"Slack 연동 사용자 조회 실패: {e}")
        return []
