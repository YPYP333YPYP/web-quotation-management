from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.custom_product import CustomProductCreate
from service.custom_product import CustomProductService

router = APIRouter(tags=["custom_product"])


@router.post("/custom-products",
             response_model=ApiResponse,
             summary="자사 제품 생성",
             description="자사 제품을 생성합니다.")
@handle_exceptions()
async def create_custom_product(custom_product_form: CustomProductCreate,
                                custom_product_service: CustomProductService = Depends(CustomProductService)):
    return await custom_product_service.create_custom_product(custom_product_form)