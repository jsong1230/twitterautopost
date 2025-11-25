from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.database import init_db
from backend.routers import keywords, insights, posts, twitter_insights, instagram_insights
from backend.services.scheduler_service import start_scheduler, stop_scheduler
from backend.config import settings

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Twitter/Instagram AI 인사이트 생성기",
    description="AI 기반 트렌드 분석 및 포스트 자동 생성 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(keywords.router)
app.include_router(insights.router)
app.include_router(posts.router)
app.include_router(twitter_insights.router)
app.include_router(instagram_insights.router)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 데이터베이스 초기화 및 스케줄러 시작"""
    logger.info("애플리케이션 시작 중...")
    init_db()
    logger.info("데이터베이스 초기화 완료")
    
    # 스케줄러 시작 (24시간 자동 실행)
    # 설정에서 enable_scheduler=False로 설정하면 비활성화됨
    if settings.enable_scheduler:
        start_scheduler()
        logger.info("스케줄러가 활성화되었습니다. 서버가 24시간 실행됩니다.")
    else:
        logger.info("스케줄러가 비활성화되어 있습니다. 수동으로만 인사이트를 생성할 수 있습니다.")
    
    logger.info("애플리케이션 시작 완료")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 스케줄러 중지"""
    logger.info("애플리케이션 종료 중...")
    stop_scheduler()
    logger.info("애플리케이션 종료 완료")


@app.get("/")
async def root():
    """Health check"""
    return {
        "message": "Twitter/Instagram AI 인사이트 생성기 API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

