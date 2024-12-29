import time
import logging

from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from functools import wraps
from typing import TypeVar, Type, Optional

from core.middleware import request_id_context, user_id_context, method_context, url_context, ip_context
from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import ServiceException, DatabaseException, GeneralException

T = TypeVar('T', bound=BaseModel)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def handle_exceptions(response_model: Optional[Type[T]] = None):
    """ Request에 대한 에러 발생 시 request 정보와 에러 정보를 로깅"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request_id = request_id_context.get()
            user_id = user_id_context.get()
            start_time = time.time()
            method = method_context.get()
            url = url_context.get()
            ip = ip_context.get()

            try:
                result = await func(*args, **kwargs)

                logger.info(
                    f"RequestID: {request_id} | UserID: {user_id} | IP: {ip} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Status: Success")

                if isinstance(result, ApiResponse):
                    return result
                elif response_model:
                    return ApiResponse[response_model].of(SuccessStatus.OK, result=result)
                else:
                    return ApiResponse.on_success()
            except GeneralException as e:
                logger.error(
                    f"RequestID: {request_id} | UserID: {user_id} | IP: {ip} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: GeneralException - {e.error_status.code} - {str(e)}")
                return ApiResponse.on_failure(e.error_status)
            except ServiceException as e:
                logger.error(
                    f"RequestID: {request_id} | UserID: {user_id} | IP: {ip} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: ServiceException - {e.error_status.code} - {str(e)}")
                return ApiResponse.on_failure(e.error_status)
            except DatabaseException as e:
                logger.error(
                    f"RequestID: {request_id} | UserID: {user_id} | IP: {ip} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: DatabaseException - {str(e)}")
                error_info = {
                    "type": "DATABASE ERROR",
                    "message": str(e)
                }
                return ApiResponse.on_failure(ErrorStatus.DB_ERROR, result=error_info)
            except Exception as e:
                logger.critical(
                    f"RequestID: {request_id} | UserID: {user_id} | IP: {ip} | Method: {method} | URL: {url} | Duration: {time.time() - start_time:.2f}s | Error: UnexpectedException - {type(e).__name__} - {str(e)}",
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
