from typing import Sequence, List

from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from models.custom_product import CustomProduct
from repository.custom_product.custom_product import CustomProductRepository
from schemas.custom_product import CustomProductCreate, CustomProductRead, CustomProductUpdate, to_custom_product_read


class CustomProductService:
    def __init__(self, custom_product_repository: CustomProductRepository = Depends(CustomProductRepository)):
        self.custom_product_repository = custom_product_repository

    async def create_custom_product(self, custom_product_data: CustomProductCreate):
        await self.custom_product_repository.create_custom_product(custom_product_data)

    async def create_custom_product_bulk(self, custom_product_form: List[CustomProductCreate]):
        for custom_product_data in custom_product_form:
            await self.create_custom_product(custom_product_data)

    async def get_custom_product(self, custom_product_id: int) -> CustomProductRead:
        custom_product = await self.custom_product_repository.get_by_id(custom_product_id)
        if not custom_product:
            raise ServiceException(ErrorStatus.CUSTOM_PRODUCT_NOT_FOUND)
        return to_custom_product_read(custom_product)

    async def update_custom_product(self, custom_product_id: int, update_data: CustomProductUpdate):
        return await self.custom_product_repository.update_custom_product(custom_product_id, update_data)

    async def delete_custom_product(self, custom_product_id: int):
        await self.custom_product_repository.delete_custom_product(custom_product_id)

    async def get_all_custom_products(self) -> Sequence[CustomProduct]:
        custom_products = await self.custom_product_repository.get_all()
        return [to_custom_product_read(x) for x in custom_products]
