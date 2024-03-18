from pydantic import BaseModel


class ProductRead(BaseModel):
    id: int
    category: str
    name: str
    unit: str
    price: float


class ProductCreate(BaseModel):
    category: str
    name: str
    unit: str
    price: float
