from typing import Annotated
from fastapi import FastAPI, Path


from fastapi import  Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from random_user_app.orm.database import Session

from random_user_app.orm.database import get_session, engine
from random_user_app.orm.models import Location, Users, Base
from random_user_app.schemas.models import GetAllUsers, GetUser, UserInDB
##################################################################

from contextlib import asynccontextmanager
import httpx
from random_user_app.utils.users import fetch_users, save_users_to_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Очистка и создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # 2. Получение данных
    users = await fetch_users(1000)

    # # 3. Сохраняем пользователей в БД
    async with Session() as session:

        await save_users_to_db(users, session)

    yield  # старт приложения

##################################################################

app = FastAPI(lifespan=lifespan)

@app.get("/", response_model=GetAllUsers)
async def get_users(limit: int = 10, offset: int = 0, db: AsyncSession = Depends(get_session)):
    # Получаем пользователей с пагинацией
    result = await db.execute(
        select(Users).offset(offset).limit(limit)
    )
    users = result.scalars().all()

    print(users)

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
async def get_users(count: Annotated[int, Path(title="The count of the users to get", ge=1)],
                    db: AsyncSession = Depends(get_session)):
    users: list[UserInDB] = await fetch_users(count)
    saved_users, skipped_users = await save_users_to_db(users, db)
    return {"message": f"{len(users)} are fetched.\n{saved_users} users are saved successfully.\n{skipped_users} users skipped(already exist in DB)"}