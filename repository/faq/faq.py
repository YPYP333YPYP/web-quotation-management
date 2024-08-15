from fastapi import Depends
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
