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