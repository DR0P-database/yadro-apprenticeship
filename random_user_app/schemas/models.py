import datetime
from typing import Optional, Union
from pydantic import BaseModel

class Name(BaseModel):
    title: str
    first: str
    last: str

class Street(BaseModel):
    number: int
    name: str

class Coordinates(BaseModel):
    latitude: str
    longitude: str

class Timezone(BaseModel):
    offset: str
    description: str

class LocationInDB(BaseModel):
    street: Street
    city: str
    state: str
    country: str
    postcode: Union[int, str]
    coordinates: Coordinates
    timezone: Timezone

import uuid
class Login(BaseModel):
    uuid: uuid.UUID
    username: str
    password: str
    salt: str
    md5: str
    sha1: str
    sha256: str

class DOB(BaseModel):
    date: datetime.datetime
    age: int

class Registered(BaseModel):
    date: datetime.datetime
    age: int

class IDInfo(BaseModel):
    name: str
    value: Optional[str] = None
    
class Picture(BaseModel):
    large: str
    medium: str
    thumbnail: str    

class UserInDB(BaseModel):
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


#########################################################
class GetUser(BaseModel):  # UserOut
    first_name: str
    last_name: str
    location: str

class GetAllUsers(BaseModel):
    users: list[GetUser]
    limit: int
    offset: int
    total: int