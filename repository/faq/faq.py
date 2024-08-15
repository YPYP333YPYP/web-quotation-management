from typing import Optional, List

from fastapi import Depends
from sqlalchemy import select, update, delete
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

    @handle_db_exceptions()
    async def get_all_faqs(self) -> List[FAQ]:
        async with self.session.begin as session:
            result = await session.execute(select(FAQ))
            return result.scalars().all()

    @handle_db_exceptions()
    async def update_faq(self, faq_id: int, faq_data: dict):
        async with self.session.begin as session:
            await session.execute(
                update(FAQ).where(FAQ.id == faq_id).values(**faq_data)
            )
            await session.commit()

    @handle_db_exceptions()
    async def delete_faq(self, faq_id: int):
        async with self.session.begin as session:
            await session.execute(
                delete(FAQ).where(FAQ.id == faq_id)
            )
            await session.commit()
