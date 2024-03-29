from fastapi import APIRouter
from .product import router as product_router
from .quotation import router as quotation_router
from .client import router as client_router

router = APIRouter(prefix="/v1")

router.include_router(product_router)
router.include_router(quotation_router)
router.include_router(client_router)