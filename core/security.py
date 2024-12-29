from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from core.config import jwt_settings
from core.response.code.error_status import ErrorStatus
from core.response.handler.exception_handler import GeneralException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
        return payload
    except JWTError:
        raise GeneralException(ErrorStatus.INVALID_TOKEN)


def refresh_access_token(refresh_token: str) -> str:
    payload = verify_refresh_token(refresh_token)
    new_access_token = create_access_token(data={"sub": payload["sub"]})
    return new_access_token


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,  jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
    return encoded_jwt