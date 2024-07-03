from datetime import datetime
from typing import Dict, Any, Optional, List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.database import async_get_db

from models.quotation_product import QuotationProduct


class QuotationProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def create_quotation_product(self, quotation_product: QuotationProduct):
        self.session.add(quotation_product)

    async def bulk_create_quotation_product(self, quotation_products: List[QuotationProduct]):
        for quotation_product in quotation_products:
            await self.create_quotation_product(quotation_product)

    async def get_quotation_product_by_quotation_id(self, quotation_id: int):
        async with self.session as session:
            try:
                quotation_product = await session.execute(
                    select(QuotationProduct).filter_by(quotation_id=quotation_id)
                )
                return quotation_product.scalar_one()
            except NoResultFound:
                return None

    async def get_quotation_products_by_quotation_id(self, quotation_id: int):
        async with self.session as session:
            quotation_products = await session.execute(
                select(QuotationProduct).filter_by(quotation_id=quotation_id)
            )
            return quotation_products.fetchall()

    async def get_quotation_product_by_quotation_id_and_product_id(self, quotation_id: int, product_id: int) -> Optional[QuotationProduct]:
        async with self.session as session:
            async with session.begin():
                query = select(QuotationProduct).filter_by(quotation_id=quotation_id, product_id=product_id)
                result = await session.execute(query)
                quotation_product = result.scalars().first()
                return quotation_product

    async def update_quotation_product(self, quotation_id: int, product_id: int, new_data: Dict[str, Any]):
        async with self.session as session:
            query = select(QuotationProduct).filter_by(quotation_id=quotation_id, product_id=product_id)
            result = await session.execute(query)
            quotation_product = result.scalars().first()
            if quotation_product:
                for key, value in new_data.items():
                    setattr(quotation_product, key, value)
                quotation_product.updated_at = datetime.utcnow()
                await session.commit()
                await session.refresh(quotation_product)
                return True
            else:
                return False