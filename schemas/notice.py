from pydantic import BaseModel


class NoticeBase(BaseModel):
    title: str
    content: str


class NoticeCreate(NoticeBase):
    ...
