from datetime import datetime, date
from typing import Dict, List

from fastapi import Depends

from repository.statistic.statistic import StatisticsRepository
from schemas.statistic import DailyTotal


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

    async def get_daily_quotation_totals(self, start_date: date, end_date: date):
        daily_totals = await self.statistic_repository.get_daily_quotation_totals(start_date, end_date)
        total_sum = sum(total['total'] for total in daily_totals)
        average = total_sum / len(daily_totals)

        def determine_status(value):
            if value < average:
                return "하"
            elif value < 2 * average:
                return "중"
            else:
                return "상"

        result = [
            DailyTotal(
                date=total['date'],
                status=determine_status(total['total'])
            ) for total in daily_totals
        ]
        return result


