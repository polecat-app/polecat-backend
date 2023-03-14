import pathlib

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base settings containing environment variables."""
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    JWT_SECRET_KEY: str
    JWT_SECRET_REFRESH_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"


settings = Settings()
