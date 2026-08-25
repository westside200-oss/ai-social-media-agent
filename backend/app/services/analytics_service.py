"""Analytics service."""

import logging
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional

from app.models.post import Post, PostAnalytics
from app.models.account import Account
from app.agents.analytics_analyzer import AnalyticsAnalyzer

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for analytics operations."""

    def __init__(self):
        """Initialize analytics service."""
        self.analyzer = AnalyticsAnalyzer()

    async def get_account_analytics(
        self, db: Session, account_id: int, days: int = 30
    ) -> dict:
        """Get analytics for an account."""
        since = datetime.utcnow() - timedelta(days=days)
        
        analytics = (
            db.query(PostAnalytics)
            .join(Post, PostAnalytics.post_id == Post.id)
            .filter(
                Post.account_id == account_id,
                PostAnalytics.created_at >= since,
            )
            .all()
        )
        
        if not analytics:
            return {
                "account_id": account_id,
                "total_posts": 0,
                "total_impressions": 0,
                "average_engagement_rate": 0.0,
            }
        
        total_impressions = sum(a.impressions for a in analytics)
        total_interactions = sum(
            (a.likes + a.comments + a.shares) for a in analytics
        )
        avg_engagement = (
            (total_interactions / total_impressions * 100)
            if total_impressions > 0
            else 0.0
        )
        
        return {
            "account_id": account_id,
            "total_posts": len(analytics),
            "total_impressions": total_impressions,
            "total_likes": sum(a.likes for a in analytics),
            "total_comments": sum(a.comments for a in analytics),
            "total_shares": sum(a.shares for a in analytics),
            "average_engagement_rate": round(avg_engagement, 2),
            "period_days": days,
        }

    async def get_platform_analytics(
        self, db: Session, platform: str, days: int = 30
    ) -> dict:
        """Get analytics for a platform."""
        since = datetime.utcnow() - timedelta(days=days)
        
        analytics = (
            db.query(PostAnalytics)
            .filter(
                PostAnalytics.platform == platform,
                PostAnalytics.created_at >= since,
            )
            .all()
        )
        
        if not analytics:
            return {
                "platform": platform,
                "total_posts": 0,
                "total_impressions": 0,
            }
        
        total_impressions = sum(a.impressions for a in analytics)
        total_interactions = sum(
            (a.likes + a.comments + a.shares) for a in analytics
        )
        avg_engagement = (
            (total_interactions / total_impressions * 100)
            if total_impressions > 0
            else 0.0
        )
        
        return {
            "platform": platform,
            "total_posts": len(analytics),
            "total_impressions": total_impressions,
            "total_likes": sum(a.likes for a in analytics),
            "total_comments": sum(a.comments for a in analytics),
            "total_shares": sum(a.shares for a in analytics),
            "average_engagement_rate": round(avg_engagement, 2),
        }

    async def get_insights(
        self,
        db: Session,
        account_id: Optional[int] = None,
        platform: Optional[str] = None,
    ) -> dict:
        """Get AI insights for content improvement."""
        query = db.query(Post)
        
        if account_id:
            query = query.filter(Post.account_id == account_id)
        
        if platform:
            query = query.filter(Post.platform == platform)
        
        # Get recent posts with analytics
        recent_posts = query.filter(Post.is_posted == True).order_by(
            Post.posted_at.desc()
        ).limit(20).all()
        
        if not recent_posts:
            return {"message": "No posts with analytics available"}
        
        # Build data for analyzer
        posts_data = []
        for post in recent_posts:
            latest_analytics = (
                db.query(PostAnalytics)
                .filter(PostAnalytics.post_id == post.id)
                .order_by(PostAnalytics.created_at.desc())
                .first()
            )
            
            if latest_analytics:
                posts_data.append({
                    "theme": post.theme,
                    "content_type": post.content_type,
                    "platform": post.platform,
                    "hashtags": post.hashtags,
                    "engagement_rate": latest_analytics.engagement_rate,
                })
        
        # Extract patterns
        patterns = self.analyzer.extract_learning_patterns(posts_data)
        return patterns

    async def sync_all_analytics(
        self,
        db: Session,
        account_id: Optional[int] = None,
        platform: Optional[str] = None,
    ) -> dict:
        """Sync analytics from all platforms."""
        # This would be called by a scheduled job
        logger.info("Analytics sync initiated")
        return {"status": "sync_started"}
