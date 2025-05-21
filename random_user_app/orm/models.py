import datetime
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    """Base database model."""
    __abstract__ = True
    pass


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)
    street_number: Mapped[int]
    street_name: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    country: Mapped[str]
    postcode: Mapped[str]

    latitude: Mapped[str]
    longitude: Mapped[str]

    timezone_offset: Mapped[str]
    timezone_description: Mapped[str]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    gender:  Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    cell: Mapped[str]
    nat: Mapped[str]

    title: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]

    dob_date: Mapped[datetime.datetime]
    dob_age: Mapped[int]

    reg_date = Mapped[datetime.datetime]
    reg_age: Mapped[int]

    id_name: Mapped[str]
    id_value: Mapped[str]

    login_uuid: Mapped[str]
    login_username: Mapped[str]
    login_password: Mapped[str]
    login_salt: Mapped[str]
    login_md5: Mapped[str]
    login_sha1: Mapped[str]
    login_sha256: Mapped[str]

    picture_large: Mapped[str]
    picture_medium: Mapped[str]
    picture_thumbnail: Mapped[str]

    location_id: Mapped[int]