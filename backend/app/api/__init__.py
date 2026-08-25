"""API routes initialization."""

from fastapi import APIRouter
from app.api.accounts import router as accounts_router
from app.api.posts import router as posts_router
from app.api.analytics import router as analytics_router
from app.api.health import router as health_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(accounts_router)
api_router.include_router(posts_router)
api_router.include_router(analytics_router)

__all__ = ["api_router"]
