import os

from dotenv import load_dotenv

from core.settings import MySQLSettings, JwtTokenSettings, RedisSettings

load_dotenv()

mysql_settings = MySQLSettings(
    MYSQL_URI=os.getenv('MYSQL_URI'),
    DB_NAME=os.getenv('DB_NAME')
)


jwt_settings = JwtTokenSettings(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    ALGORITHM=os.getenv('ALGORITHM'),
    ACCESS_TOKEN_EXPIRE_MINUTES=30,
    REFRESH_TOKEN_EXPIRE_MINUTES=120
)


redis_settings = RedisSettings(
    REDIS_HOST=os.getenv('REDIS_HOST'),
    REDIS_PORT=int(os.getenv('REDIS_PORT'))
)

