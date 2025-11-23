from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from backend.database import Base


class PostType(str, enum.Enum):
    TWEET = "tweet"
    INSTAGRAM = "instagram"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    insight_id = Column(Integer, ForeignKey("insights.id"), nullable=False)
    post_type = Column(Enum(PostType), nullable=False)
    content = Column(Text, nullable=False)
    hashtags = Column(Text, nullable=True)  # JSON string or comma-separated
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    insight = relationship("Insight", back_populates="posts")

