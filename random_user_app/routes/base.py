from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from random_user_app.orm.database import Session, engine
from random_user_app.orm.models import Base
from random_user_app.routes.homepage import homepage
from random_user_app.utils.manage_users import get_new_users


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:  # 1. Очистка и создание таблиц
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as session:  # 2. Получеаем данные и сохраняем пользователей в БД
        await get_new_users(count=1000, session=session)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(homepage)

app.mount("/static", StaticFiles(directory="random_user_app/static"), name="static")


from fastapi.responses import RedirectResponse


@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/homepage")
