from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    openai_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./twitter_insights.db"
    
    # Server
    backend_port: int = 8000
    backend_host: str = "0.0.0.0"
    
    # Scheduler
    enable_scheduler: bool = True  # 스케줄러 활성화 여부
    scheduler_hours: str = "9,15,21"  # 스케줄러 실행 시간 (콤마로 구분)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
