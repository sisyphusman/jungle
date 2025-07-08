from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config
import sys
import atexit
import logging

# 로깅 설정 (안전하게)
logging.basicConfig(level=getattr(logging, getattr(Config, 'LOG_LEVEL', 'DEBUG')))
logger = logging.getLogger(__name__)

class MongoDBConnection:
    def __init__(self):
        self.client = None
        self.db = None
        self.users_collection = None
        self.cards_collection = None
        
    def connect(self):
        try:
            # Config 검증
            if hasattr(Config, 'validate_config'):
                Config.validate_config()
            
            # MongoDB 연결 설정
            connection_params = {
                'serverSelectionTimeoutMS': 5000,
                'connectTimeoutMS': 5000
            }
            
            # 추가 설정이 있다면 적용
            if hasattr(Config, 'MONGO_MAX_POOL_SIZE'):
                connection_params['maxPoolSize'] = Config.MONGO_MAX_POOL_SIZE
            if hasattr(Config, 'MONGO_MIN_POOL_SIZE'):
                connection_params['minPoolSize'] = Config.MONGO_MIN_POOL_SIZE
            
            self.client = MongoClient(Config.MONGO_URI, **connection_params)
            
            # 연결 테스트
            self.client.admin.command('ping')
            logger.info("MongoDB 연결 성공")
            
            # 데이터베이스 및 컬렉션 설정
            self.db = self.client.til_jungle
            self.users_collection = self.db.users
            self.cards_collection = self.db.cards
            
            # 인덱스 생성
            self._create_indexes()
            
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            return False
        except Exception as e:
            logger.error(f"MongoDB 초기화 중 오류: {e}")
            return False
    
    def _create_indexes(self):
        """필수 인덱스 생성"""
        try:
            # users 컬렉션 인덱스
            self.users_collection.create_index("email", unique=True)
            
            # cards 컬렉션 인덱스 (기존 posts 대신)
            self.cards_collection.create_index("author_id")
            self.cards_collection.create_index("tags")
            self.cards_collection.create_index("created_at")
            
            logger.info("인덱스 생성 완료")
            
        except Exception as e:
            logger.warning(f"인덱스 생성 실패: {e}")
    
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