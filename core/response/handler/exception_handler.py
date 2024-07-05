from fastapi import Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse
from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus


class GeneralException(Exception):
    def __init__(self, error_status: ErrorStatus):
        self.error_status = error_status


class ServiceException(Exception):
    def __init__(self, error_status: ErrorStatus):
        self.error_status = error_status


class DatabaseException(Exception):
    def __init__(self, error_status: str):
        self.error_status = error_status


async def general_exception_handler(request: Request, exc: GeneralException):
    return JSONResponse(
        status_code=int(exc.error_status.code),
        content=ApiResponse.on_failure(exc.error_status).dict(by_alias=True)
    )


async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    error_info = {
        "type": "VALIDATION ERROR",
        "message": str(exc),
        "details": exc.errors()
    }
    return JSONResponse(
        status_code=422,
        content=ApiResponse.on_failure(ErrorStatus.INVALID_OUTPUT, result=error_info).dict()
    )
