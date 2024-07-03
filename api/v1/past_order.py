from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.past_order import PastOrderCreate, PastOrderRead
from service.past_order import PastOrderService

router = APIRouter(tags=["past_order"])


@router.post("/past-order",
             response_model=ApiResponse,
             summary="주문 내역 생성",
             description="과거에 주문 했던 내역을 프레임 형태로 DB에 저장합니다.")
@handle_exceptions()
async def create_past_order(past_order_form: PastOrderCreate,
                            past_order_service: PastOrderService = Depends(PastOrderService)):
    await past_order_service.create_past_order(past_order_form)
    return ApiResponse.on_success()


@router.get("/past-order/{past_order_id}",
            response_model=ApiResponse[PastOrderRead],
            summary="주문 내역 불러오기",
            description="주문 내역 번호를 이용하여 주문 내역을 불러옵니다.")
@handle_exceptions(PastOrderRead)
async def get_past_order(past_order_id: int, past_order_service: PastOrderService = Depends(PastOrderService)):
    return await past_order_service.get_past_order(past_order_id)

