from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    full_name: Optional[str] = None
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserList(UserBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class UserDetail(UserList):
    full_name: str
    name: str
    first_name: str
    last_name: str
    is_active: str
