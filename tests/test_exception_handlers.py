from fastapi.testclient import TestClient

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException
from main import app

client = TestClient(app)


def test_general_exception_handler():
    """ General Exception Handler 테스트 함수"""
    @app.get("/test-general-exception")
    async def raise_general_exception():
        raise GeneralException(ErrorStatus.NOT_FOUND)

    response = client.get("/test-general-exception")
    assert response.status_code == 1003

