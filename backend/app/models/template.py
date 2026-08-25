"""Content template model."""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text
from sqlalchemy.sql import func

from app.database import Base


class ContentTemplate(Base):
    """Content generation templates."""

    __tablename__ = "content_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    platform = Column(String(50), nullable=False)  # instagram, tiktok, or all
    category = Column(String(50), nullable=False)  # new_arrivals, styling_tips, promotion, etc
    prompt_template = Column(Text, nullable=False)  # Claude prompt template
    example_output = Column(Text, nullable=True)  # Example content generated
    min_length = Column(Integer, default=30)
    max_length = Column(Integer, default=2200)
    hashtag_suggestions = Column(String, nullable=True)  # Comma-separated
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ContentTemplate(id={self.id}, name={self.name}, platform={self.platform})>"
