from fastapi import APIRouter, HTTPException
from typing import List
from app.models.post import Post, PostCreate, PostUpdate

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

@router.post("/", response_model=Post)
async def create_post(payload: PostCreate):
    doc = Post(**payload.model_dump())
    await doc.insert()
    return doc

@router.get("/", response_model=List[Post])
async def list_posts():
    return await Post.find_all().to_list()

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: str):
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    return doc

@router.patch("/{post_id}", response_model=Post)
async def update_post(post_id: str, payload: PostUpdate):
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    await doc.set(payload.model_dump(exclude_unset=True))
    return doc

@router.delete("/{post_id}")
async def delete_post(post_id: str):
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    await doc.delete()
    return {"ok": True}