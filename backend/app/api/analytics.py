"""API routes for analytics and insights."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.database import get_db
from app.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
service = AnalyticsService()


@router.get("/account/{account_id}")
async def get_account_analytics(
    account_id: int,
    days: Optional[int] = 30,
    db: Session = Depends(get_db),
):
    """Get analytics for an account."""
    try:
        analytics = await service.get_account_analytics(db, account_id, days)
        return analytics
    except Exception as e:
        logger.error(f"Error fetching account analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/platform/{platform}")
async def get_platform_analytics(
    platform: str,
    days: Optional[int] = 30,
    db: Session = Depends(get_db),
):
    """Get analytics for a platform."""
    try:
        analytics = await service.get_platform_analytics(db, platform, days)
        return analytics
    except Exception as e:
        logger.error(f"Error fetching platform analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/insights")
async def get_insights(
    account_id: Optional[int] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get AI insights for content improvement."""
    try:
        insights = await service.get_insights(db, account_id, platform)
        return insights
    except Exception as e:
        logger.error(f"Error fetching insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/sync")
async def sync_analytics(
    account_id: Optional[int] = None,
    platform: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Manually sync analytics from platforms."""
    try:
        result = await service.sync_all_analytics(db, account_id, platform)
        return result
    except Exception as e:
        logger.error(f"Error syncing analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
