from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NoticeBase(BaseModel):
    title: str
    content: str


class NoticeCreate(NoticeBase):
    ...


class NoticeRead(NoticeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class NoticeUpdate(NoticeBase):
    ...