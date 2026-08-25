"""Account schemas."""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class AccountBase(BaseModel):
    """Base account schema."""
    platform: str
    username: str
    account_name: Optional[str] = None
    account_id: str
    account_type: str  # business, creator, personal


class AccountCreate(AccountBase):
    """Schema for creating an account."""
    access_token: str
    refresh_token: Optional[str] = None


class AccountUpdate(BaseModel):
    """Schema for updating an account."""
    account_name: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    is_active: Optional[bool] = None


class AccountResponse(AccountBase):
    """Schema for account responses."""
    id: int
    is_active: bool
    is_verified: bool
    followers_count: int
    last_posted_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
