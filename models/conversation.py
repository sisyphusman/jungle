from datetime import datetime
from bson import ObjectId
from models.database import db

def save_conversation(card_id, channel_id, questioner_slack_id, author_slack_id, 
                     questioner_name, author_name, post_title, messages):
    """대화 저장 또는 업데이트 (버전 관리)"""
    try:
        print(f"[DEBUG] 대화 저장 시도: 카드 {card_id}, 메시지 {len(messages)}개")
        
        # 기존 대화 세션 찾기 (같은 카드 + 같은 사용자들)
        existing = db.conversations.find_one({
            "card_id": card_id,
            "questioner_slack_id": questioner_slack_id,
            "author_slack_id": author_slack_id
        })
        
        conversation_data = {
            "messages": messages,
            "message_count": len(messages),
            "last_collected_at": datetime.utcnow(),
            "version": 1  # 기본 버전
        }
        
        if existing:
            # 🔄 기존 대화 업데이트 (메시지 병합)
            existing_messages = existing.get("messages", [])
            existing_timestamps = set(msg.get("timestamp") for msg in existing_messages)
            
            print(f"[DEBUG] 기존 메시지: {len(existing_messages)}개")
            
            # 새로운 메시지만 추가 (중복 제거)
            new_messages_to_add = []
            for msg in messages:
                if msg.get("timestamp") not in existing_timestamps:
                    new_messages_to_add.append(msg)
            
            print(f"[DEBUG] 추가될 새 메시지: {len(new_messages_to_add)}개")
            
            # 전체 메시지 = 기존 메시지 + 새 메시지
            all_messages = existing_messages + new_messages_to_add
            
            # 타임스탬프 순으로 정렬
            all_messages.sort(key=lambda x: float(x.get("timestamp", 0)))
            
            new_version = existing.get("version", 1) + 1
            
            conversation_data = {
                "messages": all_messages,  # 🎉 기존 + 새 메시지 병합
                "message_count": len(all_messages),
                "last_collected_at": datetime.utcnow(),
                "version": new_version
            }
            
            result = db.conversations.update_one(
                {"_id": existing["_id"]},
                {"$set": conversation_data}
            )
            
            print(f"[DEBUG] 대화 업데이트 완료: v{new_version}, 총 {len(all_messages)}개 메시지")
            return {
                "success": True, 
                "conversation_id": str(existing["_id"]), 
                "action": "updated",
                "version": new_version,
                "message_count": len(all_messages),
                "new_messages_added": len(new_messages_to_add)
            }
        else:
            # 🆕 새 대화 세션 생성
            conversation_data.update({
                "card_id": card_id,
                "channel_id": channel_id,
                "questioner_slack_id": questioner_slack_id,
                "author_slack_id": author_slack_id,
                "questioner_name": questioner_name,
                "author_name": author_name,
                "post_title": post_title,
                "status": "active",
                "created_at": datetime.utcnow(),
                "is_published": False,  # 🔑 중요: 기본값 False
                "tags": [],
                "helpful_votes": 0
            })
            
            result = db.conversations.insert_one(conversation_data)
            
            print(f"[DEBUG] 새 대화 생성 완료: {result.inserted_id}")
            return {
                "success": True, 
                "conversation_id": str(result.inserted_id), 
                "action": "created",
                "version": 1,
                "message_count": len(messages)
            }
            
    except Exception as e:
        print(f"[ERROR] 대화 저장 실패: {str(e)}")
        return {"success": False, "message": f"대화 저장 실패: {str(e)}"}

def publish_conversation(conversation_id):
    """대화를 Q&A 게시판에 공개"""
    try:
        print(f"[DEBUG] 대화 공개 시도: {conversation_id}")
        
        result = db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": {"is_published": True, "status": "published"}}
        )
        
        if result.matched_count > 0:
            print(f"[DEBUG] 대화 공개 성공: {conversation_id}")
            return {"success": True}
        else:
            print(f"[ERROR] 대화를 찾을 수 없음: {conversation_id}")
            return {"success": False, "message": "대화를 찾을 수 없습니다"}
            
    except Exception as e:
        print(f"[ERROR] 대화 공개 실패: {str(e)}")
        return {"success": False, "message": str(e)}

def get_conversation_by_id(conversation_id):
    """특정 대화 상세 조회"""
    try:
        conv = db.conversations.find_one({"_id": ObjectId(conversation_id)})
        if conv:
            return {
                "id": str(conv["_id"]),
                "card_id": conv["card_id"],
                "questioner_name": conv["questioner_name"],
                "author_name": conv["author_name"],
                "post_title": conv["post_title"],
                "message_count": conv["message_count"],
                "version": conv.get("version", 1),
                "created_at": conv["created_at"],
                "last_collected_at": conv["last_collected_at"],
                "is_published": conv.get("is_published", False),
                "helpful_votes": conv.get("helpful_votes", 0),
                "messages": conv["messages"]
            }
        return None
    except Exception as e:
        print(f"대화 상세 조회 실패: {str(e)}")
        return None