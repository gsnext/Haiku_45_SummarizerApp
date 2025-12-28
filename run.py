"""Application entry point and CLI for running GenAIsummarizer."""
import os
import sys
import uvicorn
from pathlib import Path

# Add the backend to the path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.main import app
from backend.app.config import settings
from backend.app.logger import logger


def run_server():
    """Start the Uvicorn web server."""
    logger.info(f"Starting {settings.APP_NAME} server on {settings.HOST}:{settings.PORT}")

    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


def main():
    """Main entry point for the CLI."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command in ["--help", "-h"]:
            print_help()
            return 0
        elif command in ["--version", "-v"]:
            print(f"{settings.APP_NAME} v{settings.APP_VERSION}")
            return 0
    else:
        # Default: run the server
        run_server()
        return 0

    return 1


def print_help():
    """Print help message."""
    print(f"""
{settings.APP_NAME} v{settings.APP_VERSION}

Usage: python run.py [COMMAND]

Commands:
    (no command)    Start the web server (default)
    --help, -h      Show this help message
    --version, -v   Show version information

Environment Variables:
    PORT                        Server port (default: 8000)
    AZURE_OPENAI_API_KEY       Azure OpenAI API key
    AZURE_OPENAI_ENDPOINT      Azure OpenAI endpoint
    AZURE_OPENAI_DEPLOYMENT_NAME   Deployment name
    JWT_SECRET_KEY             JWT secret key for token signing
    LOG_LEVEL                   Logging level (INFO, DEBUG, WARNING, ERROR)

Examples:
    python run.py                           # Start server on default port
    PORT=9000 python run.py                # Start server on port 9000
    AZURE_OPENAI_API_KEY=<key> python run.py   # Start with Azure credentials

For detailed documentation, see README.md
    """)


if __name__ == "__main__":
    sys.exit(main())
