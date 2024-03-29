from typing import List, Sequence

from fastapi import UploadFile, File, HTTPException, APIRouter, Depends, Form
from starlette.responses import JSONResponse

from models.product import Product
from schemas.product import ProductRead, ProductCreate
from service.product import ProductService

router = APIRouter(tags=["product"])


@router.post("/products/upload",
             summary="물건 견적서 파일 업로드",
             description="물건 견적서 excel 파일을 업로드해서 Product 모델로 저장합니다.")
async def upload_excel(file: UploadFile = File(...), product_service: ProductService = Depends(ProductService)):
    try:
        await product_service.upload_products(file)
        return JSONResponse(content={"message": "Upload successful"})
    except HTTPException as e:
        raise e


@router.get("/products/{category}",
            response_model=Sequence[ProductRead],
            summary="분류 별 물품 조회",
            description="분류 별 물품을 조회 합니다. ")
async def get_products_by_category(category: str, product_service: ProductService = Depends(ProductService)) -> \
        Sequence[Product]:
    result = await product_service.get_products_by_category(category)
    if result is None or len(result) == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@router.put("/products/{product_id}/update",
            response_model=ProductRead,
            summary="물품 수정",
            description="물품 번호에 해당하는 물품의 정보를 수정합니다.")
async def update_product(product_id: int, product_data: ProductCreate,
                         product_service: ProductService = Depends(ProductService)) -> ProductRead:
    new_data = product_data.dict()
    updated_product = await product_service.update_product(product_id, new_data)
    if updated_product:
        return updated_product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.post("/products/",
             summary="물품 추가 생성",
             description="견적서 물품을 추가 생성 합니다.")
async def create_product(product: ProductCreate, product_service: ProductService = Depends(ProductService)):
    new_data = product.dict()
    await product_service.create_product(new_data)
    return JSONResponse(content={"message": "Create successful"})


@router.delete("/products/{product_id}/delete",
               summary="물품 삭제",
               description="견적서 물품을 삭제 합니다.")
async def delete_product(product_id: int, product_service: ProductService = Depends(ProductService)):
    await product_service.delete_product(product_id)
    return JSONResponse(content={"message": "Delete successful"})
