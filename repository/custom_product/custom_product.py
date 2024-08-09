from datetime import datetime
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models.custom_product import CustomProduct
from schemas.custom_product import CustomProductUpdate
from service.custom_product import CustomProductCreate


class CustomProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def create_custom_product(self, custom_product_data: CustomProductCreate) -> CustomProduct:
        async with self.session as session:
            custom_product = CustomProduct(
                name=custom_product_data.name,
                image_url=custom_product_data.image_url,
                description=custom_product_data.description,
                category=custom_product_data.category,
                unit=custom_product_data.unit,
                price=custom_product_data.price,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            session.add(custom_product)
            await session.commit()
            await session.refresh(custom_product)
            return custom_product

    @handle_db_exceptions()
    async def get_by_id(self, custom_product_id: int) -> Optional[CustomProduct]:
        async with self.session as session:
            return await session.get(CustomProduct, custom_product_id)

    @handle_db_exceptions()
    async def update_custom_product(self, custom_product_id: int, update_data: CustomProductUpdate):
        async with self.session as session:
            custom_product = await session.get(CustomProduct, custom_product_id)
            if custom_product:
                for key, value in update_data.dict(exclude_unset=True).items():
                    setattr(custom_product, key, value)
                custom_product.updated_at = datetime.now()
                await session.commit()
                return custom_product