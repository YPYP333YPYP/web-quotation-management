from datetime import datetime
from http.client import HTTPException
from msilib.schema import File
from typing import List, Any, Coroutine, Sequence, Dict, Optional

import pandas as pd
from fastapi import Depends, UploadFile
from pydantic import ValidationError
from sqlalchemy import func

from models import Quotation
from repository.quotation.quotation import QuotationRepository
from repository.quotation.quotation_product import QuotationProductRepository


class QuotationService:
    def __init__(self,
                 quotation_repository: QuotationRepository = Depends(QuotationRepository),
                 quotation_product_repository: QuotationProductRepository = Depends(QuotationProductRepository)):
        self.quotation_repository = quotation_repository
        self.quotation_product_repository = quotation_product_repository

    async def create_quotation(self, quotation_data: Dict[str, Any]) -> Quotation:
        quotation_data["total_price"] = 0
        quotation = Quotation(**quotation_data)
        return await self.quotation_repository.create_quotation(quotation)

