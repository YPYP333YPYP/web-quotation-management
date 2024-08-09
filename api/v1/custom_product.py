from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.custom_product import CustomProductCreate, CustomProductRead, CustomProductUpdate
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


@router.get("/custom-products/{custom_product_id}",
            response_model=ApiResponse[CustomProductRead],
            summary="자사 제품 조회",
            description="자사 제품을 조회합니다.")
@handle_exceptions(CustomProductRead)
async def get_custom_product(custom_product_id: int,
                             custom_product_service: CustomProductService = Depends(CustomProductService)):
    return await custom_product_service.get_custom_product(custom_product_id)


@router.put("/custom-products/{custom_product_id}/update",
            response_model=CustomProductRead,
            summary="자사 제품 수정",
            description="자사 제품을 수정합니다.")
async def update_custom_product(custom_product_id: int, update_data: CustomProductUpdate,
                                custom_product_service: CustomProductService = Depends(CustomProductService)):
    return await custom_product_service.update_custom_product(custom_product_id, update_data)