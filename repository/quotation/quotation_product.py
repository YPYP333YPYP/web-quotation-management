from fastapi import Depends
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