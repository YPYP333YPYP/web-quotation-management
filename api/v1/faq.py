from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.faq import FAQCreate
from service.faq import FAQService

router = APIRouter(tags=["9. faq"])


@router.post("/faqs",
             response_model=ApiResponse,
             summary="FAQ 생성",
             description="새로운 FAQ를 생성합니다.")
@handle_exceptions()
async def create_faq(faq_data: FAQCreate, faq_service: FAQService = Depends(FAQService)):
    await faq_service.create_faq(faq_data)
    return ApiResponse.on_success()