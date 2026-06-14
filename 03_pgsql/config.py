from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvConfig(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file= ".env",
        extra= "ignore"
    )
