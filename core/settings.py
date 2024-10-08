from pydantic_settings import BaseSettings


class JwtTokenSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        extra = "ignore"


class MySQLSettings(BaseSettings):
    MYSQL_URI: str
    DB_NAME: str

    class Config:
        env_file = ".env"
        extra = "ignore"


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"
        extra = "ignore"