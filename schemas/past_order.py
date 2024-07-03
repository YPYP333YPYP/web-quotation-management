from datetime import datetime
from typing import List

from pydantic import BaseModel

from models.past_order import PastOrder
from schemas.product import ProductRead


class PastOrderCreate(BaseModel):
    client_id: int
    name: str
    product_ids: List[int]


class PastOrderRead(BaseModel):
    past_order_id: int
    name: str
    product_list: List[ProductRead]
    created_at: datetime


class PastOrderInfo(BaseModel):
    past_order_id: int
    name: str


def to_past_order_read(past_order: PastOrder, product_list: List[ProductRead]) -> PastOrderRead:
    return PastOrderRead(
        past_order_id=past_order.id,
        name=past_order.name,
        product_list=product_list,
        created_at=past_order.created_at
    )


def to_past_order_info(past_order:PastOrder) -> PastOrderInfo:
    return PastOrderInfo(
        past_order_id=past_order.id,
        name=past_order.name
    )