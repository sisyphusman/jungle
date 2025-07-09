from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config
import sys
import atexit
import logging

# 로깅 설정 (경고)
logging.getLogger('pymongo').setLevel(logging.WARNING)
# 기본 로깅 설정
logging.basicConfig(level=logging.INFO)  # DEBUG -> INFO로 변경
logger = logging.getLogger(__name__)

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.users_collection = None
        self.cards_collection = None
        
    def connect(self):
        try:
            logger.info("MongoDB 연결 시도...")
            
            # MongoDB 연결 설정 (간단하게)
            connection_params = {
                'serverSelectionTimeoutMS': 5000,
                'connectTimeoutMS': 5000
            }
            
            self.client = MongoClient(Config.MONGO_URI, **connection_params)
            
            # 연결 테스트
            self.client.admin.command('ping')
            logger.info("✅ MongoDB 연결 성공")
            
            # 데이터베이스 및 컬렉션 설정
            self.db = self.client.til_jungle
            self.users_collection = self.db.users
            self.cards_collection = self.db.cards
            
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            return False
        except Exception as e:
            logger.error(f"MongoDB 초기화 중 오류: {e}")
            return False
    
    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB 연결 해제")


# 전역 인스턴스
mongo_db = MongoDBConnection()

if not mongo_db.connect():
    logger.critical("MongoDB 연결 실패 - 애플리케이션 종료")
    sys.exit(1)

# 컬렉션 참조 (기존 코드와의 호환성)
client = mongo_db.client
db = mongo_db.db
users_collection = mongo_db.users_collection
cards_collection = mongo_db.cards_collection

# 앱 종료 시 연결 해제
atexit.register(mongo_db.disconnect)