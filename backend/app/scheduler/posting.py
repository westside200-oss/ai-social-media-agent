"""Scheduler module for posting at scheduled times."""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime
import pytz

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class PostingScheduler:
    """Schedule posts to be published at specific times."""

    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = BackgroundScheduler()
        self.timezone = pytz.timezone(settings.timezone)

    def start(self):
        """Start the scheduler."""
        self._schedule_daily_posts()
        self.scheduler.start()
        logger.info("Posting scheduler started")

    def shutdown(self):
        """Shutdown the scheduler."""
        self.scheduler.shutdown()
        logger.info("Posting scheduler shutdown")

    def _schedule_daily_posts(self):
        """Schedule posts for the two daily posting times."""
        # Parse posting times
        first_time = settings.first_post_time.split(":")
        second_time = settings.second_post_time.split(":")
        
        first_hour, first_minute = int(first_time[0]), int(first_time[1])
        second_hour, second_minute = int(second_time[0]), int(second_time[1])
        
        # Schedule first posting
        self.scheduler.add_job(
            self._post_scheduled_content,
            trigger=CronTrigger(
                hour=first_hour,
                minute=first_minute,
                timezone=self.timezone,
            ),
            id="daily_post_morning",
            name="Daily post (first time)",
            replace_existing=True,
        )
        
        # Schedule second posting
        self.scheduler.add_job(
            self._post_scheduled_content,
            trigger=CronTrigger(
                hour=second_hour,
                minute=second_minute,
                timezone=self.timezone,
            ),
            id="daily_post_evening",
            name="Daily post (second time)",
            replace_existing=True,
        )
        
        logger.info(
            f"Scheduled posts at {settings.first_post_time} and {settings.second_post_time} {settings.timezone}"
        )

    async def _post_scheduled_content(self):
        """Post scheduled content (called by scheduler)."""
        logger.info(f"Posting scheduled content at {datetime.now()}")
        # This will be implemented by the background job handler
        pass
