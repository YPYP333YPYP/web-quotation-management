import os
from datetime import date
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from dotenv import load_dotenv

from schemas.kamis import KamisPeriodProductListParams, ProductClass
from service.kamis import KamisService

load_dotenv()


@pytest.mark.asyncio
async def test_kamis_price_service():
    """ Kamis 외부 API 테스트 함수"""
    cert_key = os.getenv('KAMIS_API_KEY')
    cert_id = os.getenv('KAMIS_ID')

    # Given
    service = KamisService(
        cert_key=cert_key,
        cert_id=cert_id
    )

    params = KamisPeriodProductListParams(
        cert_key=cert_key,
        cert_id=cert_id,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
        product_cls_code=ProductClass.RETAIL,
        item_category_code="100",
        country_code="1101"
    )

    # Mock the API response
    mock_response = {
        "price": [
            {
                "item_name": "쌀",
                "item_code": "111",
                "price": "55000"
            }
        ]
    }

    # When
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response_obj = MagicMock()
        mock_response_obj.status_code = 200
        mock_response_obj.json.return_value = mock_response

        mock_get.return_value = mock_response_obj
        result = await service.get_period_product_list(params)
        print(result)

    # Then
    assert result == mock_response
