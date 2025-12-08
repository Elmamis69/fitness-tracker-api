"""Authentication utilities for JWT token handling"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings
from app.models.user import UserModel
from app.schemas.user import TokenData

# Security scheme para extraer el token del header
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token
    
    Args:
        data: Dictionary with data to encode (usually user_id)
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode JWT token

    Args:
        token: JWT token string
    
    Returns:
        TokenData with user_id or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")

        if user_id is None:
            return None
        
        return TokenData(user_id = user_id)
    
    except JWTError:
        return None
    
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get current authenticated user

    Use in routes like: user = Depdends(get_current_user)

    Returns:
        User document from database

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Extraer el token
    token = credentials.credentials

    # Verificar el token
    token_data = verify_token(token)

    if token_data is None or token_data.user_id is None:
        raise credentials_exception
    
    # Buscar el usuaurio en la base de datos
    user = await UserModel.get_user_by_id(token_data.user_id)

    if user is None:
        raise credentials_exception
    
    return user