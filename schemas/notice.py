from datetime import datetime

from pydantic import BaseModel


class NoticeBase(BaseModel):
    title: str
    content: str


class NoticeCreate(NoticeBase):
    ...


class NoticeRead(NoticeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NoticeUpdate(NoticeBase):
    ...