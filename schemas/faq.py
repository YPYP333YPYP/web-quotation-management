from datetime import datetime
from typing import Optional

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
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
