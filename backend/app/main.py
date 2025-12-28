"""Main application entry point and FastAPI setup."""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .logger import logger
from . import api
from . import ui
from .errors import SummarizerException

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="GenAIsummarizer - A self-hosted AI-powered document summarization application",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router)
app.include_router(ui.router)


@app.exception_handler(SummarizerException)
async def summarizer_exception_handler(request, exc: SummarizerException):
    """Handle custom summarizer exceptions."""
    logger.error(f"SummarizerException: {exc.message}")
    return {
        "detail": {
            "error": {
                "message": exc.message,
                "code": exc.error_code,
            }
        }
    }


logger.info("Application initialized successfully")
