from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import Config
import sys
import logging

# 로깅 설정
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class MongoDBConnection:
    """MongoDB 연결 관리 클래스"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.users_collection = None
        self.posts_collection = None
        
    def connect(self):
        """MongoDB 연결 설정"""
        try:
            # 설정 검증
            Config.validate_config()
            
            # MongoDB 클라이언트 생성
            self.client = MongoClient(
                Config.MONGO_URI,
                maxPoolSize=Config.MONGO_MAX_POOL_SIZE,
                minPoolSize=Config.MONGO_MIN_POOL_SIZE,
                serverSelectionTimeoutMS=5000,  # 5초 타임아웃
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # 연결 테스트
            self.client.admin.command('ping')
            logger.info("MongoDB 연결 성공")
            
            # 데이터베이스 선택
            self.db = self.client.til_jungle
            
            # 컬렉션 정의
            self.users_collection = self.db.users
            self.posts_collection = self.db.posts
            
            # 인덱스 생성
            self._create_indexes()
            
            logger.info("MongoDB 초기화 완료")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"MongoDB 연결 실패: {e}")
            return False
        except ServerSelectionTimeoutError as e:
            logger.error(f"MongoDB 서버 선택 타임아웃: {e}")
            return False
        except Exception as e:
            logger.error(f"MongoDB 초기화 중 오류: {e}")
            return False
    
    def _create_indexes(self):
        """필수 인덱스 생성"""
        try:
            # users 컬렉션 인덱스
            self.users_collection.create_index("slack_user_id", unique=True)
            self.users_collection.create_index("email", unique=True)
            
            # posts 컬렉션 인덱스
            self.posts_collection.create_index("author_id")
            self.posts_collection.create_index("tags")
            self.posts_collection.create_index("created_at")
            
            logger.info("인덱스 생성 완료")
            
        except Exception as e:
            logger.warning(f"인덱스 생성 실패: {e}")
    
    def disconnect(self):
        """MongoDB 연결 해제"""
        if self.client:
            self.client.close()
            logger.info("MongoDB 연결 해제")

# 전역 인스턴스
mongo_db = MongoDBConnection()

# 연결 시도
if not mongo_db.connect():
    logger.critical("MongoDB 연결 실패 - 애플리케이션 종료")
    sys.exit(1)

# 컬렉션 참조 (기존 코드와의 호환성)
client = mongo_db.client
db = mongo_db.db
users_collection = mongo_db.users_collection

# 앱 종료 시 연결 해제
import atexit
atexit.register(mongo_db.disconnect)