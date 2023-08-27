import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String

from sql_app.database import Base


class UserTypeEnum(enum.Enum):
    CLIENT = 1
    ADMIN = 2
    MODERATOR = 3


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.CLIENT)
    has_api_access = Column(Boolean, default=False)
    telegram_id = Column(Integer, nullable=True, default=None)
    first_name = Column(String(35), default='')
    last_name = Column(String(35), nullable=True, default='')
    full_name = Column(String(35), nullable=True, default='')
    name = Column(String(35), nullable=True, default='')
