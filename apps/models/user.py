import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from apps.models import mixins


class UserTypeEnum(enum.Enum):
    CLIENT = 1
    ADMIN = 2
    MODERATOR = 3


class User(mixins.IDPrimaryKeyABC):
    __tablename__ = 'user'

    telegram_id = Column(Integer, nullable=True, default=None, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(Enum(UserTypeEnum), default=UserTypeEnum.CLIENT)
    has_api_access = Column(Boolean, default=False)
    first_name = Column(String(35), default='')
    last_name = Column(String(35), nullable=True, default='')
    full_name = Column(String(35), nullable=True, default='')
    name = Column(String(35), nullable=True, default='')

    receipts = relationship('Receipt', back_populates='author')
