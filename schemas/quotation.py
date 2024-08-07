from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel

from models.quotation import Quotation


class QuotationStatus(str, Enum):
    CREATED = "CREATED"
    UPDATED = "UPDATED"
    COMPLETED = "COMPLETED"


class QuotationCreate(BaseModel):
    client_id: int
    created_at: date
    status: QuotationStatus = QuotationStatus.CREATED


class QuotationAdd(BaseModel):
    quotation_id: int
    product_id: int
    quantity: int


class QuotationProductUpdate(BaseModel):
    quantity: int


class QuotationProductRead(BaseModel):
    id: int
    category: str
    product: str
    unit: str
    quantity: int
    price: int
    created_at: datetime
    updated_at: Optional[datetime]


class QuotationInfo(BaseModel):
    products: List[QuotationProductRead]
    name: str
    total: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime]


class QuotationRead(BaseModel):
    id: int
    name: str
    total_price: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime]


class ProductInput(BaseModel):
    id: int
    price: int
    quantity: int


class QuotationUpdate(BaseModel):
    client_id: int
    name: str
    total_price: int
    status: str
    particulars: Optional[str] = None
    products: List[ProductInput]


def to_quotation_read(quotation: Quotation) -> QuotationRead:
    return QuotationRead(
        id=quotation.id,
        name=quotation.name,
        total_price=quotation.total_price,
        status=quotation.status,
        created_at=quotation.created_at,
        updated_at=quotation.updated_at
    )


