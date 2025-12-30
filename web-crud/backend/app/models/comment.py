from typing import Optional
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field


class Comment(Document):
    post_id: str
    content: str
    author_id: Optional[str] = None
    author_nickname: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "comments"


class CommentCreate(BaseModel):
    content: str
