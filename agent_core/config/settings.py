# agent_core/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    openai_api_key: str
    log_level: str = "INFO"
    model_name: str = "gpt-4.1-mini"

    class Config:
        extra = "ignore"


settings = Settings()
