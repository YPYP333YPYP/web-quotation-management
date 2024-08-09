from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from repository.custom_product.custom_product import CustomProductRepository
from schemas.custom_product import CustomProductCreate, CustomProductRead


class CustomProductService:
    def __init__(self, custom_product_repository: CustomProductRepository = Depends(CustomProductRepository)):
        self.custom_product_repository = custom_product_repository

    async def create_custom_product(self, custom_product_data: CustomProductCreate):
        return await self.custom_product_repository.create_custom_product(custom_product_data)

    async def get_custom_product(self, custom_product_id: int) -> CustomProductRead:
        custom_product = await self.custom_product_repository.get_by_id(custom_product_id)
        if not custom_product:
            raise ServiceException(ErrorStatus.CUSTOM_PRODUCT_NOT_FOUND)
        return custom_product