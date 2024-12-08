from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_TITLE: str = "FILE MANAGER API"

settings = Settings()