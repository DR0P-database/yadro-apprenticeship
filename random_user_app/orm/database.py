from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from random_user_app.settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.DB_DSN, echo=False)

Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session
