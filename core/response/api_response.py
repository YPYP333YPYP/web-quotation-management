from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field

from core.response.code.base_code import BaseCode
from core.response.code.success_status import SuccessStatus

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    is_success: bool = Field(..., alias="isSuccess")
    code: str
    message: str
    category: str
    result: Optional[T] = None

    class Config:
        populate_by_name = True

    @classmethod
    def on_success(cls, result: T = None):
        return cls(
            isSuccess=True,
            code=SuccessStatus.OK.code,
            message=SuccessStatus.OK.message,
            category=SuccessStatus.OK.category,
            result=result
        )

    @classmethod
    def of(cls, code: BaseCode, result: T = None):
        return cls(
            isSuccess=True,
            code=code.code,
            message=code.message,
            category=code.category,
            result=result
        )

    @classmethod
    def on_failure(cls, code: BaseCode, result: T = None):
        return cls(
            isSuccess=False,
            code=code.code,
            message=code.message,
            category=code.category,
            result=result
        )