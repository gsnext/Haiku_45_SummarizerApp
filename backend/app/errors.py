"""Custom error handling and exception classes."""
from typing import Optional


class SummarizerException(Exception):
    """Base exception for the summarizer application."""

    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(SummarizerException):
    """Raised when input validation fails."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, "VALIDATION_ERROR", status_code)


class FileFormatError(SummarizerException):
    """Raised when an unsupported file format is provided."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, "FILE_FORMAT_ERROR", status_code)


class FileSizeError(SummarizerException):
    """Raised when a file exceeds the maximum allowed size."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message, "FILE_SIZE_ERROR", status_code)


class ExtractionError(SummarizerException):
    """Raised when text extraction fails."""

    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message, "EXTRACTION_ERROR", status_code)


class SummarizationError(SummarizerException):
    """Raised when summarization fails."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, "SUMMARIZATION_ERROR", status_code)


class AuthenticationError(SummarizerException):
    """Raised when authentication fails."""

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, "AUTHENTICATION_ERROR", status_code)


class URLFetchError(SummarizerException):
    """Raised when fetching URL content fails."""

    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message, "URL_FETCH_ERROR", status_code)


def format_error_response(exception: SummarizerException) -> dict:
    """Format exception as API response."""
    return {
        "error": {
            "message": exception.message,
            "code": exception.error_code,
        }
    }
