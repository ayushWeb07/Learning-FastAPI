from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class EnvConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_CONNECTION_URI: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        extra= "ignore"
    )

env_config= EnvConfig()