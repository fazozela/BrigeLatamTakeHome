from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the score service.

    Reads from environment variables (12-factor). Values are inert unless
    the service actually consumes them — see ``score_service.main`` and the
    Dockerfile ``CMD`` for the current consumers.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    port: int = Field(default=8080, validation_alias="SCORE_SERVICE_PORT")
    log_level: str = Field(default="INFO", validation_alias="SCORE_LOG_LEVEL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a process-wide Settings instance, cached after first call.

    Tests can clear the cache (``get_settings.cache_clear()``) and override
    env vars to obtain a fresh instance without monkeypatching modules.
    """

    return Settings()
