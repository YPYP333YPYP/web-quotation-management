from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.notice import NoticeCreate
from service.notice import NoticeService

router = APIRouter(tags=["8. notice"])


@router.post("/notices",
             response_model=ApiResponse,
             summary="공지사항 생성",
             description="새로운 공지사항을 생성합니다.")
@handle_exceptions()
async def create_notice(notice_data: NoticeCreate, notice_service: NoticeService = Depends(NoticeService)):
    await notice_service.create_notice(notice_data)
    return ApiResponse.on_success()

