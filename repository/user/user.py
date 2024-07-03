from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession = Depends(async_get_db)):
        self.session = session

    @handle_db_exceptions()
    async def get_by_id(self, user_id: int) -> User | None:
        async with self.session as session:
            result = await session.execute(select(User).filter(User.id == user_id))
            return result.scalars().first()

    @handle_db_exceptions()
    async def get_by_email(self, email: str) -> User | None:
        async with self.session as session:
            result = await session.execute(select(User).filter(User.email == email))
            return result.scalars().first()

    @handle_db_exceptions()
    async def create(self, user: User) -> User:
        async with self.session as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @handle_db_exceptions()
    async def update_user_password(self, user_id: int, hashed_password: str):
        async with self.session as session:
            async with session.begin():
                user = await session.get(User,user_id)
                if user:
                    user.hashed_password = hashed_password
                    await session.commit()

    @handle_db_exceptions()
    async def update_client_id(self, user_id: int, client_id: int) -> None:
        async with self.session as session:
            query = update(User).where(User.id == user_id).values(client_id=client_id)
            await session.execute(query)
            await session.commit()