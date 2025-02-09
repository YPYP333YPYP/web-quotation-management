from typing import List
from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.faq import FAQCreate, FAQRead, FAQUpdate
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


@router.get("/faqs/{faq_id}",
            response_model=ApiResponse[FAQRead],
            summary="FAQ 조회",
            description="ID로 FAQ를 조회합니다.")
@handle_exceptions(FAQRead)
async def get_faq(faq_id: int, faq_service: FAQService = Depends(FAQService)):
    faq = await faq_service.get_faq_by_id(faq_id)
    return faq


@router.get("/faqs",
            response_model=ApiResponse[List[FAQRead]],
            summary="모든 FAQ 조회",
            description="모든 FAQ를 조회합니다.")
@handle_exceptions(List[FAQRead])
async def get_all_faqs(faq_service: FAQService = Depends(FAQService)):
    return await faq_service.get_all_faqs()


@router.put("/faqs/{faq_id}",
            response_model=ApiResponse,
            summary="FAQ 수정",
            description="FAQ를 수정합니다.")
@handle_exceptions()
async def update_faq(faq_id: int, faq_data: FAQUpdate, faq_service: FAQService = Depends(FAQService)):
    await faq_service.update_faq(faq_id, faq_data)
    return ApiResponse.on_success()


@router.delete("/faqs/{faq_id}",
               response_model=ApiResponse,
               summary="FAQ 삭제",
               description="FAQ를 삭제합니다.")
@handle_exceptions()
async def delete_faq(faq_id: int, faq_service: FAQService = Depends(FAQService)):
    await faq_service.delete_faq(faq_id)
    return ApiResponse.on_success()