from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel

from models import Quotation


class QuotationCreate(BaseModel):
    client_id: int
    created_at: date


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


class QuotationInfo(BaseModel):
    products: List[QuotationProductRead]
    name: str
    total: float
    created_at: datetime
    updated_at: Optional[datetime]


class QuotationRead(BaseModel):
    id: int
    name: str
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime]


def to_quotation_read(quotation: Quotation)->QuotationRead:
    return QuotationRead(
        id=quotation.id,
        name=quotation.name,
        total_price=quotation.total_price,
        created_at=quotation.created_at,
        updated_at=quotation.updated_at
    )