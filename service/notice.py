from fastapi import Depends

from models.notice import Notice
from repository.notice.notice import NoticeRepository
from schemas.notice import NoticeCreate


class NoticeService:
    def __init__(self, notice_repository: NoticeRepository = Depends(NoticeRepository)):
        self.notice_repository = notice_repository

    async def create_notice(self, notice_data: NoticeCreate) -> Notice:
        notice = Notice(**notice_data.dict())
        return await self.notice_repository.create_notice(notice)