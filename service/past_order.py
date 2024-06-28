from fastapi import Depends

from repository.past_order.past_order import PastOrderRepository
from schemas.past_order import PastOrderCreate


class PastOrderService:
    def __init__(self, past_order_repository: PastOrderRepository = Depends(PastOrderRepository)):
        self.past_order_repository = past_order_repository

    async def create_past_order(self, past_order_data: PastOrderCreate):
        return await self.past_order_repository.create_past_order(past_order_data)
