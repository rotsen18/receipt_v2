from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from database import Base


class IDPrimaryKeyABC(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class NameABC(Base):
    __abstract__ = True

    name = Column(String)


class DateTimeABC(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class IsActiveABC(Base):
    __abstract__ = True

    is_active = Column(Boolean, default=True)
