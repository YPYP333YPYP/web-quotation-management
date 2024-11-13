from typing import Dict, Any

import httpx

from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import ServiceException
from schemas.kamis import KamisPeriodProductListParams, ReturnType


class KamisService:
    BASE_URL = "http://www.kamis.or.kr/service/price/xml.do"

    def __init__(self, cert_key:str, cert_id: str):
        self.cert_key = cert_key
        self.cert_id = cert_id

    async def build_period_product_list_params(self, params: KamisPeriodProductListParams) -> Dict[str, Any]:
        request_params = {
            "action": "periodProductList",
            "p_cert_key": params.cert_key,
            "p_cert_id": params.cert_id,
            "p_returntype": params.return_type.value,
            "p_productclscode": params.product_cls_code.value,
            "p_convert_kg_yn": params.convert_kg_yn
        }

        if params.start_date:
            request_params["p_startday"] = params.start_date.strftime("%Y-%m-%d")
        if params.end_date:
            request_params["p_endday"] = params.end_date.strftime("%Y-%m-%d")
        if params.item_category_code:
            request_params["p_itemcategorycode"] = params.item_category_code
        if params.item_code:
            request_params["p_itemcode"] = params.item_code
        if params.kind_code:
            request_params["p_kindcode"] = params.kind_code
        if params.product_rank_code:
            request_params["p_productrankcode"] = params.product_rank_code
        if params.country_code:
            request_params["p_countrycode"] = params.country_code

        return request_params

    async def get_period_product_list(self, params: KamisPeriodProductListParams) -> str | Any:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.BASE_URL,
                    params=await self.build_period_product_list_params(params)
                )
                response.raise_for_status()

                if params.return_type == ReturnType.JSON:
                    return response.json()
                return response.text

        except httpx.HTTPError as e:
            raise ServiceException(ErrorStatus.EXTERNAL_SERVICE_UNAVAILABLE)
