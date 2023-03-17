from fastapi import HTTPException, Depends, APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import models, schemas
from app.config import settings
from app.database import get_db
from app.deps import get_current_user_from_refresh_token
from app.models import User
from app.schemas import TokenBase
from app.utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)

# Router and crypt context
router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


# Helpers
def authenticate_user(email: str, password: str, database):
    """Authenticate user."""
    user = database.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Routes
@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserBaseSchema,
)
async def create_user(
    payload: schemas.CreateUserSchema, database: Session = Depends(get_db)
):
    """Sign up new user."""

    # Check if user doesn't exist else raise conflict error
    user = (
        database.query(models.User)
        .filter(models.User.email == EmailStr(payload.email.lower()))
        .first()
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )

    # Define payload
    user_kwargs = {
        "hashed_password": hash_password(payload.password),
        "verified": True,
        "email": EmailStr(payload.email.lower()),
    }
    new_user = models.User(**user_kwargs)

    # Add user to database and return
    database.add(new_user)
    database.commit()
    return {"email": payload.email}


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=schemas.TokenResponse
)
async def login(payload: schemas.LoginUserSchema, database: Session = Depends(get_db)):
    """Login user and return access and refresh tokens."""

    # Check if the user exist
    user = (
        database.query(models.User)
        .filter(models.User.email == EmailStr(payload.email.lower()))
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )

    # Check if user verified his email
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please verify your email address",
        )

    # Check if the password is valid
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or Password",
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@router.get("/refresh", summary="Refresh token", response_model=TokenBase)
async def refresh_token(user: User = Depends(get_current_user_from_refresh_token)):
    """Refresh access token."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user belonging to this token no logger exist",
        )
    return {"access_token": create_access_token(user.email)}
