"""Post schemas."""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    """Base post schema."""
    platform: str
    content: str
    content_type: str  # text, video, image, carousel
    hashtags: Optional[str] = None
    mentions: Optional[str] = None


class PostCreate(PostBase):
    """Schema for creating a post."""
    account_id: int
    video_url: Optional[str] = None
    image_urls: Optional[List[str]] = None
    template_used: Optional[str] = None
    theme: Optional[str] = None
    scheduled_time: Optional[datetime] = None


class PostGenerateRequest(BaseModel):
    """Schema for AI-generated post request."""
    account_id: int
    platform: str
    theme: str
    template: Optional[str] = None
    additional_context: Optional[str] = None
    scheduled_time: Optional[datetime] = None


class PostResponse(PostBase):
    """Schema for post responses."""
    id: int
    account_id: int
    platform_post_id: Optional[str] = None
    is_posted: bool
    posted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
