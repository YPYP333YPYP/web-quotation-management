from datetime import datetime
from typing import Optional, List, Any, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from core.utils import list_to_string
from models.past_order import PastOrder
from schemas.past_order import PastOrderCreate
from sqlalchemy.future import select


class PastOrderRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def create_past_order(self, past_order_data: PastOrderCreate) -> PastOrder:
        async with self.session as session:
            past_order = PastOrder(
                client_id=past_order_data.client_id,
                name=past_order_data.name,
                product_ids=list_to_string(past_order_data.product_ids),
                updated_at=datetime.utcnow()
            )
            session.add(past_order)
            await session.commit()
            await session.refresh(past_order)
            return past_order

    @handle_db_exceptions()
    async def get_by_id(self, past_order_id: int) -> Optional[PastOrder]:
        async with self.session as session:
            return await session.get(PastOrder, past_order_id)

    @handle_db_exceptions()
    async def get_by_client_id(self, client_id: int) -> Sequence[PastOrder]:
        async with self.session as session:
            query = (select(PastOrder).filter(PastOrder.client_id == client_id))
            result = await session.execute(query)
            past_orders = result.scalars().all()
            return past_orders

    @handle_db_exceptions()
    async def update_past_order(self, past_order_id: int, update_past_order: dict):
        async with self.session as session:
            past_order = await session.get(PastOrder, past_order_id)
            past_order.name = update_past_order["name"]
            past_order.product_ids = update_past_order["product_ids"]
            await session.commit()
