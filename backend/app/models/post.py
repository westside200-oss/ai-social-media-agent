"""Post and analytics models."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey, Text
from sqlalchemy.sql import func
from datetime import datetime
import json

from app.database import Base


class Post(Base):
    """Social media post model."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # instagram, tiktok, etc
    platform_post_id = Column(String(255), nullable=True)  # ID from platform
    content = Column(Text, nullable=False)  # Caption/content
    content_type = Column(String(50), nullable=False)  # text, video, image, carousel
    video_url = Column(String, nullable=True)
    image_urls = Column(String, nullable=True)  # JSON array
    hashtags = Column(String, nullable=True)  # Comma-separated
    mentions = Column(String, nullable=True)  # Comma-separated
    template_used = Column(String(255), nullable=True)
    theme = Column(String(255), nullable=True)  # summer_collection, new_arrivals, etc
    is_posted = Column(Boolean, default=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=True)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def get_image_urls(self) -> list:
        """Get image URLs as list."""
        if self.image_urls:
            return json.loads(self.image_urls)
        return []

    def set_image_urls(self, urls: list) -> None:
        """Set image URLs from list."""
        self.image_urls = json.dumps(urls)

    def __repr__(self):
        return f"<Post(id={self.id}, account_id={self.account_id}, platform={self.platform})>"


class PostAnalytics(Base):
    """Analytics for posts."""

    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)  # Instagram specific
    clicks = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)  # (likes + comments + shares) / impressions
    sentiment = Column(String(50), nullable=True)  # positive, neutral, negative
    top_performing_features = Column(String, nullable=True)  # JSON
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<PostAnalytics(id={self.id}, post_id={self.post_id}, engagement_rate={self.engagement_rate})>"
