from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    telegram_id: Optional[int] = None
    full_name: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    telegram_id: int


class UserDetail(UserBase):
    id: int
    is_active: bool
    telegram_id: Optional[int] = None
    full_name: str
    name: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class UserList(UserBase):
    id: int
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
