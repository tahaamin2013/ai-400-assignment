from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment"""
    database_url: str
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()

