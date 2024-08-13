from typing import Optional

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
    client_id: Optional[int]
    client_name: Optional[str]
    client_region: Optional[str]

    class Config:
        from_attributes = True