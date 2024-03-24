from typing import Optional, List, Sequence, Dict, Any

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from models import Client


class ClientRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    async def get_client_by_id(self, client_id: int) -> Optional[Client]:
        async with self.session as session:
            client = await session.get(Client, client_id)
            return client if client else None

    async def get_clients_by_name(self, name: str) -> Sequence[Client]:
        async with self.session as session:
            stmt = select(Client).where(Client.name == name)
            result = await session.execute(stmt)
            clients = result.scalars().all()
            return clients

    async def get_clients_by_region(self, region: str) -> Sequence[Client]:
        async with self.session as session:
            stmt = select(Client).where(Client.region == region)
            result = await session.execute(stmt)
            clients = result.scalars().all()
            return clients

    async def create_client(self, client: Client):
        self.session.add(client)

    async def update_client(self, client_id: int, new_data: Dict[str, Any]):
        async with self.session as session:
            client = await session.get(Client, client_id)
            if client:
                for key, value in new_data.items():
                    setattr(client, key, value)
                await session.commit()
                return True
            else:
                return False

    async def delete_client_by_id(self, client_id: int):
        async with self.session as session:
            stmt = select(Client).filter(Client.id == client_id)
            result = await session.execute(stmt)
            client = result.scalar_one_or_none()

            if client:
                await session.delete(client)
                await session.commit()