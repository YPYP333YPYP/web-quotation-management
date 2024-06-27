from typing import List, Sequence

from fastapi import Depends

from models import Client
from repository.client.client import ClientRepository
from service.user import UserService


class ClientService:
    def __init__(self, client_repository: ClientRepository = Depends(ClientRepository),
                 user_service: UserService = Depends(UserService)):
        self.client_repository = client_repository
        self.user_service = user_service

    async def get_clients_by_name(self, name: str) -> Sequence[Client]:
        return await self.client_repository.get_clients_by_name(name)

    async def get_clients_by_region(self, region: str) -> Sequence[Client]:
        return await self.client_repository.get_clients_by_region(region)

    async def create_client(self, client_create, user_id):
        client_data = client_create.dict()
        client = Client(**client_data)

        response_client = await self.client_repository.create_client(client)
        await self.user_service.link_user_to_client(response_client.id, user_id)

    async def delete_client(self, client_id):
        return await self.client_repository.delete_client_by_id(client_id)

    async def update_client(self, client_id, client_update):
        client_data = client_update.dict()
        return await self.client_repository.update_client(client_id, client_data)
