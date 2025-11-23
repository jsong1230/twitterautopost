"""
스케줄러 서비스
주기적으로 활성화된 키워드에 대해 인사이트를 생성합니다.
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.keyword import Keyword
from backend.services.twitter_service import TwitterService
from backend.services.ai_service import AIService
from backend.models.insight import Insight
from backend.models.post import Post, PostType
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def generate_insight_for_keyword(keyword_id: int):
    """특정 키워드에 대한 인사이트 생성"""
    db = SessionLocal()
    try:
        keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
        if not keyword or not keyword.is_active:
            logger.info(f"키워드 {keyword_id}는 활성화되지 않았거나 존재하지 않습니다.")
            return
        
        logger.info(f"키워드 '{keyword.keyword}'에 대한 인사이트 생성 시작...")
        
        # 트윗 수집
        twitter_service = TwitterService()
        tweets = await twitter_service.search_tweets(keyword.keyword, max_results=10, hours=24)
        
        if not tweets:
            logger.warning(f"키워드 '{keyword.keyword}'에 대한 트윗을 찾을 수 없습니다.")
            return
        
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
        
        # 포스트 생성
        await generate_posts_for_insight(insight.id, insights_data, db)
        
        logger.info(f"키워드 '{keyword.keyword}'에 대한 인사이트 생성 완료 (ID: {insight.id})")
        
    except Exception as e:
        logger.error(f"키워드 {keyword_id} 인사이트 생성 중 오류: {e}", exc_info=True)
        db.rollback()
    finally:
        db.close()


async def generate_posts_for_insight(insight_id: int, insights_data: dict, db: Session):
    """인사이트에 대한 포스트 생성"""
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
    except Exception as e:
        logger.error(f"포스트 생성 중 오류: {e}", exc_info=True)
        db.rollback()


async def scheduled_insight_generation():
    """스케줄된 인사이트 생성 작업"""
    db = SessionLocal()
    try:
        # 활성화된 모든 키워드 조회
        active_keywords = db.query(Keyword).filter(Keyword.is_active == True).all()
        
        logger.info(f"활성화된 키워드 {len(active_keywords)}개에 대한 인사이트 생성 시작...")
        
        for keyword in active_keywords:
            await generate_insight_for_keyword(keyword.id)
            # API 레이트 리밋을 고려하여 약간의 딜레이
            await asyncio.sleep(2)
        
        logger.info("스케줄된 인사이트 생성 완료")
    except Exception as e:
        logger.error(f"스케줄된 인사이트 생성 중 오류: {e}", exc_info=True)
    finally:
        db.close()


def start_scheduler(hours: str = "9,15,21"):
    """스케줄러 시작"""
    from backend.config import settings
    
    # 설정에서 스케줄러 비활성화되어 있으면 시작하지 않음
    if not settings.enable_scheduler:
        logger.info("스케줄러가 비활성화되어 있습니다.")
        return
    
    # 설정에서 시간 가져오기 (기본값: 9,15,21)
    scheduler_hours = hours or settings.scheduler_hours
    
    # 매일 지정된 시간에 실행
    scheduler.add_job(
        scheduled_insight_generation,
        trigger=CronTrigger(hour=scheduler_hours, minute=0),
        id="daily_insight_generation",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"스케줄러가 시작되었습니다. 매일 {scheduler_hours}시에 인사이트를 생성합니다.")


def stop_scheduler():
    """스케줄러 중지"""
    scheduler.shutdown()
    logger.info("스케줄러가 중지되었습니다.")

