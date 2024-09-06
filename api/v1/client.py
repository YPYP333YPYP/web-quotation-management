from datetime import datetime, timedelta, date
from typing import List
from fastapi import APIRouter, Depends, Query

from core.decorator.decorator import handle_exceptions
from models import User
from schemas.client import ClientRead, ClientCreate, DateRangeType, RegionType, ClientUpdate, ClientPaginatedResponse, \
    to_client_read, ClientCheckPreview
from schemas.past_order import PastOrderInfo
from schemas.quotation import QuotationRecentInfo
from service.client import ClientService
from api.dependencies import get_current_user
from service.past_order import PastOrderService
from service.quotation import QuotationService

from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import GeneralException

router = APIRouter(tags=["2. client"])

@router.get("/clients/all",
            response_model=ApiResponse[List[ClientRead]],
            summary="모든 거래처 정보 조회",
            description="모든 거래처 정보를 조회 합니다.")
@handle_exceptions(List[ClientRead])
async def get_clients_all(client_service: ClientService = Depends(ClientService),
                          current_user: User = Depends(get_current_user)):
    result = await client_service.get_clients_all()
    return result


@router.get("/clients/name/{name}",
            response_model=ApiResponse[List[ClientRead]],
            summary="거래처 명으로 조회",
            description="거래처 명으로 거래처를 조회 합니다.")
@handle_exceptions(List[ClientRead])
async def get_clients_by_name(name: str,
                              client_service: ClientService = Depends(ClientService),
                              current_user: User = Depends(get_current_user)):
    clients = await client_service.get_clients_by_name(name)
    result = [to_client_read(client) for client in clients]
    return result


@router.patch("/clients/{client_id}/region",
              response_model=ApiResponse,
              summary="거래처 지역 선택",
              description="거래처의 지역을 선택합니다.")
@handle_exceptions()
async def update_client_region(client_id: int,
                               region: RegionType,
                               client_service: ClientService = Depends(ClientService),
                               current_user: User = Depends(get_current_user)):
    await client_service.update_client_region(client_id, region)
    return ApiResponse.on_success()


@router.get("/clients/region",
            response_model=ApiResponse[List[ClientRead]],
            summary="거래처 지역으로 조회",
            description="거래처 지역으로 거래처를 조회 합니다.")
@handle_exceptions(List[ClientRead])
async def get_clients_by_region(region: RegionType,
                                client_service: ClientService = Depends(ClientService),
                                current_user: User = Depends(get_current_user)):
    clients = await client_service.get_clients_by_region(region)
    return clients


@router.post("/clients",
             response_model=ApiResponse,
             summary="거래처 생성",
             description="새로운 거래처를 생성합니다.")
@handle_exceptions()
async def create_client(client: ClientCreate,
                        client_service: ClientService = Depends(ClientService),
                        current_user: User = Depends(get_current_user)):
    await client_service.create_client(client, current_user.id)
    return ApiResponse.on_success()


@router.put("/clients/{client_id}/update",
            response_model=ApiResponse,
            summary="거래처 수정",
            description="거래처 정보를 수정합니다.")
@handle_exceptions()
async def update_client(client_id: int,
                        client: ClientUpdate,
                        client_service: ClientService = Depends(ClientService),
                        current_user: User = Depends(get_current_user)):
    await client_service.update_client(client_id, client)
    return ApiResponse.on_success()


@router.delete("/clients/{client_id}/delete",
               response_model=ApiResponse,
               summary="거래처 삭제",
               description="거래처를 삭제합니다.")
@handle_exceptions()
async def delete_client(client_id: int,
                        client_service: ClientService = Depends(ClientService),
                        current_user: User = Depends(get_current_user)):
    await client_service.delete_client(client_id)
    return ApiResponse.on_success()


@router.get("/clients/{client_id}/quotations",
            response_model=ApiResponse[ClientPaginatedResponse],
            summary="거래처 견적서 조회 ",
            description="거래처의 모든 견적서를 조회 합니다. page -> 페이지 시작 번호, page_size -> 페이지 당 반환 개수")
@handle_exceptions(ClientPaginatedResponse)
async def get_quotations(client_id: int, quotation_service: QuotationService = Depends(QuotationService),
                         page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100),
                         current_user: User = Depends(get_current_user)):
    quotations = await quotation_service.get_paginated_quotations_for_client(client_id, page, page_size)
    return quotations


@router.get("/clients/{client_id}/quotations/date",
            response_model=ApiResponse[ClientPaginatedResponse],
            summary="거래처 견적서 기간에 따른 조회 ",
            description="거래처의 기간 별 모든 견적서를 조회 합니다. page -> 페이지 시작 번호, page_size -> 페이지 당 반환 개수")
@handle_exceptions(ClientPaginatedResponse)
async def get_quotations(
        client_id: int,
        date_range_type: DateRangeType = Query(..., description="기간 옵션 선택 WEEK -> 일주일, MONTH -> 한달, CUSTOM -> 사용자 직접 입력"),
        start_date: datetime = Query(None, description="CUSTOM 선택 시 시작일 (YYYY-MM-DD)"),
        end_date: datetime = Query(None, description="CUSTOM 선택 시 종료일 (YYYY-MM-DD)"),
        page: int = Query(1, ge=1, description="페이지 번호"),
        page_size: int = Query(10, ge=1, le=100, description="페이지 사이즈"),
        quotation_service: QuotationService = Depends(QuotationService),
        current_user: User = Depends(get_current_user)
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
    return quotations


@router.get("/clients/{client_id}/past-order",
            response_model=ApiResponse[List[PastOrderInfo]],
            summary="거래처 주문 내역 조회",
            description="거래처 id로 정해둔 주문 내역을 조회합니다")
@handle_exceptions(List[PastOrderInfo])
async def get_past_order_by_client_id(client_id: int,
                                      past_order_service: PastOrderService = Depends(PastOrderService),
                                      current_user: User = Depends(get_current_user)):
    return await past_order_service.get_past_order_by_client_id(client_id)


@router.get("/clients/{client_id}/check",
            response_model=ApiResponse[ClientCheckPreview],
            summary="거래처 해당 날짜 견적서 제출 여부 파악",
            description="거래처의 해당 날짜의 견적서 제출 여부룰 조회 합니다.")
@handle_exceptions(ClientCheckPreview)
async def get_client_check_preview(client_id: int,
                                   input_date: date,
                                   client_service: ClientService = Depends(ClientService),
                                   current_user: User = Depends(get_current_user)):
    return await client_service.get_client_check_preview(client_id, input_date)


@router.patch("/clients/{client_id}/comment",
              response_model=ApiResponse,
              summary="거래처 특이사항 작성",
              description="거래처의 특이사항을 작성합니다.")
@handle_exceptions()
async def update_client_comment(client_id: int,
                                input_comment: str,
                                client_service: ClientService = Depends(ClientService),
                                current_user: User = Depends(get_current_user)):
    await client_service.update_client_comment(client_id, input_comment)
    return ApiResponse.on_success()


@router.get("/clients/{client_id}/recent/purchase",
            response_model=ApiResponse[List[QuotationRecentInfo]],
            summary="거래처의 최근 견적서 정보 조회",
            description="거래처의 최근에 작성한 견적서의 정보를 조회합니다.")
@handle_exceptions(List[QuotationRecentInfo])
async def get_client_quotation_info_recent(client_id: int,
                                           client_service: ClientService = Depends(ClientService),
                                           current_user: User = Depends(get_current_user)):
    result = await client_service.get_client_quotation_info_recent(client_id)
    return result


