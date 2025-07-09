import os

from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()


class Config:
    MONGO_URI = os.environ.get(
        'MONGO_URI') or 'mongodb://localhost:27017/til_jungle'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'  # DEBUG -> INFO
    MONGO_MAX_POOL_SIZE = int(os.environ.get('MONGO_MAX_POOL_SIZE', '10'))
    MONGO_MIN_POOL_SIZE = int(os.environ.get('MONGO_MIN_POOL_SIZE', '1'))

    # JWT 설정 추가
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-fallback-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_HOURS', '2')))

    @staticmethod
    def validate_config():
        return True  # 간단히
