from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any
from enum import Enum


class ProductClass(Enum):
    RETAIL = "01"    # 소매
    WHOLESALE = "02" # 도매


class ReturnType(Enum):
    JSON = "json"
    XML = "xml"


@dataclass
class KamisPeriodProductListParams:
    cert_key: str
    cert_id: str
    return_type: ReturnType = ReturnType.JSON
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    product_cls_code: ProductClass = ProductClass.WHOLESALE
    item_category_code: Optional[str] = None
    item_code: Optional[str] = None
    kind_code: Optional[str] = None
    product_rank_code: Optional[str] = None
    country_code: Optional[str] = None
    convert_kg_yn: str = "N"