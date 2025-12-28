"""Unit tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from backend.app.main import app
from backend.app.auth import create_access_token


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def test_token():
    """Create a test authentication token."""
    return create_access_token(data={"sub": "test_user"})


class TestAPIEndpoints:
    """Tests for REST API endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_summarize_empty_text(self, client, test_token):
        """Test summarization with empty text."""
        response = client.post(
            "/api/summarize",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"text": "", "summary_length": "medium"},
        )
        assert response.status_code == 400

    def test_summarize_with_missing_token(self, client):
        """Test summarization without authentication token."""
        response = client.post(
            "/api/summarize",
            json={"text": "Some text", "summary_length": "medium"},
        )
        assert response.status_code == 403

    def test_batch_too_many_items(self, client, test_token):
        """Test batch processing with more than 10 items."""
        items = [{"text": f"Item {i}"} for i in range(15)]
        response = client.post(
            "/api/batch",
            headers={"Authorization": f"Bearer {test_token}"},
            json={"items": items, "summary_length": "medium"},
        )
        assert response.status_code == 400

    def test_get_history_empty(self, client, test_token):
        """Test retrieving empty history."""
        response = client.get(
            "/api/history",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert len(data["summaries"]) == 0

    def test_get_nonexistent_summary(self, client, test_token):
        """Test retrieving a non-existent summary."""
        response = client.get(
            "/api/summary/nonexistent_id",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 404

    def test_delete_nonexistent_summary(self, client, test_token):
        """Test deleting a non-existent summary."""
        response = client.delete(
            "/api/summary/nonexistent_id",
            headers={"Authorization": f"Bearer {test_token}"},
        )
        assert response.status_code == 404

    def test_unauthorized_delete(self, client):
        """Test deleting summary without authentication."""
        response = client.delete("/api/summary/some_id")
        assert response.status_code == 403
