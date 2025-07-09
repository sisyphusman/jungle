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
    


