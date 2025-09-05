import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.constants import ENV_FILE_PATH


class BaseConfig(BaseSettings):
    env: str = "development"
    app_host: str = "0.0.0.0"
    port: int = pydantic.Field(default=8000, env="PORT")
    workers: int = 1
    reload: bool = True

    # CORS settings
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
    )
