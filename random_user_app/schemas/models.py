import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class Name(BaseModel):
    title: str
    first: str
    last: str

    model_config = ConfigDict(from_attributes=True)


class Street(BaseModel):
    number: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class Coordinates(BaseModel):
    latitude: str
    longitude: str

    model_config = ConfigDict(from_attributes=True)


class Timezone(BaseModel):
    offset: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class LocationInDB(BaseModel):
    street: Street
    city: str
    state: str
    country: str
    postcode: Union[int, str]
    coordinates: Coordinates
    timezone: Timezone

    model_config = ConfigDict(from_attributes=True)


import uuid


class Login(BaseModel):
    uuid: uuid.UUID
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str

    model_config = ConfigDict(from_attributes=True)


class DOB(BaseModel):
    date: datetime.datetime
    age: int

    model_config = ConfigDict(from_attributes=True)


class Registered(BaseModel):
    date: datetime.datetime
    age: int

    model_config = ConfigDict(from_attributes=True)


class IDInfo(BaseModel):
    name: str
    value: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Picture(BaseModel):
    large: str
    medium: str
    thumbnail: str

    model_config = ConfigDict(from_attributes=True)


class UserInDB(BaseModel):
    id_pk: int = None
    gender: str
    name: Name
    location: LocationInDB
    email: str
    login: Login
    dob: DOB
    registered: Registered
    phone: str
    cell: str
    id: IDInfo
    picture: Picture
    nat: str

    model_config = ConfigDict(from_attributes=True)


class GetUser(BaseModel):
    id_pk: int
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    location: str
    image: str


class GetAllUsers(BaseModel):
    users: list[GetUser]
    limit: int
    offset: int
    total: int
