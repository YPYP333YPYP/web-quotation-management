from datetime import datetime
from typing import Sequence, Dict, Any, Optional
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.decorator.decorator import handle_db_exceptions
from core.db.database import async_get_db
from models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def create_product(self, product: Product):
        async with self.session as session:
            session.add(product)
            await session.commit()

    @handle_db_exceptions()
    async def get_products_by_category(self, category: str) -> Sequence[Product]:
        async with self.session as session:
            stmt = select(Product).filter(Product.category == category)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return products

    @handle_db_exceptions()
    async def get_all_products(self):
        async with self.session as session:
            stmt = select(Product)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return products

    @handle_db_exceptions()
    async def update_product(self, product_id: int, new_data: Dict[str, Any]):
        async with self.session as session:
            product = await session.get(Product, product_id)
            if product:
                for key, value in new_data.items():
                    setattr(product, key, value)
                product.updated_at = datetime.now()
                await session.commit()
                return True
            else:
                return False

    @handle_db_exceptions()
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        async with self.session as session:
            product = await session.get(Product, product_id)
            return product if product else None

    @handle_db_exceptions()
    async def get_product_by_name(self, product_name: str) -> Optional[Product]:
        async with self.session as session:
            result = await session.execute(select(Product).where(Product.name == product_name))
            product = result.scalar_one_or_none()
            return product if product else None

    @handle_db_exceptions()
    async def exists_product_by_name(self, name: str) -> bool:
        async with self.session as session:
            product = await session.get(Product, name)
            if product is None:
                return False
            else:
                return True

    @handle_db_exceptions()
    async def delete_product_by_id(self, product_id: int):
        async with self.session as session:
            stmt = select(Product).filter(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if product:
                await session.delete(product)
                await session.commit()

    @handle_db_exceptions()
    async def update_vegetable_product_price(self, product_id: int, price: int):
        async with self.session as session:
            product = await session.get(Product, product_id)
            if product:
                product.price = price
                product.updated_at = datetime.now()
                await session.commit()
                return True
            else:
                raise ValueError(f"Product {product_id} does not exist")

    @handle_db_exceptions()
    async def update_vegetable_products_price(self, price_data: dict):
        async with self.session as session:
            updated_count = 0
            for product_name, new_price in price_data.items():
                try:
                    product = await session.execute(select(Product).where(Product.name == product_name))
                    product = product.scalar_one_or_none()

                    if product:
                        product.price = new_price
                        product.updated_at = datetime.now()
                        updated_count += 1
                    else:
                        raise ValueError((f"Product not found: {product_name}"))
                except Exception as e:
                    raise ValueError(f"Error updating {product_name}: {str(e)}")

            await session.commit()
            return updated_count

    @handle_db_exceptions()
    async def get_products_by_prefix(self, name_prefix: str, limit: int) -> Sequence[Product]:
        async with self.session as session:
            query = (
                select(Product)
                .where(func.lower(Product.name).like(f"%{name_prefix.lower()}%"))
                .order_by(func.length(Product.name))
                .limit(limit)
            )
            result = await session.execute(query)
            products = result.scalars().all()
        return products