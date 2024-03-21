from typing import Dict, Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.database import async_get_db

from models.quotation_product import QuotationProduct


class QuotationProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def create_quotation_product(self, quotation_product: QuotationProduct):
        self.session.add(quotation_product)

    async def get_quotation_product_by_quotation_id(self, quotation_id: int):
        async with self.session as session:
            quotation_product = await session.get(QuotationProduct, quotation_id)
            return quotation_product if quotation_product else None

    async def get_quotation_product_by_quotation_id_and_product_id(self, quotation_id: int, product_id: int):
        async with self.session as session:
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
                await session.commit()
                return True
            else:
                return False