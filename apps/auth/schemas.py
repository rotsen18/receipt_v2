from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    telegram_id: int


class User(UserBase):
    id: int
    is_active: bool
    telegram_id: int
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
