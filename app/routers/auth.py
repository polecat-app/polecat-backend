from datetime import timedelta

from fastapi import HTTPException, Depends, Request, APIRouter
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from app import models, schemas
from app.config import settings
from app.database import get_db
from app.utils import hash_password, verify_password, create_access_token, \
    create_refresh_token


# Router and crypt context


router = APIRouter(
    prefix='/auth', tags=['auth'], responses={401: {'user': 'Not authorized'}}
)

ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


# Helpers


def authenticate_user(email: str, password: str, db):
    """Authenticate user."""
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# Routes


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(payload: schemas.CreateUserSchema, db: Session = Depends(get_db)):
    """Sign up new user."""

    # Check if user doesn't exist else raise conflict error
    user = db.query(models.User).filter(
        models.User.email == EmailStr(payload.email.lower())
    ).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Account already exists'
        )

    # Define payload
    payload.password = hash_password(payload.password)
    payload.verified = True
    payload.email = EmailStr(payload.email.lower())
    new_user = models.User(**payload.dict())

    # Add user to database and return
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login', status_code=status.HTTP_200_OK, response_model=schemas.TokenResponse)
async def login(payload: schemas.LoginUserSchema, db: Session = Depends(get_db)):
    """Login user."""

    # Check if the user exist
    user = db.query(models.User).filter(
        models.User.email == EmailStr(payload.email.lower())).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    # Check if user verified his email
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Please verify your email address')

    # Check if the password is valid
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }

# @router.get('/refresh')
# def refresh_token(response: Response, request: Request, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """Refresh access token."""
#     try:
#         Authorize.jwt_refresh_token_required()
#
#         user_id = Authorize.get_jwt_subject()
#         if not user_id:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail='Could not refresh access token')
#         user = db.query(models.User).filter(models.User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail='The user belonging to this token no logger exist')
#         access_token = Authorize.create_access_token(
#             subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
#     except Exception as e:
#         error = e.__class__.__name__
#         if error == 'MissingTokenError':
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=error)
#
#     response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#     response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
#     return {'access_token': access_token}
