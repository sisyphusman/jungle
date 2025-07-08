import bcrypt

def hash_password(password):
    """비밀번호 해싱"""
    # 문자열을 바이트로 변환 후 해싱
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')  # 문자열로 변환해서 MongoDB에 저장

def check_password(password, hashed_password):
    """비밀번호 검증"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)