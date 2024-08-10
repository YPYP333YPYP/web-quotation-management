from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from models import Client
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
    region: Optional[str]
    address: str


class ClientCreate(BaseModel):
    name: str
    address: str


class ClientUpdate(BaseModel):
    name: str
    address: str


class DateRangeType(str, Enum):
    WEEK = "week"
    MONTH = "month"
    CUSTOM = "custom"


class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime


class ClientCheckPreview(BaseModel):
    client_id: int
    status: bool


class RegionType(str, Enum):
    노원 = "노원"
    의정부 = "의정부"
    강남 = "강남"
    건대 = "건대"
    신촌= "신촌"


def to_client_read(client: Client) -> ClientRead:
    return ClientRead(
        id=client.id,
        name=client.name,
        region=client.region,
        address=client.address
    )


def to_client_check_preview(client: Client, status: bool) -> ClientCheckPreview:
    return ClientCheckPreview(
        client_id=client.id,
        status=status
    )
