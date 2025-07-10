import os
from dotenv import load_dotenv
from datetime import timedelta
import codecs

load_dotenv()

class Config:
    raw_uri = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/til_jungle'
    MONGO_URI = codecs.decode(raw_uri, 'unicode_escape')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    MONGO_MAX_POOL_SIZE = int(os.environ.get('MONGO_MAX_POOL_SIZE', '10'))
    MONGO_MIN_POOL_SIZE = int(os.environ.get('MONGO_MIN_POOL_SIZE', '1'))

    # JWT 설정
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-fallback-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_HOURS', '2')))
    
    # Slack 설정
    SLACK_CLIENT_ID = os.environ.get('SLACK_CLIENT_ID')
    SLACK_CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET')
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    
    # 워크스페이스 고정 설정 (선택사항)
    SLACK_TEAM_ID = os.environ.get('SLACK_TEAM_ID')  # 정글 워크스페이스 ID (설정하면 해당 워크스페이스로 제한)
    SLACK_TEAM_NAME = os.environ.get('SLACK_TEAM_NAME', 'jungle-til')  # 워크스페이스 이름
    SLACK_INVITE_URL = os.environ.get('SLACK_INVITE_URL') or 'https://join.slack.com/t/tiljungle/shared_invite/zt-38u2ezmh3-CB_Ij~WODym_T7sOpujeFA'


    # 서버 설정
    BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:5001'
    
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    SMTP_EMAIL = os.environ.get('SMTP_EMAIL')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')  # 앱 비밀번호


    @staticmethod
    def validate_config():
        """필수 설정값 검증"""
        required_vars = [
            'SLACK_CLIENT_ID', 
            'SLACK_CLIENT_SECRET', 
            'SLACK_BOT_TOKEN',
            'SLACK_TEAM_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(Config, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"필수 환경변수가 누락되었습니다: {', '.join(missing_vars)}")
        
        return True
    
    