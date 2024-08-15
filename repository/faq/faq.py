from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models import FAQ


class FAQRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def create_faq(self, faq: FAQ):
        async with self.session.begin as session:
            session.add(faq)
            await session.commit()
            await session.refresh(faq)

    @handle_db_exceptions()
    async def get_faq_by_id(self, faq_id: int) -> Optional[FAQ]:
        async with self.session.begin as session:
            result = await session.execute(select(FAQ).filter(FAQ.id == faq_id))
            return result.scalar_one_or_none()