from functools import wraps
from sqlalchemy.exc import SQLAlchemyError


class DatabaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def handle_db_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as e:
            raise DatabaseError(str(e))
    return wrapper
