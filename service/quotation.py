from datetime import datetime, date
from typing import List, Any, Coroutine, Sequence, Dict, Optional
from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy import func

from models import Quotation
from models.quotation_product import QuotationProduct
from repository.client.client import ClientRepository
from repository.product.product import ProductRepository
from repository.quotation.quotation import QuotationRepository
from repository.quotation.quotation_product import QuotationProductRepository
from schemas.quotation import QuotationProductRead, QuotationAdd


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
                raise HTTPException(status_code=404, detail="Product not found")

            quotation = await self.quotation_repository.get_quotation_by_id(quotation_id)
            if quotation is None:
                raise HTTPException(status_code=404, detail="Quotation not found")

            quotation_product = await self.quotation_product_repository.get_quotation_product_by_quotation_id_and_product_id(
                quotation_id=quotation_id,
                product_id=product_id
            )
            if quotation_product is not None:
                raise HTTPException(status_code=400, detail="Already exists product at quotation")

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

        update_data = new_data

        update_data["updated_at"] = func.now()
        update_data["price"] = product.price * update_data["quantity"]

        if await self.quotation_product_repository.update_quotation_product(quotation_id, product_id, update_data):
            updated_quotation_product = await self.quotation_product_repository.get_quotation_product_by_quotation_id_and_product_id(
                quotation_id, product_id)
            return updated_quotation_product

        return None

    async def get_quotation_products(self, quotation_id: int) -> List[QuotationProductRead]:
        quotation_products = await self.quotation_product_repository.get_quotation_products_by_quotation_id(
            quotation_id)

        result_list = []

        for quotation_product in quotation_products:
            tmp_dict = quotation_product[0].to_dict()

            product_id = tmp_dict.get("product_id")
            product = await self.product_repository.get_product_by_id(product_id)

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
