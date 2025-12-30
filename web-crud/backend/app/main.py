from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.routers.posts import router as posts_router
from app.routers.comments import router as comments_router
from app.routers.auth import router as auth_router

app = FastAPI(title="Crud API")

# Vite 개발 서버 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client.get_default_database()  # URL의 /crud가 기본 DB가 됨
    # Beanie 초기화 (모델 등록)
    await init_beanie(database=db, document_models=[Post, User, Comment])

@app.get("/health")
async def health():
    return {"status": "ok"}

# 라우터 등록
app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(comments_router)
