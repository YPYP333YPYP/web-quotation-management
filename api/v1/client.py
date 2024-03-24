from typing import Sequence

from fastapi import APIRouter, Depends

from models import Client
from schemas.client import ClientRead
from service.client import ClientService

router = APIRouter(tags=["client"])


@router.get("/clients/name/{name}",
            response_model=Sequence[ClientRead],
            summary="거래처 명으로 조회",
            description="거래처 명으로 거래처를 조회 합니다.")
async def get_clients_by_name(name: str, client_service: ClientService = Depends(ClientService)) -> Sequence[
    ClientRead]:
    return await client_service.get_clients_by_name(name)


@router.get("/clients/region/{region}",
            response_model=Sequence[ClientRead],
            summary="거래처 지역으로 조회",
            description="거래처 지역으로 거래처를 조회 합니다.")
async def get_clients_by_region(region: str, client_service: ClientService = Depends(ClientService)) -> Sequence[
    ClientRead]:
    return await client_service.get_clients_by_region(region)
