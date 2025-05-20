from random_user_app.settings import get_settings
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

settings = get_settings()
engine = create_async_engine(settings.DB_DSN)

async def get_db_session():
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError as error:
            await session.rollback()
            raise