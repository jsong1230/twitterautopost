from pydantic import BaseModel, Field, validator
from typing import List, Optional


class InsightResponse(BaseModel):
    """인사이트 생성 응답 모델"""
    summary_kr: str = Field(..., description="한글 요약", min_length=10)
    summary_en: str = Field(..., description="영문 요약", min_length=10)
    
    @validator('summary_kr', 'summary_en')
    def validate_summary(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("요약은 최소 10자 이상이어야 합니다.")
        return v.strip()


class TweetResponse(BaseModel):
    """트윗 생성 응답 모델"""
    tweets: List[str] = Field(..., description="생성된 트윗 목록")
    
    @validator('tweets')
    def validate_tweets(cls, v):
        if not v:
            raise ValueError("최소 1개 이상의 트윗이 필요합니다.")
        
        validated_tweets = []
        for tweet in v:
            tweet = tweet.strip()
            if len(tweet) > 280:
                raise ValueError(f"트윗은 280자를 초과할 수 없습니다: {len(tweet)}자")
            if len(tweet) < 10:
                continue  # 너무 짧은 트윗은 스킵
            validated_tweets.append(tweet)
        
        if not validated_tweets:
            raise ValueError("유효한 트윗이 없습니다.")
        
        return validated_tweets


class InstagramPostResponse(BaseModel):
    """인스타그램 포스트 생성 응답 모델"""
    caption: str = Field(..., description="캡션", min_length=50)
    hashtags: List[str] = Field(..., description="해시태그 목록")
    
    @validator('caption')
    def validate_caption(cls, v):
        if len(v.strip()) < 50:
            raise ValueError("캡션은 최소 50자 이상이어야 합니다.")
        return v.strip()
    
    @validator('hashtags')
    def validate_hashtags(cls, v):
        if not v:
            return ["트렌드분석", "인사이트", "데이터분석"]
        
        # 해시태그 정제
        cleaned = []
        for tag in v:
            tag = tag.strip().lstrip('#')
            if tag and len(tag) > 0:
                cleaned.append(tag)
        
        return cleaned[:15]  # 최대 15개로 제한
