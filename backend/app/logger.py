"""Logging setup and utilities for the application."""
from loguru import logger
import sys
from .config import settings


def setup_logger():
    """Configure loguru logger for the application."""
    # Remove default handler
    logger.remove()

    # Add new handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
    )

    # Add file handler for logs
    logger.add(
        "logs/summarizer.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL,
        rotation="500 MB",
        retention="7 days",
    )

    return logger


# Initialize logger on module import
logger = setup_logger()
