from enum import Enum

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserWithClient(UserInDB):
    client_id: int
    client_name: str
    client_region: str

    class Config:
        from_attributes = True