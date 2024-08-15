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


@router.get("/notices/{notice_id}",
            response_model=NoticeRead,
            summary="공지사항 조회",
            description="ID로 공지사항을 조회합니다.")
async def get_notice(notice_id: int, notice_service: NoticeService = Depends(NoticeService)):
    notice = await notice_service.get_notice_by_id(notice_id)
    return notice