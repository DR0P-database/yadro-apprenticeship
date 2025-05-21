from typing import Annotated
from fastapi import FastAPI, Path


from fastapi import  Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from random_user_app.orm.database import Session

from random_user_app.orm.database import get_session, engine
from random_user_app.orm.models import Location, Users, Base
from random_user_app.schemas.models import GetAllUsers, GetUser, UserInDB
##################################################################

from contextlib import asynccontextmanager
import httpx
from random_user_app.utils.users import fetch_users, get_new_users, save_users_to_db
from fastapi.responses import StreamingResponse
import time
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Очистка и создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 2. Получение данные и Сохраняем пользователей в БД
    async with Session() as session:
        await get_new_users(count=1000, session=session)

    yield  # старт приложения

##################################################################

app = FastAPI(lifespan=lifespan)

@app.get("/", response_model=GetAllUsers)
async def get_users(limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_session)):
    # Получаем пользователей с пагинацией
    result = await db.execute(
        select(Users).options(
        selectinload(Users.name),
        selectinload(Users.location).selectinload(Location.street))
        .offset(offset).limit(limit)
    )
    users = result.scalars().all()

    if not users:
        return GetAllUsers.model_validate({
            "users": [],
            "limit": limit,
            "offset": offset,
            "total": 0
        })


    # # Получаем все location_id одним запросом
    # location_ids = [user.location_id for user in users if user.location_id is not None]

    # Location_dict = {}
    # if location_ids:
    #     location_result = await db.execute(
    #         select(Location).where(Location.id.in_(location_ids))
    #     )
    #     Location = location_result.scalars().all()
    #     Location_dict = {loc.id: loc for loc in Location}

    # # Формируем ответ
    result_data = []
    
    for user in users:
        # location = Location_dict.get(user.location_id)
        # if not location: continue  # Пропускаем, если location_id не найден
        user_data = {
            "first_name": user.name.first,
            "last_name": user.name.last,
            "location": f"{user.location.street.name}, {user.location.street.number}",
        }
        result_data.append(GetUser.model_validate(user_data))

    response = {
        "users": result_data,
        "limit": limit,
        "offset": offset,
        "total": len(result_data),
    }

    return GetAllUsers.model_validate(response)

@app.get("/test/{count}")
async def get_users(
    count: Annotated[int, Path(title="The count of the users to get", ge=1)],
    session: AsyncSession = Depends(get_session)
):
    async def event_stream():
        yield "Processing started...\n"
        await asyncio.sleep(0.1)
        saved_users, skipped_users = await get_new_users(count=count, session=session)
        yield f"{saved_users} users are saved successfully.\n"
        yield f"{skipped_users} users skipped (already exist in DB).\n"
        yield "Processing finished.\n"

    return StreamingResponse(event_stream(), media_type="text/plain")