"""Main FastAPI application."""

import logging
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.utils.logger import setup_logging
from app.api import api_router
from app.scheduler.posting import PostingScheduler

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

settings = get_settings()

# Initialize scheduler
scheduler = PostingScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifecycle."""
    # Startup
    logger.info("Starting AI Social Media Agent API")
    init_db()
    scheduler.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Social Media Agent API")
    scheduler.shutdown()


# Create FastAPI app
app = FastAPI(
    title="AI Social Media Agent API",
    description="Automated content generation and posting for social media",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include API routes
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )
