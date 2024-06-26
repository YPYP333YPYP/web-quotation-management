from dotenv import load_dotenv
import os

from core.settings import MySQLSettings, JwtTokenSettings

load_dotenv()

mysql_settings = MySQLSettings(
    MYSQL_URI=os.getenv('MYSQL_URI'),
    DB_NAME=os.getenv('DB_NAME')
)


jwt_settings = JwtTokenSettings(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    ALGORITHM=os.getenv('ALGORITHM'),
    ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
)

