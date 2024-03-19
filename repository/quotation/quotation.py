from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.database import async_get_db
from models import Quotation


class QuotationRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def create_quotation(self, quotation: Quotation):
        self.session.add(quotation)