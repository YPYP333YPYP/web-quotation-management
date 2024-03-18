from typing import List, Sequence, Dict, Any, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from core.db.database import async_get_db
from sqlalchemy.future import select


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def create_product(self, product: Product):
        self.session.add(product)

    async def get_products_by_category(self, category: str) -> Sequence[Product]:
        async with self.session as session:
            stmt = select(Product).filter(Product.category == category)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return products

    async def update_product(self, product_id: int, new_data: Dict[str, Any]):
        async with self.session as session:
            product = await session.get(Product, product_id)
            if product:
                for key, value in new_data.items():
                    setattr(product, key, value)
                await session.commit()
                return True
            else:
                return False

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        async with self.session as session:
            product = await session.get(Product, product_id)
            return product if product else None

    async def exists_product_by_name(self, name: str) -> bool:
        async with self.session as session:
            product = await session.get(Product, name)
            if product is None:
                return False
            else:
                return True
