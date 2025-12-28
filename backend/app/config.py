"""Configuration management for the GenAIsummarizer application."""
import os
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # App settings
    APP_NAME: str = "GenAIsummarizer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server settings
    HOST: str = "127.0.0.1"
    PORT: int = int(os.getenv("PORT", "8000"))

    # Azure OpenAI settings
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

    # Summary configuration
    SUMMARY_LENGTH_SHORT: int = 50
    SUMMARY_LENGTH_MEDIUM: int = 150
    SUMMARY_LENGTH_LONG: int = 300

    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FORMATS: list = ["txt", "pdf", "docx", "url"]

    # Batch processing
    MAX_BATCH_SIZE: int = 10

    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Database settings (if needed in future)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./summarizer.db")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
