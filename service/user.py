from datetime import datetime

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from core.security import get_password_hash, verify_password
from fastapi import Depends
from models.user import User
from repository.user.user import UserRepository
from schemas.user import UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository = Depends(UserRepository)):
        self.user_repository = user_repository

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

