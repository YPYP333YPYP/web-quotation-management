from typing import List, Sequence

from fastapi import UploadFile, File, HTTPException, APIRouter, Depends, Form
from starlette.responses import JSONResponse

from schemas.quotation import QuotationCreate
from service.quotation import QuotationService

router = APIRouter(tags=["quotation"])

@router.post("/quotations/",
             summary="견적서 생성",
             description="견적서를 생성합니다.")
async def create_quotation(quotation: QuotationCreate, quotation_service: QuotationService = Depends(QuotationService)):
    new_data = quotation.dict()
    await quotation_service.create_quotation(new_data)
    return JSONResponse(content={"message": "Create successful"})