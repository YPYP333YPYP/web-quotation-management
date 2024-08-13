from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta
from typing import List

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.statistic import TopEntity, OverallStatistics, DailyTotal
from service.statistic import StatisticsService

router = APIRouter(tags=["7. statistic"])


@router.get("/statistics",
            response_model=ApiResponse[OverallStatistics],
            summary="통계 가져오기",
            description="지정된 기간 동안의 전체 통계를 반환합니다.")
@handle_exceptions(OverallStatistics)
async def get_statistics(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    statistics_service: StatisticsService = Depends(StatisticsService)
):
    statistics = await statistics_service.get_overall_statistics(start_date, end_date)
    result = OverallStatistics(**statistics)
    return ApiResponse.on_success(result)


@router.get("/statistics/top-clients",
            response_model=ApiResponse[List[TopEntity]],
            summary="상위 고객 가져오기",
            description="지정된 기간 동안 상위 고객을 반환합니다.")
@handle_exceptions(List[TopEntity])
async def get_top_clients(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    limit: int = Query(5, ge=1, le=20),
    statistics_service: StatisticsService = Depends(StatisticsService)
):
    top_clients = await statistics_service.get_top_clients(start_date, end_date, limit)
    result = [TopEntity(**client) for client in top_clients]
    return result


@router.get("/statistics/top-products",
            response_model=ApiResponse[List[TopEntity]],
            summary="상위 제품 가져오기",
            description="지정된 기간 동안 상위 제품을 반환합니다.")
@handle_exceptions(List[TopEntity])
async def get_top_products(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    limit: int = Query(5, ge=1, le=20),
    statistics_service: StatisticsService = Depends(StatisticsService)
):
    top_products = await statistics_service.get_top_products(start_date, end_date, limit)
    result = [TopEntity(**product) for product in top_products]
    return ApiResponse.on_success(result)


@router.get("/statistics/daily-quotation-totals",
            response_model=ApiResponse[List[DailyTotal]],
            summary="일별 견적서 총액 가져오기",
            description="현재일부터 2달전까지의 견적서 일별 총액을 조회합니다.")
@handle_exceptions(List[DailyTotal])
async def get_daily_quotation_totals(
        statistics_service: StatisticsService = Depends(StatisticsService)
):

    end_date = datetime.now().date()
    start_date = (end_date.replace(day=1) - timedelta(days=1)).replace(day=1)

    daily_totals = await statistics_service.get_daily_quotation_totals(start_date, end_date)
    return ApiResponse.on_success(daily_totals)