from datetime import datetime, timedelta
from typing import Sequence
from fastapi import APIRouter, Depends, Query

from models import User
from schemas.client import ClientRead, ClientCreate, DateRangeType, RegionType, ClientUpdate, ClientPaginatedResponse
from service.client import ClientService
from api.dependencies import get_current_user
from service.quotation import QuotationService

from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import GeneralException

router = APIRouter(tags=["client"])


@router.get("/clients/name/{name}",
            response_model=ApiResponse[Sequence[ClientRead]],
            summary="거래처 명으로 조회",
            description="거래처 명으로 거래처를 조회 합니다.")
async def get_clients_by_name(name: str, client_service: ClientService = Depends(ClientService)):
    clients = await client_service.get_clients_by_name(name)
    return ApiResponse[Sequence[ClientRead]].of(SuccessStatus.OK, result=clients)


@router.get("/clients/region",
            response_model=ApiResponse[Sequence[ClientRead]],
            summary="거래처 지역으로 조회",
            description="거래처 지역으로 거래처를 조회 합니다.")
async def get_clients_by_region(region: RegionType,
                                client_service: ClientService = Depends(ClientService)):
    clients = await client_service.get_clients_by_region(region)
    return ApiResponse[Sequence[ClientRead]].of(SuccessStatus.OK, result=clients)


@router.post("/clients",
             response_model=ApiResponse,
             summary="거래처 생성",
             description="새로운 거래처를 생성합니다.")
async def create_client(client: ClientCreate, client_service: ClientService = Depends(ClientService),
                        current_user: User = Depends(get_current_user)):
    await client_service.create_client(client, current_user.id)
    return ApiResponse.on_success()


@router.put("/clients/{client_id}/update",
            response_model=ApiResponse,
            summary="거래처 수정",
            description="거래처 정보를 수정합니다.")
async def update_client(client_id: int, client: ClientUpdate, client_service: ClientService = Depends(ClientService)):
    await client_service.update_client(client_id, client)
    return ApiResponse.on_success()


@router.delete("/clients/{client_id}/delete",
               response_model=ApiResponse,
               summary="거래처 삭제",
               description="거래처를 삭제합니다.")
async def delete_client(client_id: int, client_service: ClientService = Depends(ClientService)):
    await client_service.delete_client(client_id)
    return ApiResponse.on_success()


@router.get("/clients/{client_id}/quotations",
            response_model=ApiResponse[ClientPaginatedResponse],
            summary="거래처 견적서 조회 ",
            description="거래처의 모든 견적서를 조회 합니다. page -> 페이지 시작 번호, page_size -> 페이지 당 반환 개수")
async def get_quotations(client_id: int, quotation_service: QuotationService = Depends(QuotationService),
                         page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100)):
    quotations = await quotation_service.get_paginated_quotations_for_client(client_id, page, page_size)
    return ApiResponse[ClientPaginatedResponse].of(SuccessStatus.OK, result=quotations)


@router.get("/clients/{client_id}/quotations/date",
            response_model=ApiResponse[ClientPaginatedResponse],
            summary="거래처 견적서 기간에 따른 조회 ",
            description="거래처의 기간 별 모든 견적서를 조회 합니다. page -> 페이지 시작 번호, page_size -> 페이지 당 반환 개수")
async def get_quotations(
        client_id: int,
        date_range_type: DateRangeType = Query(..., description="기간 옵션 선택 WEEK -> 일주일, MONTH -> 한달, CUSTOM -> 사용자 직접 입력"),
        start_date: datetime = Query(None, description="CUSTOM 선택 시 시작일 (YYYY-MM-DD)"),
        end_date: datetime = Query(None, description="CUSTOM 선택 시 종료일 (YYYY-MM-DD)"),
        page: int = Query(1, ge=1, description="페이지 번호"),
        page_size: int = Query(10, ge=1, le=100, description="페이지 사이즈"),
        quotation_service: QuotationService = Depends(QuotationService)
):
    today = datetime.now().date()

    if date_range_type == DateRangeType.WEEK:
        start_date = today - timedelta(days=7)
        end_date = today
    elif date_range_type == DateRangeType.MONTH:
        start_date = today.replace(day=1)
        end_date = today
    elif date_range_type == DateRangeType.CUSTOM:
        if not start_date or not end_date:
            raise GeneralException(ErrorStatus.REQUIRED_FIELD_MISSING)
        start_date = start_date.date()
        end_date = end_date.date()

    quotations = await quotation_service.get_paginated_quotations_by_date_range(client_id, start_date, end_date, page,
                                                                                page_size)
    return ApiResponse[ClientPaginatedResponse].of(SuccessStatus.OK, result=quotations)

