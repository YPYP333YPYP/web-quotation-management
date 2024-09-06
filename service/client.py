from datetime import date

from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException, ServiceException
from models import Client
from repository.client.client import ClientRepository
from repository.product.product import ProductRepository
from repository.quotation.quotation import QuotationRepository
from repository.quotation.quotation_product import QuotationProductRepository
from schemas.client import to_client_check_preview, RegionType, ClientUpdate, ClientCreate, to_client_read, ClientRead
from schemas.quotation import QuotationRecentInfo
from service.user import UserService


class ClientService:
    def __init__(self, client_repository: ClientRepository = Depends(ClientRepository),
                 user_service: UserService = Depends(UserService),
                 quotation_repository: QuotationRepository = Depends(QuotationRepository),
                 product_repository: ProductRepository = Depends(ProductRepository),
                 quotation_product_repository: QuotationProductRepository = Depends(QuotationProductRepository)):
        self.client_repository = client_repository
        self.user_service = user_service
        self.quotation_repository = quotation_repository
        self.product_repository = product_repository
        self.quotation_product_repository = quotation_product_repository

    async def get_clients_by_name(self, name: str) -> list[ClientRead]:
        clients = await self.client_repository.get_clients_by_name(name)
        return [to_client_read(x) for x in clients]

    async def get_clients_by_region(self, region: str) -> list[ClientRead]:
        clients = await self.client_repository.get_clients_by_region(region)
        return [to_client_read(x) for x in clients]

    async def create_client(self, client_create: ClientCreate, user_id: int):
        client_data = client_create.dict()
        client = Client(**client_data)

        response_client = await self.client_repository.create_client(client)
        await self.user_service.link_user_to_client(response_client.id, user_id)

    async def delete_client(self, client_id: int):
        return await self.client_repository.delete_client_by_id(client_id)

    async def update_client(self, client_id: int, client_update: ClientUpdate):
        client_data = client_update.dict()
        return await self.client_repository.update_client(client_id, client_data)

    async def update_client_region(self, client_id: int, region: RegionType):
        await self.client_repository.update_client_region(client_id, region)

    async def get_client_check_preview(self, client_id: int, input_date: date):
        client = await self.client_repository.get_client_by_id(client_id)
        if not client:
            raise GeneralException(ErrorStatus.CLIENT_NOT_FOUND)

        quotation = await self.quotation_repository.get_quotation_by_client_and_date(client_id, input_date)
        status = quotation is not None

        result = to_client_check_preview(client, status)
        return result

    async def update_client_comment(self, client_id: int, input_comment: str):
        await self.client_repository.update_client_comment(client_id, input_comment)

    async def get_client_quotation_info_recent(self, client_id: int):
        quotations, _ = await self.quotation_repository.get_quotations_by_client_id(client_id)
        if len(quotations) == 0:
            raise ServiceException(ErrorStatus.QUOTATION_NOT_FOUND)
        recent_quotations = sorted(quotations, key=lambda x: x.created_at, reverse=True)[:3]
        result = []
        for quotation in recent_quotations:
            quotation_products = await self.quotation_product_repository.get_quotation_products_by_quotation_id(quotation.id)
            product_list = [await self.product_repository.get_product_by_id(x.product_id) for x in quotation_products]
            products = product_list[:5]
            product_name = [x.name for x in products]
            recent_info = QuotationRecentInfo(
                products=product_name,
                date=quotation.created_at.date()
            )

            result.append(recent_info)
        return result

    async def get_clients_all(self):
        clients = await self.client_repository.get_clients_all()
        return [to_client_read(x) for x in clients]

