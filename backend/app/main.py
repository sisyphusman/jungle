from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.post import Post
from app.routers.posts import router as posts_router

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
    db = client.get_default_database()  # URL의 /curdd가 기본 DB가 됨
    # Beanie 초기화 (모델 등록)
    await init_beanie(database=db, document_models=[Post])

    # (선택) 지오쿼리 쓸 계획이면 2dsphere 인덱스 생성
    await db["posts"].create_index([("location", "2dsphere")])

@app.get("/health")
async def health():
    return {"status": "ok"}

# 라우터 등록
app.include_router(posts_router)
