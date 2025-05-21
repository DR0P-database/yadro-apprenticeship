from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from random_user_app.settings import get_settings

settings = get_settings()

# engine = create_engine(url=settings.DB_DSN)
engine = create_async_engine(settings.DB_DSN, echo=False)

# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session

# def get_db():
#     with Session() as session:
#         yield session