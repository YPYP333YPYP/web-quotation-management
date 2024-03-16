from typing import List, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from core.db.database import async_get_db
from sqlalchemy.future import select


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def add_product(self, product: Product):
        self.session.add(product)

    async def get_products_by_category(self, category: str) -> Sequence[Product]:
        async with self.session as session:
            stmt = select(Product).filter(Product.category == category)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return products
