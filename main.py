import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from uvicorn import Config, Server

from api import router
from core.logging.config import listener
from core.response.handler.exception_handler import GeneralException, general_exception_handler, \
    validation_exception_handler
from core.middleware import RequestMiddleware, URLPatternCheckMiddleware
from service.discord import send_discord_startup_message, send_discord_shutdown_message

logger = logging.getLogger()


# 비동기 컨텍스트 관리자를 생성하는 데코레이터
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작 시 실행될 코드
    try:
        raise Exception("Test Error")
    except Exception as e:
        logging.error(f"Test error occurred: {str(e)}")
        print(f"Test error logged: {str(e)}")

    yield
    listener.stop()


def get_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(router)

    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_exception_handler(GeneralException, general_exception_handler)
    application.add_exception_handler(ResponseValidationError, validation_exception_handler)
    application.add_middleware(RequestMiddleware)
    application.add_middleware(
        URLPatternCheckMiddleware,
        url_pattern=r"^/api/v1/",
        excluded_paths=["/health", "/metrics", "/docs", "/openapi.json", "/favicon.ico"],
    )

    return application


app = get_application()


async def run_server():
    config = Config(app=app, host="127.0.0.1", port=8000, log_level="debug")
    server = Server(config=config)

    await send_discord_startup_message()

    await server.serve()

    await send_discord_shutdown_message()


if __name__ == "__main__":
    asyncio.run(run_server())