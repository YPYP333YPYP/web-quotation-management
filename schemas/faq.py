from datetime import datetime

from pydantic import BaseModel


class FAQBase(BaseModel):
    category: str
    question: str
    answer: str


class FAQCreate(FAQBase):
    ...


class FAQUpdate(FAQBase):
    ...


class FAQRead(FAQBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True