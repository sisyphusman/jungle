import smtplib
import secrets
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from models.database import db

# 이메일 인증 코드 컬렉션
email_verification_collection = db.email_verifications

def generate_verification_code():
    """6자리 인증 코드 생성"""
    return ''.join([str(secrets.randbelow(10)) for _ in range(6)])

def send_verification_email(email, code):
    """인증 코드 이메일 발송"""
    try:
        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_EMAIL
        msg['To'] = email
        msg['Subject'] = "[TIL Jungle] 이메일 인증 코드"
        
        body = f"""
        안녕하세요! TIL Jungle입니다.
        
        회원가입을 완료하려면 아래 인증 코드를 입력해주세요:
        
        인증 코드: {code}
        
        이 코드는 5분간 유효합니다.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(Config.SMTP_EMAIL, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"이메일 발송 실패: {str(e)}")
        return False

def store_verification_code(email, code):
    """인증 코드를 DB에 저장 (5분 유효)"""
    try:
        # 기존 코드 삭제
        email_verification_collection.delete_many({"email": email})
        
        # 새 코드 저장
        verification_data = {
            "email": email,
            "code": code,
            "created_at": time.time(),
            "expires_at": time.time() + 300,  # 5분 후 만료
            "verified": False
        }
        
        email_verification_collection.insert_one(verification_data)
        return True
    except Exception as e:
        print(f"인증 코드 저장 실패: {str(e)}")
        return False

def verify_email_code(email, code):
    """이메일 인증 코드 검증"""
    try:
        verification = email_verification_collection.find_one({
            "email": email,
            "code": code,
            "verified": False,
            "expires_at": {"$gt": time.time()}
        })
        
        if verification:
            # 인증 완료 처리
            email_verification_collection.update_one(
                {"_id": verification["_id"]},
                {"$set": {"verified": True}}
            )
            return True
        return False
    except Exception as e:
        print(f"인증 코드 검증 실패: {str(e)}")
        return False