from fastapi import FastAPI

from random_user_app.schemas.models import GetAllUsers

app = FastAPI()

# app.include_router(user)
@app.get("/", response_model=GetAllUsers)
async def index(limit: int = 5, offset: int = 0) -> GetAllUsers:
    return GetAllUsers(users=[], total=0, offset=0, limit=0)