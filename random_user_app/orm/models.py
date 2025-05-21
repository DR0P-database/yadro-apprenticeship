class Base(DeclarativeBase):
    __abstract__ = True
    pass

class User(Base):
    __tablename__ = "user"
    