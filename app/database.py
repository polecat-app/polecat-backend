from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

from .config import settings


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.
    Uses the Cloud SQL Python Connector package.
    """
    # initialize Cloud SQL Python Connector object
    connector = Connector()

    def getconn():
        """Get connector to cloud SQL."""
        conn = connector.connect(
            settings.INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=settings.DB_USER,
            password=settings.DB_PASS,
            db=settings.DB_NAME,
            ip_type=IPTypes.PUBLIC,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # # Pool size is the maximum number of permanent connections to keep.
        # pool_size=5,
        #
        # # Temporarily exceeds the set pool_size if no connections are available.
        # max_overflow=2,
        #
        # # The total number of concurrent connections for your application will be
        # # a total of pool_size and max_overflow.
        #
        # # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # # new connection from the pool. After the specified amount of time, an
        # # exception will be thrown.
        # pool_timeout=30,  # 30 seconds
        #
        # # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # # Connections that live longer than the specified amount of time will be
        # # re-established
        # pool_recycle=1800,  # 30 minutes
    )
    return pool


# An Engine, which the Session will use for connection resources,
# specifying location and type of database
if settings.HOST:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@"
        f"{settings.INSTANCE_CONNECTION_NAME}/{settings.DB_NAME}"
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    engine = connect_with_connector()

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
