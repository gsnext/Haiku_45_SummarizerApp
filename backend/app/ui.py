"""Web UI backend logic and route handlers."""
from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import uuid
from typing import Optional
from datetime import datetime

from .auth import get_user_token, verify_token, get_guest_token
from .api import summaries_db, users_db
from .summarizer.engine import engine
from .summarizer.utils import extract_text, validate_file_size
from .errors import SummarizerException, format_error_response
from .logger import logger

router = APIRouter(tags=["UI"])

# Setup Jinja2 environment
template_dir = Path(__file__).parent.parent.parent / "frontend" / "templates"
jinja_env = Environment(loader=FileSystemLoader(template_dir))


@router.get("/", response_class=HTMLResponse)
async def index() -> str:
    """Serve the main dashboard page (guest accessible)."""
    try:
        template = jinja_env.get_template("index.html")
        return template.render()
    except Exception as e:
        logger.error(f"Failed to render index: {str(e)}")
        return "<h1>Error loading dashboard</h1>"


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(user_id: str = Depends(verify_token)) -> str:
    """Serve the user dashboard (guest accessible)."""
    try:
        template = jinja_env.get_template("dashboard.html")
        is_guest = user_id.startswith("guest_")
        return template.render(user_id=user_id, is_guest=is_guest)
    except Exception as e:
        logger.error(f"Failed to render dashboard: {str(e)}")
        return "<h1>Error loading dashboard</h1>"


@router.get("/history", response_class=HTMLResponse)
async def history_page(user_id: str = Depends(verify_token)) -> str:
    """Serve the history page (guest accessible)."""
    try:
        user_summaries = users_db.get(user_id, [])
        summaries = [summaries_db[sid] for sid in user_summaries if sid in summaries_db]
        is_guest = user_id.startswith("guest_")

        template = jinja_env.get_template("history.html")
        return template.render(summaries=summaries, user_id=user_id, is_guest=is_guest)
    except Exception as e:
        logger.error(f"Failed to render history: {str(e)}")
        return "<h1>Error loading history</h1>"


@router.post("/api/login")
async def login(username: str = Form(...)) -> JSONResponse:
    """
    Login endpoint to get authentication token for registered users.

    Args:
        username: Username for login

    Returns:
        Authentication token and username
    """
    try:
        if not username or not username.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is required",
            )

        # Generate token for user
        token = get_user_token(username)

        logger.info(f"User {username} logged in")

        return JSONResponse({"token": token, "username": username})

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


@router.get("/api/guest-token")
async def get_guest_access() -> JSONResponse:
    """
    Get a guest access token for anonymous users.

    Returns:
        Guest token and guest ID
    """
    try:
        token, guest_id = get_guest_token()
        logger.info(f"Guest user created: {guest_id}")
        return JSONResponse({"token": token, "username": guest_id, "is_guest": True})
    except Exception as e:
        logger.error(f"Failed to create guest token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create guest token",
        )


@router.get("/about", response_class=HTMLResponse)
async def about() -> str:
    """Serve the about page."""
    try:
        template = jinja_env.get_template("about.html")
        return template.render()
    except Exception as e:
        logger.error(f"Failed to render about page: {str(e)}")
        return "<h1>About GenAIsummarizer</h1><p>An AI-powered summarization tool</p>"
