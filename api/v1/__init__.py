from fastapi import APIRouter
from .product import router as product_router
from .quotation import router as quotation_router
from .client import router as client_router
from .auth import router as auth_router
from .past_order import router as past_order_router
from .statistic import router as statistic_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(client_router)
router.include_router(product_router)
router.include_router(quotation_router)
router.include_router(past_order_router)
router.include_router(statistic_router)
