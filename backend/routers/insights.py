from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from backend.database import get_db
from backend.models.keyword import Keyword
from backend.models.insight import Insight
from backend.models.post import Post, PostType
from backend.services.twitter_service import TwitterService
from backend.services.ai_service import AIService
from datetime import datetime

router = APIRouter(prefix="/api/insights", tags=["insights"])


class InsightResponse(BaseModel):
    id: int
    keyword_id: int
    keyword: str
    summary_kr: Optional[str]
    summary_en: Optional[str]
    tweets_analyzed: int
    created_at: str
    posts: List[dict] = []

    class Config:
        from_attributes = True


@router.get("/", response_model=List[InsightResponse])
async def get_insights(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """인사이트 목록 조회"""
    insights = db.query(Insight).order_by(Insight.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for insight in insights:
        posts = db.query(Post).filter(Post.insight_id == insight.id).all()
        insight_dict = {
            "id": insight.id,
            "keyword_id": insight.keyword_id,
            "keyword": insight.keyword,
            "summary_kr": insight.summary_kr,
            "summary_en": insight.summary_en,
            "tweets_analyzed": insight.tweets_analyzed,
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
        }
        result.append(insight_dict)
    
    return result


@router.post("/generate/{keyword_id}")
async def generate_insight(
    keyword_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """키워드에 대한 인사이트 생성 (트윗 수집 + AI 분석)"""
    keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다.")
    
    # 트윗 수집
    twitter_service = TwitterService()
    tweets = await twitter_service.search_tweets(keyword.keyword, max_results=10, hours=24)
    
    # AI 분석
    ai_service = AIService()
    insights_data = await ai_service.generate_insights(tweets)
    
    # 인사이트 저장
    insight = Insight(
        keyword_id=keyword.id,
        keyword=keyword.keyword,
        summary_kr=insights_data["summary_kr"],
        summary_en=insights_data["summary_en"],
        tweets_analyzed=len(tweets)
    )
    db.add(insight)
    db.commit()
    db.refresh(insight)
    
    # 포스트 생성 (백그라운드)
    background_tasks.add_task(generate_posts_for_insight, insight.id, insights_data)
    
    return {
        "message": "인사이트가 생성되었습니다.",
        "insight_id": insight.id
    }


async def generate_posts_for_insight(insight_id: int, insights_data: dict):
    """인사이트에 대한 포스트 생성 (백그라운드 작업)"""
    from backend.database import SessionLocal
    
    db = SessionLocal()
    try:
        ai_service = AIService()
        
        # 트윗 초안 생성
        tweet_drafts = await ai_service.generate_tweets(insights_data, count=5)
        for tweet_content in tweet_drafts:
            post = Post(
                insight_id=insight_id,
                post_type=PostType.TWEET,
                content=tweet_content,
                hashtags=None
            )
            db.add(post)
        
        # 인스타그램 포스트 생성
        instagram_data = await ai_service.generate_instagram_post(insights_data)
        post = Post(
            insight_id=insight_id,
            post_type=PostType.INSTAGRAM,
            content=instagram_data["caption"],
            hashtags=",".join(instagram_data["hashtags"])
        )
        db.add(post)
        
        db.commit()
    finally:
        db.close()


@router.get("/{insight_id}", response_model=InsightResponse)
async def get_insight(
    insight_id: int,
    db: Session = Depends(get_db)
):
    """특정 인사이트 조회"""
    insight = db.query(Insight).filter(Insight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="인사이트를 찾을 수 없습니다.")
    
    posts = db.query(Post).filter(Post.insight_id == insight_id).all()
    
    return {
        "id": insight.id,
        "keyword_id": insight.keyword_id,
        "keyword": insight.keyword,
        "summary_kr": insight.summary_kr,
        "summary_en": insight.summary_en,
        "tweets_analyzed": insight.tweets_analyzed,
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
    }

