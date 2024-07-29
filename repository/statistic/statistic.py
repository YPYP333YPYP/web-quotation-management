from fastapi import Depends
from sqlalchemy import func, select

from datetime import datetime
from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models import Quotation, Client, Product
from models.quotation_product import QuotationProduct


class StatisticsRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def get_client_statistics(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        async with self.session as session:
            async with session.begin():
                result = await session.execute(
                    select(
                        Client.id,
                        Client.name,
                        func.count(Quotation.id).label('total_quotations'),
                        func.sum(Quotation.total_price).label('total_value')
                    ).join(Quotation).filter(
                        Quotation.created_at.between(start_date, end_date)
                    ).group_by(Client.id)
                )
                rows = result.mappings().all()
                return [dict(row) for row in rows]

    @handle_db_exceptions()
    async def get_product_statistics(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        async with self.session as session:
            async with session.begin():
                result = await session.execute(
                    select(
                        Product.id,
                        Product.name,
                        func.count(QuotationProduct.quotation_id).label('quotation_count'),
                        func.sum(QuotationProduct.quantity).label('total_quantity'),
                        func.sum(QuotationProduct.price * QuotationProduct.quantity).label('total_value')
                    ).join(QuotationProduct).join(Quotation).filter(
                        Quotation.created_at.between(start_date, end_date)
                    ).group_by(Product.id)
                )
                rows = result.mappings().all()
                return [dict(row) for row in rows]

    @handle_db_exceptions()
    async def get_daily_quotation_trend(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        async with self.session as session:
            async with session.begin():
                result = await session.execute(
                    select(
                        func.date(Quotation.created_at).label('date'),
                        func.count(Quotation.id).label('count'),
                        func.sum(Quotation.total_price).label('total_value')
                    ).filter(
                        Quotation.created_at.between(start_date, end_date)
                    ).group_by(func.date(Quotation.created_at))
                )
                rows = result.mappings().all()
                return [dict(row) for row in rows]