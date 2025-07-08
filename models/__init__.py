from pymongo import MongoClient
from config import Config

# MongoDB 연결
client = MongoClient(Config.MONGO_URI)
db = client.til_jungle

# 컬렉션 정의
users_collection = db.users
posts_collection = db.posts