from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.models.comment import Comment, CommentCreate
from app.models.user import User
from app.routers.auth import get_current_user
from beanie import PydanticObjectId

router = APIRouter(prefix="/api/v1/comments", tags=["comments"])


@router.get("/{post_id}", response_model=List[Comment])
async def list_comments(post_id: str):
    return await Comment.find(Comment.post_id == post_id).to_list()


@router.post("/{post_id}", response_model=Comment)
async def create_comment(post_id: str, payload: CommentCreate, current_user: User = Depends(get_current_user)):
    doc = Comment(
        post_id=post_id,
        content=payload.content,
        author_id=str(current_user.id),
        author_nickname=current_user.nickname,
    )
    await doc.insert()
    return doc


@router.delete("/{comment_id}")
async def delete_comment(comment_id: str, current_user: User = Depends(get_current_user)):
    try:
        _ = PydanticObjectId(comment_id)
    except Exception:
        raise HTTPException(400, "invalid comment id")
    doc = await Comment.get(comment_id)
    if not doc:
        raise HTTPException(404, "comment not found")
    if doc.author_id != str(current_user.id):
        raise HTTPException(403, "Not authorized to delete this comment")
    await doc.delete()
    return {"ok": True}
