from datetime import datetime

from pydantic import root_validator
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """Database model for users."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    user_likes = relationship("UserLike", cascade="all,delete", backref="users")
    user_seen = relationship("UserSee", cascade="all,delete", backref="users")

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(self, values):
        """Set update at value."""
        values["updated_at"] = datetime.now()
        return values


class Animal(Base):
    """Database model for animals."""
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    binomial = Column(String, unique=True, index=True)
    commonName = Column(String, unique=False)
    summary = Column(String, unique=False)
    image_url = Column(String, unique=False)
    rangeImage_url = Column(String, unique=False)
    animal_tags = relationship("AnimalTag", cascade="all,delete", backref="animals")
    user_likes = relationship("UserLike", cascade="all,delete", backref="animals")
    user_seen = relationship("UserSee", cascade="all,delete", backref="animals")


class UserLike(Base):
    """Database model for likes."""
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    animal_id = Column(Integer, ForeignKey("animals.id"))


class UserSee(Base):
    """Database model for sees."""
    __tablename__ = "seen"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    animal_id = Column(Integer, ForeignKey("animals.id"))


class AnimalTag(Base):
    """Database model for animal - tag relationship."""
    __tablename__ = "animal_tags"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))


class Tag(Base):
    """Database model for tags."""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    animal_tags = relationship("AnimalTag", cascade="all,delete", backref="tags")
