from fastapi import UploadFile, File, HTTPException, APIRouter, Depends
from starlette.responses import JSONResponse

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
