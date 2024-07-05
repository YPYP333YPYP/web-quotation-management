import time
import uuid
from functools import wraps
from typing import TypeVar, Type, Optional
import logging
from pydantic import BaseModel
from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode

from core.config import jwt_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import ServiceException, DatabaseException, GeneralException

T = TypeVar('T', bound=BaseModel)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)



def handle_exceptions(response_model: Optional[Type[T]] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            request_id = str(uuid.uuid4())

            start_time = time.time()

            user_id = 'anonymous'

            # todo 1 - 사용자 정보 가져 오는 방식 관련
            # try:
            #     token = await oauth2_scheme(request)
            #     payload = decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
            #     user_id = payload.get("sub_name")
            # except PyJWTError:
            #     logger.warning(f"Failed to decode token for request: {request_id}")

            method = request.method if request else 'Unknown'
            url = str(request.url) if request else 'Unknown'

            try:
                result = await func(*args, **kwargs)

                logger.info(
                    f"RequestID: {request_id} | UserID: {user_id} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Status: Success")

                if isinstance(result, ApiResponse):
                    return result
                elif response_model:
                    return ApiResponse[response_model].of(SuccessStatus.OK, result=result)
                else:
                    return ApiResponse.on_success()
            except GeneralException as e:
                logger.error(
                    f"RequestID: {request_id} | UserID: {user_id} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: GeneralException - {e.error_status.code} - {str(e)}")
                return ApiResponse.on_failure(e.error_status)
            except ServiceException as e:
                logger.error(
                    f"RequestID: {request_id} | UserID: {user_id} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: ServiceException - {e.error_status.code} - {str(e)}")
                return ApiResponse.on_failure(e.error_status)
            except DatabaseException as e:
                logger.error(
                    f"RequestID: {request_id} | UserID: {user_id} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: DatabaseException - {str(e)}")
                error_info = {
                    "type": "DATABASE ERROR",
                    "message": str(e)
                }
                return ApiResponse.on_failure(ErrorStatus.DB_ERROR, result=error_info)
            except Exception as e:
                logger.critical(
                    f"RequestID: {request_id} | UserID: {user_id} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: UnexpectedException - {type(e).__name__} - {str(e)}",
                    exc_info=True)
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
