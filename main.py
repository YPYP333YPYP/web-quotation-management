from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from api import router
from core.response.handler.exception_handler import GeneralException, general_exception_handler


def get_application() -> FastAPI:
    application = FastAPI()
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

    return application


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")