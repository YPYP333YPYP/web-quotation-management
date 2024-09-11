from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_current_user
from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException
from core.security import create_access_token, create_refresh_token, refresh_access_token
from models.user import User
from schemas.user import UserCreate, UserInDB, UserWithClient
from schemas.auth import Token, PasswordChange
from service.user import UserService

router = APIRouter(tags=["1. auth"])


@router.post("/token",
             response_model=ApiResponse[Token],
             summary="액세스 토큰 발급",
             description="사용자 로그인 시 토큰을 발급합니다.")
@handle_exceptions(Token)
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        user_service: UserService = Depends(UserService)
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise GeneralException(ErrorStatus.INVALID_CREDENTIALS)
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.email, "user_id": user.id})
    token_info = Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    return token_info


@router.post("/token/refresh",
             response_model=ApiResponse[Token],
             summary="액세스 토큰 재발급",
             description="리프레시 토큰으로 액세스 토큰을 재발급 받습니다.")
@handle_exceptions(Token)
async def refresh_token(refresh_token: str,
                        current_user: User = Depends(get_current_user)):
    new_access_token = refresh_access_token(refresh_token)
    new_refresh_token = create_refresh_token(data={"sub": current_user.email, "user_id": current_user.id})

    token_info = Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
    return token_info


@router.post("/users",
             response_model=ApiResponse[UserInDB],
             summary="유저 회원 가입",
             description="사용자 정보를 받아 회원 가입을 진행합니다.")
@handle_exceptions(UserInDB)
async def create_user(
        user: UserCreate,
        user_service: UserService = Depends(UserService)
):
    db_user = await user_service.get_user_by_email(user.email)
    if db_user:
        raise GeneralException(ErrorStatus.USER_ALREADY_EXISTS)
    return await user_service.create_user(user)


@router.get("/users/me",
            response_model=ApiResponse[UserWithClient],
            summary="내 정보 조회",
            description="내 정보를 조회 합니다.")
@handle_exceptions(UserWithClient)
async def read_users_me(current_user: User = Depends(get_current_user),
                        user_service: UserService = Depends(UserService)):
    result = await user_service.get_user_and_client_info(current_user)
    return result


@router.put("/users/me/password",
            response_model=ApiResponse,
            summary="비밀번호 변경",
            description="비밀번호를 변경 합니다.")
@handle_exceptions()
async def change_password(
        password_change: PasswordChange,
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(UserService)
):
    try:
        await user_service.change_user_password(current_user.id, password_change.current_password,
                                                password_change.new_password)
    except ValueError as e:
        raise GeneralException(ErrorStatus.INVALID_INPUT)

    return ApiResponse.on_success()


@router.get("/users/me/password/check",
            response_model=ApiResponse[bool],
            summary="비밀번호 일치 여부 조회",
            description="비밀번호가 일치하는지 여부를 조회합니다.")
@handle_exceptions(bool)
async def check_password(
        password: str,
        current_user: User = Depends(get_current_user),
        user_service: UserService = Depends(UserService)
):
    flag = await user_service.check_password(password, current_user)
    return flag


@router.patch("/users/deactivate",
              response_model=ApiResponse,
              summary="회원 비활성화",
              description="유저의 상태를 비활성화 시킵니다.")
@handle_exceptions()
async def deactivate_user(current_user: User = Depends(get_current_user),
                          user_service: UserService = Depends(UserService)):
    await user_service.deactivate_user(current_user)
    return ApiResponse.on_success()


@router.patch("/users/activate",
              response_model=ApiResponse,
              summary="회원 활성화",
              description="유저의 상태를 활성화 합니다.")
@handle_exceptions()
async def activate_user(current_user: User = Depends(get_current_user),
                        user_service: UserService = Depends(UserService)):
    await user_service.activate_user(current_user)
    return ApiResponse.on_success()


@router.get("/users/clients/check",
            response_model=ApiResponse[bool],
            summary="유저 거래처 생성 여부 조회",
            description="유저가 거래처를 생성 했는지 여부를 조회 합니다.")
@handle_exceptions(bool)
async def check_clients(current_user: User = Depends(get_current_user), user_service: UserService = Depends(UserService)):
    result = await user_service.check_client_create(current_user)
    return ApiResponse.on_success(result)