from fastapi import APIRouter, Depends

from models.past_order import PastOrder
from schemas.past_order import PastOrderCreate
from service.past_order import PastOrderService

router = APIRouter(tags=["past_order"])


@router.post("/past-order",
             summary="주문 내역 생성",
             description="과거에 주문 했던 내역을 프레임 형태로 DB에 저장합니다.")
async def create_past_order(past_order_form: PastOrderCreate, product_service: PastOrderService = Depends(PastOrderService)):
    return await product_service.create_past_order(past_order_form)
