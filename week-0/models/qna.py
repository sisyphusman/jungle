from datetime import datetime
from bson import ObjectId
from models.database import db

# Q&A 컬렉션 생성
qna_collection = db.qna

def create_qna_record(original_post_id, channel_id, questioner_name, author_name):
    """Q&A 레코드 생성"""
    qna_data = {
        "original_post_id": ObjectId(original_post_id),
        "channel_id": channel_id,
        "questioner_name": questioner_name,
        "author_name": author_name,
        "conversation": [],
        "status": "active",  # active, resolved
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = qna_collection.insert_one(qna_data)
    return str(result.inserted_id)