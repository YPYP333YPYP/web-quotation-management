from typing import List, Sequence

from fastapi import Depends

from models import Client
from repository.client.client import ClientRepository


class ClientService:
    def __init__(self, client_repository: ClientRepository = Depends(ClientRepository)):
        self.client_repository = client_repository

    async def get_clients_by_name(self, name: str) -> Sequence[Client]:
        return await self.client_repository.get_clients_by_name(name)

    async def get_clients_by_region(self, region: str) -> Sequence[Client]:
        return await self.client_repository.get_clients_by_region(region)

    async def create_client(self, client_create):
        client_data = client_create.dict()
        client = Client(**client_data)
        return await self.client_repository.create_client(client)

    async def delete_client(self, client_id):
        return await self.client_repository.delete_client_by_id(client_id)

    async def update_client(self, client_id, client_update):
        client_data = client_update.dict()
        return await self.client_repository.update_client(client_id, client_data)
