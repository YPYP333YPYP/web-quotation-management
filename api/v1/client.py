from typing import Sequence

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from schemas.client import ClientRead, ClientUpdate, ClientCreate
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


@router.post("/clients/",
             summary="거래처 생성",
             description="새로운 거래처를 생성합니다.")
async def create_client(client: ClientCreate, client_service: ClientService = Depends(ClientService)):
    await client_service.create_client(client)
    return JSONResponse(content={"message": "Create successful"})


@router.put("/clients/{client_id}/update",
            summary="거래처 수정",
            description="거래처 정보를 수정합니다.")
async def update_client(client_id: int, client: ClientUpdate, client_service: ClientService = Depends(ClientService)):
    await client_service.update_client(client_id, client)
    return JSONResponse(content={"message": "Update successful"})


@router.delete("/clients/{client_id}/delete",
               summary="거래처 삭제",
               description="거래처를 삭제합니다.")
async def delete_client(client_id: int, client_service: ClientService = Depends(ClientService)):
    await client_service.delete_client(client_id)
    return JSONResponse(content={"message": "Delete successful"})


