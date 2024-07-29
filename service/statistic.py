from datetime import datetime
from typing import Dict, List

from fastapi import Depends

from repository.statistic.statistic import StatisticsRepository


class StatisticsService:
    def __init__(self, statistic_repository: StatisticsRepository = Depends(StatisticsRepository)):
        self.statistic_repository = statistic_repository

    async def get_overall_statistics(self, start_date: datetime, end_date: datetime) -> Dict:
        return {
            "client_statistics": await self.statistic_repository.get_client_statistics(start_date, end_date),
            "product_statistics": await self.statistic_repository.get_product_statistics(start_date, end_date),
            "daily_trend": await self.statistic_repository.get_daily_quotation_trend(start_date, end_date)
        }

    async def get_top_clients(self, start_date: datetime, end_date: datetime, limit: int = 5) -> List[Dict]:
        client_stats = await self.statistic_repository.get_client_statistics(start_date, end_date)
        return sorted(client_stats, key=lambda x: x['total_value'], reverse=True)[:limit]

    async def get_top_products(self, start_date: datetime, end_date: datetime, limit: int = 5) -> List[Dict]:
        product_stats = await self.statistic_repository.get_product_statistics(start_date, end_date)
        return sorted(product_stats, key=lambda x: x['total_value'], reverse=True)[:limit]


