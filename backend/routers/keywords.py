from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from pydantic import BaseModel, field_serializer
from backend.database import get_db
from backend.models.keyword import Keyword

router = APIRouter(prefix="/api/keywords", tags=["keywords"])


class KeywordCreate(BaseModel):
    keyword: str


class KeywordResponse(BaseModel):
    id: int
    keyword: str
    is_active: bool
    created_at: datetime
    
    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat() if dt else None

    class Config:
        from_attributes = True


@router.get("/", response_model=List[KeywordResponse])
async def get_keywords(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """키워드 목록 조회"""
    keywords = db.query(Keyword).offset(skip).limit(limit).all()
    return keywords


@router.post("/", response_model=KeywordResponse)
async def create_keyword(
    keyword_data: KeywordCreate,
    db: Session = Depends(get_db)
):
    """키워드 생성"""
    # 중복 체크
    existing = db.query(Keyword).filter(Keyword.keyword == keyword_data.keyword).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 키워드입니다.")
    
    keyword = Keyword(keyword=keyword_data.keyword)
    db.add(keyword)
    db.commit()
    db.refresh(keyword)
    return keyword


@router.delete("/{keyword_id}")
async def delete_keyword(
    keyword_id: int,
    db: Session = Depends(get_db)
):
    """키워드 삭제"""
    keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다.")
    
    db.delete(keyword)
    db.commit()
    return {"message": "키워드가 삭제되었습니다."}


@router.patch("/{keyword_id}/toggle")
async def toggle_keyword(
    keyword_id: int,
    db: Session = Depends(get_db)
):
    """키워드 활성/비활성 토글"""
    keyword = db.query(Keyword).filter(Keyword.id == keyword_id).first()
    if not keyword:
        raise HTTPException(status_code=404, detail="키워드를 찾을 수 없습니다.")
    
    keyword.is_active = not keyword.is_active
    db.commit()
    db.refresh(keyword)
    return keyword

