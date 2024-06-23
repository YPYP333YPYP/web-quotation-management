from datetime import datetime
from fastapi import HTTPException
from msilib.schema import File
from typing import List, Any, Coroutine, Sequence, Dict, Optional

import pandas as pd
from fastapi import Depends, UploadFile
from pydantic import ValidationError
from sqlalchemy import func

from repository.product.product import ProductRepository
from models.product import Product


def read_excel_file_about_product_list(file_path: str) -> list[Product]:
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
                product = Product(**product_data)
                data.append(product)
            except ValidationError as e:
                raise Exception("excel file contains invalid")
    return data


def read_excel_file_about_vegetable_price_list(file_path: str) -> dict:
    data = dict()
    xls = pd.ExcelFile(file_path)
    df = pd.read_excel(file_path, header=None)

    for _, row in df.iterrows():
        product_name = row.iloc[0]
        price = row.iloc[1]
        data[product_name] = price

    return data


class ProductService:
    def __init__(self, product_repository: ProductRepository = Depends(ProductRepository)):
        self.product_repository = product_repository

    async def upload_products(self, file: UploadFile = File):
        try:
            file_path = f"./datas/excel_file/{file.filename}"
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            products = read_excel_file_about_product_list(file_path)

            for product in products:
                await self.product_repository.create_product(product)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f" IO Exception - detail -> {str(e)}")

    async def get_products_by_category(self, category: str) -> Sequence[Product]:
        return await self.product_repository.get_products_by_category(category)

    async def update_product(self, product_id: int, new_data: Dict[str, Any]) -> Optional[Product]:

        product = new_data
        product["updated_at"] = func.now()
        if not new_data:
            return None

        if await self.product_repository.update_product(product_id, product):
            updated_product = await self.product_repository.get_product_by_id(product_id)
            return updated_product

        return None

    async def create_product(self, product_data: Dict[str, Any]) -> Product:
        product_name = product_data["name"]
        if self.product_repository.exists_product_by_name(product_name):
            product = Product(**product_data)
            return await self.product_repository.create_product(product)
        else:
            raise HTTPException(status_code=404, detail="Product not found")

    async def delete_product(self, product_id: int) -> None:
        await self.product_repository.delete_product_by_id(product_id)

    async def update_vegetable_product_price(self, product_id, price):
        if await self.product_repository.update_vegetable_product_price(product_id, price):
            return True
        else:
            raise HTTPException(status_code=401, detail="Product Not updated")

    async def update_vegetable_product_price_from_file(self, file: UploadFile = File):
        try:
            file_path = f"./datas/excel_file/{file.filename}"
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            vegetable_price_data = read_excel_file_about_vegetable_price_list(file_path)
            result = await self.product_repository.update_vegetable_products_price(vegetable_price_data)
            return {"message": "Update successful", "updated_count": result}
        except Exception as e:
            print(f"Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"IO Exception - detail -> {str(e)}")




