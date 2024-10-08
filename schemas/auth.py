from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str