import urllib.parse
import zipfile
from datetime import datetime, date
from math import ceil
from typing import List, Any, Dict, Optional

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.base import _T_co

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from models import Quotation
from models.quotation_product import QuotationProduct
from repository.client.client import ClientRepository
from repository.product.product import ProductRepository
from repository.quotation.quotation import QuotationRepository
from repository.quotation.quotation_product import QuotationProductRepository
from schemas.client import ClientPaginatedResponse
from schemas.quotation import QuotationAdd, QuotationRead

import io
from openpyxl import Workbook


class QuotationService:
    def __init__(self,
                 quotation_repository: QuotationRepository = Depends(QuotationRepository),
                 quotation_product_repository: QuotationProductRepository = Depends(QuotationProductRepository),
                 product_repository: ProductRepository = Depends(ProductRepository),
                 client_repository: ClientRepository = Depends(ClientRepository)):
        self.quotation_repository = quotation_repository
        self.quotation_product_repository = quotation_product_repository
        self.product_repository = product_repository
        self.client_repository = client_repository

    async def create_quotation(self, quotation_data: Dict[str, Any]) -> Quotation:
        client_id = quotation_data.get("client_id")
        client = await self.client_repository.get_client_by_id(client_id)
        if not client:
            raise ServiceException(ErrorStatus.CLIENT_NOT_FOUND)

        now_datetime = datetime.now()
        year = now_datetime.year
        month = now_datetime.month
        day = now_datetime.day
        quotation_name = f"{year}/{month}/{day}-{client.name}"

        quotation_data["total_price"] = 0
        quotation_data["name"] = quotation_name

        quotation = Quotation(**quotation_data)
        return await self.quotation_repository.create_quotation(quotation)

    async def add_products_to_quotation(self, quotation_data: List[QuotationAdd]):
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

    async def get_quotation_products(self, quotation_id: int) -> list[
        dict[str, InstrumentedAttribute[_T_co] | _T_co | Any]]:
        quotation_products = await self.quotation_product_repository.get_quotation_products_by_quotation_id(
            quotation_id)

        result_list = []

        for quotation_product in quotation_products:
            tmp_dict = quotation_product[0].to_dict()

            product_id = tmp_dict.get("product_id")
            product = await self.product_repository.get_product_by_id(product_id)

            if not product:
                raise ServiceException(ErrorStatus.PRODUCT_NOT_FOUND)

            result_dict = {
                "product": product.name,
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

        if not products:
            raise ServiceException(ErrorStatus.PRODUCT_NOT_FOUND)

        quotation_info = {
            "products": products,
            "name": quotation.name,
            "total": quotation.total_price,
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
        return quotations

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

        quotations, total = await self.quotation_repository.get_quotations_by_client_id(client_id, page, page_size)
        quotation_reads = [
            QuotationRead(
                id=q.id,
                name=q.name,
                total_price=q.total_price,
                created_at=q.created_at,
                updated_at=q.updated_at
            ) for q in quotations
        ]

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

        quotations, total = await self.quotation_repository.get_quotations_by_data_range(client_id, start_date, end_date, page, page_size)
        quotation_reads = [
            QuotationRead(
                id=q.id,
                name=q.name,
                total_price=q.total_price,
                created_at=q.created_at,
                updated_at=q.updated_at
            ) for q in quotations
        ]

        total_pages = ceil(total / page_size)

        return ClientPaginatedResponse(
            items=quotation_reads,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    async def extract_today_quotations_to_zip(self):
        today = date.today()
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
