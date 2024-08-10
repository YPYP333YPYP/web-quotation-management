import re
import jwt
import uuid
import os
import dotenv
import sentry_sdk

from fastapi import Request, FastAPI
from jwt import InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar
from starlette.responses import JSONResponse
from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException
from sentry_sdk.integrations.fastapi import FastApiIntegration

from core.utils import get_user_id_from_token, load_blacklist
from service.discord import send_discord_alert

dotenv.load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()]
)

request_id_context = ContextVar("request_id", default=None)
user_id_context = ContextVar("user_id", default=None)
method_context = ContextVar("method", default=None)
url_context = ContextVar("url", default=None)
ip_context = ContextVar("ip", default=None)


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

        client_ip = request.client.host
        ip_context.set(client_ip)

        response = await call_next(request)
        return response


class URLPatternCheckMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            url_pattern: str = r"^/api/v1/",
            excluded_paths: list = None,
            discord_webhook_url: str = os.getenv("DISCORD_WEB_HOOK")
    ):
        super().__init__(app)
        self.url_pattern = url_pattern
        self.excluded_paths = excluded_paths or []
        self.discord_webhook_url = discord_webhook_url

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path == "" or path == "/":
            return await call_next(request)

        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return await call_next(request)

        if not re.match(self.url_pattern, path):
            error_message = f"잘못된 접근 경고: {path}"
            sentry_sdk.capture_message(error_message, level="error")

            if self.discord_webhook_url:
                await send_discord_alert(self.discord_webhook_url, error_message)

            return JSONResponse(status_code=404, content={"error": "Not Found"})

        response = await call_next(request)
        return response


class BlacklistMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, blacklist_file: str = "blacklist.txt"):
        super().__init__(app)
        self.blacklist_patterns = load_blacklist(blacklist_file)

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        for pattern in self.blacklist_patterns:
            if re.match(pattern, path):
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Access to this resource is forbidden."}
                )
        response = await call_next(request)
        return response