"""Account model for social media accounts."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer
from sqlalchemy.sql import func
from datetime import datetime
import json

from app.database import Base
from app.utils.encryption import encrypt_token, decrypt_token


class Account(Base):
    """Social media account model."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)  # instagram, tiktok, facebook, linkedin
    username = Column(String(255), nullable=False)
    account_name = Column(String(255), nullable=True)  # Display name
    encrypted_access_token = Column(String, nullable=False)
    encrypted_refresh_token = Column(String, nullable=True)
    account_id = Column(String(255), nullable=False)  # Platform's account ID
    account_type = Column(String(50), nullable=False)  # business, creator, personal
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    followers_count = Column(Integer, default=0)
    metadata = Column(String, nullable=True)  # JSON metadata
    last_posted_at = Column(DateTime(timezone=True), nullable=True)
    last_sync_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def set_access_token(self, token: str) -> None:
        """Encrypt and store access token."""
        self.encrypted_access_token = encrypt_token(token)

    def get_access_token(self) -> str:
        """Decrypt and return access token."""
        return decrypt_token(self.encrypted_access_token)

    def set_refresh_token(self, token: str) -> None:
        """Encrypt and store refresh token."""
        self.encrypted_refresh_token = encrypt_token(token)

    def get_refresh_token(self) -> str:
        """Decrypt and return refresh token."""
        if self.encrypted_refresh_token:
            return decrypt_token(self.encrypted_refresh_token)
        return None

    def get_metadata(self) -> dict:
        """Get metadata as dictionary."""
        if self.metadata:
            return json.loads(self.metadata)
        return {}

    def set_metadata(self, data: dict) -> None:
        """Set metadata from dictionary."""
        self.metadata = json.dumps(data)

    def __repr__(self):
        return f"<Account(id={self.id}, platform={self.platform}, username={self.username})>"
