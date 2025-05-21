from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from random_user_app.settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.DB_DSN)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session