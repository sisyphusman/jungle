from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from fastapi import Query
from app.models.post import Post, PostCreate, PostUpdate
from app.models.user import User
from app.routers.auth import get_current_user
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/posts", tags=["posts"])

@router.post("/", response_model=Post)
async def create_post(payload: PostCreate, current_user: User = Depends(get_current_user)):
    # 로그인한 사용자만 글 작성 가능
    doc = Post(
        **payload.model_dump(exclude={"author_id", "author_nickname"}),
        author_id=str(current_user.id),
        author_nickname=current_user.nickname,
    )
    await doc.insert()
    return doc

@router.get("/")
async def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
):
    skip = (page - 1) * limit
    cursor = Post.find_all().sort(-Post.created_at).skip(skip).limit(limit)
    items = await cursor.to_list()
    total = await Post.find_all().count()
    return {"items": items, "total": total, "page": page, "limit": limit}

@router.get("/{post_id}", response_model=Post)
async def get_post(post_id: str):
    # 잘못된 ObjectId 문자열로 인한 500 방지
    try:
        _ = PydanticObjectId(post_id)
    except Exception:
        raise HTTPException(400, "invalid post id")
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    return doc


@router.post("/{post_id}/view")
async def increment_post_view(post_id: str):
    # 잘못된 ObjectId 문자열로 인한 500 방지
    try:
        _ = PydanticObjectId(post_id)
    except Exception:
        raise HTTPException(400, "invalid post id")
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    new_views = (doc.views or 0) + 1
    await doc.set({"views": new_views})
    return {"ok": True, "views": new_views}

@router.patch("/{post_id}", response_model=Post)
async def update_post(post_id: str, payload: PostUpdate, current_user: User = Depends(get_current_user)):
    try:
        _ = PydanticObjectId(post_id)
    except Exception:
        raise HTTPException(400, "invalid post id")
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    # 작성자만 수정 가능
    if doc.author_id != str(current_user.id):
        raise HTTPException(403, "Not authorized to update this post")
    await doc.set(payload.model_dump(exclude_unset=True))
    return doc

@router.delete("/{post_id}")
async def delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    try:
        _ = PydanticObjectId(post_id)
    except Exception:
        raise HTTPException(400, "invalid post id")
    doc = await Post.get(post_id)
    if not doc:
        raise HTTPException(404, "post not found")
    # 작성자만 삭제 가능
    if doc.author_id != str(current_user.id):
        raise HTTPException(403, "Not authorized to delete this post")
    await doc.delete()
    return {"ok": True}