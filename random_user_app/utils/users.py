from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from random_user_app.schemas.models import UserInDB
from random_user_app.settings import get_settings
from random_user_app.orm.models import DOB, Coordinates, IDInfo, Login, Name, Picture, Registered, Street, Timezone
from random_user_app.orm.models import Users, Location
import logging

settings = get_settings()

logging.basicConfig(level=logging.INFO)  # Добавьте эту строку
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def get_new_users(session: AsyncSession, count: int = 1) -> list[UserInDB]:
  if count < 1: 
    logger.error("Count must be at least 1")
    raise ValueError("Count must be at least 1")
  
  total_pages, seed = -1, None
  if count > settings.LIMIT_USERS_PER_PAGE:
    total_pages = (count+settings.LIMIT_USERS_PER_PAGE-1) // settings.LIMIT_USERS_PER_PAGE
    count = settings.LIMIT_USERS_PER_PAGE

  logger.info(f"Fetching {count} users from API")
  response = await fetch_users(count)
  seed = response["info"]["seed"]
  
  parsed_users = [UserInDB.model_validate(user) for user in response["results"]]
  if not parsed_users:
    logger.warning("No users fetched from API")
    return []
  
  logger.info(f"Saving {len(parsed_users)} users to DB")
  saved_users, skipped_users = await save_users_to_db(parsed_users, session)

  while response["info"]["page"] < total_pages:
    logger.info(f"Fetching page {response['info']['page']+1} with seed {seed}")
    response = await fetch_users(count, page=response["info"]["page"]+1, seed=seed)

    parsed_users = [UserInDB.model_validate(user) for user in response["results"]]
    if not parsed_users:
      logger.warning("No users fetched from API on next page")
      break
    
    logger.info(f"Saving {len(parsed_users)} users to DB from page {response['info']['page']}")
    saved_users_per_page, skipped_users_per_page = await save_users_to_db(parsed_users, session)
    saved_users += saved_users_per_page
    skipped_users += skipped_users_per_page
  
  logger.info(f"Finished: {saved_users} users saved, {skipped_users} users skipped")
  return skipped_users, saved_users


async def fetch_users(count: int = 1, page: int = None, seed: str = None) -> dict:
  """
  Функция для получения пользователей из API
  """
  payload = {
      "results": count,
  }
  if page and seed:
      payload["page"] = page
      payload["seed"] = seed

  async with httpx.AsyncClient() as client:
      resp = await client.get(settings.API_URL, params=payload)
      
  if resp.status_code != 200:
      raise Exception(f"Error fetching data: {resp.status_code}")

  return resp.json()



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