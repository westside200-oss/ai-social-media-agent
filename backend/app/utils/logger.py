"""Logging configuration."""

import logging
import logging.config
from app.config import get_settings

settings = get_settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": settings.log_level,
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": settings.log_level,
            "formatter": "detailed",
            "filename": "logs/app.log",
            "maxBytes": 10485760,
            "backupCount": 5,
        },
    },
    "root": {
        "level": settings.log_level,
        "handlers": ["console", "file"],
    },
    "loggers": {
        "app": {
            "level": settings.log_level,
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "anthropic": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


def setup_logging():
    """Setup logging configuration."""
    logging.config.dictConfig(LOGGING_CONFIG)
