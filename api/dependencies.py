from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from core.config import jwt_settings
from fastapi import Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

from models import User
from service.user import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(access_token=Security(APIKeyHeader(name="access-token"))):
    return access_token


async def get_current_user(
    token: str = Depends(verify_token),
    # token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(UserService)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user