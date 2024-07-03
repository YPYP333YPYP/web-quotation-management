from functools import wraps
from typing import TypeVar, Type, Optional

from fastapi.exceptions import ResponseValidationError
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError

from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import ServiceException, DatabaseException

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
            except DatabaseException as e:
                error_info = {
                    "type": "DATABASE ERROR",
                    "message": str(e)
                }
                return ApiResponse.on_failure(ErrorStatus.DB_ERROR, result=error_info)
            except Exception as e:
                error_info = {
                    "type": "INTERNAL ERROR",
                    "message": str(e)
                }
                return ApiResponse.on_failure(ErrorStatus.INTERNAL_SERVER_ERROR, result=error_info)
        return wrapper
    return decorator


def handle_db_exceptions():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                raise DatabaseException(str(e))
        return wrapper
    return decorator
