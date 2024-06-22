from typing import List

from pydantic import BaseModel

from schemas.quotation import QuotationRead


class ClientPaginatedResponse(BaseModel):
    items: List[QuotationRead]
    total: int
    page: int
    page_size: int
    total_pages: int


class ClientRead(BaseModel):
    id: int
    name: str
    region: str


class ClientCreate(BaseModel):
    name: str
    region: str


class ClientUpdate(BaseModel):
    name: str
    region: str