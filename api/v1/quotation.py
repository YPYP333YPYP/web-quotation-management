from typing import List

from fastapi import HTTPException, APIRouter, Depends
from starlette.responses import JSONResponse

from schemas.quotation import QuotationCreate, QuotationAdd, QuotationUpdate, QuotationProductRead
from service.quotation import QuotationService

router = APIRouter(tags=["quotation"])


@router.post("/quotations/",
             summary="견적서 생성",
             description="견적서를 생성합니다.")
async def create_quotation(quotation: QuotationCreate, quotation_service: QuotationService = Depends(QuotationService)):
    new_data = quotation.dict()
    await quotation_service.create_quotation(new_data)
    return JSONResponse(content={"message": "Create successful"})


@router.post("/quotations/product",
             summary="견적서 물품 생성",
             description="견적서에 물품을 추가합니다.")
async def add_product_to_quotation(quotation: QuotationAdd,
                                   quotation_service: QuotationService = Depends(QuotationService)):
    new_data = quotation.dict()
    await quotation_service.add_product_to_quotation(new_data)
    return JSONResponse(content={"message": "Create successful"})


@router.put("/quotations/{quotation_id}/{product_id}",
            summary="견적서 물품 수정",
            description="견적서의 물품을 수정합니다.")
async def update_quotation_product(product_id: int,
                                   quotation_id: int,
                                   update_data: QuotationUpdate,
                                   quotation_service: QuotationService = Depends(QuotationService)) -> None:
    new_data = update_data.dict()
    updated_quotation_product = await quotation_service.update_quotation_product(product_id, quotation_id, new_data)
    if not updated_quotation_product:
        raise HTTPException(status_code=404, detail="Quotation product not found")


@router.get("/quotations/{quotation_id}",
            summary="견적서 물품 리스트 조회",
            description="견적서의 물품 리스트를 조회합니다.")
async def get_quotation_products(quotation_id: int,
                                 quotation_service: QuotationService = Depends(QuotationService)) -> List[QuotationProductRead]:
    return await quotation_service.get_quotation_products(quotation_id)