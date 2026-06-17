from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    port: int = Field(default=8080, validation_alias="SCORE_SERVICE_PORT")
    log_level: str = Field(default="INFO", validation_alias="SCORE_LOG_LEVEL")


config = Config()
