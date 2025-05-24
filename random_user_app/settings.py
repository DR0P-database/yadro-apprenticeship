from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DSN: str = "postgresql+asyncpg://postgres:postgres@localhost:5433/postgres"
    API_URL: str = "https://randomuser.me/api/"
    LIMIT_USERS_PER_PAGE: int = 100

    model_config = ConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()
