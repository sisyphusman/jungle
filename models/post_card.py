from datetime import datetime
from bson import ObjectId
from models.database import cards_collection

def create_card(**kwargs):
    try:
        default_fields = {
            "id": None,
            "title": "",
            "author": "",
            "link": "",
            "tag_list": [],
            "img": "",
            "likes": 0,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        default_fields.update(kwargs)

        result = cards_collection.insert_one(default_fields)
        
        return {
            "success": True,
            "message": "카드 등록 성공",
            "card_id": str(result.inserted_id)  # 삽입된 카드 ID 반환
        }

    except Exception as e:
        return {"success": False, "message": f"카드 등록 실패: {str(e)}"}
