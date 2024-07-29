from datetime import date
from typing import List, Optional

from fastapi import HTTPException, APIRouter, Depends, Query
from starlette.responses import JSONResponse, StreamingResponse

from api.dependencies import get_current_user
from core.decorator.decorator import handle_exceptions
from models import User
from schemas.quotation import QuotationCreate, QuotationAdd, QuotationUpdate, QuotationRead, QuotationInfo, \
    to_quotation_read
from service.quotation import QuotationService

from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import GeneralException

router = APIRouter(tags=["quotation"])


@router.post("/quotations",
             response_model=ApiResponse[QuotationRead],
             summary="견적서 생성",
             description="견적서를 생성합니다.")
@handle_exceptions(QuotationRead)
async def create_quotation(quotation: QuotationCreate, quotation_service: QuotationService = Depends(QuotationService)):
    new_data = quotation.dict()
    quotation = await quotation_service.create_quotation(new_data)
    return quotation


@router.delete("/quotations/{quotation_id}/delete",
               response_model=ApiResponse,
               summary="견적서 삭제",
               description="견적서를 삭제합니다.")
@handle_exceptions()
async def delete_quotation(quotation_id: int, quotation_service: QuotationService = Depends(QuotationService)):
    await quotation_service.delete_quotation(quotation_id)
    return ApiResponse.on_success()


@router.post("/quotations/products",
             response_model=ApiResponse,
             summary="견적서 물품 생성",
             description="견적서에 물품을 추가합니다.")
@handle_exceptions()
async def add_products_to_quotation(quotation: List[QuotationAdd],
                                    quotation_service: QuotationService = Depends(QuotationService),
                                    current_user: User = Depends(get_current_user)
                                    ):
    await quotation_service.add_products_to_quotation(quotation, current_user)
    return ApiResponse.on_success()


@router.put("/quotations/{quotation_id}/{product_id}",
            response_model=ApiResponse,
            summary="견적서 물품 수정",
            description="견적서의 물품을 수정합니다.")
@handle_exceptions()
async def update_quotation_product(quotation_id: int,
                                   product_id: int,
                                   update_data: QuotationUpdate,
                                   quotation_service: QuotationService = Depends(QuotationService)):
    new_data = update_data.dict()
    updated_quotation_product = await quotation_service.update_quotation_product(quotation_id, product_id, new_data)
    if not updated_quotation_product:
        raise GeneralException(ErrorStatus.QUOTATION_NOT_UPDATED)
    else:
        return ApiResponse.on_success()


@router.delete("/quotations/{quotation_id}/{product_id}/delete",
               response_model=ApiResponse,
               summary="견적서 물품 삭제",
               description="견적서의 물품을 삭제합니다.")
@handle_exceptions()
async def delete_quotation_product(quotation_id: int, product_id: int, quotation_service: QuotationService = Depends(QuotationService)):
    await quotation_service.delete_quotation_product(quotation_id, product_id)
    return ApiResponse.on_success()


@router.get("/quotations/{quotation_id}",
            response_model=ApiResponse[QuotationInfo],
            summary="견적서 정보 조회",
            description="견적서의 주문 물품, 이름, 총 금액, 생성 일, 수정 일 정보를 조회 합니다.")
@handle_exceptions(QuotationInfo)
async def get_quotation_products(quotation_id: int,
                                 quotation_service: QuotationService = Depends(QuotationService)) -> QuotationInfo:
    quotation = await quotation_service.get_quotation_info(quotation_id)
    return quotation


@router.get("/quotations/{quotation_id}/total",
            response_model=ApiResponse[int],
            summary="견적서 합계 금액 업데이트",
            description="견적서의 합계 금액을 업데이트 합니다.")
@handle_exceptions(int)
async def update_total_price(quotation_id: int, quotation_service: QuotationService = Depends(QuotationService)):
    updated_sum = await quotation_service.update_total_price(quotation_id)
    return updated_sum


@router.patch("/quotations/{quotation_id}/particulars",
              response_model=ApiResponse,
              summary="견적서 특이사항 작성",
              description="견적서의 특이사항을 작성합니다.")
@handle_exceptions()
async def update_particulars(quotation_id: int, particulars: str, quotation_service: QuotationService = Depends(QuotationService)):
    await quotation_service.update_particulars(quotation_id, particulars)
    return ApiResponse.on_success()


@router.get("/quotations/search/info",
            response_model=ApiResponse[List[QuotationRead]],
            summary="견적서 정보 조회",
            description="조건에 맞는 견적서를 조회 합니다. ( 조건 -> 시작일, 종료일, 검색어)")
@handle_exceptions(List[QuotationRead])
async def get_quotations_search(start: Optional[str] = Query(None, description="시작일('2024-01-01' 형식)"),
                                end: Optional[str] = Query(None, description="종료일('2024-01-01' 형식)"),
                                query: Optional[str] = Query(None, description="검색어"),
                                quotation_service: QuotationService = Depends(QuotationService)):
    quotations = await quotation_service.get_quotation_search(start, end, query)
    result = [to_quotation_read(quotation) for quotation in quotations]
    return ApiResponse[List[QuotationRead]].of(SuccessStatus.OK, result=result)


@router.get("/quotations/extract/{quotation_id}",
            summary="견적서 excel 파일로 추출",
            description="거래처 견적서를 excel 파일로 추출합니다.")
async def extract_quotations_to_excel_file(quotation_id: int,
                                           quotation_service: QuotationService = Depends(QuotationService)):
    output, filename = await quotation_service.extract_quotations(quotation_id, False)
    headers = {
        'Content-Disposition': f'attachment; filename*=UTF-8\'\'{filename}'
    }
    return StreamingResponse(output, headers=headers,
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@router.get("/quotations/extracts/today",
            summary="오늘 날짜의 모든 견적서 excel 파일로 추출",
            description="오늘 날짜의 모든 견적서를 excel 파일로 추출하고 zip으로 압축합니다.")
async def extract_today_quotations_to_zip(
        input_date: date,
        quotation_service: QuotationService = Depends(QuotationService)
):
    zip_buffer, filename = await quotation_service.extract_today_quotations_to_zip(input_date)

    headers = {
        'Content-Disposition': f'attachment; filename*=UTF-8\'\'{filename}'
    }

    return StreamingResponse(
        zip_buffer,
        headers=headers,
        media_type='application/zip'
    )

