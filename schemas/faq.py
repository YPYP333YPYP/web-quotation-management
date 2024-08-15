from pydantic import BaseModel


class FAQBase(BaseModel):
    category: str
    question: str
    answer: str


class FAQCreate(FAQBase):
    ...