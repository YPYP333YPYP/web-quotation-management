from typing import List

from pydantic import BaseModel


class PastOrderCreate(BaseModel):
    client_id: int
    name: str
    product_ids: List[int]
