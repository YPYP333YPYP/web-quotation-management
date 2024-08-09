import os
from datetime import datetime
from typing import Any, Sequence, Dict, Optional

import pandas as pd
import pytz
from fastapi import Depends, UploadFile
from pydantic import ValidationError

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from models import User
from repository.product.product import ProductRepository
from models.product import Product
from schemas.product import ProductRead, to_product_count

from core.db.redis import redis_client


def read_excel_file_about_product_list(file_path: str) -> list[Dict]:
    data = list()
    xls = pd.ExcelFile(file_path)
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        category = sheet_name
        for _, row in df.iterrows():
            try:
                price = row.iloc[2]
                if type(price) is str:
                    price = int(price.replace(",", ""))
                product_data = {
                    'name': row.iloc[0],
                    'unit': row.iloc[1],
                    'price': price,
                    'category': category
                }
                data.append(product_data)
            except ValidationError as e:
                raise ServiceException(ErrorStatus.INVALID_VALUE)
    return data


def read_excel_file_about_vegetable_price_list(file_path: str) -> dict:
    data = dict()
    df = pd.read_excel(file_path, header=None)
    try:
        for _, row in df.iterrows():
            product_name = row.iloc[0]
            price = row.iloc[1]
            data[product_name] = price
    except ValidationError as e:
        raise ServiceException(ErrorStatus.INVALID_VALUE)
    return data


class ProductService:
    def __init__(self, product_repository: ProductRepository = Depends(ProductRepository)):
        self.product_repository = product_repository

    async def upload_products(self, file: UploadFile):
        try:
            EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH')
            file_path = os.path.join(EXCEL_FILE_PATH, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            product_datas = read_excel_file_about_product_list(file_path)
            for product_data in product_datas:
                print(product_data)
                product = await self.product_repository.get_product_by_name(product_data["name"])
                if product:
                    await self.product_repository.update_product(product.id, product_data)
                else:
                    product = Product(**product_data)
                    await self.product_repository.create_product(product)

        except Exception as e:
            print(e)
            raise ServiceException(ErrorStatus.FILE_UPLOAD_ERROR)

    async def get_products_by_category(self, category: str) -> Sequence[Product]:
        return await self.product_repository.get_products_by_category(category)

    async def update_product(self, product_id: int, new_data: Dict[str, Any]) -> Optional[Product]:

        product = new_data

        if not new_data:
            return None

        if await self.product_repository.update_product(product_id, product):
            updated_product = await self.product_repository.get_product_by_id(product_id)
            return updated_product

        return None

    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        product_name = product_data["name"]
        if not await self.product_repository.exists_product_by_name(product_name):
            product = Product(**product_data)
            return await self.product_repository.create_product(product)
        else:
            raise ServiceException(ErrorStatus.PRODUCT_NOT_CREATED)

    async def delete_product(self, product_id: int) -> None:
        await self.product_repository.delete_product_by_id(product_id)

    async def update_vegetable_product_price(self, product_id, price):
        if await self.product_repository.update_vegetable_product_price(product_id, price):
            return True
        else:
            raise ServiceException(ErrorStatus.PRODUCT_NOT_UPDATED)

    async def update_vegetable_product_price_from_file(self, file: UploadFile):
        try:
            EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH')
            file_path = os.path.join(EXCEL_FILE_PATH, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            vegetable_price_data = read_excel_file_about_vegetable_price_list(file_path)
            result = await self.product_repository.update_vegetable_products_price(vegetable_price_data)
        except Exception as e:
            raise ServiceException(ErrorStatus.FILE_UPLOAD_ERROR)

    async def search_products_by_prefix(self, name_prefix: str, limit: int):
        products = await self.product_repository.get_products_by_prefix(name_prefix, limit)
        products = sorted(products, key=lambda x: x.name.lower())

        return [ProductRead.from_orm(p) for p in products]

    async def search_products_recent(self, limit: int, current_user: User):
        product_counts = await redis_client.hgetall(f"user:{current_user.client_id}:products")
        sorted_products = sorted(product_counts.items(), key=lambda x: int(x[1]), reverse=True)[:limit]
        products_list = [to_product_count(await self.product_repository.get_product_by_id(x[0]), x[1]) for x in
                         sorted_products]
        return products_list
