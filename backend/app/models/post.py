from typing import Optional, List
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field

class GeoPoint(BaseModel):
    # 네이버 지도 등 GeoJSON Point 규격
    type: str = "Point"
    coordinates: List[float] = Field(..., description="[lng, lat]")

class Post(Document):
    title: str
    body: str
    author_id: Optional[str] = None
    author_nickname: Optional[str] = None
    location: Optional[GeoPoint] = None  # 지도 마커 저장 시 사용
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "posts"  # 컬렉션명

# 생성/수정용 DTO (요청 바디에 쓰기)
class PostCreate(BaseModel):
    title: str
    body: str
    author_id: Optional[str] = None
    author_nickname: Optional[str] = None
    location: Optional[GeoPoint] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    author_id: Optional[str] = None
    location: Optional[GeoPoint] = None