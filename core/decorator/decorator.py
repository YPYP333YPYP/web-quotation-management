from functools import wraps
from typing import TypeVar, Type, Optional

from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import ServiceException


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


T = TypeVar('T', bound=BaseModel)


def handle_exceptions(response_model: Optional[Type[T]] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                if isinstance(result, ApiResponse):
                    return result
                elif response_model:
                    return ApiResponse[response_model].of(SuccessStatus.OK, result=result)
                else:
                    return ApiResponse.on_success()
            except ServiceException as e:
                return ApiResponse.on_failure(e.error_status)
            except ValueError as e:
                return ApiResponse.on_failure(ErrorStatus.INVALID_INPUT)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return ApiResponse.on_failure(e.error_status)
        return wrapper
    return decorator