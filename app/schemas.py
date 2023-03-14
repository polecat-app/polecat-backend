from datetime import datetime
import uuid
from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    """Base schema for user model."""
    email: EmailStr


class CreateUserSchema(UserBaseSchema):
    """Schema for creating user."""
    password: constr(min_length=8)
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(BaseModel):
    """Schema for logging in user."""
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(UserBaseSchema):
    """Response schema for user model."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TokenResponse(BaseModel):
    """Response schema for token model."""
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    """Payload schema for token model."""
    exp: int
    sub: str
