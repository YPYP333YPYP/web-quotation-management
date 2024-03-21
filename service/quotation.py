from typing import List, Any, Coroutine, Sequence, Dict, Optional
from fastapi import Depends, UploadFile, HTTPException

from models import Quotation
from models.quotation_product import QuotationProduct
from repository.product.product import ProductRepository
from repository.quotation.quotation import QuotationRepository
from repository.quotation.quotation_product import QuotationProductRepository


class QuotationService:
    def __init__(self,
                 quotation_repository: QuotationRepository = Depends(QuotationRepository),
                 quotation_product_repository: QuotationProductRepository = Depends(QuotationProductRepository),
                 product_repository: ProductRepository = Depends(ProductRepository)):
        self.quotation_repository = quotation_repository
        self.quotation_product_repository = quotation_product_repository
        self.product_repository = product_repository

    async def create_quotation(self, quotation_data: Dict[str, Any]) -> Quotation:
        quotation_data["total_price"] = 0
        quotation = Quotation(**quotation_data)
        return await self.quotation_repository.create_quotation(quotation)

    async def add_product_to_quotation(self, quotation_data: Dict[str, Any]):
        quotation_id = quotation_data["quotation_id"]
        product_id = quotation_data["product_id"]
        number = quotation_data["quantity"]

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
            id=quotation_id,
            product_id=product_id,
            price=product.price * number,
            number=number,
        )

        return await self.quotation_product_repository.create_quotation_product(quotation_product)
