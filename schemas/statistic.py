from typing import List

from pydantic import BaseModel
from datetime import datetime, date


class ClientStatistics(BaseModel):
    id: int
    name: str
    total_quotations: int
    total_value: float


class ProductStatistics(BaseModel):
    id: int
    name: str
    quotation_count: int
    total_quantity: int
    total_value: float


class DailyTrend(BaseModel):
    date: datetime
    count: int
    total_value: float


class TopEntity(BaseModel):
    id: int
    name: str
    total_value: float


class OverallStatistics(BaseModel):
    client_statistics: List[ClientStatistics]
    product_statistics: List[ProductStatistics]
    daily_trend: List[DailyTrend]


class DailyTotal(BaseModel):
    date: date
    total: float
