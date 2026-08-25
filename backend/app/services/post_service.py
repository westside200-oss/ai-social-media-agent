"""Post service."""

import logging
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.models.post import Post
from app.models.account import Account
from app.schemas.post import PostCreate, PostGenerateRequest
from app.agents.content_generator import ContentGenerator
from app.agents.platform_adapter import PlatformAdapter

logger = logging.getLogger(__name__)


class PostService:
    """Service for post operations."""

    def __init__(self):
        """Initialize post service."""
        self.content_gen = ContentGenerator()

    async def create_post(self, db: Session, post_data: PostCreate) -> Post:
        """Create a new post."""
        # Verify account exists
        account = db.query(Account).filter(Account.id == post_data.account_id).first()
        if not account:
            raise ValueError(f"Account {post_data.account_id} not found")
        
        post = Post(
            account_id=post_data.account_id,
            platform=post_data.platform,
            content=post_data.content,
            content_type=post_data.content_type,
            hashtags=post_data.hashtags,
            mentions=post_data.mentions,
            video_url=post_data.video_url,
            template_used=post_data.template_used,
            theme=post_data.theme,
        )
        
        if post_data.image_urls:
            post.set_image_urls(post_data.image_urls)
        
        if post_data.scheduled_time:
            post.scheduled_time = post_data.scheduled_time
        
        db.add(post)
        db.commit()
        db.refresh(post)
        
        logger.info(f"Post created: {post.id} for account {post.account_id}")
        return post

    async def generate_and_create_post(
        self, db: Session, request: PostGenerateRequest
    ) -> Post:
        """Generate content using AI and create a post."""
        # Verify account exists
        account = db.query(Account).filter(Account.id == request.account_id).first()
        if not account:
            raise ValueError(f"Account {request.account_id} not found")
        
        # Generate content
        content = self.content_gen.generate_caption(
            platform=request.platform,
            theme=request.theme,
            template=request.template,
            additional_context=request.additional_context,
        )
        
        # Create post
        post = Post(
            account_id=request.account_id,
            platform=request.platform,
            content=content,
            content_type="text",
            theme=request.theme,
            template_used=request.template,
        )
        
        if request.scheduled_time:
            post.scheduled_time = request.scheduled_time
        
        db.add(post)
        db.commit()
        db.refresh(post)
        
        logger.info(
            f"Post generated and created: {post.id} for account {post.account_id}"
        )
        return post

    async def publish_post(self, db: Session, post_id: int) -> dict:
        """Publish a post to the platform."""
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError(f"Post {post_id} not found")
        
        if post.is_posted:
            raise ValueError("Post already published")
        
        # Get account and credentials
        account = db.query(Account).filter(Account.id == post.account_id).first()
        if not account:
            raise ValueError(f"Account not found")
        
        # Use platform adapter to post
        adapter = PlatformAdapter(post.platform, account.get_access_token())
        result = await adapter.post_content(
            account_id=account.account_id,
            content=post.content,
            media_urls=post.get_image_urls() if post.image_urls else None,
            hashtags=post.hashtags,
        )
        
        if result["success"]:
            post.is_posted = True
            post.posted_at = datetime.utcnow()
            post.platform_post_id = result.get("platform_id")
            db.commit()
            logger.info(f"Post published: {post.id}")
            return {"status": "success", "platform_id": result.get("platform_id")}
        else:
            logger.error(f"Failed to publish post: {result.get('error')}")
            raise Exception(f"Failed to publish: {result.get('error')}")
