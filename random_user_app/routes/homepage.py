from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from random_user_app.orm.database import get_session
from random_user_app.orm.models import Location, Users
from random_user_app.schemas.models import UserInDB
from random_user_app.utils.manage_users import (
    fetch_users,
    get_users_from_db,
    save_user_to_db,
)
from random_user_app.utils.parsing import parse_message

from . import templates

homepage = APIRouter(prefix="/homepage")


@homepage.get("/")
async def get_users(
    request: Request,
    limit: int = 25,
    offset: int = 0,
    msg="",
    session: AsyncSession = Depends(get_session),
):
    if limit < 1:
        raise ValueError("Limit must be greater than 0")
    respones = await get_users_from_db(session=session, limit=limit, offset=offset)
    data = respones.model_dump()

    data["offset"] = data["offset"] // limit * limit

    if not data["users"]:
        msg = "Нет данных о пользователях"

    if msg:
        msg = parse_message(msg)

    return templates.TemplateResponse(
        name="homepage/homepage.html",
        context={"request": request, "data": data, "title": "Homepage", "msg": msg},
    )


from fastapi import Form
from fastapi.responses import RedirectResponse

from random_user_app.utils.manage_users import get_new_users


@homepage.post("/fetch")
async def fetch_users_post(
    count: int = Form(default=1, ge=1),
    current_total: int = Form(default=0),
    session: AsyncSession = Depends(get_session),
):
    # Загружаем новых пользователей и сохраняем в БД
    try:
        saved_users, skipped_users = await get_new_users(session=session, count=count)
        msg = (
            f"Добавлено: {saved_users} шт., пропущено: {skipped_users} шт.\nstatus: ok"
        )
    except Exception as e:
        msg = f"Какая-то ошибка\nstatus: error"

    return RedirectResponse(
        url=f"/homepage?offset={current_total}&msg={msg}", status_code=303
    )


@homepage.get("/random")
async def get_random_user(
    request: Request, session: AsyncSession = Depends(get_session)
):
    response = await fetch_users(count=1)
    user = response["results"][0]

    user, status = await save_user_to_db(UserInDB.model_validate(user), db=session)

    return templates.TemplateResponse(
        name="userpage/userpage.html", context={"request": request, "user": user}
    )


@homepage.get("/{user_id}")
async def get_user_by_id(
    user_id: Annotated[int, Path(ge=1)],
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(Users)
        .options(
            selectinload(Users.name),
            selectinload(Users.location).selectinload(Location.street),
            selectinload(Users.location).selectinload(Location.coordinates),
            selectinload(Users.location).selectinload(Location.timezone),
            selectinload(Users.picture),
            selectinload(Users.login),
            selectinload(Users.dob),
            selectinload(Users.registered),
            selectinload(Users.id),
            selectinload(Users.picture),
        )
        .where(Users.id_pk == user_id)
    )
    user = result.scalars().first()

    if not user:
        return {"error": "User not found"}

    user_data = UserInDB.model_validate(user)

    return templates.TemplateResponse(
        name="userpage/userpage.html", context={"request": request, "user": user_data}
    )
