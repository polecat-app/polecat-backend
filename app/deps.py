from typing import Union, Any, Dict
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.database import get_db
from app.schemas import TokenPayload, UserBaseSchema


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)) -> UserBaseSchema:
    """Try to get current user from jwt."""

    try:

        # Decode token
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        # Check if token is expired
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={
                    "WWW-Authenticate": "Bearer"},
            )

    except(jwt.JWTError, ValidationError):

        # Raise exception if token is invalid
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"},
        )

    # Try to get user from database
    user = db.query(models.User).filter(models.User.email == token_data.sub).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserBaseSchema(email=user)
