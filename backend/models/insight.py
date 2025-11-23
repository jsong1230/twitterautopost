from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id"), nullable=False)
    keyword = Column(String, nullable=False)
    summary_kr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    tweets_analyzed = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    posts = relationship("Post", back_populates="insight", cascade="all, delete-orphan")

