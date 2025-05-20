from pydantic import BaseModel


class GetUser(BaseModel):  # UserOut
    id: int
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    location: str
    picture: str

class GetAllUsers(BaseModel):
    users: list[GetUser]
    limit: int
    offset: int
    total: int

# class FilterParams(BaseModel):
#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0, ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []


# @app.get("/items/")
# async def read_items(filter_query: Annotated[FilterParams, Query()]):
#     return filter_query

# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
#     q: str | None = None,
#     item: Item | None = None,
# ):