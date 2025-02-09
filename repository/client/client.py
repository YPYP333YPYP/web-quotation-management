from typing import Optional, Sequence, Dict, Any
from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models import Client, Quotation, User, PastOrder, QuotationProduct
from schemas.client import RegionType


class ClientRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def get_client_by_id(self, client_id: int) -> Optional[Client]:
        async with self.session as session:
            client = await session.get(Client, client_id)
            return client if client else None

    @handle_db_exceptions()
    async def get_clients_by_name(self, name: str) -> Sequence[Client]:
        async with self.session as session:
            stmt = select(Client).where(Client.name == name)
            result = await session.execute(stmt)
            clients = result.scalars().all()
            return clients

    @handle_db_exceptions()
    async def get_clients_by_region(self, region: str) -> Sequence[Client]:
        async with self.session as session:
            stmt = select(Client).where(Client.region == region)
            result = await session.execute(stmt)
            clients = result.scalars().all()
            return clients

    @handle_db_exceptions()
    async def create_client(self, client: Client):
        async with self.session as session:
            session.add(client)
            await session.commit()
            await session.refresh(client)
        return client

    @handle_db_exceptions()
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

    @handle_db_exceptions()
    async def delete_client_by_id(self, client_id: int):
        async with self.session as session:
            await session.execute(delete(QuotationProduct).where(QuotationProduct.quotation_id.in_(
                select(Quotation.id).where(Quotation.client_id == client_id)
            )))
            await session.execute(delete(Quotation).where(Quotation.client_id == client_id))
            await session.execute(delete(PastOrder).where(PastOrder.client_id == client_id))
            await session.execute(delete(User).where(User.client_id == client_id))

            await session.commit()

            stmt = select(Client).filter(Client.id == client_id)
            result = await session.execute(stmt)
            client = result.scalar_one_or_none()

            if client:
                await session.delete(client)
                await session.commit()

    @handle_db_exceptions()
    async def update_client_region(self, client_id: int, region: RegionType):
        async with self.session as session:
            stmt = select(Client).filter(Client.id == client_id)
            result = await session.execute(stmt)
            client = result.scalar_one_or_none()

            client.region = region.value
            await session.commit()

    @handle_db_exceptions()
    async def update_client_comment(self, client_id, input_comment):
        async with self.session as session:
            stmt = select(Client).filter(Client.id == client_id)
            result = await session.execute(stmt)
            client = result.scalar_one_or_none()

            client.comment = input_comment
            await session.commit()

    @handle_db_exceptions()
    async def get_clients_all(self):
        async with self.session as session:
            stmt = select(Client)
            result = await session.execute(stmt)
            clients = result.scalars()

            return clients
