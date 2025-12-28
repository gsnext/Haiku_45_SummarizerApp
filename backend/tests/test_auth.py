"""Unit tests for authentication and JWT tokens."""
import pytest
from datetime import timedelta
from jose import jwt
from fastapi.testclient import TestClient

from backend.app.auth import create_access_token, verify_token
from backend.app.config import settings


class TestAuthentication:
    """Tests for authentication functionality."""

    def test_create_access_token(self):
        """Test JWT token creation."""
        user_id = "test_user"
        token = create_access_token(data={"sub": user_id})
        assert token is not None
        assert isinstance(token, str)

        # Decode and verify
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        assert payload["sub"] == user_id

    def test_create_access_token_with_expiration(self):
        """Test JWT token creation with custom expiration."""
        user_id = "test_user"
        expires_delta = timedelta(hours=1)
        token = create_access_token(data={"sub": user_id}, expires_delta=expires_delta)

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        assert payload["sub"] == user_id
        assert "exp" in payload

    def test_invalid_token(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.token.here"
        with pytest.raises(Exception):
            jwt.decode(
                invalid_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

    def test_token_contains_user_id(self):
        """Test that token contains the correct user ID."""
        user_id = "specific_user_123"
        token = create_access_token(data={"sub": user_id})

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        assert payload["sub"] == user_id
