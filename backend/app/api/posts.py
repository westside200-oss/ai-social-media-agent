"""API routes for post management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.database import get_db
from app.models.post import Post, PostAnalytics
from app.schemas.post import PostCreate, PostResponse, PostGenerateRequest
from app.services.post_service import PostService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/posts", tags=["posts"])
service = PostService()


@router.post("/generate", response_model=PostResponse)
async def generate_post(
    request: PostGenerateRequest,
    db: Session = Depends(get_db),
):
    """Generate a new post using AI."""
    try:
        post = await service.generate_and_create_post(db, request)
        return post
    except Exception as e:
        logger.error(f"Error generating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
):
    """Create a new post manually."""
    try:
        post = await service.create_post(db, post_data)
        return post
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    account_id: Optional[int] = None,
    platform: Optional[str] = None,
    is_posted: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """List posts with optional filters."""
    query = db.query(Post)
    
    if account_id:
        query = query.filter(Post.account_id == account_id)
    
    if platform:
        query = query.filter(Post.platform == platform)
    
    if is_posted is not None:
        query = query.filter(Post.is_posted == is_posted)
    
    posts = query.order_by(Post.created_at.desc()).all()
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific post by ID."""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    
    return post


@router.post("/{post_id}/publish")
async def publish_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    """Publish a scheduled post immediately."""
    try:
        result = await service.publish_post(db, post_id)
        return result
    except Exception as e:
        logger.error(f"Error publishing post: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{post_id}/analytics", response_model=dict)
async def get_post_analytics(
    post_id: int,
    db: Session = Depends(get_db),
):
    """Get analytics for a posted content."""
    analytics = (
        db.query(PostAnalytics)
        .filter(PostAnalytics.post_id == post_id)
        .order_by(PostAnalytics.created_at.desc())
        .first()
    )
    
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analytics not found",
        )
    
    return {
        "impressions": analytics.impressions,
        "reach": analytics.reach,
        "likes": analytics.likes,
        "comments": analytics.comments,
        "shares": analytics.shares,
        "engagement_rate": analytics.engagement_rate,
        "fetched_at": analytics.fetched_at,
    }
