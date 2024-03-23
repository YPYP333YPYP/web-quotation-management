from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from models import Client


class ClientRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def get_client_by_id(self, client_id: int) -> Optional[Client]:
        async with self.session as session:
            quotation = await session.get(Client, client_id)
            return quotation if quotation else None
