from datetime import datetime

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
            return None
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