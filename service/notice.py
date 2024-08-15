from typing import Optional, List, Sequence

from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from models.notice import Notice
from repository.notice.notice import NoticeRepository
from schemas.notice import NoticeCreate


class NoticeService:
    def __init__(self, notice_repository: NoticeRepository = Depends(NoticeRepository)):
        self.notice_repository = notice_repository

    async def create_notice(self, notice_data: NoticeCreate) -> Notice:
        notice = Notice(**notice_data.dict())
        return await self.notice_repository.create_notice(notice)

    async def get_notice_by_id(self, notice_id: int) -> Optional[Notice]:

        notice = await self.notice_repository.get_notice_by_id(notice_id)
        if not notice:
            raise ServiceException(ErrorStatus.NOTICE_NOT_FOUND)
        return notice

    async def get_all_notices(self) -> Sequence[Notice]:
        return await self.notice_repository.get_all_notices()
