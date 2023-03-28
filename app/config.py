import os

from dotenv import load_dotenv


load_dotenv()


def cast_env_var(var_name: str, cast_type: type):
    """Cast environment variable to given type."""
    var = os.getenv(var_name)
    return cast_type(var) if var else None


class Settings:
    """Base settings containing environment variables."""

    PORT = cast_env_var("PORT", int)
    HOST = cast_env_var("HOST", str)
    DATABASE_PORT = cast_env_var("DATABASE_PORT", str)
    DB_PASS = cast_env_var("DB_PASS", str)
    DB_USER = cast_env_var("DB_USER", str)
    DB_NAME = cast_env_var("DB_NAME", str)
    POSTGRES_HOST = cast_env_var("POSTGRES_HOST", str)
    INSTANCE_CONNECTION_NAME = cast_env_var("INSTANCE_CONNECTION_NAME", str)

    JWT_SECRET_KEY = cast_env_var("JWT_SECRET_KEY", str)
    JWT_SECRET_REFRESH_KEY = cast_env_var("JWT_SECRET_REFRESH_KEY", str)
    REFRESH_TOKEN_EXPIRES_IN = cast_env_var("REFRESH_TOKEN_EXPIRES_IN", int)
    ACCESS_TOKEN_EXPIRES_IN = cast_env_var("ACCESS_TOKEN_EXPIRES_IN", int)
    JWT_ALGORITHM = cast_env_var("JWT_ALGORITHM", str)


settings = Settings()
