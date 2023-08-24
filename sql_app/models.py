import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String

from sql_app.database import Base


class UserTypeEnum(enum.Enum):
    CLIENT = 1
    ADMIN = 2
    MODERATOR = 3


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.CLIENT)
