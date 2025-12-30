from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field

class Post(Document):
    title: str
    body: str
    author_id: Optional[str] = None
    author_nickname: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    views: int = 0
    comment_count: int = 0

    class Settings:
        name = "posts"  # 컬렉션명

# 생성/수정용 DTO (요청 바디에 쓰기)
class PostCreate(BaseModel):
    title: str
    body: str
    author_id: Optional[str] = None
    author_nickname: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[str] = None
