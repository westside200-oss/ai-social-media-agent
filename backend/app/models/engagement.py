"""Engagement log model for tracking AI learning."""

from sqlalchemy import Column, String, DateTime, Integer, Float, Text
from sqlalchemy.sql import func

from app.database import Base


class EngagementLog(Base):
    """Log engagement data for AI feedback loop."""

    __tablename__ = "engagement_logs"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False)
    platform = Column(String(50), nullable=False)
    theme = Column(String(255), nullable=True)
    content_type = Column(String(50), nullable=True)
    engagement_rate = Column(Float, default=0.0)
    top_performing_keywords = Column(Text, nullable=True)  # JSON
    top_performing_hashtags = Column(Text, nullable=True)  # JSON
    audience_sentiment = Column(String(50), nullable=True)
    insights = Column(Text, nullable=True)  # JSON with learnings
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<EngagementLog(id={self.id}, post_id={self.post_id}, engagement_rate={self.engagement_rate})>"
