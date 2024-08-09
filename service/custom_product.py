from fastapi import Depends

from repository.custom_product.custom_product import CustomProductRepository
from schemas.custom_product import CustomProductCreate


class CustomProductService:
    def __init__(self, custom_product_repository: CustomProductRepository = Depends(CustomProductRepository)):
        self.custom_product_repository = custom_product_repository

    async def create_custom_product(self, custom_product_data: CustomProductCreate):
        return await self.custom_product_repository.create_custom_product(custom_product_data)