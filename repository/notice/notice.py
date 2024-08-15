from typing import Optional, List, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models.notice import Notice


class NoticeRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def create_notice(self, notice: Notice) -> Notice:
        async with self.session as session:
            session.add(notice)
            await session.commit()
            await session.refresh(notice)
            return notice

    @handle_db_exceptions()
    async def get_notice_by_id(self, notice_id: int) -> Optional[Notice]:
        async with self.session as session:
            result = await session.execute(select(Notice).filter(Notice.id == notice_id))
            return result.scalar_one_or_none()

    @handle_db_exceptions()
    async def get_all_notices(self) -> Sequence[Notice]:
        async with self.session as session:
            result = await self.session.execute(select(Notice))
            return result.scalars().all()