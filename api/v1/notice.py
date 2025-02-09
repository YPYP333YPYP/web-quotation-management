from typing import List
from fastapi import APIRouter, Depends

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.notice import NoticeCreate, NoticeRead, NoticeUpdate
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
            response_model=ApiResponse[NoticeRead],
            summary="공지사항 조회",
            description="ID로 공지사항을 조회합니다.")
@handle_exceptions(NoticeRead)
async def get_notice(notice_id: int, notice_service: NoticeService = Depends(NoticeService)):
    notice = await notice_service.get_notice_by_id(notice_id)
    return notice


@router.get("/notices",
            response_model=ApiResponse[List[NoticeRead]],
            summary="모든 공지사항 조회",
            description="모든 공지사항을 조회합니다.")
@handle_exceptions(List[NoticeRead])
async def get_all_notices(notice_service: NoticeService = Depends(NoticeService)):
    return await notice_service.get_all_notices()


@router.put("/notices/{notice_id}",
            response_model=ApiResponse,
            summary="공지사항 수정",
            description="공지사항을 수정합니다.")
@handle_exceptions()
async def update_notice(notice_id: int, notice_data: NoticeUpdate, notice_service: NoticeService = Depends(NoticeService)):
    await notice_service.update_notice(notice_id, notice_data)
    return ApiResponse.on_success()


@router.delete("/notices/{notice_id}",
               response_model=ApiResponse,
               summary="공지사항 삭제",
               description="공지사항을 삭제합니다.")
@handle_exceptions()
async def delete_notice(notice_id: int, notice_service: NoticeService = Depends(NoticeService)):
    await notice_service.delete_notice(notice_id)
    return ApiResponse.on_success()