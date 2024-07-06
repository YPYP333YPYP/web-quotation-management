import os

import jwt
from fastapi import Request
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar
import uuid
import dotenv

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException

request_id_context = ContextVar("request_id", default=None)
user_id_context = ContextVar("user_id", default=None)
method_context = ContextVar("method", default=None)
url_context = ContextVar("url", default=None)

dotenv.load_dotenv()


def get_user_id_from_token(token):
    if not token:
        return None

    try:
        secret_key = os.environ.get("SECRET_KEY")
        algorithm = os.environ.get("ALGORITHM")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get('user_id')

        return user_id
    except InvalidTokenError:
        raise GeneralException(ErrorStatus.INVALID_TOKEN)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_context.set(request_id)
        token = request.headers.get("access-token")
        user_id = get_user_id_from_token(token)

        if user_id:
            user_id_context.set(user_id)

        method_context.set(request.method)
        url_context.set(str(request.url))

        response = await call_next(request)
        return response
