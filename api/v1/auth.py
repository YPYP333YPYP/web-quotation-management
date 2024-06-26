from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_current_user
from core.security import create_access_token
from models.user import User
from schemas.user import UserCreate, UserInDB, Token
from service.user import UserService

router = APIRouter(tags=["auth"])


@router.post("/token",
             response_model=Token,
             summary="액세스 토큰 발급",
             description="사용자 로그인 시 토큰을 발급합니다.")
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends()
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users",
             response_model=UserInDB,
             summary="유저 회원 가입",
             description="사용자 정보를 받아 회원 가입을 진행합니다.")
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends()
):
    db_user = await user_service.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_service.create_user(user)


@router.get("/users/me",
            response_model=UserInDB,
            summary="내 정보 조회",
            description="내 정보를 조회 합니다.")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user