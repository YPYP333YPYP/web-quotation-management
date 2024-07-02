from typing import List, Sequence

from fastapi import UploadFile, File, HTTPException, APIRouter, Depends, Form, Query
from starlette.responses import JSONResponse

from api.dependencies import get_current_user
from models import User
from models.product import Product
from schemas.product import ProductRead, ProductCreate
from service.product import ProductService

from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import GeneralException

router = APIRouter(tags=["product"])


@router.post("/products/upload",
             response_model=ApiResponse,
             summary="물건 견적서 파일 업로드",
             description="물건 견적서 excel 파일을 업로드해서 Product 모델로 저장합니다.")
async def upload_excel(file: UploadFile = File(...), product_service: ProductService = Depends(ProductService)):
    await product_service.upload_products(file)
    return ApiResponse.on_success()


@router.get("/products/{category}",
            response_model=ApiResponse[Sequence[ProductRead]],
            summary="분류 별 물품 조회",
            description="분류 별 물품을 조회 합니다. ")
async def get_products_by_category(category: str, product_service: ProductService = Depends(ProductService)):
    result = await product_service.get_products_by_category(category)
    if result is None or len(result) == 0:
        raise GeneralException(ErrorStatus.PRODUCT_NOT_FOUND)
    return ApiResponse[Sequence[ProductRead]].of(SuccessStatus.OK, result=result)


@router.put("/products/{product_id}/update",
            response_model=ApiResponse[ProductRead],
            summary="물품 수정",
            description="물품 번호에 해당하는 물품의 정보를 수정합니다.")
async def update_product(product_id: int, product_data: ProductCreate,
                         product_service: ProductService = Depends(ProductService)):
    new_data = product_data.dict()
    updated_product = await product_service.update_product(product_id, new_data)
    if updated_product:
        return ApiResponse[ProductRead].of(SuccessStatus.OK, result=updated_product)
    else:
        raise GeneralException(ErrorStatus.PRODUCT_NOT_FOUND)


@router.post("/products",
             response_model=ApiResponse,
             summary="물품 추가 생성",
             description="견적서 물품을 추가 생성 합니다.")
async def create_product(product: ProductCreate, product_service: ProductService = Depends(ProductService)):
    new_data = product.dict()
    await product_service.create_product(new_data)
    return ApiResponse.on_success()


@router.delete("/products/{product_id}/delete",
               response_model=ApiResponse,
               summary="물품 삭제",
               description="견적서 물품을 삭제 합니다.")
async def delete_product(product_id: int, product_service: ProductService = Depends(ProductService)):
    await product_service.delete_product(product_id)
    return ApiResponse.on_success()


@router.patch("/products/{product_id}/vegetable",
              response_model=ApiResponse,
              summary="vegetable(야채) 물품 가격 직접 변경",
              description="야채 물품의 가격을 직접 변경합니다.")
async def update_vegetable_product_price(product_id: int, price: int, product_service: ProductService = Depends(ProductService)):
    await product_service.update_vegetable_product_price(product_id, price)
    return ApiResponse.on_success()


@router.patch("/products/vegetable/file",
              response_model=ApiResponse,
              summary="vegetable(야채) 물품 가격 엑셀 파일로 변경",
              description="야채 물품의 가격을 엑셀 파일을 통해 변경합니다.")
async def update_vegetable_product_price(file: UploadFile = File(...), product_service: ProductService = Depends(ProductService)):
    await product_service.update_vegetable_product_price_from_file(file)
    return ApiResponse.on_success()


@router.get("/products/search/",
            response_model=ApiResponse[List[ProductRead]],
            summary="검색제안/자동완성 기능",
            description="검색어가 포함된 물품을 조회합니다.")
async def search_products_by_prefix(
    name_prefix: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=100),
    cached_time: int = Query(default=300),
    product_service: ProductService = Depends(ProductService),
    current_user: User = Depends(get_current_user)
):
    products = await product_service.search_products_by_prefix(current_user, name_prefix, limit, cached_time)
    if not products:
        raise GeneralException(ErrorStatus.PRODUCT_NOT_FOUND)
    return ApiResponse[List[ProductRead]].of(SuccessStatus.OK, result=products)



