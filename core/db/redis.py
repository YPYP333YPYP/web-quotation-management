import redis.asyncio as redis
from dotenv import load_dotenv

from core.config import redis_settings

redis_client = redis.from_url(f"redis://{redis_settings.REDIS_HOST}", decode_responses=True)
load_dotenv()
