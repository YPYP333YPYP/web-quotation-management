from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from core.utils import string_to_list, list_to_string
from repository.past_order.past_order import PastOrderRepository
from repository.product.product import ProductRepository
from schemas.past_order import PastOrderCreate, to_past_order_read, to_past_order_info
from schemas.product import to_product_read


class PastOrderService:
    def __init__(self, past_order_repository: PastOrderRepository = Depends(PastOrderRepository),
                 product_repository: ProductRepository = Depends(ProductRepository)):
        self.past_order_repository = past_order_repository
        self.product_repository = product_repository

    async def create_past_order(self, past_order_data: PastOrderCreate):
        if await self.past_order_repository.get_by_name(past_order_data.name):
            raise ServiceException(ErrorStatus.PAST_ORDER_ALREADY_EXISTS)
        past_order = await self.past_order_repository.create_past_order(past_order_data)
        past_order_id = past_order.id
        return past_order_id

    async def get_past_order(self, past_order_id: int):
        past_order = await self.past_order_repository.get_by_id(past_order_id)
        if past_order is None:
            raise ServiceException(ErrorStatus.PAST_ORDER_NOT_FOUND)
        product_idx = string_to_list(past_order.product_ids)
        products = [await self.product_repository.get_product_by_id(idx) for idx in product_idx]
        product_list = [to_product_read(product) for product in products]
        return to_past_order_read(past_order, product_list)

    async def get_past_order_by_client_id(self, client_id: int):
        past_orders = await self.past_order_repository.get_by_client_id(client_id)
        result = [to_past_order_info(past_order) for past_order in past_orders]
        return result

    async def update_past_order(self, past_order_id: int, update_past_order: dict):
        update_past_order["product_ids"] = list_to_string(update_past_order["product_ids"])
        await self.past_order_repository.update_past_order(past_order_id, update_past_order)

    async def delete_past_order(self, past_order_id: int):
        await self.past_order_repository.delete_past_order(past_order_id)

    async def add_product_past_order(self, past_order_id: int, product_id: int):
        """ 생성된 즐겨찾기에 물품 추가 """
        past_order = await self.past_order_repository.get_by_id(past_order_id)
        if past_order is None:
            raise ServiceException(ErrorStatus.PAST_ORDER_NOT_FOUND)
        product_list = string_to_list(past_order.product_ids)
        if product_id in product_list:
            raise ServiceException(ErrorStatus.PAST_ORDER_ALREADY_CONTAIN_PRODUCT)
        await self.past_order_repository.update_past_order_product(past_order_id, product_id)

    async def remove_product_past_order(self, past_order_id: int, product_id: int):
        """ 생성된 즐겨찾기에 물품 삭제 """
        past_order = await self.past_order_repository.get_by_id(past_order_id)
        if past_order is None:
            raise ServiceException(ErrorStatus.PAST_ORDER_NOT_FOUND)
        product_list = string_to_list(past_order.product_ids)
        if product_id not in product_list:
            raise ServiceException(ErrorStatus.PAST_ORDER_NOT_CONTAIN_PRODUCT)
        await self.past_order_repository.delete_path_order_product(past_order_id, product_id)
