from datetime import datetime

from pydantic import root_validator
from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.database import Base


class User(Base):
    """Database model for users which inherits attributes from Base."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(self, values):
        values["updated_at"] = datetime.now()
        return values
