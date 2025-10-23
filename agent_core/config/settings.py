# agent_core/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: str
    log_level: str = "INFO"
    model_name: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-ada-002"

    # API URLs
    springboot_healthcare_facility_url: str = "https://prod.nearcare-app.com/healthcare-facility-ms"
    springboot_healthcare_url: str = "https://prod.nearcare-app.com/healthcare-ms"
    nearcare_oauth_url: str = "https://prod.nearcare-app.com/oauth2-ms/oauth/token"

    # OAuth2 Credentials
    oauth_client_id: str
    oauth_client_secret: str
    oauth_username: str
    oauth_password: str
    oauth_grant_type: str = "password"


settings = Settings()
