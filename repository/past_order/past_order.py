from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from core.utils import list_to_string
from models.past_order import PastOrder
from schemas.past_order import PastOrderCreate


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

    # todo 1
    async def get_by_id(self):
        ...

    # todo 2
    async def get_by_client_id(self):
        ...