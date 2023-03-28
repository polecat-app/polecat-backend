import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Base settings containing environment variables."""

    PORT = int(os.getenv("PORT"))
    HOST = str(os.getenv("HOST"))
    DATABASE_PORT = str(os.getenv("DATABASE_PORT"))
    DB_PASS = str(os.getenv("DB_PASS"))
    DB_USER = str(os.getenv("DB_USER"))
    DB_NAME = str(os.getenv("DB_NAME"))
    POSTGRES_HOST = str(os.getenv("POSTGRES_HOST"))
    INSTANCE_CONNECTION_NAME = str(os.getenv("INSTANCE_CONNECTION_NAME"))

    JWT_SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
    JWT_SECRET_REFRESH_KEY = str(os.getenv("JWT_SECRET_REFRESH_KEY"))
    REFRESH_TOKEN_EXPIRES_IN = int(os.getenv("REFRESH_TOKEN_EXPIRES_IN"))
    ACCESS_TOKEN_EXPIRES_IN = int(os.getenv("ACCESS_TOKEN_EXPIRES_IN"))
    JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM"))


settings = Settings()
