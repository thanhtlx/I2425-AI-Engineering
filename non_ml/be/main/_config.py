import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ENVIRONMENT: str
    LOGGING_LEVEL: int = logging.INFO

    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_ENGINE_OPTIONS: dict = {}
    SQLALCHEMY_ECHO: bool = False

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
    )
    SECRET_KEY: str
    ALGORITHM: str
    ML_MODEL_PATH: str = ""
    SENTRY_DSN: str = ""
    SENTRY_SAMPLE_RATE: float = 1.0
    GCS_BUCKET_NAME: str = ""
    TRIGGER_BUILD_URL: str = ""
    TRIGGER_BUILD_TOKEN: str = ""
    TRIGGER_BUILD_BRANCH: str = ""
    TRIGGER_BUILD_ACCEPT: str = ""
    GOOGLE_APPLICATION_CREDENTIALS: str = ""


environment = os.environ.get("ENVIRONMENT", "local")
config = Config(
    ENVIRONMENT=environment,
    # ".env.{environment}" takes priority over ".env"
    _env_file=[".env", f".env.{environment}"],
)
