from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from backend.database import get_db
from backend.models.keyword import Keyword
from backend.models.insight import Insight
from backend.models.post import Post, PostType
from backend.services.instagram_service import InstagramService
from backend.services.ai_service import AIService

router = APIRouter(prefix="/api/instagram/insights", tags=["instagram insights"])

class InsightResponse(BaseModel):
    id: int
    keyword_id: int
    keyword: str
    summary_kr: Optional[str]
    summary_en: Optional[str]
    posts_analyzed: int
    created_at: str
    posts: List[dict] = []

    class Config:
        from_attributes = True

@router.post("/generate/{keyword_id}")
async def generate_instagram_insight(
    keyword_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """키워드에 대한 인스타그램 인사이트 생성 (포스트 수집 + AI 분석)"""
    keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다.")

    # 인스타그램 포스트 수집 (현재 더미 데이터)
    instagram_service = InstagramService()
    posts_data = await instagram_service.fetch_posts(keyword.keyword, max_results=10)

    # AI 분석 (재사용 가능한 AI 서비스)
    ai_service = AIService()
    insights_data = await ai_service.generate_insights([p["caption"] for p in posts_data])

    # 인사이트 저장
    insight = Insight(
        keyword_id=keyword.id,
        keyword=keyword.keyword,
        summary_kr=insights_data.get("summary_kr"),
        summary_en=insights_data.get("summary_en"),
        tweets_analyzed=len(posts_data)  # 여기서는 분석된 포스트 수를 저장
    )
    db.add(insight)
    db.commit()
    db.refresh(insight)

    # 포스트 저장 (백그라운드 작업)
    background_tasks.add_task(_generate_instagram_posts, insight.id, posts_data)

    return {"message": "인사이트가 생성되었습니다.", "insight_id": insight.id}

async def _generate_instagram_posts(insight_id: int, posts_data: List[dict]):
    from backend.database import SessionLocal
    db = SessionLocal()
    try:
        for post_item in posts_data:
            post = Post(
                insight_id=insight_id,
                post_type=PostType.INSTAGRAM,
                content=post_item["caption"],
                hashtags=",".join(post_item.get("hashtags", []))
            )
            db.add(post)
        db.commit()
    finally:
        db.close()

@router.get("/", response_model=List[InsightResponse])
async def list_instagram_insights(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """인스타그램 인사이트 목록 조회"""
    insights = db.query(Insight).order_by(Insight.created_at.desc()).offset(skip).limit(limit).all()
    result = []
    for insight in insights:
        posts = db.query(Post).filter(Post.insight_id == insight.id, Post.post_type == PostType.INSTAGRAM).all()
        result.append({
            "id": insight.id,
            "keyword_id": insight.keyword_id,
            "keyword": insight.keyword,
            "summary_kr": insight.summary_kr,
            "summary_en": insight.summary_en,
            "posts_analyzed": insight.tweets_analyzed,
            "created_at": insight.created_at.isoformat() if insight.created_at else None,
            "posts": [
                {
                    "id": post.id,
                    "post_type": post.post_type.value,
                    "content": post.content,
                    "hashtags": post.hashtags,
                    "created_at": post.created_at.isoformat() if post.created_at else None,
                }
                for post in posts
            ]
        })
    return result
