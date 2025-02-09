import urllib.parse
import zipfile
import io

from datetime import datetime, date
from math import ceil
from typing import List, Any, Dict, Optional
from fastapi import Depends
from sqlalchemy import func
from openpyxl import Workbook

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from models import Quotation, User, QuotationProduct
from repository.client.client import ClientRepository
from repository.product.product import ProductRepository
from repository.quotation.quotation import QuotationRepository
from repository.quotation.quotation_product import QuotationProductRepository
from schemas.client import ClientPaginatedResponse
from schemas.quotation import QuotationAdd, QuotationRead, to_quotation_read, QuotationUpdate, QuotationInfo
from core.db.redis import redis_client
from service.kakao import KakaoService


class QuotationService:
    def __init__(self,
                 quotation_repository: QuotationRepository = Depends(QuotationRepository),
                 quotation_product_repository: QuotationProductRepository = Depends(QuotationProductRepository),
                 product_repository: ProductRepository = Depends(ProductRepository),
                 client_repository: ClientRepository = Depends(ClientRepository),
                 kakao_service: KakaoService = Depends(KakaoService)):
        self.quotation_repository = quotation_repository
        self.quotation_product_repository = quotation_product_repository
        self.product_repository = product_repository
        self.client_repository = client_repository
        self.kakao_service = kakao_service

    async def create_quotation(self, quotation_data: Dict[str, Any]) -> QuotationRead:
        client_id = quotation_data.get("client_id")
        input_date = quotation_data.get("input_date")

        client = await self.client_repository.get_client_by_id(client_id)
        if not client:
            raise ServiceException(ErrorStatus.CLIENT_NOT_FOUND)

        if await self.quotation_repository.exist_quotation_by_client_id_and_today_date(client_id, input_date):
            raise ServiceException(ErrorStatus.QUOTATION_ALREADY_EXISTS)

        if quotation_data.get("input_date") < datetime.now().date():
            raise ServiceException(ErrorStatus.QUOTATION_DATE_BEFORE_CURRENT)

        year = input_date.year
        month = input_date.month
        day = input_date.day
        quotation_name = f"{year:04d}/{month:02d}/{day:02d}-{client.name}"

        quotation_data["total_price"] = 0
        quotation_data["created_at"] = datetime.now().date()
        quotation_data["name"] = quotation_name

        quotation = Quotation(**quotation_data)
        quotation_read = await self.quotation_repository.create_quotation(quotation)
        result = to_quotation_read(quotation_read)
        return result

    async def add_products_to_quotation(self, quotation_data: List[QuotationAdd], current_user: User):
        tmp_list = []
        for qt in quotation_data:
            quotation_id = qt.quotation_id
            product_id = qt.product_id
            quantity = qt.quantity

            product = await self.product_repository.get_product_by_id(product_id)
            if product is None:
                raise ServiceException(ErrorStatus.PRODUCT_NOT_FOUND)

            quotation = await self.quotation_repository.get_quotation_by_id(quotation_id)
            if quotation is None:
                raise ServiceException(ErrorStatus.QUOTATION_NOT_FOUND)

            # 견적서에 물품 중복 추가 금지
            quotation_product = await self.quotation_product_repository.get_quotation_product_by_quotation_id_and_product_id(
                quotation_id=quotation_id,
                product_id=product_id
            )
            if quotation_product is not None:
                raise ServiceException(ErrorStatus.QUOTATION_PRODUCT_ALREADY_EXISTS)

            quotation_product = QuotationProduct(
                quotation_id=quotation_id,
                product_id=product_id,
                price=product.price * quantity,
                quantity=quantity,
            )
            # 견적서에 물품 추가 시 Redis 서버에 수량 증가
            await redis_client.hincrby(f"user:{current_user.client_id}:products", product_id, 1)
            tmp_list.append(quotation_product)
        return await self.quotation_product_repository.bulk_create_quotation_product(tmp_list)

    async def update_quotation_product(self, quotation_id: int, product_id: int, new_data: Dict[str, Any]) -> Optional[
        QuotationProduct]:
        product = await self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ServiceException(ErrorStatus.PRODUCT_NOT_FOUND)

        update_data = new_data

        update_data["updated_at"] = func.now()
        update_data["price"] = product.price * update_data["quantity"]
        if await self.quotation_product_repository.update_quotation_product(quotation_id, product_id, update_data):
            updated_quotation_product = await self.quotation_product_repository.get_quotation_product_by_quotation_id_and_product_id(
                quotation_id, product_id)
            return updated_quotation_product

    async def get_quotation_products(self, quotation_id: int):
        quotation_products = await self.quotation_product_repository.get_quotation_products_by_quotation_id(
            quotation_id)
        result_list = []

        for quotation_product in quotation_products:
            tmp_dict = quotation_product.to_dict()

            product_id = tmp_dict.get("product_id")
            product = await self.product_repository.get_product_by_id(product_id)

            if not product:
                raise ServiceException(ErrorStatus.PRODUCT_NOT_FOUND)

            result_dict = {
                "id": product.id,
                "category": product.category,
                "product": product.name,
                "unit": product.unit,
                "quantity": tmp_dict.get("quantity"),
                "price": tmp_dict.get("price"),
                "created_at": tmp_dict.get("created_at"),
                "updated_at": tmp_dict.get("updated_at")
            }

            result_list.append(result_dict)

        return result_list

    async def get_quotation_info(self, quotation_id: int):
        products = await self.get_quotation_products(quotation_id)
        quotation = await self.quotation_repository.get_quotation_by_id(quotation_id)

        if not quotation:
            raise ServiceException(ErrorStatus.QUOTATION_NOT_FOUND)

        quotation_info = {
            "products": products,
            "name": quotation.name,
            "total": quotation.total_price,
            "status": quotation.status,
            "input_date": quotation.input_date,
            "created_at": quotation.created_at,
            "updated_at": quotation.updated_at
        }

        return quotation_info

    async def update_total_price(self, quotation_id: int):
        return await self.quotation_repository.update_total_price(quotation_id)

    async def get_quotation_search(self, start: str, end: str, query: str):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, '%Y-%m-%d')
        quotations = await self.quotation_repository.search_quotation(start_date, end_date, query)
        result = [to_quotation_read(x) for x in quotations]
        return result

    async def extract_quotations(self, quotation_id: int, for_zip: bool = False):
        products = await self.get_quotation_products(quotation_id)
        quotation = await self.quotation_repository.get_quotation_by_id(quotation_id)

        output = io.BytesIO()
        workbook = Workbook()
        worksheet = workbook.active

        header = ["물품", "수량", "단가"]
        worksheet.append(header)

        for result_dict in products:
            row = [
                str(result_dict["product"]),
                str(result_dict["quantity"]),
                str(result_dict["price"]),
            ]
            worksheet.append(row)

        workbook.save(output)
        output.seek(0)
        filename = f'{quotation.name} 견적서'
        if not for_zip:
            filename = urllib.parse.quote(filename, encoding='utf-8')

        else:
            filename = filename + '.xlsx'

        return output, filename

    async def get_paginated_quotations_for_client(self, client_id: int, page: int = 1, page_size: int = 10):
        """ 거래처 별 견적서 반환 """
        quotations, total = await self.quotation_repository.get_quotations_by_client_id(client_id, page, page_size)
        quotation_reads = [to_quotation_read(x) for x in quotations]

        total_pages = ceil(total / page_size)

        return ClientPaginatedResponse(
            items=quotation_reads,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def get_paginated_quotations_by_date_range(
            self,
            client_id,
            start_date: date,
            end_date: date,
            page: int,
            page_size: int):
        """ 지정 날짜 범위에 해당하는 견적서 반환 """
        quotations, total = await self.quotation_repository.get_quotations_by_data_range(client_id, start_date, end_date, page, page_size)
        quotation_reads = [to_quotation_read(x) for x in quotations]

        total_pages = ceil(total / page_size)

        return ClientPaginatedResponse(
            items=quotation_reads,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def extract_today_quotations_to_zip(self, input_date: date):
        today = input_date
        quotation_ids = await self.quotation_repository.get_today_quotation_ids(today)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for quotation_id in quotation_ids:
                excel_buffer, filename = await self.extract_quotations(quotation_id, True)
                zip_file.writestr(filename, excel_buffer.getvalue())

        zip_buffer.seek(0)
        today_str = today.strftime("%Y-%m-%d")
        filename = f'minifood_{today_str}.zip'

        return zip_buffer, filename

    async def delete_quotation_product(self, quotation_id: int, product_id: int):
        await self.quotation_repository.delete_quotation_product(quotation_id, product_id)

    async def delete_quotation(self, quotation_id: int):
        await self.quotation_repository.delete_quotation(quotation_id)

    async def update_particulars(self, quotation_id: int, particulars: str):
        await self.quotation_repository.update_particulars(quotation_id, particulars)

    async def update_status_completed(self, quotation_id: int):
        # await self.kakao_service.send_quotation_completed_message(
        #     quotation_id=quotation_id,
        #     web_url=f"http://127.0.0.1:8000/api/v1/quotations/extract/{quotation_id}"
        # )
        await self.quotation_repository.update_status_completed(quotation_id)

    async def update_quotation(self, quotation_id: int, quotation_data: QuotationUpdate):
        existing_quotation = await self.quotation_repository.get_quotation_by_id(quotation_id)
        if not existing_quotation:
            raise ServiceException(ErrorStatus.QUOTATION_NOT_FOUND)

        await self.quotation_repository.update_quotation(quotation_id, quotation_data)

    async def get_quotations_by_input_date(self, input_date: str):
        input_date = datetime.strptime(input_date, "%Y-%m-%d")
        quotations = await self.quotation_repository.get_quotations_by_input_date(input_date)
        result = [to_quotation_read(x) for x in quotations]
        return result
