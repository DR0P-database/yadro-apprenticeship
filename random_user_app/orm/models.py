import datetime
from typing import Optional
from sqlalchemy import UUID as SA_UUID, DateTime, ForeignKey
from uuid import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    """Base database model."""
    __abstract__ = True
    pass

class Street(Base):
    __tablename__ = "streets"
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int]
    name: Mapped[str]

class Coordinates(Base):
    __tablename__ = "coordinates"
    id: Mapped[int] = mapped_column(primary_key=True)
    latitude: Mapped[str]
    longitude: Mapped[str]

class Timezone(Base):
    __tablename__ = "timezones"
    id: Mapped[int] = mapped_column(primary_key=True)
    offset: Mapped[str]
    description: Mapped[str]

class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    state: Mapped[str]
    country: Mapped[str]
    postcode: Mapped[str]

    street_id: Mapped[int] = mapped_column(ForeignKey("streets.id", ondelete="CASCADE"))
    coordinates_id: Mapped[int] = mapped_column(ForeignKey("coordinates.id", ondelete="CASCADE"))
    timezone_id: Mapped[int] = mapped_column(ForeignKey("timezones.id", ondelete="CASCADE"))

    street: Mapped["Street"] = relationship()
    coordinates: Mapped["Coordinates"] = relationship()
    timezone: Mapped["Timezone"] = relationship()

class Name(Base):
    __tablename__ = "names"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    first: Mapped[str]
    last: Mapped[str]

class Login(Base):
    __tablename__ = "logins"
    uuid: Mapped[UUID] = mapped_column(SA_UUID, primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    salt: Mapped[str]
    md5: Mapped[str]
    sha1: Mapped[str]
    sha256: Mapped[str]

class DOB(Base):
    __tablename__ = "dobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    age: Mapped[int]

class Registered(Base):
    __tablename__ = "registered"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    age: Mapped[int]

class IDInfo(Base):
    __tablename__ = "id_info"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    value: Mapped[Optional[str]] = mapped_column(nullable=True)
    
class Picture(Base):
    __tablename__ = "pictures"
    id: Mapped[int] = mapped_column(primary_key=True)
    large: Mapped[str]
    medium: Mapped[str]
    thumbnail: Mapped[str]

class Users(Base):
    __tablename__ = "users"
    id_pk: Mapped[int] = mapped_column(primary_key=True)
    gender: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    cell: Mapped[str]
    nat: Mapped[str]

    name_id: Mapped[int] = mapped_column(ForeignKey("names.id", ondelete="CASCADE"))
    login_uuid: Mapped[UUID] = mapped_column(ForeignKey("logins.uuid", ondelete="CASCADE"))
    dob_id: Mapped[int] = mapped_column(ForeignKey("dobs.id", ondelete="CASCADE"))
    registered_id: Mapped[int] = mapped_column(ForeignKey("registered.id", ondelete="CASCADE"))
    id_info_id: Mapped[int] = mapped_column(ForeignKey("id_info.id", ondelete="CASCADE"))
    picture_id: Mapped[int] = mapped_column(ForeignKey("pictures.id", ondelete="CASCADE"))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))

    name: Mapped["Name"] = relationship()
    login: Mapped["Login"] = relationship()
    dob: Mapped["DOB"] = relationship()
    registered: Mapped["Registered"] = relationship()
    id: Mapped["IDInfo"] = relationship()
    picture: Mapped["Picture"] = relationship()
    location: Mapped["Location"] = relationship()
