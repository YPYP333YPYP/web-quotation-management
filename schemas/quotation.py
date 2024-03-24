from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class QuotationCreate(BaseModel):
    client_id: int


class QuotationAdd(BaseModel):
    quotation_id: int
    product_id: int
    quantity: int


class QuotationUpdate(BaseModel):
    quantity: int


class QuotationProductRead(BaseModel):
    product: str
    quantity: int
    price: int
    created_at: datetime
    updated_at: Optional[datetime]


class QuotationRead(BaseModel):
    products: List[QuotationProductRead]
    name: str
    total: float
    created_at: datetime
    updated_at: Optional[datetime]
