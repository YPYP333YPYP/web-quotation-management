from datetime import datetime
from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from core.utils import list_to_string, string_to_list
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
                updated_at=datetime.now()
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
    async def get_by_name(self, past_order_name: str) -> Optional[PastOrder]:
        async with self.session as session:
            stmt = select(PastOrder).filter(PastOrder.name == past_order_name)
            result = await session.execute(stmt)
            past_order = result.scalar_one_or_none()
            return past_order

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

    @handle_db_exceptions()
    async def delete_past_order(self, past_order_id: int):
        async with self.session as session:
            past_order = await session.get(PastOrder, past_order_id)
            await session.delete(past_order)
            await session.commit()

    @handle_db_exceptions()
    async def update_past_order_product(self, past_order_id: int, product_id: int):
        async with self.session as session:
            past_order = await session.get(PastOrder, past_order_id)
            product_list = string_to_list(past_order.product_ids)
            product_list.append(product_id)
            past_order.product_ids = list_to_string(product_list)
            await session.commit()
            await session.refresh(past_order)

    @handle_db_exceptions()
    async def delete_path_order_product(self, past_order_id: int, product_id: int):
        async with self.session as session:
            past_order = await session.get(PastOrder, past_order_id)
            product_list = string_to_list(past_order.product_ids)
            product_list.remove(product_id)
            past_order.product_ids = list_to_string(product_list)
            await session.commit()
            await session.refresh(past_order)