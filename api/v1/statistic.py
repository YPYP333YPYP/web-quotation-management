from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import List

from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from schemas.statistic import TopEntity, OverallStatistics
from service.statistic import StatisticsService

router = APIRouter(tags=["statistic"])


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

