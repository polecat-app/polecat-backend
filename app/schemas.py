from pydantic import BaseModel, EmailStr, constr


class UserBaseSchema(BaseModel):
    """Base schema for user model."""

    email: EmailStr
    id: int


class CreateUserSchema(UserBaseSchema):
    """Schema for creating user."""

    password: constr(min_length=8)


class LoginUserSchema(BaseModel):
    """Schema for logging in user."""

    email: EmailStr
    password: constr(min_length=8)


class TokenBase(BaseModel):
    """Response schema for token model."""

    access_token: str


class TokenResponse(TokenBase):
    """Response schema for token model."""

    refresh_token: str


class TokenPayload(BaseModel):
    """Payload schema for token model."""

    exp: int
    sub: str


class LikeAnimal(BaseModel):
    """Schema for liking animal."""

    animal_id: int
