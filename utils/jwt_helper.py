import jwt
from datetime import datetime, timedelta
from config import Config

def generate_token(user_id):
    """JWT 토큰 생성"""
    payload = {
        'user_id': str(user_id),
        'iat': datetime.utcnow(),  # 발급 시간
        'exp': datetime.utcnow() + Config.JWT_ACCESS_TOKEN_EXPIRES  # 만료 시간
    }
    
    token = jwt.encode(
        payload, 
        Config.JWT_SECRET_KEY, 
        algorithm='HS256'
    )
    return token

def verify_token(token):
    """JWT 토큰 검증"""
    try:
        payload = jwt.decode(
            token, 
            Config.JWT_SECRET_KEY, 
            algorithms=['HS256']
        )
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # 토큰 만료
    except jwt.InvalidTokenError:
        return None  # 잘못된 토큰