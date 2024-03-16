from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from core.db.database import async_get_db


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def add_product(self, product: Product):
        self.session.add(product)
