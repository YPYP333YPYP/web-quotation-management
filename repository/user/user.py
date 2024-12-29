import secrets
import hashlib

from fastapi import Depends
from sqlalchemy import update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.db.database import async_get_db
from core.decorator.decorator import handle_db_exceptions
from core.security import verify_password
from models.user import User
from core.security import get_password_hash


async def generate_dummy_password():
    dummy = secrets.token_hex(16)
    hashed_password = hashlib.sha256(dummy.encode()).hexdigest()
    return hashed_password


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

    @handle_db_exceptions()
    async def update_user_status(self, user_id: int, status: bool):
        async with self.session as session:
            update_stmt = (
                update(User)
                .where(User.id == user_id)
                .values(is_active=status, updated_at=func.now())
            )
            await session.execute(update_stmt)
            await session.commit()

    @handle_db_exceptions()
    async def check_password(self, user_id:int, password: str):
        async with self.session as session:
            stmt = select(User).filter(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            return verify_password(password, user.hashed_password)

    @handle_db_exceptions()
    async def get_user_by_email(self, email):
        async with self.session as session:
            stmt = select(User).filter(User.email == email)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            return user

    @handle_db_exceptions()
    async def create_kakao_user(self, kakao_id, email, nickname):
        async with self.session as session:

            dummy_password = get_password_hash(await generate_dummy_password())

            user = User(
                email=email,
                hashed_password=dummy_password,
                social=kakao_id,
                created_at=func.current_timestamp(),
                is_active=True,
                is_admin=False,
                client_id=None
            )

            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user
