"""Authentication and JWT token handling."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import settings
from .logger import logger

import uuid

security = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Payload to encode
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """
    Verify JWT token from HTTP Authorization header.
    Returns a guest user ID if no token is provided.

    Args:
        credentials: HTTP Bearer credentials (optional)

    Returns:
        User ID from token or guest ID
    """
    # If no credentials provided, return guest user ID
    if credentials is None:
        guest_id = f"guest_{uuid.uuid4().hex[:8]}"
        logger.info(f"Guest user access: {guest_id}")
        return guest_id

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        logger.info(f"Token verified for user {user_id}")
        return user_id
    except JWTError as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_token(user_id: str) -> str:
    """
    Generate a token for a user.

    Args:
        user_id: User identifier

    Returns:
        JWT token for the user
    """
    return create_access_token(data={"sub": user_id})


def get_guest_token() -> str:
    """
    Generate a guest token for anonymous users.

    Returns:
        JWT token for guest user
    """
    guest_id = f"guest_{uuid.uuid4().hex[:8]}"
    return create_access_token(data={"sub": guest_id}), guest_id
