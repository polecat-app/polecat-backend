from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings


# An Engine, which the Session will use for connection resources,
# specifying location and type of database
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# One central factory method to create a session. When SessionLocal() is called,
# this method creates a session, so it is not necessary to pass engine every time
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base database model through a factory method.
# Classes that inherit from the returned class object will be automatically
# mapped using declarative mapping.
Base = declarative_base()


def get_db():
    """Get database session."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
