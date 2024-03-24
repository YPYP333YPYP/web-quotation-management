from dotenv import load_dotenv
import os

from core.settings import MySQLSettings

load_dotenv()

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

mysql_settings = MySQLSettings(
    MYSQL_USER=DB_USERNAME,
    MYSQL_PASSWORD=DB_PASSWORD,
    MYSQL_SERVER=DB_HOST,
    MYSQL_PORT=DB_PORT,
    MYSQL_DB=DB_NAME
)
