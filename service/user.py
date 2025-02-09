from datetime import datetime
from fastapi import Depends

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from core.security import get_password_hash, verify_password
from models import User
from repository.client.client import ClientRepository
from repository.user.user import UserRepository
from schemas.user import UserCreate, UserWithClient


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository),
                client_repository: ClientRepository = Depends(ClientRepository)):
        self.user_repository = user_repository
        self.client_repository = client_repository

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ServiceException(ErrorStatus.INVALID_CREDENTIALS)
        return user

    async def create_user(self, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            social=None,
            created_at=datetime.utcnow()

        )
        return await self.user_repository.create(db_user)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_by_email(email)

    async def change_user_password(self, user_id: int, current_password: str, new_password: str):
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ServiceException(ErrorStatus.USER_NOT_FOUND)

        if not verify_password(current_password, user.hashed_password):
            raise ServiceException(ErrorStatus.INVALID_PASSWORD)

        if current_password == new_password:
            raise ServiceException(ErrorStatus.PASSWORDS_MUST_BE_DIFFERENT)
        hashed_password = get_password_hash(new_password)
        await self.user_repository.update_user_password(user_id, hashed_password)

    async def link_user_to_client(self, client_id: int, user_id: int) -> None:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ServiceException(ErrorStatus.USER_NOT_FOUND)

        await self.user_repository.update_client_id(user_id, client_id)

    async def deactivate_user(self, current_user: User):
        user = await self.user_repository.get_by_id(current_user.id)
        if not user:
            raise ServiceException(ErrorStatus.USER_NOT_FOUND)

        await self.user_repository.update_user_status(current_user.id, False)

    async def activate_user(self, current_user: User):
        user = await self.user_repository.get_by_id(current_user.id)
        if not user:
            raise ServiceException(ErrorStatus.USER_NOT_FOUND)

        await self.user_repository.update_user_status(current_user.id, True)

    async def check_client_create(self, current_user: User) -> bool:
        if current_user.client_id is None:
            return False
        else:
            return True

    async def get_user_and_client_info(self, current_user: User):
        client = await self.client_repository.get_client_by_id(current_user.client_id)

        if not client:
            raise ServiceException(ErrorStatus.CLIENT_NOT_CREATED)

        if client.region is None:
            client.region = "미정"

        return UserWithClient(
            email=current_user.email,
            id=current_user.id,
            is_active=current_user.is_active,
            is_admin=current_user.is_admin,
            client_id=client.id,
            client_name=client.name,
            client_region=client.region,
            client_address=client.address
        )

    async def check_password(self, password: str, user: User):
        return await self.user_repository.check_password(user.id, password)

    async def kakao_login_or_signup(self, kakao_id: int, email: str, nickname: str) -> User:
        user = await self.user_repository.get_user_by_email(email)

        if not user:
            created_user = await self.user_repository.create_kakao_user(
                kakao_id=kakao_id,
                email=email,
                nickname=nickname
            )
            return created_user
        else:
            return user



