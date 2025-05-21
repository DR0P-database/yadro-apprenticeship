from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from random_user_app.schemas.models import UserInDB
from random_user_app.settings import get_settings
from random_user_app.orm.models import DOB, Coordinates, IDInfo, Login, Name, Picture, Registered, Street, Timezone
from random_user_app.orm.models import Users, Location

settings = get_settings()

async def fetch_users(count: int = 1) -> list[UserInDB]:
    if count < 1: 
        raise ValueError("Count must be at least 1")
    
    # Загрузка данных
    async with httpx.AsyncClient() as client:
        resp = await client.get(settings.API_URL, params={"results": count})
        
    if resp.status_code != 200:
        raise Exception(f"Error fetching data: {resp.status_code}")

    print(resp.json())
    data = [UserInDB.model_validate(user) for user in resp.json()["results"]]  # Парсим каждый словарь из списка в модель UserInDB

    return data


async def save_users_to_db(users: list[UserInDB], db: AsyncSession):
    skipped_users = saved_users = 0
    for user in users:
        # Проверяем, есть ли такой login
        existing_login = await db.get(Login, user.login.uuid)
        if not existing_login:
            login = Login(**user.login.model_dump())
            db.add(login)
            await db.flush()
        else:
            skipped_users += 1
            continue

        street = Street(**user.location.street.model_dump())
        db.add(street)
        await db.flush()

        coords = Coordinates(**user.location.coordinates.model_dump())
        db.add(coords)
        await db.flush()

        tz = Timezone(**user.location.timezone.model_dump())
        db.add(tz)
        await db.flush()

        location = Location(
            **user.location.model_dump(exclude={"street", "coordinates", "timezone", "postcode"}),
            postcode=str(user.location.postcode),
            street_id=street.id,
            coordinates_id=coords.id,
            timezone_id=tz.id,
        )
        db.add(location)
        await db.flush()

        name = Name(**user.name.model_dump())
        db.add(name)
        await db.flush()

        dob = DOB(**user.dob.model_dump())
        db.add(dob)
        await db.flush()

        registered = Registered(**user.registered.model_dump())
        db.add(registered)
        await db.flush()

        id_info = IDInfo(**user.id.model_dump())
        db.add(id_info)
        await db.flush()

        picture = Picture(**user.picture.model_dump())
        db.add(picture)
        await db.flush()

        db_user = Users(
            **user.model_dump(exclude={"location", "name", "login", "dob", "registered", "id", "picture"}),
            name_id=name.id,
            login_uuid=login.uuid,
            dob_id=dob.id,
            registered_id=registered.id,
            id_info_id=id_info.id,
            picture_id=picture.id,
            location_id=location.id
        )
        db.add(db_user)
        saved_users += 1
    await db.commit()
    return saved_users, skipped_users