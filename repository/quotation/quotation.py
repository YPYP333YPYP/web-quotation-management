from datetime import date
from typing import List, Sequence

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.database import async_get_db
from models import Quotation
from models.quotation_product import QuotationProduct


class QuotationRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def create_quotation(self, quotation: Quotation):
        self.session.add(quotation)

    async def get_quotation_by_id(self, quotation_id: int):
        async with self.session as session:
            product = await session.get(Quotation, quotation_id)
            return product if product else None

    async def update_total_price(self, quotation_id: int) -> None:
        async with self.session as session:
            query = select(func.sum(QuotationProduct.price)). \
                where(QuotationProduct.quotation_id == quotation_id)
            result = await session.execute(query)
            total_price = result.scalar()

            query = select(Quotation).filter(Quotation.id == quotation_id)
            result = await session.execute(query)
            quotation = result.scalar_one_or_none()

            if quotation and total_price is not None:
                quotation.total_price = total_price
                await session.commit()
            return total_price

    async def search_quotation(self, start: date, end: date, query: str) -> Sequence[Quotation]:
        async with self.session as session:
            stmt = select(Quotation)

            if start:
                stmt = stmt.filter(Quotation.created_at >= start)
            if end:
                stmt = stmt.filter(Quotation.created_at <= end)
            if query:
                stmt = stmt.filter(Quotation.name.contains(query))

            tmp_result = await session.execute(stmt)
            result = tmp_result.scalars().all()

            return result
