"""REST API endpoints for the GenAIsummarizer application."""
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import datetime
import uuid
from .auth import verify_token
from .summarizer.engine import engine
from .summarizer.utils import extract_text, validate_file_size, validate_format
from .errors import SummarizerException, format_error_response, URLFetchError, ExtractionError, FileSizeError
from .logger import logger

router = APIRouter(prefix="/api", tags=["API"])

# In-memory storage for summaries (in production, use database)
summaries_db: dict = {}
users_db: dict = {}


class SummaryRequest(BaseModel):
    """Request model for text summarization."""

    text: str
    summary_length: Literal["short", "medium", "long"] = "medium"


class SummaryResponse(BaseModel):
    """Response model for summary."""

    id: str
    text: str
    summary: str
    length: str
    created_at: datetime
    user_id: Optional[str] = None


class BatchRequest(BaseModel):
    """Request model for batch processing."""

    items: List[dict]
    summary_length: Literal["short", "medium", "long"] = "medium"


class HistoryResponse(BaseModel):
    """Response model for history."""

    summaries: List[SummaryResponse]
    total: int


@router.post("/summarize")
async def summarize_text(
    request: SummaryRequest,
    user_id: str = Depends(verify_token),
) -> dict:
    """
    Summarize provided text.

    Args:
        request: Summary request with text and desired length
        user_id: Authenticated user ID

    Returns:
        Summary response with ID, original text, and summary
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text content cannot be empty",
            )

        logger.info(f"Summarizing text for user {user_id}")

        summary = await engine.generate_summary(request.text, request.summary_length)

        summary_id = str(uuid.uuid4())
        summary_record = {
            "id": summary_id,
            "text": request.text,
            "summary": summary,
            "length": request.summary_length,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
        }

        summaries_db[summary_id] = summary_record

        if user_id not in users_db:
            users_db[user_id] = []
        users_db[user_id].append(summary_id)

        logger.info(f"Summary {summary_id} created for user {user_id}")

        return summary_record

    except SummarizerException as e:
        logger.error(f"Summarization error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=format_error_response(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error during summarization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}},
        )


@router.post("/summarize/file")
async def summarize_file(
    file: UploadFile = File(...),
    summary_length: Literal["short", "medium", "long"] = Form("medium"),
    user_id: str = Depends(verify_token),
) -> dict:
    """
    Summarize uploaded file (PDF, DOCX, or TXT).

    Args:
        file: Uploaded file
        summary_length: Desired summary length
        user_id: Authenticated user ID

    Returns:
        Summary response
    """
    try:
        # Validate file format
        file_ext = file.filename.split(".")[-1].lower() if file.filename else ""
        if file_ext not in ["txt", "pdf", "docx"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"message": f"Unsupported file format: {file_ext}", "code": "FILE_FORMAT_ERROR"}},
            )

        # Read file content
        content = await file.read()

        # Validate file size
        validate_file_size(len(content))

        logger.info(f"Processing file {file.filename} for user {user_id}")

        # Extract text
        text = await extract_text(content, file_ext)

        if not text or not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"message": "Could not extract text from file", "code": "EXTRACTION_ERROR"}},
            )

        # Generate summary
        summary = await engine.generate_summary(text, summary_length)

        summary_id = str(uuid.uuid4())
        summary_record = {
            "id": summary_id,
            "text": text[:500],  # Store only first 500 chars in response
            "summary": summary,
            "length": summary_length,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "filename": file.filename,
        }

        summaries_db[summary_id] = summary_record

        if user_id not in users_db:
            users_db[user_id] = []
        users_db[user_id].append(summary_id)

        logger.info(f"File summary {summary_id} created for user {user_id}")

        return summary_record

    except SummarizerException as e:
        logger.error(f"File summarization error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=format_error_response(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error during file summarization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}},
        )


@router.post("/summarize/url")
async def summarize_url(
    url: str = Form(...),
    summary_length: Literal["short", "medium", "long"] = Form("medium"),
    user_id: str = Depends(verify_token),
) -> dict:
    """
    Summarize content from a URL.

    Args:
        url: URL to fetch and summarize
        summary_length: Desired summary length
        user_id: Authenticated user ID

    Returns:
        Summary response
    """
    try:
        logger.info(f"Processing URL {url} for user {user_id}")

        # Extract text from URL
        text = await extract_text(url, "url")

        if not text or not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"message": "Could not extract text from URL", "code": "EXTRACTION_ERROR"}},
            )

        # Generate summary
        summary = await engine.generate_summary(text, summary_length)

        summary_id = str(uuid.uuid4())
        summary_record = {
            "id": summary_id,
            "text": text[:500],
            "summary": summary,
            "length": summary_length,
            "created_at": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "source_url": url,
        }

        summaries_db[summary_id] = summary_record

        if user_id not in users_db:
            users_db[user_id] = []
        users_db[user_id].append(summary_id)

        logger.info(f"URL summary {summary_id} created for user {user_id}")

        return summary_record

    except SummarizerException as e:
        logger.error(f"URL summarization error: {e.message}")
        raise HTTPException(
            status_code=e.status_code,
            detail=format_error_response(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error during URL summarization: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Internal server error", "code": "INTERNAL_ERROR"}},
        )


@router.post("/batch")
async def batch_summarize(
    request: BatchRequest,
    user_id: str = Depends(verify_token),
) -> dict:
    """
    Batch process up to 10 items for summarization.

    Args:
        request: Batch request with up to 10 items
        user_id: Authenticated user ID

    Returns:
        List of summaries
    """
    try:
        if len(request.items) > 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": {"message": "Maximum 10 items per batch", "code": "VALIDATION_ERROR"}},
            )

        logger.info(f"Processing batch of {len(request.items)} items for user {user_id}")

        results = []
        for item in request.items:
            try:
                if "text" in item:
                    summary = await engine.generate_summary(item["text"], request.summary_length)
                    summary_id = str(uuid.uuid4())
                    summary_record = {
                        "id": summary_id,
                        "summary": summary,
                        "length": request.summary_length,
                        "created_at": datetime.utcnow().isoformat(),
                    }
                    results.append(summary_record)
                    summaries_db[summary_id] = summary_record
                    if user_id not in users_db:
                        users_db[user_id] = []
                    users_db[user_id].append(summary_id)
            except Exception as e:
                logger.error(f"Failed to process batch item: {str(e)}")
                results.append({"error": str(e)})

        logger.info(f"Batch processing completed for user {user_id}")

        return {"processed": len(results), "results": results}

    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Batch processing failed", "code": "BATCH_ERROR"}},
        )


@router.get("/history")
async def get_history(user_id: str = Depends(verify_token)) -> dict:
    """
    Get summarization history for the authenticated user.

    Args:
        user_id: Authenticated user ID

    Returns:
        List of user's previous summaries
    """
    try:
        logger.info(f"Retrieving history for user {user_id}")

        user_summaries = users_db.get(user_id, [])
        summaries = [summaries_db[sid] for sid in user_summaries if sid in summaries_db]

        return {
            "summaries": summaries,
            "total": len(summaries),
        }

    except Exception as e:
        logger.error(f"Failed to retrieve history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Failed to retrieve history", "code": "HISTORY_ERROR"}},
        )


@router.get("/summary/{summary_id}")
async def get_summary(summary_id: str, user_id: str = Depends(verify_token)) -> dict:
    """
    Get a specific summary by ID.

    Args:
        summary_id: ID of the summary
        user_id: Authenticated user ID

    Returns:
        Summary details
    """
    try:
        if summary_id not in summaries_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": {"message": "Summary not found", "code": "NOT_FOUND"}},
            )

        summary = summaries_db[summary_id]

        # Check ownership
        if summary.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": {"message": "Access denied", "code": "FORBIDDEN"}},
            )

        logger.info(f"Retrieved summary {summary_id} for user {user_id}")

        return summary

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Failed to retrieve summary", "code": "INTERNAL_ERROR"}},
        )


@router.delete("/summary/{summary_id}")
async def delete_summary(summary_id: str, user_id: str = Depends(verify_token)) -> dict:
    """
    Delete a summary.

    Args:
        summary_id: ID of the summary to delete
        user_id: Authenticated user ID

    Returns:
        Confirmation of deletion
    """
    try:
        if summary_id not in summaries_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": {"message": "Summary not found", "code": "NOT_FOUND"}},
            )

        summary = summaries_db[summary_id]

        # Check ownership
        if summary.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"error": {"message": "Access denied", "code": "FORBIDDEN"}},
            )

        del summaries_db[summary_id]

        # Remove from user history
        if user_id in users_db and summary_id in users_db[user_id]:
            users_db[user_id].remove(summary_id)

        logger.info(f"Deleted summary {summary_id} for user {user_id}")

        return {"message": "Summary deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": {"message": "Failed to delete summary", "code": "INTERNAL_ERROR"}},
        )


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}
