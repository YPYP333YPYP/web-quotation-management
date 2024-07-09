from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_current_user
from core.decorator.decorator import handle_exceptions
from core.response.api_response import ApiResponse
from core.response.code.error_status import ErrorStatus
from core.response.code.success_status import SuccessStatus
from core.response.handler.exception_handler import GeneralException
from core.security import create_access_token
from models.user import User
from schemas.user import UserCreate, UserInDB
from schemas.auth import Token, PasswordChange
from service.user import UserService

router = APIRouter(tags=["auth"])


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
    token_info = Token(access_token=access_token, token_type="bearer")
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
            response_model=ApiResponse[UserInDB],
            summary="내 정보 조회",
            description="내 정보를 조회 합니다.")
@handle_exceptions(UserInDB)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


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


@router.patch("/users/deactivate",
              response_model=ApiResponse,
              summary="회원 비활성화",
              description="유저의 상태를 비활성화 시킵니다.")
@handle_exceptions()
async def deactivate_user(current_user: User = Depends(get_current_user),
                          user_service: UserService = Depends(UserService)):
    await user_service.deactivate_user(current_user)
    return ApiResponse.on_success()
