from http.client import HTTPException
from msilib.schema import File
from typing import List, Any, Coroutine, Sequence, Dict, Optional

import pandas as pd
from fastapi import Depends, UploadFile
from pydantic import ValidationError
from repository.product.product import ProductRepository
from models.product import Product


def read_excel_file(file_path: str) -> list[Product]:
    data = []
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
                raise HTTPException(status_code=400, detail=str(e))
    return data


class ProductService:
    def __init__(self, product_repository: ProductRepository = Depends(ProductRepository)):
        self.product_repository = product_repository

    async def upload_products(self, file: UploadFile = File):
        try:
            file_path = f"./datas/excel_file/{file.filename}"
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            products = read_excel_file(file_path)

            for product in products:
                await self.product_repository.add_product(product)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_products_by_category(self, category: str) -> Sequence[Product]:
        return await self.product_repository.get_products_by_category(category)

    async def update_product(self, product_id: int, new_data: Dict[str, Any]) -> Optional[Product]:

        if not new_data:
            return None

        if await self.product_repository.update_product(product_id, new_data):
            updated_product = await self.product_repository.get_product_by_id(product_id)
            return updated_product

        return None
