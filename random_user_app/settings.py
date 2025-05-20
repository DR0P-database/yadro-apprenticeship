from functools import lru_cache

from pydantic import ConfigDict, PostgresDsn
from sqlalchemy import create_engine



from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DSN: PostgresDsn = "postgresql://postgres:postgres@localhost:5432/postgres"
    API_URL: str = ''

    model_config = ConfigDict(env_file=".env")


@lru_cache
def get_settings() -> Settings:
    return Settings()


engine = create_engine(echo=True)