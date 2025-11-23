from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from backend.database import get_db
from backend.models.post import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])


class PostResponse(BaseModel):
    id: int
    insight_id: int
    post_type: str
    content: str
    hashtags: str | None
    created_at: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 100,
    insight_id: int | None = None,
    db: Session = Depends(get_db)
):
    """포스트 목록 조회"""
    query = db.query(Post)
    
    if insight_id:
        query = query.filter(Post.insight_id == insight_id)
    
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
    return posts

