"""Application configuration."""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # App
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/ai_social_media"
    )
    database_echo: bool = os.getenv("DATABASE_ECHO", "false").lower() == "true"

    # API Keys
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "")

    # Platforms
    instagram_api_version: str = os.getenv("INSTAGRAM_API_VERSION", "v18.0")
    tiktok_api_version: str = os.getenv("TIKTOK_API_VERSION", "v1")

    # Posting Schedule (Cameroon Time)
    first_post_time: str = os.getenv("FIRST_POST_TIME", "12:00")
    second_post_time: str = os.getenv("SECOND_POST_TIME", "18:00")
    timezone: str = os.getenv("TIMEZONE", "Africa/Douala")

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # AI Model
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1024"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    # Content Generation
    default_content_theme: str = os.getenv("DEFAULT_CONTENT_THEME", "fashion")
    min_caption_length: int = int(os.getenv("MIN_CAPTION_LENGTH", "30"))
    max_caption_length: int = int(os.getenv("MAX_CAPTION_LENGTH", "2200"))

    # Analytics
    analytics_fetch_interval: int = int(
        os.getenv("ANALYTICS_FETCH_INTERVAL", "86400")
    )  # 24 hours
    keep_analytics_days: int = int(os.getenv("KEEP_ANALYTICS_DAYS", "90"))

    # Feature Flags
    enable_instagram: bool = os.getenv("ENABLE_INSTAGRAM", "true").lower() == "true"
    enable_tiktok: bool = os.getenv("ENABLE_TIKTOK", "true").lower() == "true"
    enable_facebook: bool = os.getenv("ENABLE_FACEBOOK", "false").lower() == "true"
    enable_linkedin: bool = os.getenv("ENABLE_LINKEDIN", "false").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
