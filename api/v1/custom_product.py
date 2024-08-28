from typing import List

from fastapi import APIRouter, Depends

from api.dependencies import get_current_user
from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from models import User
from schemas.custom_product import CustomProductCreate, CustomProductRead, CustomProductUpdate
from service.custom_product import CustomProductService

router = APIRouter(tags=["6. custom_product"])


@router.post("/custom-products",
             response_model=ApiResponse,
             summary="자사 제품 생성",
             description="자사 제품을 생성합니다.")
@handle_exceptions()
async def create_custom_product(custom_product_form: CustomProductCreate,
                                custom_product_service: CustomProductService = Depends(CustomProductService),
                                current_user: User = Depends(get_current_user)):
    await custom_product_service.create_custom_product(custom_product_form)


@router.post("/custom-products/bulk",
             response_model=ApiResponse,
             summary="자사 제품 여러 개 생성",
             description="자사 제품을 여러 개 생성합니다.")
@handle_exceptions()
async def create_custom_product(custom_product_form: List[CustomProductCreate],
                                custom_product_service: CustomProductService = Depends(CustomProductService),
                                current_user: User = Depends(get_current_user)):
    await custom_product_service.create_custom_product_bulk(custom_product_form)

@router.get("/custom-products/{custom_product_id}",
            response_model=ApiResponse[CustomProductRead],
            summary="자사 제품 조회",
            description="자사 제품을 조회합니다.")
@handle_exceptions(CustomProductRead)
async def get_custom_product(custom_product_id: int,
                             custom_product_service: CustomProductService = Depends(CustomProductService)):
    return await custom_product_service.get_custom_product(custom_product_id)


@router.put("/custom-products/{custom_product_id}/update",
            response_model=ApiResponse,
            summary="자사 제품 수정",
            description="자사 제품을 수정합니다.")
@handle_exceptions()
async def update_custom_product(custom_product_id: int, update_data: CustomProductUpdate,
                                custom_product_service: CustomProductService = Depends(CustomProductService),
                                current_user: User = Depends(get_current_user)):
    return await custom_product_service.update_custom_product(custom_product_id, update_data)


@router.delete("/custom-products/{custom_product_id}/delete",
               response_model=ApiResponse,
               summary="자사 제품 삭제",
               description="자사 제품을 삭제합니다.")
@handle_exceptions()
async def delete_custom_product(custom_product_id: int,
                                custom_product_service: CustomProductService = Depends(CustomProductService),
                                current_user: User = Depends(get_current_user)):
    await custom_product_service.delete_custom_product(custom_product_id)


@router.get("/custom-products",
            response_model=ApiResponse[list[CustomProductRead]],
            summary="모든 자사 제품 조회",
            description="모든 자사 제품을 조회합니다.")
@handle_exceptions(list[CustomProductRead])
async def get_all_custom_products(custom_product_service: CustomProductService = Depends(CustomProductService)):
    return await custom_product_service.get_all_custom_products()